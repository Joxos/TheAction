from loguru import logger
from events import OnMouseRelease, EventsManager
from config import SIDEBAR_WIDTH, GRID_WIDTH, BOARDER_WIDTH
from utils import coordinate_to_grid


def log_mouse_release(game, event: OnMouseRelease, em: EventsManager):
    row, column = coordinate_to_grid(event.x - SIDEBAR_WIDTH, event.y)
    if event.x < SIDEBAR_WIDTH or event.x > SIDEBAR_WIDTH + GRID_WIDTH - BOARDER_WIDTH:
        logger.debug(f"Click on sidebar. Coordinates: ({event.x}, {event.y}).")
        return

    logger.debug(
        f"Click on cell. Coordinates: ({event.x}, {event.y}). Grid coordinates: ({row}, {column}), Height: {game.map.height_map[row][column]}, Color: {game.cell_sprites_2d[row][column].color}"
    )


subscriptions = {OnMouseRelease: log_mouse_release}
