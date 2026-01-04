# Battleship Game
import os
import re
import random
import time
from colorama import init, Fore, Style
from wcwidth import wcswidth

# Initialize colorama (cross-platform color support)
init(autoreset=True)


# ========= 1) Welcome Screen =========
class WelcomeScreen:
    """Handles cinematic welcome screen for Battleships."""

    def __init__(self, title_lines, ship_art, width=100):
        self.title_lines = title_lines
        self.ship_art = ship_art
        self.width = width

    # ----- Utility Functions -----
    def strip_ansi(self, text: str) -> str:
        """Remove ANSI escape codes (needed for alignment math)."""
        ansi_escape = re.compile(r"\x1B\[[0-?]*[ -/]*[@-~]")
        return ansi_escape.sub("", text)

    def center_text(self, text: str, color: str = "") -> str:
        """Return centered text with optional color applied."""
        clean_text = self.strip_ansi(text)
        pad = (self.width - wcswidth(clean_text)) // 2
        return " " * pad + color + text + Style.RESET_ALL

    def gradient_line(self, text: str) -> str:
        """Apply rainbow gradient across one line of text."""
        colors = [
            Fore.RED, Fore.MAGENTA, Fore.BLUE,
            Fore.CYAN, Fore.GREEN, Fore.YELLOW,
        ]
        n = len(text)
        gradient = ""
        for i, ch in enumerate(text):
            color = colors[int((i / max(1, n - 1)) * (len(colors) - 1))]
            gradient += color + ch
        return gradient + Style.RESET_ALL

    # ----- Title -----
    def show_title(self):
        """Show rainbow ASCII title and tagline."""
        os.system("cls" if os.name == "nt" else "clear")
        print("\n")
        for line in self.title_lines:
            print(self.center_text(self.gradient_line(line)))
        print("\n")

        tagline = "⚓  Command Center Online — Prepare for Battle  ⚓"
        line = Fore.YELLOW + "═" * self.width + Style.RESET_ALL
        print(line)
        print(self.center_text(tagline, color=Style.BRIGHT + Fore.CYAN))
        print(line)
        print("\n")

    # ----- Ship Art -----
    def show_ship(self):
        """Show green ASCII ship centered on screen."""
        for line in self.ship_art.splitlines():
            if line.strip():
                print(self.center_text(line, color=Fore.GREEN))
        print("\n" + Fore.YELLOW + "═" * self.width + Style.RESET_ALL)

    # ----- Player Inputs -----
    def get_inputs(self):
        """Ask player for grid size (8–15) and number of ships (1–5)."""
        print("\n")

        # Ask for grid size
        while True:
            size_str = input(
                self.center_text(
                    "Enter grid size (8–15) [default = 8]: ",
                    color=Fore.CYAN,
                )
            ).strip()
            size = 8 if size_str == "" else None
            if size_str.isdigit():
                size = int(size_str)
            if size and 8 <= size <= 15:
                break
            print(
                self.center_text(
                    "❌ Grid size must be 8–15.",
                    color=Fore.RED,
                )
            )

        # Ask for number of ships
        while True:
            ships_str = input(
                self.center_text(
                    "Enter number of ships (1–5) [default = 3]: ",
                    color=Fore.CYAN,
                )
            ).strip()
            ships = 3 if ships_str == "" else None
            if ships_str.isdigit():
                ships = int(ships_str)
            if ships and 1 <= ships <= 5:
                break
            print(
                self.center_text(
                    "❌ Ships must be 1–5.",
                    color=Fore.RED,
                )
            )

        print("\n")
        return size, ships

    # ----- Mission Briefing -----
    def mission_briefing(self, size, ships):
        """Show cinematic mission briefing with rules & emojis."""
        print(
            self.center_text(
                Fore.YELLOW + Style.BRIGHT +
                "📡 Incoming Transmission..." +
                Style.RESET_ALL
            )
        )
        print("-" * self.width)
        time.sleep(0.5)

        # Mission intro text
        paragraphs = [
            Fore.CYAN +
            "Welcome, Commander. Enemy fleets lurk beyond the horizon..."
            + Style.RESET_ALL,
            f"The tactical grid is {size}×{size} sectors "
            f"(rows A–{chr(64 + size)}, columns 1–{size}).",
            f"Your fleet has deployed {ships} battleships to these waters.",
            "Enemy ships are hidden. Hunt them down with precision fire!",
        ]
        for p in paragraphs:
            print(self.center_text(p))
            time.sleep(0.2)

        # Tactical orders
        print("\n" + self.center_text(
            Fore.MAGENTA + "🎯 TACTICAL ORDERS" + Style.RESET_ALL
        ) + "\n")
        tactical_orders = [
            "• Enter strike coordinates such as A1, C7, or H8",
            f"• Radar symbols:  {HIT} Direct hit on enemy ship",
            f"            {MISS} Splash! Shot missed",
            f"          {WATER} Untouched waters",
            f"              {SHIP_CHAR} Your ship positions (your radar only)",
        ]
        for line in tactical_orders:
            print(self.center_text(line))
            time.sleep(0.15)

        # Rules of engagement
        print("\n" + self.center_text(
            Fore.YELLOW + "⚔️  RULES OF ENGAGEMENT" + Style.RESET_ALL
        ) + "\n")
        rules = [
            "• Turns alternate — one strike per side.",
            "     • Victory: Destroy the enemy fleet.",
            "     • Defeat: All your ships are sunk.",
        ]
        for line in rules:
            print(self.center_text(line))
            time.sleep(0.15)

        # Closing line
        print("\n" + self.center_text(
            "Stay sharp, Commander. The fate of the fleet rests "
            "in your hands."
        ) + "\n")

        # Footer prompt
        print("-" * self.width)
        print(
            Fore.GREEN + Style.BRIGHT +
            "▶ Press Enter to deploy your fleet... ◀".center(self.width) +
            Style.RESET_ALL
        )
        input()
        clear_screen()


