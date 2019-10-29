from const_def import *
import mazeclass
from maze_def import MazeDef
from datetime import datetime
from random import randint


def check_if_visible(pos_x, pos_y, robot_map):
    if robot_map[pos_x][pos_y] != BLOCK_UNKNOWN or \
            (SHOW_ADJACENT and (((pos_x - 1 >= 0) and (robot_map[pos_x - 1][pos_y] != BLOCK_UNKNOWN)) or
                                ((pos_x + 1 < MAZE_SIZE) and (robot_map[pos_x + 1][pos_y] != BLOCK_UNKNOWN)) or
                                ((pos_y - 1 >= 0) and (robot_map[pos_x][pos_y - 1] != BLOCK_UNKNOWN)) or
                                ((pos_y + 1 < MAZE_SIZE) and (robot_map[pos_x][pos_y + 1] != BLOCK_UNKNOWN)))):
        return True

    return False


def maze_generation(maze_size, maze_type):
    if maze_type == "full":
        # whole map generation in random
        maze = mazeclass.Map()
        maze.gen_map(maze_size, maze_size)

        if FIXED_MAP != 0:
            maze_def = MazeDef()
            maze = maze_def.gen_maze(maze)
    else:
        # blank map, just for positions
        maze = [[BLOCK_UNKNOWN for j in range(maze_size)] for i in range(maze_size)]
        maze[0][0] = BLOCK_CURRENT

    return maze


def maze_solving(maze, robot_map, current_pos):
    walls = maze.mmap[current_pos[0]][current_pos[1]].walls
    available = []

    # Right hand rule (adapted to perspective)
    # Doing it without "if chains" because of possible array position violations [-1]
    backtrack = False
    one_way = False
    special = False

    # Get discarded & passed walls
    walls_discarded = get_number_walls(robot_map, current_pos, walls, BLOCK_DISCARD)
    walls_passed = get_number_walls(robot_map, current_pos, walls, BLOCK_PASS)

    # Find if we have to backtrack
    if sum(walls) + walls_discarded == 3 and current_pos != [0, 0]:
        backtrack = True
        # If we have to backtrack, then consider player discarded actions
        robot_map = replace_conflict(robot_map)
    elif sum(walls) + walls_discarded + walls_passed == 3:
        one_way = True

    # If the path down is open & is not the end, go down
    if not walls[WALL_BOTTOM] and current_pos[1] != MAZE_SIZE - 1:
        # Only if it is not discarded
        if robot_map[current_pos[0]][current_pos[1] + 1] != BLOCK_DISCARD \
                and (robot_map[current_pos[0]][current_pos[1] + 1] != BLOCK_PASS or backtrack) \
                and (robot_map[current_pos[0]][current_pos[1] + 1] != BLOCK_CONFLICT or backtrack):
            available.append([current_pos[0], current_pos[1] + 1])
    # If the right path is open & is not the end, go right
    if not walls[WALL_RIGHT] and current_pos[0] != MAZE_SIZE - 1:
        # Only if it is not discarded
        if robot_map[current_pos[0] + 1][current_pos[1]] != BLOCK_DISCARD \
                and (robot_map[current_pos[0] + 1][current_pos[1]] != BLOCK_PASS or backtrack) \
                and (robot_map[current_pos[0] + 1][current_pos[1]] != BLOCK_CONFLICT or backtrack):
            available.append([current_pos[0] + 1, current_pos[1]])
    # If the path up is open & is not the beginning, go up
    if not walls[WALL_TOP] and current_pos[1] != 0:
        # Only if it is not discarded
        if robot_map[current_pos[0]][current_pos[1] - 1] != BLOCK_DISCARD \
                and (robot_map[current_pos[0]][current_pos[1] - 1] != BLOCK_PASS or backtrack) \
                and (robot_map[current_pos[0]][current_pos[1] - 1] != BLOCK_CONFLICT or backtrack):
            available.append([current_pos[0], current_pos[1] - 1])
    # If the right path is open & is not the end, go right
    if not walls[WALL_LEFT] and current_pos[0] != 0:
        # Only if it is not discarded
        if robot_map[current_pos[0] - 1][current_pos[1]] != BLOCK_DISCARD \
                and (robot_map[current_pos[0] - 1][current_pos[1]] != BLOCK_PASS or backtrack) \
                and (robot_map[current_pos[0] - 1][current_pos[1]] != BLOCK_CONFLICT or backtrack):
            available.append([current_pos[0] - 1, current_pos[1]])

    # SPECIAL LOGIC FOR USER MISGIVINGS, CONVERTING PASSED BLOCK TO CONFLICT ONES
    if len(available) == 0:
        special = True
        # If the path down is open & is not the end, go down
        if not walls[WALL_BOTTOM] and current_pos[1] != MAZE_SIZE - 1:
            # Only if it is not discarded
            if robot_map[current_pos[0]][current_pos[1] + 1] == BLOCK_PASS:
                available.append([current_pos[0], current_pos[1] + 1])
        # If the right path is open & is not the end, go right
        if not walls[WALL_RIGHT] and current_pos[0] != MAZE_SIZE - 1:
            # Only if it is not discarded
            if robot_map[current_pos[0] + 1][current_pos[1]] == BLOCK_PASS:
                available.append([current_pos[0] + 1, current_pos[1]])
        # If the path up is open & is not the beginning, go up
        if not walls[WALL_TOP] and current_pos[1] != 0:
            # Only if it is not discarded
            if robot_map[current_pos[0]][current_pos[1] - 1] == BLOCK_PASS:
                available.append([current_pos[0], current_pos[1] - 1])
        # If the right path is open & is not the end, go right
        if not walls[WALL_LEFT] and current_pos[0] != 0:
            # Only if it is not discarded
            if robot_map[current_pos[0] - 1][current_pos[1]] == BLOCK_PASS:
                available.append([current_pos[0] - 1, current_pos[1]])

    if len(available) == 0:
        # SPECIAL LOGIC FOR USER EXTRA MISGIVINGS, CONVERTING PASSED CONFLICT TO CURRENT
        special = True
        # If the path down is open & is not the end, go down
        if not walls[WALL_BOTTOM] and current_pos[1] != MAZE_SIZE - 1:
            # Only if it is not discarded
            if robot_map[current_pos[0]][current_pos[1] + 1] == BLOCK_CONFLICT:
                available.append([current_pos[0], current_pos[1] + 1])
        # If the right path is open & is not the end, go right
        if not walls[WALL_RIGHT] and current_pos[0] != MAZE_SIZE - 1:
            # Only if it is not discarded
            if robot_map[current_pos[0] + 1][current_pos[1]] == BLOCK_CONFLICT:
                available.append([current_pos[0] + 1, current_pos[1]])
        # If the path up is open & is not the beginning, go up
        if not walls[WALL_TOP] and current_pos[1] != 0:
            # Only if it is not discarded
            if robot_map[current_pos[0]][current_pos[1] - 1] == BLOCK_CONFLICT:
                available.append([current_pos[0], current_pos[1] - 1])
            # If the right path is open & is not the end, go right
        if not walls[WALL_LEFT] and current_pos[0] != 0:
            # Only if it is not discarded
            if robot_map[current_pos[0] - 1][current_pos[1]] == BLOCK_CONFLICT:
                available.append([current_pos[0] - 1, current_pos[1]])

    if len(available) != 0:
        if RANDOM_SELECT:
            return [available[randint(0, len(available)-1)], backtrack, one_way, special]
        else:
            return [available[0], backtrack, one_way, special]
    else:
        return [[0, 0], False, False, True]


