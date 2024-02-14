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


def create_style(
    font_color_pressed,
    border_color,
    border_color_hovered,
    border_color_pressed,
    bg_color,
    bg_color_hovered,
    bg_color_pressed,
):
    return {
        "font_name": ("calibri", "arial"),
        "font_size": 15,
        "font_color": arcade.color.WHITE,
        "font_color_pressed": font_color_pressed,
        "border_width": 2,
        "border_color": border_color,
        "border_color_hovered": border_color_hovered,
        "border_color_pressed": border_color_pressed,
        "bg_color": bg_color,
        "bg_color_hovered": bg_color_hovered,
        "bg_color_pressed": bg_color_pressed,
    }


def create_button(text, width, height, style, action):
    button = arcade.gui.UIFlatButton(text=text, width=width, height=height, style=style)
    button.on_click = action
    return button


class MainMenuView(arcade.View):
    BUTTON_WIDTH = 600
    BUTTON_HEIGHT = 50
    SPACE_BETWEEN = 20
    H_SPACE = 20

    def __init__(self, events_manager):
        super().__init__()
        self.events_manager = events_manager
        self.ui_manager = arcade.gui.UIManager()

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
        arcade.set_background_color(arcade.color.ARSENIC)
        self.ui_manager.enable()

        # Vertical box
        v_box = arcade.gui.UIBoxLayout(space_between=self.SPACE_BETWEEN)

        # Horizontal box
        h_box = arcade.gui.UIBoxLayout(space_between=self.H_SPACE, vertical=False)

        # Create and add game label
        style = {"font_color": (79, 74, 45)}
        game_label = arcade.gui.UILabel(
            text="The Action",
            width=self.BUTTON_WIDTH,
            id="game_label",
            font_size=48,
            style=style,
        )
        v_box.add(game_label)

        # Button styles
        start_button_style = create_style(
            (230, 230, 230),
            *[
                (90, 115, 87),
                (109, 130, 106),
                (98, 123, 89),
                (90, 115, 87),
                (109, 130, 106),
                (82, 107, 79),
            ],
        )
        login_button_style = create_style(
            (230, 230, 230),
            *[
                (74, 99, 120),
                (94, 122, 142),
                (67, 89, 108),
                (74, 99, 120),
                (94, 122, 142),
                (59, 79, 98),
            ],
        )
        settings_button_style = create_style(
            (230, 230, 230),
            *[
                (106, 78, 66),
                (126, 98, 88),
                (96, 70, 60),
                (106, 78, 66),
                (126, 98, 88),
                (85, 62, 54),
            ],
        )
        exit_button_style = create_style(
            (245, 245, 245),
            *[
                (128, 35, 35),
                (180, 50, 50),
                (115, 22, 22),
                (155, 30, 30),
                (175, 45, 45),
                (140, 25, 25),
            ],
        )
        print(start_button_style)

        print(login_button_style)
        print(settings_button_style)
        print(exit_button_style)

        # Create and add buttons
        v_box.add(
            create_button(
                "Carry out the Action",
                self.BUTTON_WIDTH,
                self.BUTTON_HEIGHT,
                start_button_style,
                self.show_game_view,
            )
        )
        v_box.add(
            create_button(
                "登录Login",
                self.BUTTON_WIDTH,
                self.BUTTON_HEIGHT,
                login_button_style,
                self.show_login_view,
            )
        )

        # Horizontal box for settings and exit buttons
        h_box.add(
            create_button(
                "设置",
                (self.BUTTON_WIDTH - self.H_SPACE) // 2,
                self.BUTTON_HEIGHT,
                settings_button_style,
                lambda x: x,
            )
        )
        h_box.add(
            create_button(
                "退出",
                (self.BUTTON_WIDTH - self.H_SPACE) // 2,
                self.BUTTON_HEIGHT,
                exit_button_style,
                self.exit_game,
            )
        )

        # Add horizontal box to the vertical box
        v_box.add(h_box)

        self.ui_manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x", anchor_y="center_y", child=v_box
            )
        )

    def on_draw(self):
        self.clear()
        self.ui_manager.draw()


