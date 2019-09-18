"""
	This is a simple wall follower algorithm based on
        a left hand rule.
    https://en.wikipedia.org/wiki/self_solving_algorithm#Wall_follower
    
"""
class Maze:
    def solve_maze(self):
        """
            N
        W		E
            S
        
        UP 	 	(N)	- self.get_neighbours()[0][1]
        RIGHT 	(E)	- self.get_neighbours()[1][2]
        DOWN 	(S) - self.get_neighbours()[2][1]
        LEFT 	(W) - self.get_neighbours()[1][0]
        
        """
        
        facing = "S"
        
        while self.is_self_solved() == False:
            
            left_wall = get_left_wall(facing)
            front_wall = get_front_wall(facing)
            
            if left_wall != 1:
                #facing = rotate_cw(facing)
                facing = rotate_facing(facing, "CCW")
                step_where_facing(facing)
                continue
            elif front_wall != 1:
                step_where_facing(facing)
                continue
            else:
                #facing = rotate_ccw(facing)
                facing = rotate_facing(facing, "CW")
                continue
        else:
            print("GOTCHA!!!!!")

            
    def get_left_wall(self,facing):
        if facing == "N":
            return self.get_neighbours()[1][0]
        elif facing == "E":
            return self.get_neighbours()[0][1]
        elif facing == "S":
            return self.get_neighbours()[1][2]
        elif facing == "W":
            return self.get_neighbours()[2][1]
        
    def get_front_wall(self,facing):
        if facing == "N":
            return self.get_neighbours()[0][1]
        elif facing == "E":
            return self.get_neighbours()[1][2]
        elif facing == "S":
            return self.get_neighbours()[2][1]
        elif facing == "W":
            return self.get_neighbours()[1][0]
        
    def step_where_facing(self,facing):
        if facing == "N":
            self.up()
        elif facing == "E":
            self.right()
        elif facing == "S":
            self.down()
        elif facing == "W":
            self.left()
        
    def rotate_facing(self,facing, rotation):

        directions = ["N", "E", "S", "W"]
        facindex = directions.index(facing)
        
        if rotation == "CW":
            if facindex == len(directions) - 1:
                return directions[0]
            else:
                return directions[facindex + 1]
            
        elif rotation == "CCW":
            if facindex == 0:
                return directions[-1]
            else:
                return directions[facindex - 1]

m = Maze()
m.solve_maze()