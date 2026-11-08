"""
SDCU Master CLI
Unified entrypoint for System Design, Context Graph, and UI Craft.
"""

import argparse
import sys
import json
from pathlib import Path

from sdcu_core.sd.linter import SystemDesignLinter
from sdcu_core.graph.engine import ContextGraphEngine
from sdcu_core.ui.auditor import UIAuditor

def run_sd_audit(args):
    linter = SystemDesignLinter(args.path)
    findings = linter.scan()
    print(f"\n[SDCU System Design Audit] Scanned directory: {args.path}")
    print(f"Total Checkpoint Violations Found: {len(findings)}\n")

    if not findings:
        print("✅ No critical system design or security anti-patterns detected!")
        return

    for f in findings:
        sev_icon = "🔴" if f.severity == "CRITICAL" else ("🟠" if f.severity == "HIGH" else "🟡")
        print(f"{sev_icon} [{f.severity}] Checkpoint {f.checkpoint_id} ({f.category}) in {f.file_path}:{f.line_number}")
        print(f"   Issue:       {f.message}")
        print(f"   Snippet:     {f.matched_snippet}")
        print(f"   Remediation: {f.remediation}\n")

def run_sd_template(args):
    templates_dir = Path(__file__).resolve().parent.parent.parent.parent / "skills" / "sdcu-sd" / "templates"
    tpl_name = args.name.lower()
    mapping = {
        "circuit-breaker": "circuit-breaker.ts",
        "singleflight": "singleflight.ts",
        "jittered-cache": "jittered-cache.ts"
    }

    if tpl_name not in mapping:
        print(f"Error: Unknown template '{tpl_name}'. Available templates: {list(mapping.keys())}")
        sys.exit(1)

    tpl_path = templates_dir / mapping[tpl_name]
    if tpl_path.exists():
        print(f"--- SDCU Production Template: {mapping[tpl_name]} ---")
        print(tpl_path.read_text(encoding="utf-8"))
    else:
        print(f"Template file not found at {tpl_path}")

def run_graph_build(args):
    engine = ContextGraphEngine(args.path)
    print(f"\n[SDCU Context Graph] Scanning codebase in {args.path}...")
    result = engine.build()
    print(f"✅ Graph built successfully!")
    print(f"   Nodes: {result['node_count']}")
    print(f"   Edges: {result['edge_count']}")
    if result["god_nodes"]:
        print("\n⚠️ High-coupling God Nodes detected (potential single points of failure):")
        for gn in result["god_nodes"][:5]:
            print(f"   • {gn['node']} (connections: {gn['degree']})")
    print(f"   Cached in: .sdcu/graph.json\n")

def run_graph_query(args):
    engine = ContextGraphEngine(args.path)
    print(f"\n[SDCU Context Graph Query] \"{args.query}\"")
    result = engine.query(args.query)
    print(f"Matched seed nodes: {len(result['seed_nodes'])}")
    for sn in result['seed_nodes']:
        print(f"  • {sn}")
    print(f"\nRelevant Context Subgraph (BFS 1-hop): {result['total_relevant']} nodes")
    for cn in result['context_nodes'][:10]:
        print(f"  → {cn}")
    print()

def run_graph_path(args):
    engine = ContextGraphEngine(args.path)
    print(f"\n[SDCU Shortest Path] Tracing: '{args.source}' ➔ '{args.target}'")
    path = engine.shortest_path(args.source, args.target)
    if path:
        print(f"✅ Path found ({len(path) - 1} hops):")
        for idx, step in enumerate(path):
            prefix = "   └── " if idx == len(path) - 1 else ("   ├── " if idx > 0 else "   ")
            print(f"{prefix}{step}")
    else:
        print("❌ No connection path found between the specified symbols.")
    print()

def run_ui_audit(args):
    auditor = UIAuditor(args.path)
    findings = auditor.scan()
    print(f"\n[SDCU UI Craft Audit] Scanned directory: {args.path}")
    print(f"Total AI Slop Markers Found: {len(findings)}\n")

    if not findings:
        print("✨ Clean! No vibecoded AI slop markers detected.")
        return

    for f in findings:
        print(f"🎨 [{f.severity}] Pass {f.pass_number} ({f.pass_name}): {f.sign}")
        print(f"   Location:    {f.file_path}:{f.line_number}")
        print(f"   Issue:       {f.message}")
        print(f"   Snippet:     {f.matched_snippet}")
        print(f"   Redline Fix: {f.remediation}\n")

def run_full_audit(args):
    print("=" * 60)
    print("                SDCU MASTER AUDIT REPORT")
    print("      (System Design · Context Graph · UI Craft)")
    print("=" * 60)
    run_sd_audit(args)
    run_ui_audit(args)
    run_graph_build(args)

def main():
    parser = argparse.ArgumentParser(
        prog="sdcu",
        description="SDCU: System Design, Code Context Graph, and UI Craft Suite for AI Coders"
    )
    subparsers = parser.add_subparsers(dest="command")

    # Full audit
    audit_parser = subparsers.add_parser("audit", help="Run full audit (SD + UI + Graph)")
    audit_parser.add_argument("--path", default=".", help="Root path of target project")

    # SD group
    sd_parser = subparsers.add_parser("sd", help="System design & resilience tools")
    sd_sub = sd_parser.add_subparsers(dest="sd_command")
    
    sd_audit = sd_sub.add_parser("audit", help="Run 20-checkpoint system design audit")
    sd_audit.add_argument("--path", default=".", help="Target directory")

    sd_tpl = sd_sub.add_parser("template", help="Generate resilience code templates")
    sd_tpl.add_argument("name", choices=["circuit-breaker", "singleflight", "jittered-cache"])

    # Graph group
    graph_parser = subparsers.add_parser("graph", help="Codebase context graph tools")
    graph_sub = graph_parser.add_subparsers(dest="graph_command")

    g_build = graph_sub.add_parser("build", help="Build context graph")
    g_build.add_argument("--path", default=".", help="Target directory")

    g_query = graph_sub.add_parser("query", help="Query context graph with GraphRAG")
    g_query.add_argument("query", help="Question or topic")
    g_query.add_argument("--path", default=".", help="Target directory")

    g_path = graph_sub.add_parser("path", help="Find path between two symbols")
    g_path.add_argument("source", help="Source symbol or file")
    g_path.add_argument("target", help="Target symbol or file")
    g_path.add_argument("--path", default=".", help="Target directory")

    # UI group
    ui_parser = subparsers.add_parser("ui", help="UI craft and unslopping tools")
    ui_sub = ui_parser.add_subparsers(dest="ui_command")
    ui_audit = ui_sub.add_parser("audit", help="Scan for vibecoded AI slop")
    ui_audit.add_argument("--path", default=".", help="Target directory")

    args = parser.parse_args()

    if args.command == "audit":
        run_full_audit(args)
    elif args.command == "sd":
        if args.sd_command == "audit":
            run_sd_audit(args)
        elif args.sd_command == "template":
            run_sd_template(args)
        else:
            sd_parser.print_help()
    elif args.command == "graph":
        if args.graph_command == "build":
            run_graph_build(args)
        elif args.graph_command == "query":
            run_graph_query(args)
        elif args.graph_command == "path":
            run_graph_path(args)
        else:
            graph_parser.print_help()
    elif args.command == "ui":
        if args.ui_command == "audit":
            run_ui_audit(args)
        else:
            ui_parser.print_help()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