class PasswordInputBox(arcade.gui.UIInputText):
    def __init__(self, x=0, y=0, width=0, height=0, text="", style=None):
        super().__init__(x=x, y=y, width=width, height=height, text=text, style=style)
        self.password_char = "*"

    def draw(self):
        temp_text = self.text
        if self.focused:
            self.text = self.password_char * len(self.text)
        super().draw()
        self.text = temp_text


class PlaceholderInputBox(arcade.gui.UIInputText):
    def __init__(
        self, x=0, y=0, width=0, height=0, text="", placeholder="", style=None
    ):
        super().__init__(x=x, y=y, width=width, height=height, text=text, style=style)
        self.placeholder = placeholder
        self.is_focused = False

    def on_focus(self):
        self.is_focused = True
        if not self.text:
            self.text = ""

    def on_unfocus(self):
        self.is_focused = False
        if self.text.strip() == "":
            self.text = self.placeholder

    def draw(self):
        if not self.is_focused and not self.text:
            self.text = self.placeholder
        super().draw()
        # if self.text:
        #     self.text = ""


class LoginView(arcade.View):
    BUTTON_WIDTH = 350
    BUTTON_HEIGHT = 50
    SPACE_BETWEEN = 20
    H_SPACE = 60

    def __init__(self, events_manager):
        super().__init__()
        self.events_manager = events_manager
        self.ui_manager = arcade.gui.UIManager()
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
        arcade.set_background_color(arcade.color.ARSENIC)
        self.ui_manager.enable()
        self.v_box = arcade.gui.UIBoxLayout(space_between=self.SPACE_BETWEEN)
        self.h_box = arcade.gui.UIBoxLayout(space_between=self.H_SPACE, vertical=False)

        self.username_label = arcade.gui.UILabel(
            text="用户名",
            width=300,
            height=40,
            font_size=16,
            font_name="微软雅黑",
            dpi=100,
        )
        self.v_box.add(self.username_label)

        self.username_input = arcade.gui.UIInputText(
            text="username",
            width=300,
            height=40,
            font_size=16,
            font_name="Consolas",
            text_color=(229, 231, 233),
        )
        self.v_box.add(self.username_input)

        self.password_label = arcade.gui.UILabel(
            text="密码",
            width=300,
            height=40,
            font_size=16,
            font_name="微软雅黑",
            dpi=100,
        )
        self.v_box.add(self.password_label)

        self.password_input = arcade.gui.UIInputText(
            text="password",
            width=300,
            height=40,
            font_size=16,
            font_name="Consolas",
            style={
                "bg_color": (240, 240, 240),
                "border_color": (200, 200, 200),
                "font_color": (32, 32, 32),
            },
        )
        self.v_box.add(self.password_input)

        login_button_style = create_style(
            (230, 230, 230),
            *[(0, 123, 255), (30, 144, 255), (0, 95, 230)],
            *[(0, 104, 255), (30, 130, 255), (0, 78, 204)],
        )
        self.h_box.add(
            create_button(
                "登录",
                (self.BUTTON_WIDTH - self.H_SPACE) // 2,
                self.BUTTON_HEIGHT,
                login_button_style,
                self.verify_login,
            )
        )

        back_button_style = create_style(
            (245, 245, 245),
            *[(130, 130, 130), (165, 165, 165), (120, 120, 120)],
            *[(150, 150, 150), (170, 170, 170), (140, 140, 140)],
        )
        self.h_box.add(
            create_button(
                "返回主菜单",
                (self.BUTTON_WIDTH - self.H_SPACE) // 2,
                self.BUTTON_HEIGHT,
                back_button_style,
                self.back_to_main_menu,
            )
        )

        self.v_box.add(self.h_box)

        # self.error_label = arcade.gui.UILabel(
        #     text="",
        #     x=520,
        #     y=500,
        #     font_size=16,
        #     font_name="微软雅黑",
        #     text_color=ERROR_TEXT_COLOR,
        # )
        # self.v_box.add(self.error_label)

        self.ui_manager.add(arcade.gui.UIAnchorWidget(child=self.v_box))

    def on_draw(self):
        self.clear()
        self.ui_manager.draw()
