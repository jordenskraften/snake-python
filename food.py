import pygame
import random 

 
class Food:
    def __init__(self, game_rect, collisions):
        self.game_rect = game_rect
        self.COORDS_WIDTH = game_rect.width // 10
        self.COORDS_HEIGHT = game_rect.height // 10 
        self.DRAWING_OFFSET_X = self.game_rect.x
        self.DRAWING_OFFSET_Y = self.game_rect.y
        self.collisions = collisions 
        self.food_pos = self.renew_pos()  

    def draw_food(self, surface): 
        pygame.draw.rect(
            surface, (0, 255, 0), 
            pygame.Rect
            (
            self.DRAWING_OFFSET_X + self.food_pos[0] * 10, 
            self.DRAWING_OFFSET_Y + self.food_pos[1] * 10, 
            10, 10
            )
        ) 

    def generate_random_food_pos(self): 
        return(
            random.randrange(0, self.COORDS_WIDTH ), 
            random.randrange(0, self.COORDS_HEIGHT )
        )

    def renew_pos(self):   
        new_food_pos = self.generate_random_food_pos()
        obstacles = self.collisions.get_obstacles() 
        while new_food_pos in obstacles: 
            new_food_pos = self.generate_random_food_pos()
        self.food_pos = new_food_pos 
        return self.food_pos

    def hide(self):
        self.food_pos = [22222,33333]
  
             
 


