# System configuration constants
ROBOT_IP = '192.168.1.126'
MAZE_SIZE = 7              # in squares
START_SELECT = "ROBOT"      # ROBOT / HUMAN
DEBUG_MODE = True           # If True doesn't use the robot
COIN_PERCENTAGE = 0        # To use the coin when no option is available. 0> No use, 100> Always use
PRE_NEG_CHOICES = 2
AUTO_MODE = False           # Autopilot mode that will move automatically if there is no other choice
SHOW_EXIT = True            # If True, it will show a sign on the exit block
R_SAME_CNT = 3              # Number of same actions it turns to auto mode
MAX_DISPLAY_LINES = 10

# Robot configuration constants
TIME_TURN = 1
TIME_STRAIGHT = 0.5
TILT_SPEED = 30
PAN_SPEED = 40

# Menu Selection
MENU_INITIAL = "0"
MENU_DEBUG = "1"
MENU_VS = "2"
MENU_COOP = "3"

# Menu Options
OPTION_QUIT = "q"
OPTION_DEBUG = "1"
OPTION_VS = "2"
OPTION_COOP = "3"

# Game modes
MODE_VS = "VS"
MODE_COOP = "COOP"
MODE_FINISH = "FINISH"

# Debug Options
DEBUG_FWD = "1a"
DEBUG_RIGHT = "1b"
DEBUG_BACK = "1c"
DEBUG_LEFT = "1d"
DEBUG_LEDS = "2"
DEBUG_SOUND = "3"
DEBUG_TALK = "4"
DEBUG_FACES = "5"
DEBUG_TILT = "6"
DEBUG_PAN = "7"
DEBUG_HELLO = "8"
DEBUG_QUIT = "q"

# Robot Movements
R_MOVE_FWD = "0"
R_MOVE_RIGHT = "1"
R_MOVE_BACK = "2"
R_MOVE_LEFT = "3"
R_MOVE_CIRCLE = "4"

# Player Movements
PLAYER_UP = "UP"
PLAYER_RIGHT = "RIGHT"
PLAYER_DOWN = "DOWN"
PLAYER_LEFT = "LEFT"
PLAYER_NONE = "NONE"

# Maze block status
BLOCK_UNKNOWN = 0
BLOCK_CURRENT = 1
BLOCK_PASS = 2
BLOCK_DISCARD = 3
BLOCK_SOLUTION = 4
BLOCK_CONFLICT = 5

# Wall positions
WALL_TOP = 0
WALL_RIGHT = 1
WALL_BOTTOM = 2
WALL_LEFT = 3

# Graphics
WALL_THICK = 0.1
MAZE_SHIFT_Y = 100
SCREEN_FACES_LENGTH = 500

# Player emotions
EMOTION_ANGRY = "(1)Angry"
EMOTION_BAD = "(2)Bad"
EMOTION_NEUTRAL = "(3)Neutral"
EMOTION_SMILE = "(4)Smile"
EMOTION_HAPPY = "(5)Happy"

# Turns
TURN_ROBOT = "ROBOT"
TURN_PLAYER = "HUMAN"
TURN_AUTO = "AUTO"

# Robot situations
R_SIT_START = "0"
R_SIT_DEAD_END = "1a"
R_SIT_WIN = "1b"
R_SIT_MOVING = "1c"
R_SIT_BACKTRACK = "1d"
R_SIT_WAITING = "1e"
R_SIT_DECIDE = "1f"
R_NEG_WAITING = "Waiting input"
R_NEG_AGREE = "Both Agree"
R_NEG_YIELD = "Robot Yield"
R_NEG_COIN = "Coin Toss"
R_NEG_LOSE = "Robot Loses"
R_NEG_WIN = "Robot Wins"
R_NEG_RND_1 = "2d"
R_NEG_RND_2 = "3d"
R_NEG_RND_3 = "4e"
R_AGREE = "5"
R_SAME_CHOICE = "6"

# Player situations
P_NEG_CH1 = "Choice 1"
P_NEG_CH2 = "Choice 2"
P_NEG_CH3 = "Choice 3"
P_NEG_COIN = 3
P_NEG_YIELD = 4

# Negotiation Stages
NEG_STAGE_NONE = "Idle"
NEG_STAGE_START = "Start of Negotiation"
NEG_STAGE_1 = "Negotiation First Round"
NEG_STAGE_2 = "Negotiation Second Round"
NEG_STAGE_AGREE = "Agreement"

# Robot counter message array positions
C_WAITING = 0
C_MOVEMENT = 1
C_AGREEMENT = 2
C_TURN = 3
