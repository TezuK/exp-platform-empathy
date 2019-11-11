from const_def import *
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.properties import (
    NumericProperty, ReferenceListProperty, ObjectProperty, ListProperty
)
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle, Line
import background
import foreground
import robotclass
import negotiationclass
import time
from random import randint, choice

if LANGUAGE == 'ES':
    import robotext_ES as robotext
elif LANGUAGE == 'EN':
    import robotext_EN as robotext


class Player(Widget):
    def move(self, robot_pos):
        block_size = 500/MAZE_SIZE
        center = ((500 / MAZE_SIZE) / 2) - self.size[0] / 2
        rel_pos = [robot_pos[0] * block_size, (MAZE_SIZE - 1 - robot_pos[1]) * block_size]
        self.pos = [rel_pos[0] + center, rel_pos[1] + center + MAZE_SHIFT_Y]


class RobotUI(Widget):
    labels = []

    def display_on_screen(self, message=[], init=False):
        with self.canvas:
            if init:
                # init the lines of the display
                for i in range(0, MAX_DISPLAY_LINES):
                    self.labels.append(Label(text="", pos=(600, 520 - i * 20),
                                             color=[.1, .1, 1, .9], bold=True, markup=True))

            for i in range(0, MAX_DISPLAY_LINES):
                # if it is only one line display it on the center and big size
                if len(message) == 1 or i >= len(message):
                    self.labels[i].text = ""
                else:
                    self.labels[i].text = message[i]

            if len(message) == 1:
                if len(message[0]) < 20:
                    self.labels[2].text = "[size=40sp]" + message[0] + "[/size]"
                else:
                    self.labels[0].text = message[0]


class SystemUI(Widget):
    labels = []

    def display_on_screen(self, message=[], init=False):
        with self.canvas:
            if init:
                # init the lines of the display
                for i in range(0, MAX_DISPLAY_LINES):
                    self.labels.append(Label(text="", pos=(600, 275 - i * 20),
                                             color=[.1, 1, .1, .9], bold=True, markup=True))

            if len(message) != 0:
                if len(message[0]) > 15:
                    self.labels[1].text = "[size=26sp]" + message[0] + "[/size]"
                else:
                    self.labels[1].text = "[size=40sp]" + message[0] + "[/size]"
            elif len(message) == 0:
                self.labels[1].text = ""


class HumanUI(Widget):
    labels = []

    def display_on_screen(self, message=[], init=False):
        with self.canvas:
            if init:
                # init the lines of the display
                for i in range(0, MAX_DISPLAY_LINES):
                    self.labels.append(Label(text="", pos=(600, 180 - i * 20),
                                             color=[1, .1, .1, .9], bold=True, markup=True))

            for i in range(0, MAX_DISPLAY_LINES):
                # if it is only one line display it on the center and big size
                if len(message) == 1 or i >= len(message):
                    self.labels[i].text = ""
                else:
                    self.labels[i].text = message[i]

            if len(message) == 1:
                if len(message[0]) < 20:
                    self.labels[2].text = "[size=40sp]" + message[0] + "[/size]"
                else:
                    self.labels[0].text = message[0]


class BatteryUI(Widget):
    labels = ""

    def display_on_screen(self, robot, init=False):
        battery = robot.status()
        with self.canvas:
            if init:
                self.labels = Label(text="", pos=(600, -35),
                                    color=[1, 1, 1, .9], bold=False, markup=True)

            self.labels.text = "[size=12sp]Base Battery: " + str(battery[0]) + "%             " + \
                               "Phone Battery: " + str(battery[1]) + "%[/size]"


