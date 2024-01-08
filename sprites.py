import pygame
from config import *
import math
import random
import time

class Spritesheet:
    def __init__(self, file, color_key):
        self.sheet = pygame.image.load(file).convert()
        self.color_key = color_key

    def get_sprite(self, x, y, width, height):
        sprite = pygame.Surface([width, height])
        sprite.blit(self.sheet, (0, 0), (x, y, width, height))
        sprite.set_colorkey(self.color_key)
        return sprite         

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y, player_class):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprite
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        self.player_class = player_class
        self.stats = PLAYER_STATS[player_class].copy()
        self.last_damage_time = 0.0

        self.x_change = 0
        self.y_change = 0

        self.facing = 'down'
        self.animation_loop = 0

        self.image = self.game.character_spritesheet[self.player_class].get_sprite(0, 0, self.width, self.height)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.down_animations = [self.game.character_spritesheet[self.player_class].get_sprite(0, 0, self.width, self.height),
                                self.game.character_spritesheet[self.player_class].get_sprite(32, 0, self.width, self.height),
                                self.game.character_spritesheet[self.player_class].get_sprite(64, 0, self.width, self.height)]    
        
        self.left_animations = [self.game.character_spritesheet[self.player_class].get_sprite(0, 32, self.width, self.height),
                           self.game.character_spritesheet[self.player_class].get_sprite(32, 32, self.width, self.height),
                           self.game.character_spritesheet[self.player_class].get_sprite(64, 32, self.width, self.height)]    
        
        self.right_animations = [self.game.character_spritesheet[self.player_class].get_sprite(0, 64, self.width, self.height),
                           self.game.character_spritesheet[self.player_class].get_sprite(32, 64, self.width, self.height),
                           self.game.character_spritesheet[self.player_class].get_sprite(64, 64, self.width, self.height)]    
        
        self.up_animations = [self.game.character_spritesheet[self.player_class].get_sprite(0, 96, self.width, self.height),
                           self.game.character_spritesheet[self.player_class].get_sprite(32, 96, self.width, self.height),
                           self.game.character_spritesheet[self.player_class].get_sprite(64, 96, self.width, self.height)]    
    
    def update(self):
            self.movement()
            self.animate()
            self.collide_enemy()
            self.handle_shooting()
    
            self.rect.x += self.x_change
            self.collide_block('x')
            self.rect.y += self.y_change
            self.collide_block('y')
    
            self.x_change = 0
            self.y_change = 0
    
    def movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.x_change -= self.stats["speed"]
            self.facing = 'left'
        if keys[pygame.K_d]:
            self.x_change += self.stats["speed"]
            self.facing = 'right'
        if keys[pygame.K_w]:
            self.y_change -= self.stats["speed"]
            self.facing = 'up'
        if keys[pygame.K_s]:
            self.y_change += self.stats["speed"]
            self.facing = 'down'        
            
    def collide_enemy(self):
        current_time = time.time()
        if current_time - self.last_damage_time < DAMAGE_COOLDOWN:
            return
        
        hits = pygame.sprite.spritecollide(self, self.game.enemies, False)        
        if hits:
            self.stats["hp"] -= hits[0].stats["damage"]
            self.last_damage_time = current_time
            if self.stats["hp"] <= 0 :
                self.kill()
                self.game.playing = False
                
    def handle_shooting(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.shoot()
        elif keys[pygame.K_DOWN]:
            self.shoot()
        elif keys[pygame.K_LEFT]:
            self.shoot()
        elif keys[pygame.K_RIGHT]:
            self.shoot()    
            
    def shoot(self, direction=None):
            projectile = Projectile(self.game, self.rect.x, self.rect.y, direction)
            self.game.all_sprite.add(projectile)
            self.game.attacks.add(projectile)       
            
    def collide_block(self, direction):
        if direction == "x":
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.x_change > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                if self.x_change < 0:
                    self.rect.x = hits[0].rect.right

        if direction == "y":
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom
                    
    def animate(self):                    
        
        if self.facing == 'down':
            if self.y_change == 0:
                self.game.character_spritesheet[self.player_class].get_sprite(0, 0, self.width, self.height)
            else:
                self.image = self.down_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 0
                    
        if self.facing == 'up':
            if self.y_change == 0:
                self.game.character_spritesheet[self.player_class].get_sprite(0, 96, self.width, self.height)
            else:
                self.image = self.up_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 0

        if self.facing == 'left':
            if self.x_change == 0:
                self.game.character_spritesheet[self.player_class].get_sprite(0, 32, self.width, self.height)
            else:
                self.image = self.left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 0

        if self.facing == 'right':
            if self.x_change == 0:
                self.game.character_spritesheet[self.player_class].get_sprite(0, 64, self.width, self.height)
            else:
                self.image = self.right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 0
    def shoot(self):
            projectile = Projectile(self.game, self.rect.x, self.rect.y, self.facing)
            self.game.all_sprite.add(projectile)
            self.game.attacks.add(projectile) 
            
    def level_up(self, level):
        self.stats = PLAYER_LEVELS[self.player_class][str(level)].copy()
                    
class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, x, y, enemy_type, difficulty):
        self.game = game
        self._layer = ENEMY_LAYER
        self.groups = self.game.all_sprite, self.game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)  
        
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        self.difficulty = difficulty
        self.stats = ENEMY_STATS[enemy_type].copy()
        self.stats["hp"] *= self.difficulty
        self.stats["damage"] *= self.difficulty
        
        self.animation_loop = 0
        self.movement_loop = 0
        self.enemy_type = enemy_type
        
        self.image = self.game.enemy_spritesheet[self.enemy_type].get_sprite(0, 0, self.width, self.height)
        
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y  
        
        self.down_animations = [self.game.enemy_spritesheet[self.enemy_type].get_sprite(0, 0, self.width, self.height),
                           self.game.enemy_spritesheet[self.enemy_type].get_sprite(32, 0, self.width, self.height),
                           self.game.enemy_spritesheet[self.enemy_type].get_sprite(64, 0, self.width, self.height)]    
        
        self.left_animations = [self.game.enemy_spritesheet[self.enemy_type].get_sprite(0, 32, self.width, self.height),
                           self.game.enemy_spritesheet[self.enemy_type].get_sprite(32, 32, self.width, self.height),
                           self.game.enemy_spritesheet[self.enemy_type].get_sprite(64, 32, self.width, self.height)]    
        
        self.right_animations = [self.game.enemy_spritesheet[self.enemy_type].get_sprite(0, 64, self.width, self.height),
                           self.game.enemy_spritesheet[self.enemy_type].get_sprite(32, 64, self.width, self.height),
                           self.game.enemy_spritesheet[self.enemy_type].get_sprite(64, 64, self.width, self.height)]    
        
        self.up_animations = [self.game.enemy_spritesheet[self.enemy_type].get_sprite(0, 96, self.width, self.height),
                           self.game.enemy_spritesheet[self.enemy_type].get_sprite(32, 96, self.width, self.height),
                           self.game.enemy_spritesheet[self.enemy_type].get_sprite(64, 96, self.width, self.height)]         
        
    def update(self):
        self.movement()
        self.check_collision()
        self.animate()        

        
    def movement(self):
        dx = self.game.player.rect.x - self.rect.x
        dy = self.game.player.rect.y - self.rect.y
         
        if abs(dx) > abs(dy):
            if dx > 0:
                self.rect.x += self.stats["speed"]
                self.facing = 'right'
            else:
                self.rect.x -= self.stats["speed"]
                self.facing = 'left'
        else:
            if dy > 0:
                self.rect.y += self.stats["speed"]
                self.facing = 'down'
            else:
                self.rect.y -= self.stats["speed"]
                self.facing = 'up'
               
    def animate(self):                    
        
        if self.facing == 'down':
            self.image = self.down_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.1
            if self.animation_loop >= 3:
                self.animation_loop = 0
                    
        if self.facing == 'up':
            self.image = self.up_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.1
            if self.animation_loop >= 3:
                self.animation_loop = 0

        if self.facing == 'left':
            self.image = self.left_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.1
            if self.animation_loop >= 3:
                self.animation_loop = 0

        if self.facing == 'right':
            self.image = self.right_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.1
            if self.animation_loop >= 3:
                self.animation_loop = 0
                
    def check_collision(self):
            block_hit_list = pygame.sprite.spritecollide(self, self.game.blocks, False)
            enemy_hit_list = pygame.sprite.spritecollide(self, self.game.enemies, False)
    
            for block in block_hit_list:
                if self.facing == 'right':
                    self.rect.right = block.rect.left
                elif self.facing == 'left':
                    self.rect.left = block.rect.right
                elif self.facing == 'down':
                    self.rect.bottom = block.rect.top
                elif self.facing == 'up':
                    self.rect.top = block.rect.bottom
    
            for enemy in enemy_hit_list:
                if enemy != self:
                    # Move away from the colliding enemy
                    if self.rect.x < enemy.rect.x:
                        self.rect.x -= self.stats["speed"]
                    else:
                        self.rect.x += self.stats["speed"]
    
                    if self.rect.y < enemy.rect.y:
                        self.rect.y -= self.stats["speed"]
                    else:
                        self.rect.y += self.stats["speed"]        
                    
