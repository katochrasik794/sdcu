# The 20 Production Engineering Anti-Patterns & Defenses

> **Core Axiom**: *"Prompt fixes cause regressions; learn and apply System Design first."*

---

## Part 1: Security Guardrails (01 - 10)

### 01. API Keys in Frontend
* **The Anti-Pattern**: Embedding server secrets, private API tokens, Stripe secret keys, or database credentials in client-side bundles (e.g. `NEXT_PUBLIC_STRIPE_SECRET`, raw fetch headers).
* **The Risk**: Anyone inspecting Network DevTools or bundle source code can extract credentials and compromise the entire backend infrastructure.
* **The Defense**:
  - Store all credentials exclusively in server-side environment variables (`.env.local` not committed to git).
  - Proxy all third-party external API calls through authenticated server endpoints (`/api/checkout`, `/api/ai`).
  - Enforce secret scanners (e.g., `trufflehog`, `gitleaks`) in CI/CD.

### 02. No Auth / Role Checks
* **The Anti-Pattern**: Trusting client assertions or assuming an endpoint is private simply because the UI hides the button.
* **The Risk**: Privilege escalation; regular users invoking admin endpoints (`DELETE /api/users/123`).
* **The Defense**:
  - Enforce cryptographically verified session/JWT tokens on every single state-changing server route.
  - Implement Role-Based Access Control (RBAC) or Attribute-Based Access Control (ABAC) middleware.
  - Verify authorization at the data layer, not just the presentation layer.

### 03. SQL Injection Open
* **The Anti-Pattern**: Concatenating raw user inputs into query strings:
  ```ts
  // VULNERABLE
  db.query(`SELECT * FROM users WHERE email = '${req.body.email}'`);
  ```
* **The Risk**: Complete database dump, data destruction (`DROP TABLE`), or arbitrary command execution.
* **The Defense**:
  - ALWAYS use parameterized queries or trusted ORM/Query Builders (Prisma, Kysely, Drizzle, SQLAlchemy):
  ```ts
  // SECURE
  db.query('SELECT * FROM users WHERE email = $1', [email]);
  ```

### 04. XSS: No Input Sanitization
* **The Anti-Pattern**: Rendering untrusted HTML or markdown using `dangerouslySetInnerHTML`, `v-html`, or unescaped templates.
* **The Risk**: Session hijacking, malicious script injection, cookie theft.
* **The Defense**:
  - Sanitize all user-submitted rich text using libraries like `DOMPurify`.
  - Set strict Content Security Policy (CSP) headers: `Content-Security-Policy: default-src 'self'`.
  - Prefer plain text rendering wherever rich formatting is unnecessary.

### 05. Passwords Not Hashed
* **The Anti-Pattern**: Storing passwords in plaintext, base64, or using deprecated algorithms like MD5 or plain SHA-256.
* **The Risk**: Instant credential compromise in the event of a database leak or backup exposure.
* **The Defense**:
  - Use memory-hard hashing algorithms with per-user salt: **Argon2id** (recommended) or **bcrypt** (work factor $\ge 12$).
  - Never log passwords or passwords hashes in server logs.

### 06. CORS `*` All Origins Open
* **The Anti-Pattern**: Setting `Access-Control-Allow-Origin: *` while allowing credentials or cookies.
* **The Risk**: Cross-origin attacks allowing malicious third-party websites to forge authenticated user requests from the browser.
* **The Defense**:
  - Whitelist only trusted, explicit origins:
  ```ts
  const allowedOrigins = ['https://myapp.com', 'https://admin.myapp.com'];
  ```
  - Disallow wildcard origins when `credentials: include` is active.

### 07. `.env` Pushed to GitHub
* **The Anti-Pattern**: Committing `.env`, `.env.production`, or credential files into version control.
* **The Risk**: GitHub bot scrapers index public secrets within seconds.
* **The Defense**:
  - Ensure `.env*` (except `.env.example`) is present in `.gitignore`.
  - Use secret managers (AWS Secrets Manager, Infisical, Doppler, 1Password CLI) for production secrets.
  - Automate pre-commit hooks preventing commits containing high-entropy strings.

### 08. No Rate Limit = DDoS Easy
* **The Anti-Pattern**: Exposing public endpoints (login, registration, LLM generation, search) without request rate throttling.
* **The Risk**: Cost runaway, denial of service, credential stuffing.
* **The Defense**:
  - Implement Redis-backed Token Bucket or Sliding Window rate limiters.
  - Apply stricter limits on sensitive routes (e.g. 5 attempts per 15 minutes for `/api/auth/login`).
  - Deploy edge DDoS protection (Cloudflare, AWS Shield).

### 09. IDOR: `/user/2` Data Leak
* **The Anti-Pattern**: Insecure Direct Object References: fetching resources purely by client-supplied ID without verifying ownership:
  ```ts
  // VULNERABLE
  const invoice = await db.invoices.findById(req.params.id);
  ```
* **The Risk**: User A enumerates IDs to download User B's invoices, profile data, or medical records.
* **The Defense**:
  - Always scope queries to the authenticated tenant/user ID:
  ```ts
  // SECURE
  const invoice = await db.invoices.findOne({
    id: req.params.id,
    userId: req.user.id
  });
  ```

### 10. Outdated npm Packages
* **The Anti-Pattern**: Pinning packages indefinitely without dependency vulnerability auditing.
* **The Risk**: Supply chain attacks, known CVE vulnerabilities (prototype pollution, remote code execution).
* **The Defense**:
  - Automate `npm audit` / `pnpm audit` / Dependabot / Snyk in CI.
  - Enforce lockfile freezing in deployments (`npm ci` or `pnpm install --frozen-lockfile`).

