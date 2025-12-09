"""
Game 1 - Simple Clicker Game
Click the button as many times as you can!
"""

import tkinter as tk

class ClickerGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Game 1 - Clicker")
        self.root.geometry("400x300")
        self.root.configure(bg="#ff6b6b")
        
        self.score = 0
        
        # Title
        title = tk.Label(
            root,
            text="🎮 CLICKER GAME 🎮",
            font=("Arial", 20, "bold"),
            bg="#ff6b6b",
            fg="white"
        )
        title.pack(pady=20)
        
        # Score display
        self.score_label = tk.Label(
            root,
            text=f"Score: {self.score}",
            font=("Arial", 24),
            bg="#ff6b6b",
            fg="white"
        )
        self.score_label.pack(pady=20)
        
        # Click button
        click_button = tk.Button(
            root,
            text="CLICK ME!",
            font=("Arial", 18, "bold"),
            width=15,
            height=3,
            bg="#ffffff",
            fg="#ff6b6b",
            command=self.increment_score,
            cursor="hand2"
        )
        click_button.pack(pady=20)
        
    def increment_score(self):
        """Increment score when button is clicked"""
        self.score += 1
        self.score_label.config(text=f"Score: {self.score}")


if __name__ == "__main__":
    root = tk.Tk()
    game = ClickerGame(root)
    root.mainloop()
