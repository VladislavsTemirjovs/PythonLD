import pygame
from config import *
import math
import random
import time

#Attēlu apstrāde un ielādēšana
class Spritesheet:
    def __init__(self, file, key_color):
        self.sheet = pygame.image.load(file).convert()
        #color_key atbild, lai attēla fons būtu caurspīdīgs
        self.color_key = key_color

    def get_sprite(self, x, y, width, height):
        sprite = pygame.Surface([width, height])
        sprite.blit(self.sheet, (0, 0), (x, y, width, height))
        sprite.set_colorkey(self.color_key)
        return sprite         

#Spēlētaja klase, kas manto sprite klases īpašības
class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y, player_class):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprite
        pygame.sprite.Sprite.__init__(self, self.groups)

        #Galvenie parametri
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        self.player_class = player_class
        self.stats = PLAYER_STATS[player_class].copy()
        self.last_damage_time = 0.0
        self.shoot_cooldown = self.stats["shotspeed"]
        self.last_shoot_time = 0.0   

        self.x_change = 0
        self.y_change = 0

        self.facing = 'down'
        self.animation_loop = 0

        self.image = self.game.character_spritesheet[self.player_class].get_sprite(0, 0, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        

        #Animācijas massīvi
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
      
#Funkcija, kas izpilda visas spēlētāja funkcijas, lai spēlētājs varētu atrasties uz kartes       
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

#Pārvietošanās funkcija   
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

#Pārbaude vai nav saskarsmes ar briesmoņiem            
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

#Spēlētāja šaušanas funkcijas                
    def handle_shooting(self):
        keys = pygame.key.get_pressed()
        current_time = time.time()

        if keys[pygame.K_UP]:
            self.shoot('up', current_time)
        elif keys[pygame.K_DOWN]:
            self.shoot('down', current_time)
        elif keys[pygame.K_LEFT]:
            self.shoot('left', current_time)
        elif keys[pygame.K_RIGHT]:
            self.shoot('right', current_time)

    #Izveido šāviena attēlu un norāda virzienu, nosaka vai ir pagājis pietiekami daudz laika no pēdējā šaviena
    def shoot(self, direction, current_time):
        if current_time - self.last_shoot_time < self.shoot_cooldown:
            return

        projectile = Projectile(self.game, self.rect.x, self.rect.y, direction, self.player_class)
        self.game.all_sprite.add(projectile)
        self.game.attacks.add(projectile)

        self.last_shoot_time = current_time                       

#Pārbauda saskaršanos ar sienām, ja saskarsme bija, tad spēlētājs nevar iet tajā virzienā           
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

#Funkcija, kas atbild par animāciju                    
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
#Funkcija, kas ļauj spēlētājam paaugstināt līmeni un tādā veidā mainās spēlētāja atribūti            
    def level_up(self, level):
        self.stats = PLAYER_LEVELS[self.player_class][str(level)].copy()

#Briesmoņu klase                    
class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, x, y, enemy_type,difficulty):
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
        
        #Briemoņu animācija
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

#Briesmoņu kustība, kustība notiek spēlētāja virzienā, ja starp spēlētāju un briesmoni x attālums ir lielāks nekā y attālums, tad kustība notiek pa x
#Pretējā gadījumā kustība notiek pa y asi    
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
#Animācijas funkcija             
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
#Pārbauda, vai nav sadursmes ar šķēršļiem vai citiem briesmoņiem
#Šķēršļu gadījumā kustība tiek pārtraukta, bet briesmoņu gadījumā tie attiet viens no otra                 
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
                    if self.rect.x < enemy.rect.x:
                        self.rect.x -= self.stats["speed"]
                    else:
                        self.rect.x += self.stats["speed"]
    
                    if self.rect.y < enemy.rect.y:
                        self.rect.y -= self.stats["speed"]
                    else:
                        self.rect.y += self.stats["speed"]        

#Lielo briesmoņu klase, ļoti līdzīga briesmoņu klasei                    
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
                    if self.rect.x < enemy.rect.x:
                        self.rect.x -= self.stats["speed"]
                    else:
                        self.rect.x += self.stats["speed"]
    
                    if self.rect.y < enemy.rect.y:
                        self.rect.y -= self.stats["speed"]
                    else:
                        self.rect.y += self.stats["speed"]

#Kartes sienas jeb šķērsļi                       
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
 
#Kartes "zemes" slānis        
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

#Klase, kas veido pogas, kuras tiek izmantotas main.py, sākuma un beigu ekrānā       
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

#Pārbaude, vai poga ir nospiesta        
    def is_pressed(self, pos, pressed):
        if self.rect.collidepoint(pos):
            if pressed[0]:
                return True
            else:
                return False
        return False

#Klase, kas atbild par tiešo uzbrukumu, spēlētāja priekšā                
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
        
        #Animācijas attēli
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

#Pārbauda, vai nav saskarsmes ar briesmoni
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
                
#Funkcija, kas veido animāciju
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
  
#Šāvienu klase, kas veido lidojošus uzbrukumus                                
class Projectile(pygame.sprite.Sprite):
    def __init__(self, game, x, y, direction,player_class):
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
        self.bullet_type = player_class

        #Katrai klasei savs šāviena tips
        if self.bullet_type == "peasant":
            self.image = self.game.projectile_spritesheet.get_sprite(224, 480, TILESIZE, TILESIZE)
        elif self.bullet_type == "mage":
            self.image = self.game.projectile_spritesheet.get_sprite(352, 192, TILESIZE, TILESIZE)
        elif self.bullet_type == "soldier":
            self.image = self.game.projectile_spritesheet.get_sprite(512, 192, TILESIZE, TILESIZE)

        if direction == 'up' or direction == 'down':
            self.rect = self.image.get_rect(center=(x + TILESIZE // 2, y + TILESIZE // 2))
        elif direction == 'left':
            self.rect = self.image.get_rect(center=(x, y + TILESIZE // 2))
        elif direction == 'right':
            self.rect = self.image.get_rect(center=(x + TILESIZE, y + TILESIZE // 2))

#Klase, kas atibild par šāviena kustību un pārbauda vai nav
    def update(self):
        if self.direction == 'up':
            self.rect.y -= self.speed
        elif self.direction == 'down':
            self.rect.y += self.speed
        elif self.direction == 'left':
            self.rect.x -= self.speed
        elif self.direction == 'right':
            self.rect.x += self.speed

#Ja notiek sadursme ar briesmoni, tad šāviens pazūd un briemonis saņem bojājumus
        enemy_hits = pygame.sprite.spritecollide(self, self.game.enemies, False)
        if enemy_hits:
            enemy_hits[0].stats["hp"] -= self.game.player.stats["damage"]
            if enemy_hits[0].stats["hp"] <= 0:
                enemy_hits[0].kill()
            self.kill()

        block_hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
        if block_hits:
            self.kill()        

#Klase, kura tiek izmnatota, lai veidotu jaunus briesmoņus, izveides koordinātes var mainīt config.py pie tilemap, burts "S"            
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
#Jaunu briesmoņu izveido no to "izveides punktiem"   
    def spawn_enemy(self, difficulty):
        count = random.randint(0,2)
        enemy_types = ["basic", "lowhp", "lowdmg", "lowspeed"]
        k = random.randint(0,3)
        for i in range(count):
            Enemy(self.game,self.x/TILESIZE,self.y/TILESIZE,enemy_types[k],difficulty)
