"""
MCP Server for Observability Tools.
Provides access to VictoriaLogs and VictoriaTraces for the agent.
"""

import asyncio
import logging
import sys
from typing import Any, Sequence

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Resource, Tool, TextContent, ImageContent, EmbeddedResource
from pydantic import AnyUrl

from .observability import ObservabilityClient

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create global client instance
obs_client = ObservabilityClient()

# Create the server instance
server = Server("mcp-obs")


@server.list_tools()
async def handle_list_tools() -> list[Tool]:
    """List available observability tools."""
    return [
        Tool(
            name="logs_search",
            description="Search logs using LogsQL query syntax. Supports filtering by service, severity, events, and time ranges.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "LogsQL query string (e.g., 'service.name:\"Learning Management Service\" AND severity:ERROR')",
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of results to return (default: 50, max: 1000)",
                        "default": 50,
                        "minimum": 1,
                        "maximum": 1000,
                    },
                    "time_range": {
                        "type": "string",
                        "description": "Time range for the search (e.g., '1h', '10m', '24h'). If not specified, searches all available logs.",
                        "default": None,
                    },
                },
                "required": ["query"],
            },
        ),
        Tool(
            name="logs_error_count",
            description="Count errors by service over a specified time window. Useful for getting an overview of system health.",
            inputSchema={
                "type": "object",
                "properties": {
                    "time_range": {
                        "type": "string",
                        "description": "Time range to count errors over (e.g., '1h', '10m', '24h')",
                        "default": "1h",
                    }
                },
                "required": [],
            },
        ),
        Tool(
            name="traces_list",
            description="List recent traces for a specific service. Shows trace summaries with operation names, durations, and error status.",
            inputSchema={
                "type": "object",
                "properties": {
                    "service": {
                        "type": "string",
                        "description": "Service name to list traces for (e.g., 'Learning Management Service')",
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of traces to return (default: 20, max: 100)",
                        "default": 20,
                        "minimum": 1,
                        "maximum": 100,
                    },
                },
                "required": ["service"],
            },
        ),
        Tool(
            name="traces_get",
            description="Get detailed information for a specific trace by ID. Shows the complete span hierarchy and timing information.",
            inputSchema={
                "type": "object",
                "properties": {
                    "trace_id": {
                        "type": "string",
                        "description": "Trace ID to retrieve (32-character hexadecimal string)",
                    }
                },
                "required": ["trace_id"],
            },
        ),
    ]


@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict[str, Any] | None
) -> list[TextContent]:
    """Handle tool calls for observability operations."""
    if arguments is None:
        arguments = {}

    try:
        if name == "logs_search":
            query = arguments["query"]
            limit = arguments.get("limit", 50)
            time_range = arguments.get("time_range")

            logs = await obs_client.search_logs(query, limit, time_range)

            if not logs:
                return [
                    TextContent(type="text", text=f"No logs found for query: {query}")
                ]

            # Format the results
            result_text = f"Found {len(logs)} log entries:\n\n"
            for i, log in enumerate(logs[:10]):  # Show first 10 for readability
                timestamp = log.get("_time", "unknown")
                severity = log.get("severity", "unknown")
                service = log.get("service.name", "unknown")
                message = log.get("_msg", "")
                event = log.get("event", "")
                trace_id = log.get("trace_id", "")

                result_text += f"{i + 1}. {timestamp} [{severity}] {service}\n"
                result_text += f"   Event: {event}\n"
                if message and message != event:
                    result_text += f"   Message: {message}\n"
                if trace_id:
                    result_text += f"   Trace ID: {trace_id}\n"
                result_text += "\n"

            if len(logs) > 10:
                result_text += f"... and {len(logs) - 10} more entries\n"

            return [TextContent(type="text", text=result_text)]

        elif name == "logs_error_count":
            time_range = arguments.get("time_range", "1h")

            error_counts = await obs_client.count_errors_by_service(time_range)

            if not error_counts:
                return [
                    TextContent(
                        type="text", text=f"No errors found in the last {time_range}."
                    )
                ]

            result_text = f"Error counts by service (last {time_range}):\n\n"
            for service, count in sorted(
                error_counts.items(), key=lambda x: x[1], reverse=True
            ):
                result_text += f"- {service}: {count} errors\n"

            total_errors = sum(error_counts.values())
            result_text += f"\nTotal errors: {total_errors}"

            return [TextContent(type="text", text=result_text)]

        elif name == "traces_list":
            service = arguments["service"]
            limit = arguments.get("limit", 20)

            traces = await obs_client.list_traces(service, limit)

            if not traces:
                return [
                    TextContent(
                        type="text", text=f"No traces found for service: {service}"
                    )
                ]

            result_text = f"Recent traces for {service} (last {len(traces)}):\n\n"
            for trace in traces:
                trace_id = trace["traceID"]
                operation = trace["operationName"]
                duration_ms = trace["duration"] / 1000  # Convert to milliseconds
                span_count = trace["spanCount"]
                has_errors = "❌" if trace["hasErrors"] else "✅"

                result_text += f"{has_errors} {trace_id[:8]}... - {operation}\n"
                result_text += (
                    f"    Duration: {duration_ms:.2f}ms, Spans: {span_count}\n\n"
                )

            return [TextContent(type="text", text=result_text)]

        elif name == "traces_get":
            trace_id = arguments["trace_id"]

            trace = await obs_client.get_trace(trace_id)

            if not trace:
                return [TextContent(type="text", text=f"Trace not found: {trace_id}")]

            spans = trace.get("spans", [])
            processes = trace.get("processes", {})

            # Find root span
            root_span = None
            for span in spans:
                if not span.get("references"):
                    root_span = span
                    break

            result_text = f"Trace {trace_id}:\n\n"

            if root_span:
                operation = root_span.get("operationName", "unknown")
                duration_ms = root_span.get("duration", 0) / 1000
                result_text += f"Operation: {operation}\n"
                result_text += f"Total Duration: {duration_ms:.2f}ms\n"
                result_text += f"Span Count: {len(spans)}\n\n"

            # Show span hierarchy (simplified)
            result_text += "Span Hierarchy:\n"
            for i, span in enumerate(spans[:10]):  # Show first 10 spans
                operation = span.get("operationName", "unknown")
                duration_ms = span.get("duration", 0) / 1000
                span_id = span.get("spanID", "")

                # Check if this is a child span
                is_child = bool(span.get("references"))
                indent = "  " if is_child else ""

                result_text += f"{indent}- {operation} ({duration_ms:.2f}ms)\n"

            if len(spans) > 10:
                result_text += f"... and {len(spans) - 10} more spans\n"

            return [TextContent(type="text", text=result_text)]

        else:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]

    except Exception as e:
        logger.error(f"Error in {name}: {str(e)}")
        return [TextContent(type="text", text=f"Error executing {name}: {str(e)}")]


async def main():
    """Main entry point for the MCP server."""
    async with stdio_server() as (read_stream, write_stream):
        init_options = server.create_initialization_options()
        await server.run(read_stream, write_stream, init_options)


if __name__ == "__main__":
    asyncio.run(main())
