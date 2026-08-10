# TUI Snake
# PS: Your colors may look different based on the color scheme! im using catppuccin mocha in the picture.
<img width="1209" height="640" alt="image" src="https://github.com/user-attachments/assets/076f8722-bb35-4dc1-84a4-b531ea0fc6d4" />
A simple Snake game for the terminal, written in Python using `curses`.

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

Install `windows-curses`:

```powershell
py -m pip install windows-curses
```

## Running

```powershell
py snake.py
```

## Controls

| Key               | Action  |
| ----------------- | ------- |
| WASD / Arrow Keys | Move    |
| ESC               | Pause   |
| R                 | Restart |
| Q                 | Quit    |

## Built With

Python, `curses`, `random`, and `time`.
