# Pixel Jumpers

A 2D platformer game with an integrated level editor, developed in Python using the Pygame library.

## Application Description

Pixel Jumpers is a classic platformer game where the player must navigate through levels filled with obstacles, collect fruits for points, and avoid dangerous traps. The game includes:

- Game Mode: Navigate levels with checkpoint system and multiple lives
- Level Editor: Create custom levels with an intuitive visual interface
- Progression System: Unlock 4 different characters using earned coins
- Main Menu: Graphical interface for navigation between different modes

## Programming Languages and Technologies

Programming Languages:
- Python 3.x

Libraries and Frameworks:
- Pygame 2.5.2+ for game development
  - 2D graphics rendering
  - Event handling for keyboard and mouse inputs
  - Pixel-perfect collision detection using masks

Other Technologies:
- JSON for level storage and loading
- Git for version control

## Running Instructions

Installing Dependencies:

```bash
pip install pygame
```

Running the Game:

Method 1: Through Main Menu (Recommended)

```bash
cd src
python3 menu.py
```

From the main menu you can choose:
- PLAY to start the game
- LEVEL EDITOR to open the level editor
- QUIT to exit the game

Method 2: Direct Launch

```bash
cd src
python3 main.py          # Launch game directly
python3 level_editor.py  # Launch editor directly
```

## Controls

Game Mode:
- Left/Right Arrow Keys: Move character
- Space: Jump (double jump available)
- ESC: Pause/Resume
- R: Restart level
- N: Next level
- P: Previous level
- Q: Return to menu (from pause)

Level Editor:
- Left Click: Place object
- Right Click: Remove object
- 1: Select Block (platform)
- 2: Select Fire trap
- 3: Select Checkpoint
- 4: Select End Trophy (level finish)
- 5: Select Chainsaw trap
- 6: Select Fruit collectible
- G: Toggle grid
- C: Toggle coordinates
- Space: Test level
- S: Save level
- L: Load level
- Q: Return to menu
- ESC: Clear all objects
- Arrow Keys: Move camera

## Main Features

Gameplay:
- Smooth platformer mechanics (gravity, jump, double jump)
- Checkpoint system for respawn
- Collectible fruits and coins for unlocking characters
- Dangerous enemies (static fire, oscillating chainsaws)
- Multiple lives system
- End trophy for level completion
- Functional pause system

Unlockable Characters:
- MaskDude: Free (default)
- NinjaFrog: 100 coins
- PinkMan: 400 coins
- VirtualGuy: 1000 coins

Level Editor Features:
- Visual interface with grid and coordinate displays
- 6 types of placeable objects
- Test mode for level verification
- Save/load levels in JSON format
- Scrollable camera for large levels
- Validation: level must have end trophy before saving

## Project Structure

Main Game Files (src directory):
- menu.py: Main menu interface
- main.py: Main game loop
- level_editor.py: Level editor interface

Game Entities (entities directory):
- player.py: Player logic and controls
- Base classes (base subdirectory):
  - animated_sprite.py
  - collidable_object.py
  - damageable_entity.py
- Environment objects (environment subdirectory):
  - block.py
  - checkpoint.py
  - end.py
- Damage-dealing entities (damageable subdirectory):
  - fire.py
  - chainsaw.py
- Collectible objects (collectibles subdirectory):
  - fruit.py

Supporting Systems:
- screen/screen.py: Screen rendering and overlays
- loader/sprite_loader.py: Sprite graphics loading

Assets and Levels:
- assets directory: Graphic and audio resources
  - Background graphics
  - MainCharacters sprites
  - Traps animations
  - Sound effects
- levels directory: Saved level files in JSON format
  - level_1.json
  - level_2.json
  - (more can be added using editor mode)

## Individual Contributions

Core Game Development:
- Developed complete platformer mini-game from scratch
- Implemented platformer mechanics: gravity, double jump, collision system
- Created entity hierarchy with inheritance (AnimatedSprite, CollidableObject, DamageableEntity)
- Built visual level editor with grid system and multiple object types

Game Systems:
- Developed checkpoint and respawn system
- Implemented damage system with cooldown and hit animations
- Created main menu and mode navigation system
- Built functional pause system

Bug Fixes and Features:
- Fixed multiple collision bugs and double damage issues
- Implemented 4 unlockable characters with coin progression system
- Designed and created 2 complete playable levels

## Challenges Encountered and Solutions

Double Damage in Same Frame:

Problem:
- Player received 2-3 damage instantly when touching an enemy
- Occurred even with 5 lives remaining

Cause:
- on_player_collision function was called twice in same frame
- Once in handle_vertical_collision
- Once in main game loop

Solution:
- Removed duplicate call from main loop
- Kept only checks in handle_vertical_collision and handle_horizontal_collision
- Properly managed cooldown system

Lateral Collisions Ignored:

Problem:
- Non-solid objects (fire, checkpoint, fruit) not detected when player moved into them from the side

Cause:
- handle_horizontal_collision had continue statement that skipped objects with is_solid set to False
- This happened before calling on_player_collision

Solution:
- Changed logic to call on_player_collision for all objects
- Only solid objects block movement

Pause Not Working Correctly:

Problem:
- Player could still move in background when game was paused

Cause:
- Movement logic (player.handle_move and player.moving_loop) not included in is_paused check

Solution:
- Moved entire game update logic inside is_paused conditional block
- Includes movement, sprite updates, and collisions

Pixel-Perfect Collision Detection:

Problem:
- Standard rectangle collisions were imprecise for complex sprites

Solution:
- Used pygame.mask.from_surface for creating collision masks
- Used pygame.sprite.collide_mask for accurate pixel-level collision detection

## System Requirements

- Python: 3.7 or higher
- Pygame: 2.5.2 or higher
- Operating System: Windows, Linux, or macOS
- Memory: Minimum 512 MB RAM
- Storage: Approximately 50 MB for game and assets
