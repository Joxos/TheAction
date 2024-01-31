import arcade
from map.map import Map
from events import (
    OnKeyPress,
    EventsManager,
    OnKeyRelease,
    OnGameInit,
    OnGameSetup,
    OnCellSelected,
    OnLeftMouseRelease,
)
from utils import mix_color, grid_to_central_coordinate
from config import ROW_COUNT, COLUMN_COUNT, CELL_HEIGHT, CELL_WIDTH, BIOME_STEP
from layout import on_grid
from utils import coordinate_to_grid


def map_init(game, event: OnGameInit, em: EventsManager):
    # actually the color of the boarder
    game.background_color = arcade.color.BLACK

    game.grid_selected = None
    game.map = Map(ROW_COUNT, COLUMN_COUNT, BIOME_STEP)

    # 1d list for arcade to render
    game.cell_sprites = arcade.SpriteList()

    # 2d list to control the game
    game.cell_sprites_2d = []


def map_setup(game, event: OnGameSetup, em: EventsManager):
    for row in range(ROW_COUNT):
        game.cell_sprites_2d.append([])
        for column in range(COLUMN_COUNT):
            sprite = arcade.SpriteSolidColor(
                CELL_WIDTH, CELL_HEIGHT, arcade.color.WHITE
            )
            sprite.color = game.map.get_cell_color(row, column)
            sprite.center_x, sprite.center_y = grid_to_central_coordinate(row, column)
            game.cell_sprites.append(sprite)
            game.cell_sprites_2d[row].append(sprite)

    game.draw_list.append(game.cell_sprites)


def recover_all_cell(game):
    for cell_sprite_list in range(len(game.cell_sprites_2d)):
        for cell_sprite in range(len(game.cell_sprites_2d[cell_sprite_list])):
            game.cell_sprites_2d[cell_sprite_list][
                cell_sprite
            ].color = game.map.get_cell_color(cell_sprite_list, cell_sprite)


def dim_all_obstructed_cell(game, event: OnKeyPress, em: EventsManager):
    if event.key == arcade.key.D:
        obstructed_cells = game.map.return_all_obstructed(game.grid_selected)
        for cell in obstructed_cells:
            game.cell_sprites_2d[cell[0]][cell[1]].color = mix_color(
                game.cell_sprites_2d[cell[0]][cell[1]].color, (255, 0, 0)
            )


def recover_all_obstructed_cell(game, event: OnKeyRelease, em: EventsManager):
    if event.key == arcade.key.D:
        recover_all_cell(game)


def render_cell_selected(game, event: OnCellSelected, em: EventsManager):
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


def on_mouse_release(game, event: OnLeftMouseRelease, em: EventsManager):
    if not on_grid(event.x, event.y):
        return
    row, column = coordinate_to_grid(event.x, event.y)
    em.new_event(OnCellSelected(row, column))


subscriptions = {
    OnKeyPress: dim_all_obstructed_cell,
    OnKeyRelease: recover_all_obstructed_cell,
    OnGameInit: map_init,
    OnGameSetup: map_setup,
    OnCellSelected: render_cell_selected,
    OnLeftMouseRelease: on_mouse_release,
}
