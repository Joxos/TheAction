import arcade
from utils import grid_to_central_coordinate


def generate_army(row, column, color=arcade.color.RED):
    army = arcade.SpriteCircle(3, arcade.color.RED)
    army.center_x, army.center_y = grid_to_central_coordinate(row, column)
    return army
