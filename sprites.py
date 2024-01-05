import pygame
from config import *
import math
import random
import time

class Spritesheet:
    def __init__(self,file):
        self.sheet = pygame.image.load(file).convert()
        
    def get_sprite(self,x,y,width,height):
        sprite = pygame.Surface([width,height])
        sprite.blit(self.sheet, (0,0), (x,y, width, height))
        sprite.set_colorkey(BLACK)
        return sprite           

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y,player_class):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprite
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        self.player_class = player_class
        self.stats = PLAYER_STATS[player_class]
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
        
        self.rect.x += self.x_change
        self.collide_block('x')
        self.rect.y += self.y_change
        self.collide_block('y')
        
        self.x_change = 0
        self.y_change = 0
    
    def movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            for sprite in self.game.all_sprite:
                sprite.rect.x += self.stats["speed"]
            self.x_change -= self.stats["speed"]
            self.facing = 'left'
        if keys[pygame.K_d]:
            for sprite in self.game.all_sprite:
                sprite.rect.x -= self.stats["speed"]
            self.x_change += self.stats["speed"]
            self.facing = 'right'
        if keys[pygame.K_w]:
            for sprite in self.game.all_sprite:
                sprite.rect.y += self.stats["speed"]
            self.y_change -= self.stats["speed"]
            self.facing = 'up'
        if keys[pygame.K_s]:
            for sprite in self.game.all_sprite:
                sprite.rect.y -= self.stats["speed"]
            self.y_change += self.stats["speed"]
            self.facing = 'down'
            
    def collide_enemy(self):
        current_time = time.time()
        if current_time - self.last_damage_time < DAMAGE_COOLDOWN:
            return
        
        hits = pygame.sprite.spritecollide(self, self.game.enemies, False)        
        if hits:
            self.stats["hp"] -= ENEMY_DAMAGE
            self.last_damage_time = current_time
            if self.stats["hp"] <= 0 :
                self.kill()
                self.game.playing = False
            
    def collide_block(self, direction):
        if direction == "x":
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.x_change > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                    for sprites in self.game.all_sprite:
                        sprites.rect.x += self.stats["speed"]
                if self.x_change < 0:
                    for sprites in self.game.all_sprite:
                        sprites.rect.x -= self.stats["speed"]
                    self.rect.x = hits[0].rect.right

        if direction == "y":
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                    for sprites in self.game.all_sprite:
                        sprites.rect.y += self.stats["speed"]
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom
                    for sprites in self.game.all_sprite:
                        sprites.rect.y -= self.stats["speed"]
                    
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
                    
class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = ENEMY_LAYER
        self.groups = self.game.all_sprite, self.game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)  
        
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        
        self.facing = random.choice(['left', 'right'])
        self.animation_loop = 0
        self.movement_loop = 0
        self.max_travel = random.randint(7,30)
        
        self.image = self.game.enemy_spritesheet.get_sprite(0, 0, self.width, self.height)
        
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y  
        
        self.down_animations = [self.game.enemy_spritesheet.get_sprite(0, 0, self.width, self.height),
                           self.game.enemy_spritesheet.get_sprite(32, 0, self.width, self.height),
                           self.game.enemy_spritesheet.get_sprite(64, 0, self.width, self.height)]    
        
        self.left_animations = [self.game.enemy_spritesheet.get_sprite(0, 32, self.width, self.height),
                           self.game.enemy_spritesheet.get_sprite(32, 32, self.width, self.height),
                           self.game.enemy_spritesheet.get_sprite(64, 32, self.width, self.height)]    
        
        self.right_animations = [self.game.enemy_spritesheet.get_sprite(0, 64, self.width, self.height),
                           self.game.enemy_spritesheet.get_sprite(32, 64, self.width, self.height),
                           self.game.enemy_spritesheet.get_sprite(64, 64, self.width, self.height)]    
        
        self.up_animations = [self.game.enemy_spritesheet.get_sprite(0, 96, self.width, self.height),
                           self.game.enemy_spritesheet.get_sprite(32, 96, self.width, self.height),
                           self.game.enemy_spritesheet.get_sprite(64, 96, self.width, self.height)]         
        
    def update(self):
        self.movement()
        self.animate()        

        
    def movement(self):
        dx = self.game.player.rect.x - self.rect.x
        dy = self.game.player.rect.y - self.rect.y
         
        if abs(dx) > abs(dy):
            if dx > 0:
                self.rect.x += ENEMY_SPEED
                self.facing = 'right'
            else:
                self.rect.x -= ENEMY_SPEED
                self.facing = 'left'
        else:
            if dy > 0:
                self.rect.y += ENEMY_SPEED
                self.facing = 'down'
            else:
                self.rect.y -= ENEMY_SPEED
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
    
    def __init__(self,game,x,y):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprite, self.game.attacks
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        self.x = x
        self.y = y
        self.width = TILESIZE
        self.height = TILESIZE
        
        self.animation_loop = 0
        
        self.image = self.game.attack_spritesheet.get_sprite(0, 0, self.width, self.height)
        
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        
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
        
    def update(self):
        self.animate()
        self.collide()
    
    def collide(self):
        hits = pygame.sprite.spritecollide(self, self.game.enemies, True)
        
    def animate(self):
        direction = self.game.player.facing                    
        
        if direction == 'down':
            self.image = self.down_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 5:
                self.kill()
                    
        if direction == 'up':
            self.image = self.up_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 5:
                self.kill()

        if direction == 'left':
            self.image = self.left_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 5:
                self.kill()

        if direction == 'right':
            self.image = self.right_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 5:
                self.kill()
        
        