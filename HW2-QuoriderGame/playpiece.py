from dataclasses import dataclass
from typing import Tuple

Position = tuple[int, int]


class PlayPiece:
    """Marker base class. No shared behavior."""

    pass


@dataclass(frozen=True)
class Pawn(PlayPiece):
    row: int
    col: int
    owner: str  # "MAX" or "MIN"

    @property
    def pos(self) -> Position:
        return (self.row, self.col)

    def move(self, to: Position) -> "Pawn":
        r, c = to
        return Pawn(row=r, col=c, owner=self.owner)


@dataclass(frozen=True)
class Wall(PlayPiece):
    row: int
    col: int
    orientation: str  # "H" or "V"

    def blocks_edge(self, a: Position, b: Position) -> bool:
        r1, c1 = a
        r2, c2 = b

        # vertical movement blocked by horizontal wall
        if c1 == c2 and self.orientation == "H":
            r = min(r1, r2)
            return self.row == r and self.col in {c1, c1 - 1}

        # horizontal movement blocked by vertical wall
        if r1 == r2 and self.orientation == "V":
            c = min(c1, c2)
            return self.col == c and self.row in {r1, r1 - 1}

        return False

    @staticmethod
    def place(row: int, col: int, orientation: str) -> "Wall":
        if orientation not in ("H", "V"):
            raise ValueError("Wall orientation must be 'H' or 'V'")
        if not (1 <= row <= 8 and 1 <= col <= 8):
            raise ValueError("Wall coordinates out of bounds")
        return Wall(row=row, col=col, orientation=orientation)
