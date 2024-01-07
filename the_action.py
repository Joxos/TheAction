from map import Map
import arcade
from config import (
    ROW_COUNT,
    COLUMN_COUNT,
    BIOME_STEP,
    WIDTH,
    HEIGHT,
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    HEIGHT_COLOR,
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
                sprite = arcade.SpriteSolidColor(WIDTH, HEIGHT, arcade.color.WHITE)
                sprite.color = self.get_cell_color(row, column)
                sprite.center_x, sprite.center_y = x, y
                self.cell_sprites.append(sprite)
                self.cell_sprites_2d[row].append(sprite)

        self.armies_sprites = arcade.SpriteList()
        self.put_army(1, (10, 10), arcade.color.RED)

    def on_draw(self):
        """
        Render the screen.
        """
        # We should always start by clearing the window pixels
        self.clear()

        # Draw the sprites representing our current grid
        self.cell_sprites.draw()
        self.armies_sprites.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        """
        Called when the user presses a mouse button.
        """

        # Convert the clicked mouse position into grid coordinates
        row, column = coordinate_to_grid(x, y)

        # Make sure we are on-grid. It is possible to click in the upper right
        # corner in the margin and go to a grid location that doesn't exist
        if row >= ROW_COUNT or column >= COLUMN_COUNT:
            print("Click out of grid.")
            return

        print(
            f"Click coordinates: ({x}, {y}). Grid coordinates: ({row}, {column}), Height: {self.map.height_map[row][column]}, Color: {self.cell_sprites_2d[row][column].color}"
        )

        # Flip the color of the sprite
        # self.grid_selected=[row,column]
        if self.grid_selected:
            srow, scol = self.grid_selected
            self.cell_sprites_2d[srow][scol].color = self.get_cell_color(srow, scol)
        self.cell_sprites_2d[row][column].color = mix_color(
            self.cell_sprites_2d[row][column].color, arcade.color.VIOLET
        )
        self.grid_selected = [row, column]


def main():
    game = Game(SCREEN_WIDTH, SCREEN_HEIGHT, "The Action")
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
