class Army:
    def __init__(self, id, position, color, move_interval, sprite=None):
        self.id = id
        self.position = position
        self.color = color
        self.move_interval = move_interval  # ticks between move
        self.move_interval_counter = 0
        self.sprite = sprite
        self.waypoints = []
        self.is_marching = False
