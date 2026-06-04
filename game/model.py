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
    def __init__(self, fighters: list[FighterModel], name: str):
        self._name = name
        self._size = 3  # constraint to implement simple RL
        self._fighters = fighters
        self._alive_counter = sum(1 for f in fighters if f.alive)
        self._filename = None

    def alive_counter_update(self):
        self._alive_counter = sum(1 for f in self._fighters if f.alive)


team_zalupenko = TeamModel(
    fighters=[
        FighterModel("Залупенко Михаил", 50),
        FighterModel("Залупенко Александр", 25),
        FighterModel("Залупенко Антон", 25),
    ],
    name="Команда Залупенко",
)

print(team_zalupenko._name)
print([f._name for f in team_zalupenko._fighters])
