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

    def draw_game_objects(self, score_val, score_val_ai = None, ai_vs_ai_mode = False): 
        for s in self.snakes: 
            s.draw_snake()   
        self.food.draw_food(self.surface) 
        self.display_tooltip()
        if ai_vs_ai_mode == False:
            self.display_score(score_val)
            if score_val_ai != None:
                self.display_score_ai(score_val_ai)
        else:
            self.display_score_ai(score_val)
            self.display_score_ai2(score_val_ai)

        
    def display_score(self, score_val):
        font = pygame.font.SysFont('arial', 20)
        score = font.render("Player score: " + str(score_val), True, (255, 255, 255))
        self.surface.blit(score, (500, 10)) 

    def display_score_ai(self, score_val):
        font = pygame.font.SysFont('arial', 20)
        score = font.render("AI score: " + str(score_val), True, (255, 255, 255))
        self.surface.blit(score, (100, 10)) 

    def display_score_ai2(self, score_val):
        font = pygame.font.SysFont('arial', 20)
        score = font.render("AI-2 score: " + str(score_val), True, (255, 255, 255))
        self.surface.blit(score, (500, 10)) 
 
    def display_tooltip(self):
        font = pygame.font.SysFont('arial', 20)
        score = font.render("Press ESC to main menu: ", True, (255, 255, 255))
        self.surface.blit(score, (250, 10)) 