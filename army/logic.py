from events import (
    OnGameInit,
    OnGameSetup,
    EventsManager,
    OnRightMousePress,
    OnUpdate,
    OnLeftMousePress,
)
import arcade
from army.army import Army
from utils import grid_to_central_coordinate, coordinate_to_grid
from layout import row_column_on_grid, layout_manager, LAYOUTS
import heapq


def army_init(game, event: OnGameInit, em: EventsManager):
    game.army_list = []
    game.army_selected = None


def generate_army(game, army_info: Army):
    army_sprite = arcade.SpriteCircle(5, army_info.color)
    army_sprite.center_x, army_sprite.center_y = grid_to_central_coordinate(
        army_info.position[0], army_info.position[1]
    )
    army_info.sprite = army_sprite
    game.draw_list.append(army_sprite)
    game.army_list.append(army_info)


def army_setup(game, event: OnGameSetup, em: EventsManager):
    generate_army(
        game, Army(id=1, position=(0, 0), color=arcade.color.RED, move_interval=30)
    )


def get_army(game, position):
    for army in game.army_list:
        if army.position == position:
            return army
    return None


# Define a function to calculate the distance between two points based on their heights
def calculate_distance(game, p1, p2):
    dx, dy, dh = (
        abs(p2[0] - p1[0]),
        abs(p2[1] - p1[1]),
        abs(game.map.point(p2) - game.map.point(p1)),
    )
    return (
        dx**2 + dy**2 + dh**2
    ) ** 0.5  # Multiply by the square root of 2 for diagonal movement


def get_minimum_waypoints(game, p1, p2):
    """
    A function to find the minimum number of waypoints between two points using Dijkstra's algorithm.

    Args:
    game: game.map.point(p) is used to get the height of point p.
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
                current_point = distances[current_point]  # Move to the previous point
            waypoints.insert(
                0, p1
            )  # Insert the starting point at the beginning of the list
            return waypoints[1:]

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
                    new_distance = current_distance + calculate_distance(
                        game, current_point, neighbor
                    )

                    if neighbor not in distances or new_distance < distances[neighbor]:
                        distances[
                            neighbor
                        ] = current_point  # Update the distance and previous point
                        heapq.heappush(
                            queue, (new_distance, neighbor)
                        )  # Push the neighbor and its distance to the queue

    # If no waypoints are found, return an empty list
    return []


def army_set_destination(game, event: OnRightMousePress, em: EventsManager):
    if (
        game.army_selected
        and layout_manager.on_layout(LAYOUTS.GRID, event.x, event.y)
        and not event.key_modifiers & arcade.key.MOD_SHIFT
    ):
        game.army_selected.waypoints = get_minimum_waypoints(
            game, game.army_selected.position, coordinate_to_grid(event.x, event.y)
        )


def army_append_destination(game, event: OnRightMousePress, em: EventsManager):
    if (
        game.army_selected
        and layout_manager.on_layout(LAYOUTS.GRID, event.x, event.y)
        and event.key_modifiers & arcade.key.MOD_SHIFT
    ):
        if game.army_selected.waypoints:
            game.army_selected.waypoints.extend(
                get_minimum_waypoints(
                    game,
                    game.army_selected.waypoints[-1],
                    coordinate_to_grid(event.x, event.y),
                )
            )
        else:
            game.army_selected.waypoints = get_minimum_waypoints(
                game, game.army_selected.position, coordinate_to_grid(event.x, event.y)
            )


def update_armies(game, event: OnUpdate, em: EventsManager):
    for army in game.army_list:
        # Move the army smoothly through the waypoints within army.move_interval
        # If there are no more waypoints, stop moving
        # The army should reach the next waypoint within the move_interval
        # and then stop until the move_interval is up again
        if army.waypoints and army.move_interval_counter >= army.move_interval:
            # Move the army to the next waypoint
            army.position = army.waypoints.pop(0)
            army.sprite.center_x, army.sprite.center_y = grid_to_central_coordinate(
                army.position[0], army.position[1]
            )
            army.move_interval_counter = 0
        else:
            army.move_interval_counter += 1


def select_army(game, event: OnLeftMousePress, em: EventsManager):
    for army in game.army_list:
        if army.sprite.collides_with_point((event.x, event.y)):
            game.army_selected = army
            break


subscriptions = {
    OnGameInit: army_init,
    OnGameSetup: army_setup,
    OnRightMousePress: [army_set_destination, army_append_destination],
    OnUpdate: update_armies,
    OnLeftMousePress: select_army,
}
