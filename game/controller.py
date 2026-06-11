import random
from pathlib import Path
from game.model import BattleModel
from game.ai_player import AIPlayer


class GameController:
    def __init__(self, root, view):
        self.root = root
        self.view = view
        self.battle = None
        self.ai_player = None
        self.mode = None
        self.current_player = None

        try:
            current_dir = Path(__file__).parent
            self.MODEL_PATH = current_dir / "environment" / "BattleOfTeams-v1.pt"
        except Exception as e:
            print(f"Ошибка загрузки модели: {e}")

    def start_new_game(self, mode: str):
        self.mode = mode
        team1 = BattleModel.create_random_team("Red Team")
        team2 = BattleModel.create_random_team("Blue Team")

        if mode == "pve":
            self.battle = BattleModel(team1, team2)
            self.ai_player = AIPlayer(
                checkpoint_path=self.MODEL_PATH, obs_rms_path=None
            )
            if random.choice([True, False]):  # Random choice True - adent
                self.current_player = "agent"
            else:
                self.current_player = "player"
        else:  # pvp
            self.battle = BattleModel(team1, team2)
            self.current_player = random.choice(["player1", "player2"])

        self.view.create_game_screen(
            self.battle.team_agent, self.battle.team_player, self.current_player
        )

        if mode == "pve" and self.current_player == "agent":
            self.root.after(500, self._make_ai_move)

    def _make_ai_move(self):
        if self.battle.winner or self.current_player != "agent":
            return

        obs = self.battle.get_observation(for_agent_team=True)
        raw_action = self.ai_player.get_action(obs)

        valid_actions = []
        for a in range(3):
            if not self.battle.team_agent.fighters[a].alive:
                continue
            for d in range(3):
                if self.battle.team_player.fighters[d].alive:
                    valid_actions.append(a * 3 + d)

        if not valid_actions:
            return

        action = (
            raw_action if raw_action in valid_actions else random.choice(valid_actions)
        )
        attacker_idx, defender_idx = divmod(action, 3)

        attacker = self.battle.team_agent.fighters[attacker_idx]
        defender = self.battle.team_player.fighters[defender_idx]
        att_str_before = attacker.strength
        def_str_before = defender.strength

        attack_val, defense_val = self.battle.execute_round(
            self.battle.team_agent, self.battle.team_player, action
        )

        self._log_round(
            attacker,
            defender,
            attack_val,
            defense_val,
            att_str_before,
            def_str_before,
            is_ai=True,
        )

        self._after_move()

    def on_player_action(self, attacker_idx: int, defender_idx: int):
        if self.battle.winner:
            return

        # We determine which team is attacking and which is defending
        if self.mode == "pve":
            if self.current_player != "player":
                return
            attacker_team = self.battle.team_player
            defender_team = self.battle.team_agent
        else:  # pvp
            if self.current_player == "player1":
                attacker_team = self.battle.team_agent
                defender_team = self.battle.team_player
            elif self.current_player == "player2":
                attacker_team = self.battle.team_player
                defender_team = self.battle.team_agent
            else:
                return

        if not attacker_team.fighters[
            attacker_idx
        ].alive:  # Checking that the selected fighters are alive
            self.view.log_message("❌ Атакующий боец мёртв! Выберите другого.")
            return
        if not defender_team.fighters[defender_idx].alive:
            self.view.log_message("❌ Защитник мёртв! Выберите другого.")
            return

        attacker = attacker_team.fighters[attacker_idx]
        defender = defender_team.fighters[defender_idx]
        att_str_before = attacker.strength
        def_str_before = defender.strength
        action = attacker_idx * 3 + defender_idx

        attack_val, defense_val = self.battle.execute_round(
            attacker_team, defender_team, action
        )
        self._log_round(
            attacker,
            defender,
            attack_val,
            defense_val,
            att_str_before,
            def_str_before,
            is_ai=False,
        )

        self._after_move()

    def _log_round(
        self,
        attacker,
        defender,
        attack_val,
        defense_val,
        att_str_before,
        def_str_before,
        is_ai: bool,
    ):
        prefix = "🤖 AI ходит: " if is_ai else "🎮 Ход игрока: "
        log_msg = f"{prefix}атакует {attacker.name} (число {attack_val}) -> защитник {defender.name} (число {defense_val}). "
        if attacker.strength > att_str_before:
            log_msg += f"Победа! {attacker.name} усиливается до {attacker.strength}, "
        else:
            log_msg += f"Поражение! {attacker.name} ослабевает до {attacker.strength}, "
        if defender.strength < def_str_before:
            log_msg += f"{defender.name} ослабевает до {defender.strength}. "
        else:
            log_msg += f"{defender.name} усиливается до {defender.strength}. "
        if not defender.alive:
            log_msg += f"💀 {defender.name} убит! "
        if not attacker.alive:
            log_msg += f"💀 {attacker.name} убит! "
        self.view.log_message(log_msg)

    def _after_move(self):  # Post-move update (switch player, check winner)
        if self.battle.winner:
            self.view.update_game_screen(
                self.battle.team_agent,
                self.battle.team_player,
                self.current_player,
                self.battle.winner,
            )
            return

        if self.mode == "pve":
            self.current_player = (
                "player" if self.current_player == "agent" else "agent"
            )
            self.view.update_game_screen(
                self.battle.team_agent,
                self.battle.team_player,
                self.current_player,
                None,
            )
            if self.current_player == "agent":
                self.root.after(500, self._make_ai_move)
        else:  # pvp
            self.current_player = (
                "player1" if self.current_player == "player2" else "player2"
            )
            self.view.update_game_screen(
                self.battle.team_agent,
                self.battle.team_player,
                self.current_player,
                None,
            )

    def on_skip_ai_turn(self):
        if self.mode == "pve" and self.current_player == "agent":
            self._make_ai_move()

    def return_to_main_menu(self):
        self.battle = None
        self.ai_player = None
