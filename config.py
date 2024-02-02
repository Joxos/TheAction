import arcade
import sys
from loguru import logger

# game configuration
ENABLE_LOGGING = True

# map configuration
# Set how many rows and columns we will have
ROW_COUNT = 40
COLUMN_COUNT = 40
BIOME_STEP = 5

# display configuration
GAME_TITLE = "The Action"

# cell and boarder
CELL_WIDTH = 20
CELL_HEIGHT = 20
BOARDER_WIDTH = 1

# sidebar
DEFAULT_FONT_SIZE = 15
FONT_COLOR = arcade.color.BEIGE
SIDEBAR_WIDTH = 250
SIDEBAR_TEXT_X_MARGIN = 10
SIDEBAR_TEXT_Y_MARGIN = 10 + DEFAULT_FONT_SIZE
LINE_SPACING = 10 + DEFAULT_FONT_SIZE

# bottom sidebar
BOTTOM_SIDEBAR_HEIGHT = 10

# grid and screen
GRID_WIDTH = (CELL_WIDTH + BOARDER_WIDTH) * COLUMN_COUNT + BOARDER_WIDTH
GRID_HEIGHT = (CELL_HEIGHT + BOARDER_WIDTH) * ROW_COUNT + BOARDER_WIDTH
SCREEN_WIDTH = GRID_WIDTH + SIDEBAR_WIDTH * 2
SCREEN_HEIGHT = GRID_WIDTH + BOTTOM_SIDEBAR_HEIGHT

# different colors of heights
HEIGHT_COLOR = [
    arcade.color.BLACK,
    arcade.color.GREEN,
    arcade.color.YELLOW_GREEN,
    arcade.color.YELLOW,
    arcade.color.ORANGE,
    arcade.color.RED,
]

# consequence matters
DEFAULT_MODULES = [
    "game_logic",
    "sidebar.render",
    "map.render",
    "army.logic",
]
LOG_LEVEL = "INFO"
logger.remove()
logger.add(sys.stderr, level=LOG_LEVEL, colorize=True)
if ENABLE_LOGGING:
    DEFAULT_MODULES.append("game_logging")