# ========= 2) Battleship Game =========
# Emoji constants
WATER = "🌊"
MISS = "💦"
HIT = "💥"
SHIP_CHAR = "🚢"

LEFT_TITLE = "Enemy Fleet"
RIGHT_TITLE = "Your Fleet"
CELL_VISUAL = 3
GAP_BETWEEN_BOARDS = " " * 8


def clear_screen():
    """Clear terminal window (Windows & Unix)."""
    os.system("cls" if os.name == "nt" else "clear")


def strip_ansi(s: str) -> str:
    """Strip ANSI color codes (fixes alignment math)."""
    return re.sub(r"\x1b\[[0-9;]*m", "", s)


def pad_visual(s: str, width: int) -> str:
    """Pad text so visual width matches width (handles emoji)."""
    vis = wcswidth(strip_ansi(s))
    if vis < 0:
        vis = len(strip_ansi(s))
    return s + " " * max(0, width - vis)


def format_cell(symbol: str) -> str:
    """Return one cell padded to CELL_VISUAL columns."""
    return pad_visual(symbol, CELL_VISUAL)


def build_board_block(title_text: str,
                      grid_rows: list[list[str]]) -> list[str]:
    """Build one framed board with title, numbers, rows, and border."""
    size = len(grid_rows)
    inner_width = 3 + (size * CELL_VISUAL)
    lines = []

    # Top border with centered title
    label = f" {title_text} "
    spare = inner_width - len(strip_ansi(label))
    left = max(0, spare // 2)
    right = max(0, spare - left)
    lines.append("┌" + ("─" * left) + label + ("─" * right) + "┐")

    # Number header
    nums = "".join(format_cell(str(i)) for i in range(1, size + 1))
    lines.append("│" + "   " + nums + "│")

    # Grid rows
    for r in range(size):
        row_label = chr(65 + r)  # A, B, C...
        row_cells = "".join(format_cell(ch) for ch in grid_rows[r])
        content = f"{row_label}  {row_cells}"
        content = pad_visual(content, inner_width)
        lines.append("│" + content + "│")

    # Bottom border
    lines.append("└" + ("─" * inner_width) + "┘")
    return lines


def display_boards(enemy_view: list[list[str]],
                   player_board: list[list[str]]):
    """Print enemy + player boards side-by-side."""
    left_block = build_board_block(LEFT_TITLE, enemy_view)
    right_block = build_board_block(RIGHT_TITLE, player_board)
    for lft, rgt in zip(left_block, right_block):
        print(lft + GAP_BETWEEN_BOARDS + rgt)


class BattleshipGame:
    """Main Battleship game logic (turns, ships, status)."""

    def __init__(self, size=8, num_ships=3, title_lines=None):
        self.size = size
        self.num_ships = num_ships
        self.enemy_view = [[WATER] * size for _ in range(size)]
        self.player_board = [[WATER] * size for _ in range(size)]
        self.enemy_ships = self._place_ships()
        self.player_ships = self._place_ships(reveal=True)
        self.enemy_tried = set()
        self.total_player_shots = 0
        self.total_enemy_shots = 0
        self.player_msg = ""
        self.enemy_msg = ""
        self.title_lines = title_lines or []

    def _place_ships(self, reveal=False):
        """Randomly place ships (reveal=True shows on player board)."""
        ships = set()
        while len(ships) < self.num_ships:
            r = random.randint(0, self.size - 1)
            c = random.randint(0, self.size - 1)
            ships.add((r, c))
        if reveal:
            for r, c in ships:
                self.player_board[r][c] = SHIP_CHAR
        return ships

    def _print_ascii_banner(self):
        """Print the ASCII 'BATTLESHIPS' banner above boards."""
        board_width = 3 + (self.size * CELL_VISUAL)
        total_width = (board_width * 2) + len(GAP_BETWEEN_BOARDS)
        for line in self.title_lines:
            print(line.center(total_width))
        print()  # one blank line after banner

    def play(self):
        """Main loop: player turn, then enemy turn."""
        while self.player_ships and self.enemy_ships:
            clear_screen()

            # Show banner and boards
            self._print_ascii_banner()
            display_boards(self.enemy_view, self.player_board)

            # Status bar for player turn
            self._show_status(current_turn="Player")

            # Player turn
            self._player_turn()
            if not self.enemy_ships:
                break

            # Enemy turn
            self.enemy_msg = self._enemy_turn()

            clear_screen()

            # Show banner and boards again
            self._print_ascii_banner()
            display_boards(self.enemy_view, self.player_board)

            # Status bar for enemy turn
            self._show_status(current_turn="Enemy")

        # End screen
        self._end_screen()

    def _player_turn(self):
        """Ask player for input and resolve strike."""
        guess = input(
            Fore.YELLOW + "\nEnter position (e.g., A1) or Q to quit: "
            + Style.RESET_ALL
        ).strip().upper()

        if guess == "Q":
            clear_screen()
            print("👋 Game ended by user.")
            exit()

        if len(guess) < 2:
            self.player_msg = "❌ Format must be Letter+Number (e.g., A1)."
            return

        row_letter, digits = guess[0], guess[1:]
        if not digits.isdigit():
            self.player_msg = "❌ Column must be a number (e.g., A1)."
            return

        r = ord(row_letter) - 65
        c = int(digits) - 1
        if not (0 <= r < self.size and 0 <= c < self.size):
            self.player_msg = (
                f"❌ Coordinates must be A–{chr(64 + self.size)} "
                f"+ 1–{self.size}."
            )
            return

        if self.enemy_view[r][c] in (MISS, HIT):
            self.player_msg = "⚠️ Already tried that sector."
            return

        self.total_player_shots += 1
        if (r, c) in self.enemy_ships:
            self.enemy_view[r][c] = HIT
            self.enemy_ships.remove((r, c))
            self.player_msg = (
                f"💥 Direct Hit! Enemy ship damaged at {row_letter}{c+1}!"
            )
        else:
            self.enemy_view[r][c] = MISS
            self.player_msg = (
                f"💦 Torpedo missed at {row_letter}{c+1}, enemy evaded!"
            )

    def _enemy_turn(self):
        """Enemy AI randomly fires at player fleet."""
        while True:
            r = random.randint(0, self.size - 1)
            c = random.randint(0, self.size - 1)
            if (r, c) not in self.enemy_tried:
                self.enemy_tried.add((r, c))
                break
        self.total_enemy_shots += 1
        pos = f"{chr(65+r)}{c+1}"
        if (r, c) in self.player_ships:
            self.player_board[r][c] = HIT
            self.player_ships.remove((r, c))
            return f"💥 Enemy fires at {pos} — Direct Hit!"
        self.player_board[r][c] = MISS
        return f"💦 Enemy fires at {pos} — Torpedo missed, you evaded!"

    def enemy_turn(self):
        """
        Web-compatible enemy turn wrapper.
        Flask route se call hota hai.
        """
        if not self.player_ships:
            return

        self.enemy_msg = self._enemy_turn()

    def player_turn(self, guess: str):
        """
        Web-compatible player turn.
        Accepts a position like 'A1' instead of using input().
        """
        self.player_msg = ""

        guess = (guess or "").strip().upper()

        if len(guess) < 2:
            self.player_msg = "❌ Format must be Letter+Number (e.g., A1)."
            return

        row_letter, digits = guess[0], guess[1:]

        if not digits.isdigit():
            self.player_msg = "❌ Column must be a number (e.g., A1)."
            return

        r = ord(row_letter) - 65
        c = int(digits) - 1

        if not (0 <= r < self.size and 0 <= c < self.size):
            self.player_msg = (
                f"❌ Coordinates must be A–{chr(64 + self.size)} "
                f"+ 1–{self.size}."
            )
            return

        if self.enemy_view[r][c] in (MISS, HIT):
            self.player_msg = "⚠️ Already tried that sector."
            return

        self.total_player_shots += 1

        if (r, c) in self.enemy_ships:
            self.enemy_view[r][c] = HIT
            self.enemy_ships.remove((r, c))
            self.player_msg = f"💥 Hit at {row_letter}{c + 1}!"
        else:
            self.enemy_view[r][c] = MISS
            self.player_msg = f"💦 Miss at {row_letter}{c + 1}."

    def _show_status(self, current_turn="Player"):
        """Show compact status bar and last turn results with colors."""
        enemy_left = len(self.enemy_ships)
        player_left = len(self.player_ships)

        player_bar = (
            " ".join([SHIP_CHAR] * player_left)
            if player_left else "—"
        )

        enemy_bar = (
            " ".join([SHIP_CHAR] * enemy_left)
            if enemy_left else "—"
        )

        # Turn indicator with color
        if current_turn == "Player":
            turn_text = Fore.CYAN + "🎯 Turn: Player" + Style.RESET_ALL
        else:
            turn_text = Fore.MAGENTA + "👾 Turn: Enemy" + Style.RESET_ALL

        # Compact status bar
        print(
            f"{turn_text} | "
            f"Enemy ships: {enemy_left} {enemy_bar} | "
            f"Your ships: {player_left} {player_bar}"
        )
        print(
            f"Shots — Player: {self.total_player_shots} | "
            f"Enemy: {self.total_enemy_shots}"
        )
        print()

        # Flavor messages
        if self.player_msg:
            print(Fore.CYAN + self.player_msg + Style.RESET_ALL)
        if self.enemy_msg:
            print(Fore.MAGENTA + self.enemy_msg + Style.RESET_ALL)

        # Legend footer
        legend = (
            f"{HIT}=Hit   {MISS}=Miss   "
            f"{WATER}=Water   {SHIP_CHAR}=Player"
        )
        print("\n" + Fore.YELLOW + "Legend: " + Style.RESET_ALL + legend)

    def _end_screen(self):
        """Final victory or defeat screen."""
        clear_screen()
        if self.enemy_ships and not self.player_ships:
            print("💀 Game Over: All your ships sunk.")
        elif self.player_ships and not self.enemy_ships:
            print("🏆 Victory: All enemy ships sunk! 🎉")


# ========= 3) Run Game =========
if __name__ == "__main__":
    title_lines = [
        ("██████   █████  ████████ ████████ ██      ███████ ███████ "
         "██   ██ ██ ██████  ███████"),
        ("██   ██ ██   ██    ██       ██    ██      ██      ██      "
         "██   ██ ██ ██   ██ ██     "),
        ("██████  ███████    ██       ██    ██      █████   ███████ "
         "███████ ██ ██████  ███████"),
        ("██   ██ ██   ██    ██       ██    ██      ██           ██ "
         "██   ██ ██ ██           ██"),
        ("██████  ██   ██    ██       ██    ███████ ███████ ███████ "
         "██   ██ ██ ██      ███████"),
    ]

    ship_art = r"""
⣠⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠰⠶⢿⡶⠦⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⢀⣀⣿⣿⣿⣿⣿⣿⡇⢀⠀⢀⡀⠀⣀⣀⣠⣀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠉⠻⠿⣿⣿⣿⣿⣿⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣶⣿⣿⣶⣶⣾⣧⣤⣴⣆⣀⢀⣤⡄⠀⠀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
"""

    # Run cinematic welcome
    ws = WelcomeScreen(title_lines, ship_art, width=100)
    ws.show_title()
    ws.show_ship()
    size, ships = ws.get_inputs()
    ws.mission_briefing(size, ships)

    # Start the game
    game = BattleshipGame(size=size, num_ships=ships, title_lines=title_lines)
    game.play()
