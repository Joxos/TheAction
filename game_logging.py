from loguru import logger
from events import (
    EventsManager,
    OnKeyPress,
    OnKeyRelease,
    OnLeftMousePress,
    OnRightMousePress,
    OnLeftMouseRelease,
    OnRightMouseRelease,
)
from utils import coordinate_to_grid
from layout import layout_manager, LAYOUTS
import arcade


def log_left_mouse_press(game, event: OnLeftMousePress, em: EventsManager):
    if layout_manager.on_layout(LAYOUTS.GRID, event.x, event.y):
        row, column = coordinate_to_grid(event.x, event.y)
        logger.debug(
            f"Left mouse press on cell. Coordinates: ({event.x}, {event.y}). Grid coordinates: ({row}, {column}), Height: {game.map.height_map[row][column]}, Color: {game.cell_sprites_2d[row][column].color}"
        )
        return

    logger.debug(f"Left mouse press on sidebar. Coordinates: ({event.x}, {event.y}).")


def log_right_mouse_press(game, event: OnRightMousePress, em: EventsManager):
    if layout_manager.on_layout(LAYOUTS.GRID, event.x, event.y):
        row, column = coordinate_to_grid(event.x, event.y)
        logger.debug(
            f"Right mouse press on cell. Coordinates: ({event.x}, {event.y}). Grid coordinates: ({row}, {column}), Height: {game.map.height_map[row][column]}, Color: {game.cell_sprites_2d[row][column].color}"
        )
        return

    logger.debug(f"Right mouse press on sidebar. Coordinates: ({event.x}, {event.y}).")


def log_left_mouse_release(game, event: OnLeftMouseRelease, em: EventsManager):
    if layout_manager.on_layout(LAYOUTS.GRID, event.x, event.y):
        row, column = coordinate_to_grid(event.x, event.y)
        logger.debug(
            f"Left mouse release on cell. Coordinates: ({event.x}, {event.y}). Grid coordinates: ({row}, {column}), Height: {game.map.height_map[row][column]}, Color: {game.cell_sprites_2d[row][column].color}"
        )
        return

    logger.debug(f"Left mouse release on sidebar. Coordinates: ({event.x}, {event.y}).")


def log_right_mouse_release(game, event: OnRightMouseRelease, em: EventsManager):
    if layout_manager.on_layout(LAYOUTS.GRID, event.x, event.y):
        row, column = coordinate_to_grid(event.x, event.y)
        logger.debug(
            f"Right mouse release on cell. Coordinates: ({event.x}, {event.y}). Grid coordinates: ({row}, {column}), Height: {game.map.height_map[row][column]}, Color: {game.cell_sprites_2d[row][column].color}"
        )
        return

    logger.debug(
        f"Right mouse release on sidebar. Coordinates: ({event.x}, {event.y})."
    )


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
    OnLeftMouseRelease: log_left_mouse_release,
    OnRightMouseRelease: log_right_mouse_release,
    OnLeftMousePress: log_left_mouse_press,
    OnRightMousePress: log_right_mouse_press,
    OnKeyPress: log_key_press,
    OnKeyRelease: log_key_release,
}
