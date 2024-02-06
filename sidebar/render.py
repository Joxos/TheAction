import arcade
from events import OnUpdate, OnGameInit, EventsManager
from layout import layout_manager, LAYOUTS
from utils import coordinate_to_grid
from config import (
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    SIDEBAR_WIDTH,
    GRID_WIDTH,
    SIDEBAR_DEFAULT_FONT_SIZE,
    FONT_COLOR,
    BOTTOM_SIDEBAR_HEIGHT,
    BOTTOM_SIDEBAR_Y_SPACING,
    BOTTOM_SIDEBAR_FONT_SIZE,
    BOTTOM_SIDEBAR_X_MARGIN,
    BOTTOM_SIDEBAR_X_SPACING,
    SIDEBAR_TEXT_X_MARGIN,
    SIDEBAR_TEXT_Y_MARGIN,
    SIDEBAR_LINE_SPACING,
)


def update_sidebar_info(game, event: OnUpdate, em: EventsManager):
    if layout_manager.on_layout(LAYOUTS.GRID, game.mouse_x, game.mouse_y):
        row, column = coordinate_to_grid(game.mouse_x, game.mouse_y)
        height = f"{game.map.height_map[row][column]}"
        grid_coordinate = f"({row}, {column})"
        game.hover_info.text = f"{grid_coordinate}: {height}"

    if game.army_selected:
        army = game.army_selected
        text = f"army {army.id}"
        game.army_selected_info.text = text
    else:
        game.army_selected_info.text = ""

    # update army 1 info
    if game.army_list:
        army = game.army_list[0]
        text = f"army {army.id}"
        game.army_name_1.text = text
        text = f"{army.position}"
        dest = ""
        if army.waypoints:
            dest = f"{army.waypoints[-1]}"
        game.army_position_1.text = f"{text} -> {dest}"


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

    start_x = SIDEBAR_TEXT_X_MARGIN
    start_y = SCREEN_HEIGHT - SIDEBAR_TEXT_Y_MARGIN
    game.army_name_1 = arcade.Text(
        "Army 1",
        start_x,
        start_y,
        FONT_COLOR,
        SIDEBAR_DEFAULT_FONT_SIZE,
    )
    start_y -= SIDEBAR_LINE_SPACING
    game.army_position_1 = arcade.Text(
        "Position",
        start_x,
        start_y,
        FONT_COLOR,
        SIDEBAR_DEFAULT_FONT_SIZE,
    )
    start_y -= SIDEBAR_LINE_SPACING
    game.draw_list.append(game.army_name_1)
    game.draw_list.append(game.army_position_1)

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
        SCREEN_WIDTH - SIDEBAR_WIDTH * 2, BOTTOM_SIDEBAR_HEIGHT, arcade.color.WHITE
    )
    sidebar_bg.color = arcade.color.ARSENIC
    sidebar_bg.center_x, sidebar_bg.center_y = (
        SIDEBAR_WIDTH + GRID_WIDTH / 2,
        BOTTOM_SIDEBAR_HEIGHT / 2,
    )
    game.bottom_sidebar.append(sidebar_bg)
    game.draw_list.append(game.bottom_sidebar)

    start_x = BOTTOM_SIDEBAR_X_MARGIN + SIDEBAR_WIDTH
    start_y = BOTTOM_SIDEBAR_Y_SPACING

    game.hover_info = arcade.Text(
        "", start_x, start_y, FONT_COLOR, BOTTOM_SIDEBAR_FONT_SIZE, 80
    )
    game.draw_list.append(game.hover_info)
    start_x += BOTTOM_SIDEBAR_X_SPACING + game.hover_info.width

    game.army_selected_info = arcade.Text(
        "",
        start_x,
        start_y,
        FONT_COLOR,
        SIDEBAR_DEFAULT_FONT_SIZE,
    )
    game.draw_list.append(game.army_selected_info)
    start_x += BOTTOM_SIDEBAR_X_SPACING


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
