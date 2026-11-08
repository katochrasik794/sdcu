# Resilient Cache-to-Database Playbook
*(Preventing Cache Failures from Becoming Catastrophic Database Outages)*

> **Interview- & Production-Ready Principle**:
> *"I prevent a cache failure from turning into a database failure by using circuit breakers, request coalescing, rate limiting, jittered TTLs, gradual cache warming, and database concurrency limits. The key is controlling cache misses instead of allowing every request to fall through to the database."*

---

## The Danger: The Cache Stampede (Dog-Piling) Catastrophe

In a naive architecture:
```
Normal State:
Clients (10,000 req/s) ──> [ Redis Cache ] (99% hit rate)
                                │ (100 req/s miss)
                                ▼
                       [ Primary Database ] (Healthy load)
```

When Redis fails or hot keys simultaneously expire without resilience patterns:
```
Failure State:
Clients (10,000 req/s) ──X [ Redis Crashed / Miss ]
                                │
                                ▼ (10,000 req/s fallthrough!)
                       [ Primary Database ] ──> Connection Pool Exhaustion
                                            ──> CPU 100%
                                            ──> CATASTROPHIC OUTAGE
```

---

## The 6 Pillars of Resilient Protection

### 1. Don't Let Every Request Hit the DB
* **The Rule**: When Redis is unavailable or responding with timeouts, never fall back to the database for every single incoming request.
* **Mechanism**:
  - Wrap cache access in a **Circuit Breaker** (e.g. 50% failure rate over 10 seconds opens the circuit).
  - While Open, trip directly to:
    1. A degraded fallback response (e.g. cached stale snapshot, empty list, or fast rejection).
    2. Request throttling / rate-limiting that sheds 90% of load.
  - Never allow an unthrottled 1:1 fallback from cache miss to database query.

### 2. Add Jittered Cache Expiration
* **The Rule**: Never set static identical expiration times for keys generated at the same time.
* **Mechanism**:
  $$\text{TTL} = \text{Base TTL} + \text{Random Jitter}$$
  * For example, if Base TTL is 3600 seconds (1 hour):
  ```ts
  const baseTtl = 3600; // 60 minutes
  const maxJitter = 600; // up to 10 minutes jitter
  const jitteredTtl = baseTtl + Math.floor(Math.random() * maxJitter);
  await redis.set(key, value, 'EX', jitteredTtl);
  ```
* **Effect**: Millions of keys expire smoothly over an interval instead of detonating all at once.

### 3. Use Request Coalescing (The SingleFlight Pattern)
* **The Rule**: If 10,000 concurrent requests request the same missing cache key, exactly **ONE** query goes to the database.
* **Mechanism**:
  ```mermaid
  sequenceDiagram
      participant C1 as Client 1 (First)
      participant C2 as Client 2..10,000
      participant SF as SingleFlight Coalescer
      participant DB as Database

      C1->>SF: Get key "user:123"
      Note over SF: Key not in-flight. Launch query!
      SF->>DB: SELECT * FROM users WHERE id = 123
      C2->>SF: Get key "user:123"
      Note over SF: Key already in-flight! Attach promise.
      DB-->>SF: Return user row
      SF-->>C1: Return data
      SF-->>C2: Broadcast identical data to all 9,999 callers
  ```
* **Ratio**: $10,000 \text{ Requests} \longrightarrow 1 \text{ DB Query} \longrightarrow \text{Shared Result}$.

### 4. Warm the Cache Gradually
* **The Rule**: When Redis recovers or restarts, do not immediately switch 100% of live traffic onto cold cache nodes.
* **Mechanism**:
  - Use controlled background workers / warming scripts to pre-populate the top 1,000 most frequently accessed keys.
  - Employ canary routing: route 5% of requests through the recovered cache node, monitor hit rates and latency, and incrementally ramp to 100%.

### 5. Protect the Database (Concurrency & Backpressure)
* **The Rule**: Enforce strict hardware-safe ceilings on the database connection pool and query execution queue.
* **Key Thresholds**:
  - **Connection Pool Limit**: Set to a hard limit based on DB hardware:
    $$\text{Connections} = (\text{Core Count} \times 2) + \text{Disk Spindle / Effective Concurrency}$$
  - **Query Concurrency Ceiling**: Maximum parallel in-flight queries.
  - **Queue Timeout**: Reject queries queued longer than 2 seconds with HTTP 503 (Service Unavailable) or HTTP 429 rather than letting queries pile up indefinitely.
  - **Backpressure**: Shed non-essential queries (reporting, analytics, recommendations) when DB CPU exceeds 80%.

### 6. Use Stale Data When Safe (Stale-While-Revalidate)
* **The Rule**: For non-critical data, serve a slightly stale cached value instead of hitting the database during a cache failure or refresh.
* **Mechanism**:
  - Store data with two timestamps:
    * Soft TTL (Freshness limit, e.g. 5 minutes).
    * Hard TTL (Absolute expiration, e.g. 24 hours).
  - If a request arrives between Soft TTL and Hard TTL:
    1. Immediately return the stale value to the user (0ms wait).
    2. Asynchronously fire a single background worker to refresh the DB and update Redis.
  - If Redis fails, return stale memory snapshot or fallback rather than cascading to DB failure.

