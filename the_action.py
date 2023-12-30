from map_generator import generate_map
import arcade

# Set how many rows and columns we will have
ROW_COUNT = 40
COLUMN_COUNT = 40
BIOME_STEP=5

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
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.grid = generate_map(ROW_COUNT,COLUMN_COUNT,BIOME_STEP)
        self.background_color = arcade.color.BLACK
        self.color = [
            arcade.color.BLACK,
            arcade.color.GREEN,
            arcade.color.YELLOW_GREEN,
            arcade.color.YELLOW,
            arcade.color.ORANGE,
            arcade.color.RED,
        ]
        self.update_grid()

    def update_grid(self):
        """
        Create the shapes for our current grid.

        We look at the values in each cell.
        If the cell contains 0 we crate a white shape.
        If the cell contains 1 we crate a green shape.
        """
        self.shape_list = arcade.ShapeElementList()
        for row in range(ROW_COUNT):
            for column in range(COLUMN_COUNT):
                color = self.color[self.grid[row][column]]

                x = (MARGIN + WIDTH) * column + MARGIN + WIDTH // 2
                y = (MARGIN + HEIGHT) * row + MARGIN + HEIGHT // 2

                current_rect = arcade.create_rectangle_filled(
                    x, y, WIDTH, HEIGHT, color
                )
                self.shape_list.append(current_rect)

    def on_draw(self):
        """
        Render the screen.
        """
        # We should always start by clearing the window pixels
        self.clear()

        # Draw the shapes representing our current grid
        self.shape_list.draw()

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

        # Rebuild the shapes
        self.update_grid()


def main():
    game = Game(SCREEN_WIDTH, SCREEN_HEIGHT, "The Action")
    arcade.run()


if __name__ == "__main__":
    main()
