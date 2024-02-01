from events import OnGameInit, OnGameSetup, EventsManager, OnRightMousePress
import arcade
from army.army import Army
from utils import grid_to_central_coordinate, coordinate_to_grid
from layout import on_grid
from loguru import logger


def army_init(game, event: OnGameInit, em: EventsManager):
    game.army_list = []


def generate_army(game, army_info: Army):
    army = arcade.SpriteCircle(5, army_info.color)
    army.center_x, army.center_y = grid_to_central_coordinate(
        army_info.pos[0], army_info.pos[1]
    )
    army_info.sprite = army
    game.draw_list.append(army)
    game.army_list.append(army_info)


def army_setup(game, event: OnGameSetup, em: EventsManager):
    generate_army(game, Army(1, [0, 0], arcade.color.RED, 100, 10, 10))


def get_selected_army(game):
    for army in game.army_list:
        if army.pos == game.cell_selected:
            return army
    return None


def march_army(game, event: OnRightMousePress, em: EventsManager):
    army = get_selected_army(game)
    if army is not None and on_grid(event.x, event.y):
        row, column = coordinate_to_grid(event.x, event.y)
        army.pos = [row, column]
        army.sprite.center_x, army.sprite.center_y = grid_to_central_coordinate(
            row, column
        )
        logger.info(f"Army {army.id} moved to {army.pos}")


subscriptions = {
    OnGameInit: army_init,
    OnGameSetup: army_setup,
    OnRightMousePress: march_army,
}
