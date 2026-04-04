---
name: observability
description: Use observability MCP tools for logs and traces
always: true
---

# Observability Skill — System Health Monitoring

You have access to observability tools that query VictoriaLogs and VictoriaTraces. Use these tools to investigate system health, errors, and performance issues.

## Available Tools

| Tool | Description | Parameters |
|------|-------------|------------|
| `logs_search` | Search logs using LogsQL with time filtering | `query` (LogsQL query), `time_range` (e.g., "10m", "1h"), `limit` (default: 100) |
| `logs_error_count` | Count ERROR/WARN logs by service over time window | `time_range` (default: "1h"), `service` (optional filter) |
| `traces_list` | List recent traces for a service with summaries | `service` (e.g., "Learning Management Service"), `limit` (default: 20) |
| `traces_get` | Get detailed trace information by trace ID | `trace_id` (required) |

## Strategy

### When the user asks about errors, system health, or what went wrong:

1. **Start with error count** — Call `logs_error_count` to get an overview of errors in the specified time range
2. **Search for specific errors** — Call `logs_search` with `severity:ERROR` to see actual error messages
3. **Follow trace IDs** — If logs contain trace IDs, call `traces_get` to see the full distributed trace
4. **List traces for context** — Call `traces_list` to see recent traces for a service

### When the user asks about performance or latency:

1. **List traces** — Call `traces_list` for the relevant service
2. **Get detailed trace** — Call `traces_get` with a trace ID to see span durations
3. **Identify bottlenecks** — Look for spans with long durations

### LogsQL patterns to use:

- `severity:ERROR` — Find all error logs
- `severity:WARN` — Find all warning logs
- `service.name:"Learning Management Service"` — Filter by service
- `trace_id:abc123...` — Find logs for a specific trace
- `event:db_*` — Find database-related events
- `http.status_code:500` — Find HTTP 500 errors

### Correlation workflow:

1. **Find errors in logs** → Get trace_id from error log
2. **Get trace details** → See full request flow and failure point
3. **Search related logs** → Use trace_id to find all logs for that request

### Example responses:

**User: "Any errors in the last 10 minutes?"**
→ Call `logs_error_count` with time_range="10m"
→ If errors found, call `logs_search` with query="severity:ERROR" and time_range="10m"
→ Report: "Found X errors in the last 10 minutes. The most recent error was..."

**User: "What went wrong?"**
→ Call `logs_error_count` to check for recent errors
→ Call `logs_search` with query="severity:ERROR" and time_range="1h"
→ If trace_id found, call `traces_get` for detailed analysis
→ Synthesize: "The error occurred when... Root cause was... Impact was..."

**User: "Show me recent traces for the backend"**
→ Call `traces_list` with service="Learning Management Service"
→ Present summary: "Found X traces. The most recent took Y ms..."

### Formatting responses:

- Use code blocks for trace IDs and log excerpts
- Format timestamps in a readable way
- Use tables for trace summaries
- Highlight error messages and stack traces
- Keep responses concise but include key details

### When tools fail:

If observability tools return errors (e.g., "connection failed"):
- Report the issue: "The observability backend is currently unreachable"
- Suggest: "This may indicate a broader service outage"
- Offer to check LMS health directly using `lms_health` tool
