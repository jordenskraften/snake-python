from global_timer import TimedObject
import pygame


class Boss_Voidzone(TimedObject):
    def __init__(self, lifetime, boss, snake, pos):
        super().__init__(lifetime)
        self.color = (75,75,75, 0.5)
        self.pos = pos
        self.boss = boss
        self.snake = snake
        self.size = 1
        self.boss.global_timer.attach(self)
        
    def enter(self):
        pass

    def death(self):
        self.boss.global_timer.detach(self)
        self.pos = [999,999] 
        del(self)
  
    def timer_tick(self):
        self.lifetime -= 1 
        if self.lifetime <= 0: 
            self.death()  
        else: 
            if self.lifetime <= 7: 
                self.explosion() 
            else: 
                if self.lifetime %3 == 0:
                    self.color = (75,75,75, 0.5)
                else: 
                    self.color = (35,35,35, 0.5)

        self.draw_obj() 

    def explosion(self):  
        if 2 < self.lifetime <= 9: 
            self.size = 2
            self.color = (225,225,225, 0.5)
            self.check_for_snakes_bodies_collision() 
        elif self.lifetime <= 2:   
            self.color = (135,135,135, 0.5)

    def check_for_snakes_bodies_collision(self): 
        obstacles = self.boss.collisions.get_obstacles()
        for block in obstacles: 
            if (
                abs(block[0] - self.pos[0]) <= self.size and
                abs(block[1] - self.pos[1]) <= self.size 
            ): 
                if self.snake.damage_immune_mode == False:
                    self.boss.collision_with_snake()  

  
    def get_all_surrounding_points(self, start_point, max_step_length):
        x = start_point[0]
        y = start_point[1] 
        all_surrounding_points = [] 
        for i in range(-self.size -1, self.size +1, 1):
            for j in range(-self.size -1, self.size +1, 1):
                all_surrounding_points.append([x+i,y+j])
        all_surrounding_points.append([x,y]) 
        return all_surrounding_points
    
    def get_surrounding_points(self, start_point, step_length):
        directions = [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)]
        surrounding_points = []
        step_length = step_length
        for direction in directions:
            dx, dy = direction
            new_point = (start_point[0] + dx * step_length, start_point[1] + dy * step_length)
            surrounding_points.append(new_point)
        
        return surrounding_points

    def draw_obj(self):    
        new_points = self.get_all_surrounding_points(self.pos, self.size)
          
        for point in new_points:
            pygame.draw.rect(
                self.boss.surface, self.color, 
                pygame.Rect
                ( 
                    self.boss.DRAWING_OFFSET_X + (point[0] * 10), 
                    self.boss.DRAWING_OFFSET_Y + (point[1] * 10), 
                    10, 10
                )
            ) 
 