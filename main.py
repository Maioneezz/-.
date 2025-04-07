import pygame
import random

pygame.init()

window = pygame.display.set_mode((700, 500))
pygame.display.set_caption("Космический Шутер")

pygame.mixer.music.load('space.ogg')
pygame.mixer.music.play(-1)

background = pygame.transform.scale(pygame.image.load('galaxy.jpg'), (700, 500))

clock = pygame.time.Clock()
FPS = 60

class GameSprite(pygame.sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(player_image), (65, 65))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.x < 635:
            self.rect.x += self.speed

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global missed
        if self.rect.y > 500:
            self.rect.y = 0
            self.rect.x = random.randint(0, 635)
            missed += 1

class Bullet(GameSprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__(player_image, player_x, player_y, player_speed)
        self.image = pygame.transform.scale(pygame.image.load(player_image), (22, 22))

    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

# Создание игрока
player = Player('rocket.png', 320, 400, 10)

# Создание группы врагов
enemies = pygame.sprite.Group()
for i in range(5):
    enemy = Enemy('ufo.png', random.randint(0, 635), -60, random.randint(1, 5))
    enemies.add(enemy)

# Создание группы пуль
bullets = pygame.sprite.Group()

# Звук выстрела
fire_sound = pygame.mixer.Sound('fire.ogg')

# Шрифт для статистики
pygame.font.init()
font1 = pygame.font.Font(None, 36)

# Счётчики
missed = 0
score = 0

# Игровой цикл
game = True
while game:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            game = False
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_SPACE:
                bullet = Bullet('bullet.png', player.rect.centerx, player.rect.top, 15)
                bullets.add(bullet)
                fire_sound.play()

    window.blit(background, (0, 0))
    player.update()
    player.reset()

    enemies.update()
    enemies.draw(window)

    bullets.update()
    bullets.draw(window)

    # Проверка столкновений пуль с врагами
    collisions = pygame.sprite.groupcollide(enemies, bullets, True, True)
    for collision in collisions:
        score += 1
        enemy = Enemy('ufo.png', random.randint(0, 635), -60, random.randint(1, 5))
        enemies.add(enemy)

    # Проверка условий победы и проигрыша
    if missed >= 3:
        game = False
        print("Вы проиграли!")
    if score >= 25:
        game = False
        print("Вы выиграли!")

    # Отображение статистики
    text_missed = font1.render("Пропущено: " + str(missed), 1, (255, 255, 255))
    text_score = font1.render("Сбито: " + str(score), 1, (255, 255, 255))
    window.blit(text_missed, (10, 10))
    window.blit(text_score, (10, 50))

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()