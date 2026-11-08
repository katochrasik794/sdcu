"""
SDCU System Design & Security Linter
Scans source files against the 20 Production Anti-Patterns.
"""

import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict, Any

@dataclass
class Finding:
    checkpoint_id: str
    category: str
    severity: str
    message: str
    file_path: str
    line_number: int
    matched_snippet: str
    remediation: str

class SystemDesignLinter:
    def __init__(self, root_dir: str = "."):
        self.root_dir = Path(root_dir)

    def scan(self) -> List[Finding]:
        findings: List[Finding] = []
        
        # Check 07: .env committed or not in .gitignore
        self._check_env_in_git(findings)

        # File-based static analysis
        for root, dirs, files in os.walk(self.root_dir):
            # Skip hidden and vendor directories
            dirs[:] = [d for d in dirs if not d.startswith(".") and d not in ("node_modules", "vendor", "dist", "build", "__pycache__")]
            
            for file in files:
                ext = Path(file).suffix.lower()
                if ext in (".ts", ".tsx", ".js", ".jsx", ".py", ".go", ".rs", ".sql"):
                    path = Path(root) / file
                    self._scan_file(path, findings)

        return findings

    def _check_env_in_git(self, findings: List[Finding]):
        gitignore_path = self.root_dir / ".gitignore"
        env_files = list(self.root_dir.glob(".env*"))
        env_files = [f for f in env_files if f.name != ".env.example"]

        if env_files:
            if not gitignore_path.exists():
                findings.append(Finding(
                    checkpoint_id="07",
                    category="SECURITY",
                    severity="CRITICAL",
                    message=".env file exists but no .gitignore found in project root",
                    file_path=".env",
                    line_number=1,
                    matched_snippet=f"Found: {[f.name for f in env_files]}",
                    remediation="Add .env* to .gitignore immediately and revoke any committed secrets."
                ))
            else:
                content = gitignore_path.read_text(encoding="utf-8", errors="ignore")
                if ".env" not in content:
                    findings.append(Finding(
                        checkpoint_id="07",
                        category="SECURITY",
                        severity="CRITICAL",
                        message=".env file exists but '.env' is missing from .gitignore",
                        file_path=".gitignore",
                        line_number=1,
                        matched_snippet=".gitignore missing .env",
                        remediation="Append '.env*' to .gitignore to prevent secret leaks to GitHub."
                    ))

    def _scan_file(self, path: Path, findings: List[Finding]):
        try:
            content = path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            return

        lines = content.splitlines()
        rel_path = str(path.relative_to(self.root_dir))

        # Do not flag the linter itself
        if "sdcu_core/sd/linter.py" in rel_path or "tests/" in rel_path:
            return

        for idx, line in enumerate(lines, start=1):
            stripped = line.strip()
            # Skip pure comments
            if stripped.startswith(("//", "#", "/*", "*")):
                continue
            # Check 01: API keys in frontend
            if re.search(r'NEXT_PUBLIC_.*(?:SECRET|PRIVATE|API_KEY|TOKEN)', line, re.IGNORECASE):
                findings.append(Finding(
                    checkpoint_id="01",
                    category="SECURITY",
                    severity="CRITICAL",
                    message="Sensitive secret/key exposed with public client prefix",
                    file_path=rel_path,
                    line_number=idx,
                    matched_snippet=line.strip()[:100],
                    remediation="Never expose secret tokens in NEXT_PUBLIC_ variables. Keep them server-side."
                ))

            # Check 03: SQL Injection via string interpolation
            if re.search(r'(?:SELECT|INSERT|UPDATE|DELETE).*\$\{.*\}', line, re.IGNORECASE) or \
               re.search(r'(?:SELECT|INSERT|UPDATE|DELETE).*\+\s*[a-zA-Z0-9_]+', line, re.IGNORECASE):
                findings.append(Finding(
                    checkpoint_id="03",
                    category="SECURITY",
                    severity="HIGH",
                    message="Possible SQL Injection via string interpolation or concatenation",
                    file_path=rel_path,
                    line_number=idx,
                    matched_snippet=line.strip()[:100],
                    remediation="Use parameterized queries ($1, ? or ORM parameters) instead of string formatting."
                ))

            # Check 04: XSS via dangerouslySetInnerHTML
            if "dangerouslySetInnerHTML" in line or "innerHTML" in line:
                findings.append(Finding(
                    checkpoint_id="04",
                    category="SECURITY",
                    severity="HIGH",
                    message="Direct HTML injection hazard without verified sanitization (XSS risk)",
                    file_path=rel_path,
                    line_number=idx,
                    matched_snippet=line.strip()[:100],
                    remediation="Sanitize raw HTML with DOMPurify or prefer standard text rendering."
                ))

            # Check 06: Wildcard CORS
            if re.search(r'Access-Control-Allow-Origin.*\*', line) or re.search(r'cors\(\s*\{\s*origin\s*:\s*[\'"]\*[\'"]', line):
                findings.append(Finding(
                    checkpoint_id="06",
                    category="SECURITY",
                    severity="MEDIUM",
                    message="Wildcard CORS '*' detected with open origin access",
                    file_path=rel_path,
                    line_number=idx,
                    matched_snippet=line.strip()[:100],
                    remediation="Restrict CORS to trusted origins array instead of wildcard '*'."
                ))

            # Check 12: Loop containing DB query (Potential N+1)
            if re.search(r'(?:for\s*\(|forEach|\.map\s*\().*(?:await\s+db\.|await\s+prisma\.|await\s+repository\.)', line):
                findings.append(Finding(
                    checkpoint_id="12",
                    category="SCALE",
                    severity="HIGH",
                    message="Database query executed inside iteration (Potential N+1 bottleneck)",
                    file_path=rel_path,
                    line_number=idx,
                    matched_snippet=line.strip()[:100],
                    remediation="Batch queries using DataLoader, SQL JOINs, or 'IN (...)' queries."
                ))

            # Check 13: Caching without jitter
            if re.search(r'redis\.(?:set|setex)\([^,]+,\s*[0-9]+', line):
                findings.append(Finding(
                    checkpoint_id="13",
                    category="SCALE",
                    severity="MEDIUM",
                    message="Hardcoded static cache TTL detected without jitter",
                    file_path=rel_path,
                    line_number=idx,
                    matched_snippet=line.strip()[:100],
                    remediation="Add randomized jitter to cache TTL: TTL = BaseTTL + RandomJitter to prevent stampedes."
                ))
