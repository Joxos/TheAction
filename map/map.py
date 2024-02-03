from map.line import sampling, calculate_2d_distance_squared
import heapq
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

        # Convert points to tuple type to make them hashable
        p1, p2 = tuple(p1), tuple(p2)

        # Initialize the priority queue and the distance dictionary
        queue = [(0, p1)]  # Priority queue with distance as the first element
        distances = {p1: 0}  # Store the minimum distance to each point

        # Loop until the queue is empty
        while queue:
            current_distance, current_point = heapq.heappop(queue)

            # Check if the current point is the destination
            if current_point == p2:
                # Reconstruct the path using the distances
                waypoints = []
                while current_point in distances:
                    waypoints.insert(
                        0, current_point
                    )  # Insert the current point at the beginning of the list
                    current_point = distances[
                        current_point
                    ]  # Move to the previous point
                waypoints.insert(
                    0, p1
                )  # Insert the starting point at the beginning of the list
                return waypoints[2:]

            # Explore neighbors of the current point, including the four corners
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    nx, ny = current_point[0] + dx, current_point[1] + dy
                    neighbor = (nx, ny)

                    if (
                        neighbor != current_point
                        and row_column_on_grid(nx, ny)
                        and neighbor not in distances
                    ):
                        new_distance = current_distance + self.calculate_3d_distance(
                            current_point, neighbor
                        )

                        if (
                            neighbor not in distances
                            or new_distance < distances[neighbor]
                        ):
                            distances[
                                neighbor
                            ] = current_point  # Update the distance and previous point
                            heapq.heappush(
                                queue, (new_distance, neighbor)
                            )  # Push the neighbor and its distance to the queue

        # If no waypoints are found, return an empty list
        return []


if __name__ == "__main__":
    map = Map(6, 2, 1)
    map.height_map = [[3, 2], [2, 2], [3, 3], [2, 2], [1, 1], [1, 1]]
    print(map.is_obstructed((1, 0), (5, 0)))
