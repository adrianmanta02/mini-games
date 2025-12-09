"""
Game 3 - Color Memory Game
Remember and repeat the color sequence!
"""

import tkinter as tk
from tkinter import messagebox
import random
import time

class ColorMemoryGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Game 3 - Color Memory")
        self.root.geometry("400x500")
        self.root.configure(bg="#ffe66d")
        
        self.colors = ["red", "blue", "green", "yellow"]
        self.sequence = []
        self.player_sequence = []
        self.level = 1
        
        # Title
        title = tk.Label(
            root,
            text="🌈 COLOR MEMORY 🌈",
            font=("Arial", 20, "bold"),
            bg="#ffe66d",
            fg="#333333"
        )
        title.pack(pady=20)
        
        # Level display
        self.level_label = tk.Label(
            root,
            text=f"Level: {self.level}",
            font=("Arial", 16),
            bg="#ffe66d",
            fg="#333333"
        )
        self.level_label.pack(pady=10)
        
        # Color buttons frame
        buttons_frame = tk.Frame(root, bg="#ffe66d")
        buttons_frame.pack(pady=20)
        
        self.color_buttons = {}
        for i, color in enumerate(self.colors):
            btn = tk.Button(
                buttons_frame,
                text=color.upper(),
                font=("Arial", 14, "bold"),
                width=10,
                height=3,
                bg=color,
                fg="white",
                command=lambda c=color: self.player_click(c),
                cursor="hand2"
            )
            btn.grid(row=i//2, column=i%2, padx=10, pady=10)
            self.color_buttons[color] = btn
            
        # Start button
        self.start_button = tk.Button(
            root,
            text="START GAME",
            font=("Arial", 14, "bold"),
            bg="#333333",
            fg="white",
            width=15,
            command=self.start_game,
            cursor="hand2"
        )
        self.start_button.pack(pady=20)
        
    def start_game(self):
        """Start a new game"""
        self.sequence = []
        self.level = 1
        self.level_label.config(text=f"Level: {self.level}")
        self.next_level()
        
    def next_level(self):
        """Progress to next level"""
        self.player_sequence = []
        self.sequence.append(random.choice(self.colors))
        self.show_sequence()
        
    def show_sequence(self):
        """Show the color sequence to memorize"""
        self.disable_buttons()
        self.root.after(500, lambda: self._flash_sequence(0))
        
    def _flash_sequence(self, index):
        """Flash colors one by one"""
        if index < len(self.sequence):
            color = self.sequence[index]
            original_bg = self.color_buttons[color]['bg']
            
            # Flash white
            self.color_buttons[color].config(bg="white")
            self.root.after(300, lambda: self.color_buttons[color].config(bg=original_bg))
            self.root.after(600, lambda: self._flash_sequence(index + 1))
        else:
            self.root.after(600, self.enable_buttons)
            
    def player_click(self, color):
        """Handle player color selection"""
        self.player_sequence.append(color)
        
        if self.player_sequence[-1] != self.sequence[len(self.player_sequence) - 1]:
            messagebox.showinfo("Game Over", f"Wrong! You reached level {self.level}")
            self.start_game()
        elif len(self.player_sequence) == len(self.sequence):
            self.level += 1
            self.level_label.config(text=f"Level: {self.level}")
            messagebox.showinfo("Great!", f"Level {self.level - 1} complete!")
            self.next_level()
            
    def disable_buttons(self):
        """Disable color buttons during sequence display"""
        for btn in self.color_buttons.values():
            btn.config(state=tk.DISABLED)
            
    def enable_buttons(self):
        """Enable color buttons for player input"""
        for btn in self.color_buttons.values():
            btn.config(state=tk.NORMAL)


if __name__ == "__main__":
    root = tk.Tk()
    game = ColorMemoryGame(root)
    root.mainloop()
