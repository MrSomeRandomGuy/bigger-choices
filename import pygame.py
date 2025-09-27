# sacrifices must be made

import pygame
pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 432

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Sacrifices must be made')

# Variables 
clock = pygame.time.Clock()
FPS = 60
bg_images = []
scroll = 0

# Images

# Background
for i in range(1, 12):
    bg_image = pygame.image.load(f'test_game_images/background layers/layer-{i}.png').convert_alpha()
    bg_image = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    bg_images.append(bg_image)

bg_width = bg_images[0].get_width()

def draw_bg():
    for x in range(5):
        speed = 0.2
        for i in bg_images:
            screen.blit(i, ((x * bg_width) - scroll * speed, 0))
            speed += 0.2

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.alive = True
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        
        # Idle animation
        temp_list = []
        for i in range(4):
            img = pygame.image.load(f'test_game_images/player_idle/idle{i}.png').convert_alpha()
            img = pygame.transform.scale(img, (325, 325))
            temp_list.append(img)
        self.animation_list.append(temp_list)

        # Run animation
        temp_list = []
        for i in range(8):
            img = pygame.image.load(f'test_game_images/player_run/run{i}.png').convert_alpha()
            img = pygame.transform.scale(img, (325, 325))
            temp_list.append(img)
        self.animation_list.append(temp_list)

        # Jump animation
        temp_list = []
        for i in range(2):
            img = pygame.image.load(f'test_game_images/player_jump/jump{i}.png').convert_alpha()
            img = pygame.transform.scale(img, (325, 325))
            temp_list.append(img)
        self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = pygame.Rect(0, 0, 50, 95)
        self.rect.x = x
        self.rect.y = y
        self.speed = 5
        self.vel_y = 0
        self.gravity = 1
        self.on_ground = True
        self.flip = False

    def move(self):
        global scroll
        key = pygame.key.get_pressed()

        # Movement
        if key[pygame.K_d]:
            self.rect.x += self.speed
            scroll += self.speed
            self.flip = False
        if key[pygame.K_a]:
            self.rect.x -= self.speed
            scroll -= self.speed
            self.flip = True
            if scroll < 0:
                scroll = 0
        if key[pygame.K_SPACE] and self.on_ground:
            self.vel_y = -20
            self.on_ground = False
        
        # Gravity
        self.vel_y += self.gravity
        self.rect.y += self.vel_y

        # Screen borders
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.on_ground = True
            self.vel_y = 0

        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def update_animation(self):
        ANIMATION_COOLDOWN = 100
        self.image = self.animation_list[self.action][self.frame_index]

        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
            if self.frame_index >= len(self.animation_list[self.action]):
                self.frame_index = 0

    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), (self.rect.x - 150, self.rect.y - 120))
        pygame.draw.rect(screen, (255, 0, 0), self.rect, 2 )



class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y ):
        pygame.sprite.Sprite.__init__(self)
        super().__init__(self)
        


# Create player
player = Player(100, 100)

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        super().__init__(self)
        self.re



# Game loop
run = True
while run:
    clock.tick(FPS)
    draw_bg()
    player.move()

    # Update animation based on action
    if player.alive:
        if not player.on_ground:
            player.update_action(2)  # jump
        elif pygame.key.get_pressed()[pygame.K_a] or pygame.key.get_pressed()[pygame.K_d]:
            player.update_action(1)  # run
        else:
            player.update_action(0)  # idle

    player.update_animation()
    player.draw()

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

pygame.quit()
