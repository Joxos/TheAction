class Army:
    def __init__(self, id, pos, color, max_hp, attack, attack_interval,speed, sprite=None):
        self.id = id
        self.pos = pos
        self.color = color
        self.max_hp = max_hp
        self.hp = max_hp
        self.attack = attack
        self.attack_interval = attack_interval
        self.last_attack_tick = 0
        self.speed = speed
        self.last_move_tick = self.speed
        self.sprite = sprite
        self.marching = False
        self.waypoints = []
