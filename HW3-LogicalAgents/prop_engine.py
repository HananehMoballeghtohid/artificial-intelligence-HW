from typing import Iterable
from ontology import Atom, Constant, CanAccess


def evaluate_access(x: Constant, r: Constant, facts: Iterable[Atom]) -> bool:
    """
    Propositional evaluation:
    True iff CanAccess(x,r) exists in ground facts.
    """
    return CanAccess(x, r) in set(facts)
