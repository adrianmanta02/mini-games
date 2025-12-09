# Game Launcher Arcade

A comprehensive arcade platform featuring three unique 2D games developed collaboratively by three students. The project showcases modern game development practices, including physics systems, level editing, AI integration, and collaborative development workflows using Git branching and merging.

## Overview

Game Launcher Arcade brings together three distinctive gaming experiences into one unified platform:

- **Pixel Jumpers** - A physics-driven platformer with double-jump mechanics and progression systems
- **Ghost Waver** - An action-oriented platformer featuring combat against ghost enemies with grenade mechanics
- **Shadow Switch** - A unique puzzle-platformer where environmental manipulation through state-switching is key to success

Each game is fully playable standalone or through the arcade launcher, offering diverse gameplay experiences suitable for different player preferences.

---

## System Requirements

- **Python:** 3.8 or higher
- **Operating System:** Windows, macOS, or Linux
- **Memory:** Minimum 512 MB RAM (1 GB recommended)
- **Storage:** Approximately 150 MB for all games and assets
- **Display:** Minimum 800x600 resolution recommended

---

## Installation & Setup

The arcade launcher handles all game management and selection. Simply follow these steps to get started:

### Quick Setup

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate        # On macOS/Linux
# or
venv\Scripts\activate           # On Windows

# Install dependencies (Pygame for graphics, Pillow for images)
pip install pillow pygame

# Launch the arcade
python engine.py
```

The engine will display the arcade interface where you can select and play any of the three games. All game management, selection, and launching is handled automatically by the arcade launcher.

---

## About the Engine

The `engine.py` file serves as the central hub of the arcade platform. It is responsible for:

- **Game Selection Interface:** Displays a user-friendly menu where players can browse and select which game to play
- **Game Management:** Handles the loading and execution of each game (Pixel Jumpers, Ghost Waver, Shadow Switch)
- **Resource Coordination:** Manages assets and resources across all three games
- **Player Experience:** Provides seamless transitions between the arcade menu and individual games
- **Unified Platform:** Creates a cohesive arcade experience while allowing each game to maintain its independent functionality

Once you run `python engine.py`, simply select your desired game from the arcade interface and the engine will handle launching the appropriate game. This modular approach allows new games to be easily added to the arcade in the future.

---

## Games Overview

### 1. Pixel Jumpers

A physics-driven 2D platformer featuring advanced movement mechanics and progression systems.

**Key Features:**

- Double-jump mechanics for enhanced platforming control
- Physics-based character movement and gravity system
- Multi-life health system with lives tracking
- Scrolling level design with procedural hazards
- Coin collection system for character progression
- Full Level Editor for creating custom content
- Character unlock system through coin collection

**Technologies:** Python, Pygame

---

### 2. Ghost Waver

An action-oriented 2D platformer emphasizing combat against supernatural enemies.

**Key Features:**

- Combat-focused gameplay with grenade projectiles
- Ghost enemy AI with patrol patterns and targeting
- Water hazard navigation and environmental obstacles
- Multiple lives system with lives management
- Coin collection for character unlocking
- Strategic grenade combat mechanics
- Progressive level difficulty
- Built-in Level Editor for custom level design
- Particle effects and visual feedback systems

**Technologies:** Python, Pygame

**Special Note:** Includes a comprehensive level editor with visual interface for intuitive level design.

---

### 3. Shadow Switch

A unique puzzle-platformer emphasizing environmental manipulation through state-switching mechanics.

**Key Features:**

- Core state-switching mechanic allowing character form changes
- Environmental attribute manipulation based on character state
- State-sensitive barriers and obstacles
- Puzzle-oriented level progression
- Strategic use of state changes to bypass challenges
- Environmental puzzle design
- Progressive puzzle complexity

**Technologies:** Python, Pygame

---

## Project Structure

```
python-game-launcher/
├── README.md                    # This file
├── package.json                 # Project metadata
└── scripts/
    ├── engine.py               # Main arcade launcher and game controller
    ├── game1/                  # Pixel Jumpers
    ├── game2/                  # Ghost Waver
    └── game3/                  # Shadow Switch
```

---

## System Requirements

- **Python:** 3.8 or higher
- **Operating System:** Windows, macOS, or Linux
- **Memory:** Minimum 512 MB RAM (1 GB recommended)
- **Storage:** Approximately 150 MB for all games and assets
- **Display:** Minimum 800x600 resolution recommended
- **Dependencies:** Pygame 2.5.2+, Pillow (for image processing)

---

## Installation & Setup

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd python-game-launcher
```

