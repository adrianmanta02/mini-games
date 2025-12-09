"""
Game 2 - Number Guessing Game
Guess the random number between 1 and 100!
"""

import tkinter as tk
from tkinter import messagebox
import random

class GuessingGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Game 2 - Number Guesser")
        self.root.geometry("400x350")
        self.root.configure(bg="#4ecdc4")
        
        self.target_number = random.randint(1, 100)
        self.attempts = 0
        
        # Title
        title = tk.Label(
            root,
            text="🎲 NUMBER GUESSER 🎲",
            font=("Arial", 20, "bold"),
            bg="#4ecdc4",
            fg="white"
        )
        title.pack(pady=20)
        
        # Instructions
        instructions = tk.Label(
            root,
            text="Guess a number between 1 and 100",
            font=("Arial", 12),
            bg="#4ecdc4",
            fg="white"
        )
        instructions.pack(pady=10)
        
        # Entry for guess
        self.entry = tk.Entry(
            root,
            font=("Arial", 18),
            width=10,
            justify="center"
        )
        self.entry.pack(pady=20)
        
        # Submit button
        submit_button = tk.Button(
            root,
            text="GUESS",
            font=("Arial", 14, "bold"),
            bg="white",
            fg="#4ecdc4",
            width=12,
            command=self.check_guess,
            cursor="hand2"
        )
        submit_button.pack(pady=10)
        
        # Result label
        self.result_label = tk.Label(
            root,
            text="",
            font=("Arial", 14),
            bg="#4ecdc4",
            fg="white"
        )
        self.result_label.pack(pady=20)
        
    def check_guess(self):
        """Check if the guess is correct"""
        try:
            guess = int(self.entry.get())
            self.attempts += 1
            
            if guess < self.target_number:
                self.result_label.config(text=f"Too low! Try again.\nAttempts: {self.attempts}")
            elif guess > self.target_number:
                self.result_label.config(text=f"Too high! Try again.\nAttempts: {self.attempts}")
            else:
                messagebox.showinfo(
                    "Winner!",
                    f"🎉 Correct! You guessed it in {self.attempts} attempts!"
                )
                self.reset_game()
                
            self.entry.delete(0, tk.END)
            
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number!")
            
    def reset_game(self):
        """Reset the game with a new number"""
        self.target_number = random.randint(1, 100)
        self.attempts = 0
        self.result_label.config(text="")


if __name__ == "__main__":
    root = tk.Tk()
    game = GuessingGame(root)
    root.mainloop()
