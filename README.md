# TUI Snake
<img width="1209" height="640" alt="image" src="https://github.com/user-attachments/assets/d89bc073-812d-4652-be56-e56bf2b76d9b" />
A simple Snake game for the terminal, written in Python using `curses`.

> **Note:** Colors may look different depending on your terminal's color scheme. The screenshots use **Catppuccin Mocha**.

## Features

* WASD and arrow-key movement
* 10 apples on the board
* Score counter
* Increasing game speed
* Pause with `ESC`
* Restart after game over
* Colored terminal interface

## Requirements

* Python 3
* `windows-curses` on Windows

## Installation

### 1. Install Python

Download and install Python 3 from [python.org](https://www.python.org/downloads/).

During installation, make sure **"Add Python to PATH"** is enabled.

### 2. Install `windows-curses`

Open PowerShell and run:

```powershell
py -m pip install windows-curses
```

### 3. Download the repository

Clone the repository with Git:

```powershell
git clone https://github.com/raider-500/TUI-Snake
```

Then enter the project folder:

```powershell
cd YOUR-REPOSITORY
```

Alternatively, download the repository as a ZIP from GitHub and extract it.

## Running

Open PowerShell in the folder containing `TUI-Snake.py` and run:

```powershell
py TUI-Snake.py
```

Make sure your terminal window is large enough for the game board.

## Updates

### Latest Update

* Added **multiple fruit types**: Apple, Orange, Lemon, Grape, Strawberry, and Cherry
* Added a **Fruit selector** to the Options menu
* Use **LEFT / RIGHT** in Options to change the selected fruit
* Each fruit has its own **point value**
* Added a **session timer** to track how long you've been playing
* Added a brief **NEW HIGH SCORE!** notification next to the score display
* Fixed fruit collection handling to prevent errors when removing collected fruit
* Improved the pause and options menus
* Added mouse support for menu interaction and movement


## Controls

| Key               | Action                  |
| ----------------- | ----------------------- |
| WASD / Arrow Keys | Move                    |
| `ESC`             | Pause / Resume          |
| `R`               | Restart after game over |
| `Q`               | Quit after game over    |

## Built With

Python, `curses`, `random`, and `time`.
