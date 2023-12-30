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


class Game(arcade.Window):
    def get_cell_color(self, row, column):
        return self.color[self.grid[row][column]]

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.grid = generate_map(ROW_COUNT, COLUMN_COUNT, BIOME_STEP)
        self.background_color = arcade.color.BLACK
        self.color = [
            arcade.color.BLACK,
            arcade.color.GREEN,
            arcade.color.YELLOW_GREEN,
            arcade.color.YELLOW,
            arcade.color.ORANGE,
            arcade.color.RED,
        ]

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
                x = column * (WIDTH + MARGIN) + (WIDTH / 2 + MARGIN)
                y = row * (HEIGHT + MARGIN) + (HEIGHT / 2 + MARGIN)
                sprite = arcade.SpriteSolidColor(
                    WIDTH, HEIGHT, self.get_cell_color(row, column)
                )
                sprite.center_x = x
                sprite.center_y = y
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
        column = int(x // (WIDTH + MARGIN))
        row = int(y // (HEIGHT + MARGIN))

        # Make sure we are on-grid. It is possible to click in the upper right
        # corner in the margin and go to a grid location that doesn't exist
        if row >= ROW_COUNT or column >= COLUMN_COUNT:
            print(f"Click out of grid.")
            return

        print(
            f"Click coordinates: ({x}, {y}). Grid coordinates: ({row}, {column}), Height: {self.grid[row][column]}"
        )

        # Flip the location between 1 and 0.
        # if self.grid[row][column] == 0:
        #     self.grid[row][column] = 1
        # else:
        #     self.grid[row][column] = 0


def main():
    game = Game(SCREEN_WIDTH, SCREEN_HEIGHT, "The Action")
    arcade.run()


if __name__ == "__main__":
    main()
