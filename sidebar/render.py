import arcade
from events import OnUpdate, OnGameInit, EventsManager
from layout import layout_manager, LAYOUTS
from utils import coordinate_to_grid
from config import (
    SCREEN_HEIGHT,
    SIDEBAR_WIDTH,
    GRID_WIDTH,
    SIDEBAR_TEXT_X_MARGIN,
    SIDEBAR_TEXT_Y_MARGIN,
    DEFAULT_FONT_SIZE,
    LINE_SPACING,
    FONT_COLOR,
    BOTTOM_SIDEBAR_HEIGHT,
)


def update_sidebar_info(game, event: OnUpdate, em: EventsManager):
    if layout_manager.on_layout(LAYOUTS.LEFT_SIDEBAR, game.mouse_x, game.mouse_y):
        row, column = coordinate_to_grid(game.mouse_x, game.mouse_y)
        height = f"{game.map.height_map[row][column]}"
        grid_coordinate = f"({row}, {column})"
        game.hover_info.text = f"{grid_coordinate}: {height}"

    if game.army_selected:
        army = game.army_selected
        text = f"army {army.id} selected"
        game.army_selected_info.text = text
    else:
        game.army_selected_info.text = ""


def sidebar_init(game, event: OnGameInit, em: EventsManager):
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

    game.army_selected_info = arcade.Text(
        "",
        start_x,
        start_y,
        FONT_COLOR,
        DEFAULT_FONT_SIZE,
    )
    game.draw_list.append(game.army_selected_info)
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

    game.bottom_sidebar = arcade.SpriteList()
    sidebar_bg = arcade.SpriteSolidColor(
        SIDEBAR_WIDTH, SCREEN_HEIGHT, arcade.color.WHITE
    )
    sidebar_bg.color = arcade.color.ARSENIC
    sidebar_bg.center_x, sidebar_bg.center_y = (
        SIDEBAR_WIDTH + GRID_WIDTH + SIDEBAR_WIDTH / 2,
        SCREEN_HEIGHT - BOTTOM_SIDEBAR_HEIGHT / 2,
    )
    game.bottom_sidebar.append(sidebar_bg)
    game.draw_list.append(game.bottom_sidebar)


# def render_sidebar_selected_cell_info(game, event: OnCellSelected, em: EventsManager):
#     row, column = event.row, event.column
#     # update sidebar info
#     height = f"{game.map.height_map[row][column]}"
#     grid_coordinate = f"({row}, {column})"
#     game.grid_info.text = f"{grid_coordinate}: {height}"

#     text = ""
#     for army in game.army_list:
#         if army.pos[0] == row and army.pos[1] == column:
#             text = f"army {army.id}"
#     game.army_info.text = text
#     text = ""


subscriptions = {
    OnUpdate: update_sidebar_info,
    OnGameInit: sidebar_init,
}
