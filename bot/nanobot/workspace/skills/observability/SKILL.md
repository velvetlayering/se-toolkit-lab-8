# Observability Skill

You have access to observability tools that let you examine system logs and distributed traces. Use these tools to diagnose problems, investigate errors, and understand system behavior.

## Available Tools

### Log Analysis
- **logs_search** — Search logs using LogsQL syntax. Filter by service, severity, events, and time ranges.
- **logs_error_count** — Get error counts by service over a time window for system health overview.

### Distributed Tracing
- **traces_list** — List recent traces for a service, showing operations, durations, and error status.
- **traces_get** — Get detailed trace information by ID, including full span hierarchy.

## Investigation Workflows

### Multi-Step Investigation ("What went wrong?" / "Check system health")
When users ask about system problems, follow this systematic investigation:

1. **Start broad** — `logs_error_count` with recent time window (5-10m) to assess error scope
2. **Focus search** — `logs_search` for ERROR severity on the most affected service
3. **Extract trace ID** — Look for `trace_id` field in error logs
4. **Deep dive** — `traces_get` with the trace ID to see full request flow and failure points
5. **Synthesize findings** — Provide one coherent summary citing both log and trace evidence

### Health Monitoring
For proactive system monitoring:
1. Use `logs_error_count` with short time windows (2-5m)
2. If errors found, investigate with `logs_search` and `traces_get`
3. Report concisely: either "system healthy" or brief error summary

### When to Use These Tools

**When users ask about errors or problems:**
- **"What went wrong?"** → Full multi-step investigation workflow
- **"Any errors recently?"** → `logs_error_count` + targeted `logs_search`
- **"Check system health"** → Health monitoring workflow

**When investigating performance issues:**
1. Use `traces_list` to see recent request durations
2. Use `traces_get` on slow traces to identify bottlenecks

## LogsQL Query Examples

**Find recent errors for a service:**
```
service.name:"Learning Management Service" AND severity:ERROR
```

**Find specific events:**
```
event:db_query AND severity:ERROR
```

**Find logs for a specific trace:**
```
trace_id:abc123def456
```

## Key Fields in Logs

- `service.name` — Service that generated the log
- `severity` — Log level (INFO, WARN, ERROR)
- `event` — Structured event type (request_started, db_query, etc.)
- `trace_id` — Links logs to distributed traces
- `_time` — Timestamp
- `_msg` — Log message

## Response Guidelines

**Be concise and actionable:**
- Summarize findings, don't dump raw JSON
- Explain what the errors mean in business terms
- Always correlate logs with traces when trace IDs are available
- Focus on recent problems unless asked about historical data
- Use time ranges like "5m", "10m" or "1h" to scope queries appropriately

**For systematic investigation ("What went wrong?"):**
1. **Count errors** — `logs_error_count` to understand scope and timing
2. **Search details** — `logs_search` for specific error messages and contexts
3. **Follow traces** — `traces_get` with trace_id from logs to see request flow
4. **Correlate evidence** — Mention BOTH log evidence AND trace evidence in your summary
5. **Name root cause** — Identify the failing service and specific operation

**Example investigation response:**
```
I found 3 database connection errors in the last 10 minutes affecting the Learning Management Service.

**Log Evidence:** Error logs show "connection to server at 'postgres:5432' failed" with trace ID 1a2b3c4d.

**Trace Evidence:** Trace 1a2b3c4d shows the HTTP GET /items/ request (45ms) failed during the db.connect span (3ms timeout).

**Root Cause:** PostgreSQL database is unreachable, causing API requests to fail. However, the backend is incorrectly returning 404 "Items not found" instead of the actual database connection error.
```

**For health monitoring:**
- Start each check with `logs_error_count` over the monitoring window
- If no errors: "System looks healthy - no backend errors in the last [X] minutes"
- If errors found: Brief summary with service and error type, investigate with traces if needed