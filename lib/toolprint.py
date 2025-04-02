from lib.colorprint import format_string


INFO_PREFIX    = "[*]"
WARN_PREFIX    = "[!]"
ERR_PREFIX     = "[-]"
SUCCESS_PREFIX = "[+]"

def print_info(message: str):
    print(f"{format_string(INFO_PREFIX, foreground='blue')} {message}")

def print_warn(message: str):
    print(f"{format_string(WARN_PREFIX, foreground='yellow')} {message}")

def print_err(message: str):
    print(f"{format_string(ERR_PREFIX, foreground='red')} {message}")

def print_success(message: str):
    print(f"{format_string(SUCCESS_PREFIX, foreground='green')} {message}")
