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
            if x + 1 < stdscr.getmaxyx()[1]:
                stdscr.addstr(
                    y, x, "██",
                    snake_color | curses.A_BOLD
                )
        else:
            if x + 1 < stdscr.getmaxyx()[1]:
                stdscr.addstr(
                    y, x, "██",
                    snake_color
                )


def draw_apples(stdscr, apples, apple_color):
    height, width = stdscr.getmaxyx()

    for y, x in apples:
        if 0 < y < height - 1 and 0 < x < width - 1:
            stdscr.addch(
                y, x, "O",
                apple_color | curses.A_BOLD | curses.A_REVERSE
            )


def draw_pause_menu(
    stdscr,
    height,
    width,
    score,
    high_score,
    text_color
):
    # =====================================
    # UNIVERSAL PAUSE MENU
    # =====================================

    # Minimum dimensions required for the menu
    min_box_width = 34
    min_box_height = 13

    # Adapt box width to terminal
    box_width = min(
        min_box_width,
        max(20, width - 4)
    )

    # Adapt box height to terminal
    box_height = min(
        min_box_height,
        max(7, height - 4)
    )

    # Center the box
    start_y = max(
        1,
        (height - box_height) // 2
    )

    start_x = max(
        1,
        (width - box_width) // 2
    )

    # =====================================
    # CLEAR MENU AREA
    # =====================================

    for y in range(
        start_y,
        min(height - 1, start_y + box_height)
    ):
        try:
            stdscr.addstr(
                y,
                start_x,
                " " * (box_width - 1),
                text_color
            )
        except curses.error:
            pass

    # =====================================
    # BOX DRAWING
    # =====================================

    try:
        # Top
        stdscr.addch(
            start_y,
            start_x,
            "╔",
            text_color | curses.A_BOLD
        )

        for x in range(
            start_x + 1,
            start_x + box_width - 1
        ):
            stdscr.addch(
                start_y,
                x,
                "═",
                text_color | curses.A_BOLD
            )

        stdscr.addch(
            start_y,
            start_x + box_width - 1,
            "╗",
            text_color | curses.A_BOLD
        )

        # Bottom
        bottom_y = start_y + box_height - 1

        stdscr.addch(
            bottom_y,
            start_x,
            "╚",
            text_color | curses.A_BOLD
        )

        for x in range(
            start_x + 1,
            start_x + box_width - 1
        ):
            stdscr.addch(
                bottom_y,
                x,
                "═",
                text_color | curses.A_BOLD
            )

        stdscr.addch(
            bottom_y,
            start_x + box_width - 1,
            "╝",
            text_color | curses.A_BOLD
        )

        # Sides
        for y in range(
            start_y + 1,
            bottom_y
        ):
            stdscr.addch(
                y,
                start_x,
                "║",
                text_color
            )

            stdscr.addch(
                y,
                start_x + box_width - 1,
                "║",
                text_color
            )

    except curses.error:
        pass

    # =====================================
    # SAFE TEXT FUNCTION
    # =====================================

    def put_text(row, text, bold=False):
        if row <= start_y:
            return

        if row >= start_y + box_height - 1:
            return

        # Keep text inside box
        max_length = box_width - 4

        if len(text) > max_length:
            text = text[:max_length]

        x = start_x + (box_width - len(text)) // 2

        if x < start_x + 1:
            x = start_x + 1

        try:
            stdscr.addstr(
                row,
                x,
                text,
                text_color | (
                    curses.A_BOLD if bold else 0
                )
            )
        except curses.error:
            pass

    # =====================================
    # TITLE
    # =====================================

    put_text(
        start_y + 1,
        "GAME PAUSED",
        True
    )

    # =====================================
    # SNAKE ASCII ART
    # =====================================

    if box_height >= 11:

        put_text(
            start_y + 3,
            "████"
        )

        put_text(
            start_y + 4,
            "████████████"
        )

        put_text(
            start_y + 5,
            "████    ████"
        )

        put_text(
            start_y + 6,
            "████ O  ████"
        )

    # =====================================
    # SCORE
    # =====================================

    score_y = start_y + box_height - 5

    put_text(
        score_y,
        f"Score: {score} | High: {high_score}"
    )

    # =====================================
    # CONTROLS
    # =====================================

    if box_height >= 10:

        put_text(
            start_y + box_height - 4,
            "[ESC] Resume"
        )

        put_text(
            start_y + box_height - 3,
            "[R] Restart"
        )

        put_text(
            start_y + box_height - 2,
            "[Q] Quit"
        )

    stdscr.refresh()


def redraw_game(
    stdscr,
    height,
    width,
    score,
    high_score,
    snake,
    apples,
    grid_color,
    border_color,
    text_color,
    snake_color,
    apple_color,
    background_color
):
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


