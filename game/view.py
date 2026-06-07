import tkinter as tk

GEOMETRY = "600x600"


class GameView:
    def __init__(self, root):
        self.root = root
        self.game_window = None
        self.create_main_menu()

    def create_main_menu(self):
        self.root.geometry(GEOMETRY)

        title = tk.Label(
            self.root,
            text="Battle of Teams",  # in eng - Battle of Teams
            font=("Arial", 32, "bold"),
        )
        title.pack(pady=48)

        # create buttons for main menu
        button_new_game = tk.Button(
            self.root,
            command=self.on_game_button_click,
            text="Start new game",
            font=("Consolas", 18),
        )
        button_exit = tk.Button(
            self.root,
            command=self.on_exit_button_click,
            text="Exit game",
            font=("Consolas", 18),
        )

        buttons = (button_new_game, button_exit)

        for btn in buttons:
            btn.pack(pady=20)

        # create settings menu like a hierarchical menu

    def on_game_button_click(self):
        # prevent multiple game windows
        if self.game_window and self.game_window.winfo_exists():
            self.game_window.lift()  # bring to front
            return

        self.root.withdraw()

        self.game_window = tk.Toplevel(self.root)
        self.game_window.geometry(GEOMETRY)
        self.game_window.title("Select Game Mode")
        self.game_window.grab_set()

        btn_pvp = tk.Button(
            self.game_window,
            text="Player VS Player",
            command=self.on_pvp_btn_click,
            font=("Consolas", 18),
        )

        btn_pve = tk.Button(
            self.game_window,
            text="Player VS Environment",
            command=self.on_pve_btn_click,
            font=("Consolas", 18),
        )

        btn_exit = tk.Button(
            self.game_window,
            text="Return to main menu",
            command=self.return_to_main_menu,
            font=("Consolas", 18),
        )

        buttons = (btn_exit, btn_pve, btn_pvp)

        self.game_window.protocol("WM_DELETE_WINDOW", self.return_to_main_menu)

        for btn in buttons:
            btn.pack(pady=20)

    def on_exit_button_click(self):
        self.root.destroy()

    def on_pvp_btn_click(self):
        if self.game_window:
            self.game_window.destroy()

        self.root.deiconify()

    def on_pve_btn_click(self):
        if self.game_window:
            self.game_window.destroy()

        self.root.deiconify()

    def return_to_main_menu(self):
        if self.game_window and self.game_window.winfo_exists():
            self.game_window.destroy()

        self.game_window = None
        self.root.deiconify()
