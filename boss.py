import pygame  
from collisions import Collisiions
from keyboard_inputs import MovementDirection 
from snake import Snake
from random import randrange
from boss_projectile import Boss_Projectile
from boss_voidzone import Boss_Voidzone 
from boss_laser_spell import BossLaserSpell
from boss_minion import BossMinion
from boss_road_spell import BossRoadSpell
from boss_pentagram import BossPentagram
from boss_wave_spell import BossWaveSpell
import math
class Boss:
    def __init__(self, surface, game_rect, collisions, snake, renderer, global_timer ): 
        self.surface = surface
        self.game_rect = game_rect
        self.color_base = (255, 155, 0)   
        self.color = self.color_base
        self.snake = snake
        self.DRAWING_OFFSET_X = self.game_rect.x
        self.DRAWING_OFFSET_Y = self.game_rect.y
        self.COORDS_WIDTH = game_rect.width // 10
        self.COORDS_HEIGHT = game_rect.height // 10
        self.snake_spawn_x = 3
        self.snake_spawn_y = 3
        self.center_pos = [self.snake_spawn_x, self.snake_spawn_y] 
        self.collisions = collisions 
        self.direction = MovementDirection.RIGHT
        self.change_to = self.direction 
        self.renderer = renderer
        self.global_timer = global_timer
        self.target = None
        #-------------
        self.time_tick = 0   
        self.base_abilities_cd = 0
        self.active_abilities_cd = 0
        self.base_abilities_cd_full = 40
        self.active_abilities_cd_full = 130
        self.boss_ultimate_ability_cd = 0
        self.boss_ultimate_ability_cd_full = 200
        self.current_active_ability = 0
        self.current_ultimate_ability = 0
        self.minions_cd = 135 #начнем за 15 тиков до миньонов
        self.minions_cd_full = 150
        #---------
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
        self.in_active_spell_action = False
        #------  
        self.boss_lives = 40
        self.boss_phase = 1 #фаза
        self.boss_phase_2_enabled = False
        self.boss_phase_3_enabled = False
        self.boss_phase_4_enabled = False
        self.size = 1
        #-----
        #sounds 
        self.boss_injured_sound = pygame.mixer.Sound("sounds/boss_injured_sound.mp3")
        self.boss_injured_sound2 = pygame.mixer.Sound("sounds/boss_injured_sound2.mp3")
        self.boss_injured_sound3 = pygame.mixer.Sound("sounds/boss_injured_sound3.mp3")

        self.boss_levelup_2 = pygame.mixer.Sound("sounds/boss_levelup_2.mp3")
        self.boss_levelup_3 = pygame.mixer.Sound("sounds/boss_levelup_3.mp3")
        self.boss_levelup_4 = pygame.mixer.Sound("sounds/boss_levelup_4.mp3")
 
        self.boss_touch_snake = pygame.mixer.Sound("sounds/boss_touch_snake.mp3")
        self.boss_touch_snake2 = pygame.mixer.Sound("sounds/boss_touch_snake2.mp3")
        self.boss_touch_snake3 = pygame.mixer.Sound("sounds/boss_touch_snake3.mp3")
        self.boss_touch_snake4 = pygame.mixer.Sound("sounds/boss_touch_snake4.mp3")

        self.boss_laser = pygame.mixer.Sound("sounds/boss_laser.mp3")
 
        self.boss_minions = pygame.mixer.Sound("sounds/boss_minions.mp3")

        self.boss_road = pygame.mixer.Sound("sounds/boss_road.mp3")
 
        self.boss_pentagram = pygame.mixer.Sound("sounds/boss_pentagram.mp3") 
 
        self.boss_wave = pygame.mixer.Sound("sounds/boss_wave.mp3")
         

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
   
    def injury_emotion(self):
        r = randrange(0,3)
        match r:
            case 0:
                self.create_floating_text("Ouch, it hurts!") 
                self.boss_injured_sound.play()
            case 1:
                self.create_floating_text("Aww, stop it!") 
                self.boss_injured_sound2.play()
            case 2:
                self.create_floating_text("Nooooooo!") 
                self.boss_injured_sound3.play()
            case _:
                self.create_floating_text("Ouch, it hurts!") 
                self.boss_injured_sound.play()


    def injury(self):
        #реакция на то когда игрок съедает яблоко 
        self.pause_boss_timer += 8
        self.time_tick -= 9 #чтобы после дамага босс сразу не кастовал добавим к гкд паузу инжури стейта
        self.injured = True 
        self.add_movespeed(0.05)   
        self.boss_lives -= 1
        if self.boss_lives <= 0:
            self.death()
        else:
            boss_lvlup = self.change_boss_phase() 
            if boss_lvlup == False:
                self.injury_emotion()  
   
    def change_boss_phase(self):
        result = False 
        if  self.boss_lives <= 30 and self.boss_phase_2_enabled == False:
            self.boss_phase_2_enabled = True
            self.boss_phase = 2
            self.size = 2
            self.color_base = (255, 125, 0)   
            self.create_floating_text("I'll crush you! - phase 2", True)  
            self.boss_levelup_2.play()
            result = True
            #змейке кд на спейс снизим раз босс усилился
            self.snake.set_new_space_ability_cd(100)
        elif self.boss_lives <= 20 and self.boss_phase_3_enabled == False:
            self.boss_phase_3_enabled = True
            self.boss_phase = 3
            self.size = 3
            self.color_base = (255, 95, 0)  
            self.snake.set_new_space_ability_cd(80)
            self.create_floating_text("Play time is over! - phase 3", True)  
            self.boss_levelup_3.play()
            result = True
        elif self.boss_lives <= 10 and self.boss_phase_4_enabled == False:
            self.boss_phase_4_enabled = True
            self.boss_phase = 4
            self.size = 4
            self.color_base = (255, 65, 0)  
            self.snake.set_new_space_ability_cd(60)
            self.create_floating_text("Ready to die? - phase 4", True)  
            self.boss_levelup_4.play()
            result = True
        return result

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
   
    def generate_boss_body_points(self, start_point):
        x = start_point[0]
        y = start_point[1] 
        all_surrounding_points = [] 
        for i in range(-self.size -1, self.size +1, 1):
            for j in range(-self.size -1, self.size +1, 1):
                all_surrounding_points.append([x+i,y+j])
        all_surrounding_points.append([x,y]) 
        return all_surrounding_points

    def draw_boss(self, red = False):  
        #мы не будем физически создавать 7 точек в тело чтоб сделать жир боссу
        #мы йобнем иллюзию, отрисовав все соседние точки его центра на 1 шаг   
        new_points = self.generate_boss_body_points(self.center_pos)
          
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
  
    def boss_touch_snake_emotion(self):
        r = randrange(0,4) 
        match r:
            case 0:
                self.create_floating_text("Haha, catched!")
                self.boss_touch_snake.play()
            case 1:
                self.create_floating_text("Huh?")
                self.boss_touch_snake2.play()
            case 2:
                self.create_floating_text("Mmm, yummy snake!")
                self.boss_touch_snake3.play() 
            case 3:
                self.create_floating_text("Did you like it?")
                self.boss_touch_snake4.play()
            case _:
                self.create_floating_text("Haha, catched!")
                self.boss_touch_snake.play()

    def boss_snake_eat_himself_emotion(self):
        self.create_floating_text("Eat himself, look at this looser!")
        self.boss_touch_snake.play()

    def collision_with_snake(self):
        #if self.paused == False and self.injured == False and self.snake.damage_immune_mode == False: 
        if self.snake.damage_immune_mode == False: 
            #реакция на то когда босс догнал змею
            self.collision_cooldown_timer, self.pause_boss_timer = 21, 21
            self.collision_on_cooldown = True   
            if len(self.snake.snake_body) >= 2:
                self.snake.snake_body.pop()
            self.snake.damage_immune_after_hit()
            self.snake.snake_lives -= 1
            self.boss_touch_snake_emotion()

    def check_for_snakes_bodies_collision(self):
        if self.collision_on_cooldown == False:
            obstacles = self.collisions.get_obstacles()
            for block in obstacles: 
                if (
                    abs(block[0] - self.center_pos[0]) <= self.size + 1 and
                    abs(block[1] - self.center_pos[1]) <= self.size + 1
                ):
                    self.collision_with_snake()
            return False

    def actions(self):    
        if self.paused == False and self.in_active_spell_action == False:
            self.change_to = self.ai_movement() 
            self.change_boss_center_position() 
        self.check_for_snakes_bodies_collision() 
  
    def ai_movement(self): 
        self.create_path()

    def create_path(self):  
        s_x = self.center_pos[0]
        s_y = self.center_pos[1]
        start = (s_x, s_y)

        self.target = self.select_closest_snake_segment_to_boss()
        e_x = self.target[0] 
        e_y = self.target[1] 
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
        self.boss_base_abilities_casting_event()
        self.boss_active_abilities_casting_event()
        self.boss_minions_spell_casting_event() 
        self.boss_ultimate_spell_casting_event() 

    def boss_base_abilities_casting_event(self):
        self.base_abilities_cd += 1
        if self.base_abilities_cd >= self.base_abilities_cd_full and self.paused == False and self.injured == False and self.in_active_spell_action == False:     
                self.base_abilities_cd = 0  
                self.boss_select_base_ability_action() 
        self.boss_charging_spell_effect()
        
    def boss_active_abilities_casting_event(self):
        self.active_abilities_cd += 1
        if self.active_abilities_cd >= self.active_abilities_cd_full and self.paused == False and self.injured == False and self.in_active_spell_action == False:     
                self.active_abilities_cd = 0
                self.boss_select_active_ability_action()  
                
    def boss_minions_spell_casting_event(self):
        self.minions_cd += 1
        if self.minions_cd >= self.minions_cd_full and self.paused == False and self.injured == False and self.in_active_spell_action == False:     
                self.minions_cd = 0  
                self.minions()  

    def boss_ultimate_spell_casting_event(self):
        self.boss_ultimate_ability_cd += 1
        if self.boss_ultimate_ability_cd >= self.boss_ultimate_ability_cd_full and self.paused == False and self.injured == False and self.in_active_spell_action == False:     
                self.boss_ultimate_ability_cd = 0
                self.boss_select_ultimate_ability_action()  
   
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
                self.color = self.color_base
