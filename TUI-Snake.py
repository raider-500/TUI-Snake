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
# COLORS
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
        curses.color_pair(3)
    )


# ============================================================
# GRID
# ============================================================

def draw_grid(stdscr, height, width, text_color):
    for y in range(1, height - 1):
        for x in range(1, width - 2):
            try:
                stdscr.addch(
                    y,
                    x,
                    ".",
                    text_color
                )
            except curses.error:
                pass


# ============================================================
# SNAKE
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
# APPLES
# ============================================================

def draw_apples(stdscr, apples, apple_color):
    height, width = stdscr.getmaxyx()

    for y, x in apples:

        if (
            0 < y < height - 1
            and 0 < x < width - 2
        ):

            try:
                stdscr.addstr(
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
# FORMAT TIMER
# ============================================================

def format_time(seconds):
    seconds = int(seconds)

    minutes = seconds // 60
    seconds = seconds % 60

    return f"{minutes:02d}:{seconds:02d}"


# ============================================================
# GAME DRAW
# ============================================================

def redraw_game(
    stdscr,
    height,
    width,
    score,
    high_score,
    snake,
    apples,
    settings,
    elapsed_time,
    show_high_score
):
    snake_color, apple_color, text_color = (
        setup_colors(settings)
    )

    stdscr.bkgd(" ", text_color)
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

        timer_text = format_time(elapsed_time)

        score_text = (
            f" Score: {score} | "
            f"High Score: {high_score} | "
            f"Time: {timer_text} "
        )

        if show_high_score:
            score_text += "| NEW HIGH SCORE! "

        stdscr.addstr(
            0,
            2,
            score_text,
            text_color | curses.A_BOLD
        )

    except curses.error:
        pass

    draw_apples(
        stdscr,
        apples,
        apple_color
    )

    draw_snake(
        stdscr,
        snake,
        snake_color
    )

    stdscr.refresh()


# ============================================================
# MAIN MENU
# ============================================================

def main_menu(stdscr, settings):
    height, width = stdscr.getmaxyx()

    curses.init_pair(
        10,
        settings["text"],
        settings["background"]
    )

    menu_color = curses.color_pair(10)

    stdscr.bkgd(" ", menu_color)
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

    # Title
    for i, line in enumerate(title):

        y = start_y + i

        x = max(
            0,
            (width - len(line)) // 2
        )

        try:
            stdscr.addstr(
                y,
                x,
                line,
                menu_color | curses.A_BOLD
            )
        except curses.error:
            pass

    # Subtitle
    subtitle = "Terminal Snake"

    try:
        stdscr.addstr(
            start_y + 7,
            max(
                0,
                (width - len(subtitle)) // 2
            ),
            subtitle,
            menu_color
        )
    except curses.error:
        pass

    # Play button
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
                menu_color | curses.A_BOLD
            )
        except curses.error:
            pass

    # Controls
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
            menu_color
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
# OPTIONS
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

        curses.init_pair(
            10,
            settings["text"],
            settings["background"]
        )

        menu_color = curses.color_pair(10)

        stdscr.bkgd(" ", menu_color)
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
                menu_color | curses.A_BOLD
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
                menu_color
            )
        except curses.error:
            pass

        for i, (name, setting_key) in enumerate(options):

            y = 7 + i * 2

            color_name = "Unknown"

            for name_value, color_id in COLOR_NAMES:

                if color_id == settings[setting_key]:
                    color_name = name_value
                    break

            prefix = "> " if i == selected else "  "

            line = (
                f"{prefix}{name}: {color_name}"
            )

            try:

                attr = menu_color

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
                menu_color
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

            colors = [
                color_id
                for _, color_id in COLOR_NAMES
            ]

            current = colors.index(
                settings[setting_key]
            )

            current = (
                current - 1
            ) % len(colors)

            settings[setting_key] = colors[current]

        elif key in (
            curses.KEY_RIGHT,
            ord("d"),
            ord("D"),
        ):

            setting_key = options[selected][1]

            colors = [
                color_id
                for _, color_id in COLOR_NAMES
            ]

            current = colors.index(
                settings[setting_key]
            )

            current = (
                current + 1
            ) % len(colors)

            settings[setting_key] = colors[current]

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

        curses.init_pair(
            10,
            settings["text"],
            settings["background"]
        )

        menu_color = curses.color_pair(10)

        stdscr.bkgd(" ", menu_color)
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
                menu_color | curses.A_BOLD
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
                    menu_color
                )

                stdscr.addstr(
                    y,
                    start_x + box_width - 1,
                    "║",
                    menu_color
                )

            # Bottom
            stdscr.addstr(
                start_y + box_height - 1,
                start_x,
                "╚" + "═" * (box_width - 2) + "╝",
                menu_color | curses.A_BOLD
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
                menu_color | curses.A_BOLD
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
                menu_color
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
                menu_color
            )

        except curses.error:
            pass

        for i, option in enumerate(options):

            y = start_y + 7 + i

            prefix = "> " if i == selected else "  "

            line = prefix + option

            try:

                attr = menu_color

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
                menu_color
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

            elif selected == 1:

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

    if width < 30 or height < 12:

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

    # Enable mouse
    curses.mousemask(
        curses.ALL_MOUSE_EVENTS
        | curses.REPORT_MOUSE_POSITION
    )

    curses.mouseinterval(0)

    # ========================================================
    # GAME VARIABLES
    # ========================================================

    score = 0

    # Timer starts when the game starts.
    game_start_time = time.monotonic()

    # Timestamp until the high-score notification stays visible.
    new_high_score_until = 0

    snake = [
        [height // 2, width // 2 - 2],
        [height // 2, width // 2 - 3],
        [height // 2, width // 2 - 4],
    ]

    direction = curses.KEY_RIGHT

    apples = []

    # Create 10 apples.
    while len(apples) < 10:

        apple = [
            random.randint(1, height - 2),
            random.randint(1, width - 3)
        ]

        if (
            apple not in snake
            and apple not in apples
        ):

            apples.append(apple)

    mouse_dragging = False

    # Initial draw
    redraw_game(
        stdscr,
        height,
        width,
        score,
        high_score,
        snake,
        apples,
        settings,
        0,
        False
    )

    # ========================================================
    # GAME LOOP
    # ========================================================

    while True:

        # Faster as score increases.
        speed = max(
            30,
            85 - score * 3
        )

        stdscr.timeout(speed)

        key = stdscr.getch()

        # ====================================================
        # MOUSE DRAGGING
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

            # Save timer before pause.
            pause_start = time.monotonic()

            result = pause_menu(
                stdscr,
                score,
                high_score,
                settings
            )

            # Keep the timer from counting paused time.
            pause_duration = (
                time.monotonic() - pause_start
            )

            game_start_time += pause_duration

            if result == "resume":

                elapsed_time = (
                    time.monotonic()
                    - game_start_time
                )

                redraw_game(
                    stdscr,
                    height,
                    width,
                    score,
                    high_score,
                    snake,
                    apples,
                    settings,
                    elapsed_time,
                    time.monotonic()
                    < new_high_score_until
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
        # ARROW KEYS
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

        # ====================================================
        # WASD
        # ====================================================

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
        # APPLE
        # ====================================================

        if head in apples:

            score += 1

            # First score of the session.
            # Establish the first high score silently.
            if not has_high_score:

                high_score = score
                has_high_score = True

            # Existing high score beaten.
            elif score > high_score:

                high_score = score

                # Show "NEW HIGH SCORE!" beside HUD
                # for 1.5 seconds.
                new_high_score_until = (
                    time.monotonic() + 1.5
                )

            apples.remove(head)

            # Spawn another apple.
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

            # Snake growth blink.
            for _ in range(3):

                snake_color, apple_color, text_color = (
                    setup_colors(settings)
                )

                stdscr.refresh()

                time.sleep(0.05)

                for y, x in snake:

                    try:

                        stdscr.addstr(
                            y,
                            x,
                            "  ",
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

            snake_color, apple_color, text_color = (
                setup_colors(settings)
            )

            try:

                stdscr.addstr(
                    old_tail[0],
                    old_tail[1],
                    "..",
                    text_color
                )

            except curses.error:
                pass

        # ====================================================
        # REDRAW HUD + GAME
        # ====================================================

        elapsed_time = (
            time.monotonic()
            - game_start_time
        )

        show_high_score = (
            time.monotonic()
            < new_high_score_until
        )

        redraw_game(
            stdscr,
            height,
            width,
            score,
            high_score,
            snake,
            apples,
            settings,
            elapsed_time,
            show_high_score
        )


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

    # Session-only high score.
    high_score = 0

    # Prevent the first score from triggering
    # the NEW HIGH SCORE notification.
    has_high_score = False

    # Default configuration.
    settings = {
        "snake": curses.COLOR_BLUE,
        "apple": curses.COLOR_RED,
        "text": curses.COLOR_BLACK,
        "background": curses.COLOR_GREEN,
    }

    # ========================================================
    # MAIN MENU LOOP
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

            curses.init_pair(
                10,
                settings["text"],
                settings["background"]
            )

            game_over_color = curses.color_pair(10)

            stdscr.bkgd(
                " ",
                game_over_color
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
                    game_over_color | curses.A_BOLD
                )

                stdscr.addstr(
                    height // 2 + 1,
                    max(
                        0,
                        (width - len(controls)) // 2
                    ),
                    controls,
                    game_over_color
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
