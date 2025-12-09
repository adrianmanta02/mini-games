# Shadow Switch - Firefly's Journey

A 2D platformer game featuring dual-form mechanics where you play as a firefly navigating through challenging levels.

---

## Game Description

Shadow Switch is a puzzle-platformer where players control a firefly that can switch between Light Form and Shadow Form. Each form has unique abilities and restrictions, requiring strategic thinking to overcome obstacles, collect light orbs, avoid enemies, and reach the finish portal.
---
### Core Mechanics:
- **Dual-Form System**: Switch between Light (fast, bright) and Shadow (slow, stealthy) forms
- **Light Management**: Your light level constantly drains - collect orbs to survive
- **Form Barriers**: Color-coded barriers that only allow specific forms to pass
- **Shadow Zones**: Areas that force you into Shadow form
- **Dynamic Enemies**: Three types of animated enemies (Bugs, Ants, Evil Fireflies)
- **Progressive Difficulty**: 4 levels with increasing complexity
---
## Features

**Gameplay Features:**
- Smooth character movement and physics
- Strategic form-switching mechanic
- Light drain system creating time pressure
- Moving platforms
- Hazards (spike traps)
- Animated enemies with patrol patterns

**Visual Features:**
- Gradient sky backgrounds
- Glowing effects for firefly and orbs

**Audio:**
- Jump sound effects
- Collection sounds
- Death sounds
- Victory sounds
---
## Technologies Used

- **Language**: Python 3.12
- **Framework**: Pygame 2.6.1
- **Development Environment**: PyCharm
- **Version Control**: Git
---

## Installation & Setup

### Prerequisites:
- Python 3.8 or higher
- pip (Python package manager)

### Steps:

1. **Navigate to project directory:**
```bash
   cd Python
```

2. **(Optional) Create virtual environment:**
```bash
   python -m venv .venv
```

3. **(Optional) Activate virtual environment:**
```bash
   # Windows
   .venv\Scripts\activate
   
   # Mac/Linux
   source .venv/bin/activate
```

## How to Run

**From the project directory:**
```bash
python main.py
```
---
## Controls

- `←` `→` -> Move left/right 
- `SPACE` -> Jump 
- `S` -> Switch between Light and Shadow form 
- `R` -> Restart level (when game over) 
- `N` -> Next level
--- 
## How to Play

### Objective:
Navigate through each level, collect light orbs to maintain your light level, and reach the purple portal at the end.

### Forms:

** Light Form (Yellow):**
- Faster movement speed
- Slower light drain
- Can pass through yellow barriers
- More visible to enemies

** Shadow Form (Purple):**
- Slower movement speed
- Faster light drain
- Can pass through purple barriers
- Less visible

### Strategy:
- Collect light orbs frequently to survive
- Switch forms strategically to pass barriers
- Shadow zones force you into Shadow form
- Plan your route to minimize light drain
- Enemies patrol in patterns - time your movements
## Project Structure
```
Python/
├── main.py              # Entry point & game loop
├── firefly.py           # Player class with dual-form mechanics
├── constants.py         # Game constants & colors
├── obstacle.py          # Platforms, barriers, hazards, shadow zones
├── enemies.py           # Enemy classes (Bug, Ant, Firefly_Enemy)
├── collectibles.py      # Light orbs and portal
├── level_manager.py     # Level definitions
└── sounds/              # Audio assets
    ├── jump-sound.wav
    ├── death-sound.wav
    ├── collect-sound.wav
    └── win-sound.wav
```
### Code Organization:
- **Modular design**: Each game entity has its own class and file
- **Separation of concerns**: Game logic, rendering, and data separated
- **~1850 lines** of code across 7 Python files
- **Clean code**: English comments, descriptive variable names

---

## Level Design

### Level 1: 
- Introduction to basic mechanics
- Simple platform layout
- Few enemies
- Focus on learning form-switching

### Level 2:
- More complex platforming
- Multiple shadow zones
- Strategic barrier placement
- Increased hazards

### Level 3:
- Introduction of moving platforms
- More enemies (Bugs, Ants, Evil Fireflies)
- Tighter timing requirements
- Complex navigation

### Level 4:
- Longest level
- All mechanics combined
- Maximum difficulty
- Multiple moving platforms
- Many enemies and hazards

---
## Individual Contribution

- Player character with dual-form mechanics
- Three enemy types with animated movement patterns
- Four complete levels with manual design
- Form barrier system (strategic gameplay element)
- Shadow zone mechanics
- Moving platforms with vertical movement
- Hazards (spike traps)
- Collectibles (light orbs, portal)
- Camera system with smooth scrolling
- UI system (health bar, form indicator, level counter)
- Sound effects integration
- Intro screen with animations
- Game over and victory screens
- Background decorations (sun, animated clouds)
---

## Difficulties Encountered & Solutions

### 1. Form Barrier Collision
**Problem:** Player could pass through form barriers regardless of current form.

**Solution:** 
- Saved player's old position before movement
- Implemented proper collision detection checking player form
- Restored old position when collision with wrong-form barrier detected

### 2. Firefly Rendering Transparency
**Problem:** Firefly appeared nearly invisible during gameplay due to complex alpha blending.

**Solution:**
- Simplified rendering from 20+ glow layers to 3 layers
- Made main body completely opaque
- Reduced darkness overlay intensity

### 3. Enemies Not Appearing
**Problem:** Enemy objects defined but not visible on screen.

**Solution:**
- Discovered inconsistent camera variable usage
- Changed enemy drawing to use correct camera variable
