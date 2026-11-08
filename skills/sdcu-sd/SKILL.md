---
name: sdcu-sd
description: "Production System Design & Resilience Auditor. Enforces the 20 Security & Scale Checkpoints, 17 System Design Pillars, and 6 Cache-to-Database Resilience mechanisms (SingleFlight, Jittered TTL, Circuit Breakers, Stale-While-Revalidate). Audits code against security leaks, N+1 queries, unindexed schemas, and cascading outages."
trigger: /sdcu-sd
---

# /sdcu-sd: System Design & Resilience Auditor

The **System Design (SD)** module audits client-side, server-side, and database architecture to prevent fragile AI-generated code.

## When to Use
Run `/sdcu-sd` whenever:
* Designing or modifying client-server architecture, database schemas, or caching layers.
* Reviewing code for security leaks (API keys, CORS, IDOR, SQL injection, XSS).
* Designing high-throughput endpoints vulnerable to cache stampedes, N+1 queries, or database pool exhaustion.
* Planning microservice vs monolith trade-offs, message queues, or rate limiting.

## Core Rules & Checklists
1. **[The 20 Critical Checkpoints](references/20-checkpoints.md)**:
   - *Security*: No frontend API keys, strict auth & RBAC, parameterized SQL, XSS sanitization, Argon2/bcrypt hashing, restricted CORS, no `.env` in git, rate limiting, IDOR prevention, up-to-date dependencies.
   - *Backend & Scale*: DB schema planning & migrations, indexed queries (zero N+1), multi-tier caching, structured error handling, structured logging & telemetry, backups & rollback.
   - *Code Health*: Test coverage, modular architecture, regression-guarded edits, self-debuggability.

2. **[The 17 System Design Concepts](references/17-concepts.md)**:
   - Load Balancing, Caching, CDN, API Gateway, Microservices, Monolithic Architecture, Replication, Partitioning/Sharding, Message Queues, Rate Limiting, Consistent Hashing, CAP Theorem, Horizontal Scaling, Vertical Scaling, Fault Tolerance, Circuit Breaker, Event-Driven Architecture.

3. **[Resilient Cache-to-DB Playbook](references/cache-db-resilience.md)**:
   - Don't let every cache miss hit the DB (circuit breakers & throttling).
   - Jittered Cache Expiration: $\text{TTL} = \text{Base TTL} + \text{Random Jitter}$.
   - Request Coalescing (SingleFlight): 10,000 concurrent requests $\to$ 1 DB query $\to$ shared result.
   - Gradual Cache Warming with controlled background workers.
   - Strict database pool limits, query concurrency caps, and backpressure.
   - Stale-While-Revalidate: safe stale serving during cache degradation.

## Reusable Resilience Code Templates
* [Circuit Breaker](templates/circuit-breaker.ts)
* [SingleFlight Request Coalescing](templates/singleflight.ts)
* [Jittered Cache with Stale-While-Revalidate](templates/jittered-cache.ts)

## How to Audit Code
1. Inspect the codebase for security leaks: grep for client-exposed secrets (`process.env.NEXT_PUBLIC_*_KEY`), raw SQL string concatenation, wildcard CORS headers (`*`), and missing auth wrappers.
2. Inspect database queries for unindexed lookups and loops executing queries (N+1).
3. Verify cache logic: ensure all TTLs include random jitter, concurrent requests coalesce via SingleFlight, and fallback strategies exist when the cache drops.
4. Output a structured report with:
   - **Vulnerabilities Found** (Ranked by Severity: Critical, High, Medium)
   - **Architectural Bottlenecks** (Scaling limits, pool exhaustion risks)
   - **Remediation Code & Drop-In Diff**

