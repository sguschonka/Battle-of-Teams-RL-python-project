import tkinter as tk

GEOMETRY = "600x600"


class GameView:
    def __init__(self, root):
        self.root = root
        self.create_main_menu()

    def create_main_menu(self):
        self.root.geometry(GEOMETRY)

        title = tk.Label(
            text="Battle of Teams",  # in eng - Battle of Teams
            font=("Arial", 32, "bold"),
        )
        title.pack(pady=12)

        # create buttons for main menu
        button_new_game = tk.Button(
            self.root, command=self.on_game_button_click, text="Start new game"
        )
        button_exit = tk.Button(
            self.root, command=self.on_exit_button_click, text="Exit game"
        )

        buttons = (button_new_game, button_exit)

        for btn in buttons:
            btn.pack()

        # create settings menu like a hierarchical menu

    def on_game_button_click(self):
        self.root.withdraw()

        self.window = tk.Toplevel(self.root)
        btn_exit = tk.Button(
            self.window, text="Return to main menu", command=self.return_to_main_menu
        )
        btn_exit.pack()
        self.window.geometry(GEOMETRY)
        self.window.title("Active game window")

        self.window.protocol("WM_DELETE_WINDOW", self.return_to_main_menu)

    def on_exit_button_click(self):
        self.root.destroy()

    def return_to_main_menu(self):
        if self.window:
            self.window.destroy()

        self.root.deiconify()
