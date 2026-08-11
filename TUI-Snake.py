import curses
import random
import time


def draw_grid(stdscr, height, width, grid_color):
    for y in range(1, height - 1):
        for x in range(1, width - 1):
            try:
                stdscr.addch(y, x, ".", grid_color)
            except curses.error:
                pass


def draw_snake(stdscr, snake, snake_color):
    height, width = stdscr.getmaxyx()

    for i, (y, x) in enumerate(snake):
        if not (0 <= y < height and 0 <= x < width):
            continue

        try:
            if i == 0:
                if x + 1 < width:
                    stdscr.addstr(
                        y, x, "██",
                        snake_color | curses.A_BOLD
                    )
            else:
                if x + 1 < width:
                    stdscr.addstr(
                        y, x, "██",
                        snake_color
                    )
        except curses.error:
            pass


def draw_apples(stdscr, apples, apple_color):
    height, width = stdscr.getmaxyx()

    for y, x in apples:
        if 0 < y < height - 1 and 0 < x < width - 1:
            try:
                stdscr.addch(
                    y,
                    x,
                    "O",
                    apple_color | curses.A_BOLD | curses.A_REVERSE
                )
            except curses.error:
                pass


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

    try:
        stdscr.attron(border_color)
        stdscr.border()
        stdscr.attroff(border_color)

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


