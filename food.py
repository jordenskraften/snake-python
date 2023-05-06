import pygame
import random 

 
class Food:
    def __init__(self, snake_body, game_rect):
        self.game_rect = game_rect
        self.NODE_WIDTH = game_rect.width // 10
        self.NODE_HEIGHT = game_rect.height // 10
        #округлили стартовые координаты игровой зоны вверх
        #например 25 округлили до 30, для коллизии змейки важно четность на 10 
        self.rounded_rect_start_x = ((self.game_rect.x - 1) // 10 + 1) * 10   
        self.rounded_rect_start_y = ((self.game_rect.y - 1) // 10 + 1) * 10  
        self.snake_body = snake_body 
        self.food_pos = self.renew_pos()  

    def draw_food(self, surface): 
        pygame.draw.rect(surface, (0, 255, 0), pygame.Rect(
            self.food_pos[0], self.food_pos[1], 10, 10)) 

    def generate_random_food_pos(self): 
        return([
            random.randrange(self.rounded_rect_start_x, self.NODE_WIDTH * 9, 10), 
            random.randrange(self.rounded_rect_start_y, self.NODE_HEIGHT * 9, 10)
        ])

    def renew_pos(self):   
        new_food_pos = self.generate_random_food_pos()
        while new_food_pos in self.snake_body:
            new_food_pos = self.generate_random_food_pos()
        self.food_pos = new_food_pos 
        return self.food_pos
  
             
 


