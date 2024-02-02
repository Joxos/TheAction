from events import OnGameInit, OnGameSetup, EventsManager, OnRightMousePress,OnUpdate,OnLeftMousePress
import arcade
from army.army import Army
from utils import grid_to_central_coordinate, coordinate_to_grid
from layout import row_column_on_grid
import heapq


def army_init(game, event: OnGameInit, em: EventsManager):
    game.army_list = []
    game.army_selected = None


def generate_army(game, army_info: Army):
    army = arcade.SpriteCircle(5, army_info.color)
    army.center_x, army.center_y = grid_to_central_coordinate(
        army_info.pos[0], army_info.pos[1]
    )
    army_info.sprite = army
    game.draw_list.append(army)
    game.army_list.append(army_info)


def army_setup(game, event: OnGameSetup, em: EventsManager):
    generate_army(game, Army(1, [0, 0], arcade.color.RED, 100, 10, 10,speed=10))


def get_army(game,pos):
    for army in game.army_list:
        if army.pos == pos:
            return army
    return None

def get_minimum_waypoints(game, p1, p2):
    '''
    A function to find the minimum number of waypoints between two points using Dijkstra's algorithm.

    Args:
    game: game.map.point(p) is used to get the height of point p.
    p1: Starting point.
    p2: Ending point.

    Returns:
    A list of waypoints from p1 to p2 with the minimum distance based on point heights.
    '''

    # Convert points to tuple type to make them hashable
    p1, p2 = tuple(p1), tuple(p2)

    # Define a function to calculate the distance between two points based on their heights
    def calculate_distance(p1, p2):
        dx, dy ,dh= abs(p2[0] - p1[0]), abs(p2[1] - p1[1]), abs(game.map.point(p2) - game.map.point(p1))
        return (dx**2 + dy**2 +dh**2)**0.5  # Multiply by the square root of 2 for diagonal movement

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
                waypoints.insert(0, current_point)  # Insert the current point at the beginning of the list
                current_point = distances[current_point]  # Move to the previous point
            waypoints.insert(0, p1)  # Insert the starting point at the beginning of the list
            return waypoints[1:]

        # Explore neighbors of the current point, including the four corners
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                nx, ny = current_point[0] + dx, current_point[1] + dy
                neighbor = (nx, ny)

                if neighbor != current_point and row_column_on_grid(nx, ny) and neighbor not in distances:
                    new_distance = current_distance + calculate_distance(current_point, neighbor)

                    if neighbor not in distances or new_distance < distances[neighbor]:
                        distances[neighbor] = current_point  # Update the distance and previous point
                        heapq.heappush(queue, (new_distance, neighbor))  # Push the neighbor and its distance to the queue

    # If no waypoints are found, return an empty list
    return []


def march_army(game, event: OnRightMousePress, em: EventsManager):
    if game.army_selected:
        army=game.army_selected
        army.waypoints= get_minimum_waypoints(game, army.pos, coordinate_to_grid(event.x, event.y))
        print(army.waypoints)
        army.marching = True

def update_armies(game, event: OnUpdate, em: EventsManager):
    for army in game.army_list:
        if army.marching:
            if army.waypoints:
                if army.last_move_tick == 0:
                    row, column = army.waypoints.pop(0)
                    army.sprite.center_x, army.sprite.center_y = grid_to_central_coordinate(
                        row, column
                    )
                    army.pos = [row, column]
                    army.last_move_tick = army.speed
                else:
                    army.last_move_tick -= 1
            else:
                army.marching = False

def select_army(game, event: OnLeftMousePress, em: EventsManager):
    for army in game.army_list:
        if army.sprite.collides_with_point((event.x, event.y)):
            game.army_selected = army
            break

subscriptions = {
    OnGameInit: army_init,
    OnGameSetup: army_setup,
    OnRightMousePress: march_army,
    OnUpdate: update_armies,
    OnLeftMousePress: select_army
}
