import importlib
from loguru import logger


class Event:
    def __init__(self):
        pass


class OnMouseMotion(Event):
    def __init__(self, x, y, delta_x, delta_y):
        self.x = x
        self.y = y
        self.delta_x = delta_x
        self.delta_y = delta_y


class OnLeftMousePress(Event):
    def __init__(self, x, y, key_modifiers):
        self.x = x
        self.y = y
        self.key_modifiers = key_modifiers


class OnRightMousePress(Event):
    def __init__(self, x, y, key_modifiers):
        self.x = x
        self.y = y
        self.key_modifiers = key_modifiers


class OnLeftMouseRelease(Event):
    def __init__(self, x, y, key_modifiers):
        self.x = x
        self.y = y
        self.key_modifiers = key_modifiers


class OnRightMouseRelease(Event):
    def __init__(self, x, y, key_modifiers):
        self.x = x
        self.y = y
        self.key_modifiers = key_modifiers


class OnDraw(Event):
    def __init__(self):
        pass


class OnGameSetup(Event):
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


class OnCellSelected(Event):
    def __init__(self, row, column):
        self.row = row
        self.column = column


IGNORED_EVENTS_LOGGING = [OnUpdate, OnDraw, OnMouseMotion]


class EventsManager:
    def __init__(self):
        self.events = {}
        self.game_ref = None

    def set_game_ref(self, game_ref):
        self.game_ref = game_ref

    def register(self, event):
        if isinstance(event, list):
            for e in event:
                logger.debug(f"Registering event: {e.__name__}")
                self.events[e] = []
        else:
            logger.debug(f"Registering event: {event}")
            self.events[event] = []

    def subscribe(self, event, func):
        if isinstance(func, list):
            for f in func:
                logger.debug(f"{event.__name__} -> {f.__name__}")
                self.events[event].append(f)
        else:
            logger.debug(f"{event.__name__} -> {func.__name__}")
            self.events[event].append(func)

    def multi_subscribe(self, subscriptions):
        for event, func in subscriptions.items():
            self.subscribe(event, func)

    def new_event(self, new_event):
        event_type = type(new_event)
        if event_type not in IGNORED_EVENTS_LOGGING:
            logger.debug(f"New event: {new_event.__class__.__name__}")
        for event, func_list in self.events.items():
            if event == event_type:
                for func in func_list:
                    if event_type not in IGNORED_EVENTS_LOGGING:
                        logger.debug(
                            f"Calling function: {func.__name__} with event: {new_event.__class__.__name__}"
                        )
                    func(self.game_ref, new_event, self)
                return

    def import_module(self, name):
        logger.debug(f"Importing module: {name}")
        module = importlib.import_module(name)
        if hasattr(module, "subscriptions"):
            logger.debug(f"Found subscriptions in module: {name}")
            self.multi_subscribe(module.subscriptions)
        if hasattr(module, "registrations"):
            logger.debug(f"Found registrations in module: {name}")
            self.register(module.registrations)

    def import_modules(self, names):
        for name in names:
            self.import_module(name)

    def verbose_subscription_info(self):
        logger.info("Event subscriptions:")
        for event, func_list in self.events.items():
            logger.info(f"{event.__name__}:")
            for func in func_list:
                logger.info(f"  {func.__name__}")


DEFAULT_EVENT_LIST = [
    OnDraw,
    OnMouseMotion,
    OnLeftMousePress,
    OnRightMousePress,
    OnLeftMouseRelease,
    OnRightMouseRelease,
    OnGameSetup,
    BeforeGameInit,
    OnGameInit,
    OnUpdate,
    OnKeyPress,
    OnKeyRelease,
    OnCellSelected,
]
