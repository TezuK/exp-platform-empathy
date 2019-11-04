# ----------------------------------------
#     System configuration parameters
# ----------------------------------------
ROBOT_IP = '192.168.1.126'
MAZE_SIZE = 7               # in squares
START_SELECT = "ROBOT"      # ROBOT / HUMAN
TIME_LIMIT = 10             # Time limit (in minutes) for the challenge, if it meets then the test ends
FIXED_MAP = 1               # Use the predetermined maps. 0 => Random, 1 or 2 for defined in maze_def.py
DEBUG_MODE = True          # If True doesn't use the robot
DEBUG_TIME = 0.75           # Sleep time on debug mode
SHOW_ALL = False            # If True, show the whole map
SHOW_ADJACENT = False       # If True, show the adjacent blocks
SHOW_EXIT = True            # If True, it will show a sign on the exit block
COIN_PERCENTAGE = 50        # To use the coin when no option is available. 0> No use, 100> Always use
PRE_NEG_CHOICES = 2
COUNT_SAME_DEC = True       # If True, increments the decision counter for the one that suggested it first
                            # in negotiation mode even if they agree on the way
AUTO_MODE = False           # Autopilot mode that will move automatically if there is no other choice
RANDOM_SELECT = True        # If True, robot will choose random from available choices. If False, right-hand rule
EMOTION_MANDATORY = True    # If True, emotion input is mandatory and user can't do anything until it is selected
EMOTION_TURNS = 10          # Number of turn spacing that the human will be prompted to give emotion feedback
                            # this turn count refers to the total turn count, including the robot
R_SAME_CNT = 3              # Number of same actions it turns to auto mode
MAX_DISPLAY_LINES = 10
LANGUAGE = 'EN'		    # Language to use: ES or EN


# ----------------------------------------
#       Log Configuration parameters
# ----------------------------------------
LOG_SHOW_TIMESTAMP = True       # Show timestamp on each line
LOG_SHOW_TURN = True            # Show turn count on each line
LOG_SHOW_MOVEMENT = True        # Show destination of each action
LOG_SHOW_EMOTION = True         # Show current emotion on each line

# Robot configuration constants
TIME_TURN = 1
TIME_STRAIGHT = 0.5
TILT_SPEED = 50
PAN_SPEED = 40

# Main Program States
STATE_LOGIC = 0
STATE_UI = 1
STATE_ROBOT = 2

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
R_SIT_AUTO = "1c"
R_SIT_BACKTRACK = "1d"
R_SIT_WAITING = "1e"
R_SIT_DECIDE = "1f"
R_SIT_FAIL = "1g"
R_NEG_WAITING = "Waiting input"
R_NEG_AGREE = "Both Agree"
R_NEG_YIELD = "Robot Yield"
R_NEG_COIN = "Coin Toss"
R_NEG_COIN_WIN = "Coin Toss"
R_NEG_COIN_LOSE = "Robot Loses"
R_NEG_WIN = "Robot Wins"
R_NEG_RND_1 = "2d"
R_NEG_RND_2 = "3d"
R_NEG_RND_3 = "4e"

# Player situations
P_NEG_CH1 = 0
P_NEG_CH2 = 1
P_NEG_CH3 = 2
P_NEG_COIN = 3
P_NEG_YIELD = 4

# Negotiation Stages
NEG_STAGE_NONE = "Idle"
NEG_STAGE_START = "Start of Negotiation"
NEG_STAGE_1 = "Negotiation First Round"
NEG_STAGE_2 = "Negotiation Second Round"
NEG_STAGE_AGREE = "Agreement"

# Robot counter message array positions
C_WAITING     = 0
C_MOVEMENT    = 1
C_AGREEMENT   = 2
C_NEG_R_YIELD = 3
C_TURN        = 4
C_BACKTRACK   = 5
C_DOWN        = 6
C_RIGHT       = 7
C_LEFT        = 8
C_UP          = 9
C_DEADEND     = 10
