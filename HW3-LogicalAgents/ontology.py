
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Iterable, Tuple


class EntityKind(str, Enum):
    PERSON = "PERSON"
    ROOM = "ROOM"
    PROJECT = "PROJECT"

@dataclass(frozen=True, slots=True)
class Constant:
    """
    A typed constant symbol in the world.
    """
    name: str
    kind: EntityKind

    def __post_init__(self) -> None:
        if not isinstance(self.name, str) or not self.name.strip():
            raise ValueError("Constant.name must be a non-empty string.")


def Person(name: str) -> Constant:
    return Constant(name=name, kind=EntityKind.PERSON)

def Room(name: str) -> Constant:
    return Constant(name=name, kind=EntityKind.ROOM)

def Project(name: str) -> Constant:
    return Constant(name=name, kind=EntityKind.PROJECT)


@dataclass(frozen=True, slots=True)
class Predicate:
    name: str
    arity: int
    arg_kinds: Tuple[EntityKind, ...]

    def __post_init__(self) -> None:
        if not self.name or not isinstance(self.name, str):
            raise ValueError("Predicate.name must be a non-empty string.")
        if self.arity < 0:
            raise ValueError("Predicate.arity must be >= 0.")
        if len(self.arg_kinds) != self.arity:
            raise ValueError("Predicate.arg_kinds length must match arity.")
        

@dataclass(frozen=True, slots=True)
class Atom:
    """
    A ground atom: Predicate applied to typed Constants.
    """
    pred: Predicate
    args: Tuple[Constant, ...]

    def __post_init__(self) -> None:
        _validate_atom(self.pred, self.args)

    def __str__(self) -> str:
        if self.pred.arity == 0:
            return f"{self.pred.name}"
        return f"{self.pred.name}(" + ", ".join(a.name for a in self.args) + ")"

    def as_tuple(self) -> Tuple[str, Tuple[str, ...]]:
        return (self.pred.name, tuple(a.name for a in self.args))


def _validate_atom(pred: Predicate, args: Iterable[Any]) -> None:
    args = tuple(args)
    if len(args) != pred.arity:
        raise TypeError(
            f"{pred.name} expects {pred.arity} argument(s), got {len(args)}."
        )
    for i, (arg, expected_kind) in enumerate(zip(args, pred.arg_kinds)):
        if not isinstance(arg, Constant):
            raise TypeError(
                f"{pred.name} arg#{i} must be a Constant, got {type(arg).__name__}."
            )
        if arg.kind != expected_kind:
            raise TypeError(
                f"{pred.name} arg#{i} must be {expected_kind.value}, got {arg.kind.value} ({arg.name})."
            )


def make_atom(pred: Predicate, *args: Constant) -> Atom:
    return Atom(pred=pred, args=tuple(args))

# Roles
PRED_Student = Predicate("Student", 1, (EntityKind.PERSON,))
PRED_Professor = Predicate("Professor", 1, (EntityKind.PERSON,))
PRED_Dean = Predicate("Dean", 1, (EntityKind.PERSON,))

# Attributes
PRED_HasID = Predicate("HasID", 1, (EntityKind.PERSON,))
PRED_PassedSafetyCourse = Predicate("PassedSafetyCourse", 1, (EntityKind.PERSON,))
PRED_IsSecureLab = Predicate("IsSecureLab", 1, (EntityKind.ROOM,))

# Relationships
PRED_MemberOf = Predicate("MemberOf", 2, (EntityKind.PERSON, EntityKind.PROJECT))
PRED_ProjectRoom = Predicate("ProjectRoom", 2, (EntityKind.PROJECT, EntityKind.ROOM))
PRED_Mentor = Predicate("Mentor", 2, (EntityKind.PERSON, EntityKind.PERSON))
PRED_Office = Predicate("Office", 2, (EntityKind.PERSON, EntityKind.ROOM))

# State
PRED_InRoom = Predicate("InRoom", 2, (EntityKind.PERSON, EntityKind.ROOM))
PRED_DoorOpen = Predicate("DoorOpen", 1, (EntityKind.ROOM,))
PRED_Emergency = Predicate("Emergency", 1, (EntityKind.ROOM,))

# Goal
PRED_CanAccess = Predicate("CanAccess", 2, (EntityKind.PERSON, EntityKind.ROOM))

# Roles
def Student(x: Constant) -> Atom:
    return make_atom(PRED_Student, x)

def Professor(x: Constant) -> Atom:
    return make_atom(PRED_Professor, x)

def Dean(x: Constant) -> Atom:
    return make_atom(PRED_Dean, x)

# Attributes
def HasID(x: Constant) -> Atom:
    return make_atom(PRED_HasID, x)

def PassedSafetyCourse(x: Constant) -> Atom:
    return make_atom(PRED_PassedSafetyCourse, x)

def IsSecureLab(r: Constant) -> Atom:
    return make_atom(PRED_IsSecureLab, r)

# Relationships
def MemberOf(x: Constant, p: Constant) -> Atom:
    return make_atom(PRED_MemberOf, x, p)

def ProjectRoom(p: Constant, r: Constant) -> Atom:
    return make_atom(PRED_ProjectRoom, p, r)

def Mentor(x: Constant, y: Constant) -> Atom:
    return make_atom(PRED_Mentor, x, y)

def Office(x: Constant, r: Constant) -> Atom:
    return make_atom(PRED_Office, x, r)

# State
def InRoom(x: Constant, r: Constant) -> Atom:
    return make_atom(PRED_InRoom, x, r)

def DoorOpen(r: Constant) -> Atom:
    return make_atom(PRED_DoorOpen, r)

def Emergency(r: Constant) -> Atom:
    return make_atom(PRED_Emergency, r)

# Goal
def CanAccess(x: Constant, r: Constant) -> Atom:
    return make_atom(PRED_CanAccess, x, r)
