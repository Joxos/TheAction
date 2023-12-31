from map_generator import generate_map
import arcade

# Set how many rows and columns we will have
ROW_COUNT = 40
COLUMN_COUNT = 40
BIOME_STEP = 5

# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 20
HEIGHT = 20

# This sets the margin between each cell
# and on the edges of the screen.
MARGIN = 2

# Do the math to figure out our screen dimensions
SCREEN_WIDTH = (WIDTH + MARGIN) * COLUMN_COUNT + MARGIN
SCREEN_HEIGHT = (HEIGHT + MARGIN) * ROW_COUNT + MARGIN


def mix_color(a, b):
    return ((a[0] + b[0]) // 2, (a[1] + b[1]) // 2, (a[2] + b[2] // 2))


class Game(arcade.Window):
    def grid_to_central_coordinate(self, row, column):
        x = column * (WIDTH + MARGIN) + (WIDTH / 2 + MARGIN)
        y = row * (HEIGHT + MARGIN) + (HEIGHT / 2 + MARGIN)
        return [x, y]

    def coordinate_to_grid(self, x, y):
        column = int(x // (WIDTH + MARGIN))
        row = int(y // (HEIGHT + MARGIN))
        return [row, column]

    def get_cell_color(self, row, column):
        return self.height_color[self.grid_height[row][column]]

    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        self.grid_height = generate_map(ROW_COUNT, COLUMN_COUNT, BIOME_STEP)

        self.background_color = arcade.color.BLACK
        self.height_color = [
            arcade.color.BLACK,
            arcade.color.GREEN,
            arcade.color.YELLOW_GREEN,
            arcade.color.YELLOW,
            arcade.color.ORANGE,
            arcade.color.RED,
        ]

        self.grid_selected = None

        # One dimensional list of all sprites in the two-dimensional sprite list
        self.grid_sprite_list = arcade.SpriteList()

        # This will be a two-dimensional grid of sprites to mirror the two
        # dimensional grid of numbers. This points to the SAME sprites that are
        # in grid_sprite_list, just in a 2d manner.
        self.grid_sprites = []

        # Create a list of solid-color sprites to represent each grid location
        for row in range(ROW_COUNT):
            self.grid_sprites.append([])
            for column in range(COLUMN_COUNT):
                x, y = self.grid_to_central_coordinate(row, column)
                sprite = arcade.SpriteSolidColor(WIDTH, HEIGHT, arcade.color.WHITE)
                sprite.color = self.get_cell_color(row, column)
                sprite.center_x, sprite.center_y = x, y
                self.grid_sprite_list.append(sprite)
                self.grid_sprites[row].append(sprite)

    def on_draw(self):
        """
        Render the screen.
        """
        # We should always start by clearing the window pixels
        self.clear()

        # Draw the sprites representing our current grid
        self.grid_sprite_list.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        """
        Called when the user presses a mouse button.
        """

        # Convert the clicked mouse position into grid coordinates
        row, column = self.coordinate_to_grid(x, y)

        # Make sure we are on-grid. It is possible to click in the upper right
        # corner in the margin and go to a grid location that doesn't exist
        if row >= ROW_COUNT or column >= COLUMN_COUNT:
            print(f"Click out of grid.")
            return

        print(
            f"Click coordinates: ({x}, {y}). Grid coordinates: ({row}, {column}), Height: {self.grid_height[row][column]}, Color: {self.grid_sprites[row][column].color}"
        )

        # Flip the color of the sprite
        # self.grid_selected=[row,column]
        if self.grid_selected:
            srow, scol = self.grid_selected
            self.grid_sprites[srow][scol].color = self.get_cell_color(srow, scol)
        self.grid_sprites[row][column].color = mix_color(
            self.grid_sprites[row][column].color, arcade.color.GRAY
        )
        self.grid_selected = [row, column]


def main():
    Game(SCREEN_WIDTH, SCREEN_HEIGHT, "The Action")
    arcade.run()


if __name__ == "__main__":
    main()
