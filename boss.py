import pygame  
from collisions import Collisiions
from keyboard_inputs import MovementDirection 
from snake import Snake
from random import randrange
from boss_projectile import Boss_Projectile
import math
class Boss:
    def __init__(self, surface, game_rect, collisions, snake, renderer, global_timer ): 
        self.surface = surface
        self.game_rect = game_rect
        self.color = (0, 0, 255) 
        self.snake = snake
        self.DRAWING_OFFSET_X = self.game_rect.x
        self.DRAWING_OFFSET_Y = self.game_rect.y
        self.COORDS_WIDTH = game_rect.width // 10
        self.COORDS_HEIGHT = game_rect.height // 10
        self.snake_spawn_x = 3
        self.snake_spawn_y = 3
        self.center_pos = [self.snake_spawn_x, self.snake_spawn_y] 
        self.collisions = collisions
        self.color = (255, 125, 0)   
        self.direction = MovementDirection.RIGHT
        self.change_to = self.direction 
        self.renderer = renderer
        self.global_timer = global_timer
        #-------------
        self.time_tick = 0   
        self.base_movespeed = 0.4
        self.movespeed_current = self.base_movespeed
        self.pause_boss_timer = 0
        self.paused = False  
        self.injured = False
        self.collision_cooldown_timer = 0
        self.collision_on_cooldown = False  
        #----------------
        self.charging_spell = False  
        self.charging_spell_timer = 0
        #------  
        self.boss_lives = 30
 
    def add_movespeed(self, val):
        self.base_movespeed += val
        if self.base_movespeed < 0.4:
            self.base_movespeed = 0.4 
        if self.base_movespeed > 0.9:
            self.base_movespeed = 0.9 

    def create_floating_text(self, text, down_dir = False):
        pos = (
                self.DRAWING_OFFSET_X + (self.center_pos[0] * 10),
                self.DRAWING_OFFSET_Y + (self.center_pos[1] * 10)
            ) 
        self.renderer.create_floating_text(pos, 1, text, down_dir)
   
    def injury(self):
        #реакция на то когда игрок съедает яблоко
        self.pause_boss_timer = 5
        self.time_tick = 6 #чтобы после дамага босс сразу не кастовал добавим к гкд паузу инжури стейта
        self.injured = True 
        self.add_movespeed(0.05)  
        self.create_floating_text("awww, i feels pain!") 
        self.boss_lives -= 1
        if self.boss_lives <= 0:
            self.death()
   
    def death(self):
        pass

    def change_boss_center_position(self): 
        if self.direction == MovementDirection.RIGHT:
            self.center_pos[0] += self.movespeed_current 
        elif self.direction == MovementDirection.LEFT:
            self.center_pos[0] -= self.movespeed_current 
        elif self.direction == MovementDirection.UP:
            self.center_pos[1] -= self.movespeed_current 
        elif self.direction == MovementDirection.DOWN:
            self.center_pos[1] += self.movespeed_current 
  
    def generate_boss_body_points(self, x, y):
        directions = [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)]

        points = []
        for direction in directions:
            new_x = x + direction[0]
            new_y = y + direction[1]
            points.append((new_x, new_y))

        return points

    def draw_boss(self, red = False):  
        #мы не будем физически создавать 7 точек в тело чтоб сделать жир боссу
        #мы йобнем иллюзию, отрисовав все соседние точки его центра на 1 шаг  
        c_x = self.center_pos[0]
        c_y = self.center_pos[1]
        new_points = self.generate_boss_body_points(c_x, c_y)
          
        for point in new_points:
            pygame.draw.rect(
                self.surface, self.color, 
                pygame.Rect
                ( 
                    self.DRAWING_OFFSET_X + (point[0] * 10), 
                    self.DRAWING_OFFSET_Y + (point[1] * 10), 
                    10, 10
                )
            ) 
  
    def collision_with_snake(self):
        if self.paused == False and self.injured == False and self.snake.damage_immune_mode == False: 
            #реакция на то когда босс догнал змею
            self.collision_cooldown_timer, self.pause_boss_timer = 21, 21
            self.collision_on_cooldown = True  
            self.create_floating_text("haha, catched!")
            if len(self.snake.snake_body) >= 2:
                self.snake.snake_body.pop()
            self.snake.damage_immune_after_hit()
            self.snake.snake_lives -= 1

    def check_for_snakes_bodies_collision(self):
        if self.collision_on_cooldown == False:
            obstacles = self.collisions.get_obstacles()
            for block in obstacles: 
                if (
                    abs(block[0] - self.center_pos[0]) <= 2 and
                    abs(block[1] - self.center_pos[1]) <= 2 
                ):
                    self.collision_with_snake()
            return False

    def actions(self):    
        if self.paused == False:
            self.change_to = self.ai_movement() 
            self.change_boss_center_position() 
            self.check_for_snakes_bodies_collision() 
  
    def ai_movement(self): 
        self.create_path()

    def create_path(self):  
        s_x = self.center_pos[0]
        s_y = self.center_pos[1]
        start = (s_x, s_y)

        target = self.select_closest_snake_segment_to_boss()
        e_x = target[0] 
        e_y = target[1] 
        end = (e_x, e_y)

        new_dir = (
                end[0] - start[0],
                end[1] - start[1]
        ) 
        self.ai_change_direction(new_dir)

    def select_closest_snake_segment_to_boss(self):
        result = self.snake.snake_head_pos
        x1 = self.center_pos[0]
        y1 = self.center_pos[1]
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


    def ai_change_direction(self, vector):
        x, y = vector  
        horizontal_move = True
        if abs(x) - abs(y) <= 1.5:
            horizontal_move = False 
        if horizontal_move:
            if x > 0:
                self.direction = MovementDirection.RIGHT  
            else:
                self.direction = MovementDirection.LEFT  
        else:
            if y > 0:
                self.direction = MovementDirection.DOWN 
            else:
                self.direction = MovementDirection.UP  
 
