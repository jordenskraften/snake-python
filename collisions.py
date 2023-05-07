class Collisiions:
    def __init__(self) :
        self.foods_list = []
        self.snakes = []
        self.obstacles = set()

    def add_snake_to_list(self, snake):
        self.snakes.append(snake)
    
    def remove_snake_from_list(self, snake):
        self.snakes.remove(snake)

    def update_obstacles(self):
        self.obstacles.clear()
        for s in self.snakes:
            for b in s.snake_body: 
                self.obstacles.add((b[0], b[1]))
         
 
    def check_other_snakes_collisions(self, snake):
        if len(self.snakes) >= 1:
            for snake2 in self.snakes: 
                if (snake2 != snake):
                    for segment in snake2.snake_body:
                        if snake.snake_body[0][0] == segment[0] and snake.snake_body[0][1] == segment[1]: 
                            print(f"{snake.snake_body[-1]} {snake.snake_body[0]} {snake.snake_head_pos} {segment}")
                            print("----------------") 
                            return True
        return False

    def get_obstacles(self): 
        return self.obstacles
 
            
         

