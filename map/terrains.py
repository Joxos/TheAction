import numpy as np
from opensimplex import OpenSimplex
from random import randint


def simplex_noise_generate_terrain(
    width, height, scale, octaves, persistence, max_height, seed=None
):
    """
    Generates a 2D array of terrain values using simplex noise.

    Parameters:
    width (int): The number of columns in the 2D array.
    height (int): The number of rows in the 2D array.
    scale (float): The scale of the noise. Deciding the changing speed of the generated terrain.
    octaves (int): The number of octaves in the noise. Deciding the complexity of the generated terrain.
    persistence (float): The persistence of the noise. Deciding the amplitude of the generated terrain.
    seed (int): The seed for the random number generator.

    Returns:
    A 2D array of terrain height values.
    """
    if not seed:
        seed = randint(0, 100)
    simplex = OpenSimplex(seed)
    noise = np.zeros((width, height))
    for y in range(height):
        for x in range(width):
            value = 0
            for o in range(octaves):
                frequency = 2**o
                amplitude = persistence**o
                value += (
                    simplex.noise2(x * frequency / scale, y * frequency / scale)
                    * amplitude
                )
            noise[y][x] = value

    # Normalize the noise values to be between 0 and 1
    min_val = np.min(noise)
    max_val = np.max(noise)
    noise = (noise - min_val) / (max_val - min_val)

    # Scale the noise values to be between 0 and max_height
    noise = np.interp(noise, (0, 1), (0, max_height))

    # Convert the noise values to integers
    noise = noise.astype(int)

    return noise
