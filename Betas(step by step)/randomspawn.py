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
        self.current_animation = None 
        self.attack_rect = None
        self.is_attacking = False
        self.attack_cooldown = 500  # Cooldown in milliseconds
        self.last_attack_time = 0
        self.attack_frames = 2
        self.health = 100
        self.max_health = 100
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
    
    def update_attack_rect(self):
        offset = 50
        size = (40, 40)  # Size of the attack rectangle
        if self.direction == "left":
            self.attack_rect = pygame.Rect(self.pos.x - offset - size[0], self.pos.y, *size)
        elif self.direction == "right":
            self.attack_rect = pygame.Rect(self.pos.x + offset, self.pos.y, *size)
        elif self.direction == "up":
            self.attack_rect = pygame.Rect(self.pos.x, self.pos.y - offset - size[1], *size)
        elif self.direction == "down":
            self.attack_rect = pygame.Rect(self.pos.x, self.pos.y + offset, *size)
        
        pygame.time.set_timer(pygame.USEREVENT + 1, 100)
        
    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.die()
    
    def die(self):
        # Handle player death (game over, respawn, etc.)
        print("Player has died!")
    
    def draw_health_bar(self, surface):
        # Similar to the Enemy's draw_health_bar method
        bar_length = 100
        bar_height = 10
        health_bar_x = self.rect.x + (self.rect.width / 2) - (bar_length / 2)
        health_bar_y = self.rect.y - bar_height - 20
        health_ratio = self.health / self.max_health
        health_bar_length = bar_length * health_ratio
        pygame.draw.rect(surface, (255, 0, 0), (health_bar_x, health_bar_y, bar_length, bar_height))
        pygame.draw.rect(surface, (0, 255, 0), (health_bar_x, health_bar_y, health_bar_length, bar_height))

    def update(self):
        current_time = pygame.time.get_ticks()
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
            if keys[K_SPACE] and current_time - self.last_attack_time >= self.attack_cooldown:
                self.attack()
                self.last_attack_time = current_time
            # Проверяем, что персонаж атакует и находится рядом с объектом
            if self.is_attacking and self.rect.colliderect(Pc.rect):
                # Здесь меняем фотографию объекта на вторую
                Pc.image = pygame.image.load("laptop2.png").convert_alpha()

            self.attack()

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
        self.update_attack_rect()
        if self.attack_rect:
            # Check for collisions with enemy
                if self.attack_rect.colliderect(enemy.rect):
                    enemy.take_damage(1)  # Apply damage
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
    def __init__(self, x, y, image_path, target_sprites, barriers):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, 3)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 2
        self.target_sprites = target_sprites
        self.barriers = barriers
        self.health = 100  # Enemy health
        self.max_health = 100  # Max health for full health bar
        self.attack_cooldown = 1000  # Cooldown in milliseconds
        self.last_attack_time = pygame.time.get_ticks()  # Time when the last attack was made
        self.knockback_distance = 5  # Distance to move the enemy back when hit
    
    def update(self):
        current_time = pygame.time.get_ticks()
        self.move_towards_targets(current_time)

    def move_towards_targets(self, current_time):
        self_position = pygame.math.Vector2(self.rect.centerx, self.rect.centery)
        nearest_target, nearest_distance = None, float('inf')
        for target in self.target_sprites:
            target_position = pygame.math.Vector2(target.rect.centerx, target.rect.centery)
            distance = self_position.distance_to(target_position)
            if distance < nearest_distance:
                nearest_target, nearest_distance = target, distance

        if nearest_target is not None:
            direction_vector = pygame.math.Vector2(nearest_target.rect.center) - self_position
            if direction_vector.length() > 0:
                direction_vector = direction_vector.normalize()

            # Move the enemy towards the target and check for collisions
            original_position = self.rect.copy()  # Store the original position
            self.rect.x += direction_vector.x * self.speed
            if pygame.sprite.spritecollideany(self, self.barriers):
                self.rect.x = original_position.x  # Revert to original position if collision occurs

            self.rect.y += direction_vector.y * self.speed
            if pygame.sprite.spritecollideany(self, self.barriers):
                self.rect.y = original_position.y  # Revert to original position if collision occurs
        self.attack(current_time)
        

    def draw_health_bar(self, surface):
        # Health bar position and size
        bar_length = 50
        bar_height = 5
        health_bar_x = self.rect.x + (self.rect.width / 2) - (bar_length / 2)
        health_bar_y = self.rect.y - bar_height - 10  # 10 pixels above the enemy

        # Calculate health ratio
        health_ratio = self.health / self.max_health
        health_bar_length = bar_length * health_ratio

        # Draw the background (empty part) of the health bar
        pygame.draw.rect(surface, (255, 0, 0), (health_bar_x, health_bar_y, bar_length, bar_height))
        # Draw the health (filled part) of the health bar
        pygame.draw.rect(surface, (0, 255, 0), (health_bar_x, health_bar_y, health_bar_length, bar_height))
    

    def take_damage(self, damage):
        print(f"Enemy taking {damage} damage.")
        self.health -= damage
        print(f"Enemy remaining health: {self.health}")
        if self.health <= 0:
            self.kill()  # Remove enemy if dead
        else:
            self.knockback()
    
    def attack(self, current_time):
         for target in self.target_sprites:
            if self.rect.colliderect(target.rect):
                if current_time - self.last_attack_time > self.attack_cooldown:
                    target.take_damage(5)
                    self.last_attack_time = current_time
    
    def knockback(self):
        original_position = self.rect.copy()
        # Simple knockback mechanic
        if player.direction == "left":
            self.rect.x -= self.knockback_distance
        elif player.direction == "right":
            self.rect.x += self.knockback_distance
        elif player.direction == "up":
            self.rect.y -= self.knockback_distance
        elif player.direction == "down":
            self.rect.y += self.knockback_distance
        # Ensure the enemy doesn't move outside the play area or into barriers
        if pygame.sprite.spritecollideany(self, self.barriers):
            self.rect = original_position

