import tkinter as tk
from tkinter import scrolledtext
from tkinter import ttk
from typing import Optional, List, Tuple, Callable

GEOMETRY = "800x600"


class GameView:
    def __init__(self, root: tk.Tk, controller):
        """
        controller: объект, который имеет методы:
          - start_new_game(mode: str)   # mode = 'pvp' или 'pve'
          - on_player_action(attacker_idx: int, defender_idx: int)  # для PvE и PvP
          - return_to_main_menu()
        """
        self.root = root
        self.controller = controller
        self.game_window = None          # окно с игровым процессом
        self.current_mode = None

        self.create_main_menu()

    # ======================== ГЛАВНОЕ МЕНЮ ========================
    def create_main_menu(self):
        """Создаёт главное меню с кнопками."""
        self.root.geometry(GEOMETRY)
        self.root.title("Battle of Teams")

        # Очищаем предыдущее содержимое, если есть
        for widget in self.root.winfo_children():
            widget.destroy()

        title = tk.Label(
            self.root,
            text="Battle of Teams",
            font=("Arial", 32, "bold"),
        )
        title.pack(pady=48)

        button_new_game = tk.Button(
            self.root,
            text="Start new game",
            font=("Consolas", 18),
            command=self.show_mode_selection
        )
        button_exit = tk.Button(
            self.root,
            text="Exit game",
            font=("Consolas", 18),
            command=self.root.destroy
        )

        button_new_game.pack(pady=20)
        button_exit.pack(pady=20)

    def show_mode_selection(self):
        """Отображает окно выбора режима игры."""
        # Прячем главное меню
        self.root.withdraw()

        mode_window = tk.Toplevel(self.root)
        mode_window.geometry(GEOMETRY)
        mode_window.title("Select Game Mode")
        mode_window.grab_set()

        def select_mode(mode: str):
            mode_window.destroy()
            self.current_mode = mode
            self.controller.start_new_game(mode)

        btn_pvp = tk.Button(mode_window, text="Player VS Player", command=lambda: select_mode('pvp'), font=("Consolas", 18))
        btn_pve = tk.Button(mode_window, text="Player VS Environment (AI)", command=lambda: select_mode('pve'), font=("Consolas", 18))
        btn_back = tk.Button(mode_window, text="Back to Main Menu", command=lambda: self._close_mode_window(mode_window), font=("Consolas", 18))

        btn_pvp.pack(pady=20)
        btn_pve.pack(pady=20)
        btn_back.pack(pady=20)

        mode_window.protocol("WM_DELETE_WINDOW", lambda: self._close_mode_window(mode_window))

    def _close_mode_window(self, window):
        """Закрывает окно выбора режима и возвращает главное меню."""
        window.destroy()
        self.root.deiconify()

    # ======================== ИГРОВОЙ ЭКРАН ========================
    def create_game_screen(self, team_agent, team_player, current_player: str):
        """Создаёт игровой экран (один раз)."""
        if self.game_window and self.game_window.winfo_exists():
            # Окно уже есть — просто обновляем отображение
            self._update_team_display('agent', team_agent)
            self._update_team_display('player', team_player)
            self._rebuild_controls(team_agent, team_player, current_player)
            return

        # Создаём новое окно (только при первом вызове)
        self.game_window = tk.Toplevel(self.root)
        self.game_window.geometry(GEOMETRY)
        self.game_window.title("Battle of Teams - Game")
        self.game_window.grab_set()
        self.game_window.protocol("WM_DELETE_WINDOW", self._return_to_main_menu)

        main_frame = ttk.Frame(self.game_window, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Фреймы для команд
        left_frame = ttk.LabelFrame(main_frame, text=team_agent.name, padding="10")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        right_frame = ttk.LabelFrame(main_frame, text=team_player.name, padding="10")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.team_widgets = {
            'agent': {'frame': left_frame, 'labels': []},
            'player': {'frame': right_frame, 'labels': []}
        }
        self._draw_team(left_frame, team_agent, 'agent')
        self._draw_team(right_frame, team_player, 'player')

        # Лог
        log_frame = ttk.LabelFrame(main_frame, text="Ход боя (лог)", padding="5")
        log_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)
        self.log_text = scrolledtext.ScrolledText(log_frame, height=8, width=80, state='disabled')
        self.log_text.pack(fill=tk.BOTH, expand=True)

        # Панель действий (будем переиспользовать)
        self.action_frame = ttk.Frame(main_frame, padding="10")
        self.action_frame.pack(side=tk.BOTTOM, fill=tk.X)

        # Кнопка выхода
        quit_btn = ttk.Button(main_frame, text="Quit to Main Menu", command=self._return_to_main_menu)
        quit_btn.pack(side=tk.BOTTOM, pady=10)

        # Первоначальная отрисовка панели управления
        self._rebuild_controls(team_agent, team_player, current_player)

    def _rebuild_controls(self, team_agent, team_player, current_player):
        """Перестраивает панель управления в зависимости от режима и текущего игрока."""
        # Очищаем старые виджеты
        for widget in self.action_frame.winfo_children():
            widget.destroy()

        if self.current_mode == 'pve':
            self._create_pve_controls(self.action_frame, team_agent, team_player, current_player)
        else:  # pvp
            self._create_pvp_controls(self.action_frame, team_agent, team_player, current_player)

    def update_game_screen(self, team_agent, team_player, current_player: str, winner: Optional[str] = None):
        """Обновляет экран после хода (без пересоздания окна)."""
        if not self.game_window or not self.game_window.winfo_exists():
            return

        self._update_team_display('agent', team_agent)
        self._update_team_display('player', team_player)

        if winner:
            self._show_winner(winner)
        else:
            self._rebuild_controls(team_agent, team_player, current_player)

    def log_message(self, msg: str):
        """Добавляет сообщение в лог-поле."""
        if hasattr(self, 'log_text') and self.log_text.winfo_exists():
            self.log_text.config(state='normal')
            self.log_text.insert(tk.END, msg + "\n")
            self.log_text.see(tk.END)
            self.log_text.config(state='disabled')
        else:
            print(msg)  # fallback на случай, если лог ещё не создан

    def _draw_team(self, parent_frame, team, team_side: str):
        """Отрисовывает список бойцов команды."""
        for idx, fighter in enumerate(team.fighters):
            status = "Жив" if fighter.alive else "Мёртв"
            text = f"{fighter.name}\nСила: {fighter.strength}\n{status}"
            label = tk.Label(parent_frame, text=text, font=("Consolas", 12), relief=tk.RIDGE, padx=10, pady=5)
            label.pack(fill=tk.X, pady=2)
            # Сохраняем ссылку для обновления
            self.team_widgets[team_side]['labels'].append(label)

    def _create_pve_controls(self, parent, agent_team, player_team, current_player):
        """Создаёт элементы управления для режима PvE (игрок против AI)."""
        if current_player == 'agent':
            # Ход AI, контроллер сам вызовет метод AI и обновит экран
            info = tk.Label(parent, text="AI делает ход...", font=("Arial", 12, "bold"))
            info.pack()
            # Для удобства можно добавить кнопку "Пропустить" для отладки
            skip_btn = tk.Button(parent, text="Skip AI turn (debug)", command=self._skip_ai_turn)
            skip_btn.pack()
        else:
            info = tk.Label(parent, text="Ваш ход! Выберите атакующего и защитника", font=("Arial", 12, "bold"))
            info.pack()

            # ---- Атакующий (из команды игрока) ----
            attacker_indices = []
            attacker_options = []
            for i, f in enumerate(player_team.fighters):
                if f.alive:
                    attacker_indices.append(i)
                    attacker_options.append(f"{i}: {f.name} (сила {f.strength})")
            attacker_var = tk.IntVar(value=-1)
            attacker_menu = ttk.Combobox(parent, textvariable=attacker_var, state="readonly", width=30)
            attacker_menu['values'] = attacker_options
            attacker_menu.pack(pady=5)
            # Не нужно привязывать bind, просто при атаке берём current()

            # ---- Защитник (из команды AI) ----
            defender_indices = []
            defender_options = []
            for i, f in enumerate(agent_team.fighters):
                if f.alive:
                    defender_indices.append(i)
                    defender_options.append(f"{i}: {f.name} (сила {f.strength})")
            defender_var = tk.IntVar(value=-1)
            defender_menu = ttk.Combobox(parent, textvariable=defender_var, state="readonly", width=30)
            defender_menu['values'] = defender_options
            defender_menu.pack(pady=5)

            def on_attack():
                att_pos = attacker_menu.current()
                defe_pos = defender_menu.current()
                if att_pos == -1 or defe_pos == -1:
                    info.config(text="Выберите и атакующего, и защитника!", fg="red")
                    return
                att = attacker_indices[att_pos]
                defe = defender_indices[defe_pos]
                self.controller.on_player_action(att, defe)

            attack_btn = tk.Button(parent, text="Атаковать!", command=on_attack, font=("Consolas", 14))
            attack_btn.pack(pady=10)

    def _create_pvp_controls(self, parent, team1, team2, current_player):
        """Элементы управления для PvP (чередование ходов)."""
        info = tk.Label(parent, text=f"Ход {current_player.upper()}. Выберите атакующего и защитника", font=("Arial", 12, "bold"))
        info.pack()

        # Определяем, какая команда атакует, какая защищается
        if current_player == 'player1':
            attacking_team = team1
            defending_team = team2
        else:
            attacking_team = team2
            defending_team = team1

        # Выбор атакующего
        attacker_var = tk.IntVar(value=-1)
        attacker_menu = ttk.Combobox(parent, textvariable=attacker_var, state="readonly", width=30)
        attacker_options = [f"{i}: {f.name} (сила {f.strength})" for i, f in enumerate(attacking_team.fighters) if f.alive]
        if not attacker_options:
            attacker_options = ["Нет живых бойцов"]
        attacker_menu['values'] = attacker_options
        attacker_menu.pack(pady=5)
        attacker_menu.bind("<<ComboboxSelected>>", lambda e: attacker_var.set(attacker_menu.current()))

        # Выбор защитника
        defender_var = tk.IntVar(value=-1)
        defender_menu = ttk.Combobox(parent, textvariable=defender_var, state="readonly", width=30)
        defender_options = [f"{i}: {f.name} (сила {f.strength})" for i, f in enumerate(defending_team.fighters) if f.alive]
        if not defender_options:
            defender_options = ["Нет живых бойцов"]
        defender_menu['values'] = defender_options
        defender_menu.pack(pady=5)
        defender_menu.bind("<<ComboboxSelected>>", lambda e: defender_var.set(defender_menu.current()))

        def on_attack():
            att = attacker_var.get()
            defe = defender_var.get()
            if att == -1 or defe == -1:
                info.config(text="Выберите и атакующего, и защитника!", fg="red")
                return
            # Передаём действие в контроллер
            self.controller.on_player_action(att, defe)

        attack_btn = tk.Button(parent, text="Атаковать!", command=on_attack, font=("Consolas", 14))
        attack_btn.pack(pady=10)

    def _update_team_display(self, team_side: str, team):
        """Обновляет тексты меток для указанной команды."""
        labels = self.team_widgets[team_side]['labels']
        for idx, fighter in enumerate(team.fighters):
            status = "Жив" if fighter.alive else "Мёртв"
            new_text = f"{fighter.name}\nСила: {fighter.strength}\n{status}"
            labels[idx].config(text=new_text)

    def _show_winner(self, winner_name: str):
        """Отображает окно победителя и кнопку возврата."""
        for widget in self.game_window.winfo_children():
            widget.destroy()
        winner_label = tk.Label(self.game_window, text=f"ПОБЕДИТЕЛЬ: {winner_name}", font=("Arial", 24, "bold"), fg="green")
        winner_label.pack(expand=True, pady=50)
        back_btn = tk.Button(self.game_window, text="В главное меню", command=self._return_to_main_menu, font=("Consolas", 16))
        back_btn.pack(pady=20)

    def _return_to_main_menu(self):
        """Закрывает игровое окно и возвращает главное меню."""
        if self.game_window and self.game_window.winfo_exists():
            self.game_window.destroy()
        self.game_window = None
        self.root.deiconify()
        self.controller.return_to_main_menu()

    def _on_game_window_close(self):
        """Обработчик закрытия игрового окна (крестик)."""
        self._return_to_main_menu()

    def _skip_ai_turn(self):
        """Вспомогательная функция для отладки: принудительно завершает ход AI."""
        # Просто просим контроллер сделать ход AI (обычно он сам вызывается при current_player == 'agent')
        self.controller.on_skip_ai_turn()   # можно добавить этот метод в контроллер

    # ======================== ДИАЛОГИ И СООБЩЕНИЯ ========================
    def show_error(self, message: str):
        tk.messagebox.showerror("Ошибка", message)

    def show_info(self, message: str):
        tk.messagebox.showinfo("Информация", message)

    def display_teams(self, team_agent, team_player):
        """Метод для обратной совместимости со старым контроллером."""
        if not self.game_window or not self.game_window.winfo_exists():
            self.create_game_screen(team_agent, team_player, self.current_player or 'agent')
        else:
            self.update_game_screen(team_agent, team_player, self.current_player or 'agent', None)