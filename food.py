import pygame
import random 

 
class Food:
    def __init__(self, snake_body):
        self.snake_body = snake_body 
        self.food_pos = self.renew_pos() 

    def draw_food(self, surface): 
        pygame.draw.rect(surface, (0, 255, 0), pygame.Rect(
            self.food_pos[0], self.food_pos[1], 10, 10)) 
  
    def renew_pos(self):
        correct_spawn_food = False
        while correct_spawn_food == False:
            success_checking_counter = 0 
            snake_length = len(self.snake_body)
            new_food_pos = [random.randrange(1, 72) * 10, random.randrange(1, 46) * 10]
 
            #print(new_food_pos)

            for segment in self.snake_body:
                if new_food_pos[0] != segment[0] and new_food_pos[1] != segment[1]: 
                #если координаты спавна новой еды совпадают с координатами тела змейки
                    #self.food_pos = new_food_pos
                    success_checking_counter += 1
                else:
                    success_checking_counter = 0 
                    break
            if success_checking_counter >= snake_length:   
                self.food_pos = new_food_pos
                correct_spawn_food = True
                return(new_food_pos) 
            
 


