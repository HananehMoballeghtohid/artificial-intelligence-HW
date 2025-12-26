from dataclasses import dataclass, field
from typing import FrozenSet
from playpiece import Pawn, Wall


@dataclass(frozen=True)
class State:
    p1: Pawn
    p2: Pawn
    p1_walls: int
    p2_walls: int
    walls: FrozenSet[Wall] = field(default_factory=frozenset)
    active_player: str = "MAX"  # "MAX" or "MIN"

    @staticmethod
    def get_initial_state() -> "State":
        return State(
            p1=Pawn(1, 5, "MAX"),
            p2=Pawn(9, 5, "MIN"),
            p1_walls=10,
            p2_walls=10,
            walls=frozenset(),
            active_player="MAX",
        )
