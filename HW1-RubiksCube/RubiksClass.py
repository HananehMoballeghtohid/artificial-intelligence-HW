import numpy as np

COLORS = {'W':1, 'Y':2, 'R':3, 'O':4, 'B':5, 'G':6}
REV_COLORS = {v:k for k,v in COLORS.items()}

class RubiksCube4:
    def __init__(self):
        self.cubies = self.initialize_cubies()
        self.solved_hash = self.serialize_colors()

    def initialize_cubies(self):
        cubie_dtype = np.dtype([
            ('x_face', [('coord', 'i4'), ('color', 'i4')]),
            ('y_face', [('coord', 'i4'), ('color', 'i4')]),
            ('z_face', [('coord', 'i4'), ('color', 'i4')])
        ])
        cubies = np.zeros((4,4,4), dtype=cubie_dtype)

        for x in range(4):
            for y in range(4):
                for z in range(4):
                    cubies[x,y,z]['x_face']['coord'] = x
                    cubies[x,y,z]['y_face']['coord'] = y
                    cubies[x,y,z]['z_face']['coord'] = z

                    # Assign colors
                    cubies[x,y,z]['y_face']['color'] = COLORS['B'] if y==0 else COLORS['G'] if y==3 else 0
                    cubies[x,y,z]['x_face']['color'] = COLORS['R'] if x==0 else COLORS['O'] if x==3 else 0
                    cubies[x,y,z]['z_face']['color'] = COLORS['Y'] if z==0 else COLORS['W'] if z==3 else 0
        return cubies

    def display_cube(self):
        print("Rubik's Cube 4x4:")
        print("="*50)
        faces = {
            'Front (White)': self.get_face('z', 3),
            'Back (Yellow)': self.get_face('z', 0),
            'Right (Orange)': self.get_face('x', 3),
            'Left (Red)': self.get_face('x', 0),
            'Up (Green)': self.get_face('y', 3),
            'Down (Blue)': self.get_face('y', 0)
        }
        for name, face in faces.items():
            display_face = np.vectorize(lambda c: REV_COLORS[c] if c != 0 else ' ')
            print(f"\n{name}:")
            print(display_face(face))

    def get_face(self, axis, coord):
        face = np.empty((4,4), dtype='i4')
        face.fill(0)
        if axis=='x':
            for y in range(4):
                for z in range(4):
                    face[y,z] = self.cubies[coord,y,z]['x_face']['color']
        elif axis=='y':
            for x in range(4):
                for z in range(4):
                    face[x,z] = self.cubies[x,coord,z]['y_face']['color']
        elif axis=='z':
            for x in range(4):
                for y in range(4):
                    face[x,y] = self.cubies[x,y,coord]['z_face']['color']
        return face

    def reverse_row(self, axis, fixed1, fixed2):
        """Mirror a line along the given axis in-place"""
        if axis=='x':
            y, z = fixed1, fixed2
            self.cubies[[0,3],y,z], self.cubies[[1,2],y,z] = self.cubies[[3,0],y,z].copy(), self.cubies[[2,1],y,z].copy()
        elif axis=='y':
            x, z = fixed1, fixed2
            self.cubies[x,[0,3],z], self.cubies[x,[1,2],z] = self.cubies[x,[3,0],z].copy(), self.cubies[x,[2,1],z].copy()
        elif axis=='z':
            x, y = fixed1, fixed2
            self.cubies[x,y,[0,3]], self.cubies[x,y,[1,2]] = self.cubies[x,y,[3,0]].copy(), self.cubies[x,y,[2,1]].copy()

    def is_solved(self):
        return self.serialize_colors() == self.solved_hash

    def random_scramble(self, moves=50, seed=42):
        rng = np.random.default_rng(seed)
        for _ in range(moves):
            axis = rng.choice(['x','y','z'])
            f1 = rng.integers(0,4)
            f2 = rng.integers(0,4)
            self.reverse_row(axis, f1, f2)

    def serialize_colors(self):
        """Flatten all color values as a 1D tuple"""
        colors = []
        for x in range(4):
            for y in range(4):
                for z in range(4):
                    colors.append(self.cubies[x,y,z]['x_face']['color'])
                    colors.append(self.cubies[x,y,z]['y_face']['color'])
                    colors.append(self.cubies[x,y,z]['z_face']['color'])
        return tuple(colors)

    def copy(self):
        new_cube = RubiksCube4()
        new_cube.cubies = self.cubies.copy()
        return new_cube

    def get_all_moves(self):
        moves = []
        for axis in ['x','y','z']:
            for f1 in range(4):
                for f2 in range(4):
                    moves.append((axis,f1,f2))
        return moves