#---------------
#spells
    def boss_select_base_ability_action(self):
        #тут нарн в зависимости от дистанции будем стрелять, телепортироваться или еще че делать 
        if self.pause_boss_timer <= 0: 
            x1 = self.center_pos[0]
            y1 = self.center_pos[1]
            x2 = self.target[0] 
            y2 = self.target[1] 
            distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
             
            if distance < 12:
                if self.boss_phase <= 1:
                    self.charge()  
            elif 12 < distance < 25:
                if self.boss_phase <= 1:
                    self.shoot() 
                elif self.boss_phase == 2:
                    self.shoot_lvl2()  
                elif self.boss_phase == 3:
                    self.shoot_lvl3()  
            elif distance >= 25: 
                if self.boss_phase <= 1:
                    self.void_zone() 
                elif self.boss_phase == 2:
                    self.void_zone_lvl2()   
                elif self.boss_phase == 3:
                    self.void_zone_lvl3()   
                elif self.boss_phase == 4:
                    self.void_zone_lvl4()   
  
    def clap(self):
        self.create_floating_text("casting CLAP!", True)  

    def charge(self):
        self.create_floating_text("casting CHARGE!", True)  
        self.boss_charging_spell_activate(6) 

    def shoot(self):
        self.create_floating_text("SHOOTING", True) 
        dir = (1,0)
        pj = Boss_Projectile(25, self, self.snake, self.center_pos, dir) 
        dir = (-1,0)
        pj = Boss_Projectile(25, self, self.snake, self.center_pos, dir) 
        dir = (0,1)
        pj = Boss_Projectile(25, self, self.snake, self.center_pos, dir) 
        dir = (0,-1)
        pj = Boss_Projectile(25, self, self.snake, self.center_pos, dir) 

    def shoot_lvl2(self):
        self.create_floating_text("SHOOTING lvl2", True) 
        dir = (1,0)
        pj = Boss_Projectile(25, self, self.snake, self.center_pos, dir) 
        dir = (-1,0)
        pj = Boss_Projectile(25, self, self.snake, self.center_pos, dir) 
        dir = (0,1)
        pj = Boss_Projectile(25, self, self.snake, self.center_pos, dir) 
        dir = (0,-1)
        pj = Boss_Projectile(25, self, self.snake, self.center_pos, dir) 
        dir = (-1,-1)
        pj = Boss_Projectile(25, self, self.snake, self.center_pos, dir) 
        dir = (-1,1)
        pj = Boss_Projectile(25, self, self.snake, self.center_pos, dir) 
        dir = (1,1)
        pj = Boss_Projectile(25, self, self.snake, self.center_pos, dir) 
        dir = (1,-1)
        pj = Boss_Projectile(25, self, self.snake, self.center_pos, dir) 
        
    def shoot_lvl3(self):
        self.create_floating_text("SHOOTING lvl3", True) 
        dir = (1,0)
        pj = Boss_Projectile(15, self, self.snake, self.center_pos, dir, True)
        dir = (-1,0)
        pj = Boss_Projectile(15, self, self.snake, self.center_pos, dir, True) 
        dir = (0,1)
        pj = Boss_Projectile(15, self, self.snake, self.center_pos, dir, True) 
        dir = (0,-1)
        pj = Boss_Projectile(15, self, self.snake, self.center_pos, dir, True)
        dir = (-1,-1)
        pj = Boss_Projectile(15, self, self.snake, self.center_pos, dir, True) 
        dir = (-1,1)
        pj = Boss_Projectile(15, self, self.snake, self.center_pos, dir, True) 
        dir = (1,1)
        pj = Boss_Projectile(15, self, self.snake, self.center_pos, dir, True)
        dir = (1,-1)
        pj = Boss_Projectile(15, self, self.snake, self.center_pos, dir, True)

    def shoot_single_projectile(self, pos, dir):
        pj = Boss_Projectile(20, self, self.snake, pos, dir)


    def void_zone(self):
        self.create_floating_text("casting VOID ZONES", True)  
        x = self.snake.snake_head_pos[0] 
        y = self.snake.snake_head_pos[1]
        pos = [x,y]
        vz = Boss_Voidzone(30, self, self.snake, pos) 

    def void_zone_lvl2(self):
        self.create_floating_text("casting VOID ZONES lvl2", True)  
        x = self.snake.snake_head_pos[0] 
        y = self.snake.snake_head_pos[1]
        pos = [x, y]
        vz = Boss_Voidzone(30, self, self.snake, pos)  
        pos = [x + 9, y]
        vz = Boss_Voidzone(30, self, self.snake, pos) 
        pos = [x - 9, y]
        vz = Boss_Voidzone(30, self, self.snake, pos) 
        
    def void_zone_lvl3(self):
        self.create_floating_text("casting VOID ZONES lvl3", True)  
        x = self.snake.snake_head_pos[0] 
        y = self.snake.snake_head_pos[1]
        pos = [x, y]
        vz = Boss_Voidzone(30, self, self.snake, pos)  
        pos = [x + 9, y]
        vz = Boss_Voidzone(30, self, self.snake, pos) 
        pos = [x - 9, y]
        vz = Boss_Voidzone(30, self, self.snake, pos) 
        pos = [x, y + 9]
        vz = Boss_Voidzone(30, self, self.snake, pos)  
        pos = [x, y - 9]
        vz = Boss_Voidzone(30, self, self.snake, pos)  
                
    def void_zone_lvl4(self):
        self.create_floating_text("casting VOID ZONES lvl4", True)  
        x = self.snake.snake_head_pos[0] 
        y = self.snake.snake_head_pos[1]
        pos = [x, y]
        vz = Boss_Voidzone(30, self, self.snake, pos)  
        pos = [x + 9, y]
        vz = Boss_Voidzone(30, self, self.snake, pos) 
        pos = [x - 9, y]
        vz = Boss_Voidzone(30, self, self.snake, pos) 
        pos = [x, y + 9]
        vz = Boss_Voidzone(30, self, self.snake, pos)  
        pos = [x, y - 9]
        vz = Boss_Voidzone(30, self, self.snake, pos) 
        #----------
        pos = [x + 9, y - 9]
        vz = Boss_Voidzone(30, self, self.snake, pos)  
        pos = [x - 9, y - 9]
        vz = Boss_Voidzone(30, self, self.snake, pos)  
        pos = [x + 9, y + 9]
        vz = Boss_Voidzone(30, self, self.snake, pos)  
        pos = [x - 9, y + 9]
        vz = Boss_Voidzone(30, self, self.snake, pos)  
        #----------
        pos = [x + 18, y]
        vz = Boss_Voidzone(30, self, self.snake, pos)  
        pos = [x - 18, y]
        vz = Boss_Voidzone(30, self, self.snake, pos)  
        pos = [x, y + 18]
        vz = Boss_Voidzone(30, self, self.snake, pos)  
        pos = [x, y - 18]
        vz = Boss_Voidzone(30, self, self.snake, pos)  
    
    def boss_create_single_voidzone(self, pos):
        vz = Boss_Voidzone(15, self, self.snake, pos)  
