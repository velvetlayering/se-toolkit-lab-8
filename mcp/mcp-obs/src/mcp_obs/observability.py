"""
Observability tools for querying VictoriaLogs and VictoriaTraces APIs.
"""

import asyncio
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional
import httpx
import json


class ObservabilityClient:
    """Client for interacting with VictoriaLogs and VictoriaTraces APIs."""

    def __init__(
        self,
        logs_base_url: str = "http://localhost:42010",
        traces_base_url: str = "http://localhost:42011",
    ):
        self.logs_base_url = logs_base_url
        self.traces_base_url = traces_base_url

    async def search_logs(
        self, query: str, limit: int = 50, time_range: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Search logs using LogsQL query syntax.

        Args:
            query: LogsQL query string (e.g., 'service.name:"Learning Management Service" AND severity:ERROR')
            limit: Maximum number of results to return
            time_range: Time range (e.g., '1h', '10m', '24h')

        Returns:
            List of log entries as dictionaries
        """
        # Build the query with time range if provided
        full_query = query
        if time_range:
            full_query = f"_time:{time_range} {query}"

        url = f"{self.logs_base_url}/select/logsql/query"
        params = {"query": full_query, "limit": limit}

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, params=params, timeout=30.0)
                response.raise_for_status()

                # Parse NDJSON response (each line is a JSON object)
                logs = []
                for line in response.text.strip().split("\n"):
                    if line:
                        try:
                            logs.append(json.loads(line))
                        except json.JSONDecodeError:
                            continue

                return logs
            except Exception as e:
                raise Exception(f"Failed to search logs: {str(e)}")

    async def count_errors_by_service(self, time_range: str = "1h") -> Dict[str, int]:
        """
        Count errors by service over a time window.

        Args:
            time_range: Time range (e.g., '1h', '10m', '24h')

        Returns:
            Dictionary mapping service names to error counts
        """
        query = f"_time:{time_range} severity:ERROR"

        try:
            logs = await self.search_logs(query, limit=1000)
            error_counts = {}

            for log in logs:
                service_name = log.get("service.name", "unknown")
                error_counts[service_name] = error_counts.get(service_name, 0) + 1

            return error_counts
        except Exception as e:
            raise Exception(f"Failed to count errors: {str(e)}")

    async def list_traces(self, service: str, limit: int = 20) -> List[Dict[str, Any]]:
        """
        List recent traces for a service using Jaeger-compatible API.

        Args:
            service: Service name to query traces for
            limit: Maximum number of traces to return

        Returns:
            List of trace summaries
        """
        url = f"{self.traces_base_url}/select/jaeger/api/traces"
        params = {"service": service, "limit": limit}

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, params=params, timeout=30.0)
                response.raise_for_status()

                data = response.json()
                traces = data.get("data", [])

                # Extract trace summaries
                trace_summaries = []
                for trace in traces:
                    trace_id = trace.get("traceID", "")
                    spans = trace.get("spans", [])

                    # Find root span for operation name and duration
                    root_span = None
                    for span in spans:
                        if not span.get("references"):  # Root span has no references
                            root_span = span
                            break

                    if root_span:
                        summary = {
                            "traceID": trace_id,
                            "operationName": root_span.get("operationName", "unknown"),
                            "duration": root_span.get("duration", 0),
                            "startTime": root_span.get("startTime", 0),
                            "spanCount": len(spans),
                            "hasErrors": any(
                                tag.get("key") == "error" and tag.get("value") == True
                                for span in spans
                                for tag in span.get("tags", [])
                            ),
                        }
                        trace_summaries.append(summary)

                return trace_summaries
            except Exception as e:
                raise Exception(f"Failed to list traces: {str(e)}")

    async def get_trace(self, trace_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a specific trace by ID.

        Args:
            trace_id: Trace ID to retrieve

        Returns:
            Full trace data or None if not found
        """
        url = f"{self.traces_base_url}/select/jaeger/api/traces/{trace_id}"

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, timeout=30.0)
                response.raise_for_status()

                data = response.json()
                traces = data.get("data", [])

                return traces[0] if traces else None
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 404:
                    return None
                raise Exception(f"Failed to get trace: {str(e)}")
            except Exception as e:
                raise Exception(f"Failed to get trace: {str(e)}")
