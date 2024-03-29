import pygame as pg
from sprites import *
from config import *
import sys
import math

class Game:
    def __init__(self):
        pg.init()
#pamata atribūtu izveide
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.clock = pg.time.Clock()
        self.font = pg.font.Font('comici.ttf', 32)
        self.font_stats = pg.font.Font('comici.ttf', 16)
        self.running = True
        self.points = 0
        
#Attēlu inicializācija
        self.character_spritesheet = {"peasant": Spritesheet('img/peasant.png',BLACK),
                                      "soldier": Spritesheet('img/soldier.png',BLACK),
                                      "mage": Spritesheet('img/mage.png',BLACK)}
        self.projectile_spritesheet =Spritesheet('img/projectile.png',BLACK)
        self.terrain_spritesheet = Spritesheet('img/terrain.png',BLACK)
        self.enemy_spritesheet = {"basic": Spritesheet('img/enemy.png',BLACK),
                                  "lowhp": Spritesheet('img/lowhp.png',BLACK),
                                  "lowdmg": Spritesheet('img/lowdmg.png',BLACK),
                                  "lowspeed": Spritesheet('img/lowspeed.png',BLACK)}
        self.boss_spritesheet = Spritesheet('img/Boss.png', WHITE)
        self.intro_background = pg.image.load('img/introbackground.png')
        self.go_background = pg.image.load('img/gameover.png')
        self.attack_spritesheet = Spritesheet('img/attack.png',BLACK)

#Attēlu savstarpējs novietojums
        self.PLAYER_LAYER = PLAYER_LAYER
        self.ENEMY_LAYER = ENEMY_LAYER
        self.BLOCK_LAYER = BLOCK_LAYER
        self.GROUND_LAYER = GROUND_LAYER
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.spawn_points = []
        self.difficulty = 1
        
#Eventu izveide
        self.level_up_interval = LEVEL_UP_DELAY
        self.level_up_event = pg.USEREVENT+0
        pg.time.set_timer(self.level_up_event, self.level_up_interval) 
        
        self.new_enemy_interval = ENEMY_SPAWN_DELAY
        self.new_enemy_event = pg.USEREVENT+1
        pg.time.set_timer(self.new_enemy_event, self.new_enemy_interval)
        
        self.new_boss_interval = BOSS_SPAWN_DELAY
        self.new_boss_event = pg.USEREVENT+2
        pg.time.set_timer(self.new_boss_event, self.new_boss_interval) 
            
#Kartes inicializācija
    def create_tilemap(self):
        for i, row in enumerate(tilemap):
            for j, column in enumerate(row):
                Ground(self, j, i)
                if column == "#":
                    Block(self, j, i)
                if column == "P":
                    self.player = Player(self,j,i,self.player_class)
                if column == "E":
                    Enemy(self,j,i,"basic",self.difficulty)
                if column == "S":
                    self.spawn_points.append(Spawn(self,j,i))
            
#Jaunas spēles izveide, tiek inicializēti attēli un to novietojums
    def new(self):
        self.playing = True
        self.all_sprite = pg.sprite.LayeredUpdates()
        self.blocks = pg.sprite.LayeredUpdates()
        self.enemies = pg.sprite.LayeredUpdates()
        self.attacks = pg.sprite.LayeredUpdates()
        
        self.create_tilemap()
        
#Eventu pārbaude un izpilde       
    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.playing = False
                self.running = False
            
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.handle_attack()
                    
            if event.type == self.level_up_event:
                if self.player.stats["level"] >= 20:
                    pass
                else:
                    self.player.stats = PLAYER_LEVELS[self.player.player_class][str(self.player.stats["level"]+1)]
                    
            if event.type == self.new_enemy_event:
                for spawner in self.spawn_points:
                    spawner.spawn_enemy(self.difficulty)
                    
            if event.type == self.new_boss_event:
                for sprite in self.enemies:
                    sprite.kill()
                type = random.randint(0,2)
                Boss(self, 20,10,BOSS_TYPES[type],self.difficulty)
                self.difficulty += 0.25
                
                
#Funkcija, kas atbild par uzbrukumu veidošanu                
    def handle_attack(self):
        Attack(self, self.player.rect.x, self.player.rect.y + TILESIZE, self.player.facing)   

   
    def update(self):
        self.events()
        self.all_sprite.update()
        self.points += self.clock.tick() / 100
        

