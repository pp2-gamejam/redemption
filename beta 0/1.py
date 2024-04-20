import pygame
from sys import exit
import math

pygame.init()

# Game setup
WIDTH = 1280
HEIGHT = 720
FPS = 60

# Player settings
PLAYER_START_X = 400
PLAYER_START_Y = 500
PLAYER_SPEED = 4
GUN_OFFSET_X = 45
GUN_OFFSET_Y = 20

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Revenge")
clock = pygame.time.Clock()


# Loads images
background = pygame.transform.scale(pygame.image.load("background.png").convert(), (WIDTH, HEIGHT))

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.pos = pygame.math.Vector2(PLAYER_START_X, PLAYER_START_Y)
        self.base_player_image = pygame.image.load("walk_down1.png").convert_alpha()
        self.image = self.base_player_image
        self.hitbox_rect = self.base_player_image.get_rect(center = self.pos)
        self.rect = self.hitbox_rect.copy()
        self.angle = 0
        self.speed = PLAYER_SPEED
        self.hit_counter = 0
        self.animation_speed = FPS // 8
        self.frame_counter = 0
        self.current_frame_index = 0
        
        self.walk_left_animation = [
            pygame.image.load("walk_left1.png").convert_alpha(),
            pygame.image.load("walk_left2.png").convert_alpha(),
            pygame.image.load("walk_left3.png").convert_alpha(),
            pygame.image.load("walk_left4.png").convert_alpha(),
            ]
        self.walk_right_animation = [
            pygame.image.load("walk_right1.png").convert_alpha(),
            pygame.image.load("walk_right2.png").convert_alpha(),
            pygame.image.load("walk_right3.png").convert_alpha(),
            pygame.image.load("walk_right4.png").convert_alpha(),
        ]
        self.walk_up_animation = [
            pygame.image.load("walk_up1.png").convert_alpha(),
            pygame.image.load("walk_up2.png").convert_alpha(),
            pygame.image.load("walk_up3.png").convert_alpha(),
            pygame.image.load("walk_up4.png").convert_alpha(),
        ]
        self.walk_down_animation = [
            pygame.image.load("walk_down1.png").convert_alpha(),
            pygame.image.load("walk_down2.png").convert_alpha(),
            pygame.image.load("walk_down3.png").convert_alpha(),
            pygame.image.load("walk_down4.png").convert_alpha(),
        ]

        self.current_animation = None
        self.current_frame_index = 0
        self.is_walking = False

        self.animation_speed = FPS // 8
        self.animation_counter = 0

        self.hit_left_animation = [
            pygame.image.load("hit_left1.png").convert_alpha(),
            pygame.image.load("hit_left2.png").convert_alpha(),
        ]
        self.hit_right_animation = [
            pygame.image.load("hit_right1.png").convert_alpha(),
            pygame.image.load("hit_right2.png").convert_alpha(),
        ]
        self.hit_up_animation = [
            pygame.image.load("hit_up1.png").convert_alpha(),
            pygame.image.load("hit_up2.png").convert_alpha(),
        ]
        self.hit_down_animation = [
            pygame.image.load("hit_down1.png").convert_alpha(),
            pygame.image.load("hit_down2.png").convert_alpha(),
        ]

        self.is_hitting = False
        self.hit_animation_speed = FPS // 5
        self.hit_counter = 0
        self.hit_frame_index = 0

    def check_collision(self, sprite):
        return self.rect.colliderect(sprite.rect)


    def update(self):
        self.user_input()
        self.move()
        if self.is_walking and self.frame_counter % self.animation_speed == 0:
            self.current_frame_index += 1
            if self.current_frame_index >= len(self.current_animation):
                self.current_frame_index = 0
            self.image = self.current_animation[self.current_frame_index]

        self.frame_counter += 1
        if self.frame_counter >= self.animation_speed:
            self.frame_counter = 0

        if self.is_hitting:
            if self.hit_counter % self.hit_animation_speed == 0:
                self.hit_frame_index += 1
                if self.hit_frame_index >= 2:  # Два кадра удара
                    self.hit_frame_index = 0
                    self.is_hitting = False  # Завершаем удар
                    self.current_animation = self.walk_down_animation  # Возвращаемся к обычной анимации
                else:
                    if self.current_animation == self.walk_left_animation:
                        self.image = self.hit_left_animation[self.hit_frame_index]
                    elif self.current_animation == self.walk_right_animation:
                        self.image = self.hit_right_animation[self.hit_frame_index]
                    elif self.current_animation == self.walk_up_animation:
                        self.image = self.hit_up_animation[self.hit_frame_index]
                    elif self.current_animation == self.walk_down_animation:
                        self.image = self.hit_down_animation[self.hit_frame_index]

            self.hit_counter += 1
            if self.hit_frame_index == 0:  # Проверяем, когда анимация удара возвращается к начальному кадру
                self.is_hitting = False  # Завершаем удар
                self.current_animation = self.walk_down_animation

    def user_input(self):
        self.velocity_x = 0
        self.velocity_y = 0

        keys = pygame.key.get_pressed()

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.velocity_y = -self.speed
            self.current_animation = self.walk_up_animation
            self.is_walking = True
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.velocity_y = self.speed
            self.current_animation = self.walk_down_animation
            self.is_walking = True
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.velocity_x = self.speed
            self.current_animation = self.walk_right_animation
            self.is_walking = True
        elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.velocity_x = -self.speed
            self.current_animation = self.walk_left_animation
            self.is_walking = True
        else:
            self.is_walking = False

        if keys[pygame.K_SPACE]:
            self.hit()

    def hit(self):
        if not self.is_hitting:
            self.is_hitting = True
            self.hit_frame_index = 0

    def move(self):
        self.pos += pygame.math.Vector2(self.velocity_x, self.velocity_y)
        self.hitbox_rect.center = self.pos
        self.rect.center = self.hitbox_rect.center

player = Player()

all_sprites_group = pygame.sprite.Group()

all_sprites_group.add(player)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(background, (0, 0))

    all_sprites_group.draw(screen)
    all_sprites_group.update()

    pygame.display.update()
    clock.tick(FPS)
pygame.quit()