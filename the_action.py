import arcade
from fractions import Fraction
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
from utils import mix_color, grid_to_central_coordinate, coordinate_to_grid
from army import generate_army, Army


class Game(arcade.Window):
    def get_cell_color(self, row, column):
        return HEIGHT_COLOR[self.map.height_map[row][column]]

    def put_army(self, id, pos: tuple[int, int], color):
        army_info = Army(id, pos, color)
        self.map.armies.append(army_info)
        self.armies_sprites.append(generate_army(army_info))

    def select_cell(self, row, column):
        if self.grid_selected:
            # recover the color of last selected cell
            srow, scol = self.grid_selected
            self.cell_sprites_2d[srow][scol].color = self.get_cell_color(srow, scol)
        # change the color of newly selected cell
        self.cell_sprites_2d[row][column].color = mix_color(
            self.cell_sprites_2d[row][column].color, arcade.color.VIOLET
        )
        self.grid_selected = [row, column]

        # update sidebar info
        height = f"{self.map.height_map[row][column]}"
        grid_coordinate = f"({row}, {column})"
        self.grid_info.text = f"{grid_coordinate}: {height}"

        text = ""
        for army in self.map.armies:
            if army.pos[0] == row and army.pos[1] == column:
                text = f"army {army.id}"
        self.army_info.text = text
        text = ""

    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        self.background_color = arcade.color.BLACK
        self.grid_selected = None

    def setup(self):
        # map setup
        self.map = Map(ROW_COUNT, COLUMN_COUNT, BIOME_STEP)

        # cell render setup
        # 1d list for arcade to render
        self.cell_sprites = arcade.SpriteList()

        # 2d list to control the game
        self.cell_sprites_2d = []
        for row in range(ROW_COUNT):
            self.cell_sprites_2d.append([])
            for column in range(COLUMN_COUNT):
                x, y = grid_to_central_coordinate(row, column)
                sprite = arcade.SpriteSolidColor(
                    CELL_WIDTH, CELL_HEIGHT, arcade.color.WHITE
                )
                sprite.color = self.get_cell_color(row, column)
                sprite.center_x, sprite.center_y = x, y
                self.cell_sprites.append(sprite)
                self.cell_sprites_2d[row].append(sprite)

        # a test army
        self.armies_sprites = arcade.SpriteList()
        self.put_army(1, (10, 10), arcade.color.RED)

        # sidebar render setup
        self.sidebar = arcade.SpriteList()
        sidebar_bg = arcade.SpriteSolidColor(
            SIDEBAR_WIDTH, SCREEN_HEIGHT, arcade.color.WHITE
        )
        sidebar_bg.color = arcade.color.AERO_BLUE
        sidebar_bg.center_x, sidebar_bg.center_y = (
            GRID_WIDTH + SIDEBAR_WIDTH / 2,
            SCREEN_HEIGHT / 2,
        )
        self.sidebar.append(sidebar_bg)

        # sidebar text render setup
        start_x = GRID_WIDTH + SIDEBAR_TEXT_X_MARGIN
        start_y = SCREEN_HEIGHT - SIDEBAR_TEXT_Y_MARGIN

        self.hover_info = arcade.Text(
            "", start_x, start_y, FONT_COLOR, DEFAULT_FONT_SIZE
        )
        start_y -= LINE_SPACING

        self.grid_info = arcade.Text(
            "",
            start_x,
            start_y,
            FONT_COLOR,
            DEFAULT_FONT_SIZE,
        )
        start_y -= LINE_SPACING

        self.army_info = arcade.Text(
            "",
            start_x,
            start_y,
            FONT_COLOR,
            DEFAULT_FONT_SIZE,
        )
        start_y -= LINE_SPACING

        self.obstruct_info = arcade.Text(
            "",
            start_x,
            start_y,
            FONT_COLOR,
            DEFAULT_FONT_SIZE,
        )
        start_y -= LINE_SPACING

    def on_draw(self):
        self.clear()

        self.cell_sprites.draw()
        self.armies_sprites.draw()
        self.sidebar.draw()

        self.grid_info.draw()
        self.army_info.draw()
        self.hover_info.draw()
        self.obstruct_info.draw()

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        # update sidebar info
        row, column = coordinate_to_grid(x, y)
        if row >= ROW_COUNT or column >= COLUMN_COUNT:
            return
        height = f"{self.map.height_map[row][column]}"
        grid_coordinate = f"({row}, {column})"
        self.hover_info.text = f"{grid_coordinate}: {height}"
        if self.grid_selected:
            self.obstruct_info.text = self.map.is_obstructed(
                (row, column), self.grid_selected
            )

    def on_mouse_press(self, x, y, button, modifiers):
        pass

    def on_mouse_release(self, x, y, button, key_modifiers):
        row, column = coordinate_to_grid(x, y)

        if row >= ROW_COUNT or column >= COLUMN_COUNT:
            print(f"Click on sidebar. Coordinates: ({x}, {y}).")
            return

        # print(
        #     f"Click on cell. Coordinates: ({x}, {y}). Grid coordinates: ({row}, {column}), Height: {self.map.height_map[row][column]}, Color: {self.cell_sprites_2d[row][column].color}"
        # )

        self.select_cell(row, column)


def main():
    game = Game(SCREEN_WIDTH, SCREEN_HEIGHT, GAME_TITLE)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
