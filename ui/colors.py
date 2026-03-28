# Color utilities
from colorama import Fore, Style, init
init(autoreset=True)

def success(message):
    print(f"{Fore.GREEN}{message}{Style.RESET_ALL}")

def error(message):
    print(f"{Fore.RED}{message}{Style.RESET_ALL}")

def warning(message):
    print(f"{Fore.YELLOW}{message}{Style.RESET_ALL}")

def info(message):
    print(f"{Fore.CYAN}{message}{Style.RESET_ALL}")

def header(message):
    print(f"{Style.BRIGHT}{message}{Style.RESET_ALL}")

def section(message):
    print(f"{Fore.BLUE}{Style.BRIGHT}{message}{Style.RESET_ALL}")

def input_prompt(message):
    print(f"{Fore.CYAN}{message}{Style.RESET_ALL}", end=" ")

def menu_item(number, text):
    print(f"  {Fore.CYAN}{number}.{Style.RESET_ALL} {text}")

def separator(char="─", length=50):
    print(f"{Style.DIM}{char * length}{Style.RESET_ALL}")
