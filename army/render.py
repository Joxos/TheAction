from events import OnUpdate, EventsManager
from utils import grid_to_central_coordinate


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


subscriptions = {OnUpdate: update_armies}
