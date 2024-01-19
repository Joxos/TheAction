from utils import coordinate_to_grid, grid_to_central_coordinate
import arcade
from map import Map
from events import OnDraw, OnMouseRelease, OnSetup
from config import (
    ROW_COUNT,
    COLUMN_COUNT,
    BIOME_STEP,
    CELL_WIDTH,
    CELL_HEIGHT,
)


def on_mouse_release(game, event: OnMouseRelease):
    row, column = coordinate_to_grid(event.x, event.y)

    if row >= ROW_COUNT or column >= COLUMN_COUNT:
        print(f"Click on sidebar. Coordinates: ({event.x}, {event.y}).")
        return

    # print(
    #     f"Click on cell. Coordinates: ({x}, {y}). Grid coordinates: ({row}, {column}), Height: {self.map.height_map[row][column]}, Color: {self.cell_sprites_2d[row][column].color}"
    # )

    game.select_cell(row, column)


def on_draw(game, event: OnDraw):
    game.clear()

    game.cell_sprites.draw()
    game.armies_sprites.draw()


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


subscriptions = {OnDraw: on_draw, OnSetup: on_setup, OnMouseRelease: on_mouse_release}
