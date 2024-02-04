from collections import deque
from config import SPEED_PRECISION


class Army:
    def __init__(self, id, position, color, move_interval, sprite=None):
        self.id = id
        self.position = position
        self.color = color
        self.move_interval = move_interval * SPEED_PRECISION  # ticks between move
        self.move_interval_counter = 0
        self.sprite = sprite
        self.waypoints = deque()
        self.is_marching = False
        self.change_x = 0
        self.change_y = 0
