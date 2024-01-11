import arcade

# map configuration
# Set how many rows and columns we will have
ROW_COUNT = 40
COLUMN_COUNT = 40
BIOME_STEP = 5

# display configuration
# This sets the WIDTH and HEIGHT of each grid location
CELL_WIDTH = 20
CELL_HEIGHT = 20

# This sets the margin between each cell
# and on the edges of the screen.
BOARDER_WIDTH = 2
SIDEBAR_WIDTH = 200

# Do the math to figure out our screen dimensions
GRID_WIDTH = (CELL_WIDTH + BOARDER_WIDTH) * COLUMN_COUNT + BOARDER_WIDTH
SCREEN_WIDTH = GRID_WIDTH + SIDEBAR_WIDTH
GRID_HEIGHT = (CELL_HEIGHT + BOARDER_WIDTH) * ROW_COUNT + BOARDER_WIDTH
SCREEN_HEIGHT = GRID_WIDTH

HEIGHT_COLOR = [
    arcade.color.BLACK,
    arcade.color.GREEN,
    arcade.color.YELLOW_GREEN,
    arcade.color.YELLOW,
    arcade.color.ORANGE,
    arcade.color.RED,
]
