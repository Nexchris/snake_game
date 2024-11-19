import pygame
import time
from game import Game
import os

base_dir = os.path.dirname(__file__)
font = os.path.join(base_dir, 'assets', 'font', 'bitfont.TTF')
background = os.path.join(base_dir, 'assets', 'image', 'background.png')
title = os.path.join(base_dir, 'assets', 'image', 'title.png')

countdown_path = os.path.join(base_dir, 'assets', 'audio', 'countdown.mp3')
game_music_path = os.path.join(base_dir, 'assets', 'audio', 'gamemusic.mp3')
coin_path = os.path.join(base_dir, 'assets', 'audio', 'coin.mp3')

galaxy1 = os.path.join(base_dir, 'assets', 'image', 'galaxy1.jpg')
galaxy2 = os.path.join(base_dir, 'assets', 'image', 'galaxy2.jpg')
galaxy3 = os.path.join(base_dir, 'assets', 'image', 'galaxy3.png')
galaxy4 = os.path.join(base_dir, 'assets', 'image', 'galaxy4.jpg')
galaxy5 = os.path.join(base_dir, 'assets', 'image', 'galaxy5.webp')

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()

pygame.mixer.music.load(countdown_path)
apple_sound = pygame.mixer.Sound(coin_path)

background_images = [galaxy1, galaxy2, galaxy3, galaxy4, galaxy5]

def countdown(screen, background, title, font):
    count = 10
    pygame.mixer.music.play()
    while count >= 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False

        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))
        screen.blit(title, (150, -40))

        countdown_text = font.render(f"Start in {count} seconds", True, (0, 0, 0))
        text_rect = countdown_text.get_rect(center=(screen.get_width() // 2, 680))
        screen.blit(countdown_text, text_rect)

        pygame.display.flip()
        time.sleep(1)
        count -= 1

    pygame.mixer.music.stop()
    return True

def game_loop():
    game = Game(screen)
    running = True

    pygame.mixer.music.load(game_music_path)
    pygame.mixer.music.play(-1)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            game.snake.change_direction(0, -1)
        elif keys[pygame.K_DOWN]:
            game.snake.change_direction(0, 1)
        elif keys[pygame.K_LEFT]:
            game.snake.change_direction(-1, 0)
        elif keys[pygame.K_RIGHT]:
            game.snake.change_direction(1, 0)

        game.update_background(background_images)
        game.snake.movement()
        game.handle_apple_collision(apple_sound)
        game.check_collisions()
        game.draw(background_images)

        if game.score >= 20:
            clock.tick(25)
        else:
            clock.tick(20)

        pygame.display.flip()

    pygame.quit()

if countdown(screen, pygame.image.load(background), pygame.image.load(title), pygame.font.Font(font, 32)):
    game_loop()