#-----------------
    def boss_charging_spell_activate(self, time): 
        if self.charging_spell == False:
            self.charging_spell = True
            self.charging_spell_timer = time

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
#---------------------------
#active spells

    def boss_select_active_ability_action(self):
        if self.boss_phase >= 2:  
            match self.current_active_ability:
                case 0:
                    self.laser()
                case 1:
                    self.road_spell()
                case _:
                    self.laser() 
            self.current_active_ability += 1
            if self.current_active_ability >= 2:
                self.current_active_ability = 0

    def boss_select_ultimate_ability_action(self):
        if self.boss_phase >= 4:  
            self.wave_spell()
        elif self.boss_phase == 3:
            self.pentagram_spell()

    def wave_spell(self):
        self.in_active_spell_action = True
        wave = BossWaveSpell([self.COORDS_WIDTH // 2, self.COORDS_HEIGHT // 2], self, self.snake)

    def pentagram_spell(self):
        self.in_active_spell_action = True
        penta = BossPentagram(30, [self.COORDS_WIDTH // 2, self.COORDS_HEIGHT // 2], self, self.snake)

    def road_spell(self):
        self.in_active_spell_action = True
        road = BossRoadSpell(150, self, self.snake)

    def laser(self):     
        self.in_active_spell_action = True
        if self.boss_phase <= 2: 
                laser_spell = BossLaserSpell(
                                            35, 2, 
                                            (self.COORDS_WIDTH // 2, self.COORDS_HEIGHT // 2), 
                                            self, self.snake, 1 #убрать в конце 3 это тест 
                                            )
        elif self.boss_phase == 3: 
                laser_spell = BossLaserSpell(
                                            35, 2, 
                                            (self.COORDS_WIDTH // 2, self.COORDS_HEIGHT // 2), 
                                            self, self.snake, 2
                                            )
        elif self.boss_phase >= 4: 
                laser_spell = BossLaserSpell(
                                            35, 2, 
                                            (self.COORDS_WIDTH // 2, self.COORDS_HEIGHT // 2), 
                                            self, self.snake, 3
                                            )
#----------- 
    def minions(self): 
        self.boss_minions.play()
        lifetime = 70
        x = self.center_pos[0] 
        y = self.center_pos[1]
        if self.boss_phase <= 1: 
            self.create_floating_text("casting Minions lvl1", True)  
            pos = [x + 10, y]
            minion = BossMinion(lifetime, self, self.snake, pos)
            pos = [x - 10, y]
            minion = BossMinion(lifetime, self, self.snake, pos)
        if self.boss_phase == 2: 
            self.create_floating_text("casting Minions lvl2", True)  
            pos = [x + 10, y]
            minion = BossMinion(lifetime, self, self.snake, pos)
            pos = [x - 10, y]
            minion = BossMinion(lifetime, self, self.snake, pos)
            pos = [x, y + 10]
            minion = BossMinion(lifetime, self, self.snake, pos)
            pos = [x, y - 10]
            minion = BossMinion(lifetime, self, self.snake, pos)
        if self.boss_phase >= 3: 
            self.create_floating_text("casting Minions lvl3", True)  
            pos = [x + 10, y]
            minion = BossMinion(lifetime, self, self.snake, pos)
            pos = [x - 10, y]
            minion = BossMinion(lifetime, self, self.snake, pos)
            pos = [x, y + 10]
            minion = BossMinion(lifetime, self, self.snake, pos)
            pos = [x, y - 10]
            minion = BossMinion(lifetime, self, self.snake, pos)
            #--------
            pos = [x - 10, y - 10]
            minion = BossMinion(lifetime, self, self.snake, pos)
            pos = [x - 10, y + 10]
            minion = BossMinion(lifetime, self, self.snake, pos)
            pos = [x + 10, y - 10]
            minion = BossMinion(lifetime, self, self.snake, pos)
            pos = [x + 10, y + 10]
            minion = BossMinion(lifetime, self, self.snake, pos) 