class Event:
    def __init__(self):
        pass


class EventsManager:
    def __init__(self):
        self.events = {}

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

    def new_event(self, new_event):
        event_type = type(new_event)
        for event, func_list in self.events.items():
            if event == event_type:
                for func in func_list:
                    func(self.game_ref, new_event)
                return


class OnMouseMotion(Event):
    def __init__(self, x, y):
        self.x = x
        self.y = y


class OnMousePress(Event):
    def __init__(self, x, y):
        self.x = x
        self.y = y


class OnMouseRelease(Event):
    def __init__(self, x, y):
        self.x = x
        self.y = y


class OnDraw(Event):
    def __init__(self):
        pass


class OnSetup(Event):
    def __init__(self):
        pass