def get_number_walls(robot_map, current_pos, walls, wall_type):
    total = 0

    if not walls[WALL_BOTTOM] and robot_map[current_pos[0]][current_pos[1] + 1] == wall_type:
        total += 1
    if not walls[WALL_RIGHT] and robot_map[current_pos[0] + 1][current_pos[1]] == wall_type:
        total += 1
    if not walls[WALL_TOP] and robot_map[current_pos[0]][current_pos[1] - 1] == wall_type:
        total += 1
    if not walls[WALL_LEFT] and robot_map[current_pos[0] - 1][current_pos[1]] == wall_type:
        total += 1

    return total


def move_position(robot_map, current_pos, next_pos, prev_pos, backtrack):
    if robot_map[current_pos[0]][current_pos[1]] == BLOCK_CONFLICT:
        # if this block has been marked as conflict on purpose then mantain it
        # if it is the first block then reconvert all to unkown
        if current_pos == [0, 0]:
            robot_map = replace_conflict(robot_map)
    elif next_pos == prev_pos and not backtrack:
        # If there is a backtracking on purpose by the user without need, then erase the last block data
        # this is because future actions may be affected by that
        robot_map[current_pos[0]][current_pos[1]] = BLOCK_CONFLICT
    elif robot_map[next_pos[0]][next_pos[1]] == BLOCK_PASS:
        # if we are backtracking then mark the previous block as discarded
        robot_map[current_pos[0]][current_pos[1]] = BLOCK_DISCARD
    else:
        robot_map[current_pos[0]][current_pos[1]] = BLOCK_PASS

    robot_map[next_pos[0]][next_pos[1]] = BLOCK_CURRENT

    return robot_map


