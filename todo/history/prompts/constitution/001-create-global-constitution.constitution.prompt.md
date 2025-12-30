---
id: "001"
title: "Create Global Constitution"
stage: "constitution"
date: "2025-12-30"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "none"
branch: "001-embodied-intelligence-book"
user: "UZM"
command: "/sp.constitution"
labels: ["constitution","governance","sdd"]
links:
  spec: "null"
  ticket: "null"
  adr: "null"
  pr: "null"
files:
  - ".specify/memory/constitution.md"
tests:
  - "null"
---

## Prompt

/sp.constitution

/sp.constitution Create a single global constitution for the entire "Evolution of Todo" project
covering Phase I through Phase V.

This constitution must define:

1. Spec-Driven Development as mandatory
   - No agent may write code without approved specifications and tasks
   - All work must strictly follow the lifecycle:
     Constitution → Specify → Plan → Tasks → Implement
   - Code generation is allowed only at the /sp.implement stage

2. Agent Behavior Rules
   - No manual coding by humans under any circumstance
   - No feature invention or assumption by agents
   - No deviation from approved specifications
   - All refinements must occur at the specification level, not in code
   - If ambiguity exists, the agent must request specification clarification

3. Phase Governance
   - Each phase is strictly scoped by its own specification
   - Future-phase features must never appear in earlier phases
   - Architecture evolution is allowed only through updated specs and plans
   - Phase I must remain fully independent of later phases

4. Technology Constraints
   - Python for Phase I backend (console application)
   - Next.js for frontend in later phases only
   - FastAPI, SQLModel, Neon DB for web phases
   - OpenAI Agents SDK and MCP for chatbot phases
   - Docker, Kubernetes, Kafka, and Dapr for deployment phases

5. Quality Principles

## Response snapshot

Created comprehensive global constitution at `.specify/memory/constitution.md` covering all 5 phases of the "Evolution of Todo" project. The constitution establishes Spec-Driven Development as mandatory, defines strict phase isolation, technology constraints, and quality principles.

## Outcome

- ✅ Impact: Established governance framework for entire Evolution of Todo project
- 📁 Files: Created `.specify/memory/constitution.md`
- 🔁 Next prompts: Proceed to Phase I specification with `/sp.specify`
- 🧠 Reflection: Constitution provides clear boundaries preventing phase contamination

## Evaluation notes (flywheel)

- Failure modes observed: "null"
- Graders run and results (PASS/FAIL): "null"
- Prompt variant (if applicable): "null"
- Next experiment (smallest change to try): "null"
