# SDCU
### *System Design · Code Context Graph · UI Craft*

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Node 18+](https://img.shields.io/badge/node-18+-green.svg)](https://nodejs.org/)
[![AI Agents: Antigravity | Claude | Cursor | Codex](https://img.shields.io/badge/AI%20Agents-Ready-purple.svg)](#agent-skills-installation)

> **Cure AI coding amnesia, prevent cascading database stampedes, and eliminate vibecoded frontend slop with a unified open-source engineering suite.**

---

## The Problem With AI-Generated Code

When developers use modern AI coding assistants, agents routinely fail in three predictable ways:

```
❌ The Fragile System (SD)    ❌ Token Amnesia (C)           ❌ Vibecoded Slop (U)
─────────────────────────────  ─────────────────────────────  ─────────────────────────────
• API keys leaked in frontend  • Flat context window loss     • Blinding neon purple glows
• Unindexed N+1 SQL queries    • Cannot trace cross-file      • Emoji badges in buttons
• Cache failure drops DB         call hierarchies             • Robotic marketing buzzwords
• 10k requests stampede DB     • Hallucinates file schemas    • Mismatched 3px margins
```

---

## The SDCU Architecture

**SDCU** unites three battle-tested superpowers into one unified developer tool and multi-agent skill suite:

```
┌────────────────────────────────────────────────────────────────────────┐
│                                  SDCU                                  │
│             Unified CLI & Multi-Agent Architecture Protocol            │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
        ┌───────────────────────────┼───────────────────────────┐
        ▼                           ▼                           ▼
┌───────────────┐           ┌───────────────┐           ┌───────────────┐
│      SD       │           │       C       │           │       U       │
│ System Design │           │ Context Graph │           │   UI Craft    │
│ & Resilience  │           │   & Memory    │           │ & Unslopping  │
├───────────────┤           ├───────────────┤           ├───────────────┤
│ • 20 Checkpts │           │ • Tree-Sitter │           │ • 9-Pass      │
│ • 17 Pillars  │           │ • NetworkX    │           │   Redline     │
│ • Cache-to-DB │           │ • In-Memory   │           │ • Quiet Chrome│
│   Resilience  │           │   Cache       │           │ • Bespoke     │
│ • SingleFlight│           │ • GraphRAG    │           │   Palette     │
│ • Jitter TTL  │           │ • God-Nodes   │           │ • Snapshots   │
└───────────────┘           └───────────────┘           └───────────────┘
```

---

## 1. System Design (SD) Engine

### The 20 Production Guardrails & Checkpoints
1. **Security**: No frontend API keys, strict authentication & RBAC, parameterized SQL queries, XSS sanitization, memory-hard Argon2/bcrypt password hashing, restricted CORS origins, secret leak prevention (`.env`), Redis-backed rate limiting, IDOR prevention, and automated dependency auditing.
2. **Backend & Scale**: Planned database schemas & migrations, indexed queries (zero N+1 loops), multi-tier caching (L1 Memory + L2 Redis), structured error handling, structured JSON logs & OpenTelemetry tracing, and automated backups with zero-downtime rollbacks.
3. **Code Health**: Automated test pyramids, clean modular architecture, regression-guarded prompt edits, and self-documenting debuggability.

### The 17 Core System Design Concepts
Embedded knowledge and verification across:
*Load Balancing · Caching · CDN · API Gateway · Microservices · Monolithic Architecture · Replication · Partitioning/Sharding · Message Queues · Rate Limiting · Consistent Hashing · CAP Theorem · Horizontal Scaling · Vertical Scaling · Fault Tolerance · Circuit Breakers · Event-Driven Architecture.*

### Resilient Cache-to-Database Playbook
Preventing cache failures (like Redis outages) from becoming catastrophic database crashes:

```
Clients (10,000 req/s) ──> [ Redis Cache / Miss ]
                                 │
                                 ▼
                     [ SingleFlight Coalescer ]
                                 │ (Only 1 query in-flight!)
                                 ▼
                     [ Primary Database ]
                                 │ (Shared Result broadcasted to all 10k)
```

1. **Don't Let Every Request Hit the DB**: Trip circuit breakers to fallback responses; shed non-critical traffic.
2. **Add Jittered Cache Expiration**: $\text{TTL} = \text{Base TTL} + \text{Random Jitter}$ to disperse expiration spikes.
3. **Use Request Coalescing (SingleFlight)**: $10,000 \text{ Requests} \longrightarrow 1 \text{ DB Query} \longrightarrow \text{Shared Result}$.
4. **Gradual Cache Warming**: Use background workers to pre-warm hot keys upon cache recovery before opening traffic.
5. **Protect the Database**: Hard caps on DB connection pools, query concurrency ceilings, and backpressure.
6. **Serve Stale Data When Safe**: Stale-While-Revalidate serves instant responses while refreshing asynchronously.

---

## 2. Context Graph (C) Engine

AI coding agents struggle because context windows read code flatly. SDCU constructs a queryable, persistent in-memory knowledge graph of your entire codebase:
* **AST Multi-Language Extraction**: Maps functions, classes, interfaces, imports, and calls across Python, TypeScript, Rust, Go, etc.
* **In-Memory & SQLite Cache**: Stored in `.sdcu/graph.json` for sub-millisecond retrieval.
* **GraphRAG & Path Tracing**:
  * `sdcu graph path <Source> <Target>` finds the shortest execution path across files.
  * `sdcu graph query "<question>"` performs BFS neighborhood expansion to supply AI agents with exact context.
  * Automatically detects over-coupled **God Nodes** (potential architectural bottlenecks).

---

## 3. UI Craft & Unslopping (U) Engine

Transforms generic vibecoded interfaces into bespoke, crafted designs using the **9-Pass Redline Review**:
1. **Spacing**: Enforce a rigid spatial cadence (4px / 8px rhythm).
2. **Color**: Quiet tinted neutrals + single sharp brand accent (no multi-hue purple gradients).
3. **Quiet Chrome**: Clean, non-distracting navigation and card containers (no neon glows).
4. **Typography**: Intentional font pairing and optical hierarchy.
5. **Layout**: Natural visual focus and whitespace.
6. **Copy & Content**: Punchy, human microcopy (no AI buzzwords like *"seamlessly supercharge"*).
7. **Details**: Crisp 1px borders, subtle light/shadow contrasts.
8. **Bespoke Visuals**: Authentic product previews and diagrams.
9. **Motion**: Purposeful 150-200ms ease-out transitions.

---

## Installation & CLI Usage

### Local CLI Setup
```bash
git clone https://github.com/<your-username>/sdcu.git
cd sdcu

# Python core engine
pip install -e packages/core

# Or run via Node CLI
./packages/cli/bin/sdcu.js --help
```

### Run an Automated Audit
```bash
# Run full master audit (System Design + Context Graph + UI Craft)
sdcu audit

# Audit code for the 20 System Design & Security Checkpoints
sdcu sd audit

# Audit frontend files for AI slop and get 9-pass redline fixes
sdcu ui audit

# Build or refresh codebase context graph
sdcu graph build

# Query codebase relationships using GraphRAG
sdcu graph query "How does authentication flow to the database?"

# Trace execution path between two symbols
sdcu graph path "cli.py" "linter.py"

# Export production resilience templates
sdcu sd template singleflight
sdcu sd template circuit-breaker
sdcu sd template jittered-cache
```

---

## Agent Skills Installation

To empower your AI coding assistant with SDCU, simply copy or symlink the `skills/` folder into your agent's skills directory:

### For Google Antigravity
```bash
cp -r skills/* ~/.gemini/config/skills/
```

### For Claude Code
```bash
cp -r skills/* ~/.claude/skills/
```

### For Cursor / Codex / OpenCode
Add the rules from `skills/sdcu/SKILL.md` and `skills/sdcu-sd/references/20-checkpoints.md` to your `.cursorrules` or system prompt.

---

## Production Templates

SDCU includes production-ready TypeScript templates ready to drop into your projects:
* [`circuit-breaker.ts`](skills/sdcu-sd/templates/circuit-breaker.ts) - Resilient circuit breaker state machine (Closed, Open, Half-Open).
* [`singleflight.ts`](skills/sdcu-sd/templates/singleflight.ts) - Request coalescing engine (10,000 requests $\to$ 1 DB query).
* [`jittered-cache.ts`](skills/sdcu-sd/templates/jittered-cache.ts) - Jittered TTL cache with Stale-While-Revalidate support.

---

## Contributing & License

Contributions are welcome! Please check [CONTRIBUTING.md](CONTRIBUTING.md) for details on submitting new checkpoints, graph algorithms, or UI craft passes.

Distributed under the [MIT License](LICENSE).
*(UI Craft module builds upon unslopping principles created by Damir Sokolovsky, CC BY 4.0)*
