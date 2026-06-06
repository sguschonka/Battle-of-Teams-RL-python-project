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

        # create buttons for main menu, use lamda-functions for comfort
        button = tk.Button(
            self.root, command=self.on_game_button_click, text="Start new game"
        )
        button.pack()

        # create settings menu like a hierarchical menu

    def on_game_button_click(self):
        self.root.destroy()
        self.window = tk.Tk()
        self.window.geometry(GEOMETRY)
        self.window.title("Active game window")
