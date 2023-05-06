import pygame 
import random 

class Snake:
    def __init__(self, surface):
        self.surface = surface
        self.color = (0, 0, 255)
        self.snake_head_pos = [100, 50]
        self.snake_body = [[100, 50], [90, 50], [80, 50]] 
        self.direction = "RIGHT"
        self.change_to = self.direction

    def validate_direction_and_change(self):
        if any((self.change_to == "RIGHT" and not self.direction == "LEFT",
                self.change_to == "LEFT" and not self.direction == "RIGHT",
                self.change_to == "UP" and not self.direction == "DOWN",
                self.change_to == "DOWN" and not self.direction == "UP")):
            self.direction = self.change_to

    def change_head_position(self):
        if self.direction == "RIGHT":
            self.snake_head_pos[0] += 10
        elif self.direction == "LEFT":
            self.snake_head_pos[0] -= 10
        elif self.direction == "UP":
            self.snake_head_pos[1] -= 10
        elif self.direction == "DOWN":
            self.snake_head_pos[1] += 10

    def snake_body_mechanism(self, score, food):
        """
        Метод отвечает за механизм движения змейки и ее рост при поедании еды.
        """
        new_head_pos = self.snake_head_pos[:]
        # Проверяем, столкнулась ли змейка с едой
        if new_head_pos == food.food_pos:
            # Если да, то генерируем новое положение еды и добавляем блок к змейке
            food.food_pos = food.renew_pos()
            score += 1
        else:
            # Если нет, то просто двигаем змейку без добавления блока
            self.snake_body.pop()
        self.snake_body.insert(0, new_head_pos)
        return score 


    def draw_snake(self): 
        for pos in self.snake_body: 
            pygame.draw.rect(self.surface, self.color, pygame.Rect(
                pos[0], pos[1], 10, 10))
  
    def check_for_boundaries(self, game_over, score):
        if any((
            self.snake_head_pos[0] > 710 or self.snake_head_pos[0] < 0,
            self.snake_head_pos[1] > 450 or self.snake_head_pos[1] < 0
        )):
            game_over = True
            return game_over, score
        return game_over, score

    def check_for_self_body_collision(self, game_over, score):
        for block in self.snake_body[1:]:
            if (block[0] == self.snake_head_pos[0] and
                block[1] == self.snake_head_pos[1]):
                game_over = True
                return game_over, score
        return game_over, score
