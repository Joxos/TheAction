import arcade
from config import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    GAME_TITLE,
    DEFAULT_MODULES,
)
from events import (
    EventsManager,
    default_events_list,
    OnGameSetup,
    OnDraw,
    OnMouseMotion,
    OnLeftMousePress,
    OnRightMousePress,
    OnLeftMouseRelease,
    OnRightMouseRelease,
    BeforeGameInit,
    OnUpdate,
    OnKeyPress,
    OnGameInit,
    OnKeyRelease,
)

events_manager = EventsManager()
events_manager.register(default_events_list)
events_manager.import_modules(DEFAULT_MODULES)
events_manager.verbose_subscription_info()
events_manager.new_event(BeforeGameInit())


class Game(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        events_manager.set_game_ref(self)
        events_manager.new_event(OnGameInit())

    def setup(self):
        events_manager.new_event(OnGameSetup())

    def on_draw(self):
        events_manager.new_event(OnDraw())

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        events_manager.new_event(OnMouseMotion(x, y, delta_x, delta_y))

    def on_mouse_press(self, x, y, button, key_modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            events_manager.new_event(OnLeftMousePress(x, y, key_modifiers))
        elif button == arcade.MOUSE_BUTTON_RIGHT:
            events_manager.new_event(OnRightMousePress(x, y, key_modifiers))

    def on_mouse_release(self, x, y, button, key_modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            events_manager.new_event(OnLeftMouseRelease(x, y, key_modifiers))
        elif button == arcade.MOUSE_BUTTON_RIGHT:
            events_manager.new_event(OnRightMouseRelease(x, y, key_modifiers))

    def on_update(self, delta_time):
        events_manager.new_event(OnUpdate(delta_time))

    def on_key_press(self, key, key_modifiers):
        """
        For a full list of keys, see:
        https://api.arcade.academy/en/latest/arcade.key.html
        """
        events_manager.new_event(OnKeyPress(key, key_modifiers))

    def on_key_release(self, key, key_modifiers):
        events_manager.new_event(OnKeyRelease(key, key_modifiers))


def main():
    game = Game(SCREEN_WIDTH, SCREEN_HEIGHT, GAME_TITLE)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