#-------------------------------------
#таймеры 
#------------------- 
    def timer_tick(self):
        self.time_tick += 1
        self.boss_pause_event()
        self.collisions_and_injury_event()
        self.boss_abilities_casting_event()


    def boss_abilities_casting_event(self):
        if self.time_tick >= 35 and self.paused == False and self.injured == False:    
            self.time_tick = 0
            self.boss_select_ability_action() 
        self.boss_charging_spell_effect()

    def boss_pause_event(self):
        #--------------- 
        if self.pause_boss_timer <= 0:
            self.paused = False
            self.injured = False
        else:
            self.pause_boss_timer -= 1
            self.paused = True 


    def collisions_and_injury_event(self):
        #--------------
        if self.collision_cooldown_timer <= 0:
            self.collision_on_cooldown = False 
        else:
            self.collision_cooldown_timer -= 1 
            self.collision_on_cooldown = True 
        #---------------
        if self.injured == True:
            self.color = (255, 0, 0)  
        else:
            if self.collision_on_cooldown == True:
                self.color = (255, 225, 0)  
            else:
                self.color = (255, 125, 0)  
#---------------
#spells
    def boss_select_ability_action(self):
        #тут нарн в зависимости от дистанции будем стрелять, телепортироваться или еще че делать 
        if self.pause_boss_timer <= 0:
            r = randrange(0, 3)
            match r:
                case 0:
                    self.shoot()
                case 1:
                    self.charge()
                case 2:
                    self.shoot()
                case 3:
                    self.charge()
                case _:
                    pass 


    def teleport(self):
        self.create_floating_text("casting TELEPORT!", True) 

    def clap(self):
        self.create_floating_text("casting CLAP!", True)  

    def shoot(self):
        self.create_floating_text("SHOOTING", True) 
        dir = (1,0)
        pj = Boss_Projectile(200, self, self.snake, self.center_pos, dir)
        self.global_timer.attach(pj)
        dir = (-1,0)
        pj = Boss_Projectile(200, self, self.snake, self.center_pos, dir)
        self.global_timer.attach(pj)
        dir = (0,1)
        pj = Boss_Projectile(200, self, self.snake, self.center_pos, dir)
        self.global_timer.attach(pj)
        dir = (0,-1)
        pj = Boss_Projectile(200, self, self.snake, self.center_pos, dir)
        self.global_timer.attach(pj)

    def void_zone(self):
        self.create_floating_text("casting VOID ZONES", True)  

    def charge(self):
        self.create_floating_text("casting CHARGE!", True)  
        self.boss_charging_spell_activate()
#-----------------
    def boss_charging_spell_activate(self): 
        if self.charging_spell == False:
            self.charging_spell = True
            self.charging_spell_timer = 4

    def boss_charging_spell_effect(self): 
        bonus_ms = 2
        if self.charging_spell == False:
            self.movespeed_current = self.base_movespeed
        else: 
            self.movespeed_current = self.base_movespeed + bonus_ms 
        self.charging_spell_timer -= 1
        if self.charging_spell_timer < 0:
            self.charging_spell = False
            self.charging_spell_timer = 0