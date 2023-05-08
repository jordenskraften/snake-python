class SnakeAI:
    def __init__(self, width, height, collisions, snake, food):
        self.grid_width = width
        self.grid_height = height
        self.collisions = collisions
        self.snake = snake
        self.food = food 

    def create_path(self):  
        s_x = self.snake.snake_head_pos[0]
        s_y = self.snake.snake_head_pos[1]
        start = (s_x, s_y)

        e_x = self.food.food_pos[0]
        e_y = self.food.food_pos[1]
        end = (e_x, e_y)

        new_dir = (
                end[0] - start[0],
                end[1] - start[1]
        ) 
        self.snake.ai_change_direction(new_dir)
         
      