### Step 2: Create Virtual Environment

```bash
python -m venv venv
```

### Step 3: Activate Virtual Environment

**On Windows:**

```bash
venv\Scripts\activate
```

**On macOS/Linux:**

```bash
source venv/bin/activate
```

### Step 4: Install Dependencies

```bash
pip install pillow pygame
```

---

## Running Instructions

### Launch the Arcade Launcher

To run the main arcade interface with game selection:

```bash
python engine.py
```

---

## Development Workflow

This project was developed using a collaborative branching strategy:

1. **Initial Setup:** Created the main repository and established the project structure
2. **Feature Development:** Each team member worked on their assigned game (Pixel Jumpers, Ghost Waver, Shadow Switch) in separate feature branches
3. **Parallel Development:**
   - **Manta Adrian Gabriel:** Pixel Jumpers development and arcade integration
   - **Mihaela Ciuranu:** Ghost Waver development with level editor and arcade interface
   - **Ana Maria Cocoru:** Shadow Switch development with state-switching mechanics
4. **Integration & Merging:** All feature branches were merged into the main branch, combining all three games into the unified arcade launcher
5. **Documentation:** Comprehensive READMEs were created for each game and the main project

**Repository:** https://github.com/adrianmanta02/mini-games

---

## Technical Implementation

### Game Engine Architecture

- **Main Launcher:** `engine.py` serves as the central arcade controller, managing game selection and execution
- **Modular Design:** Each game is independently executable while maintaining integration with the launcher
- **Resource Management:** Centralized asset loading and management across all games

### Game Development Framework

- **Pygame Integration:** All games utilize Pygame 2.5.2+ for graphics rendering, event handling, and collision detection
- **Physics System:** Gravity-based physics in Pixel Jumpers for realistic platforming mechanics
- **AI Implementation:** Ghost Waver features ghost enemies with patrol and targeting AI
- **Level System:** JSON-based level storage allowing both pre-designed and user-created content

### Advanced Features Implemented

- **Level Editors:** Built-in visual editors for custom level creation (Ghost Waver)
- **Particle Effects:** Visual feedback systems for gameplay events
- **Audio Integration:** Sound effects and background music support
- **Character Progression:** Coin collection systems unlocking different playable characters
- **Health & Lives Systems:** Multiple life tracking and health management across all games

---

## Features & Technologies

### Programming Language

- **Python 3.8+** - Modern Python with object-oriented design patterns

### Libraries & Frameworks

- **Pygame 2.5.2+** - Game development framework providing:
  - 2D graphics rendering and sprite management
  - Event handling for keyboard and mouse inputs
  - Collision detection systems
  - Audio playback capabilities
- **Pillow** - Image processing and asset manipulation

### Other Technologies

- **Git** - Version control and collaborative development
- **JSON** - Level data storage and game configuration
- **Tkinter** - UI framework components (if used)

---

## Key Accomplishments

✅ **Collaborative Development:** Successfully merged three independently developed games into a unified arcade platform

✅ **Feature Diversity:** Three games with distinctly different mechanics and gameplay styles:

- Physics-driven platforming (Pixel Jumpers)
- Action-focused combat (Ghost Waver)
- Puzzle-oriented state-switching (Shadow Switch)

✅ **User Content Creation:** Level editors enabling players to create and share custom content

✅ **Code Quality:** ~2,550 lines of code total (~850 per team member) following OOP principles

✅ **Documentation:** Comprehensive README files for main project and individual games

✅ **Version Control:** Proper Git workflow with feature branches and merge integration

---

## Troubleshooting

### Common Issues & Solutions

**Issue:** Assets or resources not loading

- **Solution:** Ensure you're running games from their respective directories (`game1/`, `game2/src/`, `game3/`) so relative paths resolve correctly
- **Solution:** Verify all asset folders are present in the game directories

**Issue:** Pygame not found or import errors

- **Solution:** Verify virtual environment is activated
- **Solution:** Run `pip install pygame pillow` to install dependencies
- **Solution:** Check Python version is 3.8 or higher with `python --version`

**Issue:** Games run but no graphics display

- **Solution:** Check display resolution is at least 800x600
- **Solution:** Verify graphics drivers are up to date
- **Solution:** Try running from a terminal to see error messages

**Issue:** Virtual environment activation fails (Windows PowerShell)