def draw_pause_menu(
    stdscr,
    height,
    width,
    score,
    high_score,
    text_color
):
    box_width = min(44, max(24, width - 4))
    box_height = min(15, max(11, height - 4))

    start_y = max(1, (height - box_height) // 2)
    start_x = max(1, (width - box_width) // 2)

    # Clear menu area
    for y in range(
        start_y,
        min(height - 1, start_y + box_height)
    ):
        try:
            stdscr.addstr(
                y,
                start_x,
                " " * min(
                    box_width,
                    width - start_x - 1
                )
            )
        except curses.error:
            pass

    # Box
    try:
        stdscr.addstr(
            start_y,
            start_x,
            "╔" + "═" * (box_width - 2) + "╗",
            text_color | curses.A_BOLD
        )

        for y in range(
            start_y + 1,
            start_y + box_height - 1
        ):
            stdscr.addstr(
                y,
                start_x,
                "║",
                text_color | curses.A_BOLD
            )

            stdscr.addstr(
                y,
                start_x + box_width - 1,
                "║",
                text_color | curses.A_BOLD
            )

        stdscr.addstr(
            start_y + box_height - 1,
            start_x,
            "╚" + "═" * (box_width - 2) + "╝",
            text_color | curses.A_BOLD
        )

    except curses.error:
        pass

    def put_text(y, text, bold=False):
        if y <= start_y or y >= start_y + box_height - 1:
            return

        max_length = box_width - 4
        text = text[:max_length]

        x = start_x + (box_width - len(text)) // 2

        try:
            stdscr.addstr(
                y,
                x,
                text,
                text_color | (
                    curses.A_BOLD if bold else 0
                )
            )
        except curses.error:
            pass

    put_text(
        start_y + 1,
        "GAME PAUSED",
        True
    )

    if box_height >= 13:
        put_text(start_y + 3, "████")
        put_text(start_y + 4, "████████████")
        put_text(start_y + 5, "████    ████")
        put_text(start_y + 6, "████ O  ████")

    put_text(
        start_y + box_height - 5,
        f"Score: {score} | High: {high_score}"
    )

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


def mouse_direction(
    snake,
    mouse_x,
    mouse_y,
    current_direction
):
    head_y, head_x = snake[0]

    dx = mouse_x - head_x
    dy = mouse_y - head_y

    # Ignore tiny mouse movements
    if abs(dx) <= 1 and abs(dy) <= 1:
        return current_direction

    # Move toward the mouse's strongest axis
    if abs(dx) > abs(dy):

        if dx > 0:
            if current_direction != curses.KEY_LEFT:
                return curses.KEY_RIGHT
        else:
            if current_direction != curses.KEY_RIGHT:
                return curses.KEY_LEFT

    else:

        if dy > 0:
            if current_direction != curses.KEY_UP:
                return curses.KEY_DOWN
        else:
            if current_direction != curses.KEY_DOWN:
                return curses.KEY_UP

    return current_direction


def play_game(stdscr, high_score):

    height, width = stdscr.getmaxyx()

    if width < 25 or height < 12:
        stdscr.erase()

        try:
            stdscr.addstr(
                max(0, height // 2 - 1),
                max(0, (width - 20) // 2),
                "Terminal too small."
            )

            stdscr.addstr(
                max(0, height // 2),
                max(0, (width - 30) // 2),
                "Resize the window and retry."
            )
        except curses.error:
            pass

        stdscr.refresh()
        stdscr.getch()

        return 0, high_score, "quit"

    # =========================
    # COLORS
    # =========================

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

    # =========================
    # ENABLE MOUSE
    # =========================

    curses.mousemask(
        curses.ALL_MOUSE_EVENTS
        | curses.REPORT_MOUSE_POSITION
    )

    curses.mouseinterval(0)

    # =========================
    # GAME VARIABLES
    # =========================

    score = 0
    paused = False
    mouse_dragging = False

    snake = [
        [height // 2, width // 2 - 2],
        [height // 2, width // 2 - 3],
        [height // 2, width // 2 - 4]
    ]

    direction = curses.KEY_RIGHT

    # =========================
    # CREATE 10 APPLES
    # =========================

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

    # =========================
    # GAME LOOP
    # =========================

    while True:

        speed = max(
            35,
            80 - score * 3
        )

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

            elif key in (
                ord("r"),
                ord("R")
            ):

                return 0, high_score, "restart"

            elif key in (
                ord("q"),
                ord("Q")
            ):

                return score, high_score, "quit"

            continue

        # =========================
        # NORMAL GAME
        # =========================

        stdscr.timeout(speed)

        key = stdscr.getch()

        # =========================
        # MOUSE
        # =========================

        if key == curses.KEY_MOUSE:

            try:
                (
                    _,
                    mouse_x,
                    mouse_y,
                    _,
                    mouse_state
                ) = curses.getmouse()

                # Left mouse button pressed
                if mouse_state & curses.BUTTON1_PRESSED:

                    head_y, head_x = snake[0]

                    # Check whether click is on/near snake
                    if (
                        abs(mouse_y - head_y) <= 1
                        and abs(mouse_x - head_x) <= 2
                    ):
                        mouse_dragging = True

                # Mouse movement while dragging
                if mouse_dragging:

                    direction = mouse_direction(
                        snake,
                        mouse_x,
                        mouse_y,
                        direction
                    )

                # Release left mouse button
                if mouse_state & curses.BUTTON1_RELEASED:
                    mouse_dragging = False

            except curses.error:
                pass

            continue

        # =========================
        # ESC = PAUSE
        # =========================

        if key == 27:
            paused = True
            mouse_dragging = False
            continue

        # =========================
        # KEYBOARD CONTROLS
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

        # =========================
        # MOVE SNAKE
        # =========================

        old_tail = snake[-1].copy()

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
        # WALL COLLISION
        # =========================

        if (
            head[0] <= 0
            or head[0] >= height - 1
            or head[1] <= 0
            or head[1] >= width - 2
        ):
            return score, high_score, "dead"

        # =========================
        # SELF COLLISION
        # =========================

        if head in snake:
            return score, high_score, "dead"

        snake.insert(0, head)

        # =========================
        # APPLE
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

            # Grow blink
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

        # =========================
        # DRAW
        # =========================

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

    # Session-only high score
    high_score = 0

    while True:

        score, high_score, result = play_game(
            stdscr,
            high_score
        )

        if result == "quit":
            return

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

        try:
            stdscr.addstr(
                y,
                x,
                message,
                curses.color_pair(2) | curses.A_BOLD
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
