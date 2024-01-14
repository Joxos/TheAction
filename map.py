import random
from enum import Enum, auto
from collections import OrderedDict
from line import sampling, calculate_distance


class Biome(Enum):
    PLAIN = auto()
    HILL = auto()


# chances
biome_chances = {Biome.PLAIN: 60, Biome.HILL: 40}
biome_chances_max = sum(biome_chances.values())
plain_chances = OrderedDict({1: 80, 2: 10})
plain_chances_max = sum(plain_chances.values())
hill_chances = OrderedDict({1: 10, 2: 40, 3: 40, 4: 10})
hill_chances_max = sum(hill_chances.values())


def convert_chances(chances: OrderedDict, max_value):
    current = 0
    choice = random.randint(1, max_value)
    for selection, chance in chances.items():
        current += chance
        if choice <= current:
            return selection
    raise ValueError(f"{choice} is bigger than the sum of chances({max_value}).")


def random_biome():
    return convert_chances(biome_chances, biome_chances_max)


def random_height(biome: Biome):
    if biome == Biome.PLAIN:
        return convert_chances(plain_chances, plain_chances_max)
    elif biome == Biome.HILL:
        return convert_chances(hill_chances, hill_chances_max)
    else:
        return 0


def generate_map(row_count, column_count, biome_step, seed=None):
    if row_count % biome_step != 0 or column_count % biome_step != 0:
        raise ValueError(
            f"Row count({row_count}) or column count({column_count}) is not divided by biome step({biome_step})."
        )
    if seed:
        random.seed(seed)
    grid = [[1 for _ in range(column_count)] for _ in range(row_count)]
    biome = [
        [random_biome() for _ in range(column_count // biome_step)]
        for _ in range(row_count // biome_step)
    ]
    for x in range(len(grid)):
        for y in range(len(grid[x])):
            grid[x][y] = random_height(biome[x // biome_step - 1][y // biome_step - 1])
    return grid


# map object
class Map:
    def __init__(self, row_count, column_count, biome_step, seed=None):
        self.height_map = generate_map(row_count, column_count, biome_step, seed)
        self.armies = []

    def is_obstructed(self, p1, p2):
        points = sampling(p1, p2)
        h1 = self.height_map[p1[0]][p1[1]]
        h2 = self.height_map[p2[0]][p2[1]]
        for point in points:
            hp = self.height_map[point[0]][point[1]]
            dh1 = h1 - hp
            dh2 = h2 - hp
            dx1 = calculate_distance(p1, point)
            dx2 = calculate_distance(p2, point)
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


if __name__ == "__main__":
    map = Map(6, 2, 1)
    map.height_map = [[3, 2], [2, 2], [3, 3], [2, 2], [1, 1], [1, 1]]
    print(map.is_obstructed((0, 0), (5, 1)))
    print()
    print(map.is_obstructed((5, 1), (0, 0)))