class MainGame(Widget):
    player = ObjectProperty(None)
    robotui = ObjectProperty(None)
    systemui = ObjectProperty(None)
    humanui = ObjectProperty(None)
    batteryui = ObjectProperty(None)
    exitsign = Image()

    def __init__(self, **kwargs):
        super(MainGame, self).__init__(**kwargs)

        # Variables
        self.solved = False
        self.prev_r_pos = [0, 0]
        self.prev_decision = None
        self.player_choice = PLAYER_NONE
        self.player_neg_choice = PLAYER_NONE
        self.robot_choice = None
        self.game_mode = None
        self.turn_count = 0
        self.robot = robotclass.Robot(ROBOT_IP)
        self.maze = background.maze_generation(MAZE_SIZE, "full")
        self.robot_map = background.maze_generation(MAZE_SIZE, "empty")
        self.painted_map = [[False for j in range(MAZE_SIZE)] for i in range(MAZE_SIZE)]
        self.block_map = [[False for j in range(MAZE_SIZE)] for i in range(MAZE_SIZE)]
        self.robot_pos = [0, 0]  # [x, y]
        self.player_feel = EMOTION_NEUTRAL
        self.current_turn = START_SELECT
        self.waiting_input = True
        self.action_done = False
        self.emotions = [EMOTION_ANGRY, EMOTION_BAD, EMOTION_NEUTRAL, EMOTION_SMILE, EMOTION_HAPPY]
        self.neg_stage = NEG_STAGE_NONE
        self.negotiation = negotiationclass.Negotiation()
        self.labels = []
        self.toss_time = 0.0
        self.toss_counter = 0
        self.toss_aux = 0
        self.current_toss = None
        self.waiting_toss = False
        self.next_step = None
        self.emotion_count = 0
        self.current_state = STATE_UI
        self.robot_action = None
        self.one_way = False
        self.backtrack = False
        self.take_step = False
        self.time = time.time()
        self.waiting_emotion_input = False  # to control time to request emotion input from user
        self.last_emotion_utterance_time = 0

        # Decisions taken in negotiation from the [Robot,Human] & Dead End encounters due to their decisions
        self.decisions_taken = [0, 0]
        self.deadend_count = [0, 0]
        self.last_decision = None
        self.robot_neg = -1

        # Keyboard inputs
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

        # selection screen
        self.display_on_screen(init=True)
        self.robotui.display_on_screen(init=True)
        self.systemui.display_on_screen(init=True)
        self.humanui.display_on_screen(init=True)
        self.batteryui.display_on_screen(robot=self.robot, init=True)
        self.message_generalui = ["Press key to select Mode:", "1. Turns", "2. Cooperative", "3. Presentation"]
        self.message_robotui = []
        self.message_humanui = []
        self.message_systemui = []

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        selection = PLAYER_NONE
        neg_choice = False
        available = False

        if self.waiting_input and not (EMOTION_MANDATORY and self.emotion_count >= EMOTION_TURNS) or \
                self.game_mode == MODE_FINISH:
            if self.game_mode == MODE_VS or (self.game_mode == MODE_COOP and self.neg_stage == NEG_STAGE_START):
                if keycode[1] == 'up':
                    selection = PLAYER_UP
                elif keycode[1] == 'right':
                    selection = PLAYER_RIGHT
                elif keycode[1] == 'down':
                    selection = PLAYER_DOWN
                elif keycode[1] == 'left':
                    selection = PLAYER_LEFT
            elif self.game_mode == MODE_COOP and \
                    self.neg_stage != NEG_STAGE_START and self.neg_stage != NEG_STAGE_NONE:
                if keycode[1] == '1':
                    selection = P_NEG_CH1
                    available = self.negotiation.mark_as_used(is_robot=False, arg_number=0)
                elif keycode[1] == '2':
                    selection = P_NEG_CH2
                    available = self.negotiation.mark_as_used(is_robot=False, arg_number=1)
                elif keycode[1] == '3':
                    selection = P_NEG_CH3
                    available = self.negotiation.mark_as_used(is_robot=False, arg_number=2)
                elif keycode[1] == '4':
                    selection = P_NEG_COIN
                    available = True
                elif keycode[1] == '5':
                    selection = P_NEG_YIELD
                    available = True
                    background.write_log(player=TURN_ROBOT, negotiation=True,
                                         neg_reason="YIELD")
                elif keycode[1] == '6':
                    selection = P_NEG_DENY
                    available = True
                    background.write_log(player=TURN_ROBOT, negotiation=True,
                                         neg_reason="DENY")

                if selection != PLAYER_NONE and available:
                    neg_choice = True
            # This is done at the end of the game, close screen
            elif self.game_mode == MODE_FINISH:
                if keycode[1] == 'q':
                    exit()
            # This is done at the start of the game, selection of the mode
            elif not self.game_mode:
                if keycode[1] == '1':
                    self.game_mode = MODE_VS
                    self.waiting_input = False
                    self.robot_action = R_SIT_START
                elif keycode[1] == '2':
                    self.game_mode = MODE_COOP
                    self.waiting_input = False
                    self.robot_action = R_SIT_START
                elif keycode[1] == '3':
                    self.robot.presentation()

            if selection != PLAYER_NONE and self.game_mode is not None:
                if neg_choice:
                    self.player_neg_choice = selection
                    self.waiting_input = False
                else:
                    map_choice = background.input_to_pos(self.robot_pos, selection)
                    if background.check_if_valid(self.maze, self.robot_map, self.robot_pos, map_choice):
                        self.player_choice = map_choice
                        self.waiting_input = False

        return True

    def emotion_press(self, *args):
        face_size = 50
        face_margin = 20
        face_pos_x = SCREEN_FACES_LENGTH / 5

        # Check if the press is done on the emotions panel faces
        for i in range(len(self.emotions)):
            face_boundary = [i * face_pos_x + face_margin, i * face_pos_x + face_margin + face_size]
            if (args[1].pos[0] > face_boundary[0]) and (args[1].pos[0] < face_boundary[1]):
                self.player_feel = self.emotions[i]
                self.change_active_emotion()
                background.write_log(emotion=self.player_feel)
                self.emotion_count = 0
                self.waiting_emotion_input = False
                self.message_systemui= [""]
                if DEBUG_MODE:
                    print(self.player_feel)

                return True

    def change_active_emotion(self):
        with self.canvas:
            for i in range(len(self.emotions)):
                rectangle_pos = [i * SCREEN_FACES_LENGTH/5 + 10, 10]
                if self.player_feel == self.emotions[i]:
                    Color(1., 1., 0)
                else:
                    Color(0, 0, 0)
                Line(rectangle=(rectangle_pos[0], rectangle_pos[1], 70, 70))
            Color(1., 1., 1.)

    def display_on_screen(self, message=[], init=False):
        with self.canvas:
            if init:
                # init the lines of the display
                for i in range(0, MAX_DISPLAY_LINES):
                    self.labels.append(Label(text="", pos=(600, 520 - i * 20)))
                    self.waiting_input = True

            for i in range(0, MAX_DISPLAY_LINES):
                # clean the unused lines
                if i < len(message):
                    if self.solved:
                        Color(1., 1., 0)
                    self.labels[i].text = message[i]
                else:
                    self.labels[i].text = ""

    def clean_message_ui(self):
        self.message_generalui = []
        self.message_robotui = []
        self.message_systemui = []
        self.message_humanui = []

    def update(self, dt):
        if self.current_state == STATE_LOGIC:
            self.game_logic()
            self.current_state = STATE_UI
        elif self.current_state == STATE_UI:
            self.game_ui()
            self.current_state = STATE_ROBOT
        else:
            if self.robot_action is not None:
                self.game_robot()
            self.current_state = STATE_LOGIC

    def game_logic(self):
        self.robot_action = None

        if time.time() - self.time > TIME_LIMIT*60 and not self.waiting_input:
            self.clean_message_ui()
            self.message_generalui = robotext.end_failure
            self.robot_action = R_SIT_FAIL
            self.game_mode = MODE_FINISH
            self.waiting_input = True
        elif self.take_step:
            self.prev_r_pos = self.robot_pos
            self.robot_pos = self.next_step
            self.take_step = False

            if sum(self.maze.mmap[self.next_step[0]][self.next_step[1]].walls) > 2 and not self.solved:
                if self.last_decision == TURN_ROBOT:
                    self.deadend_count[0] += 1
                else:
                    self.deadend_count[1] += 1
                self.robot_action = R_SIT_DEAD_END
                self.message_robotui = ["Owwwwwww..."]
        elif not self.waiting_input and not self.waiting_toss and not self.solved and not self.waiting_emotion_input:
            self.clean_message_ui()
            special = False
            if self.emotion_count >= EMOTION_TURNS:
                self.message_systemui = ["Please select emotion"]
                self.waiting_emotion_input = True
                self.last_emotion_utterance_time = 0

            # Get robot's next possible choice
            if self.game_mode == MODE_VS or self.neg_stage == NEG_STAGE_NONE:
                [self.robot_choice, self.backtrack, self.one_way, special] = background.maze_solving(self.maze,
                                                                                                     self.robot_map,
                                                                                                     self.robot_pos)
            if special:
                self.robot_map[self.robot_pos[0]][self.robot_pos[1]] = BLOCK_CONFLICT

            if not self.backtrack and (not AUTO_MODE or (AUTO_MODE and not self.one_way and not self.backtrack)):
                # VS Mode logic
                if self.game_mode == MODE_VS:
                    if self.current_turn == TURN_ROBOT:
                        self.next_step = self.robot_choice
                        self.prev_r_pos = self.robot_pos
                        self.current_turn = TURN_PLAYER
                        self.robot_action = R_SIT_DECIDE
                        self.message_robotui = ["Deciding..."]
                    else:
                        # Get player's next choice
                        if self.player_choice == PLAYER_NONE:
                            self.waiting_input = True
                            self.message_humanui = ["Your turn!!"]
                            self.robot_action = R_SIT_WAITING
                        # Process player's choice
                        elif self.player_choice != PLAYER_NONE:
                            self.next_step = self.player_choice
                            self.current_turn = TURN_ROBOT
                # Cooperation Mode logic
                else:
                    # Do the previous inquiry before starting the negotiation
                    if self.neg_stage == NEG_STAGE_NONE:
                        if self.current_turn == TURN_ROBOT:
                            trad_choice = background.pos_to_input(self.robot_pos, self.robot_choice)
                            self.message_robotui = ["I want to go " + trad_choice, "Where do you want to go?"]
                            if not DEBUG_MODE:
                                self.robot.robobo.sayText(choice(eval("robotext.robot_choice_" + trad_choice.lower())),
                                                          wait=True)
                        else:
                            self.message_robotui = ["Where do you want to go?"]

                        self.neg_stage = NEG_STAGE_START
                        self.waiting_input = True
                        self.robot_action = R_NEG_WAITING
                    # Start the negotiation
                    elif self.neg_stage == NEG_STAGE_START:
                        # if the choice of the two is the same then finish it directly
                        if self.robot_choice == self.player_choice:
                            self.message_robotui = ["We thought the same! Nice!"]
                            self.robot_action = R_NEG_AGREE
                            self.neg_stage = NEG_STAGE_AGREE
                            self.next_step = self.robot_choice
                            self.take_step = True

                            # Give the decision counter to the first that suggested it
                            if COUNT_SAME_DEC:
                                if not self.one_way and not self.backtrack and self.current_turn == TURN_ROBOT:
                                    self.decisions_taken[0] += 1
                                    self.last_decision = TURN_ROBOT
                                elif not self.one_way and not self.backtrack:
                                    self.decisions_taken[1] += 1
                                    self.last_decision = TURN_PLAYER
                        # if the emotion is angry or for the first two decisions, robot will have to yield
                        elif self.player_feel == EMOTION_ANGRY or \
                                (self.decisions_taken[0] + self.decisions_taken[1] < PRE_NEG_CHOICES):
                            self.message_robotui = ["Let's try it your way"]
                            self.robot_action = R_NEG_YIELD
                            self.neg_stage = NEG_STAGE_AGREE
                            self.decisions_taken[1] += 1
                            self.last_decision = TURN_PLAYER
                            self.next_step = self.player_choice
                            self.take_step = True
                        else:
                            self.neg_stage = NEG_STAGE_1
                    # if there is any input pending from the user
                    elif self.player_neg_choice != PLAYER_NONE:
                        if self.player_neg_choice == P_NEG_YIELD:
                            self.next_step = self.robot_choice
                            self.neg_stage = NEG_STAGE_AGREE
                            self.message_robotui = ["Thanks!"]
                            self.robot_action = R_NEG_WIN
                            self.decisions_taken[0] += 1
                            self.last_decision = TURN_ROBOT
                            self.take_step = True
                        elif self.player_neg_choice == P_NEG_DENY:
                            self.next_step = self.player_choice
                            self.neg_stage = NEG_STAGE_AGREE
                            self.message_robotui = ["Ok..."]
                            self.robot_action = R_NEG_YIELD
                            self.decisions_taken[1] += 1
                            self.last_decision = TURN_PLAYER
                            self.take_step = True
                        elif self.player_neg_choice == P_NEG_COIN:
                            self.coin_toss(init=True)
                        else:
                            self.neg_stage = NEG_STAGE_2

                        self.player_neg_choice = PLAYER_NONE
                    # Negotiations steps should all use the same logic
                    elif self.neg_stage != NEG_STAGE_AGREE:
                        self.negotiation.check_arg_availability(self.decisions_taken,
                                                                self.deadend_count,
                                                                self.player_feel)
                        if self.current_turn == TURN_ROBOT:
                            self.clean_message_ui()
                            robot_neg_choice = self.negotiation.choose_first_avail()
                            self.message_robotui = ["Then let's negotiate. I say that...",
                                                    self.negotiation.arg_description[robot_neg_choice][2:], ""]
                            self.negotiation.mark_as_used(is_robot=True, arg_number=robot_neg_choice)
                            # Coin toss
                            if robot_neg_choice == P_NEG_COIN:
                                self.coin_toss(init=True)
                                self.message_robotui = ["Toss the coin!"]
                            elif robot_neg_choice == P_NEG_YIELD:
                                self.neg_stage = NEG_STAGE_AGREE
                                self.message_robotui = ["Let's try it your way"]
                                self.robot_action = R_NEG_YIELD
                                self.next_step = self.player_choice
                                self.decisions_taken[0] += 1
                                self.last_decision = TURN_PLAYER
                                self.take_step = True
                                background.write_log(player=self.last_decision, negotiation=True,
                                                     neg_reason="YIELD")
                            else:
                                # do a robot cue with more emphasis if it is the 2nd step
                                if self.neg_stage != NEG_STAGE_1:
                                    self.robot_action = R_NEG_RND_2
                                else:
                                    self.robot_action = R_NEG_RND_1
                                print("ROUND: " + str(self.neg_stage) + " >>>>>>>>" + str(robot_neg_choice))
                                self.robot_neg = robot_neg_choice
                                self.message_humanui = self.negotiation.get_display_msg()
                                self.waiting_input = True
                        else:
                            robot_neg_choice = self.negotiation.choose_first_avail()
                            self.message_robotui = ["Then let's negotiate. I say that...",
                                                    self.negotiation.arg_description[robot_neg_choice][2:], ""]
                            self.negotiation.mark_as_used(arg_number=robot_neg_choice)
                            # Coin toss
                            if robot_neg_choice == P_NEG_COIN:
                                self.coin_toss(init=True)
            else:
                self.next_step = self.robot_choice

            if (self.game_mode == MODE_VS and not self.waiting_input) or \
                    (self.game_mode == MODE_COOP and self.neg_stage == NEG_STAGE_AGREE) or \
                    (AUTO_MODE and self.one_way) or self.backtrack:

                # Update position
                self.robot_map = background.move_position(self.robot_map, self.robot_pos, self.next_step,
                                                          self.prev_r_pos, self.backtrack)
                self.player_choice = PLAYER_NONE
                self.take_step = True

                # If it is a dead end, count it
                if self.backtrack:
                    self.robot_action = R_SIT_BACKTRACK
                    self.message_robotui = ["Backtracking..."]
                elif self.one_way and AUTO_MODE:
                    self.message_robotui = ["There is only one way!"]
                    self.robot_action = R_SIT_AUTO

                if self.next_step == [MAZE_SIZE - 1, MAZE_SIZE - 1]:
                    self.solved = True

                background.write_log(current_mov=self.next_step, game_mode=self.game_mode, turn_count=self.turn_count,
                                     player=self.current_turn, one_way=self.one_way, backtracking=self.backtrack,
                                     emotion=self.player_feel)
                self.turn_count += 1
                self.emotion_count += 1
                self.neg_stage = NEG_STAGE_NONE
                self.negotiation.reset()
        elif self.waiting_toss:
            self.coin_toss()
        elif not self.waiting_input and self.solved:
            self.clean_message_ui()
            self.message_generalui = robotext.end_win
            self.change_maze_color()
            self.robot_action = R_SIT_WIN
            self.game_mode = MODE_FINISH
            self.waiting_input = True
        elif self.waiting_emotion_input:
            if time.time() - self.last_emotion_utterance_time > 5 and not DEBUG_MODE:
                self.robot.robobo.sayText(choice(robotext.input_emotion))
                self.last_emotion_utterance_time = time.time()

    def game_ui(self):
        # show the exit if activated
        if self.turn_count == 0:
            if SHOW_EXIT:
                size = [500/MAZE_SIZE, 500/MAZE_SIZE]
                self.exitsign.size = [size[0]*0.8, size[1]*0.8]
                self.exitsign.pos = [500 - size[0] + 5, 110]
            else:
                self.exitsign.size = 0, 0

        # show player and current emotion
        self.player.move(self.robot_pos)
        self.change_active_emotion()

        # paint the maze when the turn is made
        if not self.take_step:
            for j in range(MAZE_SIZE):
                for i in range(MAZE_SIZE):
                    if (SHOW_ALL or background.check_if_visible(j, MAZE_SIZE - 1 - i, self.robot_map)) \
                            and not self.painted_map[j][i]:
                        walls_value = self.maze.mmap[j][MAZE_SIZE - 1 - i].walls
                        self.show_walls(maze_pos=[j, i], walls_value=walls_value, win=self.solved)
                        self.painted_map[j][i] = True

        self.display_on_screen(message=self.message_generalui)
        self.robotui.display_on_screen(message=self.message_robotui)
        self.systemui.display_on_screen(message=self.message_systemui)
        self.humanui.display_on_screen(message=self.message_humanui)
        self.batteryui.display_on_screen(robot=self.robot)

    def game_robot(self):
        walls = self.maze.mmap[self.robot_pos[0]][self.robot_pos[1]].walls

        if self.robot_action == R_SIT_DECIDE or self.robot_action == R_NEG_WAITING or self.robot_action == R_NEG_RND_2:
            self.robot.make_action(situation=self.robot_action,
                                   move=background.move_translate(self.prev_r_pos, self.robot_choice),
                                   mode=self.game_mode, one_way=self.one_way or self.backtrack,
                                   neg_stage=self.neg_stage, neg_option=self.robot_neg)
        elif self.robot_action == R_NEG_RND_1:
            self.robot.make_action(situation=self.robot_action,
                                   move=background.move_translate(self.prev_r_pos, self.robot_choice),
                                   one_way=False,
                                   neg_option=self.robot_neg)
        elif self.robot_action == R_NEG_COIN:
            self.robot.make_action(situation=self.robot_action, move=self.current_toss)
        else:
            self.robot.make_action(situation=self.robot_action)

    def show_walls(self, maze_pos, walls_value, win=False):
        block_size = 500/MAZE_SIZE
        block_pos = maze_pos[0] * block_size, maze_pos[1] * block_size
        
        # Paint all the walls that are in the block
        with self.canvas:
            if win:
                Color(0, 1., 0)

            if not maze_pos == [MAZE_SIZE-1, 0]:
                if walls_value[WALL_TOP]:
                    wall_pos = [block_pos[0], block_pos[1] + block_size * (1 - WALL_THICK) + MAZE_SHIFT_Y]
                    wall_size = [block_size, WALL_THICK * block_size]
                    self.block_map[maze_pos[0]][maze_pos[1]] = Rectangle(pos=wall_pos, size=wall_size)

                if walls_value[WALL_RIGHT]:
                    wall_pos = [block_pos[0] + block_size * (1 - WALL_THICK), block_pos[1] + MAZE_SHIFT_Y]
                    wall_size = [WALL_THICK * block_size, block_size]
                    self.block_map[maze_pos[0]][maze_pos[1]] = Rectangle(pos=wall_pos, size=wall_size)

                if walls_value[WALL_BOTTOM]:
                    wall_pos = [block_pos[0], block_pos[1] + MAZE_SHIFT_Y]
                    wall_size = [block_size, WALL_THICK * block_size]
                    self.block_map[maze_pos[0]][maze_pos[1]] = Rectangle(pos=wall_pos, size=wall_size)

                if walls_value[WALL_LEFT]:
                    wall_pos = [block_pos[0], block_pos[1] + MAZE_SHIFT_Y]
                    wall_size = [WALL_THICK * block_size, block_size]
                    self.block_map[maze_pos[0]][maze_pos[1]] = Rectangle(pos=wall_pos, size=wall_size)

    def change_maze_color(self):
        for j in range(MAZE_SIZE):
            for i in range(MAZE_SIZE):
                walls_value = self.maze.mmap[j][MAZE_SIZE - 1 - i].walls
                self.show_walls(maze_pos=[j, i], walls_value=walls_value, win=True)

    def coin_toss(self, init=False):
        if init:
            self.waiting_toss = True
            self.toss_time = time.time()
            self.message_systemui = ["Tossing coin"]
            self.toss_counter += 1
            self.toss_aux = 0
            self.robot_action = R_NEG_COIN
            self.current_toss = None
            self.robot.robobo.sayText(choice(robotext.toss_coin))
        elif self.neg_stage != NEG_STAGE_AGREE and self.toss_aux > 3:
            # Clean screen and show the winner
            self.clean_message_ui()
            if randint(0, 1) == 1:
                self.message_robotui = ["My turn!",
                                        "Let's go " + background.pos_to_input(self.robot_pos, self.robot_choice)]
                self.next_step = self.robot_choice
                self.robot_action = R_NEG_COIN_WIN
                self.decisions_taken[0] += 1
                self.last_decision = TURN_ROBOT
            else:
                self.message_humanui = ["Your turn!",
                                        "Let's go " + background.pos_to_input(self.robot_pos, self.player_choice)]
                self.next_step = self.player_choice
                self.robot_action = R_NEG_COIN_LOSE
                self.decisions_taken[1] += 1
                self.last_decision = TURN_PLAYER

            self.neg_stage = NEG_STAGE_AGREE
            self.toss_time = time.time()
            background.write_log(player=self.last_decision, negotiation=True, neg_reason="COIN TOSS")
        elif self.neg_stage == NEG_STAGE_AGREE and time.time() - self.toss_time > 2:
            # option to reveal the winner on screen
            self.waiting_toss = False
        elif self.neg_stage != NEG_STAGE_AGREE and \
                time.time() - self.toss_time > 2 and self.current_toss != TURN_PLAYER:
            # one second flickering between screens
            self.message_robotui = []
            self.message_humanui = ["Your turn!"]
            self.toss_time = time.time()
            self.toss_aux += 1
            self.robot_action = R_NEG_COIN
            self.current_toss = TURN_PLAYER
        elif self.neg_stage != NEG_STAGE_AGREE and \
                time.time() - self.toss_time > 1 and self.current_toss != TURN_ROBOT:
            # one second flickering between screens
            self.message_robotui = ["My turn!"]
            self.message_humanui = []
            self.robot_action = R_NEG_COIN
            self.current_toss = TURN_ROBOT


