from collections import deque
from typing import List, Tuple, FrozenSet
from state import State
from playpiece import Pawn, Wall

Position = Tuple[int, int]


def edge_blocked(state: State, a: Position, b: Position) -> bool:
    return any(w.blocks_edge(a, b) for w in state.walls)


def wall_conflicts(state: State, new_wall: Wall) -> bool:
    for w in state.walls:
        if w.row == new_wall.row and w.col == new_wall.col:
            return True
        if (
            w.orientation != new_wall.orientation
            and w.row == new_wall.row
            and w.col == new_wall.col
        ):
            return True
    return False


def pawn_moves(state: State) -> List[Position]:
    pawn = state.p1 if state.active_player == "MAX" else state.p2
    opp = state.p2 if state.active_player == "MAX" else state.p1

    r, c = pawn.row, pawn.col
    moves: List[Position] = []

    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nr, nc = r + dr, c + dc
        if 1 <= nr <= 9 and 1 <= nc <= 9:
            if (nr, nc) != (opp.row, opp.col) and not edge_blocked(
                state, (r, c), (nr, nc)
            ):
                moves.append((nr, nc))

    dr, dc = opp.row - r, opp.col - c
    if abs(dr) + abs(dc) == 1 and not edge_blocked(state, (r, c), (opp.row, opp.col)):
        br, bc = opp.row + dr, opp.col + dc
        if (
            1 <= br <= 9
            and 1 <= bc <= 9
            and not edge_blocked(state, (opp.row, opp.col), (br, bc))
        ):
            moves.append((br, bc))
        else:
            if dr == 0:
                for d in [-1, 1]:
                    nr = opp.row + d
                    if 1 <= nr <= 9 and not edge_blocked(
                        state, (opp.row, opp.col), (nr, opp.col)
                    ):
                        moves.append((nr, opp.col))
            else:
                for d in [-1, 1]:
                    nc = opp.col + d
                    if 1 <= nc <= 9 and not edge_blocked(
                        state, (opp.row, opp.col), (opp.row, nc)
                    ):
                        moves.append((opp.row, nc))
    return moves


def has_path(start: Pawn, goal_row: int, walls: FrozenSet[Wall]) -> bool:
    q = deque([start.row, start.col])
    seen = {(start.row, start.col)}

    q = deque([start.pos])
    seen = {start.pos}

    while q:
        r, c = q.popleft()
        if r == goal_row:
            return True
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 1 <= nr <= 9 and 1 <= nc <= 9 and (nr, nc) not in seen:
                if not any(w.blocks_edge((r, c), (nr, nc)) for w in walls):
                    seen.add((nr, nc))
                    q.append((nr, nc))
    return False


def wall_moves(state: State) -> List[Wall]:
    walls_left = state.p1_walls if state.active_player == "MAX" else state.p2_walls
    if walls_left == 0:
        return []

    moves: List[Wall] = []

    for r in range(1, 9):
        for c in range(1, 9):
            for o in ("H", "V"):
                w = Wall.place(r, c, o)
                if wall_conflicts(state, w):
                    continue
                new_walls = frozenset(state.walls | {w})
                if not has_path(state.p1, 9, new_walls):
                    continue
                if not has_path(state.p2, 1, new_walls):
                    continue
                moves.append(w)
    return moves


def legal_moves(state: State):
    moves = []
    for pos in pawn_moves(state):
        moves.append(("MOVE", pos))
    for wall in wall_moves(state):
        moves.append(("WALL", wall))
    return moves


def apply(state: State, move) -> State:
    kind, payload = move
    if kind == "MOVE":
        if state.active_player == "MAX":
            return State(
                p1=state.p1.move(payload),
                p2=state.p2,
                p1_walls=state.p1_walls,
                p2_walls=state.p2_walls,
                walls=state.walls,
                active_player="MIN",
            )
        else:
            return State(
                p1=state.p1,
                p2=state.p2.move(payload),
                p1_walls=state.p1_walls,
                p2_walls=state.p2_walls,
                walls=state.walls,
                active_player="MAX",
            )
    else:  # WALL
        wall: Wall = payload
        new_walls = frozenset(state.walls | {wall})
        if state.active_player == "MAX":
            return State(
                p1=state.p1,
                p2=state.p2,
                p1_walls=state.p1_walls - 1,
                p2_walls=state.p2_walls,
                walls=new_walls,
                active_player="MIN",
            )
        else:
            return State(
                p1=state.p1,
                p2=state.p2,
                p1_walls=state.p1_walls,
                p2_walls=state.p2_walls - 1,
                walls=new_walls,
                active_player="MAX",
            )


def is_terminal(state: State) -> bool:
    return state.p1.row == 9 or state.p2.row == 1