class Boss(pygame.sprite.Sprite):
    def __init__(self, game, x, y, boss_type, difficulty):
        self.game = game
        self._layer = ENEMY_LAYER
        self.groups = self.game.all_sprite, self.game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)  
        
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE * 3
        self.height = TILESIZE * 3
        self.difficulty = difficulty
        self.stats = BOSS_STATS[boss_type].copy()
        self.stats["hp"] *= self.difficulty * 0.75
        self.stats["damage"] *= self.difficulty * 0.75
        
        self.animation_loop = 0
        self.movement_loop = 0
        self.boss_type = boss_type
        
        if self.boss_type == "lowhp":
            self.image = self.game.boss_spritesheet.get_sprite(0, 288, self.width, self.height)
        elif self.boss_type == "lowdmg":
            self.image = self.game.boss_spritesheet.get_sprite(0, 0, self.width, self.height)
        elif self.boss_type == "lowspeed":
            self.image = self.game.boss_spritesheet.get_sprite(0, 96, self.width, self.height)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        
        if self.boss_type == "lowhp":
            self.animations = [self.game.boss_spritesheet.get_sprite(0, 288, self.width, self.height),
                           self.game.boss_spritesheet.get_sprite(96, 288, self.width, self.height),
                           self.game.boss_spritesheet.get_sprite(192, 288, self.width, self.height)]
        elif self.boss_type == "lowdmg":
            self.animations = [self.game.boss_spritesheet.get_sprite(0, 0, self.width, self.height),
                           self.game.boss_spritesheet.get_sprite(96, 0, self.width, self.height),
                           self.game.boss_spritesheet.get_sprite(192, 0, self.width, self.height)]
        elif self.boss_type == "lowspeed":
            self.animations = [self.game.boss_spritesheet.get_sprite(0, 96, self.width, self.height),
                           self.game.boss_spritesheet.get_sprite(96, 96, self.width, self.height),
                           self.game.boss_spritesheet.get_sprite(192, 96, self.width, self.height)]

            
    def update(self):
        self.movement()
        self.check_collision()
        self.animate()
    
    def movement(self):
        dx = self.game.player.rect.x - self.rect.x
        dy = self.game.player.rect.y - self.rect.y
         
        if abs(dx) > abs(dy):
            if dx > 0:
                self.rect.x += self.stats["speed"]
                self.facing = 'right'
            else:
                self.rect.x -= self.stats["speed"]
                self.facing = 'left'
        else:
            if dy > 0:
                self.rect.y += self.stats["speed"]
                self.facing = 'down'
            else:
                self.rect.y -= self.stats["speed"]
                self.facing = 'up'
                
    def animate(self):                    
        
        self.image = self.animations[math.floor(self.animation_loop)]
        self.animation_loop += 0.1
        if self.animation_loop >= 3:
           self.animation_loop = 0

    def check_collision(self):
            block_hit_list = pygame.sprite.spritecollide(self, self.game.blocks, False)
            enemy_hit_list = pygame.sprite.spritecollide(self, self.game.enemies, False)
    
            for block in block_hit_list:
                if self.facing == 'right':
                    self.rect.right = block.rect.left
                elif self.facing == 'left':
                    self.rect.left = block.rect.right
                elif self.facing == 'down':
                    self.rect.bottom = block.rect.top
                elif self.facing == 'up':
                    self.rect.top = block.rect.bottom
    
            for enemy in enemy_hit_list:
                if enemy != self:
                    # Move away from the colliding enemy
                    if self.rect.x < enemy.rect.x:
                        self.rect.x -= self.stats["speed"]
                    else:
                        self.rect.x += self.stats["speed"]
    
                    if self.rect.y < enemy.rect.y:
                        self.rect.y -= self.stats["speed"]
                    else:
                        self.rect.y += self.stats["speed"]
    

