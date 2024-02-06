import arcade
import arcade.gui
from config import FONT_COLOR
from events import (
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


class GameView(arcade.View):
    def __init__(self, events_manager):
        super().__init__()
        self.events_manager = events_manager
        self.events_manager.set_game_ref(self)
        # we use a draw list to avoid problems
        # when multiple modules want to draw and clear the screen after previous module has drawn up
        self.draw_list = []

        self.mouse_x = 0
        self.mouse_y = 0
        self.events_manager.new_event(OnGameInit())

    def setup(self):
        self.events_manager.new_event(OnGameSetup())

    def on_draw(self):
        self.clear()

        for sprite in self.draw_list:
            sprite.draw()
        self.events_manager.new_event(OnDraw())

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        self.mouse_x = x
        self.mouse_y = y
        self.events_manager.new_event(OnMouseMotion(x, y, delta_x, delta_y))

    def on_mouse_press(self, x, y, button, key_modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.events_manager.new_event(OnLeftMousePress(x, y, key_modifiers))
        elif button == arcade.MOUSE_BUTTON_RIGHT:
            self.events_manager.new_event(OnRightMousePress(x, y, key_modifiers))

    def on_mouse_release(self, x, y, button, key_modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.events_manager.new_event(OnLeftMouseRelease(x, y, key_modifiers))
        elif button == arcade.MOUSE_BUTTON_RIGHT:
            self.events_manager.new_event(OnRightMouseRelease(x, y, key_modifiers))

    def on_update(self, delta_time):
        self.events_manager.new_event(OnUpdate(delta_time))

    def on_key_press(self, key, key_modifiers):
        """
        For a full list of keys, see:
        https://api.arcade.academy/en/latest/arcade.key.html
        """
        self.events_manager.new_event(OnKeyPress(key, key_modifiers))

    def on_key_release(self, key, key_modifiers):
        self.events_manager.new_event(OnKeyRelease(key, key_modifiers))


BUTTON_NORMAL = arcade.color.LIGHT_GRAY
BUTTON_HOVER = arcade.color.GRAY
BUTTON_PRESSED = arcade.color.DARK_GRAY
INPUT_BOX_COLOR = arcade.color.WHITE
ERROR_TEXT_COLOR = arcade.color.RED
DEFAULT_STYLE = {
    "font_name": ("Consolas"),
    "font_size": 16,
    "font_color": FONT_COLOR,
    "bg_color": None,
    "bg_color_hover": None,
    "bg_color_press": None,
    "border_width": 0,
    "border_color": None,
    "border_color_hover": None,
    "border_color_press": None,
}


class MainMenuView(arcade.View):
    def __init__(self, events_manager):
        super().__init__()
        self.events_manager = events_manager
        self.ui_manager = None

    def on_show_view(self):
        self.setup()

    def show_game_view(self, event):
        self.ui_manager.disable()
        game_view = GameView(self.events_manager)
        game_view.setup()
        self.window.show_view(game_view)

    def show_login_view(self, event):
        self.ui_manager.disable()
        self.window.show_view(LoginView(self.events_manager))

    def setup(self):
        arcade.set_background_color(arcade.color.BEIGE)
        self.ui_manager = arcade.gui.UIManager()
        self.ui_manager.enable()

        self.ui_manager.add(
            arcade.gui.UILabel(
                text="The Action",
                x=670,
                y=0,
                width=300,
                height=100,
                font_size=48,
                font_name=("微软雅黑", "Consolas"),
            )
        )

        start_button = arcade.gui.UIFlatButton(
            text="开始行动",
            x=520,
            y=366 - 70,
            width=300,
            height=70,
            id="start_button",
            style={
                "font_name": ("微软雅黑", "Consolas"),
                "font_size": 24,
                "font_color": arcade.color.BLACK,
                "bg_color": BUTTON_NORMAL,
                "bg_color_hover": BUTTON_HOVER,
                "bg_color_press": BUTTON_PRESSED,
                "border_width": 2,
                "border_color": arcade.color.BLACK,
                "border_color_hover": arcade.color.WHITE,
                "border_color_press": arcade.color.WHITE,
            },
        )
        start_button.on_click = self.show_game_view
        self.ui_manager.add(start_button)

        login_button = arcade.gui.UIFlatButton(
            text="登录Login",
            x=520,
            y=440 - 50,
            width=300,
            height=50,
            font_size=18,
            font_name="Consolas",
            id="show_login_view_button",
            style={
                "font_name": ("Consolas"),
                "font_size": 20,
                "font_color": arcade.color.BLACK,
                "bg_color": BUTTON_NORMAL,
                "bg_color_hover": BUTTON_HOVER,
                "bg_color_press": BUTTON_PRESSED,
                "border_width": 2,
                "border_color": arcade.color.BLACK,
                "border_color_hover": arcade.color.WHITE,
                "border_color_press": arcade.color.WHITE,
            },
        )
        login_button.on_click = self.show_login_view
        self.ui_manager.add(login_button)

        settings_button = arcade.gui.UIFlatButton(
            text="设置",
            x=1171,
            y=716 - 50,
            width=150,
            height=50,
            font_size=18,
            font_name="Consolas",
            id="settings_button",
            style={
                "font_name": ("微软雅黑", "Consolas"),
                "font_size": 20,
                "font_color": arcade.color.BLACK,
                "bg_color": BUTTON_NORMAL,
                "bg_color_hover": BUTTON_HOVER,
                "bg_color_press": BUTTON_PRESSED,
                "border_width": 2,
                "border_color": arcade.color.BLACK,
                "border_color_hover": arcade.color.WHITE,
                "border_color_press": arcade.color.WHITE,
            },
        )
        self.ui_manager.add(settings_button)

    def on_draw(self):
        self.clear()
        self.ui_manager.draw()


class LoginView(arcade.View):
    def __init__(self, events_manager):
        super().__init__()
        self.events_manager = events_manager
        self.ui_manager = None
        self.username_input = None
        self.password_input = None
        self.error_label = None

    def on_show_view(self):
        self.setup()

    def back_to_main_menu(self, event):
        self.ui_manager.disable()
        self.window.show_view(MainMenuView(self.events_manager))

    def verify_login(self, event):
        username = self.username_input.text
        password = self.password_input.text
        if username == "admin" and password == "password":
            self.error_label.text = ""
            self.events_manager.new_event(BeforeGameInit())
            self.window.show_view(GameView(self.events_manager))
        else:
            self.error_label.text = "用户名或密码错误"

    def setup(self):
        arcade.set_background_color(arcade.color.BEIGE)
        self.ui_manager = arcade.gui.UIManager()
        self.ui_manager.enable()

        self.username_input = arcade.gui.UIInputText(
            text="username",
            x=520,
            y=320 - 40,
            width=300,
            height=40,
            font_size=16,
            font_name="Consolas",
        )
        self.ui_manager.add(self.username_input)

        self.password_input = arcade.gui.UIInputText(
            text="password",
            x=520,
            y=380 - 40,
            width=300,
            height=40,
            font_size=16,
            font_name="Consolas",
        )
        self.ui_manager.add(self.password_input)

        login_button = arcade.gui.UIFlatButton(
            text="登录",
            x=520,
            y=440 - 50,
            width=300,
            height=50,
            font_size=20,
            font_name="Consolas",
            id="login_button",
            style={
                "font_name": ("微软雅黑", "Consolas"),
                "font_size": 20,
                "font_color": arcade.color.BLACK,
                "bg_color": BUTTON_NORMAL,
                "bg_color_hover": BUTTON_HOVER,
                "bg_color_press": BUTTON_PRESSED,
                "border_width": 2,
                "border_color": arcade.color.BLACK,
                "border_color_hover": arcade.color.WHITE,
                "border_color_press": arcade.color.WHITE,
            },
        )
        login_button.on_click = self.verify_login
        self.ui_manager.add(login_button)

        self.error_label = arcade.gui.UILabel(
            text="",
            x=520,
            y=500,
            font_size=16,
            font_name="微软雅黑",
            text_color=ERROR_TEXT_COLOR,
        )
        self.ui_manager.add(self.error_label)

        back_button = arcade.gui.UIFlatButton(
            text="返回主菜单",
            x=670,
            y=716 - 50,
            width=150,
            height=50,
            font_size=18,
            font_name="Consolas",
            id="back_button",
            style={
                "font_name": ("微软雅黑", "Consolas"),
                "font_size": 20,
                "font_color": arcade.color.BLACK,
                "bg_color": BUTTON_NORMAL,
                "bg_color_hover": BUTTON_HOVER,
                "bg_color_press": BUTTON_PRESSED,
                "border_width": 2,
                "border_color": arcade.color.BLACK,
                "border_color_hover": arcade.color.WHITE,
                "border_color_press": arcade.color.WHITE,
            },
        )
        back_button.on_click = self.back_to_main_menu
        self.ui_manager.add(back_button)

    def on_draw(self):
        self.clear()
        self.ui_manager.draw()
