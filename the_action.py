from map import Map
import arcade
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

    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        self.background_color = arcade.color.BLACK
        self.grid_selected = None

    def setup(self):
        # generate the map height
        self.map = Map(ROW_COUNT, COLUMN_COUNT, BIOME_STEP)

        # One dimensional list of all sprites in the two-dimensional sprite list
        self.cell_sprites = arcade.SpriteList()

        # This will be a two-dimensional grid of sprites to mirror the two
        # dimensional grid of numbers. This points to the SAME sprites that are
        # in grid_sprite_list, just in a 2d manner.
        self.cell_sprites_2d = []

        # Create a list of solid-color sprites to represent each grid location
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

        self.armies_sprites = arcade.SpriteList()
        self.put_army(1, (10, 10), arcade.color.RED)

        # render side bar
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

        # init sidebar text
        start_y = SCREEN_HEIGHT - SIDEBAR_TEXT_Y_MARGIN

        self.grid_info = arcade.Text(
            "",
            GRID_WIDTH + SIDEBAR_TEXT_X_MARGIN,
            start_y,
            FONT_COLOR,
            DEFAULT_FONT_SIZE,
        )
        start_y -= LINE_SPACING

        self.army_info = arcade.Text(
            "",
            GRID_WIDTH + SIDEBAR_TEXT_X_MARGIN,
            start_y,
            FONT_COLOR,
            DEFAULT_FONT_SIZE,
        )
        start_y -= LINE_SPACING

    def on_draw(self):
        """
        Render the screen.
        """
        # We should always start by clearing the window pixels
        self.clear()

        # Draw the sprites representing our current grid
        self.cell_sprites.draw()
        self.armies_sprites.draw()
        self.sidebar.draw()

        # render sidebar text
        if self.grid_selected:
            text = f"Height {self.map.height_map[self.grid_selected[0]][self.grid_selected[1]]} "
            text += f"({self.grid_selected[0]}, {self.grid_selected[1]})"
            self.grid_info.text = text
            self.grid_info.draw()
            text = ""

            for army in self.map.armies:
                if (
                    army.pos[0] == self.grid_selected[0]
                    and army.pos[1] == self.grid_selected[1]
                ):
                    text = f"army {army.id}"
            self.army_info.text = text
            self.army_info.draw()
        else:
            self.grid_info.text = "No cell selected."
            self.grid_info.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        """
        Called when the user presses a mouse button.
        """

        # Convert the clicked mouse position into grid coordinates
        row, column = coordinate_to_grid(x, y)

        # if row >= ROW_COUNT or column >= COLUMN_COUNT:
        #     print(f"Click on sidebar. Coordinates: ({x}, {y}).")
        #     return

        # print(
        #     f"Click on cell. Coordinates: ({x}, {y}). Grid coordinates: ({row}, {column}), Height: {self.map.height_map[row][column]}, Color: {self.cell_sprites_2d[row][column].color}"
        # )

        # recover the color of last selected cell
        if self.grid_selected:
            srow, scol = self.grid_selected
            self.cell_sprites_2d[srow][scol].color = self.get_cell_color(srow, scol)
        # change the color of newly selected cell
        self.cell_sprites_2d[row][column].color = mix_color(
            self.cell_sprites_2d[row][column].color, arcade.color.VIOLET
        )
        self.grid_selected = [row, column]


def main():
    game = Game(SCREEN_WIDTH, SCREEN_HEIGHT, GAME_TITLE)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
