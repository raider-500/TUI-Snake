import curses
import random
import time


# ============================================================
# COLOR OPTIONS
# ============================================================

COLOR_NAMES = [
    ("Blue", curses.COLOR_BLUE),
    ("Red", curses.COLOR_RED),
    ("Green", curses.COLOR_GREEN),
    ("Yellow", curses.COLOR_YELLOW),
    ("Cyan", curses.COLOR_CYAN),
    ("Magenta", curses.COLOR_MAGENTA),
    ("White", curses.COLOR_WHITE),
    ("Black", curses.COLOR_BLACK),
]


# ============================================================
# SETUP COLORS
# ============================================================

def setup_colors(settings):
    curses.start_color()

    curses.init_pair(
        1,
        settings["snake"],
        settings["background"]
    )

    curses.init_pair(
        2,
        settings["apple"],
        settings["background"]
    )

    curses.init_pair(
        3,
        settings["text"],
        settings["background"]
    )

    return (
        curses.color_pair(1),
        curses.color_pair(2),
        curses.color_pair(3),
    )


# ============================================================
# NEW HIGH SCORE SCREEN
# ============================================================

def new_high_score_screen(stdscr, score, text_color):
    height, width = stdscr.getmaxyx()

    art = [
        "███╗   ██╗███████╗██╗    ██╗",
        "████╗  ██║██╔════╝██║    ██║",
        "██╔██╗ ██║█████╗  ██║ █╗ ██║",
        "██║╚██╗██║██╔══╝  ██║███╗██║",
        "██║ ╚████║███████╗╚███╔███╔╝",
        "╚═╝  ╚═══╝╚══════╝ ╚══╝╚══╝ ",
        "",
        "██╗  ██╗██╗ ██████╗ ██╗  ██╗",
        "██║  ██║██║██╔════╝ ██║  ██║",
        "███████║██║██║      ███████║",
        "██╔══██║██║██║      ██╔══██║",
        "██║  ██║██║╚██████╗ ██║  ██║",
        "╚═╝  ╚═╝╚═╝ ╚═════╝ ╚═╝  ╚═╝",
    ]

    stdscr.erase()

    for i, line in enumerate(art):

        y = height // 2 - len(art) // 2 + i
        x = max(0, (width - len(line)) // 2)

        try:
            stdscr.addstr(
                y,
                x,
                line,
                text_color | curses.A_BOLD
            )
        except curses.error:
            pass

    score_text = f"NEW HIGH SCORE: {score}"

    try:
        y = min(
            height - 2,
            height // 2 + len(art) // 2 + 2
        )

        x = max(
            0,
            (width - len(score_text)) // 2
        )

        stdscr.addstr(
            y,
            x,
            score_text,
            text_color | curses.A_BOLD
        )

    except curses.error:
        pass

    stdscr.refresh()

    time.sleep(1.5)


# ============================================================
# DRAW GRID
# ============================================================

def draw_grid(stdscr, height, width, grid_color):

    for y in range(1, height - 1):

        for x in range(1, width - 2):

            try:
                stdscr.addch(
                    y,
                    x,
                    ".",
                    grid_color
                )
            except curses.error:
                pass


# ============================================================
# DRAW SNAKE
# ============================================================

def draw_snake(stdscr, snake, snake_color):

    height, width = stdscr.getmaxyx()

    for i, (y, x) in enumerate(snake):

        if not (
            0 <= y < height
            and 0 <= x < width - 1
        ):
            continue

        try:

            if i == 0:

                stdscr.addstr(
                    y,
                    x,
                    "██",
                    snake_color | curses.A_BOLD
                )

            else:

                stdscr.addstr(
                    y,
                    x,
                    "██",
                    snake_color
                )

        except curses.error:
            pass


# ============================================================
# DRAW APPLES
# ============================================================

def draw_apples(stdscr, apples, apple_color):

    height, width = stdscr.getmaxyx()

    for y, x in apples:

        if (
            0 < y < height - 1
            and 0 < x < width - 2
        ):

            try:
                stdscr.addch(
                    y,
                    x,
                    "●",
                    apple_color | curses.A_BOLD
                )

            except curses.error:

                try:
                    stdscr.addch(
                        y,
                        x,
                        "O",
                        apple_color | curses.A_BOLD
                    )
                except curses.error:
                    pass


# ============================================================
# DRAW GAME
# ============================================================

def redraw_game(
    stdscr,
    height,
    width,
    score,
    high_score,
    snake,
    apples,
    snake_color,
    apple_color,
    text_color
):

    stdscr.erase()

    draw_grid(
        stdscr,
        height,
        width,
        text_color
    )

    try:

        stdscr.attron(text_color)

        stdscr.border()

        stdscr.attroff(text_color)

        score_text = (
            f" Score: {score} | High Score: {high_score} "
        )

        stdscr.addstr(
            0,
            2,
            score_text,
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


# ============================================================
# MAIN MENU
# ============================================================

def main_menu(stdscr, settings):

    height, width = stdscr.getmaxyx()

    _, _, text_color = setup_colors(settings)

    stdscr.erase()

    title = [
        "████████╗██╗   ██╗██╗",
        "╚══██╔══╝██║   ██║██║",
        "   ██║   ██║   ██║██║",
        "   ██║   ██║   ██║██║",
        "   ██║   ╚██████╔╝██║",
        "   ╚═╝    ╚═════╝ ╚═╝",
    ]

    start_y = max(
        1,
        height // 2 - 9
    )

    for i, line in enumerate(title):

        x = max(
            0,
            (width - len(line)) // 2
        )

        try:
            stdscr.addstr(
                start_y + i,
                x,
                line,
                text_color | curses.A_BOLD
            )
        except curses.error:
            pass

    subtitle = "Terminal Snake"

    try:
        stdscr.addstr(
            start_y + 7,
            max(
                0,
                (width - len(subtitle)) // 2
            ),
            subtitle,
            text_color
        )
    except curses.error:
        pass

    button = [
        "╔══════════════════════════╗",
        "║          PLAY            ║",
        "╚══════════════════════════╝",
    ]

    button_y = start_y + 10

    for i, line in enumerate(button):

        x = max(
            0,
            (width - len(line)) // 2
        )

        try:
            stdscr.addstr(
                button_y + i,
                x,
                line,
                text_color | curses.A_BOLD
            )
        except curses.error:
            pass

    controls = (
        "ENTER / Left Click to Play    Q to Quit"
    )

    try:
        stdscr.addstr(
            button_y + 5,
            max(
                0,
                (width - len(controls)) // 2
            ),
            controls,
            text_color
        )
    except curses.error:
        pass

    stdscr.refresh()

    stdscr.timeout(100)

    while True:

        key = stdscr.getch()

        if key in (
            curses.KEY_ENTER,
            10,
            13,
            ord(" "),
        ):
            return "play"

        if key in (
            ord("q"),
            ord("Q"),
        ):
            return "quit"

        if key == curses.KEY_MOUSE:

            try:

                _, mouse_x, mouse_y, _, mouse_state = (
                    curses.getmouse()
                )

                if mouse_state & curses.BUTTON1_CLICKED:

                    button_width = 28

                    button_x = max(
                        0,
                        (width - button_width) // 2
                    )

                    if (
                        button_y
                        <= mouse_y
                        <= button_y + 2
                        and
                        button_x
                        <= mouse_x
                        <= button_x + button_width
                    ):
                        return "play"

            except curses.error:
                pass


# ============================================================
# OPTIONS MENU
# ============================================================

def options_menu(stdscr, settings):

    selected = 0

    options = [
        ("Snake Color", "snake"),
        ("Apple Color", "apple"),
        ("Text / Grid Color", "text"),
        ("Background Color", "background"),
    ]

    while True:

        height, width = stdscr.getmaxyx()

        _, _, text_color = setup_colors(settings)

        stdscr.erase()

        title = "OPTIONS"

        try:
            stdscr.addstr(
                2,
                max(
                    0,
                    (width - len(title)) // 2
                ),
                title,
                text_color | curses.A_BOLD
            )
        except curses.error:
            pass

        description = (
            "UP/DOWN = Select    LEFT/RIGHT = Change"
        )

        try:
            stdscr.addstr(
                4,
                max(
                    0,
                    (width - len(description)) // 2
                ),
                description,
                text_color
            )
        except curses.error:
            pass

        for i, (name, setting_key) in enumerate(options):

            y = 7 + i * 2

            color_value = settings[setting_key]

            color_name = "Unknown"

            for name_value, color_id in COLOR_NAMES:

                if color_id == color_value:

                    color_name = name_value
                    break

            prefix = "> " if i == selected else "  "

            line = (
                f"{prefix}{name}: {color_name}"
            )

            try:

                attr = text_color

                if i == selected:
                    attr |= curses.A_REVERSE

                stdscr.addstr(
                    y,
                    max(
                        0,
                        (width - len(line)) // 2
                    ),
                    line,
                    attr
                )

            except curses.error:
                pass

        back = "ESC / B = Back"

        try:
            stdscr.addstr(
                height - 2,
                max(
                    0,
                    (width - len(back)) // 2
                ),
                back,
                text_color
            )
        except curses.error:
            pass

        stdscr.refresh()

        stdscr.timeout(-1)

        key = stdscr.getch()

        if key in (
            curses.KEY_UP,
            ord("w"),
            ord("W"),
        ):

            selected = (
                selected - 1
            ) % len(options)

        elif key in (
            curses.KEY_DOWN,
            ord("s"),
            ord("S"),
        ):

            selected = (
                selected + 1
            ) % len(options)

        elif key in (
            curses.KEY_LEFT,
            ord("a"),
            ord("A"),
        ):

            setting_key = options[selected][1]

            color_ids = [
                color_id
                for _, color_id in COLOR_NAMES
            ]

            current_index = color_ids.index(
                settings[setting_key]
            )

            current_index = (
                current_index - 1
            ) % len(color_ids)

            settings[setting_key] = (
                color_ids[current_index]
            )

        elif key in (
            curses.KEY_RIGHT,
            ord("d"),
            ord("D"),
        ):

            setting_key = options[selected][1]

            color_ids = [
                color_id
                for _, color_id in COLOR_NAMES
            ]

            current_index = color_ids.index(
                settings[setting_key]
            )

            current_index = (
                current_index + 1
            ) % len(color_ids)

            settings[setting_key] = (
                color_ids[current_index]
            )

        elif key in (
            27,
            ord("b"),
            ord("B"),
        ):

            return


# ============================================================
# PAUSE MENU
# ============================================================

def pause_menu(
    stdscr,
    score,
    high_score,
    settings
):

    selected = 0

    options = [
        "Resume",
        "Options",
        "Restart",
        "Quit",
    ]

    while True:

        height, width = stdscr.getmaxyx()

        _, _, text_color = setup_colors(settings)

        stdscr.erase()

        box_width = min(
            44,
            max(28, width - 4)
        )

        box_height = min(
            17,
            max(10, height - 2)
        )

        start_y = max(
            0,
            (height - box_height) // 2
        )

        start_x = max(
            0,
            (width - box_width) // 2
        )

        # Top
        try:

            stdscr.addstr(
                start_y,
                start_x,
                "╔" + "═" * (box_width - 2) + "╗",
                text_color | curses.A_BOLD
            )

            # Sides
            for y in range(
                start_y + 1,
                start_y + box_height - 1
            ):

                stdscr.addstr(
                    y,
                    start_x,
                    "║",
                    text_color
                )

                stdscr.addstr(
                    y,
                    start_x + box_width - 1,
                    "║",
                    text_color
                )

            # Bottom
            stdscr.addstr(
                start_y + box_height - 1,
                start_x,
                "╚" + "═" * (box_width - 2) + "╝",
                text_color | curses.A_BOLD
            )

        except curses.error:
            pass

        title = "GAME PAUSED"

        try:
            stdscr.addstr(
                start_y + 1,
                start_x
                + (box_width - len(title)) // 2,
                title,
                text_color | curses.A_BOLD
            )
        except curses.error:
            pass

        description = (
            "The game is currently paused."
        )

        try:
            stdscr.addstr(
                start_y + 3,
                start_x
                + (box_width - len(description)) // 2,
                description,
                text_color
            )
        except curses.error:
            pass

        score_text = (
            f"Score: {score}   High Score: {high_score}"
        )

        try:
            stdscr.addstr(
                start_y + 5,
                start_x
                + (box_width - len(score_text)) // 2,
                score_text,
                text_color
            )
        except curses.error:
            pass

        for i, option in enumerate(options):

            y = start_y + 7 + i

            if y >= start_y + box_height - 1:
                continue

            prefix = "> " if i == selected else "  "

            line = prefix + option

            try:

                attr = text_color

                if i == selected:
                    attr |= curses.A_REVERSE

                stdscr.addstr(
                    y,
                    start_x
                    + (box_width - len(line)) // 2,
                    line,
                    attr
                )

            except curses.error:
                pass

        controls = (
            "UP/DOWN = Select    ENTER = Confirm"
        )

        try:
            stdscr.addstr(
                start_y + box_height - 2,
                start_x
                + (box_width - len(controls)) // 2,
                controls,
                text_color
            )
        except curses.error:
            pass

        stdscr.refresh()

        stdscr.timeout(-1)

        key = stdscr.getch()

        if key in (
            curses.KEY_UP,
            ord("w"),
            ord("W"),
        ):

            selected = (
                selected - 1
            ) % len(options)

        elif key in (
            curses.KEY_DOWN,
            ord("s"),
            ord("S"),
        ):

            selected = (
                selected + 1
            ) % len(options)

        elif key in (
            curses.KEY_ENTER,
            10,
            13,
        ):

            if selected == 0:
                return "resume"

            if selected == 1:

                options_menu(
                    stdscr,
                    settings
                )

            elif selected == 2:
                return "restart"

            elif selected == 3:
                return "quit"

        elif key == 27:

            return "resume"


# ============================================================
# GAME
# ============================================================

def play_game(
    stdscr,
    high_score,
    has_high_score,
    settings
):

    height, width = stdscr.getmaxyx()

    if width < 25 or height < 12:

        stdscr.erase()

        message = "Terminal too small."

        try:

            stdscr.addstr(
                height // 2,
                max(
                    0,
                    (width - len(message)) // 2
                ),
                message
            )

            stdscr.refresh()

        except curses.error:
            pass

        stdscr.getch()

        return (
            0,
            high_score,
            has_high_score,
            "quit"
        )

    curses.mousemask(
        curses.ALL_MOUSE_EVENTS
        | curses.REPORT_MOUSE_POSITION
    )

    curses.mouseinterval(0)

    snake_color, apple_color, text_color = (
        setup_colors(settings)
    )

    score = 0

    snake = [
        [height // 2, width // 2 - 2],
        [height // 2, width // 2 - 3],
        [height // 2, width // 2 - 4],
    ]

    direction = curses.KEY_RIGHT

    apples = []

    while len(apples) < 10:

        apple = [
            random.randint(1, height - 2),
            random.randint(1, width - 3),
        ]

        if (
            apple not in snake
            and apple not in apples
        ):

            apples.append(apple)

    mouse_dragging = False

    redraw_game(
        stdscr,
        height,
        width,
        score,
        high_score,
        snake,
        apples,
        snake_color,
        apple_color,
        text_color
    )

    while True:

        speed = max(
            35,
            80 - score * 3
        )

        stdscr.timeout(speed)

        key = stdscr.getch()

        # ====================================================
        # MOUSE
        # ====================================================

        if key == curses.KEY_MOUSE:

            try:

                _, mouse_x, mouse_y, _, state = (
                    curses.getmouse()
                )

                head_y, head_x = snake[0]

                if state & curses.BUTTON1_PRESSED:

                    if (
                        abs(mouse_y - head_y) <= 1
                        and
                        abs(mouse_x - head_x) <= 2
                    ):
                        mouse_dragging = True

                if mouse_dragging:

                    dx = mouse_x - head_x
                    dy = mouse_y - head_y

                    if abs(dx) > abs(dy):

                        if (
                            dx > 0
                            and direction != curses.KEY_LEFT
                        ):
                            direction = curses.KEY_RIGHT

                        elif (
                            dx < 0
                            and direction != curses.KEY_RIGHT
                        ):
                            direction = curses.KEY_LEFT

                    else:

                        if (
                            dy > 0
                            and direction != curses.KEY_UP
                        ):
                            direction = curses.KEY_DOWN

                        elif (
                            dy < 0
                            and direction != curses.KEY_DOWN
                        ):
                            direction = curses.KEY_UP

                if state & curses.BUTTON1_RELEASED:

                    mouse_dragging = False

            except curses.error:
                pass

            continue

        # ====================================================
        # PAUSE
        # ====================================================

        if key == 27:

            result = pause_menu(
                stdscr,
                score,
                high_score,
                settings
            )

            if result == "resume":

                snake_color, apple_color, text_color = (
                    setup_colors(settings)
                )

                redraw_game(
                    stdscr,
                    height,
                    width,
                    score,
                    high_score,
                    snake,
                    apples,
                    snake_color,
                    apple_color,
                    text_color
                )

                continue

            if result == "restart":

                return (
                    0,
                    high_score,
                    has_high_score,
                    "restart"
                )

            if result == "quit":

                return (
                    score,
                    high_score,
                    has_high_score,
                    "quit"
                )

        # ====================================================
        # KEYBOARD MOVEMENT
        # ====================================================

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
            ord("W"),
        ):

            if direction != curses.KEY_DOWN:
                direction = curses.KEY_UP

        elif key in (
            ord("s"),
            ord("S"),
        ):

            if direction != curses.KEY_UP:
                direction = curses.KEY_DOWN

        elif key in (
            ord("a"),
            ord("A"),
        ):

            if direction != curses.KEY_RIGHT:
                direction = curses.KEY_LEFT

        elif key in (
            ord("d"),
            ord("D"),
        ):

            if direction != curses.KEY_LEFT:
                direction = curses.KEY_RIGHT

        # ====================================================
        # MOVE
        # ====================================================

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

        # ====================================================
        # WALL COLLISION
        # ====================================================

        if (
            head[0] <= 0
            or head[0] >= height - 1
            or head[1] <= 0
            or head[1] >= width - 2
        ):

            return (
                score,
                high_score,
                has_high_score,
                "dead"
            )

        # ====================================================
        # SELF COLLISION
        # ====================================================

        if head in snake:

            return (
                score,
                high_score,
                has_high_score,
                "dead"
            )

        snake.insert(0, head)

        # ====================================================
        # EAT APPLE
        # ====================================================

        if head in apples:

            score += 1

            # ------------------------------------------------
            # FIRST SCORE OF SESSION
            # ------------------------------------------------

            if not has_high_score:

                high_score = score

                has_high_score = True

            # ------------------------------------------------
            # NEW HIGH SCORE
            # ------------------------------------------------

            elif score > high_score:

                high_score = score

                snake_color, apple_color, text_color = (
                    setup_colors(settings)
                )

                new_high_score_screen(
                    stdscr,
                    score,
                    text_color
                )

                # Completely redraw everything.
                redraw_game(
                    stdscr,
                    height,
                    width,
                    score,
                    high_score,
                    snake,
                    apples,
                    snake_color,
                    apple_color,
                    text_color
                )

            apples.remove(head)

            # Spawn replacement apple
            while True:

                new_apple = [
                    random.randint(
                        1,
                        height - 2
                    ),
                    random.randint(
                        1,
                        width - 3
                    ),
                ]

                if (
                    new_apple not in snake
                    and new_apple not in apples
                ):

                    apples.append(new_apple)
                    break

            # ------------------------------------------------
            # GROWTH BLINK
            # ------------------------------------------------

            for _ in range(3):

                stdscr.refresh()

                time.sleep(0.05)

                try:

                    for y, x in snake:

                        stdscr.addstr(
                            y,
                            x,
                            "..",
                            text_color
                        )

                except curses.error:
                    pass

                stdscr.refresh()

                time.sleep(0.05)

                draw_snake(
                    stdscr,
                    snake,
                    snake_color
                )

        else:

            snake.pop()

            try:

                stdscr.addstr(
                    old_tail[0],
                    old_tail[1],
                    "..",
                    text_color
                )

            except curses.error:
                pass

        # Refresh colors
        snake_color, apple_color, text_color = (
            setup_colors(settings)
        )

        # ====================================================
        # DRAW SCORE
        # ====================================================

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


# ============================================================
# MAIN
# ============================================================

def main(stdscr):

    curses.curs_set(0)

    curses.mousemask(
        curses.ALL_MOUSE_EVENTS
        | curses.REPORT_MOUSE_POSITION
    )

    curses.mouseinterval(0)

    # Session-only high score
    high_score = 0

    # Prevent the first score from showing
    # the NEW HIGH SCORE screen.
    has_high_score = False

    # Default colors
    settings = {
        "snake": curses.COLOR_BLUE,
        "apple": curses.COLOR_RED,
        "text": curses.COLOR_BLACK,
        "background": curses.COLOR_GREEN,
    }

    # ========================================================
    # MAIN MENU
    # ========================================================

    while True:

        result = main_menu(
            stdscr,
            settings
        )

        if result == "quit":
            return

        # ====================================================
        # GAME LOOP
        # ====================================================

        while True:

            (
                score,
                high_score,
                has_high_score,
                result
            ) = play_game(
                stdscr,
                high_score,
                has_high_score,
                settings
            )

            if result == "restart":
                continue

            if result == "quit":
                return

            # =================================================
            # GAME OVER
            # =================================================

            height, width = stdscr.getmaxyx()

            _, _, text_color = setup_colors(
                settings
            )

            stdscr.erase()

            stdscr.timeout(-1)

            message = (
                f"GAME OVER | Score: {score} | "
                f"High Score: {high_score}"
            )

            controls = (
                "R = Restart    Q = Quit"
            )

            try:

                stdscr.addstr(
                    height // 2 - 1,
                    max(
                        0,
                        (width - len(message)) // 2
                    ),
                    message,
                    text_color | curses.A_BOLD
                )

                stdscr.addstr(
                    height // 2 + 1,
                    max(
                        0,
                        (width - len(controls)) // 2
                    ),
                    controls,
                    text_color
                )

                stdscr.refresh()

            except curses.error:
                pass

            while True:

                key = stdscr.getch()

                if key in (
                    ord("r"),
                    ord("R"),
                ):

                    break

                if key in (
                    ord("q"),
                    ord("Q"),
                ):

                    return


# ============================================================
# START
# ============================================================

curses.wrapper(main)
