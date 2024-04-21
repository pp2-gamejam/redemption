import pygame
from pygame.locals import *
import sys
import time

pygame.init()

# Определение констант
WIDTH = 1280
HEIGHT = 720
FPS = 60

# Определение цветов
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Revenge")
clock = pygame.time.Clock()

# Загрузка изображений
background_image = pygame.transform.scale(pygame.image.load("background.png").convert(), (WIDTH, HEIGHT))

# Класс для невидимых объектов (преград)
class Barrier(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)

# Создание невидимых объектов (преград)
barrier1 = Barrier(620, 200, 25, 150) # Столб вверхний
barrier2 = Barrier(620, 520, 25, 200) # Столб нижний
barrier3 = Barrier(420, 580, 180, 50) # люк
barrier4 = Barrier(0, 520, 120, 200) # стол
barrier5 = Barrier(1265, 260, 1, 400) # правая гр
barrier6 = Barrier(0, 0, 180, 310) # кровать
barrier7 = Barrier(0, 0, 1280, 190) # вверхння гр
barrier8 = Barrier(0, 700, 1280, 1) # нижняя гр
barrier9 = Barrier(0, 0, 1, 660) # левая гр
barrier10 = Barrier(0, 311, 160, 100) # Pc
barrier11 = Barrier(1152, 425, 128, 148) # ящики
barrier12 = Barrier(1128, 567, 152, 149) # бочки
barrier13 = Barrier(900, 410, 148, 13) # нижние стулья
barrier14 = Barrier(880, 290, 180, 50) # stol
barrier15 = Barrier(820, 321, 39, 13) # levie styl
barrier16 = Barrier(1100, 325, 39, 13) # pravie stul

# Группировка всех невидимых объектов в одну группу
barriers_group = pygame.sprite.Group(barrier1, barrier2, barrier3, barrier4, barrier5, barrier6, barrier7, barrier8, barrier9, barrier10, barrier11, barrier12, barrier13, barrier14, barrier15, barrier16)

