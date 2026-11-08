# 17 Essential System Design Concepts Every Engineer & Agent Must Master

A production-grade system requires deliberate trade-offs across these 17 foundational pillars:

---

## 1. Load Balancing
* **What it is**: Distributing network traffic across multiple servers to prevent any single server from becoming overloaded.
* **Layers**:
  * **L4 (Transport Layer)**: Routes based on IP and TCP/UDP ports (e.g. AWS NLB, HAProxy). Blazing fast throughput.
  * **L7 (Application Layer)**: Routes based on HTTP headers, cookies, URLs (e.g. Nginx, AWS ALB, Envoy). Supports path-based routing and SSL termination.
* **Algorithms**: Round-robin, Weighted Round-Robin, Least Connections, IP Hash.

## 2. Caching
* **What it is**: Storing copies of data in fast, volatile memory (RAM) to serve future requests with sub-millisecond latency.
* **Patterns**:
  * **Cache-Aside (Lazy Loading)**: Application checks cache; if miss, reads from DB and writes to cache.
  * **Read-Through**: Cache library automatically fetches from DB on miss.
  * **Write-Through**: Data written simultaneously to cache and DB.
  * **Write-Behind (Write-Back)**: Data written to cache immediately, flushed asynchronously to DB.
* **Eviction Policies**: LRU (Least Recently Used), LFU (Least Frequently Used), FIFO, TTL expiration.

## 3. Content Delivery Network (CDN)
* **What it is**: A geographically distributed network of proxy servers that cache content close to end users.
* **Key Capabilities**: Static asset caching (images, JS, CSS), video streaming chunk caching, Anycast routing, DDoS absorption, SSL/TLS edge handshake termination.

## 4. API Gateway
* **What it is**: The single entry point into a backend system that decouples external clients from internal service topology.
* **Core Responsibilities**: Request routing, centralized authentication & token verification, rate limiting, request transformation, response compression, SSL termination, and telemetry collection.

## 5. Microservices
* **What it is**: An architectural style that structures an application as a collection of loosely coupled, independently deployable services around business domains.
* **Trade-offs**:
  * *Pros*: Independent team velocity, polyglot technology stack, targeted scaling.
  * *Cons*: Distributed transaction complexity (Saga pattern), network latency, eventual consistency, difficult observability.

## 6. Monolithic Architecture
* **What it is**: An application structured as a single unified code repository and executable deployment.
* **Modern Best Practice**: **Modular Monolith**. Well-defined domain boundaries inside one binary. Avoids distributed network latency and complexity while preserving maintainability.

## 7. Replication
* **What it is**: Copying data across multiple database nodes to provide fault tolerance and read scaling.
* **Topologies**:
  * **Primary-Replica (Master-Slave)**: All writes go to Primary; reads are distributed across Replicas. Suffers from replication lag.
  * **Multi-Primary**: Writes accepted at multiple nodes; requires distributed conflict resolution.

## 8. Partitioning & Sharding
* **What it is**: Splitting a massive database into smaller, faster, more manageable pieces across distinct servers.
* **Strategies**:
  * **Horizontal Partitioning (Sharding)**: Splitting rows across databases (e.g. Users 1-1,000,000 on DB 1; 1,000,001-2,000,000 on DB 2).
  * **Vertical Partitioning**: Splitting columns into separate tables or databases (e.g. separating profile metadata from large text blobs).
  * **Hash-based vs Range-based Sharding**.

## 9. Message Queues
* **What it is**: Asynchronous communication buffers between producers and consumers (e.g. Kafka, RabbitMQ, SQS, BullMQ).
* **Benefits**: Decouples services, absorbs massive traffic spikes (load leveling), guarantees message delivery with retries and dead-letter queues (DLQ).

## 10. Rate Limiting
* **What it is**: Controlling the rate of traffic sent or received by a network or API.
* **Algorithms**:
  * **Token Bucket**: Tokens added at constant rate; bursts allowed up to capacity.
  * **Leaky Bucket**: Requests processed at smooth, steady rate.
  * **Fixed Window**: Counters reset at fixed intervals (prone to burst at window edges).
  * **Sliding Window Log / Counter**: Smooth rate limiting without boundary spikes.

## 11. Consistent Hashing
* **What it is**: A distributed hashing scheme that minimizes the number of keys remapped when nodes are added or removed from a cluster.
* **Mechanism**: Maps both nodes and keys onto a virtual hash ring (0 to $2^{32}-1$). Keys are assigned to the next clockwise node.
* **Virtual Nodes**: Solves data hotspotting by mapping each physical machine to multiple virtual points on the ring.

## 12. CAP Theorem
* **What it is**: In any distributed data store, you can only simultaneously guarantee at most two out of three:
  * **Consistency (C)**: Every read receives the most recent write or an error.
  * **Availability (A)**: Every non-failing node returns a reasonable response (without error), but might not be the latest data.
  * **Partition Tolerance (P)**: The system continues to operate despite arbitrary message loss or network failure.
* **Rule**: Since network partitions are inevitable in real hardware networks, systems must choose between **CP** (e.g., MongoDB, Spanner, ZooKeeper) or **AP** (e.g., Cassandra, DynamoDB, CouchDB).

## 13. Horizontal Scaling (Scale-Out)
* **What it is**: Adding more machines to the pool of resources (e.g., adding 5 more container instances behind a load balancer).
* **Requirement**: Application tier must be completely stateless (sessions stored in Redis/DB, not in local server memory).

## 14. Vertical Scaling (Scale-Up)
* **What it is**: Adding more power (CPU, RAM, NVMe SSD) to an existing machine (e.g. upgrading an AWS `t3.medium` to `r6i.8xlarge`).
* **Limitations**: Hardware limits, exponential cost curve, single point of failure (downtime during upgrade).

## 15. Fault Tolerance & Graceful Degradation
* **What it is**: The ability of a system to continue operating properly in the event of the failure of one or more of its components.
* **Techniques**: Redundancy, health checks, automatic failover, shedding non-critical load (e.g., turning off recommendations to keep checkout working).

## 16. Circuit Breakers
* **What it is**: A design pattern used to detect failures and encapsulate the logic of preventing a failure from constantly recurring during maintenance, temporary external or internal outages.
* **States**:
  * **Closed**: Requests flow normally. Failures are tracked.
  * **Open**: Failure threshold exceeded. Requests fail immediately with a fallback, avoiding load on downstream systems.
  * **Half-Open**: After a cooldown timer, a small percentage of test requests are allowed through. If successful, state resets to Closed.

## 17. Event-Driven Architecture (EDA)
* **What it is**: A software architecture paradigm where decoupled components interact primarily by producing, detecting, and consuming asynchronous events.
* **Patterns**: Event Notification, Event-Carried State Transfer, Event Sourcing (storing every state change as an immutable append-only event log), CQRS (Command Query Responsibility Segregation).
