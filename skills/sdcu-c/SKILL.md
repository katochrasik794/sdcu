---
name: sdcu-c
description: "Codebase Context Graph Engine. Solves AI agent memory amnesia by generating and querying an in-memory knowledge graph of symbols, imports, AST relationships, call hierarchies, god nodes, and architectural communities. Powers BFS/DFS code paths and GraphRAG context retrieval."
trigger: /sdcu-c
---

# /sdcu-c: Code Context Graph Engine

The **Context (C)** module cures AI context amnesia by representing codebases as connected knowledge graphs in cache and memory, rather than flat token windows.

## When to Use
Run `/sdcu-c` whenever:
* Navigating an unfamiliar codebase or mapping complex multi-file relationships.
* Tracing call flows: e.g., "What services call `processPayment`?" or "Trace request from Route to DB."
* Detecting architectural bottlenecks, over-coupled "god nodes", or isolated components.
* Performing GraphRAG context injection before modifying core APIs.

## Commands

```bash
# Build / update codebase knowledge graph
sdcu graph build

# Query codebase relationships using GraphRAG (BFS traversal)
sdcu graph query "<question about codebase>"

# Find shortest execution path between two symbols
sdcu graph path "<SourceSymbolOrFile>" "<TargetSymbolOrFile>"

# Explain a complex symbol and its complete blast radius
sdcu graph explain "<SymbolName>"

# Detect over-coupled god nodes and community clusters
sdcu graph cluster
```

## How It Works
1. **AST Extraction**:
   Uses Tree-Sitter to extract classes, functions, interfaces, methods, imports, and calls across TypeScript, Python, Rust, Go, Java, C++, and SQL schemas.
2. **Graph Construction**:
   Creates a directed multigraph where:
   - **Nodes**: Files, modules, classes, functions, database tables.
   - **Edges**: `IMPORTS`, `CALLS`, `EXTENDS`, `IMPLEMENTS`, `QUERIES`, `MUTATES`.
3. **In-Memory & SQLite Cache**:
   Caches the built graph at `.sdcu/graph.json` and in memory for sub-millisecond graph queries without rescanning unchanged files.
4. **Community Detection & God-Node Scoring**:
   Applies Louvain community clustering to partition modules into architectural domains and calculates degree centrality to flag high-risk god nodes.

## Agent Guidelines
* Before modifying any core function, run `sdcu graph path` or `sdcu graph explain` to understand all upstream callers and downstream dependencies.
* Never guess where a symbol is defined; query the context graph.

