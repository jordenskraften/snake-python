import pygame
import random

class Food:
    def __init__(self):
        self.food_pos = [random.randrange(1, 72) * 10, random.randrange(1, 46) * 10]
        self.food_spawn = True

    def draw_food(self, surface):
        if self.food_spawn == True:
            pygame.draw.rect(surface, (0, 255, 0), pygame.Rect(
                self.food_pos[0], self.food_pos[1], 10, 10))
        #self.food_spawn = False

    def set_food_spawn(self, value):
        self.food_spawn = value
