import arcade
from config import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    HEIGHT_COLOR,
    GAME_TITLE,
)
from utils import mix_color
from army import generate_army, Army
from events import (
    EventsManager,
    default_events_list,
    OnSetup,
    OnDraw,
    OnMouseMotion,
    OnMousePress,
    OnMouseRelease,
)
import sidebar
import game_logic

events_manager = EventsManager()


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
        events_manager.new_event(OnSetup())

    def on_draw(self):
        events_manager.new_event(OnDraw())

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        events_manager.new_event(OnMouseMotion(x, y))

    def on_mouse_press(self, x, y, button, modifiers):
        pass

    def on_mouse_release(self, x, y, button, key_modifiers):
        events_manager.new_event(OnMouseRelease(x, y))


def main():
    game = Game(SCREEN_WIDTH, SCREEN_HEIGHT, GAME_TITLE)
    events_manager.set_game_ref(game)

    events_manager.register(default_events_list)

    # note that the sequence matters when modules subscribe to on_draw()
    # maybe a hidden bug in the future
    # try to figure out a solution
    events_manager.multi_subscribe(game_logic.subscriptions)
    events_manager.multi_subscribe(sidebar.subscriptions)

    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
