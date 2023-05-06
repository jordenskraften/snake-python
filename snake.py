import pygame  
from keyboard_inputs import MovementDirection


class Snake:
    def __init__(self, surface, game_rect): 
        self.surface = surface
        self.game_rect = game_rect
        self.color = (0, 0, 255)
        #стартовые коорды змейки это координаты середины игровой зоны
        #змейке важно чтобы коорды были кратны 10, поэтому нижней формулой приводим их к округлению до десятых
        #колизия работает как точное сравнение коордов, поэтому важно чтобы коорды и яблока и змеи делились на 10
        self.snake_spawn_x = game_rect.width * 0.5
        self.snake_spawn_y = game_rect.height * 0.5
        self.snake_spawn_x = ((self.snake_spawn_x - 1) // 10 + 1) * 10
        self.snake_spawn_y = ((self.snake_spawn_y - 1) // 10 + 1) * 10

        self.snake_head_pos = [self.snake_spawn_x, self.snake_spawn_y]
        self.snake_body = [self.snake_head_pos] 
        self.direction = MovementDirection.RIGHT
        self.change_to = self.direction

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
            self.snake_head_pos[0] += 10
        elif self.direction == MovementDirection.LEFT:
            self.snake_head_pos[0] -= 10
        elif self.direction == MovementDirection.UP:
            self.snake_head_pos[1] -= 10
        elif self.direction == MovementDirection.DOWN:
            self.snake_head_pos[1] += 10

    def snake_body_mechanism(self, score, food): 
        new_head_pos = self.snake_head_pos[:] 
        if new_head_pos == food.food_pos: 
            food.food_pos = food.renew_pos()
            score += 1
        else: 
            self.snake_body.pop()
        self.snake_body.insert(0, new_head_pos)
        return score 


    def draw_snake(self): 
        for pos in self.snake_body: 
            pygame.draw.rect(self.surface, self.color, pygame.Rect(
                pos[0], pos[1], 10, 10))
  
    def check_for_boundaries(self, game_over, score):
        if any((
            self.snake_head_pos[0] > self.game_rect.width or self.snake_head_pos[0] < self.game_rect.x,
            self.snake_head_pos[1] > self.game_rect.height or self.snake_head_pos[1] < self.game_rect.y
        )):
            game_over = True
            return game_over, score
        return game_over, score

    def check_for_self_body_collision(self, game_over, score):
        for block in self.snake_body[1:]:
            if (
                block[0] == self.snake_head_pos[0] and
                block[1] == self.snake_head_pos[1]
            ):
                game_over = True
                return game_over, score
        return game_over, score
