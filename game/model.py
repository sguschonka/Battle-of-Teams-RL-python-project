class FighterModel:
    def __init__(self, name: str, base_strength: int):
        self._name = name
        self._strength = base_strength
        self._base_strength = base_strength
        self._kills = 0
        self._alive = True

    @property  # getters and setters
    def alive(self):
        return self._alive

    def take_damage(self, damage: int):
        self._strength -= damage
        if self._strength <= 0:
            self._alive = False
            self._strength = 0


class TeamModel:
    def __init__(self, fighters: list[FighterModel]):
        self._size = 3  # constraint to implement simple RL
        self._fighters = fighters
        self._alive_counter = sum(1 for f in fighters if f.alive)
        self._filename = None

    def alive_counter_update(self):
        self._alive_counter = sum(1 for f in self._fighters if f.alive)