---

## Part 2: Backend & Scale Architecture (11 - 16)

### 11. No DB Schema Planning
* **The Anti-Pattern**: Dumping arbitrary JSON blobs into unstructured collections or ad-hoc relational tables without foreign key constraints, field validations, or migration history.
* **The Risk**: Data corruption, orphaned records, and impossible schema migrations down the line.
* **The Defense**:
  - Use schema definition languages and declarative migration engines (Prisma, Flyway, Alembic).
  - Explicitly define primary keys, foreign keys, unique constraints, and non-nullability.

### 12. N+1 Queries, No Indexes
* **The Anti-Pattern**: Querying relational data in loops:
  ```ts
  // VULNERABLE: 1 query for posts + N queries for authors
  const posts = await db.posts.findMany();
  for (const post of posts) {
    post.author = await db.users.findById(post.authorId);
  }
  ```
  Missing B-Tree / GIN indexes on foreign keys and frequently queried filter columns (`WHERE user_id = ? AND status = ?`).
* **The Risk**: Database CPU spikes to 100%, severe query latency degradation under load.
* **The Defense**:
  - Use `JOIN`, batch loader patterns (DataLoader), or ORM eager loading (`include: { author: true }`).
  - Add indexes on all foreign keys, status filters, and compound query columns.
  - Regularly analyze queries using `EXPLAIN ANALYZE`.

### 13. No Caching Layer
* **The Anti-Pattern**: Forcing the primary relational database to recompute identical read queries hundreds of times per second.
* **The Risk**: Database connection pool exhaustion, slow page loads.
* **The Defense**:
  - Implement a multi-tier caching hierarchy:
    * L1: In-memory LRU cache in Node/Go/Rust process.
    * L2: Distributed Redis cluster with jittered TTL and stale-while-revalidate.
    * L3: HTTP CDN edge caching for public assets and static pages.

### 14. Zero Error Handling
* **The Anti-Pattern**: Silent `catch (e) {}` blocks, or unhandled promise rejections crashing Node.js processes, or dumping raw stack traces with database connection strings to the client.
* **The Risk**: Process crashes, information disclosure to attackers, silent data loss.
* **The Defense**:
  - Centralized error-handling middleware.
  - Strongly typed Result types (`Result<T, E>`) for domain operations.
  - Return sanitized HTTP error payloads: `{ status: "error", code: "NOT_FOUND", message: "User not found" }`.

### 15. No Logs, No Monitoring
* **The Anti-Pattern**: Scattered `console.log("here")` or complete silence during runtime failures.
* **The Risk**: Downtime occurs without alert; post-mortem root-cause debugging is impossible.
* **The Defense**:
  - Structured JSON logging (Pino, Winston, Zap) with correlation IDs (`trace_id`, `request_id`).
  - OpenTelemetry metrics and traces piped to Datadog, Prometheus/Grafana, or CloudWatch.
  - Healthcheck endpoints (`/healthz`, `/livez`, `/readyz`).

### 16. No Backups or Rollback
* **The Anti-Pattern**: Deploying direct schema changes without migration rollback scripts, and operating databases without point-in-time recovery (PITR).
* **The Risk**: Irrecoverable data loss during bad deployments or hardware failure.
* **The Defense**:
  - Automated daily snapshots and continuous WAL (Write-Ahead Log) archiving for Point-In-Time Recovery.
  - Backward-compatible database migrations (Expand and Contract pattern).
  - Blue-Green or Canary deployment strategies with instant one-click rollback.

---

## Part 3: Code Health & AI Rigor (17 - 20)

### 17. No Tests at All
* **The Anti-Pattern**: Shipping features based purely on "it worked once in localhost."
* **The Risk**: High regression rate; refactoring becomes terrifying and unsafe.
* **The Defense**:
  - Test pyramid: Unit tests for core domain logic, integration tests for DB queries/APIs, end-to-end tests for critical user journeys.
  - Fast test execution in CI before merging PRs.

### 18. Copy-Paste, No Structure
* **The Anti-Pattern**: 2,000-line god components where UI rendering, business calculations, SQL queries, and state management are mixed together.
* **The Risk**: Incomprehensible spaghetti code; high cognitive load; impossible to mock or unit test.
* **The Defense**:
  - Separation of Concerns: Clean Architecture / Hexagonal Architecture:
    * Domain Layer (Pure business logic)
    * Application Layer (Use cases & orchestration)
    * Infrastructure Layer (DB, external APIs)
    * Presentation Layer (UI / API controllers)

### 19. Prompt Fix = New Bugs (Regression Sprawl)
* **The Anti-Pattern**: Blindly applying AI agent fixes for an isolated bug without running regression tests, causing breakage in adjacent components.
* **The Risk**: Whack-a-mole development loop; code quality degrades progressively with every prompt.
* **The Defense**:
  - Run regression test suite on every agent edit.
  - Require the agent to provide automated tests for every bug fix it claims to make.
  - Check blast radius using the Context Graph (`sdcu path <modified_module> <consumers>`).

### 20. Can't Debug Own Code
* **The Anti-Pattern**: Engineers and AI agents generating code whose internal execution path they do not understand, resorting to random trial-and-error edits when errors occur.
* **The Risk**: Unmaintainable software; catastrophic failures during production incidents.
* **The Defense**:
  - Enforce readable, self-documenting code with meaningful naming.
  - Require architecture decision records (ADRs) and call-flow diagrams for non-trivial modules.
  - Use `sdcu graph explain <node>` to generate human-readable explanations of complex interactions.
