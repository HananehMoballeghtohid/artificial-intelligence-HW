import random
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
    def get_initial_state(random_turn: bool = False) -> "State":
        player = random.choice(["MAX", "MIN"]) if random_turn else "MAX"
        opponent = "MIN" if player == "MAX" else "MAX"
        return State(
            p1=Pawn(1, 5, player),
            p2=Pawn(9, 5, opponent),
            p1_walls=10,
            p2_walls=10,
            walls=frozenset(),
            active_player=player,
        )

    def display(self):
        size = 9
        board_rows = 2 * size - 1
        board_cols = 2 * size - 1
        grid = [[" " for _ in range(board_cols)] for _ in range(board_rows)]

        for r in range(size):
            for c in range(size):
                grid[2 * r][2 * c] = "."

        grid[2 * (self.p1.row - 1)][2 * (self.p1.col - 1)] = "1"
        grid[2 * (self.p2.row - 1)][2 * (self.p2.col - 1)] = "2"

        for w in self.walls:
            if w.orientation == "H":
                row = 2 * (w.row - 1) + 1
                col = 2 * (w.col - 1)
                grid[row][col] = "-"
                grid[row][col + 1] = "-"
                grid[row][col + 2] = "-"  # span full width
            else:
                row = 2 * (w.row - 1)
                col = 2 * (w.col - 1) + 1
                grid[row][col] = "|"
                grid[row + 1][col] = "|"

        col_nums = "   " + " ".join(str(c) for c in range(1, size + 1))
        print(col_nums)
        for r in range(board_rows):
            row_label = f"{r//2 + 1} " if r % 2 == 0 else "  "
            print(row_label + " ".join(grid[r]))
