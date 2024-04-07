import pygame
import sys
import random

# Инициализация Pygame
pygame.init()

# Размеры экрана
WIDTH, HEIGHT = 500, 500
win = pygame.display.set_mode((WIDTH, HEIGHT))

# Цвет надписи
WHITE = (255, 255, 255)
yellow = (255,255,0)

# Загрузка заднего фона
background_img = pygame.image.load("1 (2).png")
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

# Загрузка музыки
pygame.mixer.music.load("akim-apachev-leto-i-arbalety-mp3.mp3")
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1)  # Зацикливание музыки

# Загрузка звука крыльев
flap_sound = pygame.mixer.Sound("flap.wav")
flap_sound.set_volume(0.05)  # Установка громкости звука крыльев

# Загрузка изображения птицы
bird_img = pygame.image.load("1(3).png")
bird_rect = bird_img.get_rect()
bird_x = WIDTH // 3
bird_y = HEIGHT // 2
bird_dy = 0

# Параметры труб
pipe_img = pygame.image.load("pipe1.png")
pipe_x = WIDTH
pipe_y = 0
pipe_gap = 155
pipe_speed = 9
pipe_width = pipe_img.get_width()
pipe_height = pipe_img.get_height()

# Гравитация
gravity = 1

# Счет
score = 0
font = pygame.font.Font(None, 36)

# Функция отрисовки
def draw():
    win.blit(background_img, (0, 0))
    win.blit(bird_img, (bird_x, bird_y))
    win.blit(pipe_img, (pipe_x, pipe_y))
    win.blit(pipe_img, (pipe_x, pipe_y + pipe_height + pipe_gap))
    score_text = font.render("Score: " + str(score), True, WHITE)
    win.blit(score_text, (10, 10))
    pygame.display.update()

# Основной игровой цикл
paused = False
game_over = False
closing = False  #переменная для отслеживания закрытия окна
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            closing = True  # Флаг закрытия окна
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_dy = -8
                flap_sound.play()  # Воспроизведение звука крыльев
            elif event.key == pygame.K_ESCAPE:
                paused = not paused
                if paused:
                    pygame.mixer.music.pause()  # Пауза музыки
                else:
                    pygame.mixer.music.unpause()  # Продолжение музыки

    if not paused and not game_over:
        bird_dy += gravity
        bird_y += bird_dy

        pipe_x -= pipe_speed
        if pipe_x <= -pipe_width:
            pipe_x = WIDTH
            pipe_y = random.randint(-pipe_height // 2, 0)
            score += 1

        if bird_y <= 0 or bird_y >= HEIGHT - bird_rect.height:
            game_over = True

        bird_rect.topleft = (bird_x, bird_y)
        pipe_rect1 = pygame.Rect(pipe_x, pipe_y, pipe_width, pipe_height)
        pipe_rect2 = pygame.Rect(pipe_x, pipe_y + pipe_height + pipe_gap, pipe_width, pipe_height)
        if bird_rect.colliderect(pipe_rect1) or bird_rect.colliderect(pipe_rect2):
            game_over = True
        if score == 11:
            score_text = font.render("ТЫ ВЫЙГРАЛ!", True, yellow)
            win.blit(score_text, (150, 200))
            pygame.mixer.music.stop()
            pygame.display.update()
            pygame.time.delay(2000)  # Задержка перед выходом из игры
            pygame.quit()
            sys.exit()

        draw()

    if game_over:
        score_text = font.render("ты проиграл, попробуй еще!", True, WHITE)
        win.blit(score_text, (150, 200))
        pygame.mixer.music.stop()
        pygame.display.update()
        pygame.time.delay(2000)  # Задержка перед выходом из игры
        pygame.quit()
        sys.exit()

    clock.tick(30)