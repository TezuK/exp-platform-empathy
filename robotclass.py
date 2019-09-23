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
import robotext


class Robot:

    def __init__(self, robot_ip):
        # Initialize the connection
        self.speed = 30
        self.turn_speed = 20
        self.robobo = Robobo(robot_ip)
        self.same_sit_cnt = 1
        self.counters = [0, 0, 0, 0]
        self.prev_sit = None
        if not DEBUG_MODE:
            self.robobo.connect()
    
    def end(self):
        self.robobo.stopMotors()
        self.robobo.disconnect()

    def do_movement(self, move, lite=False):
        if move == R_MOVE_FWD:
            self.robobo.moveWheelsByTime(self.speed, self.speed, TIME_STRAIGHT*2)
            self.robobo.moveWheelsByTime(-1 * self.speed, -1*self.speed, TIME_STRAIGHT*0.75)
            self.robobo.moveWheelsByTime(self.speed, self.speed, TIME_STRAIGHT*0.75)
            self.robobo.moveWheelsByTime(-1 * self.speed, -1*self.speed, TIME_STRAIGHT*2)
        elif move == R_MOVE_RIGHT:
            # make a 45 degree turn & advance, finally revert
            self.robobo.moveWheelsByTime(-1 * self.turn_speed, self.turn_speed, TIME_TURN)
            if not lite:
                self.fwd_and_back()
                self.fwd_and_back()
            self.robobo.moveWheelsByTime(self.turn_speed, -1*self.turn_speed, TIME_TURN)
        elif move == R_MOVE_BACK:
            # make a 90 degree turn & advance, finally revert
            self.robobo.moveWheelsByTime(-1*self.turn_speed, self.turn_speed, TIME_TURN * 2)
            if not lite:
                self.fwd_and_back()
                self.fwd_and_back()
            self.robobo.moveWheelsByTime(self.turn_speed, -1*self.turn_speed, TIME_TURN * 2)
        elif move == R_MOVE_LEFT: 
            # make a 45 degree turn & advance, finally revert
            self.robobo.moveWheelsByTime(self.turn_speed, -1*self.turn_speed, TIME_TURN)
            if not lite:
                self.fwd_and_back()
                self.fwd_and_back()
            self.robobo.moveWheelsByTime(-1*self.turn_speed, -1*self.turn_speed, TIME_TURN)
        elif move == R_MOVE_CIRCLE:
            # make a 360 degree turn
            self.robobo.moveWheelsByTime(-1*self.turn_speed, self.turn_speed, TIME_TURN * 4.7)
        
    def fwd_and_back(self):
        # Sends the robot forward and then backwards to the same position
        self.robobo.moveWheelsByTime(self.speed, self.speed, TIME_STRAIGHT)
        self.robobo.moveWheelsByTime(-1*self.speed, -1*self.speed, TIME_STRAIGHT)
        
    def talk(self, phrase):
        self.robobo.sayText(phrase)
    
    def status(self):
        # Returns battery level as a string to display
        return self.robobo.readBatteryLevel()
        
    def presentation(self):
        self.robobo.setEmotionTo(Emotions.NORMAL)
        self.talk("Hello. Nice to meet you")
        self.robobo.moveTiltTo(degrees=110, speed=TILT_SPEED)
        self.robobo.moveTiltTo(degrees=85, speed=TILT_SPEED)
        self.talk("I'm Robobo")
        self.robobo.setEmotionTo(Emotions.HAPPY)

    def make_action(self, situation, move="", mode=MODE_VS, one_way=False, neg_stage=NEG_STAGE_NONE):
        if not DEBUG_MODE:
            self.reset_state()

        if situation == R_SIT_START:
            if DEBUG_MODE:
                print("Lets Start!!!")
            else:
                self.robobo.setEmotionTo(Emotions.LAUGHING)
                self.robobo.playSound(Sounds.APPROVE)
                self.robobo.setLedColorTo(led=LED.All, color=Color.CYAN)
                self.do_movement(R_MOVE_CIRCLE)
        elif situation == R_SIT_DEAD_END:
            if DEBUG_MODE:
                print("Robobo is sad. Dead End.")
            else:
                self.robobo.setEmotionTo(Emotions.AFRAID)
                self.robobo.playSound(Sounds.DISAPPROVE)
                self.robobo.setLedColorTo(led=LED.All, color=Color.ORANGE)
                self.robobo.moveTiltTo(degrees=130, speed=TILT_SPEED)
                self.robobo.sayText("We need to go back")
        elif situation == R_SIT_WIN:
            if DEBUG_MODE:
                print("WIN. HAPPY.")
            else:
                self.robobo.setEmotionTo(Emotions.HAPPY)
                self.robobo.setLedColorTo(led=LED.All, color=Color.BLUE)
                self.robobo.playSound(sound=Sounds.LAUGH)
                self.do_movement(R_MOVE_CIRCLE)
        elif situation == R_SIT_MOVING:
            if DEBUG_MODE:
                if self.same_sit_cnt < R_SAME_CNT:
                    print("AUTO MOVING~~")
                elif self.same_sit_cnt % R_SAME_CNT == 0:
                    print("Brrooom")
            else:
                self.robobo.setEmotionTo(Emotions.NORMAL)
                self.set_upper_leds(color=Color.GREEN)
                if self.same_sit_cnt < R_SAME_CNT:
                    self.robobo.setEmotionTo(Emotions.NORMAL)
                    self.robobo.movePanTo(degrees=-5, speed=PAN_SPEED*2)
                    self.robobo.movePanTo(degrees=5, speed=PAN_SPEED*2)
                    self.robobo.movePanTo(degrees=0, speed=PAN_SPEED)
                    self.set_upper_leds(color=Color.GREEN)
                elif self.same_sit_cnt % R_SAME_CNT == 0 and AUTO_MODE:
                    self.robobo.sayText("Brrooom")
                    self.robobo.setLedColorTo(led=LED.All, color=Color.GREEN)
        elif situation == R_SIT_BACKTRACK:
            if DEBUG_MODE:
                print("Returning...")
            else:
                self.robobo.setEmotionTo(Emotions.TIRED)
                self.robobo.playSound(Sounds.MUMBLE)
                self.set_upper_leds(color=Color.YELLOW)
        elif situation == R_SIT_WAITING:
            if DEBUG_MODE:
                print("Waiting for direction input...")
            else:
                self.robobo.sayText(robotext.waiting[self.same_sit_cnt % len(robotext.waiting)])
                #print(robotext.waiting[self.counters[C_WAITING] % len(robotext.waiting)])

                self.counters[C_WAITING] += 1

                self.set_upper_leds(color=Color.CYAN)
                self.robobo.moveTiltTo(degrees=100, speed=TILT_SPEED)
        elif situation == R_SIT_DECIDE:
            if DEBUG_MODE:
                print("Deciding...")
                time.sleep(1)
            else:
                self.robobo.sayText(robotext.waiting[self.same_sit_cnt % len(robotext.waiting)])
                #print(robotext.robot_turn[self.counters[C_TURN] % len(robotext.robot_turn)])

                self.robobo.movePanTo(degrees=-10, speed=PAN_SPEED)
                self.robobo.movePanTo(degrees=10, speed=PAN_SPEED)
                self.robobo.movePanTo(degrees=0, speed=PAN_SPEED)
                self.set_upper_leds(color=Color.CYAN)

                self.base_moves(move, mode, one_way)
                self.counters[C_TURN] += 1
        elif situation == R_NEG_WAITING:
            if DEBUG_MODE:
                print("Waiting for direction input...")
            else:
                self.base_moves(move, mode, one_way, neg_stage)

                self.robobo.sayText(robotext.waiting[self.same_sit_cnt % len(robotext.waiting)])
                #print(robotext.waiting[self.counters[C_WAITING] % len(robotext.waiting)])

                self.set_upper_leds(color=Color.CYAN)
                self.robobo.moveTiltTo(degrees=75, speed=TILT_SPEED)
                self.counters[C_WAITING] += 1
        elif situation == R_NEG_RND_1:
            if DEBUG_MODE:
                print("Negotiation round 1...")
            else:
                self.robobo.playSound(Sounds.THINKING)
                self.set_upper_leds(color=Color.CYAN)
                self.robobo.moveTiltTo(degrees=100, speed=TILT_SPEED)
        elif situation == R_NEG_AGREE:
            if DEBUG_MODE:
                print("Happy there is an agreement!")
            else:
                self.robobo.setEmotionTo(Emotions.HAPPY)

                self.robobo.sayText(robotext.waiting[self.same_sit_cnt % len(robotext.waiting)])
                #print(robotext.agreement[self.counters[C_AGREEMENT] % len(robotext.agreement)])
                self.counters[C_AGREEMENT] += 1
        elif situation == R_NEG_YIELD:
            if DEBUG_MODE:
                print("It's ok.")
            else:
                self.robobo.sayText("Let's try it your way")
                self.robobo.setEmotionTo(Emotions.HAPPY)
                self.robobo.moveTiltTo(degrees=80, speed=round(TILT_SPEED/2))
        elif situation == R_NEG_COIN:
            if DEBUG_MODE:
                print("Tossing coin~")
            else:
                if move == TURN_ROBOT:
                    #print("ROBOT SIGN")
                    self.robobo.playNote(note=60, duration=0.5, wait=False)
                    self.robobo.movePanTo(degrees=-5, speed=PAN_SPEED*2, wait=False)
                elif move == TURN_PLAYER:
                    #print("HUMAN SIGN")
                    self.robobo.playNote(note=64, duration=0.5, wait=False)
                    self.robobo.movePanTo(degrees=5, speed=PAN_SPEED*2, wait=False)
        elif situation == R_NEG_LOSE:
            if DEBUG_MODE:
                print("Ow...Its your decision")
            else:
                self.robobo.setEmotionTo(Emotions.SAD)
                self.robobo.playSound(Sounds.OUCH)
                self.robobo.moveTiltTo(degrees=100, speed=round(TILT_SPEED/2))
        elif situation == R_NEG_WIN:
            if DEBUG_MODE:
                print("Yay! Thanks")
            else:
                self.robobo.setEmotionTo(Emotions.HAPPY)
                self.robobo.sayText("Thanks!")

    def base_moves(self, move, mode=MODE_VS, one_way=False, neg_stage=NEG_STAGE_NONE):

        if one_way:
            self.robobo.sayText(robotext.one_way[self.same_sit_cnt % len(robotext.one_way)])
            #print(robotext.one_way[self.counters[C_WAITING] % len(robotext.one_way)])
        elif (mode == MODE_VS and self.counters[C_MOVEMENT] % 3 == 0)\
                or (mode == MODE_COOP and neg_stage == NEG_STAGE_START):
            self.do_movement(move, lite=True)
            #print("DO LITE MOVE")
        elif (mode == MODE_VS and self.counters[C_MOVEMENT] % 3 == 1)\
                or (mode == MODE_COOP and neg_stage == NEG_STAGE_2):
            self.do_movement(move, lite=False)
            #print("DO FULL MOVE")
        else:
            if move == R_MOVE_FWD:
                self.robobo.moveTiltTo(degrees=100, speed=TILT_SPEED * 4)
                self.robobo.moveTiltTo(degrees=95, speed=TILT_SPEED * 4)
                self.robobo.sayText("Down")
                self.robobo.moveTiltTo(degrees=100, speed=TILT_SPEED * 4)
                self.robobo.moveTiltTo(degrees=85, speed=TILT_SPEED * 4)
            elif move == R_MOVE_LEFT:
                # Note: Robobo is mirrored as it is looking to the human
                self.robobo.movePanTo(degrees=-15, speed=PAN_SPEED * 4)
                self.robobo.movePanTo(degrees=-5, speed=PAN_SPEED * 4)
                self.robobo.sayText("Right")
                self.robobo.movePanTo(degrees=-15, speed=PAN_SPEED * 4)
                self.robobo.movePanTo(degrees=0, speed=PAN_SPEED * 4)
            elif move == R_MOVE_RIGHT:
                # Note: Robobo is mirrored as it is looking to the human
                self.robobo.movePanTo(degrees=15, speed=PAN_SPEED * 4)
                self.robobo.movePanTo(degrees=5, speed=PAN_SPEED * 4)
                self.robobo.sayText("Left")
                self.robobo.movePanTo(degrees=15, speed=PAN_SPEED * 4)
                self.robobo.movePanTo(degrees=0, speed=PAN_SPEED * 4)
            elif move == R_MOVE_BACK:
                self.robobo.moveTiltTo(degrees=70, speed=TILT_SPEED * 4)
                self.robobo.moveTiltTo(degrees=80, speed=TILT_SPEED * 4)
                self.robobo.sayText("Up")
                self.robobo.moveTiltTo(degrees=70, speed=TILT_SPEED * 4)
                self.robobo.moveTiltTo(degrees=85, speed=TILT_SPEED * 4)

        if not one_way:
            self.counters[C_MOVEMENT] += 1

    def reset_state(self):
        self.robobo.setEmotionTo(Emotions.NORMAL)
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
        #self.robobo.moveTiltTo(degrees=5, speed=30)

    def test_pan(self):
        self.robobo.movePanTo(degrees=-160, speed=30)
        self.robobo.movePanTo(degrees=160, speed=30)
        self.robobo.movePanTo(degrees=0, speed=30)