class Collisiions:
    def __init__(self) :
        self.foods_list = []
        self.snakes = []
        self.obstacles = []
        self.new_obstacles = set()

    def add_snake_to_list(self, snake):
        self.snakes.append(snake)
    
    def remove_snake_from_list(self, snake):
        self.snakes.remove(snake)

    def update_obstacles(self):
        self.obstacles.clear()
        self.new_obstacles.clear()
        for s in self.snakes:
            for b in s.snake_body: 
                self.new_obstacles.add((b[0], b[1]))
        for ob in self.new_obstacles:
            self.obstacles.append(ob)
         
 
    def check_other_snakes_collisions(self, snake):
        if len(self.snakes) >= 1:
            for snake2 in self.snakes: 
                if (snake2 != snake):
                    for segment in snake2.snake_body:
                        if (
                            abs(snake.snake_body[0][0] - segment[0]) < 1 and
                            abs(snake.snake_body[0][1] - segment[1]) < 1
                        ):  
                            return True
        return False

    def get_obstacles(self): 
        result = []
        for a in self.new_obstacles:
            result.append(a)
        return result
 
            
         

