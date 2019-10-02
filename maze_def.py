from const_def import *
import mazeclass


class MazeDef:
    MAZE_1 = []
    MAZE_2 = []

    def __init__(self):
        self.MAZE_1 = [0] * MAZE_SIZE
        self.MAZE_2 = [0] * MAZE_SIZE
        # FIRST MAZE
        self.MAZE_1[0] = [[True, False, False, True], [False, True, False, True], [False, True, False, True],
                          [False, True, False, True], [False, True, False, True], [False, True, True, True],
                          [True, False, True, True]]
        self.MAZE_1[1] = [[True, False, False, False], [False, True, False, True], [False, True, True, True],
                          [True, True, False, True], [False, True, False, True], [False, False, False, True],
                          [False, True, True, False]]
        self.MAZE_1[2] = [[True, False, False, False], [False, False, False, True], [False, True, True, True],
                          [True, False, False, True], [False, True, False, True], [False, False, False, False],
                          [False, True, True, True]]
        self.MAZE_1[3] = [[True, False, True, False], [True, False, False, False], [False, True, True, True],
                          [True, True, False, False], [False, True, True, True], [True, True, False, False],
                          [False, False, True, True]]
        self.MAZE_1[4] = [[True, True, True, False], [True, False, True, False], [True, False, False, True],
                          [False, True, False, True], [False, False, True, True], [True, True, False, True],
                          [False, False, True, False]]
        self.MAZE_1[5] = [[True, False, True, True], [True, False, True, False], [True, True, True, False],
                          [True, False, False, True], [False, True, False, False], [False, True, False, True],
                          [False, False, True, False]]
        self.MAZE_1[6] = [[True, True, False, False], [False, True, False, False], [False, True, False, True],
                          [False, True, False, False], [False, True, True, True], [True, True, False, True],
                          [True, True, False, True]]

        # SECOND MAZE
        self.MAZE_2[0] = [[True, False, False, True], [False, True, False, True], [False, False, False, True],
                          [False, False, True, True], [True, True, False, True], [False, False, False, True],
                          [False, False, True, True]]
        self.MAZE_2[1] = [[True, False, False, False], [False, False, True, True], [True, True, True, False],
                          [True, False, True, False], [True, False, True, True], [True, True, True, False],
                          [True, False, True, False]]
        self.MAZE_2[2] = [[True, True, True, False], [True, True, False, False], [False, True, True, True],
                          [True, False, True, False], [True, False, True, False], [True, False, False, True],
                          [False, True, True, False]]
        self.MAZE_2[3] = [[True, False, True, True], [True, False, True, True], [True, True, False, True],
                          [False, True, False, False], [False, True, False, False], [False, False, True, False],
                          [True, False, True, True]]
        self.MAZE_2[4] = [[True, True, False, False], [False, False, False, False], [False, False, True, True],
                          [True, False, False, True], [False, True, False, True], [False, True, False, False],
                          [False, False, True, False]]
        self.MAZE_2[5] = [[True, False, False, True], [False, True, True, False], [True, False, False, False],
                          [False, True, True, False], [True, False, True, True], [True, False, True, True],
                          [True, False, True, False]]
        self.MAZE_2[6] = [[True, True, True, False], [True, True, False, True], [False, True, True, False],
                          [True, True, False, True], [False, True, False, False], [False, True, False, False],
                          [False, True, True, False]]

    def gen_maze(self, maze):
        for i in range(0, MAZE_SIZE):
            for j in range(0, MAZE_SIZE):
                if FIXED_MAP == 1:
                    maze.mmap[i][j].walls = self.MAZE_1[i][j]
                else:
                    maze.mmap[i][j].walls = self.MAZE_2[i][j]
        return maze