#Ekrāna zīmēšana        
    def draw(self):
        self.screen.fill(BLACK)
        self.all_sprite.draw(self.screen)
        
        timer_text = self.font.render(f'Score: {int(self.points)}', True, WHITE)
        self.screen.blit(timer_text, (10,10))
        stats_text1 = self.font_stats.render(f'HP: {math.floor(self.player.stats["hp"])} | Speed: {self.player.stats["speed"]}', True, WHITE)
        stats_rect1 = stats_text1.get_rect(topright=(WIDTH - 10, 10))
        self.screen.blit(stats_text1, stats_rect1)
        stats_text2 = self.font_stats.render(f'Damage: {self.player.stats["damage"]} | Range: {self.player.stats["range"]}', True, WHITE)
        stats_rect2 = stats_text2.get_rect(topright=(WIDTH - 10, 26))
        self.screen.blit(stats_text2, stats_rect2)
        stats_text3 = self.font_stats.render(f'Level: {self.player.stats["level"]}', True, WHITE)
        stats_rect3 = stats_text3.get_rect(topright=(WIDTH - 10, 42))
        self.screen.blit(stats_text3, stats_rect3)

        
        self.clock.tick(FPS)
        pg.display.update()
        
#Galvenais spēles ekrāns, kur notiek spēle       
    def main(self):
        while self.playing:
            self.events()
            self.update()
            self.draw()
 
#Zaudējuma ekrāns       
    def game_over(self):
        text = self.font.render('Game Over', True, WHITE)
        text_rect = text.get_rect(center=(WIDTH/2, HEIGHT/2))
        restart_peasant_button = Button(10, 150, 300, 50, WHITE, BLACK, 'Restart as Peasant', 32)
        restart_mage_button = Button(10, 250, 300, 50, WHITE, BLACK, 'Restart as Mage', 32)
        restart_soldier_button = Button(10, 350, 300, 50, WHITE, BLACK, 'Restart as Soldier', 32)

        for sprite in self.all_sprite:
            sprite.kill()
        
        while self.running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
            
            mouse_pos = pg.mouse.get_pos()
            mouse_pressed = pg.mouse.get_pressed()
            
            
            if restart_peasant_button.is_pressed(mouse_pos, mouse_pressed):
                self.player_class = "peasant"
                self.points = 0
                self.new()
                self.main()
            
            if restart_mage_button.is_pressed(mouse_pos, mouse_pressed):
                self.player_class = "mage"
                self.points = 0
                self.new()
                self.main()
            
            if restart_soldier_button.is_pressed(mouse_pos, mouse_pressed):
                self.player_class = "soldier"
                self.points = 0
                self.new()
                self.main()
                
            self.screen.blit(self.go_background, (0,0))
            self.screen.blit(text, text_rect)
            self.screen.blit(restart_peasant_button.image, restart_peasant_button.rect)
            self.screen.blit(restart_mage_button.image, restart_mage_button.rect)
            self.screen.blit(restart_soldier_button.image, restart_soldier_button.rect)
            self.clock.tick(FPS)
            pg.display.update()

#Sākuma ekrāns        
    def intro_screen(self):
        intro = True
        
        title = self.font.render('Not your average Survival Game', True, BLACK)
        title_rect = title.get_rect(x=10, y=10)
        peasant_button = Button(10, 150, 300, 50, WHITE, BLACK, 'Play as Peasant', 32)
        mage_button = Button(10, 250, 300, 50, WHITE, BLACK, 'Play as Mage', 32)
        soldier_button = Button(10, 350, 300, 50, WHITE, BLACK, 'Play as Soldier', 32)
        
        while intro:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    intro = False
                    self.running = False
            mouse_pos = pg.mouse.get_pos()
            mouse_pressed = pg.mouse.get_pressed()
            
            if peasant_button.is_pressed(mouse_pos,mouse_pressed):
                self.player_class = "peasant"
                intro = False
            
            if mage_button.is_pressed(mouse_pos,mouse_pressed):
                self.player_class = "mage"
                intro = False
                
            if soldier_button.is_pressed(mouse_pos,mouse_pressed):
                self.player_class = "soldier"
                intro = False
                
            self.screen.blit(self.intro_background, (0,0))
            self.screen.blit(title, title_rect)
            self.screen.blit(peasant_button.image, peasant_button.rect)
            self.screen.blit(mage_button.image, mage_button.rect)
            self.screen.blit(soldier_button.image, soldier_button.rect)
            self.clock.tick(FPS)
            pg.display.update()

#Spēles izveide un palaišana
g = Game()
g.intro_screen()
g.new()
while g.running:
    g.main()
    g.game_over()
    
pg.quit()
sys.exit()
