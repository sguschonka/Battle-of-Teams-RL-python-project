import tkinter as tk
from game.view import GameView

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Battle of Teams")

    view = GameView(root)

    root.mainloop()
