# Observability Skill

You have access to observability tools that let you examine system logs and distributed traces. Use these tools to diagnose problems, investigate errors, and understand system behavior.

## Available Tools

### Log Analysis
- **logs_search** — Search logs using LogsQL syntax. Filter by service, severity, events, and time ranges.
- **logs_error_count** — Get error counts by service over a time window for system health overview.

### Distributed Tracing
- **traces_list** — List recent traces for a service, showing operations, durations, and error status.
- **traces_get** — Get detailed trace information by ID, including full span hierarchy.

## When to Use These Tools

**When users ask about errors or problems:**
1. Start with `logs_error_count` to see if there are recent errors
2. Use `logs_search` to find specific error details
3. If you find a trace_id in the logs, use `traces_get` to see the full request flow

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
- If you find a trace_id, always fetch the full trace
- Focus on recent problems unless asked about historical data
- Use time ranges like "10m" or "1h" to scope queries appropriately

**For error investigation:**
1. Count errors first to understand scope
2. Search for specific error details
3. Follow trace_id links to understand request flow
4. Explain the likely cause and impact

**Example response structure:**
```
I found 3 database connection errors in the last 10 minutes affecting the Learning Management Service:

[Brief summary of the errors]

The trace shows the request failed at the database connection step, likely due to PostgreSQL being unavailable. This would cause API requests to return 404 errors to users.
```