def play_game(stdscr, high_score):

    height, width = stdscr.getmaxyx()

    # =====================================
    # TERMINAL SIZE CHECK
    # =====================================

    if width < 25 or height < 12:

        stdscr.erase()

        message1 = "Terminal too small."
        message2 = "Resize the window and try again."

        try:
            stdscr.addstr(
                height // 2 - 1,
                max(0, (width - len(message1)) // 2),
                message1
            )

            stdscr.addstr(
                height // 2,
                max(0, (width - len(message2)) // 2),
                message2
            )

        except curses.error:
            pass

        stdscr.refresh()
        stdscr.getch()

        return 0, high_score, "quit"

    # =====================================
    # COLORS
    # =====================================

    curses.start_color()

    curses.init_pair(
        1,
        curses.COLOR_BLUE,
        curses.COLOR_GREEN
    )

    curses.init_pair(
        2,
        curses.COLOR_RED,
        curses.COLOR_GREEN
    )

    curses.init_pair(
        3,
        curses.COLOR_BLACK,
        curses.COLOR_GREEN
    )

    snake_color = curses.color_pair(1)
    apple_color = curses.color_pair(2)
    text_color = curses.color_pair(3)
    border_color = curses.color_pair(3)
    grid_color = curses.color_pair(3)
    background_color = curses.color_pair(3)

    # =====================================
    # GAME VARIABLES
    # =====================================

    score = 0
    paused = False

    snake = [
        [height // 2, width // 2 - 2],
        [height // 2, width // 2 - 3],
        [height // 2, width // 2 - 4]
    ]

    direction = curses.KEY_RIGHT

    # =====================================
    # APPLES
    # =====================================

    apples = []

    while len(apples) < 10:

        new_apple = [
            random.randint(1, height - 2),
            random.randint(1, width - 3)
        ]

        if (
            new_apple not in snake
            and new_apple not in apples
        ):
            apples.append(new_apple)

    # =====================================
    # INITIAL DRAW
    # =====================================

    redraw_game(
        stdscr,
        height,
        width,
        score,
        high_score,
        snake,
        apples,
        grid_color,
        border_color,
        text_color,
        snake_color,
        apple_color,
        background_color
    )

    # =====================================
    # GAME LOOP
    # =====================================

    while True:

        speed = max(
            35,
            80 - score * 3
        )

        # =================================
        # PAUSED
        # =================================

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

                redraw_game(
                    stdscr,
                    height,
                    width,
                    score,
                    high_score,
                    snake,
                    apples,
                    grid_color,
                    border_color,
                    text_color,
                    snake_color,
                    apple_color,
                    background_color
                )

            # Restart
            elif key in (
                ord("r"),
                ord("R")
            ):

                return (
                    0,
                    high_score,
                    "restart"
                )

            # Quit
            elif key in (
                ord("q"),
                ord("Q")
            ):

                return (
                    score,
                    high_score,
                    "quit"
                )

            continue

        # =================================
        # NORMAL GAME
        # =================================

        stdscr.timeout(speed)

        key = stdscr.getch()

        # ESC
        if key == 27:

            paused = True
            continue

        # =================================
        # MOVEMENT
        # =================================

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

        elif key in (
            ord("w"),
            ord("W")
        ):
            if direction != curses.KEY_DOWN:
                direction = curses.KEY_UP

        elif key in (
            ord("s"),
            ord("S")
        ):
            if direction != curses.KEY_UP:
                direction = curses.KEY_DOWN

        elif key in (
            ord("a"),
            ord("A")
        ):
            if direction != curses.KEY_RIGHT:
                direction = curses.KEY_LEFT

        elif key in (
            ord("d"),
            ord("D")
        ):
            if direction != curses.KEY_LEFT:
                direction = curses.KEY_RIGHT

        # =================================
        # OLD TAIL
        # =================================

        old_tail = snake[-1].copy()

        # =================================
        # NEW HEAD
        # =================================

        head = snake[0].copy()

        if direction == curses.KEY_UP:
            head[0] -= 1

        elif direction == curses.KEY_DOWN:
            head[0] += 1

        elif direction == curses.KEY_LEFT:
            head[1] -= 1

        elif direction == curses.KEY_RIGHT:
            head[1] += 1

        # =================================
        # COLLISION
        # =================================

        if (
            head[0] <= 0
            or head[0] >= height - 1
            or head[1] <= 0
            or head[1] >= width - 2
        ):
            return (
                score,
                high_score,
                "dead"
            )

        if head in snake:
            return (
                score,
                high_score,
                "dead"
            )

        # =================================
        # ADD HEAD
        # =================================

        snake.insert(0, head)

        # =================================
        # APPLE
        # =================================

        if head in apples:

            score += 1

            if score > high_score:
                high_score = score

            apples.remove(head)

            while True:

                new_apple = [
                    random.randint(
                        1,
                        height - 2
                    ),
                    random.randint(
                        1,
                        width - 3
                    )
                ]

                if (
                    new_apple not in snake
                    and new_apple not in apples
                ):
                    apples.append(new_apple)
                    break

            # Blink
            for _ in range(3):

                for y, x in snake:

                    try:
                        stdscr.addstr(
                            y,
                            x,
                            "..",
                            grid_color
                        )
                    except curses.error:
                        pass

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

            try:
                stdscr.addstr(
                    old_tail[0],
                    old_tail[1],
                    "..",
                    grid_color
                )
            except curses.error:
                pass

        # =================================
        # SCORE
        # =================================

        try:

            stdscr.addstr(
                0,
                2,
                f" Score: {score} | High Score: {high_score} ",
                text_color | curses.A_BOLD
            )

        except curses.error:
            pass

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

    high_score = 0

    while True:

        score, high_score, result = play_game(
            stdscr,
            high_score
        )

        # Quit
        if result == "quit":
            return

        # Restart
        if result == "restart":
            continue

        # =================================
        # GAME OVER
        # =================================

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

        try:

            stdscr.addstr(
                y,
                x,
                message,
                curses.color_pair(2)
                | curses.A_BOLD
            )

        except curses.error:
            pass

        stdscr.refresh()

        while True:

            key = stdscr.getch()

            if key in (
                ord("r"),
                ord("R")
            ):
                break

            elif key in (
                ord("q"),
                ord("Q")
            ):
                return


curses.wrapper(main)
