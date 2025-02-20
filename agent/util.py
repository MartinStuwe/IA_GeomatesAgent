from enum import Enum

class AgentType(Enum):
    UNKNOWN = 0
    DISC = 1
    RECT = 2

NO_ACT_KEY = "o"
UP_KEY = "w"
DOWN_KEY = "s"
LEFT_KEY = "a"
RIGHT_KEY = "d"

VALID_KEY_LIST = [UP_KEY, DOWN_KEY, LEFT_KEY, RIGHT_KEY]