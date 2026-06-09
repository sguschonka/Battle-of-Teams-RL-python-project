# model.py
from dataclasses import dataclass
from typing import List
import random

@dataclass
class Fighter:
    name: str
    strength: int
    alive: bool = True

@dataclass
class Team:
    name: str
    fighters: List[Fighter]

    def total_strength(self) -> int:
        return sum(f.strength for f in self.fighters if f.alive)

    def alive_count(self) -> int:
        return sum(1 for f in self.fighters if f.alive)

    def is_defeated(self) -> bool:
        return self.alive_count() == 0

class BattleModel:
    def __init__(self, team1: Team, team2: Team):
        self.team_agent = team1   # AI или первый игрок
        self.team_player = team2  # человек или второй игрок
        self.winner = None

    @staticmethod
    def create_random_team(name: str, total_strength: int = 100, num_fighters: int = 3) -> Team:
        strengths = []
        remaining = total_strength
        for i in range(num_fighters - 1):
            s = random.randint(1, max(1, remaining - (num_fighters - i -1)))
            strengths.append(s)
            remaining -= s
        strengths.append(remaining)
        fighters = [Fighter(name=f"Боец {i+1}", strength=s) for i, s in enumerate(strengths)]
        return Team(name=name, fighters=fighters)

    def execute_round(self, attacker_team: Team, defender_team: Team, action: int) -> float | tuple[int, int]:
        num_f = len(attacker_team.fighters)
        attacker_idx = action // num_f
        defender_idx = action % num_f

        alive_attackers = [i for i, f in enumerate(attacker_team.fighters) if f.alive]
        alive_defenders = [i for i, f in enumerate(defender_team.fighters) if f.alive]

        if not alive_attackers or not alive_defenders:
            return 0.0

        if attacker_idx not in alive_attackers or defender_idx not in alive_defenders:
            attacker_idx = random.choice(alive_attackers)
            defender_idx = random.choice(alive_defenders)

        attacker = attacker_team.fighters[attacker_idx]
        defender = defender_team.fighters[defender_idx]

        attack_val = random.randint(0, attacker.strength)
        defense_val = random.randint(0, defender.strength)
        min_val = min(attack_val, defense_val)

        if attack_val==defense_val:
            if random.random() < 0.5:
                attacker.strength += min_val
                defender.strength -= min_val
                if defender.strength <= 0:
                    defender.alive = False
                    defender.strength = 0
            else:
                defender.strength += min_val
                attacker.strength -= min_val
                if attacker.strength <= 0:
                    attacker.alive = False
                    attacker.strength = 0

        else:
            if defense_val == min_val:
                attacker.strength += min_val
                defender.strength -= min_val
                if defender.strength <= 0:
                    defender.alive = False
                    defender.strength = 0
            else:
                defender.strength += min_val
                attacker.strength -= min_val
                if attacker.strength <= 0:
                    attacker.alive = False
                    attacker.strength = 0

        for f in attacker_team.fighters + defender_team.fighters:
            f.strength = max(0, int(f.strength))

        if attacker_team.is_defeated():
            self.winner = defender_team.name
        elif defender_team.is_defeated():
            self.winner = attacker_team.name

        return attack_val, defense_val

    def get_observation(self, for_agent_team: bool = True) -> List[float]:
        if for_agent_team:
            team_a = self.team_agent
            team_b = self.team_player
        else:
            team_a = self.team_player
            team_b = self.team_agent

        obs = []
        for team in (team_a, team_b):
            for fighter in team.fighters:
                obs.append(float(fighter.strength if fighter.alive else 0))
                obs.append(1.0 if fighter.alive else 0.0)
        return obs