"""
Arcade Game Launcher
A GUI application that displays 3 game icons and launches the selected game
"""

import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import sys
import subprocess
import threading

class ArcadeLauncher:
    def __init__(self, root):
        self.root = root
        self.root.title("Arcade Game Launcher")
        self.root.geometry("1000x750")
        self.root.configure(bg="#0a0e27")
        
        # Track animation states
        self.animation_active = {}
        self.current_offset = {}
        
        # Title Label with gradient-like effect using a frame
        title_frame = tk.Frame(root, bg="#0a0e27")
        title_frame.pack(expand=True, side=tk.TOP, pady=(40, 0))
        
        title_label = tk.Label(
            title_frame,
            text="ARCADE GAMES",
            font=("Arial", 48, "bold"),
            fg="#00ffff",
            bg="#0a0e27"
        )
        title_label.pack()
        
        # Subtitle with neon effect
        subtitle_label = tk.Label(
            title_frame,
            text="━━━━━━━━━━━━━━━━━━━",
            font=("Arial", 16),
            fg="#ff00ff",
            bg="#0a0e27"
        )
        subtitle_label.pack()
        
        # Frame to hold game buttons with padding
        games_frame = tk.Frame(root, bg="#0a0e27")
        games_frame.pack(expand=True, pady=20)
        
        # Game configurations with electric neon colors and display names
        games = [
            {"name": "Pixel Jumpers", "folder": "game1", "color": "#ff006e", "glow": "#ff1493", "emoji": "🎮"},
            {"name": "Ghost Waver", "folder": "game2", "color": "#00f5ff", "glow": "#00bfff", "emoji": "👻"},
            {"name": "Shadow Switch", "folder": "game3", "color": "#ffbe0b", "glow": "#ffd700", "emoji": "🌙"}
        ]
        
        # Create game buttons
        for i, game in enumerate(games):
            self.create_game_button(games_frame, game, i)
        
        # Instructions with neon styling
        instructions = tk.Label(
            root,
            text="Click any game to launch it",
            font=("Arial", 16, "bold"),
            fg="#00ffff",
            bg="#0a0e27"
        )
        instructions.pack(pady=15)
        
    def create_game_button(self, parent, game, index):
        """Create a clickable game card with animation and play button"""
        # Initialize animation state
        self.animation_active[game['folder']] = False
        self.current_offset[game['folder']] = 0
        
        # Main container frame that will move left/right
        container_frame = tk.Frame(parent, bg="#0a0e27")
        container_frame.grid(row=0, column=index, padx=15, pady=20)
        
        # Card frame with border
        card_frame = tk.Frame(
            container_frame,
            bg="#0a0e27",
            highlightthickness=2,
            highlightbackground=game['glow'],
            relief=tk.FLAT
        )
        card_frame.pack()
        
        # Game button
        game_button = tk.Button(
            card_frame,
            text=game['emoji'],
            font=("Arial", 56, "bold"),
            width=12,
            height=5,
            bg=game['color'],
            fg="#000000",
            activebackground=game['glow'],
            activeforeground="#000000",
            relief=tk.FLAT,
            bd=0,
            cursor="hand2",
            overrelief=tk.RAISED
        )
        game_button.pack(padx=3, pady=3)
        
        # Game name label
        name_label = tk.Label(
            card_frame,
            text=game['name'],
            font=("Arial", 20, "bold"),
            fg=game['color'],
            bg="#1a1f3a"
        )
        name_label.pack(fill=tk.X, padx=3, pady=(5, 0))
        
        # Play button
        play_button = tk.Button(
            card_frame,
            text="▶ PLAY",
            font=("Arial", 11, "bold"),
            fg="#000000",
            bg=game['glow'],
            activebackground=game['color'],
            activeforeground="#000000",
            relief=tk.FLAT,
            bd=0,
            cursor="hand2",
            padx=15,
            pady=8,
            command=lambda: self.launch_game(game['folder'], game['name'])
        )
        play_button.pack(padx=3, pady=(0, 5))
        
        # Bind hover events with animation
        game_button.bind("<Enter>", lambda e: self.on_hover_card(game_button, game['glow'], game['color'], game['folder'], card_frame, name_label, game['glow']))
        game_button.bind("<Leave>", lambda e: self.on_leave_card(game_button, game['color'], game['folder'], card_frame, name_label, game['glow']))
        
        card_frame.bind("<Enter>", lambda e: self.on_hover_card(game_button, game['glow'], game['color'], game['folder'], card_frame, name_label, game['glow']))
        card_frame.bind("<Leave>", lambda e: self.on_leave_card(game_button, game['color'], game['folder'], card_frame, name_label, game['glow']))
        
        play_button.bind("<Enter>", lambda e: self.on_hover_card(game_button, game['glow'], game['color'], game['folder'], card_frame, name_label, game['glow']))
        play_button.bind("<Leave>", lambda e: self.on_leave_card(game_button, game['color'], game['folder'], card_frame, name_label, game['glow']))
        
        name_label.bind("<Enter>", lambda e: self.on_hover_card(game_button, game['glow'], game['color'], game['folder'], card_frame, name_label, game['glow']))
        name_label.bind("<Leave>", lambda e: self.on_leave_card(game_button, game['color'], game['folder'], card_frame, name_label, game['glow']))
        
    def on_hover_card(self, button, glow_color, original_color, folder, card_frame, name_label, glow):
        """Effect when mouse hovers over card - triggers animation"""
        button.config(bg=glow_color, relief=tk.SUNKEN)
        card_frame.config(highlightthickness=3)
        name_label.config(fg=glow)
        
        # Start left-right animation
        if not self.animation_active[folder]:
            self.animation_active[folder] = True
            self.animate_card(card_frame, folder, 0, True)
        
    def on_leave_card(self, button, original_color, folder, card_frame, name_label, glow):
        """Effect when mouse leaves card"""
        button.config(bg=original_color, relief=tk.FLAT)
        card_frame.config(highlightthickness=2)
        name_label.config(fg=original_color)
        
        # Stop animation
        self.animation_active[folder] = False
        self.current_offset[folder] = 0
        card_frame.place(relx=0, x=0, rely=0, y=0)
    
    def animate_card(self, card_frame, folder, direction, is_right):
        """Animate card moving left and right"""
        if not self.animation_active[folder]:
            return
        
        # Move 10 pixels at a time
        max_offset = 15
        
        if is_right:
            direction += 3
            if direction >= max_offset:
                is_right = False
        else:
            direction -= 3
            if direction <= -max_offset:
                is_right = True
        
        self.current_offset[folder] = direction
        card_frame.place(relx=0, x=direction, rely=0, y=0)
        
        # Schedule next animation frame
        self.root.after(30, lambda: self.animate_card(card_frame, folder, direction, is_right))
        
    def launch_game(self, folder_name, game_name):
        """Launch the selected game by navigating to its folder and running main.py"""
        # Get the directory where engine.py is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Build path to game folder
        game_folder = os.path.join(script_dir, folder_name)
        
        # Check for main.py in different locations
        game_main = None
        game_cwd = None
        
        # Priority order: src/main.py, then main.py in root
        potential_paths = [
            (os.path.join(game_folder, "src", "main.py"), os.path.join(game_folder, "src")),
            (os.path.join(game_folder, "main.py"), game_folder)
        ]
        
        for main_path, cwd_path in potential_paths:
            if os.path.exists(main_path):
                game_main = main_path
                game_cwd = cwd_path
                break
        
        # Check if game exists
        if game_main is None:
            messagebox.showerror(
                "Game Not Found",
                f"Could not find main.py in {folder_name} folder!\n\nLooking for:\n- {os.path.join(folder_name, 'src', 'main.py')}\n- {os.path.join(folder_name, 'main.py')}"
            )
            return
        
        print(f"[v0] Launching {game_name} from {game_cwd}")
        
        try:
            # Launch the game in a new process
            # This allows the game to run independently
            subprocess.Popen(
                [sys.executable, game_main],
                cwd=game_cwd  # Set working directory to game folder
            )
            
            messagebox.showinfo(
                "Game Launched",
                f"{game_name} has been launched!\n\nThe game is running in a separate window."
            )
            
        except Exception as e:
            messagebox.showerror(
                "Launch Error",
                f"Failed to launch {game_name}\n\nError: {str(e)}"
            )
            print(f"[v0] Error launching game: {e}")


def main():
    """Main function to run the arcade launcher"""
    root = tk.Tk()
    app = ArcadeLauncher(root)
    root.mainloop()


if __name__ == "__main__":
    main()
