import numpy as np
import noise
# import random
# from enum import Enum, auto
# from collections import OrderedDict

# class Biome(Enum):
#     PLAIN = auto()
#     HILL = auto()


# # chances
# biome_chances = {Biome.PLAIN: 60, Biome.HILL: 40}
# biome_chances_max = sum(biome_chances.values())
# plain_chances = OrderedDict({1: 80, 2: 10})
# plain_chances_max = sum(plain_chances.values())
# hill_chances = OrderedDict({1: 10, 2: 40, 3: 40, 4: 10})
# hill_chances_max = sum(hill_chances.values())


# def convert_chances(chances: OrderedDict, max_value):
#     current = 0
#     choice = random.randint(1, max_value)
#     for selection, chance in chances.items():
#         current += chance
#         if choice <= current:
#             return selection
#     raise ValueError(f"{choice} is bigger than the sum of chances({max_value}).")


# def random_biome():
#     return convert_chances(biome_chances, biome_chances_max)


# def random_height(biome: Biome):
#     if biome == Biome.PLAIN:
#         return convert_chances(plain_chances, plain_chances_max)
#     elif biome == Biome.HILL:
#         return convert_chances(hill_chances, hill_chances_max)
#     else:
#         return 0


# def generate_map(row_count, column_count, biome_step, seed=None):
#     if row_count % biome_step != 0 or column_count % biome_step != 0:
#         raise ValueError(
#             f"Row count({row_count}) or column count({column_count}) is not divided by biome step({biome_step})."
#         )
#     if seed:
#         random.seed(seed)
#     grid = [[1 for _ in range(column_count)] for _ in range(row_count)]
#     biome = [
#         [random_biome() for _ in range(column_count // biome_step)]
#         for _ in range(row_count // biome_step)
#     ]
#     for x in range(len(grid)):
#         for y in range(len(grid[x])):
#             grid[x][y] = random_height(biome[x // biome_step - 1][y // biome_step - 1])
#     return grid


def generate_terrain(rows, cols, scale, octaves, persistence, lacunarity, seed):
    """
    Generates a 2D array of terrain values using Perlin noise.

    Parameters:
    rows (int): The number of rows in the 2D array.
    cols (int): The number of columns in the 2D array.
    scale (float): The scale of the noise. Deciding the changing speed of the generated terrain.
    octaves (int): The number of octaves in the noise. Deciding the complexity of the generated terrain.
    persistence (float): The persistence of the noise. Deciding the amplitude of the generated terrain.
    lacunarity (float): The lacunarity of the noise. Deciding the frequency of the generated terrain.
    seed (int): The seed for the random number generator.

    Returns:
    A 2D array of terrain height values.
    """
    terrain_map = np.zeros((rows, cols))

    for i in range(rows):
        for j in range(cols):
            terrain_map[i][j] = noise.pnoise2(
                i / scale,
                j / scale,
                octaves=octaves,
                persistence=persistence,
                lacunarity=lacunarity,
                repeatx=1024,
                repeaty=1024,
                base=seed,
            )

    min_val = np.min(terrain_map)
    max_val = np.max(terrain_map)
    terrain_map = (terrain_map - min_val) / (max_val - min_val)
    terrain_map = np.interp(terrain_map, (0, 1), (0, 8))

    return terrain_map.astype(int)


if __name__ == "__main__":
    terrain_map = generate_terrain(10, 10, 10, 6, 0.5, 2, 123)
    print(terrain_map)