barriers = list(barriers_group.sprites())

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.pos = pygame.math.Vector2(860,650)
        self.speed = 3
        self.hp = 100  # Health points
        self.attack_power = 10
        self.attack_radius = 100  # Set the attack radius for the player  # Attack power
        self.attack_cooldown = 1000  # Attack cooldown in milliseconds
        self.last_attack_time = pygame.time.get_ticks()  # Last attack time
        self.current_animation = None 
        self.is_attacking = False
        self.attack_frames = 2
        self.attack_animation_speed = FPS // 7 #скорость анимации удара
        self.attack_counter = 0
        self.walk_counter = 0
        self.walk_index = 0
        self.image_index = 0
        self.walk_animation_speed = FPS // 20  # Скорость анимации ходьбы
        self.images = {
            "walk_left": [pygame.image.load("walk_left1.png").convert_alpha(), pygame.image.load("walk_left2.png").convert_alpha(),
                          pygame.image.load("walk_left3.png").convert_alpha(), pygame.image.load("walk_left4.png").convert_alpha()],
            "walk_right": [pygame.image.load("walk_right1.png").convert_alpha(), pygame.image.load("walk_right2.png").convert_alpha(),
                           pygame.image.load("walk_right3.png").convert_alpha(), pygame.image.load("walk_right4.png").convert_alpha()],
            "walk_up": [pygame.image.load("walk_up1.png").convert_alpha(), pygame.image.load("walk_up2.png").convert_alpha(),
                        pygame.image.load("walk_up3.png").convert_alpha(), pygame.image.load("walk_up4.png").convert_alpha()],
            "walk_down": [pygame.image.load("walk_down1.png").convert_alpha(), pygame.image.load("walk_down2.png").convert_alpha(),
                          pygame.image.load("walk_down3.png").convert_alpha(), pygame.image.load("walk_down4.png").convert_alpha()],
            "attack_left": [pygame.image.load("hit_left1.png").convert_alpha(), pygame.image.load("hit_left2.png").convert_alpha()],
            "attack_right": [pygame.image.load("hit_right1.png").convert_alpha(), pygame.image.load("hit_right2.png").convert_alpha()],
            "attack_up": [pygame.image.load("hit_up1.png").convert_alpha(), pygame.image.load("hit_up2.png").convert_alpha()],
            "attack_down": [pygame.image.load("hit_down1.png").convert_alpha(), pygame.image.load("hit_down2.png").convert_alpha()],
        }

        self.direction = "down"  # Начальное направление вниз
        self.current_animation = self.images["walk_down"]
        self.walk_frame_duration = self.walk_animation_speed // len(self.current_animation)
        self.is_walking = False  # Флаг для определения, идет ли анимация ходьбы

    def update(self):
        keys = pygame.key.get_pressed()
        if not self.is_attacking:
            if keys[K_LEFT]:
                self.pos.x -= self.speed
                if pygame.sprite.spritecollideany(self, barriers):  # Check collision after moving
                    self.pos.x += self.speed  # Move back if there's a collision
                self.current_animation = self.images["walk_left"]
                self.direction = "left"
                self.is_walking = True
            elif keys[K_RIGHT]:
                self.pos.x += self.speed
                if pygame.sprite.spritecollideany(self, barriers):
                    self.pos.x -= self.speed
                self.current_animation = self.images["walk_right"]
                self.direction = "right"
                self.is_walking = True
            elif keys[K_UP]:
                self.pos.y -= self.speed
                if pygame.sprite.spritecollideany(self, barriers):
                    self.pos.y += self.speed
                self.current_animation = self.images["walk_up"]
                self.direction = "up"
                self.is_walking = True
            elif keys[K_DOWN]:
                self.pos.y += self.speed
                if pygame.sprite.spritecollideany(self, barriers):
                    self.pos.y -= self.speed
                self.current_animation = self.images["walk_down"]
                self.direction = "down"
                self.is_walking = True
            else:
                self.is_walking = False

        if keys[K_SPACE]:
            if pygame.sprite.spritecollideany(self, all_sprites_group, pygame.sprite.collide_circle):
             for sprite in pygame.sprite.spritecollide(self, all_sprites_group, False, pygame.sprite.collide_circle):
                if isinstance(sprite, Enemy):
                    if self.rect.distance_to(sprite.rect) <= self.attack_radius:
                        self.attack(sprite)

        self.animate()

    def animate(self):
        if self.is_attacking:
            # Анимация для атаки
            self.attack_counter += 1
            if self.attack_counter >= self.attack_animation_speed:
                self.attack_counter = 0
                self.image_index += 1
                if self.image_index >= self.attack_frames:
                    self.is_attacking = False
                    self.image_index = 0  # Сброс индекса для следующей атаки
        else:
            # Анимация для ходьбы
            if self.is_walking:
                self.image_index += 1
                if self.image_index >= len(self.current_animation):
                    self.image_index = 0
                pygame.time.wait(self.walk_frame_duration)  # Задержка для управления скоростью анимации
            else:
                self.image_index = 0

            # Переключение анимаций в зависимости от направления движения
            if self.direction == "left":
                self.current_animation = self.images["walk_left"]
            elif self.direction == "right":
                self.current_animation = self.images["walk_right"]
            elif self.direction == "up":
                self.current_animation = self.images["walk_up"]
            elif self.direction == "down":
                self.current_animation = self.images["walk_down"]

    def attack(self):
        self.is_attacking = True
        if self.direction == "left":
            self.current_animation = self.images["attack_left"]
        elif self.direction == "right":
            self.current_animation = self.images["attack_right"]
        elif self.direction == "up":
            self.current_animation = self.images["attack_up"]
        elif self.direction == "down":
            self.current_animation = self.images["attack_down"]
        self.image_index = 0  # Начать анимацию атаки сначала

    @property
    def image(self):
        if self.current_animation and 0 <= self.image_index < len(self.current_animation):
            return self.current_animation[self.image_index]
        else:
            return None

    @property
    def rect(self):
        return self.current_animation[self.walk_index].get_rect(center=self.pos)
        if self.image:
            return self.image.get_rect(center=self.pos)
        else:
            return None

    def draw(self, surface):
        surface.blit(self.current_animation[self.walk_index], self.rect)
        if self.image:
            surface.blit(self.image, self.rect)

    def check_collision_with_object(self, object):
        if self.rect.colliderect(object.rect):
            return True
        else:
            return False

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path, target_sprites):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha() 
        self.image = pygame.transform.rotozoom(self.image, 0, 3)
        self.rect = self.image.get_rect(center=(x, y))  # Position the enemy at the given coordinates
        self.attack_radius = 100  # Set the attack radius for the enemy
        self.speed = 2 
        self.hp = 100  # Health points
        self.attack_power = 10  # Attack power
        self.attack_cooldown = 1500  # Attack cooldown in milliseconds
        self.last_attack_time = pygame.time.get_ticks()
        self.last_attack_time = pygame.time.get_ticks()  # Last attack time
        self.target_sprites = target_sprites  # The sprites that the enemy will target

    def update(self):
       # Convert self.rect.center to a Vector2 for distance calculations
        self_position = pygame.math.Vector2(self.rect.centerx, self.rect.centery)

        # Find the nearest target based on the center position, not the rect
        nearest_target, nearest_distance = None, float('inf')
        for target in self.target_sprites:
            target_position = pygame.math.Vector2(target.rect.centerx, target.rect.centery)
            distance = self_position.distance_to(target_position)
            if distance < nearest_distance:
                nearest_target, nearest_distance = target, distance

        if nearest_target is not None:
            # Move towards the nearest target
            direction_vector = pygame.math.Vector2(nearest_target.rect.center) - self_position
            if direction_vector.length() > 0:  # Avoid division by zero
                direction_vector = direction_vector.normalize()

            # Calculate potential new position
            new_x = self.rect.x + direction_vector.x * self.speed
            new_y = self.rect.y + direction_vector.y * self.speed

            # Move horizontally
            self.rect.x = new_x
            # Check for horizontal collisions
            if pygame.sprite.spritecollideany(self, barriers_group):
                self.rect.x -= direction_vector.x * self.speed  # Move back if there's a collision
            
            # Move vertically
            self.rect.y = new_y
            # Check for vertical collisions
            if pygame.sprite.spritecollideany(self, barriers_group):
                self.rect.y -= direction_vector.y * self.speed  # Move back if there's a collision   
            if pygame.sprite.spritecollideany(self, all_sprites_group, pygame.sprite.collide_circle):
             for sprite in pygame.sprite.spritecollide(self, all_sprites_group, False, pygame.sprite.collide_circle):
                if isinstance(sprite, Player):
                    distance = ((self.rect.centerx - sprite.rect.centerx) ** 2 + (self.rect.centery - sprite.rect.centery) ** 2) ** 0.5
                    if distance <= self.attack_radius:
                        self.attack(sprite) 
            # Check for attack cooldown and perform attack
            current_time = pygame.time.get_ticks()
            if current_time - self.last_attack_time >= self.attack_cooldown:
                self.attack(nearest_target)
                self.last_attack_time = current_time

    def attack(self, target):
        target.hp -= self.attack_power
        print("Enemy attacks!")
        print("Player's HP:", target.hp)

