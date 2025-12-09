#!/usr/bin/env python3
"""
Game runner script - runs main.py from the src directory
Sets working directory to game root for proper asset loading
"""
import os
import sys

# Get the directory of this script (game root)
game_root = os.path.dirname(os.path.abspath(__file__))

# Set working directory to game root (for asset loading)
os.chdir(game_root)

# Add src to path
sys.path.insert(0, os.path.join(game_root, 'src'))

# Import and run main
from src.main import *
