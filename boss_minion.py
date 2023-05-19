from global_timer import TimedObject
import pygame 
import math

class BossMinion(TimedObject):
    def __init__(self, lifetime, boss, snake, pos):
        self.lifetime = lifetime 
        self.color = (255,155,0)
        self.pos = pos 
        self.boss = boss
        self.snake = snake
        self.speed = 1  
        self.boss.global_timer.attach(self)
        
    def enter(self):
        pass

    def death(self):
        self.boss.global_timer.detach(self)
        self.pos = [999,999] 
        del(self)

    def limit_number(self, value, limit):
        if value >= limit:
            return limit
        elif value <= -limit:
            return -limit
        else: 
            return 0

    def timer_tick(self):
        self.lifetime -= 1
        if self.lifetime <= 0: 
            self.death() 
         
        self.move_to_snake()
        self.check_for_snakes_bodies_collision()
        self.draw_obj() 

    def move_to_snake(self):
        target = self.select_closest_snake_segment()
        d_x = target[0] - self.pos[0]
        d_y = target[1] - self.pos[1]
        distance = math.sqrt(d_x**2 + d_y**2)
        step_x = d_x / distance 
        step_y = d_y / distance 
        dir = (step_x,step_y)   
        self.pos = [
                    self.pos[0] + dir[0] * self.speed,
                    self.pos[1] + dir[1] * self.speed
                    ]  

    def select_closest_snake_segment(self):
        result = self.snake.snake_head_pos
        x1 = self.pos[0]
        y1 = self.pos[1]
        x2 = self.snake.snake_head_pos[0] 
        y2 = self.snake.snake_head_pos[1]
        closest_dist = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        for seg in self.snake.snake_body:
            x2 = seg[0]
            y2 = seg[1]
            closest_dist2 = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
            if (closest_dist > closest_dist2):
                closest_dist = closest_dist2
                result = seg
        return result

    def check_for_snakes_bodies_collision(self): 
        obstacles = self.boss.collisions.get_obstacles()
        for block in obstacles: 
            if (
                abs(block[0] - self.pos[0]) <= 1 and
                abs(block[1] - self.pos[1]) <= 1 
            ): 
                if self.snake.damage_immune_mode == False:
                    self.boss.collision_with_snake() 
                self.death()  

    def draw_obj(self):     
        pygame.draw.rect(
            self.boss.surface, self.color, 
            pygame.Rect
            ( 
                self.boss.DRAWING_OFFSET_X + (self.pos[0] * 10), 
                self.boss.DRAWING_OFFSET_Y + (self.pos[1] * 10), 
                10, 10
            ) 
        )
        
 
    def limit_number(self, value, limit):
        if value >= limit:
            return limit
        elif value <= -limit:
            return -limit
        else: 
            return 0