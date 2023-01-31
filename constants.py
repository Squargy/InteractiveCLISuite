from enum import Enum, IntEnum

class KEY:
    CTRLC = b'\x03'
    DOWN = b'P'
    ENTER = b'\r'
    SPACE = b' '
    UP = b'H'

class DIRECTION(IntEnum):
    UP = -1
    DOWN = 1

class ARG_SOURCE(Enum):
    ARGS = 0
    VALUE = 1
    TEXT = 2

class ANSI_COLORS:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    BLACK = '\u001b[30m'
    RED = '\u001b[31m'
    GREEN = '\u001b[32m'
    YELLOW = '\u001b[33m'
    BLUE = '\u001b[34m'
    MAGENTA = '\u001b[35m'
    CYAN = '\u001b[36m'
    WHITE = '\u001b[37m'
    RESET = '\u001b[0m'
    BRIGHT_BLACK = '\u001b[30;1m'
    BRIGHT_RED = '\u001b[31;1m'
    BRIGHT_GREEN = '\u001b[32;1m'
    BRIGHT_YELLOW = '\u001b[33;1m'
    BRIGHT_BLUE = '\u001b[34;1m'
    BRIGHT_MAGENTA = '\u001b[35;1m'
    BRIGHT_CYAN = '\u001b[36;1m'
    BRIGHT_WHITE = '\u001b[37;1m'