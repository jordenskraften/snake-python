import heapq 
import math
from keyboard_inputs import MovementDirection
 
class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position
class SnakeAI:
    def __init__(self, width, height, collisions, snake, food):
        self.grid_width = width
        self.grid_height = height
        self.collisions = collisions
        self.snake = snake
        self.food = food 

    def create_path(self): 
        maze = [[0 for j in range(self.grid_width)] for i in range(self.grid_height)]     
        j = 1
        columns = len([row[j] for row in maze]) 
        rows = len(maze[0])  
        #print(maze[columns-1][rows-1])
        obstacles = self.collisions.get_obstacles()    
        for i in range(0, columns-1):
            for j in range(0, rows-1):
                if (i,j) in obstacles: 
                    if maze[i][j] != None:
                        maze[i][j] = 1 
 
        #for col in range(0, columns-1):
            #print(maze[col])  

        s_x = self.snake.snake_head_pos[0]
        s_y = self.snake.snake_head_pos[1]
        start = (s_x, s_y)

        e_x = self.food.food_pos[0]
        e_y = self.food.food_pos[1]
        end = (e_x, e_y)
        #print(f"{type(start)} {start} {type(end)} {end}")    
        new_dir = (
                end[0] - start[0],
                end[1] - start[1]
        ) 
        print(new_dir)
        self.snake.ai_change_direction(new_dir)
         
      