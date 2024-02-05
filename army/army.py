from collections import deque
from config import SPEED_PRECISION


class Army:
    """Represents an army with its attributes and methods to handle its behavior."""

    def __init__(self, id, position, color, move_interval, sprite=None):
        self.id = id
        self.position = position
        self.color = color
        self.move_interval = move_interval * SPEED_PRECISION  # ticks between moves
        self.move_interval_counter = 0  # ticks since last move
        self.sprite = sprite
        self.waypoints = deque()

    def update_position(self, new_position):
        """Updates the army's current position."""
        self.position = new_position

    def add_waypoint(self, waypoint):
        """Adds a waypoint to the army's path."""
        self.waypoints.append(waypoint)

    def pop_waypoint(self):
        """Pops the next waypoint from the army's path."""
        return self.waypoints.popleft() if self.waypoints else None

    def has_waypoints(self):
        """Checks if the army has waypoints to follow."""
        return len(self.waypoints) > 0

    def set_sprite_position(self, x, y):
        """Updates the sprite's position if it exists."""
        if self.sprite:
            self.sprite.center_x = x
            self.sprite.center_y = y

    def get_sprite_position(self):
        """Returns the sprite's current position."""
        return (
            (self.sprite.center_x, self.sprite.center_y)
            if self.sprite
            else (None, None)
        )
