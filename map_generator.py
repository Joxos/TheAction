import random
from enum import Enum, auto


class Biome(Enum):
    PLAIN = auto()
    HILL = auto()


# chances
biome_chances = {Biome.PLAIN: 60, Biome.HILL: 40}
plain_chances = [80, 20]
hill_chances = [10, 20, 30, 30, 10]


def convert_chance(n, chances):
    cur = 0
    for i in range(0, len(chances)):
        cur += chances[i]
        if n <= cur:
            return i + 1
    # throw convert error


def random_biome():
    choice = random.randint(1, 100)
    chance = convert_chance(choice, list(biome_chances.values())) - 1  # minus 1 because it has been plus 1 for the height can't be 0
    return list(biome_chances.keys())[chance]


def random_height(biome: Biome):
    if biome == Biome.PLAIN:
        choice = random.randint(1, 100)
        return convert_chance(choice,plain_chances)
    elif biome == Biome.HILL:
        choice = random.randint(1, 100)
        return convert_chance(choice,hill_chances)
    else:
        return 0


def generate_map(row_count,column_count,biome_step,seed=None):
    if row_count%biome_step!=0 or column_count%biome_step!=0:
        return None
    if seed:
        random.seed(seed)
    grid = [[1 for _ in range(column_count)] for _ in range(row_count)]
    biome = [[random_biome() for _ in range(column_count//biome_step)] for _ in range(row_count//biome_step)]
    for x in range(len(grid)):
        for y in range(len(grid[x])):
            grid[x][y] = random_height(biome[x // biome_step - 1][y // biome_step - 1])
    return grid


if __name__ == "__main__":
    for x in generate_map(114):
        for y in x:
            print(y, end=" ")
        print()
