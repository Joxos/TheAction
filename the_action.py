import arcade
from config import SCREEN_HEIGHT, SCREEN_WIDTH, GAME_TITLE, DEFAULT_MODULES
from events import EventsManager, DEFAULT_EVENT_LIST
from views import MainMenuView


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, GAME_TITLE)
    window.center_window()

    events_manager = EventsManager()
    events_manager.register(DEFAULT_EVENT_LIST)
    events_manager.import_modules(DEFAULT_MODULES)
    events_manager.verbose_subscription_info()
    main_view = MainMenuView(events_manager)
    window.show_view(main_view)
    arcade.run()


if __name__ == "__main__":
    main()
