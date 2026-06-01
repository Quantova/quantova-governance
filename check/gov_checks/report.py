"""Check results, severities, and reporting."""

from dataclasses import dataclass, field
from typing import List, Optional

PASS = "PASS"
WARN = "WARN"
FAIL = "FAIL"
SKIP = "SKIP"
INFO = "INFO"


@dataclass
class Result:
    check: str
    status: str
    detail: str = ""
    category: str = "general"


@dataclass
class Report:
    results: List[Result] = field(default_factory=list)

    def add(self, check: str, status: str, detail: str = "", category: str = "general") -> None:
        self.results.append(Result(check, status, detail, category))

    def counts(self) -> dict:
        c = {PASS: 0, WARN: 0, FAIL: 0, SKIP: 0, INFO: 0}
        for r in self.results:
            c[r.status] = c.get(r.status, 0) + 1
        return c

    def ok(self) -> bool:
        """Overall pass = no FAILs (warnings/skips do not fail the run)."""
        return self.counts()[FAIL] == 0

    def exit_code(self) -> int:
        return 0 if self.ok() else 1

    # --- rendering ---------------------------------------------------------
    _ICON = {PASS: "PASS", WARN: "WARN", FAIL: "FAIL", SKIP: "SKIP", INFO: "INFO"}

    def to_text(self) -> str:
        lines = []
        cat = None
        for r in self.results:
            if r.category != cat:
                cat = r.category
                lines.append(f"\n[{cat}]")
            tag = self._ICON.get(r.status, r.status)
            line = f"  {tag:4}  {r.check}"
            if r.detail:
                line += f" — {r.detail}"
            lines.append(line)
        c = self.counts()
        lines.append("")
        lines.append("-" * 60)
        lines.append(f"  {c[PASS]} pass · {c[WARN]} warn · {c[FAIL]} fail · {c[SKIP]} skip")
        lines.append("  RESULT: " + ("OK" if self.ok() else "FAILURES PRESENT"))
        lines.append("-" * 60)
        return "\n".join(lines)

    def to_dict(self) -> dict:
        return {
            "results": [
                {"check": r.check, "status": r.status, "detail": r.detail, "category": r.category}
                for r in self.results
            ],
            "summary": self.counts(),
            "ok": self.ok(),
        }
