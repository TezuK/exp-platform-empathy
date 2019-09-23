from const_def import *
import time
from random import randint


class Negotiation:

    def __init__(self):
        # Argument descriptions for the screen display
        self.arg_description = ["1. I've decided the most, let me lead",
                                "2. You chose the most, now let me!",
                                "3. Your decisions took us to dead ends",
                                "4. Just toss a coin and get it over with",
                                "5. Fine, let's do it your way"]
        # All arguments should be available at the start
        self.arg_avail_robot = [True, True, True, True, True]
        self.arg_avail_human = [True, True, True, True, True]

    def check_arg_availability(self, decisions_taken=[0, 0], deadend_count=[0, 0], emotion=EMOTION_NEUTRAL):
        # This method is to DISCARD any argument that is not applicable
        # Each condition is independent so it should be evaluated without anidating it.
        # First check the number of decisions taken
        if decisions_taken[0] >= decisions_taken[1]:
            self.arg_avail_human[0] = False
            self.arg_avail_robot[1] = False
        if decisions_taken[0] <= decisions_taken[1]:
            self.arg_avail_human[1] = False
            self.arg_avail_robot[0] = False

        # Dead end count
        if deadend_count[0] >= deadend_count[1]:
            self.arg_avail_robot[2] = False
        if deadend_count[0] <= deadend_count[1]:
            self.arg_avail_human[2] = False

        # If the human is angry then yield always
        if emotion == EMOTION_ANGRY:
            self.arg_avail_robot = [False, False, False, False, True]

    def get_display_msg(self):
        # Gets the possible arguments that the human has and puts it in the display string format
        message = ["What do you say?"]

        for i in range(0, len(self.arg_avail_human)):
            if self.arg_avail_human[i]:
                message.append(self.arg_description[i])

        return message

    def mark_as_used(self, is_robot=True, arg_number=0):
        if is_robot:
            self.arg_avail_robot[arg_number] = False
        else:
            self.arg_avail_human[arg_number] = False

    def choose_first_avail(self):
        print("AVAIL: " + str(self.arg_avail_robot))
        for i in range(0, len(self.arg_avail_robot)):
            if self.arg_avail_robot[i]:
                # If it is the coin toss, do the percentage
                if i != P_NEG_COIN or (i == P_NEG_COIN and randint(0, 100) < COIN_PERCENTAGE):
                    return i
                else:
                    return i + 1

    def is_the_only_choice(self, is_robot=True, arg_number=0):
        result = True

        if is_robot:
            t_list = self.arg_avail_robot
        else:
            t_list = self.arg_avail_human

        # if anyone except for the one selected is False, then it will return True
        for i in range(0, len(t_list)):
            if i != arg_number:
                result = result and not t_list[i]

        return result

    def reset(self):
        self.arg_avail_robot = [True, True, True, True, True]
        self.arg_avail_human = [True, True, True, True, True]
