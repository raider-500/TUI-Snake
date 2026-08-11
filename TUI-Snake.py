import curses
import random
import time


def draw_grid(stdscr, height, width, grid_color):
    for y in range(1, height - 1):
        for x in range(1, width - 1):
            stdscr.addch(y, x, ".", grid_color)


def draw_snake(stdscr, snake, snake_color):
    for i, (y, x) in enumerate(snake):
        if i == 0:
            stdscr.addstr(
                y, x, "██",
                snake_color | curses.A_BOLD
            )
        else:
            stdscr.addstr(
                y, x, "██",
                snake_color
            )


def draw_apples(stdscr, apples, apple_color):
    for y, x in apples:
        stdscr.addch(
            y, x, "O",
            apple_color | curses.A_BOLD | curses.A_REVERSE
        )


def draw_pause_menu(stdscr, height, width, score, high_score, text_color):
    # =========================
    # PAUSE MENU
    # =========================

    box_width = 46
    box_height = 13

    start_y = max(1, (height - box_height) // 2)
    start_x = max(1, (width - box_width) // 2)

    # Clear the area where the menu will go
    for y in range(
        start_y,
        min(height - 1, start_y + box_height)
    ):
        stdscr.addstr(
            y,
            start_x,
            " " * min(box_width, width - start_x - 1),
            text_color
        )

    # ASCII box
    top = "╔" + "═" * (box_width - 2) + "╗"
    bottom = "╚" + "═" * (box_width - 2) + "╝"

    stdscr.addstr(
        start_y,
        start_x,
        top,
        text_color | curses.A_BOLD
    )

    # Title
    title = "║          GAME PAUSED           ║"

    stdscr.addstr(
        start_y + 1,
        start_x,
        title,
        text_color | curses.A_BOLD
    )

    # Snake ASCII art
    art = [
        "║       ████                    ║",
        "║   ████████████                ║",
        "║ ████      ████                ║",
        "║ ████  O   ████                ║",
        "║   ████████████                ║",
        "║       ████                    ║",
    ]

    for i, line in enumerate(art):
        stdscr.addstr(
            start_y + 2 + i,
            start_x,
            line,
            text_color
        )

    # Score
    score_text = (
        f"║  Score: {score:<6} "
        f"High Score: {high_score:<6}║"
    )

    stdscr.addstr(
        start_y + 8,
        start_x,
        score_text,
        text_color
    )

    # Options
    options = [
        "║  [ESC] Resume                 ║",
        "║  [R]   Restart                ║",
        "║  [Q]   Quit                   ║",
    ]

    for i, line in enumerate(options):
        stdscr.addstr(
            start_y + 9 + i,
            start_x,
            line,
            text_color
        )

    # Bottom border
    stdscr.addstr(
        start_y + box_height - 1,
        start_x,
        bottom,
        text_color | curses.A_BOLD
    )

    stdscr.refresh()


def play_game(stdscr, high_score):
    height, width = stdscr.getmaxyx()

    if width < 50 or height < 16:
        stdscr.addstr(
            1,
            1,
            "Terminal too small! Make the window bigger."
        )
        stdscr.getch()
        return 0, high_score, "quit"

    # =========================
    # COLORS
    # =========================

    curses.start_color()

    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_GREEN)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_GREEN)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_GREEN)
    curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_GREEN)
    curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_GREEN)
    curses.init_pair(6, curses.COLOR_BLACK, curses.COLOR_GREEN)

    snake_color = curses.color_pair(1)
    apple_color = curses.color_pair(2)
    text_color = curses.color_pair(3)
    border_color = curses.color_pair(4)
    background_color = curses.color_pair(5)
    grid_color = curses.color_pair(6)

    # =========================
    # BACKGROUND
    # =========================

    stdscr.bkgd(" ", background_color)
    stdscr.erase()

    # =========================
    # GAME VARIABLES
    # =========================

    score = 0
    paused = False

    snake = [
        [height // 2, width // 2 - 2],
        [height // 2, width // 2 - 3],
        [height // 2, width // 2 - 4]
    ]

    direction = curses.KEY_RIGHT

    # =========================
    # CREATE APPLES
    # =========================

    apples = []

    while len(apples) < 10:
        new_apple = [
            random.randint(1, height - 2),
            random.randint(1, width - 3)
        ]

        if new_apple not in snake and new_apple not in apples:
            apples.append(new_apple)

    # =========================
    # INITIAL DRAW
    # =========================

    draw_grid(
        stdscr,
        height,
        width,
        grid_color
    )

    stdscr.attron(border_color)
    stdscr.border()
    stdscr.attroff(border_color)

    stdscr.addstr(
        0,
        2,
        f" Score: {score} | High Score: {high_score} ",
        text_color | curses.A_BOLD
    )

    draw_snake(
        stdscr,
        snake,
        snake_color
    )

    draw_apples(
        stdscr,
        apples,
        apple_color
    )

    stdscr.refresh()

    # =========================
    # GAME LOOP
    # =========================

    while True:

        speed = max(35, 80 - score * 3)

        # =========================
        # PAUSED
        # =========================

        if paused:

            stdscr.timeout(-1)

            draw_pause_menu(
                stdscr,
                height,
                width,
                score,
                high_score,
                text_color
            )

            key = stdscr.getch()

            # Resume
            if key == 27:

                paused = False

                stdscr.erase()
                stdscr.bkgd(" ", background_color)

                draw_grid(
                    stdscr,
                    height,
                    width,
                    grid_color
                )

                stdscr.attron(border_color)
                stdscr.border()
                stdscr.attroff(border_color)

                stdscr.addstr(
                    0,
                    2,
                    f" Score: {score} | High Score: {high_score} ",
                    text_color | curses.A_BOLD
                )

                draw_snake(
                    stdscr,
                    snake,
                    snake_color
                )

                draw_apples(
                    stdscr,
                    apples,
                    apple_color
                )

                stdscr.refresh()

            # Restart
            elif key in (ord("r"), ord("R")):
                return 0, high_score, "restart"

            # Quit
            elif key in (ord("q"), ord("Q")):
                return score, high_score, "quit"

            continue

        # =========================
        # NORMAL GAME
        # =========================

        stdscr.timeout(speed)

        key = stdscr.getch()

        # ESC = PAUSE
        if key == 27:
            paused = True
            continue

        # =========================
        # ARROW KEYS
        # =========================

        if key == curses.KEY_UP:
            if direction != curses.KEY_DOWN:
                direction = curses.KEY_UP

        elif key == curses.KEY_DOWN:
            if direction != curses.KEY_UP:
                direction = curses.KEY_DOWN

        elif key == curses.KEY_LEFT:
            if direction != curses.KEY_RIGHT:
                direction = curses.KEY_LEFT

        elif key == curses.KEY_RIGHT:
            if direction != curses.KEY_LEFT:
                direction = curses.KEY_RIGHT

        # =========================
        # WASD
        # =========================

        elif key in (ord("w"), ord("W")):
            if direction != curses.KEY_DOWN:
                direction = curses.KEY_UP

        elif key in (ord("s"), ord("S")):
            if direction != curses.KEY_UP:
                direction = curses.KEY_DOWN

        elif key in (ord("a"), ord("A")):
            if direction != curses.KEY_RIGHT:
                direction = curses.KEY_LEFT

        elif key in (ord("d"), ord("D")):
            if direction != curses.KEY_LEFT:
                direction = curses.KEY_RIGHT

        # =========================
        # OLD TAIL
        # =========================

        old_tail = snake[-1].copy()

        # =========================
        # NEW HEAD
        # =========================

        head = snake[0].copy()

        if direction == curses.KEY_UP:
            head[0] -= 1

        elif direction == curses.KEY_DOWN:
            head[0] += 1

        elif direction == curses.KEY_LEFT:
            head[1] -= 1

        elif direction == curses.KEY_RIGHT:
            head[1] += 1

        # =========================
        # COLLISION
        # =========================

        if (
            head[0] == 0
            or head[0] == height - 1
            or head[1] == 0
            or head[1] >= width - 2
        ):
            return score, high_score, "dead"

        if head in snake:
            return score, high_score, "dead"

        # =========================
        # ADD HEAD
        # =========================

        snake.insert(0, head)

        # =========================
        # EAT APPLE
        # =========================

        if head in apples:

            score += 1

            if score > high_score:
                high_score = score

            apples.remove(head)

            while True:

                new_apple = [
                    random.randint(1, height - 2),
                    random.randint(1, width - 3)
                ]

                if (
                    new_apple not in snake
                    and new_apple not in apples
                ):
                    apples.append(new_apple)
                    break

            # =========================
            # GROW BLINK
            # =========================

            for _ in range(3):

                for y, x in snake:
                    stdscr.addstr(
                        y,
                        x,
                        "..",
                        grid_color
                    )

                stdscr.refresh()
                time.sleep(0.06)

                draw_snake(
                    stdscr,
                    snake,
                    snake_color
                )

                stdscr.refresh()
                time.sleep(0.06)

        else:

            snake.pop()

            stdscr.addstr(
                old_tail[0],
                old_tail[1],
                "..",
                grid_color
            )

        # =========================
        # SCORE
        # =========================

        stdscr.addstr(
            0,
            2,
            f" Score: {score} | High Score: {high_score} ",
            text_color | curses.A_BOLD
        )

        draw_snake(
            stdscr,
            snake,
            snake_color
        )

        draw_apples(
            stdscr,
            apples,
            apple_color
        )

        stdscr.refresh()


def main(stdscr):

    curses.curs_set(0)

    # Session-only high score
    high_score = 0

    while True:

        score, high_score, result = play_game(
            stdscr,
            high_score
        )

        # Quit from pause menu
        if result == "quit":
            return

        # Restart directly
        if result == "restart":
            continue

        # =========================
        # GAME OVER
        # =========================

        stdscr.nodelay(False)

        height, width = stdscr.getmaxyx()

        message = (
            f" GAME OVER | Score: {score} | "
            f"High Score: {high_score} | "
            "R = Restart | Q = Quit "
        )

        y = height // 2
        x = max(
            0,
            (width - len(message)) // 2
        )

        stdscr.addstr(
            y,
            x,
            message,
            curses.color_pair(2) | curses.A_BOLD
        )

        stdscr.refresh()

        while True:

            key = stdscr.getch()

            if key in (ord("r"), ord("R")):
                break

            elif key in (ord("q"), ord("Q")):
                return


curses.wrapper(main)
