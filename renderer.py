import pygame

class Renderer: 
    def __init__(self, surface, food):
        self.surface = surface
        self.snakes = []
        self.food = food 

    def add_snake(self, snake):
        self.snakes.append(snake)

    def remove_sname(self, snake):
        self.snakes.remove(snake)

    def draw_game_objects(self, score_val): 
        for s in self.snakes: 
            s.draw_snake()   
        self.food.draw_food(self.surface)
        self.display_score(score_val)
        
    def display_score(self, score_val):
        font = pygame.font.SysFont('arial', 20)
        score = font.render("Score: " + str(score_val), True, (255, 255, 255))
        self.surface.blit(score, (600, 10)) 