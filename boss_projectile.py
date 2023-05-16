from global_timer import TimedObject
import pygame

class Boss_Projectile(TimedObject):
    def __init__(self, lifetime, boss, snake, pos, dir):
        super().__init__(lifetime)
        self.color = (255,0,0)
        self.pos = pos
        self.dir = dir
        self.boss = boss
        self.snake = snake
        self.speed = 1.5
        self.boss.global_timer.attach(self)
        
    def enter(self):
        pass

    def death(self):
        self.boss.global_timer.detach(self)
        self.pos = [999,999]
        self.dir = [0,0]
        del(self)
  
    def timer_tick(self):
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.death() 
        self.pos = (
                    self.pos[0] + self.dir[0] * self.speed,
                    self.pos[1] + self.dir[1] * self.speed, 
                    ) 
        self.draw_obj()
        self.check_for_snakes_bodies_collision()

    def check_for_snakes_bodies_collision(self): 
        obstacles = self.boss.collisions.get_obstacles()
        for block in obstacles: 
            if (
                abs(block[0] - self.pos[0]) <= self.speed and
                abs(block[1] - self.pos[1]) <= self.speed 
            ): 
                if self.snake.damage_immune_mode == False:
                    self.boss.collision_with_snake() 
                self.death()  

    def draw_obj(self, red = False):     
        pygame.draw.rect(
            self.boss.surface, self.color, 
            pygame.Rect
            ( 
                self.boss.DRAWING_OFFSET_X + (self.pos[0] * 10), 
                self.boss.DRAWING_OFFSET_Y + (self.pos[1] * 10), 
                10, 10
            ) 
        )