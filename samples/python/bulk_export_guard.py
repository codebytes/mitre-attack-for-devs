"""
MITRE ATT&CK T1213 (Data from Information Repositories) and
T1567 (Exfiltration Over Web Service).

An attacker with a valid session makes requests that are individually legal.
The identity provider sees a healthy sign-in and nothing more. Only the
application knows that a support agent just asked for 40,000 customer rows
when the job normally needs five.

This is deliberately NOT an anomaly score. A fixed, explainable budget is
something you can reason about, test, and put in a runbook. A floating
"suspicion score" is something nobody can debug at 3am.

Reference:
  https://attack.mitre.org/techniques/T1213/
  https://attack.mitre.org/techniques/T1567/
"""

import logging
import time
from collections import deque
from dataclasses import dataclass, field
from typing import Deque, Dict, Optional, Tuple

logger = logging.getLogger(__name__)


class ExportDenied(Exception):
    """Raised when an export exceeds policy. Callers must not return data."""


@dataclass(frozen=True)
class ExportPolicy:
    """Per-role limits. Derived from what the job actually requires."""

    max_rows_per_request: int
    max_rows_per_hour: int
    require_step_up_over_rows: int


# Start from the real workflow, not from a round number. If support genuinely
# needs 500 rows to do their job, 500 is the limit; anything more is a question.
POLICIES: Dict[str, ExportPolicy] = {
    "support": ExportPolicy(
        max_rows_per_request=500,
        max_rows_per_hour=2_000,
        require_step_up_over_rows=200,
    ),
    "analyst": ExportPolicy(
        max_rows_per_request=10_000,
        max_rows_per_hour=50_000,
        require_step_up_over_rows=5_000,
    ),
}


@dataclass
class _Window:
    """Rolling one-hour record of granted rows."""

    events: Deque[Tuple[float, int]] = field(default_factory=deque)

    def trim(self, now: float, window_seconds: int = 3600) -> None:
        cutoff = now - window_seconds
        while self.events and self.events[0][0] < cutoff:
            self.events.popleft()

    def total(self) -> int:
        return sum(rows for _, rows in self.events)


class BulkExportGuard:
    """
    Enforces an export budget and emits ATT&CK-tagged events.

    In production the counters belong in shared, atomic storage (Redis INCR,
    a database row with a lock). An in-process dict is per-instance and resets
    on deploy, which an attacker can simply wait out.
    """

    def __init__(self, policies: Optional[Dict[str, ExportPolicy]] = None) -> None:
        self._policies = policies or POLICIES
        self._windows: Dict[str, _Window] = {}

    def authorize_export(
        self,
        *,
        subject: str,
        tenant: str,
        role: str,
        requested_rows: int,
        step_up_satisfied: bool = False,
        now: Optional[float] = None,
    ) -> int:
        """
        Decide an export BEFORE the query runs.

        Checking after the rows are already in memory means the expensive query
        still ran and the data is one serialization bug away from leaving.

        Returns the number of rows the caller is permitted to read.
        Raises ExportDenied when the request must not proceed.
        """
        now = time.time() if now is None else now
        policy = self._policies.get(role)
        if policy is None:
            self._emit("T1213", "denied", subject, tenant, role, requested_rows,
                       "no export policy defined for role")
            raise ExportDenied(f"role {role!r} is not permitted to export")

        if requested_rows > policy.max_rows_per_request:
            self._emit("T1213", "denied", subject, tenant, role, requested_rows,
                       f"request exceeds per-request cap of {policy.max_rows_per_request}")
            raise ExportDenied("export request too large")

        window = self._windows.setdefault(subject, _Window())
        window.trim(now)
        already = window.total()

        if already + requested_rows > policy.max_rows_per_hour:
            # This is the signal that matters: each request looked fine, the
            # accumulation did not. T1567 is about the aggregate, not the call.
            self._emit("T1567", "denied", subject, tenant, role, requested_rows,
                       f"hourly budget exhausted ({already}/{policy.max_rows_per_hour} rows)")
            raise ExportDenied("hourly export budget exhausted")

        if requested_rows > policy.require_step_up_over_rows and not step_up_satisfied:
            self._emit("T1213", "step_up_required", subject, tenant, role, requested_rows,
                       "large export requires a recently proven credential")
            raise ExportDenied("step-up authentication required")

        window.events.append((now, requested_rows))
        logger.info(
            "export granted",
            extra={"subject": subject, "tenant": tenant, "rows": requested_rows},
        )
        return requested_rows

    def _emit(self, technique: str, decision: str, subject: str, tenant: str,
              role: str, rows: int, reason: str) -> None:
        """
        Structured, correlatable, and free of customer data.

        Log the shape of the request, never the result set and never the
        predicate values, which are themselves sensitive.
        """
        logger.warning(
            "export decision",
            extra={
                "event": "export.decision",
                "attack_technique": technique,
                "decision": decision,
                "subject": subject,
                "tenant": tenant,
                "role": role,
                "requested_rows": rows,
                "reason": reason,
            },
        )


# =============================================================================
# DEMONSTRATION
# =============================================================================

def _demo() -> None:
    guard = BulkExportGuard()
    now = time.time()

    print("=" * 68)
    print("Export budget for a support agent (500/request, 2000/hour)")
    print("=" * 68)

    print("\n1. Routine lookup of 50 rows:")
    print(f"   granted {guard.authorize_export(subject='u1', tenant='t1', role='support', requested_rows=50, now=now)} rows")

    print("\n2. 400 rows without step-up (threshold is 200):")
    try:
        guard.authorize_export(subject="u1", tenant="t1", role="support", requested_rows=400, now=now)
    except ExportDenied as exc:
        print(f"   denied: {exc}")

    print("\n3. Same 400 rows after the user re-authenticated:")
    print(f"   granted {guard.authorize_export(subject='u1', tenant='t1', role='support', requested_rows=400, step_up_satisfied=True, now=now)} rows")

    print("\n4. Drip-feed: 500 rows at a time, each individually legal:")
    for attempt in range(1, 8):
        try:
            guard.authorize_export(
                subject="u2", tenant="t1", role="support",
                requested_rows=500, step_up_satisfied=True, now=now,
            )
            print(f"   request {attempt}: granted 500 rows")
        except ExportDenied as exc:
            print(f"   request {attempt}: denied — {exc}")
            print("\n   The per-request check passed every time. The hourly budget")
            print("   is what caught the accumulation (T1567).")
            break


if __name__ == "__main__":
    logging.basicConfig(level=logging.WARNING, format="   [%(levelname)s] %(message)s")
    _demo()
    print("\n" + "=" * 68)
    print("Key points")
    print("=" * 68)
    print("1. Decide before the query runs, not after the rows are in memory.")
    print("2. Derive limits from the real workflow so they are defensible.")
    print("3. Budget the aggregate; individually-legal requests are the attack.")
    print("4. Require step-up for large exports, and let the IdP prove it.")
    print("5. Use shared atomic counters in production, not per-process state.")
    print("6. Give legitimate bulk work a reviewed path instead of a raised cap.")
    print("=" * 68)
