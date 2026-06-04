

class GameView:
    def __init__(self, root):
        self.root = root
        self.create_ui()

    def create_ui(self):
        self.root.geometry("600x600")
