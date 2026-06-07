from dataclasses import dataclass, field


@dataclass()
class FighterState:
    name: str = "fighter"
    strength: int = 0
    base_strength: int = 1
    kills: int = 0
    alive: bool = True


@dataclass()
class TeamState:
    name: str = "Command"
    size: int = 3  # constraint to implement simple RL
    fighters: list = field(default_factory=list)
    filename = None


class FighterModel:
    def __init__(self):
        self.state = FighterState()

    @property  # getters and setters
    def alive(self):
        return self.state.alive

    def take_damage(self, damage: int):
        self.state.strength -= damage
        if self.state.strength <= 0:
            self.state.alive = False
            self.state.strength = 0


class TeamModel:
    def __init__(self, fighters: list[FighterModel], name: str):
        self.state = TeamState(name=name, fighters=fighters)
        self.validate_team_strength()

    def alive_counter_update(self):
        return sum(1 for f in self.state.fighters if f.state.alive)

    def validate_team_strength(self):
        total = sum(f.state.base_strength for f in self.state.fighters)
        if total > 30:
            raise ValueError("Превышена суммарная сила команды")


try:
    team_zalupenko = TeamModel(
        fighters=[
            FighterModel(),
            FighterModel(),
            FighterModel(),
        ],
        name="Команда Залупенко",
    )

    team_zalupenko.state.fighters[0].state.name = "Дима Залупенко"
    team_zalupenko.state.fighters[1].state.name = "Дарья Залупенко"
    team_zalupenko.state.fighters[2].state.name = "Саша Залупенко"

    team_zalupenko.state.fighters[0].state.base_strength = 55
    team_zalupenko.state.fighters[1].state.base_strength = 2
    team_zalupenko.state.fighters[2].state.base_strength = 8

    team_zalupenko.validate_team_strength()
except ValueError as e:
    print(e)

print(team_zalupenko.state.name)
print([f.state for f in team_zalupenko.state.fighters])
