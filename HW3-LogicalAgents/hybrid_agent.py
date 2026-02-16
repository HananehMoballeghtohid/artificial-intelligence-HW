from typing import Iterable, Set
from ontology import *
from fol_engine import forward_chain_access
from rules_kb import _blocking_rules, _granting_rules
from prop_engine import evaluate_access


class HybridAccessAgent:

    def __init__(self, closed_world: bool = True):
        self.closed_world = closed_world

    def decide_with_report(self, x: Constant, r: Constant, facts: Iterable[Atom]) -> str:

        facts = set(facts)
        # Phase 1 — FOL Grounding
        report = []
        report.append("## Phase 1: First-Order Logic Inference (FOL Grounding)\n")

        granting = _granting_rules(x, r, facts)
        blocking = _blocking_rules(x, r, facts, closed_world=self.closed_world)

        if not granting:
            report.append("• No granting rule activated.\n")
        else:
            report.append("• Granting rules activated:\n")
            for g in granting:
                report.append(f"  - {g}")

        # Show discovered base facts
        report.append("\n• Facts available:")
        for f in facts:
            report.append(f"  - {str(f)}")

        # Generate derived facts
        extended_facts = forward_chain_access(
            x, r, facts, closed_world=self.closed_world
        )

        if CanAccess(x, r) in extended_facts:
            report.append(f"\n• New proposition generated: CanAccess({x.name}, {r.name})")
        else:
            report.append(f"\n• No new CanAccess proposition derived.")
        # Phase 2 — Propositional Logic
        report.append("\n---\n")
        report.append("## Phase 2: Checking Constraints (Propositional Logic)\n")

        report.append("• Checking Blocking Rules:")

        if not blocking:
            report.append("  - No blocking constraints triggered.")
        else:
            for b in blocking:
                report.append(f"  - {b}")

        decision = evaluate_access(x, r, extended_facts)

        report.append("\n## Conclusion:")

        if decision:
            report.append("No blocking constraints found, and at least one permission is active.")
            report.append("\n### Final Result: **True (Access Granted)**")
        else:
            if blocking:
                report.append("Access denied due to blocking rule.")
            else:
                report.append("No granting rule satisfied.")
            report.append("\n### Final Result: **False (Access Denied)**")

        return "\n".join(report)
