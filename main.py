import pygame
import sys

# Constants
WIDTH, HEIGHT = 1200, 700
PLAYER_SIZE = 50
PROJECTILE_SIZE = 10
MAP_WIDTH, MAP_HEIGHT = 3000, 1500
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
MENU_FONT_SIZE = 48

# Initialize pygame
pygame.init()

# Display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("The Cool Game")

# Menu
class Menu:
    def __init__(self):
        self.font = pygame.font.Font(None, MENU_FONT_SIZE)

    def draw(self, screen):
        title_text = self.font.render("The Cool Game", True, WHITE)
        start_text = self.font.render("Press SPACE to start", True, WHITE)

        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 3))
        screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2))

# Player
class Player:
    def __init__(self, x, y, size):
        self.rect = pygame.Rect(x, y, size, size)

    def can_move_x(self, dx, obstacles):
        test_rect = self.rect.copy()
        test_rect.x += dx
        return all(not test_rect.colliderect(obstacle) for obstacle in obstacles) and 0 <= test_rect.left and test_rect.right <= MAP_WIDTH

    def can_move_y(self, dy, obstacles):
        test_rect = self.rect.copy()
        test_rect.y += dy
        return all(not test_rect.colliderect(obstacle) for obstacle in obstacles) and 0 <= test_rect.bottom and test_rect.top <= MAP_HEIGHT

    def move(self, dx, dy, obstacles):
        if self.can_move_x(dx, obstacles):
            self.rect.x += dx
        if self.can_move_y(dy, obstacles):
            self.rect.y += dy

    def draw(self, surface, camera_x, camera_y):
        pygame.draw.rect(surface, BLUE, (self.rect.x - camera_x, self.rect.y - camera_y, self.rect.width, self.rect.height))

# Projectile
class Projectile:
    def __init__(self, x, y, size, speed, direction):
        self.rect = pygame.Rect(x - size // 2, y - size // 2, size, size)
        self.size = size
        self.speed = speed
        self.direction = direction

    def move(self):
        if self.direction == "up":
            self.rect.y -= self.speed
        elif self.direction == "down":
            self.rect.y += self.speed
        elif self.direction == "left":
            self.rect.x -= self.speed
        elif self.direction == "right":
            self.rect.x += self.speed

    def draw(self, surface, camera_x, camera_y):
        pygame.draw.rect(surface, BLACK, (self.rect.x - camera_x, self.rect.y - camera_y, self.rect.width, self.rect.height))

# GameMap
class GameMap:
    def __init__(self, data):
        self.data = data

    def draw(self, surface, camera_x, camera_y, tile_size):
        for y, row in enumerate(self.data):
            for x, char in enumerate(row):
                if char == "#":
                    pygame.draw.rect(surface, BLACK, (x * tile_size - camera_x, y * tile_size - camera_y, tile_size, tile_size))

    def get_obstacles(self, tile_size):
        obstacles = [pygame.Rect(x * tile_size, y * tile_size, tile_size, tile_size) for y, row in enumerate(self.data) for x, char in enumerate(row) if char == "#"]
        return obstacles

# Initialize game entities
player = Player(WIDTH // 2 - PLAYER_SIZE // 2, HEIGHT - 2 * PLAYER_SIZE, PLAYER_SIZE)
projectiles = []  
projectile_delay = 0  
projectile_delay_max = 10  
game_map = GameMap([
    "#############################################################",
    "#                                                           #",
    "#   #####              ####                                 #",
    "#   #   #           ####                                    #",
    "#   #   #           #    ####                               #",
    "#   #   #           #    #                                  #",
    "#                                                           #",
    "#                                                           #",
    "#      ###                                                  #",
    "#                   #                               #       #",
    "#     ###                                                   #",
    "#                                                           #",
    "#                   ####                                    #",
    "#                   #  ##                                   #",
    "#          #        #                                       #",
    "#          #        #####                                   #",
    "#       ####                                                #",
    "#          #                                                #",
    "#                                                           #",
    "#                                                           #",
    "#                                                           #",
    "#                                                           #",
    "#                                                           #",
    "#                                                           #",
    "#                                                           #",
    "#                                                           #",
    "#                                                           #",
    "#                                                           #",
    "#                                                           #",
    "#                                                           #",
    "#############################################################",
])

menu = Menu()

# Game loop
clock = pygame.time.Clock()
running = True
is_in_menu = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            is_in_menu = False

    if is_in_menu:
        screen.fill(BLACK)
        menu.draw(screen)
    else:
        keys = pygame.key.get_pressed()
        player_speed = 5
        dx = (keys[pygame.K_d] - keys[pygame.K_a]) * player_speed
        dy = (keys[pygame.K_s] - keys[pygame.K_w]) * player_speed
        player.move(dx, dy, game_map.get_obstacles(PLAYER_SIZE))

        # Shooting projectiles with arrow keys
        if keys[pygame.K_LEFT] and projectile_delay <= 0:
            arrow = Projectile(player.rect.x, player.rect.y + player.rect.height // 2, PROJECTILE_SIZE, 6, "left")
            projectiles.append(arrow)
            projectile_delay = projectile_delay_max
        elif keys[pygame.K_RIGHT] and projectile_delay <= 0:
            arrow = Projectile(player.rect.x + player.rect.width, player.rect.y + player.rect.height // 2, PROJECTILE_SIZE, 6, "right")
            projectiles.append(arrow)
            projectile_delay = projectile_delay_max
        elif keys[pygame.K_UP] and projectile_delay <= 0:
            arrow = Projectile(player.rect.x + player.rect.width // 2, player.rect.y, PROJECTILE_SIZE, 6, "up")
            projectiles.append(arrow)
            projectile_delay = projectile_delay_max
        elif keys[pygame.K_DOWN] and projectile_delay <= 0:
            arrow = Projectile(player.rect.x + player.rect.width // 2, player.rect.y + player.rect.height, PROJECTILE_SIZE, 6, "down")
            projectiles.append(arrow)
            projectile_delay = projectile_delay_max

        # Move and draw projectiles
        for projectile in projectiles:
            projectile.move()

        # Remove projectiles that are out of the screen
        projectiles = [projectile for projectile in projectiles if
                       0 <= projectile.rect.left <= MAP_WIDTH and 0 <= projectile.rect.top <= MAP_HEIGHT]

        screen.fill(WHITE)

        # Calculate camera position based on player's position
        camera_x = player.rect.x - WIDTH // 2
        camera_y = player.rect.y - HEIGHT // 2

        # Draw the map and player with adjusted positions
        game_map.draw(screen, camera_x, camera_y, PLAYER_SIZE)
        player.draw(screen, camera_x, camera_y)

        # Draw projectiles
        for projectile in projectiles:
            projectile.draw(screen, camera_x, camera_y)

    # Refresh display
    pygame.display.flip()

    # Set the frame rate
    clock.tick(60)

    # Update projectile delay
    projectile_delay = max(0, projectile_delay - 1)

# Quit pygame
pygame.quit()
sys.exit()

