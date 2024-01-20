import arcade
from events import OnMouseMotion, OnSetup
from utils import coordinate_to_grid
from config import (
    ROW_COUNT,
    COLUMN_COUNT,
    SCREEN_HEIGHT,
    SIDEBAR_WIDTH,
    GRID_WIDTH,
    SIDEBAR_TEXT_X_MARGIN,
    SIDEBAR_TEXT_Y_MARGIN,
    DEFAULT_FONT_SIZE,
    LINE_SPACING,
    FONT_COLOR,
    BOARDER_WIDTH,
)


def update_sidebar_info(game, event: OnMouseMotion):
    row, column = coordinate_to_grid(event.x - SIDEBAR_WIDTH, event.y)
    if (
        event.x <= SIDEBAR_WIDTH
        or event.x >= SIDEBAR_WIDTH + GRID_WIDTH - BOARDER_WIDTH
        or event.y >= SCREEN_HEIGHT - BOARDER_WIDTH
    ):
        # not in grid
        return
    height = f"{game.map.height_map[row][column]}"
    grid_coordinate = f"({row}, {column})"
    game.hover_info.text = f"{grid_coordinate}: {height}"
    if game.grid_selected:
        game.obstruct_info.text = game.map.is_obstructed(
            (row, column), game.grid_selected
        )


def on_setup(game, event: OnSetup):
    game.left_sidebar = arcade.SpriteList()
    sidebar_bg = arcade.SpriteSolidColor(
        SIDEBAR_WIDTH, SCREEN_HEIGHT, arcade.color.WHITE
    )
    sidebar_bg.color = arcade.color.ARSENIC
    sidebar_bg.center_x, sidebar_bg.center_y = (
        SIDEBAR_WIDTH / 2,
        SCREEN_HEIGHT / 2,
    )
    game.left_sidebar.append(sidebar_bg)
    game.draw_list.append(game.left_sidebar)

    # sidebar text render setup
    start_x = SIDEBAR_TEXT_X_MARGIN
    start_y = SCREEN_HEIGHT - SIDEBAR_TEXT_Y_MARGIN

    game.hover_info = arcade.Text("", start_x, start_y, FONT_COLOR, DEFAULT_FONT_SIZE)
    game.draw_list.append(game.hover_info)
    start_y -= LINE_SPACING

    game.grid_info = arcade.Text(
        "",
        start_x,
        start_y,
        FONT_COLOR,
        DEFAULT_FONT_SIZE,
    )
    game.draw_list.append(game.grid_info)
    start_y -= LINE_SPACING

    game.army_info = arcade.Text(
        "",
        start_x,
        start_y,
        FONT_COLOR,
        DEFAULT_FONT_SIZE,
    )
    game.draw_list.append(game.army_info)
    start_y -= LINE_SPACING

    game.obstruct_info = arcade.Text(
        "",
        start_x,
        start_y,
        FONT_COLOR,
        DEFAULT_FONT_SIZE,
    )
    game.draw_list.append(game.obstruct_info)
    start_y -= LINE_SPACING

    game.right_sidebar = arcade.SpriteList()
    sidebar_bg = arcade.SpriteSolidColor(
        SIDEBAR_WIDTH, SCREEN_HEIGHT, arcade.color.WHITE
    )
    sidebar_bg.color = arcade.color.ARSENIC
    sidebar_bg.center_x, sidebar_bg.center_y = (
        SIDEBAR_WIDTH + GRID_WIDTH + SIDEBAR_WIDTH / 2,
        SCREEN_HEIGHT / 2,
    )
    game.left_sidebar.append(sidebar_bg)
    game.draw_list.append(game.right_sidebar)


subscriptions = {OnMouseMotion: update_sidebar_info, OnSetup: on_setup}
