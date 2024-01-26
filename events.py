import importlib


class Event:
    def __init__(self):
        pass


class EventsManager:
    def __init__(self):
        self.events = {}
        self.game_ref = None

    def set_game_ref(self, game_ref):
        self.game_ref = game_ref

    def register(self, event):
        if type(event) == list:
            for e in event:
                self.events[e] = []
        else:
            self.events[event] = []

    def subscribe(self, event, func):
        if type(func) == list:
            for f in func:
                self.events[event].append(f)
        else:
            self.events[event].append(func)

    def multi_subscribe(self, subscriptions):
        for event, func in subscriptions.items():
            self.subscribe(event, func)

    def new_event(self, new_event):
        event_type = type(new_event)
        for event, func_list in self.events.items():
            if event == event_type:
                for func in func_list:
                    func(self.game_ref, new_event)
                return

    def import_module(self, name):
        module = importlib.import_module(name)
        if hasattr(module, "subscriptions"):
            self.multi_subscribe(module.subscriptions)

    def import_modules(self, names):
        for name in names:
            self.import_module(name)


class OnMouseMotion(Event):
    def __init__(self, x, y, delta_x, delta_y):
        self.x = x
        self.y = y
        self.delta_x = delta_x
        self.delta_y = delta_y


class OnMousePress(Event):
    def __init__(self, x, y, button, key_modifiers):
        self.x = x
        self.y = y
        self.button = button
        self.key_modifiers = key_modifiers


class OnMouseRelease(Event):
    def __init__(self, x, y, button, key_modifiers):
        self.x = x
        self.y = y
        self.button = button
        self.key_modifiers = key_modifiers


class OnDraw(Event):
    def __init__(self):
        pass


class OnSetup(Event):
    def __init__(self):
        pass


class BeforeGameInit(Event):
    def __init__(self):
        pass


class OnUpdate(Event):
    def __init__(self, delta_time):
        self.delta_time = delta_time


class OnKeyPress(Event):
    def __init__(self, key, key_modifiers):
        self.key = key
        self.key_modifiers = key_modifiers


class OnKeyRelease(Event):
    def __init__(self, key, key_modifiers):
        self.key = key
        self.key_modifiers = key_modifiers


class OnGameInit(Event):
    def __init__(self):
        pass


default_events_list = [
    OnDraw,
    OnMouseMotion,
    OnMousePress,
    OnMouseRelease,
    OnSetup,
    BeforeGameInit,
    OnGameInit,
    OnUpdate,
    OnKeyPress,
    OnKeyRelease,
]