class Block(pygame.sprite.Sprite):
    def __init__(self,game,x,y):
        
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprite, self.game.blocks
        pygame.sprite.Sprite.__init__(self,self.groups)
        
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        
        self.image = self.game.terrain_spritesheet.get_sprite(960, 544, self.width, self.height)
        
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        
class Ground(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprite
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        
        self.image = self.game.terrain_spritesheet.get_sprite(256, 160, self.width, self.height)
        
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        
class Button:
    def __init__(self, x, y, width, height, fg, bg, content, fontsize):
        self.font = pygame.font.Font('comici.ttf', fontsize)
        self.content = content
        
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
        self.fg = fg
        self.bg = bg
        
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.bg)
        self.rect = self.image.get_rect()
        
        self.rect.x = self.x
        self.rect.y = self.y
        
        self.text = self.font.render(self.content, True, self.fg)
        self.text_rect = self.text.get_rect(center = (self.width/2, self.height/2))
        self.image.blit(self.text, self.text_rect)
        
    def is_pressed(self, pos, pressed):
        if self.rect.collidepoint(pos):
            if pressed[0]:
                return True
            else:
                return False
        return False
                
class Attack(pygame.sprite.Sprite):
    def __init__(self, game, x, y, direction):
        super().__init__()
        self.game = game
        self._layer = game.PLAYER_LAYER
        self.groups = game.all_sprite, game.attacks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x
        self.y = y
        self.width = TILESIZE
        self.height = TILESIZE
        self.direction = direction
        self.speed = 8
        self.last_damage_time = 0.0

        self.animation_loop = 0

        self.right_animations = [self.game.attack_spritesheet.get_sprite(0, 64, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(32, 64, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(64, 64, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(96, 64, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(128, 64, self.width, self.height)]

        self.down_animations = [self.game.attack_spritesheet.get_sprite(0, 32, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(32, 32, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(64, 32, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(96, 32, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(128, 32, self.width, self.height)]

        self.left_animations = [self.game.attack_spritesheet.get_sprite(0, 96, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(32, 96, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(64, 96, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(96, 96, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(128, 96, self.width, self.height)]

        self.up_animations = [self.game.attack_spritesheet.get_sprite(0, 0, self.width, self.height),
                         self.game.attack_spritesheet.get_sprite(32, 0, self.width, self.height),
                         self.game.attack_spritesheet.get_sprite(64, 0, self.width, self.height),
                         self.game.attack_spritesheet.get_sprite(96, 0, self.width, self.height),
                         self.game.attack_spritesheet.get_sprite(128, 0, self.width, self.height)]

        self.image = self.down_animations[0]

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.animate()
        self.collide()

        if self.direction == 'up':
            self.rect.y -= self.speed
        elif self.direction == 'down':
            self.rect.y += self.speed
        elif self.direction == 'left':
            self.rect.x -= self.speed
        elif self.direction == 'right':
            self.rect.x += self.speed

        player_center_x = self.game.player.rect.x + self.game.player.width / 2
        player_center_y = self.game.player.rect.y + self.game.player.height / 2

        if self.direction == 'up':
            self.rect.centery = player_center_y
            self.rect.centerx = player_center_x
        elif self.direction == 'down':
            self.rect.centery = player_center_y
            self.rect.centerx = player_center_x
        elif self.direction == 'left':
            self.rect.centery = player_center_y
            self.rect.right = player_center_x
        elif self.direction == 'right':
            self.rect.centery = player_center_y
            self.rect.left = player_center_x                

    def collide(self):
        current_time = time.time()
        if current_time - self.last_damage_time < 0.25:
            return
        hits = pygame.sprite.spritecollide(self, self.game.enemies, False)
        if hits:
            self.last_damage_time = current_time
            hits[0].stats["hp"] -= self.game.player.stats["damage"]
            if hits[0].stats["hp"] <= 0:
                hits[0].kill()
                

    def animate(self):
        direction = self.direction
    
        if direction == 'down':
            self.image = self.down_animations[math.floor(self.animation_loop)]
        elif direction == 'up':
            self.image = self.up_animations[math.floor(self.animation_loop)]
        elif direction == 'left':
            self.image = self.left_animations[math.floor(self.animation_loop)]
        elif direction == 'right':
            self.image = self.right_animations[math.floor(self.animation_loop)]
    
        self.animation_loop += 0.5
        if self.animation_loop >= 5:
            self.kill() 
                
                
class Projectile(pygame.sprite.Sprite):
    def __init__(self, game, x, y, direction):
        super().__init__()
        self.game = game
        self._layer = game.PLAYER_LAYER
        self.groups = game.all_sprite, game.attacks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x
        self.y = y
        self.width = TILESIZE
        self.height = TILESIZE
        self.direction = direction
        self.speed = 4

        if direction == 'up':
            self.image = self.game.attack_spritesheet.get_sprite(0, 0, self.width, self.height)
        elif direction == 'down':
            self.image = self.game.attack_spritesheet.get_sprite(0, 64, self.width, self.height)
        elif direction == 'left':
            self.image = self.game.attack_spritesheet.get_sprite(0, 96, self.width, self.height)
        elif direction == 'right':
            self.image = self.game.attack_spritesheet.get_sprite(0, 32, self.width, self.height)

        if direction == 'up' or direction == 'down':
            self.rect = self.image.get_rect(center=(x + TILESIZE // 2, y + TILESIZE // 2))
        elif direction == 'left':
            self.rect = self.image.get_rect(center=(x, y + TILESIZE // 2))
        elif direction == 'right':
            self.rect = self.image.get_rect(center=(x + TILESIZE, y + TILESIZE // 2))

    def update(self):
        if self.direction == 'up':
            self.rect.y -= self.speed
        elif self.direction == 'down':
            self.rect.y += self.speed
        elif self.direction == 'left':
            self.rect.x -= self.speed
        elif self.direction == 'right':
            self.rect.x += self.speed

        hits = pygame.sprite.spritecollide(self, self.game.enemies, True)
        if hits:
            self.kill()

class Spawn(pygame.sprite.Sprite):
    def __init__(self,game,x,y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprite
        pygame.sprite.Sprite.__init__(self,self.groups)
        
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        
        self.image = self.game.terrain_spritesheet.get_sprite(256, 160, self.width, self.height)
        
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
    
    def spawn_enemy(self,difficulty):
        count = random.randint(0,2)
        ENEMY_TYPES = ["basic", "lowhp", "lowdmg", "lowspeed"]
        k = random.randint(0,3)
        for i in range(count):
            Enemy(self.game,self.x/TILESIZE,self.y/TILESIZE,ENEMY_TYPES[k],difficulty)