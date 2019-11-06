from Robobo import Robobo
from random import randint
from const_def import *
from utils.Wheels import Wheels
from utils.IR import IR
from utils.Sounds import Sounds
from utils.Emotions import Emotions
from utils.LED import LED
from utils.Color import Color
import time

if LANGUAGE == 'ES':
    import robotext_ES as robotext
elif LANGUAGE == 'EN':
    import robotext_EN as robotext


class Robot:

    def __init__(self, robot_ip):
        # Initialize the connection
        self.speed = 30
        self.turn_speed = 20
        self.robobo = Robobo(robot_ip)
        self.same_sit_cnt = 1
        self.counters = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.prev_sit = None
        self.cues_counter = 0
        if not DEBUG_MODE:
            self.robobo.connect()

    def end(self):
        self.robobo.stopMotors()
        self.robobo.disconnect()

    def do_movement(self, move, lite=False):
        if move == R_MOVE_FWD:
            self.robobo.moveWheelsByTime(self.speed, self.speed, TIME_STRAIGHT * 2)
            self.robobo.moveWheelsByTime(-1 * self.speed, -1 * self.speed, TIME_STRAIGHT * 0.75)
            self.robobo.moveWheelsByTime(self.speed, self.speed, TIME_STRAIGHT * 0.75)
            self.robobo.moveWheelsByTime(-1 * self.speed, -1 * self.speed, TIME_STRAIGHT * 2)
        elif move == R_MOVE_RIGHT:
            # make a 45 degree turn & advance, finally revert
            self.robobo.moveWheelsByTime(-1 * self.turn_speed, self.turn_speed, TIME_TURN)
            if not lite:
                self.fwd_and_back()
                self.fwd_and_back()
            self.robobo.moveWheelsByTime(self.turn_speed, -1 * self.turn_speed, TIME_TURN)
        elif move == R_MOVE_BACK:
            # make a 90 degree turn & advance, finally revert
            self.robobo.moveWheelsByTime(-1 * self.turn_speed, self.turn_speed, TIME_TURN * 2)
            if not lite:
                self.fwd_and_back()
                self.fwd_and_back()
            self.robobo.moveWheelsByTime(self.turn_speed, -1 * self.turn_speed, TIME_TURN * 2)
        elif move == R_MOVE_LEFT:
            # make a 45 degree turn & advance, finally revert
            self.robobo.moveWheelsByTime(self.turn_speed, -1 * self.turn_speed, TIME_TURN)
            if not lite:
                self.fwd_and_back()
                self.fwd_and_back()
            self.robobo.moveWheelsByTime(-1 * self.turn_speed, -1 * self.turn_speed, TIME_TURN)
        elif move == R_MOVE_CIRCLE:
            # make a 360 degree turn
            self.robobo.moveWheelsByTime(-1 * self.turn_speed, self.turn_speed, TIME_TURN * 4.7)

    def fwd_and_back(self):
        # Sends the robot forward and then backwards to the same position
        self.robobo.moveWheelsByTime(self.speed, self.speed, TIME_STRAIGHT)
        self.robobo.moveWheelsByTime(-1 * self.speed, -1 * self.speed, TIME_STRAIGHT)

    def talk(self, phrase):
        self.robobo.sayText(phrase)

    def status(self):
        # Returns battery level as a string to display
        return [self.robobo.readBatteryLevel("base"), self.robobo.readBatteryLevel("phone")]

    def presentation(self):
        self.robobo.setEmotionTo(Emotions.NORMAL)
        self.talk("Hello. Nice to meet you")
        self.robobo.moveTiltTo(degrees=110, speed=TILT_SPEED)
        self.robobo.moveTiltTo(degrees=85, speed=TILT_SPEED)
        self.talk("I'm Robobo")
        self.robobo.setEmotionTo(Emotions.HAPPY)

    def make_action(self, situation, move="", mode=MODE_VS, one_way=False, neg_stage=NEG_STAGE_NONE, neg_option=-1):
        if not DEBUG_MODE:
            self.reset_state()

        if situation == R_SIT_START:
            if DEBUG_MODE:
                print("Lets Start!!!")
                time.sleep(DEBUG_TIME)
            else:
                self.robobo.setEmotionTo(Emotions.LAUGHING)
                self.robobo.playSound(Sounds.APPROVE)
                self.robobo.setLedColorTo(led=LED.All, color=Color.CYAN)
                self.do_movement(R_MOVE_CIRCLE)
        elif situation == R_SIT_DEAD_END:
            if DEBUG_MODE:
                print("Robobo is sad. Dead End.")
                time.sleep(DEBUG_TIME)
            else:
                self.robobo.setEmotionTo(Emotions.AFRAID)
                self.robobo.playSound(Sounds.DISAPPROVE)
                self.robobo.setLedColorTo(led=LED.All, color=Color.ORANGE)
                self.robobo.moveTiltTo(degrees=130, speed=TILT_SPEED)
                self.robobo.sayText(robotext.deadend[self.counters[C_DEADEND] % len(robotext.deadend)])
                self.counters[C_DEADEND] += 1
        elif situation == R_SIT_WIN:
            if DEBUG_MODE:
                print("WIN. HAPPY.")
                time.sleep(DEBUG_TIME)
            else:
                self.robobo.setEmotionTo(Emotions.LAUGHING)
                self.robobo.setLedColorTo(led=LED.All, color=Color.BLUE)
                self.robobo.sayText(robotext.finish)
                self.robobo.playSound(sound=Sounds.LAUGH)
                self.do_movement(R_MOVE_CIRCLE)
        elif situation == R_SIT_AUTO:
            if DEBUG_MODE:
                if self.same_sit_cnt < R_SAME_CNT:
                    print("AUTO MOVING~~")
                    time.sleep(DEBUG_TIME)
                elif self.same_sit_cnt % R_SAME_CNT == 0:
                    print("Brrooom")
                    time.sleep(DEBUG_TIME)
            else:
                self.robobo.setEmotionTo(Emotions.NORMAL)
                self.set_upper_leds(color=Color.GREEN)
                if self.same_sit_cnt < R_SAME_CNT:
                    self.robobo.setEmotionTo(Emotions.NORMAL)
                    self.robobo.movePanTo(degrees=-5, speed=PAN_SPEED * 2)
                    self.robobo.movePanTo(degrees=5, speed=PAN_SPEED * 2)
                    self.robobo.movePanTo(degrees=0, speed=PAN_SPEED)
                    self.set_upper_leds(color=Color.GREEN)
                elif self.same_sit_cnt % R_SAME_CNT == 0 and AUTO_MODE:
                    self.robobo.sayText("Brrooom")
                    self.robobo.setLedColorTo(led=LED.All, color=Color.GREEN)
        elif situation == R_SIT_BACKTRACK:
            if DEBUG_MODE:
                print("Returning...")
                time.sleep(DEBUG_TIME)
            else:
                self.robobo.setEmotionTo(Emotions.TIRED)
                self.set_upper_leds(color=Color.YELLOW)

                if self.counters[C_BACKTRACK] % 3 == 0:
                    self.robobo.playSound(Sounds.MUMBLE)
                    self.robobo.sayText(robotext.backtrack[self.counters[C_BACKTRACK] % len(robotext.backtrack)])
                else:
                    time.sleep(DEBUG_TIME)
                self.counters[C_BACKTRACK] += 1
        elif situation == R_SIT_WAITING:
            if DEBUG_MODE:
                print("Waiting for direction input...")
                time.sleep(DEBUG_TIME)
            else:
                self.robobo.setEmotionTo(Emotions.NORMAL)
                self.robobo.sayText(robotext.waiting[self.counters[C_WAITING] % len(robotext.waiting)], wait=False)
                self.set_upper_leds(color=Color.CYAN)
                self.robobo.moveTiltTo(degrees=75, speed=TILT_SPEED)
                self.counters[C_WAITING] += 1
        elif situation == R_SIT_DECIDE:
            if DEBUG_MODE:
                print("Deciding...")
                self.decision_moves(move, mode, one_way)
                time.sleep(DEBUG_TIME)
            else:
                self.robobo.setEmotionTo(Emotions.NORMAL)
                self.robobo.sayText(robotext.robot_turn[self.counters[C_TURN] % len(robotext.robot_turn)], wait=False)
                self.robobo.movePanTo(degrees=-10, speed=PAN_SPEED)
                self.robobo.movePanTo(degrees=10, speed=PAN_SPEED)
                self.robobo.movePanTo(degrees=0, speed=PAN_SPEED)
                self.set_upper_leds(color=Color.CYAN)
                self.decision_moves(move, mode, one_way)
                self.counters[C_TURN] += 1
        elif situation == R_SIT_FAIL:
            if DEBUG_MODE:
                print("Ow... We lost")
                time.sleep(DEBUG_TIME)
            else:
                self.robobo.setEmotionTo(Emotions.SAD)
                self.robobo.sayText(robotext.end_failure[1])
                self.robobo.setLedColorTo(LED.All, color=Color.RED)
                self.robobo.moveTiltTo(degrees=130, speed=TILT_SPEED)
        elif situation == R_NEG_WAITING:
            if DEBUG_MODE:
                print("Waiting for direction input...")
                self.decision_moves(move, mode, one_way, neg_stage)
                time.sleep(DEBUG_TIME)
            else:
                self.decision_moves(move, mode, one_way, neg_stage)
                self.robobo.setEmotionTo(Emotions.NORMAL)
                self.robobo.sayText(robotext.waiting[self.counters[C_WAITING] % len(robotext.waiting)])
                self.set_upper_leds(color=Color.CYAN)
                self.robobo.moveTiltTo(degrees=75, speed=TILT_SPEED)
                self.counters[C_WAITING] += 1
        elif situation == R_NEG_RND_1:
            if DEBUG_MODE:
                print("Negotiation round 1...")
                if neg_option != -1:
                    print(robotext.deciding[neg_option][3:])
                time.sleep(DEBUG_TIME)
            else:
                self.robobo.setEmotionTo(Emotions.NORMAL)
                self.robobo.playSound(Sounds.THINKING)
                self.set_upper_leds(color=Color.CYAN)
                self.robobo.moveTiltTo(degrees=100, speed=TILT_SPEED)
                if neg_option != -1:
                    self.robobo.sayText(robotext.negotiate[randint(0, len(robotext.negotiate) - 1)])
                    self.robobo.sayText(robotext.deciding[neg_option][3:])
        elif situation == R_NEG_RND_2:
            if DEBUG_MODE:
                print("Negotiation round 2...")
                if neg_option != -1:
                    print(robotext.deciding[neg_option][3:])
                self.decision_moves(move, mode, one_way, neg_stage)
                time.sleep(DEBUG_TIME)
            else:
                self.robobo.setEmotionTo(Emotions.ANGRY)
                self.set_upper_leds(color=Color.RED)
                if neg_option != -1:
                    self.robobo.sayText(robotext.deciding[neg_option][3:], False)
                self.decision_moves(move, mode, one_way, neg_stage)
        elif situation == R_NEG_AGREE:
            if DEBUG_MODE:
                print("Happy there is an agreement!")
                time.sleep(DEBUG_TIME)
            else:
                self.robobo.setEmotionTo(Emotions.HAPPY)
                self.robobo.sayText(robotext.agreement[self.counters[C_AGREEMENT] % len(robotext.agreement)])
                self.counters[C_AGREEMENT] += 1
        elif situation == R_NEG_YIELD:
            if DEBUG_MODE:
                print("It's ok.")
                time.sleep(DEBUG_TIME)
            else:
                self.robobo.sayText(robotext.negotiation_robot_yield[
                                        self.counters[C_NEG_R_YIELD] % len(robotext.negotiation_robot_yield)])
                self.robobo.setEmotionTo(Emotions.HAPPY)
                self.robobo.moveTiltTo(degrees=80, speed=round(TILT_SPEED / 2))
                self.counters[C_NEG_R_YIELD] += 1
        elif situation == R_NEG_COIN:
            if DEBUG_MODE:
                print("Tossing coin~")
            else:
                self.robobo.setEmotionTo(Emotions.NORMAL)
                if move is None:
                    self.robobo.sayText(robotext.toss_coin)
                elif move == TURN_ROBOT:
                    # print("ROBOT SIGN")
                    self.robobo.playNote(note=60, duration=0.5, wait=False)
                    self.robobo.movePanTo(degrees=-5, speed=PAN_SPEED * 2, wait=False)
                elif move == TURN_PLAYER:
                    # print("HUMAN SIGN")
                    self.robobo.playNote(note=64, duration=0.5, wait=False)
                    self.robobo.movePanTo(degrees=5, speed=PAN_SPEED * 2, wait=False)
        elif situation == R_NEG_COIN_LOSE:
            if DEBUG_MODE:
                print("Ow...Its your decision")
                time.sleep(DEBUG_TIME)
            else:
                self.robobo.setEmotionTo(Emotions.SAD)
                self.robobo.playSound(Sounds.OUCH)
                self.robobo.sayText(robotext.coin_lose[randint(0, len(robotext.coin_loss) - 1)])
                self.robobo.moveTiltTo(degrees=100, speed=round(TILT_SPEED / 2))
        elif situation == R_NEG_COIN_WIN:
            if DEBUG_MODE:
                print("I won!")
                time.sleep(DEBUG_TIME)
            else:
                self.robobo.setEmotionTo(Emotions.HAPPY)
                self.robobo.sayText(robotext.coin_win[randint(0, len(robotext.coin_win) - 1)])
                self.robobo.playSound(Sounds.LIKES)
                self.set_upper_leds(Color.GREEN)
        elif situation == R_NEG_WIN:
            if DEBUG_MODE:
                print("Yay! Thanks")
                time.sleep(DEBUG_TIME)
            else:
                self.robobo.setEmotionTo(Emotions.LAUGHING)
                self.robobo.sayText(robotext.thanks)

    def decision_moves(self, move, mode=MODE_VS, one_way=False, neg_stage=NEG_STAGE_NONE):
        decided_cue = None

        if one_way:
            if DEBUG_MODE:
                print(robotext.one_way[self.counters[C_WAITING] % len(robotext.one_way)])
            else:
                self.robobo.sayText(robotext.one_way[self.counters[C_WAITING] % len(robotext.one_way)])
        else:
            if mode == MODE_VS:
                if CUES_ORDER == "Sequential":
                    decided_cue = self.cues_counter % TOTAL_CUES
                elif CUES_ORDER == "Random":
                    decided_cue = randint(0, TOTAL_CUES - 1)
                elif CUES_ORDER == "TalkOnly":
                    decided_cue = 1
                else:
                    decided_cue = VS_CUES[self.cues_counter % TOTAL_CUES]
            else:
                if neg_stage == NEG_STAGE_START:
                    if CUES_ORDER == "Sequential":
                        decided_cue = self.cues_counter % 2        # Only decide between lite and head movement
                    elif CUES_ORDER == "Random":
                        decided_cue = randint(0, TOTAL_CUES - 2)   # Full movement cue is reserved for 2nd stage
                    elif CUES_ORDER == "TalkOnly":
                        decided_cue = 1
                    else:
                        decided_cue = COOP_CUES[self.cues_counter % 2]
                else:
                    # Both Random and Sequential share the same cue for 2nd stage: Full movement
                    decided_cue = 2
                    if CUES_ORDER == "Custom":
                        decided_cue = COOP_CUES[self.cues_counter % 2]
            self.cues_counter += 1

        if DEBUG_MODE:
            print("MOV NEG STAGE: " + str(neg_stage))
            print("DECIDED CUE: " + str(decided_cue) + ", MOVE: " + str(move))

        # Lite Movement
        if decided_cue == 0:
            if DEBUG_MODE:
                print("DO LITE MOVE")
            else:
                self.do_movement(move, lite=True)
        # Head Movement
        elif decided_cue == 1:
            if DEBUG_MODE:
                print("DO HEAD MOVE")
            else:
                self.head_movement(move)
        # Full Movement
        elif decided_cue == 2:
            if DEBUG_MODE:
                print("DO FULL MOVE")
            else:
                self.do_movement(move, lite=False)

        if not one_way:
            self.counters[C_MOVEMENT] += 1

    def head_movement(self, move):
        if move == R_MOVE_FWD:
            self.robobo.sayText(robotext.down[self.counters[C_DOWN] % len(robotext.down)])
            self.robobo.moveTiltTo(degrees=100, speed=TILT_SPEED)
            self.robobo.moveTiltTo(degrees=85, speed=TILT_SPEED)
            self.robobo.moveTiltTo(degrees=100, speed=TILT_SPEED)
            self.robobo.moveTiltTo(degrees=80, speed=int(TILT_SPEED * 0.7))
            time.sleep(0.1)
            self.robobo.moveTiltTo(degrees=80, speed=int(TILT_SPEED * 0.5))
            self.counters[C_DOWN] += 1
        elif move == R_MOVE_LEFT:
            # Note: Robobo is mirrored as it is looking to the human
            self.robobo.sayText(robotext.right[self.counters[C_RIGHT] % len(robotext.right)])
            self.robobo.movePanTo(degrees=-15, speed=PAN_SPEED * 4)
            self.robobo.movePanTo(degrees=-5, speed=PAN_SPEED * 4)
            self.robobo.movePanTo(degrees=-15, speed=PAN_SPEED * 4)
            self.robobo.movePanTo(degrees=0, speed=PAN_SPEED * 4)
            self.counters[C_LEFT] += 1
        elif move == R_MOVE_RIGHT:
            # Note: Robobo is mirrored as it is looking to the human
            self.robobo.sayText(robotext.left[self.counters[C_LEFT] % len(robotext.left)])
            self.robobo.movePanTo(degrees=15, speed=PAN_SPEED * 4)
            self.robobo.movePanTo(degrees=5, speed=PAN_SPEED * 4)
            self.robobo.movePanTo(degrees=15, speed=PAN_SPEED * 4)
            self.robobo.movePanTo(degrees=0, speed=PAN_SPEED * 4)
            self.counters[C_RIGHT] += 1
        elif move == R_MOVE_BACK:
            self.robobo.sayText(robotext.up[self.counters[C_UP] % len(robotext.up)])
            self.robobo.moveTiltTo(degrees=70, speed=TILT_SPEED)
            self.robobo.moveTiltTo(degrees=85, speed=TILT_SPEED)
            self.robobo.moveTiltTo(degrees=70, speed=TILT_SPEED)
            self.robobo.moveTiltTo(degrees=80, speed=int(TILT_SPEED * 0.7))
            time.sleep(0.1)
            self.robobo.moveTiltTo(degrees=80, speed=int(TILT_SPEED * 0.5))
            self.counters[C_UP] += 1

    def reset_state(self):
        self.robobo.setLedColorTo(LED.All, color=Color.OFF)
        self.robobo.movePanTo(degrees=0, speed=20)
        self.robobo.moveTiltTo(degrees=85, speed=20)

    def set_upper_leds(self, color):
        self.robobo.setLedColorTo(led=LED.FrontLL, color=color)
        self.robobo.setLedColorTo(led=LED.FrontC, color=color)
        self.robobo.setLedColorTo(led=LED.FrontRE, color=color)

    def test_leds(self):
        for elem in LED:
            self.robobo.setLedColorTo(led=elem, color=Color.YELLOW)
            time.sleep(0.5)

        for elem in Color:
            self.robobo.setLedColorTo(led=LED.All, color=elem)
            time.sleep(0.5)

        # Turn all off
        self.robobo.setLedColorTo(led=LED.All, color=Color.OFF)

    def test_sound(self):
        for elem in Sounds:
            self.robobo.playSound(elem)
            time.sleep(1)

    def test_faces(self):
        for elem in Emotions:
            self.robobo.setEmotionTo(elem)
            time.sleep(1)

    def test_tilt(self):
        self.robobo.moveTiltTo(degrees=85, speed=30)
        # self.robobo.moveTiltTo(degrees=5, speed=30)

    def test_pan(self):
        self.robobo.movePanTo(degrees=-160, speed=30)
        self.robobo.movePanTo(degrees=160, speed=30)
        self.robobo.movePanTo(degrees=0, speed=30)
