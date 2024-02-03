import arcade
import sys
from loguru import logger

# game configuration
ENABLE_LOGGING = True

# map configuration
# Set how many rows and columns we will have
ROW_COUNT = 40
COLUMN_COUNT = 40

# terrain configuration
TERRAIN_SCALE = 15
TERRAIN_COMPLEXITY = 100
TERRAIN_AMPLITUDE = 0.6
SEED = None

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
BOTTOM_SIDEBAR_FONT_SIZE = 12
BOTTOM_SIDEBAR_X_MARGIN = 10
BOTTOM_SIDEBAR_X_SPACING = 10
BOTTOM_SIDEBAR_Y_SPACING = 5
BOTTOM_SIDEBAR_HEIGHT = DEFAULT_FONT_SIZE + BOTTOM_SIDEBAR_Y_SPACING * 2

# grid and screen
GRID_WIDTH = (CELL_WIDTH + BOARDER_WIDTH) * COLUMN_COUNT + BOARDER_WIDTH
GRID_HEIGHT = (CELL_HEIGHT + BOARDER_WIDTH) * ROW_COUNT + BOARDER_WIDTH
SCREEN_WIDTH = GRID_WIDTH + SIDEBAR_WIDTH * 2
SCREEN_HEIGHT = GRID_WIDTH + BOTTOM_SIDEBAR_HEIGHT

# different colors of heights
HEIGHT_COLOR = [
    (0, 102, 0),  # 0m - 深绿色
    (51, 153, 51),  # 100m - 绿色
    (102, 204, 102),  # 200m - 浅绿色
    (204, 255, 153),  # 300m - 浅绿色
    (255, 255, 153),  # 400m - 浅黄色
    (255, 204, 102),  # 500m - 浅橙色
    (255, 153, 51),  # 600m - 橙黄色
    (204, 102, 102),  # 700m - 浅红色
    (153, 0, 0),  # 800m - 深红色
]
MAX_HEIGHT = len(HEIGHT_COLOR) - 1


# consequence matters
DEFAULT_MODULES = [
    "game_logic",
    "sidebar.render",
    "map.render",
    "army.logic",
    "army.render",
]
LOG_LEVEL = "DEBUG"
logger.remove()
logger.add(sys.stderr, level=LOG_LEVEL, colorize=True)
if ENABLE_LOGGING:
    DEFAULT_MODULES.append("game_logging")

# anime configuration
ANIME_DURATION = 5
