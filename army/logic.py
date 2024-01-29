from events import OnGameInit, OnGameSetup, EventsManager
import arcade
from army.army import Army
from utils import grid_to_central_coordinate
from config import SIDEBAR_WIDTH


def on_game_init(game, event: OnGameInit, em: EventsManager):
    game.army_list = []


def generate_army(game, army_info: Army):
    army = arcade.SpriteCircle(5, army_info.color)
    army.center_x, army.center_y = grid_to_central_coordinate(
        army_info.pos[0], army_info.pos[1]
    )
    army.center_x += SIDEBAR_WIDTH
    game.draw_list.append(army)
    game.army_list.append(army_info)


def on_game_setup(game, event: OnGameSetup, em: EventsManager):
    generate_army(game, Army(1, (0, 0), arcade.color.RED, 100, 10, 10))


subscriptions = {OnGameInit: on_game_init, OnGameSetup: on_game_setup}