def move_translate(current_pos, robot_input):
    if robot_input == [current_pos[0], current_pos[1] - 1]:
        return R_MOVE_BACK
    elif robot_input == [current_pos[0] + 1, current_pos[1]]:
        return R_MOVE_LEFT
    elif robot_input == [current_pos[0], current_pos[1] + 1]:
        return R_MOVE_FWD
    elif robot_input == [current_pos[0] - 1, current_pos[1]]:
        return R_MOVE_RIGHT

    return None


def input_to_pos(current_pos, player_input):
    if player_input == PLAYER_UP and current_pos[1] != 0:
        return [current_pos[0], current_pos[1] - 1]
    elif player_input == PLAYER_RIGHT and current_pos[0] != MAZE_SIZE - 1:
        return [current_pos[0] + 1, current_pos[1]]
    elif player_input == PLAYER_DOWN and current_pos[1] != MAZE_SIZE - 1:
        return [current_pos[0], current_pos[1] + 1]
    elif player_input == PLAYER_LEFT and current_pos[0] != 0:
        return [current_pos[0] - 1, current_pos[1]]

    # If it hasn't entered in any condition then the input is not valid
    return None


def pos_to_input(current_pos, robot_input):
    if robot_input == [current_pos[0], current_pos[1] - 1]:
        return PLAYER_UP
    elif robot_input == [current_pos[0] + 1, current_pos[1]]:
        return PLAYER_RIGHT
    elif robot_input == [current_pos[0], current_pos[1] + 1]:
        return PLAYER_DOWN
    elif robot_input == [current_pos[0] - 1, current_pos[1]]:
        return PLAYER_LEFT

    # If it hasn't entered in any condition then the input is not valid
    return None


def check_if_valid(maze, robot_map, current_pos, map_choice):
    walls = maze.mmap[current_pos[0]][current_pos[1]].walls

    if map_choice is not None:
        # If the player wants to go down
        if map_choice[0] == current_pos[0] and map_choice[1] == current_pos[1] + 1:
            if not walls[WALL_BOTTOM] and current_pos[1] != MAZE_SIZE - 1:
                return True

        # If the player wants to go right
        elif map_choice[0] == current_pos[0] + 1 and map_choice[1] == current_pos[1]:
            if not walls[WALL_RIGHT] and current_pos[0] != MAZE_SIZE - 1:
                return True

        # If the player wants to go up
        elif map_choice[0] == current_pos[0] and map_choice[1] == current_pos[1] - 1:
            if not walls[WALL_TOP] and current_pos[1] != 0:
                return True

        # If the player wants to go left
        elif map_choice[0] == current_pos[0] - 1 and map_choice[1] == current_pos[1]:
            if not walls[WALL_LEFT] and current_pos[0] != 0:
                return True

    return False


def replace_conflict(robot_map):
    # This procedure converts all conflict blocks into unknown so they can be traversed
    # with priority over already passed blocks by consensus
    for j in range(MAZE_SIZE):
        for i in range(MAZE_SIZE):
            if robot_map[i][j] == BLOCK_CONFLICT:
                robot_map[i][j] = BLOCK_UNKNOWN

    return robot_map


def write_log(current_mov=[], game_mode="", turn_count=-1, player="", one_way=False, backtracking=False,
              emotion=None, negotiation=False, neg_time=0.0, neg_reason="", summary=False, total_time=0.0, neg_count=0):
    file = open("logs.txt", "a+")
    message = ""

    if turn_count == 1:
        message += "[" + str(datetime.now()) + "] *" + game_mode + " MODE START*\n"

    if LOG_SHOW_TIMESTAMP:
        message += "[" + str(datetime.now()) + "] "

    if summary:
        message = "*SUMMARY* | TOTAL TURNS: " + str(turn_count) + " | TOTAL TIME: " + str(total_time)
        if game_mode == MODE_COOP:
            message += " | NEGOTIATIONS: " + str(neg_count)
    elif current_mov == [] and emotion is not None:
        message += "*EMOTION CHANGE* | " + str(emotion)
    elif negotiation:
        message += "*NEGOTIATION* | WINNER: " + player + " | TIME: " + str(neg_time) + " | REASON: " + neg_reason
    else:
        if backtracking:
            player = "BACKTRACKING"
        elif one_way and AUTO_MODE:
            player = "AUTO"

        if LOG_SHOW_EMOTION:
            message += "EMOTION: " + emotion + " | "

        if LOG_SHOW_TURN:
            message += "TURN: " + str(turn_count) + " | "

        if game_mode == MODE_VS:
            message += player + " | "

        if LOG_SHOW_MOVEMENT:
            message += "MOVE => [" + str(current_mov[0]) + "," + str(current_mov[1]) + "]"

    file.write(message + "\n")
    file.close()
