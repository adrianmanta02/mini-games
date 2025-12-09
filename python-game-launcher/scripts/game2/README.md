# Ghost Waver

A 2D platformer game with action elements, developed in Python using the Pygame library. Navigate through water-based hazards, defeat ghost enemies, collect coins and magic potions, and progress through multiple challenging levels.

## Application Description

Ghost Waver is an engaging 2D platformer where players must navigate through tile-based levels filled with obstacles, water hazards, and ghost enemies. The game combines classic platformer mechanics with combat and progression systems. Key components include:

- **Game Mode:** Navigate levels with a multiple lives system, collect coins for unlocking characters, use magic potions to restore health, and defeat enemies to progress
- **Level Editor:** Create custom levels with an intuitive visual interface for tile placement, enemy positioning, and level design
- **Progression System:** Earn coins throughout levels to unlock different characters and enhance replayability
- **Combat & Hazards:** Throw grenades to defeat ghost enemies and navigate around water-based obstacles

## Programming Languages and Technologies

**Programming Languages:**

- Python 3.8+

**Libraries and Frameworks:**

- Pygame 2.5.2+ for game development
  - 2D graphics rendering
  - Event handling for keyboard and mouse inputs
  - Sprite collision detection
  - Audio playback

**Other Technologies:**

- Git for version control
- JSON for level storage and loading

## Game Mode Details

- **Multiple Lives System:** Players start with a set number of lives. Taking damage from enemies or hazards costs one life. Lose all lives and restart the level.
- **Coins & Character Progression:** Collect coins scattered throughout levels to unlock different playable characters, adding replay value and customization.
- **Magic Potions:** Health pickups scattered across levels. Collect potions to restore health and survive longer. Managing health is crucial to level completion.
- **Platforming Mechanics:** Jump, move left/right with precise controls. Tile-based physics ensures predictable movement and collision.
- **Enemy Combat:** Ghost enemies patrol levels. Use grenades to defeat them and clear safe paths. Strategic grenade use is key to survival.
- **Water Hazards:** Navigate around water obstacles that damage the player. Careful jumping and timing are required.

## Level Editor

Ghost Waver includes a built-in level editor allowing you to design custom levels:

- **Tile placement:** Place platforms, water hazards, and terrain
- **Enemy positioning:** Add and position ghost enemies
- **Player spawning:** Set the player's starting position
- **Item placement:** Place coins, magic potions, and grenades
- **Test mode:** Preview and test your level before saving
- **Save/Load:** Store levels in JSON format for later play

### Important Note on Level Editor Scaling

The level editor may display levels that aren't scaled properly on screen. This is addressed through the main game's scaling system—levels designed in the editor will display correctly when played in main.py.

## Main Features

**Gameplay:**

- Smooth platformer mechanics with gravity and jumping
- Tile-based collision detection
- Multiple challenging levels with progressive difficulty
- Parallax scrolling backgrounds for visual depth
- Particle effects for visual feedback

**Platforms & Obstacles:**

- Various tile types including solid platforms and water hazards
- Dynamic level layouts with increasing difficulty
- Environmental hazards that require precise timing

**Enemy Shooting System:**

- Ghost enemies
- Strategic grenade combat to defeat enemies
- Enemy patrol patterns and damage mechanics

**Health & Progression:**

- Multiple lives system
- Collectible coins for character unlocking
- Magic potions for health restoration
- Progressive level difficulty

**Level Editor Features:**

- Visual interface for intuitive level design
- Grid display and coordinate information
- Test mode for level verification
- Save/load levels in JSON format
- Player spawn point configuration
- Multiple hazard and enemy types

## Project Structure

```
game2/
├── src/
│   ├── main.py              # Game entry point
│   ├── level_editor.py      # Level editor interface
│   ├── player.py            # Player logic and controls
│   ├── enemies.py           # Ghost AI and behavior
│   ├── world.py             # Level and world management
│   ├── projectiles.py       # Grenades and projectiles
│   ├── button.py            # UI button components
│   ├── texts.py             # Text rendering utilities
│   ├── particles.py         # Particle effects
│   └── __pycache__/         # Python cache (auto-generated)
├── Assets/                  # Game graphics and sprites
│   ├── Ghost/               # Ghost enemy sprites
│   ├── Player/              # Player character sprites
│   └── Nature Platformer/   # Tileset graphics
├── Data/                    # Game data and documentation
├── Fonts/                   # Custom fonts
├── Levels/                  # Level data files (JSON format)
├── Sounds/                  # Audio files and effects
├── Tiles/                   # Tile graphics
└── README.md                # This file
```

## System Requirements

- **Python:** 3.8 or higher
- **Pygame:** 2.5.2 or higher
- **Operating System:** Windows, macOS, or Linux
- **Memory:** Minimum 512 MB RAM
- **Storage:** Approximately 50 MB for game and assets
- **Display:** Minimum 800x600 resolution recommended

## Installing Dependencies

```bash
cd scripts/game2
python -m venv venv
```

**On Windows:**

```bash
venv\Scripts\activate
```

**On macOS/Linux:**

```bash
source venv/bin/activate
```

Then install Pygame:

```bash
pip install pygame
```

## Running Instructions

**Method 1: Launch the Game**

```bash
cd scripts/game2/src
python main.py
```

**Method 2: Open the Level Editor**

```bash
cd scripts/game2/src
python level_editor.py
```

## Controls

**Game Mode:**

- **Left/Right Arrow Keys:** Move character left and right
- **Up Arrow Key:** Jump
- **G:** Throw grenade at enemies
- **ESC:** Exit game

**Level Editor:**

- **Left Click:** Place tile/object at cursor
- **Right Click:** Remove tile/object at cursor
- **Number Keys (1-6):** Select different tile/object types
- **Arrow Keys:** Move camera around the level
- **Space:** Test the level in-game
- **S:** Save your level
- **L:** Load a previously saved level
- **ESC:** Clear all objects / Exit editor

## Troubleshooting

- **Assets not loading:** Ensure you're running `main.py` and `level_editor.py` from the `src/` directory so relative paths work correctly.
- **Pygame not found:** Verify you've activated the virtual environment and run `pip install pygame`.
- **Level editor scaling:** Levels may appear unscaled in the editor. They will display correctly when played in `main.py`. This is handled through the game's scaling system.
- **Windows PowerShell:** Use `venv\Scripts\activate` to activate the virtual environment.
- **Player movement issues:** Scaling ensures proper collision and movement. If you encounter issues, ensure you're running from the correct directory.

## License

All rights reserved.
