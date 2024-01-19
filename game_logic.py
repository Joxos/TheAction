from utils import coordinate_to_grid, grid_to_central_coordinate
import arcade
from map import Map
from config import (
    ROW_COUNT,
    COLUMN_COUNT,
    BIOME_STEP,
    CELL_WIDTH,
    CELL_HEIGHT,
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    HEIGHT_COLOR,
    SIDEBAR_WIDTH,
    GRID_WIDTH,
    SIDEBAR_TEXT_X_MARGIN,
    SIDEBAR_TEXT_Y_MARGIN,
    DEFAULT_FONT_SIZE,
    LINE_SPACING,
    FONT_COLOR,
    GAME_TITLE,
)


def on_mouse_motion(game, event):
    # update sidebar info
    row, column = coordinate_to_grid(event.x, event.y)
    if row >= ROW_COUNT or column >= COLUMN_COUNT:
        return
    height = f"{game.map.height_map[row][column]}"
    grid_coordinate = f"({row}, {column})"
    game.hover_info.text = f"{grid_coordinate}: {height}"
    if game.grid_selected:
        game.obstruct_info.text = game.map.is_obstructed(
            (row, column), game.grid_selected
        )


def on_mouse_release(game, event):
    row, column = coordinate_to_grid(event.x, event.y)

    if row >= ROW_COUNT or column >= COLUMN_COUNT:
        print(f"Click on sidebar. Coordinates: ({event.x}, {event.y}).")
        return

    # print(
    #     f"Click on cell. Coordinates: ({x}, {y}). Grid coordinates: ({row}, {column}), Height: {self.map.height_map[row][column]}, Color: {self.cell_sprites_2d[row][column].color}"
    # )

    game.select_cell(row, column)


def on_draw(game, event):
    game.clear()

    game.cell_sprites.draw()
    game.armies_sprites.draw()
    game.sidebar.draw()

    game.grid_info.draw()
    game.army_info.draw()
    game.hover_info.draw()
    game.obstruct_info.draw()


def on_setup(game, event):
    game.map = Map(ROW_COUNT, COLUMN_COUNT, BIOME_STEP)

    # cell render setup
    # 1d list for arcade to render
    game.cell_sprites = arcade.SpriteList()

    # 2d list to control the game
    game.cell_sprites_2d = []
    for row in range(ROW_COUNT):
        game.cell_sprites_2d.append([])
        for column in range(COLUMN_COUNT):
            x, y = grid_to_central_coordinate(row, column)
            sprite = arcade.SpriteSolidColor(
                CELL_WIDTH, CELL_HEIGHT, arcade.color.WHITE
            )
            sprite.color = game.get_cell_color(row, column)
            sprite.center_x, sprite.center_y = x, y
            game.cell_sprites.append(sprite)
            game.cell_sprites_2d[row].append(sprite)

    # a test army
    game.armies_sprites = arcade.SpriteList()
    game.put_army(1, (10, 10), arcade.color.RED)

    # sidebar render setup
    game.sidebar = arcade.SpriteList()
    sidebar_bg = arcade.SpriteSolidColor(
        SIDEBAR_WIDTH, SCREEN_HEIGHT, arcade.color.WHITE
    )
    sidebar_bg.color = arcade.color.AERO_BLUE
    sidebar_bg.center_x, sidebar_bg.center_y = (
        GRID_WIDTH + SIDEBAR_WIDTH / 2,
        SCREEN_HEIGHT / 2,
    )
    game.sidebar.append(sidebar_bg)

    # sidebar text render setup
    start_x = GRID_WIDTH + SIDEBAR_TEXT_X_MARGIN
    start_y = SCREEN_HEIGHT - SIDEBAR_TEXT_Y_MARGIN

    game.hover_info = arcade.Text("", start_x, start_y, FONT_COLOR, DEFAULT_FONT_SIZE)
    start_y -= LINE_SPACING

    game.grid_info = arcade.Text(
        "",
        start_x,
        start_y,
        FONT_COLOR,
        DEFAULT_FONT_SIZE,
    )
    start_y -= LINE_SPACING

    game.army_info = arcade.Text(
        "",
        start_x,
        start_y,
        FONT_COLOR,
        DEFAULT_FONT_SIZE,
    )
    start_y -= LINE_SPACING

    game.obstruct_info = arcade.Text(
        "",
        start_x,
        start_y,
        FONT_COLOR,
        DEFAULT_FONT_SIZE,
    )
    start_y -= LINE_SPACING
