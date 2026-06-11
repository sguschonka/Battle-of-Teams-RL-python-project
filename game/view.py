import tkinter as tk
from tkinter import scrolledtext
from tkinter import ttk
from typing import Optional
from PIL import Image, ImageTk
from pathlib import Path
import os

GEOMETRY = "900x700"  # чуть увеличим для карточек

class GameView:
    def __init__(self, root: tk.Tk, controller):
        self.root = root
        self.controller = controller
        self.game_window = None
        self.current_mode = None
        self.current_player = None
        self.selected_attacker = None
        self.selected_defender = None

        try:
            current_dir = Path(__file__).parent
            fighter_dir = current_dir / "fighter"
            self.hamster_img1 = None
            self.hamster_img2 = None
            img1_path = fighter_dir / "hamster.jpg"
            if img1_path.exists():
                pil_img = Image.open(img1_path).resize((84, 84), Image.Resampling.LANCZOS)
                self.hamster_img1 = ImageTk.PhotoImage(pil_img)
            img2_path = fighter_dir / "hamster_2.jpg"
            if img2_path.exists():
                pil_img2 = Image.open(img2_path).resize((84, 84), Image.Resampling.LANCZOS)
                self.hamster_img2 = ImageTk.PhotoImage(pil_img2)
        except Exception as e:
            print(f"Ошибка загрузки изображений: {e}")

        self.create_main_menu()

    # ---------------------- ГЛАВНОЕ МЕНЮ (без изменений) ----------------------
    def create_main_menu(self):
        self.root.geometry(GEOMETRY)
        self.root.title("Battle of Teams")
        for widget in self.root.winfo_children():
            widget.destroy()

        title = tk.Label(self.root, text="Battle of Teams", font=("Arial", 32, "bold"))
        title.pack(pady=48)

        button_new_game = tk.Button(self.root, text="Start new game", font=("Consolas", 18),
                                    command=self.show_mode_selection)
        button_exit = tk.Button(self.root, text="Exit game", font=("Consolas", 18),
                                command=self.root.destroy)
        button_new_game.pack(pady=20)
        button_exit.pack(pady=20)

    def show_mode_selection(self):
        self.root.withdraw()
        mode_window = tk.Toplevel(self.root)
        mode_window.geometry(GEOMETRY)
        mode_window.title("Select Game Mode")
        mode_window.grab_set()

        def select_mode(mode: str):
            mode_window.destroy()
            self.current_mode = mode
            self.controller.start_new_game(mode)

        btn_pvp = tk.Button(mode_window, text="Player VS Player", command=lambda: select_mode('pvp'),
                            font=("Consolas", 18))
        btn_pve = tk.Button(mode_window, text="Player VS Environment (AI)", command=lambda: select_mode('pve'),
                            font=("Consolas", 18))
        btn_back = tk.Button(mode_window, text="Back to Main Menu",
                             command=lambda: self._close_mode_window(mode_window), font=("Consolas", 18))
        btn_pvp.pack(pady=20)
        btn_pve.pack(pady=20)
        btn_back.pack(pady=20)
        mode_window.protocol("WM_DELETE_WINDOW", lambda: self._close_mode_window(mode_window))

    def _close_mode_window(self, window):
        window.destroy()
        self.root.deiconify()

    # ---------------------- ОСНОВНОЙ ИГРОВОЙ ЭКРАН ----------------------
    def create_game_screen(self, team_agent, team_player, current_player: str):
        self.current_player = current_player
        if self.game_window and self.game_window.winfo_exists():
            self._update_team_display('agent', team_agent)
            self._update_team_display('player', team_player)
            return

        self.game_window = tk.Toplevel(self.root)
        self.game_window.geometry(GEOMETRY)
        self.game_window.title("Battle of Teams - Game")
        self.game_window.grab_set()
        self.game_window.protocol("WM_DELETE_WINDOW", self._return_to_main_menu)

        main_frame = ttk.Frame(self.game_window, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        cards_frame = ttk.Frame(main_frame)
        cards_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=10)

        left_frame = ttk.LabelFrame(cards_frame, text=team_agent.name, padding="10")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        right_frame = ttk.LabelFrame(cards_frame, text=team_player.name, padding="10")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.team_widgets = {
            'agent': {'frame': left_frame, 'buttons': []},
            'player': {'frame': right_frame, 'buttons': []}
        }

        self._draw_team_cards(left_frame, team_agent, 'agent', image=self.hamster_img1)
        self._draw_team_cards(right_frame, team_player, 'player', image=self.hamster_img2)

        bottom_frame = ttk.Frame(main_frame)
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)

        log_frame = ttk.LabelFrame(bottom_frame, text="Ход боя (лог)", padding="5")
        log_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        self.log_text = scrolledtext.ScrolledText(log_frame, height=10, width=80, state='disabled')
        self.log_text.pack(fill=tk.BOTH, expand=True)

        quit_btn = ttk.Button(bottom_frame, text="Quit to Main Menu", command=self._return_to_main_menu)
        quit_btn.pack(pady=5)

    def _draw_team_cards(self, parent_frame, team, team_side: str, image=None):
        for idx, fighter in enumerate(team.fighters):
            status = "Жив" if fighter.alive else "Мёртв"
            text = f"{fighter.name}\nСила: {fighter.strength}\n{status}"
            btn = tk.Button(parent_frame,
                            image=image,
                            compound="top",
                            text=text,
                            font=("Consolas", 12, "bold"),
                            width=150,
                            height=150,
                            relief=tk.RAISED,
                            bg="light green" if fighter.alive else "light gray",
                            command=lambda i=idx, side=team_side: self._on_fighter_click(side, i))
            btn.pack(side=tk.TOP, padx=10, pady=5, expand=False)
            self.team_widgets[team_side]['buttons'].append(btn)

    def _update_team_display(self, team_side: str, team):
        """Обновляет текст и цвет кнопок при изменении состояния бойцов."""
        buttons = self.team_widgets[team_side]['buttons']
        for idx, fighter in enumerate(team.fighters):
            btn = buttons[idx]
            if not btn.winfo_exists():
                continue
            status = "Жив" if fighter.alive else "Мёртв"
            new_text = f"{fighter.name}\nСила: {fighter.strength}\n{status}"
            btn.config(text=new_text,
                       bg="light green" if fighter.alive else "light gray",
                       state=tk.NORMAL if fighter.alive else tk.DISABLED)
            # Если боец мёртв, делаем кнопку неактивной и убираем подсветку
            if not fighter.alive:
                btn.config(relief=tk.SUNKEN)

    def _on_fighter_click(self, team_side: str, idx: int):
        # Режим PvE: игрок может ходить только когда current_player == 'player'
        if self.current_mode == 'pve':
            if self.current_player != 'player':
                return
            # Если атакующий ещё не выбран, проверяем, что клик по команде игрока
            if self.selected_attacker is None and team_side != 'player':
                self.log_message("Вы должны атаковать своим бойцом! Выберите атакующего из своей команды (справа).")
                return
            # Если атакующий уже выбран, то защитник должен быть из команды AI
            if self.selected_attacker is not None and team_side != 'agent':
                self.log_message("Выберите защитника из команды противника (слева).")
                return

        # Режим PvP: (оставляем без изменений, как было ранее)
        if self.current_mode == 'pvp':
            allowed_attacker_side = 'agent' if self.current_player == 'player1' else 'player'
            if self.selected_attacker is None and team_side != allowed_attacker_side:
                self.log_message("Сейчас не ваш ход! Выбирайте атакующего из своей команды.")
                return

        fighter = self._get_fighter_by_side(team_side, idx)
        if not fighter or not fighter.alive:
            return

        if self.selected_attacker is None:
            self._clear_selection_highlight()
            self.selected_attacker = (team_side, idx)
            self._highlight_button(team_side, idx, highlight=True)
            self.log_message(f"Выбран атакующий: {fighter.name}")
        else:
            attacker_side, attacker_idx = self.selected_attacker
            if team_side == attacker_side:
                self.log_message("❌ Нельзя атаковать своего бойца! Выберите защитника из команды противника.")
                return
            if not fighter.alive:
                self.log_message("❌ Защитник мёртв! Выберите живого.")
                return
            self.controller.on_player_action(attacker_idx, idx)
            self._clear_selection()

    def _is_player_turn(self) -> bool:
        """Определяет, может ли игрок сейчас кликать по карточкам."""
        if self.current_mode == 'pve':
            # В PvE ход игрока только когда current_player == 'player'
            # Но контроллер сам управляет, но для UI узнаем из состояния?
            # Проще довериться контроллеру: добавим метод в контроллер? Или храним в view.
            # Сделаем так: будем обновлять активность через отдельный метод _set_controls_active_state,
            # который вызывается при каждом обновлении экрана.
            # Поэтому здесь просто вернём True, если кнопки активны.
            # Более надёжно: проверять, разрешены ли клики, по наличию обработчика.
            # Для простоты положимся на то, что контроллер не вызовет on_player_action, если не его ход.
            # Но для UI лучше запретить клики. Поэтому добавим флаг.
            return self._player_can_click
        else:  # pvp
            # В PvP активность зависит от current_player
            # Аналогично: будем использовать флаг
            return self._player_can_click

    def _set_controls_active_state(self, current_player: str):
        """Включает/отключает возможность клика по карточкам в зависимости от текущего игрока."""
        if self.current_mode == 'pve':
            # В PvE игрок может кликать только когда ход 'player'
            self._player_can_click = (current_player == 'player')
        else:  # pvp
            # В PvP оба игрока могут кликать, но нужно различать, кто сейчас ходит.
            # Однако выбор атакующего и защитника одинаков для обоих, просто контроллер
            # будет знать, какая команда атакует. Поэтому разрешаем клики всегда,
            # но контроллер проверит соответствие команды текущему игроку.
            self._player_can_click = True

        # Также можно визуально показать, активны ли карточки (например, изменить курсор)
        # Для простоты оставим как есть.

    def _get_fighter_by_side(self, team_side: str, idx: int):
        if not self.controller.battle:
            return None
        if team_side == 'agent':
            team = self.controller.battle.team_agent
        else:
            team = self.controller.battle.team_player
        if team and 0 <= idx < len(team.fighters):
            return team.fighters[idx]
        return None

    def _highlight_button(self, team_side: str, idx: int, highlight: bool):
        btn = self.team_widgets[team_side]['buttons'][idx]
        if highlight:
            btn.config(bg="yellow")
        else:
            fighter = self._get_fighter_by_side(team_side, idx)
            btn.config(bg="light green" if fighter and fighter.alive else "light gray")

    def _clear_selection_highlight(self):
        for side in ('agent', 'player'):
            for idx, btn in enumerate(self.team_widgets[side]['buttons']):
                if not btn.winfo_exists():
                    continue
                fighter = self._get_fighter_by_side(side, idx)
                if fighter and fighter.alive:
                    btn.config(bg="light green")
                else:
                    btn.config(bg="light gray")

    def _clear_selection(self):
        self._clear_selection_highlight()
        self.selected_attacker = None
        self.selected_defender = None

    def update_game_screen(self, team_agent, team_player, current_player: str, winner: Optional[str] = None):
        if not self.game_window or not self.game_window.winfo_exists():
            return
        self.current_player = current_player
        self._update_team_display('agent', team_agent)
        self._update_team_display('player', team_player)
        self._clear_selection()
        if winner:
            self._show_winner(winner)

    def _show_winner(self, winner_name: str):
        for widget in self.game_window.winfo_children():
            widget.destroy()
        winner_label = tk.Label(self.game_window, text=f"ПОБЕДИТЕЛЬ: {winner_name}",
                                font=("Arial", 24, "bold"), fg="green")
        winner_label.pack(expand=True, pady=50)
        back_btn = tk.Button(self.game_window, text="В главное меню",
                             command=self._return_to_main_menu, font=("Consolas", 16))
        back_btn.pack(pady=20)

    def _return_to_main_menu(self):
        if self.game_window and self.game_window.winfo_exists():
            self.game_window.destroy()
        self.game_window = None
        self.root.deiconify()
        self.controller.return_to_main_menu()

    # ---------------------- ВСПОМОГАТЕЛЬНЫЕ МЕТОДЫ ----------------------
    def log_message(self, msg: str):
        if hasattr(self, 'log_text') and self.log_text.winfo_exists():
            self.log_text.config(state='normal')
            self.log_text.insert(tk.END, msg + "\n")
            self.log_text.see(tk.END)
            self.log_text.config(state='disabled')
        else:
            print(msg)

    def _skip_ai_turn(self):
        self.controller.on_skip_ai_turn()

    def show_error(self, message: str):
        tk.messagebox.showerror("Ошибка", message)

    def show_info(self, message: str):
        tk.messagebox.showinfo("Информация", message)

    # Методы для совместимости со старым контроллером (не используются, но оставим)
    def display_teams(self, team_agent, team_player):
        if not self.game_window or not self.game_window.winfo_exists():
            self.create_game_screen(team_agent, team_player, self.controller.current_player or 'agent')
        else:
            self.update_game_screen(team_agent, team_player, self.controller.current_player or 'agent', None)

    def _create_pve_controls(self, *args, **kwargs):
        pass

    def _create_pvp_controls(self, *args, **kwargs):
        pass

    def _rebuild_controls(self, *args, **kwargs):
        pass