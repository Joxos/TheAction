from map.line import sampling, distance_squared
from config import (
    HEIGHT_COLOR,
    TERRAIN_AMPLITUDE,
    TERRAIN_FREQUENCY,
    TERRAIN_COMPLEXITY,
    TERRAIN_SCALE,
    MAX_HEIGHT,
)
from map.terrains import generate_terrain


# map object
class Map:
    def __init__(self, row_count, column_count, seed):
        self.height_map = generate_terrain(
            row_count,
            column_count,
            TERRAIN_SCALE,
            TERRAIN_COMPLEXITY,
            TERRAIN_AMPLITUDE,
            TERRAIN_FREQUENCY,
            MAX_HEIGHT,
            seed,
        )

    def point(self, pos):
        return self.height_map[pos[0]][pos[1]]

    def is_obstructed(self, p1, p2):
        samples = sampling(p1, p2)
        h1 = self.point(p1)
        h2 = self.point(p2)
        for sample in samples:
            hp = self.point(sample)
            dh1 = h1 - hp
            dh2 = h2 - hp
            dx1 = distance_squared(p1, sample)
            dx2 = distance_squared(p2, sample)
            k1 = dh1 / dx1
            k2 = dh2 / dx2
            if (
                hp > h1
                and hp > h2
                or abs(k1) > abs(k2)
                and h1 < h2
                or abs(k1) < abs(k2)
                and h1 > h2
            ):
                return False
        return True

    def return_all_obstructed(self, point):
        return [
            (x, y)
            for x in range(len(self.height_map))
            for y in range(len(self.height_map[x]))
            if self.is_obstructed((x, y), point)
        ]

    def get_cell_color(self, row, column):
        return HEIGHT_COLOR[self.height_map[row][column]]


if __name__ == "__main__":
    map = Map(6, 2, 1)
    map.height_map = [[3, 2], [2, 2], [3, 3], [2, 2], [1, 1], [1, 1]]
    print(map.is_obstructed((1, 0), (5, 0)))
