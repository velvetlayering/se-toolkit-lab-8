# Lab 8 — Report

Paste your checkpoint evidence below. Add screenshots as image files in the repo and reference them with `![description](path)`.

## Task 1A — Bare agent

The agentic loop is the fundamental cycle that an autonomous AI agent follows to accomplish tasks. It's the core reasoning and action pattern that
enables agents to work independently toward goals.

The Basic Loop

The agentic loop typically consists of these stages:

1 Perceive — Gather information about the current state (from the environment, user input, tools, memory, etc.)
2 Reason/Plan — Analyze the situation, decide what to do next, and formulate a plan or action
3 Act — Execute the chosen action (call a tool, modify a file, send a message, etc.)
4 Observe — Receive feedback from the action (success, failure, output, new state)
5 Repeat — Continue the loop until the goal is achieved or a stopping condition is met

Visual Representation

┌─────────────┐
│ Perceive │
└──────┬──────┘
│
▼
┌─────────────┐
│ Reason │
└──────┬──────┘
│
▼
┌─────────────┐
│ Act │
└──────┬──────┘
│
▼
┌─────────────┐
│ Observe │
└──────┬──────┘
│
└──────→ (back to Perceive)

Why It Matters

• Autonomy: The loop enables agents to work without constant human guidance
• Adaptability: Agents can adjust their approach based on feedback
• Complex Tasks: Multi-step problems can be solved iteratively
• Self-Correction: Errors can be detected and corrected in subsequent iterations

Example in Practice

When you asked me this question, I went through the agentic loop:

1 Perceive: Read your question "What is the agentic loop?"
2 Reason: Determined this is a knowledge question I can answer directly
3 Act: Formulated and delivered this explanation
4 Observe: Awaiting your response or follow-up questions

More complex tasks (like coding, research, or multi-file operations) may involve many iterations of this loop with tool calls in the Act phase.

---

The agentic loop is the core reasoning cycle that enables autonomous AI agents to accomplish tasks independently. It's a continuous feedback loop of
perception, decision-making, and action.

Core Stages

Stage Description
───────────────────────────────────────────────────────────────────────────────
Perceive Gather information from the environment, user input, tools, or memory
Reason Analyze the situation, plan next steps, make decisions
Act Execute actions (call tools, modify files, send messages, etc.)
Observe Receive feedback from actions (results, errors, new state)
Repeat Continue until goal is achieved or stopping condition is met

Simple Diagram

Perceive → Reason → Act → Observe → (loop back)

Why It's Important

• Autonomy — Agents can work without constant human guidance
• Adaptability — Agents adjust based on feedback and changing conditions
• Complex Problem Solving — Multi-step tasks are handled iteratively
• Self-Correction — Errors can be detected and fixed in subsequent iterations

Example

When I answer your questions, I'm running the agentic loop:

1 Perceive: Read your question
2 Reason: Determine what information you need
3 Act: Generate and deliver a response
4 Observe: Wait for your feedback or follow-up

For more complex tasks (coding, research, file operations), the loop may iterate many times with different tool calls until the task is complete.

```
What is the agentic loop?
- Not run yet

What labs are available in our LMS?
- Not run yet
```

## Task 1B — Agent with LMS tools

The LMS backend is healthy, but there are currently no labs available (item count: 0). This could mean:

1 No labs have been configured yet
2 The labs haven't been synced to the system

Would you like me to trigger the LMS sync pipeline to see if that loads any labs?

---

Yes, the LMS backend is healthy. It's currently running with 0 items in the system.

## Task 1C — Skill prompt

## Task 1C — Skill prompt

I'll help you see the scores. First, let me check what labs are available.

I can see there are 8 labs available. Since you didn't specify which lab, let me show you the pass rates for all labs. I'll check each one:

Here are the scores (average scores by task) for all labs:

**Lab 01 – Products, Architecture & Roles**
| Task | Avg Score | Attempts |
|------|-----------|----------|
| Lab setup | 84.3% | 3,429 |
| Task 0: Practice the Git workflow | 64.5% | 306 |
| Task 1: Product & architecture description | 55.1% | 161 |
| Task 2: Roles and skills mapping | 49.8% | 83 |
| Optional: Resolve a merge conflict | 34.6% | 13 |

**Lab 02 – Run, Fix, and Deploy a Backend Service**
| Task | Avg Score | Attempts |
|------|-----------|----------|
| Task 1: Run the web server | 67.9% | 210 |
| Task 2: Identify, report, and fix a bug | 66.7% | 216 |
| Task 4: Deploy the web server to the VM | 56.2% | 84 |

[Additional labs truncated for brevity - agent showed detailed scores for all 8 labs]

**Lab 08**
No data available yet.

Would you like me to show completion rates, top learners, or group performance for any specific lab?

## Task 2A — Deployed agent

<!-- Paste a short nanobot startup log excerpt showing the gateway started inside Docker -->

## Task 2B — Web client

<!-- Screenshot of a conversation with the agent in the Flutter web app -->

## Task 3A — Structured logging

<!-- Paste happy-path and error-path log excerpts, VictoriaLogs query screenshot -->

## Task 3B — Traces

<!-- Screenshots: healthy trace span hierarchy, error trace -->

## Task 3C — Observability MCP tools

<!-- Paste agent responses to "any errors in the last hour?" under normal and failure conditions -->

## Task 4A — Multi-step investigation

<!-- Paste the agent's response to "What went wrong?" showing chained log + trace investigation -->

## Task 4B — Proactive health check

<!-- Screenshot or transcript of the proactive health report that appears in the Flutter chat -->

## Task 4C — Bug fix and recovery

<!-- 1. Root cause identified
     2. Code fix (diff or description)
     3. Post-fix response to "What went wrong?" showing the real underlying failure
     4. Healthy follow-up report or transcript after recovery -->
