import tkinter as tk
from game.view import GameView
from game.controller import GameController

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Battle of Teams")

    view = GameView(root, controller=None)

    controller = GameController(root, view)

    view.controller = controller

    root.mainloop()
