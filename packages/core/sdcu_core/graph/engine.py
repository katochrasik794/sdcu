"""
SDCU Context Graph Engine
Extracts AST symbols, imports, and relationships to construct an in-memory & cached knowledge graph.
"""

import ast
import json
import os
import re
from pathlib import Path
from typing import Dict, List, Any, Optional
import networkx as nx

class ContextGraphEngine:
    def __init__(self, root_dir: str = "."):
        self.root_dir = Path(root_dir)
        self.graph = nx.DiGraph()
        self.output_dir = self.root_dir / ".sdcu"
        self.graph_file = self.output_dir / "graph.json"

    def build(self) -> Dict[str, Any]:
        """Scans codebase and constructs code dependency graph."""
        self.graph.clear()
        self.output_dir.mkdir(parents=True, exist_ok=True)

        for root, dirs, files in os.walk(self.root_dir):
            dirs[:] = [d for d in dirs if not d.startswith(".") and d not in ("node_modules", "vendor", "dist", "build", "__pycache__")]
            
            for file in files:
                ext = Path(file).suffix.lower()
                full_path = Path(root) / file
                rel_path = str(full_path.relative_to(self.root_dir))

                if ext == ".py":
                    self._parse_python(rel_path, full_path)
                elif ext in (".ts", ".tsx", ".js", ".jsx"):
                    self._parse_javascript_typescript(rel_path, full_path)

        # Second pass: link module imports to local files if matching
        for node in list(self.graph.nodes):
            if node.startswith("module::"):
                mod_name = node.replace("module::", "")
                mod_as_path = mod_name.replace(".", "/")
                for candidate in list(self.graph.nodes):
                    if candidate.startswith("file::"):
                        file_subpath = candidate.replace("file::", "")
                        if file_subpath.endswith(f"{mod_as_path}.py") or file_subpath.endswith(f"{mod_name}.py"):
                            self.graph.add_edge(node, candidate, relation="RESOLVES_TO")

        # Compute graph metrics (degree centrality, god nodes)
        degrees = dict(self.graph.degree())
        sorted_nodes = sorted(degrees.items(), key=lambda item: item[1], reverse=True)
        god_nodes = [{"node": node, "degree": deg} for node, deg in sorted_nodes[:10] if deg > 2]

        data = {
            "node_count": self.graph.number_of_nodes(),
            "edge_count": self.graph.number_of_edges(),
            "god_nodes": god_nodes,
            "nodes": [
                {"id": n, **self.graph.nodes[n]} for n in self.graph.nodes
            ],
            "edges": [
                {"source": u, "target": v, **self.graph.edges[u, v]} for u, v in self.graph.edges
            ]
        }

        # Save to cache
        with open(self.graph_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        return data

    def query(self, question: str) -> Dict[str, Any]:
        """GraphRAG context retrieval using BFS traversal."""
        self._ensure_loaded()
        keywords = re.findall(r'[a-zA-Z0-9_]{3,}', question.lower())
        
        matched_nodes = []
        for n in self.graph.nodes:
            node_label = str(n).lower()
            if any(k in node_label for k in keywords):
                matched_nodes.append(n)

        # BFS neighborhood
        subgraph_nodes = set(matched_nodes)
        for n in matched_nodes[:5]:
            subgraph_nodes.update(self.graph.successors(n))
            subgraph_nodes.update(self.graph.predecessors(n))

        return {
            "matched_keywords": keywords,
            "seed_nodes": matched_nodes[:10],
            "context_nodes": list(subgraph_nodes)[:25],
            "total_relevant": len(subgraph_nodes)
        }

    def shortest_path(self, source: str, target: str) -> Optional[List[str]]:
        """Finds shortest execution/dependency path between two nodes."""
        self._ensure_loaded()
        s_node = self._resolve_node(source)
        t_node = self._resolve_node(target)

        if not s_node or not t_node:
            return None

        # Try directed first, then undirected
        try:
            return nx.shortest_path(self.graph, source=s_node, target=t_node)
        except (nx.NetworkXNoPath, nx.NodeNotFound):
            try:
                return nx.shortest_path(self.graph.to_undirected(), source=s_node, target=t_node)
            except (nx.NetworkXNoPath, nx.NodeNotFound):
                return None

    def _resolve_node(self, term: str) -> Optional[str]:
        if term in self.graph.nodes:
            return term
        term_lower = term.lower()
        # 1. Exact match at end of node ID (e.g. /cli.py or ::cli.py)
        for n in self.graph.nodes:
            nl = str(n).lower()
            if nl.endswith(f"/{term_lower}") or nl.endswith(f"::{term_lower}") or nl == term_lower:
                return n
        # 2. Substring match
        for n in self.graph.nodes:
            if term_lower in str(n).lower():
                return n
        return None

    def _ensure_loaded(self):
        if self.graph.number_of_nodes() > 0:
            return
        if self.graph_file.exists():
            with open(self.graph_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            for n in data.get("nodes", []):
                nid = n["id"]
                attrs = {k: v for k, v in n.items() if k != "id"}
                self.graph.add_node(nid, **attrs)
            for e in data.get("edges", []):
                u, v = e["source"], e["target"]
                attrs = {k: v for k, v in e.items() if k not in ("source", "target")}
                self.graph.add_edge(u, v, **attrs)
        else:
            self.build()

    def _parse_python(self, rel_path: str, full_path: Path):
        file_node = f"file::{rel_path}"
        self.graph.add_node(file_node, kind="file", path=rel_path)
        try:
            tree = ast.parse(full_path.read_text(encoding="utf-8", errors="ignore"))
        except Exception:
            return

        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                func_node = f"func::{rel_path}::{node.name}"
                self.graph.add_node(func_node, kind="function", name=node.name, line=node.lineno)
                self.graph.add_edge(file_node, func_node, relation="DEFINES")
            elif isinstance(node, ast.ClassDef):
                cls_node = f"class::{rel_path}::{node.name}"
                self.graph.add_node(cls_node, kind="class", name=node.name, line=node.lineno)
                self.graph.add_edge(file_node, cls_node, relation="DEFINES")
            elif isinstance(node, (ast.Import, ast.ImportFrom)):
                if isinstance(node, ast.ImportFrom) and node.module:
                    imported = f"module::{node.module}"
                    self.graph.add_node(imported, kind="module")
                    self.graph.add_edge(file_node, imported, relation="IMPORTS")

    def _parse_javascript_typescript(self, rel_path: str, full_path: Path):
        file_node = f"file::{rel_path}"
        self.graph.add_node(file_node, kind="file", path=rel_path)
        try:
            content = full_path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            return

        # Extract import statements: import ... from './target'
        imports = re.findall(r'import\s+.*?from\s+[\'"](.*?)[\'"]', content)
        for imp in imports:
            imp_node = f"import::{imp}"
            self.graph.add_node(imp_node, kind="import")
            self.graph.add_edge(file_node, imp_node, relation="IMPORTS")

        # Extract exported functions and classes
        exports = re.findall(r'export\s+(?:async\s+)?(?:function|class|const)\s+([a-zA-Z0-9_]+)', content)
        for sym in exports:
            sym_node = f"sym::{rel_path}::{sym}"
            self.graph.add_node(sym_node, kind="symbol", name=sym)
            self.graph.add_edge(file_node, sym_node, relation="EXPORTS")
