from loguru import logger
from events import OnMouseRelease, EventsManager, OnKeyPress, OnKeyRelease
from config import SIDEBAR_WIDTH, GRID_WIDTH, BOARDER_WIDTH
from utils import coordinate_to_grid, on_grid
import arcade


def log_mouse_release(game, event: OnMouseRelease, em: EventsManager):
    if on_grid(event.x, event.y):
        row, column = coordinate_to_grid(event.x, event.y)
        logger.debug(
            f"Click on cell. Coordinates: ({event.x}, {event.y}). Grid coordinates: ({row}, {column}), Height: {game.map.height_map[row][column]}, Color: {game.cell_sprites_2d[row][column].color}"
        )
        return

    logger.debug(f"Click on sidebar. Coordinates: ({event.x}, {event.y}).")


def get_key_by_value(value):
    for key, val in arcade.key.__dict__.items():
        if val == value:
            return key
    return None


def log_key_press(game, event: OnKeyPress, em: EventsManager):
    logger.debug(f"Key pressed: {get_key_by_value(event.key)}")


def log_key_release(game, event: OnKeyRelease, em: EventsManager):
    logger.debug(f"Key released: {get_key_by_value(event.key)}")


subscriptions = {
    OnMouseRelease: log_mouse_release,
    OnKeyPress: log_key_press,
    OnKeyRelease: log_key_release,
}
