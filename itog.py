import pygame
from pygame import sprite, transform, image, mixer, font
import random


pygame.init()
font.init()


WIDTH = 700
HEIGHT = 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Космическая Защита")


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)


FPS = 60
clock = pygame.time.Clock()


background = transform.scale(image.load("galaxy.jpg"), (WIDTH, HEIGHT))


mixer.init()
mixer.music.load("space.ogg")
mixer.music.play(-1 )



class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))



class Player(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__(player_image, player_x, player_y, size_x, size_y, player_speed)

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.x < WIDTH - self.rect.width:
            self.rect.x += self.speed



class Enemy(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__(player_image, player_x, player_y, size_x, size_y, player_speed)
        self.speed_y = player_speed

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.top > HEIGHT:
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.rect.y = random.randrange(-200, -50)
            global missed
            missed += 1



player = Player("rocket.png", WIDTH // 2 - 25, HEIGHT - 80, 50, 80, 5)
enemies = sprite.Group()


for _ in range(5):
    enemy = Enemy("ufo.png", random.randrange(0, WIDTH - 50), random.randrange(-200, -50), 50, 40, random.randint(1, 3))
    enemies.add(enemy)


font1 = font.Font(None, 36)


score = 0
missed = 0


running = True
while running:
    clock.tick(FPS)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    player.update()
    enemies.update()


    hits = sprite.spritecollide(player, enemies, False)
    if hits:
        print("Столкновение!")
        running = False


    screen.blit(background, (0, 0))  # Фон
    player.reset()
    player.update()

    enemies.draw(screen)
    enemies.update()


    score_text = font1.render(f"Сбито: {score}", True, WHITE)
    missed_text = font1.render(f"Пропущено: {missed}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(missed_text, (10, 50))


    pygame.display.flip()

pygame.quit()
