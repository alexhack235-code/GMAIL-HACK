# utils.py
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

def print_colored(text: str, color: str = "RESET"):
    """Prints text with specified color."""
    colors = {
        "RED": Fore.RED,
        "GREEN": Fore.GREEN,
        "YELLOW": Fore.YELLOW,
        "BLUE": Fore.BLUE,
        "CYAN": Fore.CYAN,
        "MAGENTA": Fore.MAGENTA,
        "WHITE": Fore.WHITE,
        "RED_BRIGHT": Fore.LIGHTRED_EX,
        "GREEN_BRIGHT": Fore.LIGHTGREEN_EX,
        "YELLOW_BRIGHT": Fore.LIGHTYELLOW_EX,
        "BLUE_BRIGHT": Fore.LIGHTBLUE_EX,
        "CYAN_BRIGHT": Fore.LIGHTCYAN_EX,
        "MAGENTA_BRIGHT": Fore.LIGHTMAGENTA_EX,
        "RESET": Fore.RESET
    }
    # Map simple names to potentially brighter colors for more impact
    color_map = {
        "RED": Fore.RED, "GREEN": Fore.GREEN, "YELLOW": Fore.YELLOW, "BLUE": Fore.BLUE,
        "CYAN": Fore.CYAN, "MAGENTA": Fore.MAGENTA, "WHITE": Fore.WHITE, "RESET": Fore.RESET
    }

    color_code = colors.get(color.upper(), Fore.RESET)
    print(f"{color_code}{text}{Style.RESET_ALL}")