- **Solution:** Use `venv\Scripts\activate.ps1` instead of `venv\Scripts\activate`
- **Solution:** If execution policy blocks scripts, run: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

**Issue:** Level editor display appears unscaled

- **Solution:** This is expected behavior in the editor; levels display correctly when played in the main game
- **Solution:** Use the test mode within the level editor for accurate preview

---

## Future Enhancements

Potential areas for future development:

- **Network Multiplayer:** Online competitive modes for all games
- **Mobile Ports:** Adaptation to iOS/Android platforms
- **Leaderboard System:** Global and local high score tracking
- **Additional Games:** Expanding the arcade with more game titles
- **Audio System:** Enhanced soundtrack and sound effect management
- **Graphics Enhancement:** Higher resolution assets and visual improvements
- **Analytics:** Player behavior tracking and game statistics
- **Accessibility:** Colorblind modes, difficulty adjustments, control remapping

---

## Difficulties & Solutions

### Challenge 1: Integrating Three Separate Games

- **Problem:** Merging three independently developed games with different structures and dependencies
- **Solution:** Established a centralized launcher (`engine.py`) that manages game selection and execution, allowing each game to maintain its own structure while integrating cleanly into the arcade platform

### Challenge 2: Asset Management

- **Problem:** Managing relative paths and asset loading across multiple game directories
- **Solution:** Ensured each game runs from its designated directory with clear path structure documentation in each game's README

### Challenge 3: Physics Implementation (Pixel Jumpers)

- **Problem:** Implementing realistic double-jump mechanics and gravity physics
- **Solution:** Developed a robust physics system that accurately tracks velocity, acceleration, and collision states

### Challenge 4: Enemy AI (Ghost Waver)

- **Problem:** Creating believable ghost enemy behavior with patrol and targeting mechanics
- **Solution:** Implemented state-based AI with pattern recognition and distance-based targeting logic

### Challenge 5: State-Switching Mechanics (Shadow Switch)

- **Problem:** Designing a flexible state system for character form changes and environmental interaction
- **Solution:** Created a modular state machine allowing seamless transitions between character forms with associated attribute changes

---

## Team Members & Contributions

This project was developed by three students working on different branches and features, which were later merged together:

### Manta Adrian Gabriel

- **Responsibilities:** Pixel Jumpers Development & Repository Setup & Documentation
- **Contributions:**
  - Developed "Pixel Jumpers" - a physics-driven platformer
  - Set up the main repository structure and arcade launcher
  - Implemented the engine and game integration system
  - Established development workflow and branching strategy
- **Lines of Code:** ~850

### Mihaela Ciuranu

- **Responsibilities:** Ghost Waver Development, Arcade Interface, Project README & Documentation
- **Contributions:**
  - Developed "Ghost Waver" - an action-oriented platformer with combat mechanics
  - Created the arcade interface and game selection system
  - Designed and implemented comprehensive project README and game documentation
  - Integrated UI/UX for the arcade launcher
- **Lines of Code:** ~850

### Ana Maria Cocoru

- **Responsibilities:** Shadow Switch Development & Documentation
- **Contributions:**
  - Developed "Shadow Switch" - a unique puzzle-platformer
  - Implemented the state-switching mechanic system
  - Created environmental manipulation puzzles
- **Lines of Code:** ~850

---

## Team Notes

**Development Approach:**

- Each team member worked on their assigned game independently in feature branches
- Regular merges and integration testing ensured compatibility
- Code reviews and collaborative problem-solving addressed integration challenges
- Approximately 850 lines of code per team member, maintaining quality and consistency

**Version Control:**

- Feature branching strategy maintained code isolation during development
- Periodic merges integrated new features into the main arcade
- Clean commit history enables easy tracking of contributions

**Communication:**

- Remote collaboration required clear documentation and code standards
- README files serve as primary documentation for each component
- Code comments and structure facilitate knowledge sharing

---

## License

All rights reserved. © 2024 Manta Adrian Gabriel, Mihaela Ciuranu, Ana Maria Cocoru

---

## Repository

**GitHub Repository:** https://github.com/adrianmanta02/mini-games

Feel free to explore the code, make modifications, and contribute improvements! For detailed information about individual games, refer to their respective README files in the `game2/` directory.

---

## How to Contribute

If you'd like to contribute to this project:

1. Fork the repository
2. Create a feature branch for your changes
3. Commit your work with clear messages
4. Push to your fork
5. Submit a pull request with a detailed description

For detailed implementation details, see the README files in individual game directories.
