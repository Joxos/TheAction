import arcade
from utils import grid_to_central_coordinate


class Army:
    def __init__(self, id, pos, color):
        self.id = id
        self.pos = pos
        self.color = color


def generate_army(info: Army):
    army = arcade.SpriteCircle(3, info.color)
    army.center_x, army.center_y = grid_to_central_coordinate(info.pos[0], info.pos[1])
    return army
