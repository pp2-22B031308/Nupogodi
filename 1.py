import pygame
import random

# Define constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 500
WOLF_POSITIONS = [(50, 320), (200, 320), (370, 320), (540, 320)]

# Define classes
class Player(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.image = pygame.image.load("player.png").convert_alpha()
        self.rect = self.image.get_rect(center=position)

    class Arm:
        def __init__(self, image, positions):
            self.image = image
            self.positions = positions
            self.current_position = 0

        def move_left(self):
            self.current_position = (self.current_position - 1) % len(self.positions)

        def move_right(self):
            self.current_position = (self.current_position + 1) % len(self.positions)

        def draw(self, screen):
            screen.blit(self.image, self.positions[self.current_position])
            return pygame.Rect(self.positions[self.current_position], self.image.get_size())

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.move_ip(-5, 0)
        if keys[pygame.K_RIGHT]:
            self.rect.move_ip(5, 0)
        self.rect.left = max(self.rect.left, 0)
        self.rect.right = min(self.rect.right, SCREEN_WIDTH)

class Egg(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.image = pygame.image.load("egg.png").convert_alpha()
        self.rect = self.image.get_rect(center=position)

    def update(self):
        self.rect.move_ip(0, 5)
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

# Initialize Pygame
pygame.init()

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("nu pogodi")

# Load the images
background_img = pygame.image.load("fon.png").convert()
basket_img = pygame.image.load("arm.png").convert_alpha()
chicken_img = pygame.image.load("lose.png").convert_alpha()

# Load the sounds
egg_sound = pygame.mixer.Sound("egg.ogg")
chicken_sound = pygame.mixer.Sound("catch.ogg")

# Set up the clock
clock = pygame.time.Clock()

# Set up the game variables
all_sprites = pygame.sprite.Group()
eggs = pygame.sprite.Group()
player = Player(WOLF_POSITIONS[0])
all_sprites.add(player)
score = 0
penalty = 0

# Set up the font
font = pygame.font.Font(None, 36)

# Set up the game loop
running = True
while running:

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    # Spawn new eggs
    if random.random() < 0.1:
        egg = Egg((random.randint(0, SCREEN_WIDTH-64), 0))
        all_sprites.add(egg)
        eggs.add(egg)

    # Update all sprites
    all_sprites.update()

    # Check for collisions
    hits = pygame.sprite.spritecollide(player, eggs, True)
    for hit in hits:
        score += 1
        egg_sound.play()
    for egg in eggs:
        if egg.rect.top > SCREEN_HEIGHT:
            penalty += 1
            chicken_sound.play()
            egg.kill()

    # Draw the background
    screen.blit(background_img, (0, 0))

    # Draw the sprites
    all_sprites.draw(screen)

    # Draw the penalty indicators
    for i in range(penalty):
        screen.blit(chicken_img, (SCREEN_WIDTH-64-i*32, 0))

    # Draw the score
    score_text = font.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    pygame.display.flip()

    clock.tick(60)

# Quit Pygame
pygame.quit()
