from map.line import sampling, calculate_2d_distance_squared
import heapq
from collections import deque
from config import (
    HEIGHT_COLOR,
    TERRAIN_AMPLITUDE,
    TERRAIN_COMPLEXITY,
    TERRAIN_SCALE,
    MAX_HEIGHT,
)
from map.terrains import simplex_noise_generate_terrain
from utils import row_column_on_grid


# map object
class Map:
    def __init__(self, row_count, column_count, seed):
        self.height_map = simplex_noise_generate_terrain(
            row_count,
            column_count,
            TERRAIN_SCALE,
            TERRAIN_COMPLEXITY,
            TERRAIN_AMPLITUDE,
            MAX_HEIGHT,
            seed,
        )

    def point(self, pos):
        return self.height_map[pos[0]][pos[1]]

    def calculate_3d_distance(self, p1, p2):
        dx, dy, dh = (
            abs(p2[0] - p1[0]),
            abs(p2[1] - p1[1]),
            abs(self.point(p2) - self.point(p1)),
        )
        return (dx**2 + dy**2 + dh**2) ** 0.5

    def is_obstructed(self, p1, p2):
        samples = sampling(p1, p2)
        h1 = self.point(p1)
        h2 = self.point(p2)
        for sample in samples:
            hp = self.point(sample)
            dh1 = h1 - hp
            dh2 = h2 - hp
            dx1 = calculate_2d_distance_squared(p1, sample)
            dx2 = calculate_2d_distance_squared(p2, sample)
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

    def get_minimum_waypoints(self, p1, p2):
        """
        A function to find the minimum number of waypoints between two points using Dijkstra's algorithm.

        Args:
        p1: Starting point.
        p2: Ending point.

        Returns:
        A list of waypoints from p1 to p2 with the minimum distance based on point heights.
        """
        p1, p2 = tuple(p1), tuple(p2)

        queue = [(0, p1)]
        distances = {p1: 0}
        prev_point = {p1: None}

        visited = set()

        while queue:
            current_distance, current_point = heapq.heappop(queue)
            visited.add(current_point)

            if current_point == p2:
                waypoints = deque()
                # prev_point to rebuilt the path
                while current_point:
                    waypoints.append(current_point)
                    current_point = prev_point[current_point]
                waypoints.reverse()  # reverse the list to get the correct order
                return waypoints

            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    if dx == 0 and dy == 0:
                        continue  # skip the current point
                    nx, ny = current_point[0] + dx, current_point[1] + dy
                    neighbor = (nx, ny)

                    if neighbor not in visited and row_column_on_grid(nx, ny):
                        new_distance = current_distance + self.calculate_3d_distance(
                            current_point, neighbor
                        )

                        if (
                            neighbor not in distances
                            or new_distance < distances[neighbor]
                        ):
                            distances[neighbor] = new_distance
                            prev_point[neighbor] = current_point
                            heapq.heappush(queue, (new_distance, neighbor))

        return deque()  # return empty list if no waypoints are found


if __name__ == "__main__":
    map = Map(6, 2, 1)
    map.height_map = [[3, 2], [2, 2], [3, 3], [2, 2], [1, 1], [1, 1]]
    print(map.is_obstructed((1, 0), (5, 0)))
