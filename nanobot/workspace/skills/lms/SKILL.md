---
name: lms
description: Use LMS MCP tools for live course data
always: true
---

# LMS Skill — Learning Management System

You have access to the LMS backend through MCP tools. Use these tools to answer questions about labs, learners, scores, and completion rates.

## Available Tools

| Tool | Description | Parameters |
|------|-------------|------------|
| `lms_health` | Check if the LMS backend is healthy and report the item count | None |
| `lms_labs` | List all labs available in the LMS | None |
| `lms_learners` | List all learners registered in the LMS | None |
| `lms_pass_rates` | Get pass rates (avg score and attempt count per task) for a lab | `lab` (required): Lab identifier, e.g. 'lab-04' |
| `lms_timeline` | Get submission timeline (date + submission count) for a lab | `lab` (required): Lab identifier |
| `lms_groups` | Get group performance (avg score + student count per group) for a lab | `lab` (required): Lab identifier |
| `lms_top_learners` | Get top learners by average score for a lab | `lab` (required), `limit` (optional, default 5) |
| `lms_completion_rate` | Get completion rate (passed / total) for a lab | `lab` (required): Lab identifier |
| `lms_sync_pipeline` | Trigger the LMS sync pipeline. May take a moment | None |

## Strategy

### When the user asks about labs, scores, pass rates, completion, groups, timeline, or top learners:

1. **If a lab is specified**: Use the appropriate tool directly with the provided lab identifier.

2. **If no lab is specified**:
   - First call `lms_labs` to get the list of available labs
   - If multiple labs exist, ask the user to choose one
   - Present lab choices using the lab title as the label (e.g., "Lab 01 – Products, Architecture & Roles")
   - Wait for the user to select a lab before proceeding

### When the user asks "what can you do?":

Explain your current capabilities clearly:
- You can query the LMS backend for information about labs, learners, scores, and completion rates
- You can check system health
- You can trigger the sync pipeline if data seems outdated
- You need a lab identifier for detailed queries (pass rates, timeline, groups, top learners, completion rate)

### Formatting responses:

- Format numeric results nicely: percentages with `%`, counts as plain numbers
- Use tables for structured data (scores, timelines, groups)
- Keep responses concise but informative
- When showing scores or pass rates, include both the average score percentage and attempt count

### Example workflows:

**User: "Show me the scores"**
→ Call `lms_labs` first
→ If multiple labs: "I found 8 labs. Which one would you like to see scores for?"
→ After user selects: Call `lms_pass_rates` with the lab identifier
→ Format results as a table

**User: "Which lab has the lowest pass rate?"**
→ Call `lms_labs` to get all labs
→ Call `lms_pass_rates` for each lab
→ Compare and report the lowest

**User: "Is the LMS backend healthy?"**
→ Call `lms_health`
→ Report the status and item count

**User: "Trigger a sync"**
→ Call `lms_sync_pipeline`
→ Inform the user it may take a moment
