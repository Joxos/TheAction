import arcade
import arcade.gui
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

    def exit_game(self, event):
        arcade.exit()

    def setup(self):
        self.ui_manager = arcade.gui.UIManager()
        self.ui_manager.enable()
        self.v_box = arcade.gui.UIBoxLayout(space_between=20)
        arcade.set_background_color(arcade.color.ARSENIC)

        style = {"font_color": (79, 74, 45)}
        game_label = arcade.gui.UILabel(
            text="The Action",
            width=400,
            height=100,
            style=style,
            id="game_label",
            font_size=48,
        )
        self.v_box.add(game_label)

        style = {
            "font_name": ("calibri", "arial"),
            "font_size": 15,
            "font_color": arcade.color.WHITE,
            "font_color_pressed": (230, 230, 230),
            "border_width": 2,
            "border_color": (90, 115, 87),
            "border_color_hovered": (109, 130, 106),
            "border_color_pressed": (98, 123, 89),
            "bg_color": (90, 115, 87),
            "bg_color_hovered": (109, 130, 106),
            "bg_color_pressed": (82, 107, 79),
        }
        start_button = arcade.gui.UIFlatButton(
            text="Carry out the Action",
            width=300,
            height=70,
            id="start_button",
            style=style,
        )
        start_button.on_click = self.show_game_view
        self.v_box.add(start_button)

        style = {
            "font_name": ("calibri", "arial"),
            "font_size": 15,
            "font_color": arcade.color.WHITE,
            "font_color_pressed": (230, 230, 230),
            "border_width": 2,
            "border_color": (74, 99, 120),
            "border_color_hovered": (94, 122, 142),
            "border_color_pressed": (67, 89, 108),
            "bg_color": (74, 99, 120),
            "bg_color_hovered": (94, 122, 142),
            "bg_color_pressed": (59, 79, 98),
        }
        login_button = arcade.gui.UIFlatButton(
            text="登录Login",
            width=300,
            height=50,
            font_size=18,
            font_name="Consolas",
            id="show_login_view_button",
            style=style,
        )
        login_button.on_click = self.show_login_view
        self.v_box.add(login_button)

        style = {
            "font_name": ("calibri", "arial"),
            "font_size": 15,
            "font_color": arcade.color.WHITE,
            "font_color_pressed": (230, 230, 230),
            "border_width": 2,
            "border_color": (106, 78, 66),
            "border_color_hovered": (126, 98, 88),
            "border_color_pressed": (96, 70, 60),
            "bg_color": (106, 78, 66),
            "bg_color_hovered": (126, 98, 88),
            "bg_color_pressed": (85, 62, 54),
        }
        settings_button = arcade.gui.UIFlatButton(
            text="设置",
            width=300,
            height=50,
            font_size=18,
            font_name="Consolas",
            id="settings_button",
            style=style,
        )
        self.v_box.add(settings_button)

        style = {
            "font_name": ("calibri", "arial"),
            "font_size": 15,
            "font_color": arcade.color.WHITE,
            "font_color_pressed": (245, 245, 245),
            "border_width": 2,
            "border_color": (128, 35, 35),
            "border_color_hovered": (180, 50, 50),
            "border_color_pressed": (115, 22, 22),
            "bg_color": (155, 30, 30),
            "bg_color_hovered": (175, 45, 45),
            "bg_color_pressed": (140, 25, 25),
        }
        exit_button = arcade.gui.UIFlatButton(
            text="退出",
            width=300,
            height=50,
            font_size=18,
            font_name="Consolas",
            id="settings_button",
            style=style,
        )
        exit_button.on_click = self.exit_game
        self.v_box.add(exit_button)

        self.ui_manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x", anchor_y="center_y", child=self.v_box
            )
        )

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
        self.ui_manager = arcade.gui.UIManager()
        self.ui_manager.enable()
        self.v_box = arcade.gui.UIBoxLayout(space_between=20)
        arcade.set_background_color(arcade.color.ARSENIC)

        self.username_input = arcade.gui.UIInputText(
            text="username",
            width=300,
            height=40,
            font_size=16,
            font_name="Consolas",
        )
        self.v_box.add(self.username_input)

        self.password_input = arcade.gui.UIInputText(
            text="password",
            width=300,
            height=40,
            font_size=16,
            font_name="Consolas",
        )
        self.v_box.add(self.password_input)

        login_button = arcade.gui.UIFlatButton(
            text="登录",
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
        self.v_box.add(login_button)

        self.error_label = arcade.gui.UILabel(
            text="",
            x=520,
            y=500,
            font_size=16,
            font_name="微软雅黑",
            text_color=ERROR_TEXT_COLOR,
        )
        self.v_box.add(self.error_label)

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
        self.v_box.add(back_button)

        self.ui_manager.add(arcade.gui.UIAnchorWidget(child=self.v_box))

    def on_draw(self):
        self.clear()
        self.ui_manager.draw()