class Pc(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))
        self.health = 50
        self.max_health = 50
    
    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.destroy()
    
    def destroy(self):
        # Handle Pc destruction
        print("Pc has been destroyed!")
    
    def draw_health_bar(self, surface):
        bar_length = 100
        bar_height = 10
        health_bar_x = self.rect.x + (self.rect.width / 2) - (bar_length / 2)
        health_bar_y = self.rect.y - bar_height - 20
        health_ratio = self.health / self.max_health
        health_bar_length = bar_length * health_ratio
        pygame.draw.rect(surface, (255, 0, 0), (health_bar_x, health_bar_y, bar_length, bar_height))
        pygame.draw.rect(surface, (0, 255, 0), (health_bar_x, health_bar_y, health_bar_length, bar_height))

        pass

player = Player()
all_sprites_group = pygame.sprite.Group()
all_sprites_group.add(player)
Pc = Pc(140, 395, "laptop1.png")
target_sprites = [player, Pc]
all_sprites_group.add(Pc)
enemy_image_path = "zomzon1.1.png"  
enemy_spawn_x = 600  # Replace with the x-coordinate where you want to spawn the enemy
enemy_spawn_y = 400  # Replace with the y-coordinate where you want to spawn the enemy
enemy = Enemy(enemy_spawn_x, enemy_spawn_y, enemy_image_path, target_sprites, barriers_group)

all_sprites_group.add(enemy)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.USEREVENT + 1:  # Custom event for clearing attack rect
            player.attack_rect = None

    screen.blit(background_image, (0, 0))

    if player.attack_rect:
        pygame.draw.rect(screen, (255, 0, 0), player.attack_rect)  # Draw attack rectangle in red


    all_sprites_group.draw(screen)  # Отрисовка всех спрайтов, включая игрока
    player.update()
    player.draw(screen)  # Отрисовка игрока
    player.draw_health_bar(screen)
    Pc.draw_health_bar(screen)
    if enemy.alive():
            enemy.draw_health_bar(screen)
    all_sprites_group.update()

    pygame.display.update()
    clock.tick(FPS)
pygame.quit()
