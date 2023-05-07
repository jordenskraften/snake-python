import pygame  
from collisions import Collisiions
from keyboard_inputs import MovementDirection
  
class Snake:
    def __init__(self, surface, game_rect, collisions, is_ai = False): 
        self.surface = surface
        self.game_rect = game_rect
        self.color = (0, 0, 255) 
        self.DRAWING_OFFSET_X = self.game_rect.x
        self.DRAWING_OFFSET_Y = self.game_rect.y
        self.COORDS_WIDTH = game_rect.width // 10
        self.COORDS_HEIGHT = game_rect.height // 10
        self.snake_spawn_x = self.COORDS_WIDTH // 2
        self.snake_spawn_y = self.COORDS_HEIGHT // 2 
        self.is_ai = is_ai
        self.snake_head_pos = [self.snake_spawn_x, self.snake_spawn_y]
        if self.is_ai == True: 
            self.snake_head_pos = [3, 3]
            self.color = (255, 125, 125) 
        self.snake_body = [self.snake_head_pos]  
        self.direction = MovementDirection.RIGHT
        self.change_to = self.direction
        self.score = 0
        self.collisions = collisions

    def clear(self):
        self.surface = None
        self.game_rect = None
        self.color = None
        self.DRAWING_OFFSET_X = None
        self.DRAWING_OFFSET_Y = None
        self.COORDS_WIDTH = None
        self.COORDS_HEIGHT = None
        self.snake_spawn_x = None
        self.snake_spawn_y = None
        self.is_ai = None
        self.snake_head_pos = None 
        self.snake_body = None
        self.direction = None
        self.change_to = None
        self.score = None
        self.collisions = None

    def validate_direction_and_change(self):
        if any((
            self.change_to == MovementDirection.UP and not self.direction == MovementDirection.DOWN, 
            self.change_to == MovementDirection.DOWN and not self.direction == MovementDirection.UP, 
            self.change_to == MovementDirection.LEFT and not self.direction == MovementDirection.RIGHT, 
            self.change_to == MovementDirection.RIGHT and not self.direction == MovementDirection.LEFT, 
        )): 
            self.direction = self.change_to

    def change_head_position(self):
        if self.direction == MovementDirection.RIGHT:
            self.snake_head_pos[0] += 1
        elif self.direction == MovementDirection.LEFT:
            self.snake_head_pos[0] -= 1
        elif self.direction == MovementDirection.UP:
            self.snake_head_pos[1] -= 1
        elif self.direction == MovementDirection.DOWN:
            self.snake_head_pos[1] += 1

    def snake_body_mechanism(self, food): 
        new_head_pos = self.snake_head_pos[:] 
        if new_head_pos == food.food_pos: 
            food.food_pos = food.renew_pos()
            self.score += 1
        else: 
            self.snake_body.pop()
        self.snake_body.insert(0, new_head_pos) 


    def draw_snake(self): 
        for pos in self.snake_body: 
            pygame.draw.rect(
                self.surface, self.color, 
                pygame.Rect
                ( 
                    self.DRAWING_OFFSET_X + (pos[0] * 10), 
                    self.DRAWING_OFFSET_Y + (pos[1] * 10), 
                    10, 10
                )
            )
  
    def check_for_boundaries(self, game_over):
        if any((
            self.snake_head_pos[0] > self.COORDS_WIDTH  or self.snake_head_pos[0] < 0,
            self.snake_head_pos[1] > self.COORDS_HEIGHT or self.snake_head_pos[1] < 0
        )):
            game_over = True
            return game_over
        return game_over

    def check_for_snakes_bodies_colli2sion(self, game_over):
        for block in self.snake_body[1:]: 
            if (
                block[0] == self.snake_head_pos[0] and
                block[1] == self.snake_head_pos[1]
            ):
                game_over = True
                return game_over
        return game_over

    def check_for_snakes_bodies_collision(self, game_over):
        obstacles = self.collisions.get_obstacles()
        for block in obstacles: 
            if (
                block[0] == self.snake_head_pos[0] and
                block[1] == self.snake_head_pos[1]
            ):
                game_over = True
                return game_over 
        return game_over

    def actions(self, food): 
        if self.is_ai == True:
            self.change_to = self.ai_movement()
        self.validate_direction_and_change()
        self.change_head_position()
        self.snake_body_mechanism(food)
        game_over = False
        if game_over == False:
            game_over = self.check_for_boundaries(game_over)
        if game_over == False:
            game_over = self.check_for_snakes_bodies_collision(game_over) 
        if game_over == False:
            game_over = self.collisions.check_other_snakes_collisions(self)
        return game_over

    def ai_movement(self): 
        pass

