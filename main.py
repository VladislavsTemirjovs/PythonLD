import pygame as pg
from sprites import *
from config import *
import sys

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH,HEIGHT))
        self.clock = pg.time.Clock()
        self.font = pg.font.Font('comici.ttf', 32)
        self.running = True
        self.points = 0
        
        self.character_spritesheet = Spritesheet('img/character.png')
        self.terrain_spritesheet = Spritesheet('img/terrain.png')
        self.enemy_spritesheet = Spritesheet('img/enemy.png')
        self.intro_background = pg.image.load('img/introbackground.png')
        self.go_background = pg.image.load('img/gameover.png')
        self.attack_spritesheet = Spritesheet('img/attack.png')
        
    def create_tilemap(self):
        for i, row in enumerate(tilemap):
            for j, column in enumerate(row):
                Ground(self, j, i)
                if column == "#":
                    Block(self, j, i)
                if column == "P":
                    self.player = Player(self,j,i)
                if column == "E":
                    Enemy(self,j,i)
            
        
    def new(self):
        self.playing = True
        self.all_sprite = pg.sprite.LayeredUpdates()
        self.blocks = pg.sprite.LayeredUpdates()
        self.enemies = pg.sprite.LayeredUpdates()
        self.attacks = pg.sprite.LayeredUpdates()
        
        self.create_tilemap()
        
        
    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.playing = False
                self.running = False
            
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    if self.player.facing == 'up':
                        Attack(self, self.player.rect.x, self.player.rect.y - TILESIZE)
                    if self.player.facing == 'down':
                        Attack(self, self.player.rect.x, self.player.rect.y + TILESIZE)
                    if self.player.facing == 'left':
                        Attack(self, self.player.rect.x - TILESIZE, self.player.rect.y)
                    if self.player.facing == 'right':
                        Attack(self, self.player.rect.x + TILESIZE, self.player.rect.y)       
    
    def update(self):
        self.all_sprite.update()
        
        self.points += self.clock.get_rawtime()/600
        
    def draw(self):
        self.screen.fill(BLACK)
        self.all_sprite.draw(self.screen)
        
        timer_text = self.font.render(f'Score: {int(self.points)}', True, WHITE)
        self.screen.blit(timer_text, (10,10))
        
        self.clock.tick(FPS)
        pg.display.update()
        
        
    def main(self):
        while self.playing:
            self.events()
            self.update()
            self.draw()
        
    def game_over(self):
        text = self.font.render('Game Over', True, WHITE)
        text_rect = text.get_rect(center=(WIDTH/2, HEIGHT/2))

        restart_button = Button(10, 50, 150, 50, WHITE, BLACK, 'Restart', 32)

        for sprite in self.all_sprite:
            sprite.kill()
        
        while self.running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
            
            mouse_pos = pg.mouse.get_pos()
            mouse_pressed = pg.mouse.get_pressed()
            
            if restart_button.is_pressed(mouse_pos, mouse_pressed):
                self.new()
                self.main()
                
            self.screen.blit(self.go_background, (0,0))
            self.screen.blit(text, text_rect)
            self.screen.blit(restart_button.image, restart_button.rect)
            self.clock.tick(FPS)
            pg.display.update()
        
    def intro_screen(self):
        intro = True
        
        title = self.font.render('Python Lielais Darbs', True, BLACK)
        title_rect = title.get_rect(x=10, y=10)
        
        play_button = Button(10, 50, 100, 50, WHITE, BLACK, 'Play', 32)
        
        while intro:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    intro = False
                    self.running = False
            mouse_pos = pg.mouse.get_pos()
            mouse_pressed = pg.mouse.get_pressed()

            if play_button.is_pressed(mouse_pos, mouse_pressed):
                intro = False
                
            self.screen.blit(self.intro_background, (0,0))
            self.screen.blit(title, title_rect)
            self.screen.blit(play_button.image, play_button.rect)
            self.clock.tick(FPS)
            pg.display.update()

g = Game()
g.intro_screen()
g.new()
while g.running:
    g.main()
    g.game_over()
    
pg.quit()
sys.exit()
