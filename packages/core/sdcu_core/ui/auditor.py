"""
SDCU UI Craft & Slop Auditor
Detects markers of generic AI-generated interfaces and checks adherence to the 9-pass design framework.
"""

import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import List

@dataclass
class SlopFinding:
    sign: str
    severity: str
    message: str
    file_path: str
    line_number: int
    matched_snippet: str
    pass_number: int
    pass_name: str
    remediation: str

class UIAuditor:
    def __init__(self, root_dir: str = "."):
        self.root_dir = Path(root_dir)

    def scan(self) -> List[SlopFinding]:
        findings: List[SlopFinding] = []

        for root, dirs, files in os.walk(self.root_dir):
            dirs[:] = [d for d in dirs if not d.startswith(".") and d not in ("node_modules", "vendor", "dist", "build", "__pycache__")]
            
            for file in files:
                ext = Path(file).suffix.lower()
                if ext in (".tsx", ".jsx", ".html", ".vue", ".svelte", ".css"):
                    path = Path(root) / file
                    self._scan_file(path, findings)

        return findings

    def _scan_file(self, path: Path, findings: List[SlopFinding]):
        try:
            content = path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            return

        lines = content.splitlines()
        rel_path = str(path.relative_to(self.root_dir))

        for idx, line in enumerate(lines, start=1):
            # Sign 1: Purple / Indigo gradients (AI hallmark)
            if re.search(r'bg-gradient-to-[a-z]+\s+from-(?:purple|violet|indigo)-[0-9]+\s+to-(?:pink|fuchsia|cyan)-[0-9]+', line):
                findings.append(SlopFinding(
                    sign="AI Purple Gradient",
                    severity="HIGH",
                    message="Generic AI purple/violet gradient detected",
                    file_path=rel_path,
                    line_number=idx,
                    matched_snippet=line.strip()[:100],
                    pass_number=2,
                    pass_name="Color / Palette",
                    remediation="Replace loud multi-hue gradient with quiet tinted neutral and a single sharp brand accent."
                ))

            # Sign 2: Neon glowing box-shadows
            if re.search(r'shadow-\[0_0_[0-9]+px_rgba\([0-9]+,\s*[0-9]+,\s*[0-9]+', line) or "glow" in line.lower() and "shadow" in line.lower():
                findings.append(SlopFinding(
                    sign="Neon Chrome Glow",
                    severity="MEDIUM",
                    message="Blinding neon glow on container/card chrome",
                    file_path=rel_path,
                    line_number=idx,
                    matched_snippet=line.strip()[:100],
                    pass_number=3,
                    pass_name="Quiet Chrome",
                    remediation="Keep chrome quiet: use crisp 1px borders with subtle dark/light contrast instead of glowing edges."
                ))

            # Sign 3: Emoji badges in buttons/headers
            if re.search(r'(?:✨|🚀|⚡|🔥|💡)\s*(?:New|AI|Smart|Supercharge|Instant)', line):
                findings.append(SlopFinding(
                    sign="Emoji Badge Spam",
                    severity="MEDIUM",
                    message="Unironic emoji label in interface chrome",
                    file_path=rel_path,
                    line_number=idx,
                    matched_snippet=line.strip()[:100],
                    pass_number=3,
                    pass_name="Icons & Badges",
                    remediation="Remove gratuitous emoji; use clean typographic pills or deliberate single-color Lucide icons."
                ))

            # Sign 4: AI Buzzword Copy
            if re.search(r'\b(seamlessly|revolutionize|unleash|effortlessly|supercharge)\b', line, re.IGNORECASE):
                findings.append(SlopFinding(
                    sign="AI Marketing Slop Copy",
                    severity="LOW",
                    message="AI cliché buzzword detected in UI copy",
                    file_path=rel_path,
                    line_number=idx,
                    matched_snippet=line.strip()[:100],
                    pass_number=6,
                    pass_name="Copy & Content",
                    remediation="Rewrite with punchy, concrete human language stating what the product actually does."
                ))
