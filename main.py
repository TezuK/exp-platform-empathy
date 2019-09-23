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
from random import randint


class Player(Widget):
    def move(self, robot_pos):
        block_size = 500/MAZE_SIZE
        center = ((500 / MAZE_SIZE) / 2) - self.size[0] / 2
        rel_pos = [robot_pos[0] * block_size, (MAZE_SIZE - 1 - robot_pos[1]) * block_size]
        self.pos = [rel_pos[0] + center, rel_pos[1] + center + MAZE_SHIFT_Y]


class RobotUI(Widget):
    labels = []

    def display_on_screen(self, message=[], init=False, mode=MODE_VS):
        with self.canvas:
            if init:
                # init the lines of the display
                for i in range(0, MAX_DISPLAY_LINES):
                    self.labels.append(Label(text="", pos=(600, 520 - i * 20),
                                             color=[.1, .1, 1, .9], bold=True, markup=True))

            for i in range(0, MAX_DISPLAY_LINES):
                # in VS Mode only use the center
                if mode == MODE_VS:
                    if len(message) != 0 and i == 0:
                        self.labels[2].text = "[size=40sp]" + message[i] + "[/size]"
                    elif len(message) == 0:
                        self.labels[i].text = ""
                # other type of display in negotiation
                else:
                    if i < len(message):
                        self.labels[i].text = message[i]
                    else:
                        self.labels[i].text = ""


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
                self.labels[1].text = "[size=40sp]" + message[0] + "[/size]"
            elif len(message) == 0:
                self.labels[i].text = ""


class HumanUI(Widget):
    labels = []

    def display_on_screen(self, message=[], init=False, mode=MODE_VS):
        with self.canvas:
            if init:
                # init the lines of the display
                for i in range(0, MAX_DISPLAY_LINES):
                    self.labels.append(Label(text="", pos=(600, 180 - i * 20),
                                             color=[1, .1, .1, .9], bold=True, markup=True))

            for i in range(0, MAX_DISPLAY_LINES):
                # in VS Mode only use the center
                if mode == MODE_VS:
                    if len(message) != 0 and i == 0:
                        self.labels[2].text = "[size=40sp]" + message[i] + "[/size]"
                    elif len(message) == 0:
                        self.labels[i].text = ""
                # other type of display in negotiation
                else:
                    if i < len(message):
                        self.labels[i].text = message[i]
                    else:
                        self.labels[i].text = ""


