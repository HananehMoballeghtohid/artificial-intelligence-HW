import numpy as np

# Color mapping
COLORS = {"W": 1, "Y": 2, "R": 3, "O": 4, "B": 5, "G": 6}
REV_COLORS = {v: k for k, v in COLORS.items()}


class RubiksCube4:
    def __init__(self):
        # Use a 4x4x4x3 integer array for colors
        self.cubies = np.zeros((4, 4, 4, 3), dtype=np.int8)
        self.initialize_colors()
        self.solved_hash = self.serialize_colors()

    def initialize_colors(self):
        for x in range(4):
            for y in range(4):
                for z in range(4):
                    # x_face, y_face, z_face
                    self.cubies[x, y, z, 0] = (
                        COLORS["R"] if x == 0 else COLORS["O"] if x == 3 else 0
                    )
                    self.cubies[x, y, z, 1] = (
                        COLORS["B"] if y == 0 else COLORS["G"] if y == 3 else 0
                    )
                    self.cubies[x, y, z, 2] = (
                        COLORS["Y"] if z == 0 else COLORS["W"] if z == 3 else 0
                    )

    def display_cube(self):
        print("Rubik's Cube 4x4:")
        print("=" * 50)
        faces = {
            "Front (White)": self.get_face("z", 3),
            "Back (Yellow)": self.get_face("z", 0),
            "Right (Orange)": self.get_face("x", 3),
            "Left (Red)": self.get_face("x", 0),
            "Up (Green)": self.get_face("y", 3),
            "Down (Blue)": self.get_face("y", 0),
        }
        for name, face in faces.items():
            display_face = np.vectorize(lambda c: REV_COLORS[c] if c != 0 else " ")
            print(f"\n{name}:")
            print(display_face(face))

    def get_face(self, axis, coord):
        face = np.zeros((4, 4), dtype=np.int8)
        if axis == "x":
            for y in range(4):
                for z in range(4):
                    face[y, z] = self.cubies[coord, y, z, 0]
        elif axis == "y":
            for x in range(4):
                for z in range(4):
                    face[x, z] = self.cubies[x, coord, z, 1]
        elif axis == "z":
            for x in range(4):
                for y in range(4):
                    face[x, y] = self.cubies[x, y, coord, 2]
        return face

    def reverse_row(self, axis, f1, f2):
        """Mirror a line along the given axis"""
        if axis == "x":
            y, z = f1, f2
            self.cubies[[0, 3], y, z, :] = self.cubies[[3, 0], y, z, :]
            self.cubies[[1, 2], y, z, :] = self.cubies[[2, 1], y, z, :]
        elif axis == "y":
            x, z = f1, f2
            self.cubies[x, [0, 3], z, :] = self.cubies[x, [3, 0], z, :]
            self.cubies[x, [1, 2], z, :] = self.cubies[x, [2, 1], z, :]
        elif axis == "z":
            x, y = f1, f2
            self.cubies[x, y, [0, 3], :] = self.cubies[x, y, [3, 0], :]
            self.cubies[x, y, [1, 2], :] = self.cubies[x, y, [2, 1], :]

    def is_solved(self):
        return self.serialize_colors() == self.solved_hash

    def random_scramble(self, moves=50, seed=42):
        rng = np.random.default_rng(seed)
        for _ in range(moves):
            axis = rng.choice(["x", "y", "z"])
            f1 = rng.integers(0, 4)
            f2 = rng.integers(0, 4)
            self.reverse_row(axis, f1, f2)

    def serialize_colors(self):
        """Flatten all color values as a tuple"""
        return tuple(self.cubies.flatten())

    def copy(self):
        new_cube = RubiksCube4()
        new_cube.cubies = self.cubies.copy()
        new_cube.solved_hash = self.solved_hash
        return new_cube

    def get_all_moves(self):
        moves = []
        for axis in ["x", "y", "z"]:
            for f1 in range(4):
                for f2 in range(4):
                    moves.append((axis, f1, f2))
        return moves

    def heuristic(self):
        """
        Calculates the number of misaligned colors (Hamming Distance)
        compared to the solved state using NumPy for speed.
        """
        solved_cubies = np.array(self.solved_hash, dtype=np.int8).reshape(4, 4, 4, 3)
        misaligned = self.cubies != solved_cubies
        return np.sum(misaligned)
