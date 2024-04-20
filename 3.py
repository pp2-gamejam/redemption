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
        self.speed = 4
        self.current_animation = None
        self.is_attacking = False
        self.attack_frames = 2
        self.attack_animation_speed = FPS // 2
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


class Pc(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))


player = Player()
all_sprites_group = pygame.sprite.Group()
all_sprites_group.add(player)
Pc = Pc(140, 395, "laptop1.png")
all_sprites_group.add(Pc)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(background_image, (0, 0))

    all_sprites_group.draw(screen)  # Отрисовка всех спрайтов, включая игрока
    player.update()
    player.draw(screen)  # Отрисовка игрока
    all_sprites_group.update()

    pygame.display.update()
    clock.tick(FPS)
pygame.quit()