class MainGame(Widget):
    player = ObjectProperty(None)
    robotui = ObjectProperty(None)
    systemui = ObjectProperty(None)
    humanui = ObjectProperty(None)
    exitsign = Image()

    def __init__(self, **kwargs):
        super(MainGame, self).__init__(**kwargs)

        # Variables
        self.show_all = False
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
        self.waiting_input = False
        self.action_done = False
        self.emotions = [EMOTION_ANGRY, EMOTION_BAD, EMOTION_NEUTRAL, EMOTION_SMILE, EMOTION_HAPPY]
        self.message_counter = 0
        self.neg_stage = NEG_STAGE_NONE
        self.negotiation = negotiationclass.Negotiation()
        self.labels = []
        self.toss_time = 0.0
        self.toss_counter = 0
        self.toss_aux = 0
        self.current_toss = None
        self.waiting_toss = False
        self.next_step = None

        # Decisions taken in negotiation from the [Robot,Human] & Dead End encounters due to their decisions
        self.decisions_taken = [0, 0]
        self.deadend_count = [0, 0]
        self.last_decision = None

        # Keyboard inputs
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

        # selection screen
        self.display_on_screen(message=["Press key to select Mode:", "1. Turns", "2. Cooperative", "3. Presentation"],
                               init=True)
        self.robotui.display_on_screen(message=[""], init=True)
        self.systemui.display_on_screen(message=[""], init=True)
        self.humanui.display_on_screen(message=[""], init=True)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        choice = PLAYER_NONE
        neg_choice = False

        if self.waiting_input:
            if self.game_mode == MODE_VS or (self.game_mode == MODE_COOP and self.neg_stage == NEG_STAGE_START):
                if keycode[1] == 'up':
                    choice = PLAYER_UP
                elif keycode[1] == 'right':
                    choice = PLAYER_RIGHT
                elif keycode[1] == 'down':
                    choice = PLAYER_DOWN
                elif keycode[1] == 'left':
                    choice = PLAYER_LEFT
            elif self.game_mode == MODE_COOP and \
                    self.neg_stage != NEG_STAGE_START and self.neg_stage != NEG_STAGE_NONE:
                if keycode[1] == '1':
                    choice = P_NEG_CH1
                    self.negotiation.mark_as_used(is_robot=False, arg_number=0)
                elif keycode[1] == '2':
                    choice = P_NEG_CH2
                    self.negotiation.mark_as_used(is_robot=False, arg_number=1)
                elif keycode[1] == '3':
                    choice = P_NEG_CH3
                    self.negotiation.mark_as_used(is_robot=False, arg_number=2)
                elif keycode[1] == '4':
                    choice = P_NEG_COIN
                elif keycode[1] == '5':
                    choice = P_NEG_YIELD

                if choice != PLAYER_NONE:
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
                elif keycode[1] == '2':
                    self.game_mode = MODE_COOP
                    self.waiting_input = False
                elif keycode[1] == '3':
                    self.robot.presentation()

            if choice != PLAYER_NONE and self.game_mode is not None:
                if neg_choice:
                    self.player_neg_choice = choice
                    self.waiting_input = False
                else:
                    map_choice = background.input_to_pos(self.robot_pos, choice)
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

        self.message_counter += 1

    def clean_screen(self):
        self.display_on_screen([""])
        self.robotui.display_on_screen(message=[""], mode=self.game_mode)
        self.systemui.display_on_screen(message=[""])
        self.humanui.display_on_screen(message=[""], mode=self.game_mode)

    def update(self, dt):

        if self.turn_count == 0:
            # show the first block
            self.player.move(self.robot_pos)
            walls_value = self.maze.mmap[0][0].walls
            self.show_walls(maze_pos=[0, MAZE_SIZE - 1], walls_value=walls_value)
            self.robot_react()
            self.turn_count += 1
            self.change_active_emotion()
            # show the exit if activated
            if SHOW_EXIT:
                size = [500/MAZE_SIZE, 500/MAZE_SIZE]
                self.exitsign.size = [size[0]*0.8, size[1]*0.8]
                self.exitsign.pos = [500 - size[0] + 5, 110]
            else:
                self.exitsign.size = 0, 0
        else:
            self.maze_game()
            self.player.move(self.robot_pos)

            for j in range(MAZE_SIZE):
                for i in range(MAZE_SIZE):
                    if (self.show_all or background.check_if_visible(j, MAZE_SIZE - 1 - i, self.robot_map))\
                            and not self.painted_map[j][i]:
                        walls_value = self.maze.mmap[j][MAZE_SIZE - 1 - i].walls
                        self.show_walls(maze_pos=[j, i], walls_value=walls_value)
                        self.painted_map[j][i] = True
    
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

    def maze_game(self):
        if not self.waiting_input and not self.waiting_toss and not self.solved:
            self.clean_screen()
            # Get robot's next possible choice
            [self.robot_choice, backtrack, one_way] = background.maze_solving(self.maze, self.robot_map, self.robot_pos)

            if not backtrack and (not AUTO_MODE or (AUTO_MODE and not one_way and not backtrack)):
                # VS Mode logic
                if self.game_mode == MODE_VS:
                    if self.current_turn == TURN_ROBOT:
                        self.next_step = self.robot_choice
                        self.prev_r_pos = self.robot_pos
                        self.current_turn = TURN_PLAYER
                        self.robot.make_action(R_SIT_DECIDE,
                                               background.move_translate(self.prev_r_pos, self.robot_choice),
                                               self.game_mode, one_way or backtrack)
                    else:
                        # Get player's next choice
                        if self.player_choice == PLAYER_NONE:
                            self.waiting_input = True
                            self.robot_react(one_way, backtrack)
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
                            self.robotui.display_on_screen(["I want to go " + trad_choice, "Where do you want to go?"],
                                                           mode=self.game_mode)
                        else:
                            self.robotui.display_on_screen(["Where do you want to go?"], mode=self.game_mode)

                        self.neg_stage = NEG_STAGE_START
                        self.waiting_input = True
                        self.robot.make_action(R_NEG_WAITING,
                                               background.move_translate(self.robot_pos, self.robot_choice),
                                               self.game_mode, one_way or backtrack, self.neg_stage)
                    # Start the negotiation
                    elif self.neg_stage == NEG_STAGE_START:
                        # if the choice of the two is the same then finish it directly
                        if self.robot_choice == self.player_choice:
                            self.robotui.display_on_screen(["We thought the same! Nice!"], mode=self.game_mode)
                            self.robot.make_action(R_NEG_AGREE)
                            self.neg_stage = NEG_STAGE_AGREE
                            self.next_step = self.robot_choice

                            # Give the decision counter to the first that suggested it
                            if not one_way and not backtrack and self.current_turn == TURN_ROBOT:
                                self.decisions_taken[0] += 1
                                self.last_decision = TURN_ROBOT
                            elif not one_way and not backtrack:
                                self.decisions_taken[1] += 1
                                self.last_decision = TURN_PLAYER
                        # if the emotion is angry or for the first two decisions, robot will have to yield
                        elif self.player_feel == EMOTION_ANGRY or \
                                (self.decisions_taken[0] + self.decisions_taken[1] < PRE_NEG_CHOICES):
                            self.robotui.display_on_screen(["Lets try it your way"], mode=self.game_mode)
                            self.robot.make_action(R_NEG_YIELD)
                            self.neg_stage = NEG_STAGE_AGREE
                            self.decisions_taken[1] += 1
                            self.last_decision = TURN_PLAYER
                            self.next_step = self.player_choice
                        else:
                            self.neg_stage = NEG_STAGE_1
                    # if there is any input pending from the user
                    elif self.player_neg_choice != PLAYER_NONE:
                        if self.player_neg_choice == P_NEG_YIELD:
                            self.next_step = self.robot_choice
                            self.neg_stage = NEG_STAGE_AGREE
                            self.robot.make_action(R_NEG_WIN)
                            self.decisions_taken[0] += 1
                            self.last_decision = TURN_ROBOT
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
                            self.clean_screen()
                            robot_neg_choice = self.negotiation.choose_first_avail()
                            robot_neg_msg = ["Then let's negotiate. I say that...",
                                             self.negotiation.arg_description[robot_neg_choice][2:], ""]
                            self.robotui.display_on_screen(robot_neg_msg, mode=self.game_mode)
                            self.negotiation.mark_as_used(is_robot=True, arg_number=robot_neg_choice)
                            # Coin toss
                            if robot_neg_choice == P_NEG_COIN:
                                self.coin_toss(init=True)
                            elif robot_neg_choice == P_NEG_YIELD:
                                self.neg_stage = NEG_STAGE_AGREE
                                self.robot.make_action(R_NEG_YIELD)
                                self.next_step = self.player_choice
                                self.decisions_taken[0] += 1
                                self.last_decision = TURN_PLAYER
                            else:
                                # do a robot cue with more emphasis if it is the 2nd step
                                if self.neg_stage != NEG_STAGE_1:
                                    self.robot.make_action(R_NEG_WAITING,
                                                           background.move_translate(self.prev_r_pos,
                                                                                     self.robot_choice),
                                                           self.game_mode, one_way or backtrack, self.neg_stage)
                                else:
                                    self.robot.make_action(R_NEG_RND_1)

                                self.humanui.display_on_screen(message=self.negotiation.get_display_msg(),
                                                               mode=self.game_mode)
                                self.waiting_input = True
                        else:
                            robot_neg_choice = self.negotiation.choose_first_avail()
                            self.robotui.display_on_screen(["Then let's negotiate. I say that...",
                                                            self.negotiation.arg_description[robot_neg_choice]],
                                                           mode=self.game_mode)
                            self.negotiation.mark_as_used(robot_neg_choice)
                            # Coin toss
                            if robot_neg_choice == 3:
                                self.coin_toss(init=True)
            else:
                self.next_step = self.robot_choice

            if (self.game_mode == MODE_VS and not self.waiting_input) or \
                    (self.game_mode == MODE_COOP and self.neg_stage == NEG_STAGE_AGREE) or \
                    (AUTO_MODE and one_way) or backtrack:

                # Update position
                self.robot_map = background.move_position(self.robot_map, self.robot_pos, self.next_step,
                                                          self.prev_r_pos, backtrack)
                self.robot_pos = self.next_step
                self.player_choice = PLAYER_NONE

                # If it is a dead end, count it
                if sum(self.maze.mmap[self.next_step[0]][self.next_step[1]].walls) > 2:
                    if self.last_decision == TURN_ROBOT:
                        self.deadend_count[0] += 1
                    else:
                        self.deadend_count[1] += 1

                if self.next_step == [MAZE_SIZE - 1, MAZE_SIZE - 1]:
                    self.solved = True
                    self.robot_react()
                else:
                    self.robot_react(one_way, backtrack)

                background.write_log(self.next_step, self.game_mode, self.turn_count,
                                     self.current_turn, self.neg_stage, one_way)
                self.turn_count += 1
                self.neg_stage = NEG_STAGE_NONE
                self.negotiation.reset()
                print(str(self.decisions_taken))
        elif self.waiting_toss:
            self.coin_toss()
        elif not self.waiting_input and self.solved:
            self.display_on_screen(["CONGRATULATIONS!!", "WE FOUND THE EXIT!!", "", "Press Q to Quit."])
            self.game_mode = MODE_FINISH
            self.waiting_input = True

    def coin_toss(self, init=False):
        if init:
            self.waiting_toss = True
            self.toss_time = time.time()
            self.systemui.display_on_screen(["Tossing coin"])
            self.toss_counter += 1
            self.toss_aux = 0

        # one second flickering between screens
        if time.time() - self.toss_time > 2 and self.current_toss != TURN_PLAYER:
            self.robotui.display_on_screen([""])
            self.humanui.display_on_screen(["Your turn!"])
            self.toss_time = time.time()
            self.toss_aux += 1
            self.robot.make_action(R_NEG_COIN, TURN_PLAYER)
            self.current_toss = TURN_PLAYER
        elif time.time() - self.toss_time > 1 and self.current_toss != TURN_ROBOT:
            self.robotui.display_on_screen(["My turn!"])
            self.humanui.display_on_screen([""])
            self.robot.make_action(R_NEG_COIN, TURN_ROBOT)
            self.current_toss = TURN_ROBOT

        if self.toss_aux > 4:
            # Clean screen and show the winner
            self.clean_screen()
            if randint(0, 1) == 1:
                self.robotui.display_on_screen(["My turn!"])
                self.next_step = self.robot_choice
                self.robot.make_action(R_NEG_AGREE)
                self.decisions_taken[0] += 1
                self.last_decision = TURN_ROBOT
            else:
                self.humanui.display_on_screen(["Your turn!"])
                self.next_step = self.player_choice
                self.robot.make_action(R_NEG_LOSE)
                self.decisions_taken[1] += 1
                self.last_decision = TURN_PLAYER

            time.sleep(2)
            self.neg_stage = NEG_STAGE_AGREE
            self.waiting_toss = False

    def robot_react(self, one_way=False, backtrack=False):
        walls = self.maze.mmap[self.robot_pos[0]][self.robot_pos[1]].walls

        if self.turn_count == 0:
            self.robot.make_action(R_SIT_START)
        elif self.waiting_input:
            self.humanui.display_on_screen(["Your turn!!"], mode=self.game_mode)
            self.robot.make_action(R_SIT_WAITING)
        elif self.solved:
            self.change_maze_color()
            self.robot.make_action(R_SIT_WIN)
        elif sum(walls) == 3 and self.robot_pos != [0, 0]:
            self.robotui.display_on_screen(["Owwwwwww..."], mode=self.game_mode)
            self.robot.make_action(R_SIT_DEAD_END)
        elif one_way and AUTO_MODE:
            self.roboui.display_on_screen(["There is only one way!"], mode=self.game_mode)
            self.robot.make_action(R_SIT_MOVING)
        elif backtrack:
            self.robotui.display_on_screen(["Backtracking..."], mode=self.game_mode)
            self.robot.make_action(R_SIT_BACKTRACK)
        elif not self.waiting_input and self.current_turn == TURN_PLAYER:
            self.robotui.display_on_screen(["Deciding..."], mode=self.game_mode)


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
            elif m_option == OPTION_VS:  # 2
                self.maze_vs()
            elif m_option == OPTION_COOP:  # 3
                self.maze_coop()
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

    def maze_vs(self):
        # Just starting with the robot playing solo
        i_solved = False

        while not i_solved:
            # debug
            print("MAP: " + str(self.maze.mmap[self.robot_pos[0]][self.robot_pos[1]].walls))
            print("ROBOT: " + str(self.robot_map))

            time.sleep(2)

            next_step = background.maze_solving(self.maze, self.robot_map, self.robot_pos)
            self.robot_map = background.move_position(self.robot_map, self.robot_pos, next_step)

            # Update position
            self.robot_pos = self.next_step

            if self.robot_pos == [MAZE_SIZE - 1, MAZE_SIZE - 1]:
                i_solved = True

        else:
            print("Solved")
        
    def maze_coop(self):
        reserved = ""


if __name__ == '__main__':
    MainApp().run()
