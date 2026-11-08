---
name: sdcu
description: "The complete SDCU Suite for AI coding agents: (SD) System Design & Resilience Auditor, (C) Code Context Graph Memory Cache, and (U) UI Craft & Unslopping Engine. Solves AI code amnesia, prevents architectural collapse, and eliminates vibecoded frontend slop."
trigger: /sdcu
---

# /sdcu: System Design · Context Graph · UI Craft

The **SDCU** suite is the unified engineering backbone for coders using AI. It guarantees that AI coding assistants do not generate vulnerable, disconnected, or visually sloppy applications.

```
       ┌─────────────────────────────────────────────────────────────┐
       │                            SDCU                             │
       │    The Universal AI Pair Programming & Architecture Suite   │
       └──────────────────────────────┬──────────────────────────────┘
                                      │
         ┌────────────────────────────┼────────────────────────────┐
         ▼                            ▼                            ▼
   ┌───────────┐                ┌───────────┐                ┌───────────┐
   │    SD     │                │     C     │                │     U     │
   │  System   │                │  Context  │                │    UI     │
   │  Design   │                │   Graph   │                │   Craft   │
   └─────┬─────┘                └─────┬─────┘                └─────┬─────┘
         │                            │                            │
   • 20 Checkpoints             • In-Memory Graph            • 9-Pass Redline
   • 17 SD Pillars              • AST Relationship Map       • Quiet Chrome
   • Cache-to-DB Playbook       • BFS/DFS Path Tracing       • Bespoke Identity
   • SingleFlight & Jitter      • GraphRAG Querying          • Visual Snapshots
```

---

## When to Run SDCU

| Phase | What SDCU Does | Sub-Skill |
|---|---|---|
| **Before Planning / Coding** | Extracts full codebase AST graph, discovers call relationships, prevents hallucinated architectural context. | `/sdcu-c` |
| **During Architecture & DB Design** | Enforces the 20 Security & Scale Checkpoints, 17 System Design Pillars, and the 6 Cache-to-DB resilience mechanisms. | `/sdcu-sd` |
| **During Frontend & UI Development** | Performs the 9-pass design review to remove generic purple gradients, emoji spam, and misaligned grids. | `/sdcu-u` |
| **Full Health Check** | Runs an end-to-end audit: System Design linter + Context Graph analysis + UI slop audit. | `/sdcu audit` |

---

## Quick Reference Commands

```bash
# Run full automated audit on current project
sdcu audit

# Build or refresh the code context graph
sdcu graph build

# Query code context via GraphRAG
sdcu graph query "How does authentication flow to the database?"

# Trace execution path between two symbols
sdcu graph path "<SourceSymbol>" "<TargetSymbol>"

# Audit backend & database resilience against the 20 checkpoints
sdcu sd audit

# Generate production resilience templates (SingleFlight, CircuitBreaker, Jitter)
sdcu sd template [circuit-breaker | singleflight | jittered-cache]

# Audit frontend code for AI slop and run the 9-pass design review
sdcu ui audit
```

---

## Integration with Coding Assistants

### For Antigravity / Claude Code / Cursor / Codex
Simply add the `sdcu` skills to your agent configuration:
```bash
# Clone the repository
git clone https://github.com/<your-username>/sdcu.git

# Link skills into your agent directory (e.g. for Claude Code or Antigravity)
cp -r sdcu/skills/* ~/.gemini/config/skills/ # or ~/.claude/skills/
```

### Agent Autonomous Protocol
When working on any repository with `sdcu` installed:
1. **Never guess dependencies**: Query the context graph (`sdcu graph query` or read `.sdcu/graph.json`).
2. **Never commit security/scale flaws**: Check the proposed changes against the 20 checkpoints in `skills/sdcu-sd/references/20-checkpoints.md`.
3. **Never write vibecoded UI**: Apply the 9 design passes in `skills/sdcu-u/SKILL.md` before finalizing frontend code.
