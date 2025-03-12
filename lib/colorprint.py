from enum import Enum

CTRL_SEQ = "\033["
RESET = "\033[0m"

class IntensityCode(Enum):
    bold             = 1
    faint            = 2
    italic           = 3
    underline        = 4

class ColorCode(Enum):
    black          = 30
    red            = 31
    green          = 32
    yellow         = 33
    blue           = 34
    magenta        = 35
    cyan           = 36
    white          = 37
    bright_black   = 90
    bright_red     = 91
    bright_green   = 92
    bright_yellow  = 93
    bright_blue    = 94
    bright_magenta = 95
    bright_cyan    = 96
    bright_white   = 97

def _get_color(string: str):
    return ColorCode[string].value

def _get_intensity(string: str):
    return IntensityCode[string].value

def _create_sequence(foreground, background, intensity) -> str:
    out = CTRL_SEQ
    if foreground:
        out += str(_get_color(foreground)) + ";"
    if background:
        out += str(_get_color(background) + 10) + ";"
    if intensity:
        out += str(_get_intensity(intensity)) + ";"
    out += out[:-1] + "m"

    return out

def format_string(string: str, foreground="", background="", intensity="") -> str:
    if foreground and not _get_color(foreground):
        raise ValueError(f"{foreground} is not a valid color")
    if background and not _get_color(background):
        raise ValueError(f"{background} is not a valid color")
    if intensity and not _get_intensity(intensity):
        raise ValueError(f"{intensity} is not a valid intensity")
    
    sequence = _create_sequence(foreground, background, intensity)
    return f"{sequence}{string}{RESET}"