class MainApp(App):
    def build(self):
        game = MainGame()
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game


class MainLogic:
    def __init__(self):
        # Initialize robot and maze
        self.robot = robotclass.Robot(ROBOT_IP)
        self.maze = background.maze_generation(MAZE_SIZE, "full")
        self.robot_map = background.maze_generation(MAZE_SIZE, "empty")
        self.robot_pos = [0, 0]  # [x, y]
        self.prev_move = None

    def run(self):
        m_running = True
        while m_running:
            m_option = foreground.menu(MENU_INITIAL)
            
            if m_option == OPTION_DEBUG:  # 1
                self.robot_debug()
            elif m_option == OPTION_QUIT:  # q
                m_running = False
        
        self.robot.end()
        
    def robot_debug(self):
        # Robot debug procedure, for testing only
        i_running = True
        
        while i_running:
            i_option = foreground.menu(MENU_DEBUG)
            
            if i_option == DEBUG_FWD:  # 1a
                self.robot.do_movement(R_MOVE_FWD)
            elif i_option == DEBUG_RIGHT:  # 1b
                self.robot.do_movement(R_MOVE_RIGHT)
            elif i_option == DEBUG_BACK:  # 1c
                self.robot.do_movement(R_MOVE_BACK)
            elif i_option == DEBUG_LEFT:  # 1d
                self.robot.do_movement(R_MOVE_LEFT)
            elif i_option == DEBUG_LEDS:  # 2
                self.robot.test_leds()
            elif i_option == DEBUG_SOUND:  # 3
                self.robot.test_sound()
            elif i_option == DEBUG_TALK:  # 4
                self.robot.talk(input("Write what you want to hear: "))
            elif i_option == DEBUG_FACES:  # 5
                self.robot.test_faces()
            elif i_option == DEBUG_TILT:  # 6
                self.robot.test_tilt()
            elif i_option == DEBUG_PAN:  # 7
                self.robot.test_pan()
            elif i_option == DEBUG_HELLO:  # 8
                self.robot.presentation()
            elif i_option == DEBUG_QUIT:  # q
                i_running = False


if __name__ == '__main__':
    MainApp().run()
