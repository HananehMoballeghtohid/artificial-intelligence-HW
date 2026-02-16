from __future__ import annotations
from typing import Set, Iterable

from ontology import Atom, Constant, CanAccess
from rules_kb import _blocking_rules, _granting_rules


Facts = Set[Atom]


def forward_chain_access(
    x: Constant,
    r: Constant,
    facts: Iterable[Atom],
    *,
    closed_world: bool = True,
) -> Facts:
    """
    Applies FOL rules and derives new facts.
    Specifically derives CanAccess(x,r) if granting rules fire
    and no blocking rules apply.
    """

    facts_set: Facts = set(facts)
    new_facts = set(facts_set)

    # Evaluate rules
    blocking = _blocking_rules(x, r, facts_set, closed_world=closed_world)
    granting = _granting_rules(x, r, facts_set)

    if len(blocking) == 0 and len(granting) > 0:
        new_facts.add(CanAccess(x, r))

    return new_facts