class Pc(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))
        self.hp = 100  # Health points

player = Player()
all_sprites_group = pygame.sprite.Group()
all_sprites_group.add(player)
Pc = Pc(140, 395, "laptop1.png")
target_sprites = [player, Pc]
all_sprites_group.add(Pc)
enemy_image_path = "zomzon1.1.png"  
enemy_spawn_x = 600  #
enemy_spawn_y = 600  # 
enemy = Enemy(enemy_spawn_x, enemy_spawn_y, enemy_image_path, target_sprites)

all_sprites_group.add(enemy)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.blit(background_image, (0, 0))

    all_sprites_group.draw(screen)  # Отрисовка всех спрайтов, включая игрока
    player.update()
    enemy.update()
    player.draw(screen)  # Отрисовка игрока
    all_sprites_group.update()

    if pygame.sprite.spritecollide(player, all_sprites_group, False):
        for sprite in pygame.sprite.spritecollide(player, all_sprites_group, False):
            if isinstance(sprite, Enemy):
                player.hp -= sprite.attack_power
                sprite.attack(player)
                if player.hp <= 0  :
                    player.kill()

    # Check for interactions between enemy and PC
    if pygame.sprite.spritecollide(Pc, all_sprites_group, False):
        for sprite in pygame.sprite.spritecollide(Pc, all_sprites_group, False):
            if isinstance(sprite, Enemy):
                Pc.hp -= sprite.attack_power
                sprite.attack(Pc)
                if Pc.hp <= 0:
                    Pc.kill()

    # Check for player and enemy deaths
    if not player.alive():
        # Player is dead
        print("Player has died!")
        running = False  # End the game loop

    if not enemy.alive():
        # Enemy is dead
        print("Enemy has died!")
        running = False  # End the game loop

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
