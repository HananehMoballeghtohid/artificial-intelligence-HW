from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Optional, Sequence, Set, Tuple

from ontology import (
    Atom,
    Constant,
    CanAccess,
    Dean,
    DoorOpen,
    Emergency,
    HasID,
    InRoom,
    IsSecureLab,
    MemberOf,
    Mentor,
    Office,
    PassedSafetyCourse,
    Professor,
    ProjectRoom,
    Student,
)

Facts = Set[Atom]

@dataclass(frozen=True, slots=True)
class DecisionResult:
    allowed: bool
    blocking_reasons: Tuple[str, ...]
    granting_reasons: Tuple[str, ...]

def _has(facts: Facts, atom: Atom) -> bool:
    return atom in facts

def _blocking_rules(x: Constant, r: Constant, facts: Facts, *, closed_world: bool = True) -> List[str]:
    """
    Blocking rules (higher priority):
      1) Emergency(r) -> ¬CanAccess(x, r)
      2) ¬DoorOpen(r) -> ¬CanAccess(x, r)

    Note: For rule (2), we treat "not DoorOpen" under a closed-world assumption:
      - if DoorOpen(r) is NOT in facts => considered closed (blocked).
    """
    reasons: List[str] = []

    if _has(facts, Emergency(r)):
        reasons.append(f"Blocked: Emergency({r.name}) is true.")

    if closed_world:
        if not _has(facts, DoorOpen(r)):
            reasons.append(f"Blocked: DoorOpen({r.name}) is not known/false (closed-world).")
    else:
        pass

    return reasons


def _granting_rules(x: Constant, r: Constant, facts: Facts) -> List[str]:
    """
    Granting rules (need at least one true if no blockers):
      G1) Dean(x) -> CanAccess(x, r)
      G2) Professor(x) ∧ Office(x,r) -> CanAccess(x,r)
      G3) Student(x) ∧ MemberOf(x,p) ∧ ProjectRoom(p,r) ∧ HasID(x) -> CanAccess(x,r)
      G4) Student(x) ∧ Mentor(y,x) ∧ InRoom(y,r) -> CanAccess(x,r)
      G5) HasID(x) ∧ IsSecureLab(r) ∧ PassedSafetyCourse(x) -> CanAccess(x,r)
    """
    reasons: List[str] = []

    # G1: dean can access any room
    if _has(facts, Dean(x)):
        reasons.append(f"Grant: Dean({x.name}) implies access to any room (incl. {r.name}).")

    # G2: professor can access their office
    if _has(facts, Professor(x)) and _has(facts, Office(x, r)):
        reasons.append(f"Grant: Professor({x.name}) and Office({x.name},{r.name}).")

    # G3: student project room access + has ID
    if _has(facts, Student(x)) and _has(facts, HasID(x)):
        # exists p: MemberOf(x,p) and ProjectRoom(p,r)
        # we discover p by scanning facts
        for a in facts:
            if a.pred.name == "MemberOf" and len(a.args) == 2:
                px, p = a.args
                if px == x:
                    if _has(facts, ProjectRoom(p, r)):
                        reasons.append(
                            f"Grant: Student({x.name}) ∧ HasID({x.name}) ∧ MemberOf({x.name},{p.name}) "
                            f"∧ ProjectRoom({p.name},{r.name})."
                        )
                        break

    # G4: student can enter if their mentor is in the room
    # rule: Student(x) ∧ Mentor(y,x) ∧ InRoom(y,r) -> CanAccess(x,r)
    if _has(facts, Student(x)):
        for a in facts:
            if a.pred.name == "Mentor" and len(a.args) == 2:
                y, mentee = a.args
                if mentee == x and _has(facts, InRoom(y, r)):
                    reasons.append(
                        f"Grant: Student({x.name}) ∧ Mentor({y.name},{x.name}) ∧ InRoom({y.name},{r.name})."
                    )
                    break

    # G5: secure lab requires ID + safety course
    if _has(facts, HasID(x)) and _has(facts, IsSecureLab(r)) and _has(facts, PassedSafetyCourse(x)):
        reasons.append(
            f"Grant: HasID({x.name}) ∧ IsSecureLab({r.name}) ∧ PassedSafetyCourse({x.name})."
        )

    return reasons


def decide_access(
    x: Constant,
    r: Constant,
    facts: Iterable[Atom],
    *,
    closed_world: bool = True,
) -> DecisionResult:
    """
    Implements:
      Decision = (¬BlockingRules) ∧ (∨ GrantingRules)

    - If any blocker triggers => denied (even if granting rules trigger).
    - If no blocker triggers AND at least one grant triggers => allowed.
    - Otherwise => denied.
    """
    facts_set: Facts = set(facts)

    blocking = _blocking_rules(x, r, facts_set, closed_world=closed_world)
    granting = _granting_rules(x, r, facts_set)

    allowed = (len(blocking) == 0) and (len(granting) > 0)

    return DecisionResult(
        allowed=allowed,
        blocking_reasons=tuple(blocking),
        granting_reasons=tuple(granting),
    )


def goal_can_access(x: Constant, r: Constant) -> Atom:
    return CanAccess(x, r)

