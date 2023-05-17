from global_timer import TimedObject
import pygame 

class Boss_Projectile(TimedObject):
    def __init__(self, lifetime, boss, snake, pos, dir, return_back = False):
        super().__init__(lifetime)
        self.color = (255,0,0)
        self.pos = pos
        self.dir = dir
        self.boss = boss
        self.snake = snake
        self.speed = 1.5
        if return_back == True:
            self.speed = 2
        self.return_back = return_back
        self.enabled_back_path = False
        self.boss.global_timer.attach(self)
        
    def enter(self):
        pass

    def death(self):
        self.boss.global_timer.detach(self)
        self.pos = [999,999]
        self.dir = [0,0]
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
            if self.return_back == False:
                self.death()
            else:
                if self.enabled_back_path == False:
                    self.enabled_back_path = True
                    self.return_back = False
                    self.lifetime = 20
        
        if self.enabled_back_path == False:
            self.pos = (
                        self.pos[0] + self.dir[0] * self.speed,
                        self.pos[1] + self.dir[1] * self.speed, 
                        ) 
        else:
            n_x = self.boss.center_pos[0] - self.pos[0]
            n_y = self.boss.center_pos[1] - self.pos[1]
            n_x = self.limit_number(n_x, 1.5) 
            n_y = self.limit_number(n_y, 1.5) 
            self.dir = (n_x,n_y) 
            self.pos = (
                        self.pos[0] + self.dir[0] * self.speed,
                        self.pos[1] + self.dir[1] * self.speed
                        )  
            if (
                abs(self.boss.center_pos[0] - self.pos[0]) <= 8 and
                abs(self.boss.center_pos[1] - self.pos[1]) <= 8 
            ):
                self.death()
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