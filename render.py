from events import OnGameSetup, OnGameInit, OnCellSelected, EventsManager
import arcade
from config import ROW_COUNT, COLUMN_COUNT, CELL_WIDTH, CELL_HEIGHT, SIDEBAR_WIDTH
from utils import grid_to_central_coordinate, mix_color


def on_init(game, event: OnGameInit, em: EventsManager):
    game.background_color = arcade.color.BLACK

    # we use a draw list to avoid problems
    # when multiple modules want to draw and clear the screen after previous module has drawn up
    game.draw_list = []

    # cell render setup
    # 1d list for arcade to render
    game.cell_sprites = arcade.SpriteList()

    # 2d list to control the game
    game.cell_sprites_2d = []


def recover_all_cell(game):
    for cell_sprite_list in range(len(game.cell_sprites_2d)):
        for cell_sprite in range(len(game.cell_sprites_2d[cell_sprite_list])):
            game.cell_sprites_2d[cell_sprite_list][
                cell_sprite
            ].color = game.map.get_cell_color(cell_sprite_list, cell_sprite)


def on_setup(game, event: OnGameSetup, em: EventsManager):
    for row in range(ROW_COUNT):
        game.cell_sprites_2d.append([])
        for column in range(COLUMN_COUNT):
            x, y = grid_to_central_coordinate(row, column)
            sprite = arcade.SpriteSolidColor(
                CELL_WIDTH, CELL_HEIGHT, arcade.color.WHITE
            )
            sprite.color = game.map.get_cell_color(row, column)
            sprite.center_x, sprite.center_y = SIDEBAR_WIDTH + x, y
            game.cell_sprites.append(sprite)
            game.cell_sprites_2d[row].append(sprite)

    game.draw_list.append(game.cell_sprites)


def on_cell_selected(game, event: OnCellSelected, em: EventsManager):
    row, column = event.row, event.column
    if game.grid_selected:
        # recover the color of last selected cell
        srow, scol = game.grid_selected
        game.cell_sprites_2d[srow][scol].color = game.map.get_cell_color(srow, scol)
    # change the color of newly selected cell
    game.cell_sprites_2d[row][column].color = mix_color(
        game.cell_sprites_2d[row][column].color, arcade.color.VIOLET
    )
    game.grid_selected = [row, column]


subscriptions = {
    OnGameSetup: on_setup,
    OnGameInit: on_init,
    OnCellSelected: on_cell_selected,
}
