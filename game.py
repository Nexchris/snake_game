import pygame
from snake import Snake
from apple import Apple
import os
base_dir = os.path.dirname(__file__)
font = os.path.join(base_dir, 'assets', 'font', 'bitfont.TTF')

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.score = 0
        self.bestscore = 0
        self.current_background = 0
        self.snake = Snake(self)
        self.apple = Apple(self)
        self.big_apple = None

    def reset(self):
        self.score = 0
        self.snake = Snake(self)
        self.apple.comeback()
        self.big_apple = None

    def update_background(self, background_images):
        if self.score % 5 == 0 and self.score != 0:
            self.current_background = (self.score // 5) % len(background_images)

    def check_collisions(self):
        if self.snake.wallCollision() or self.snake.selfCollision():
            print("Game Over")
            if self.score > self.bestscore:
                self.bestscore = self.score
            self.reset()

    def handle_apple_collision(self, apple_sound):
        if self.score < 20:
            if self.big_apple is None:
                if self.snake.snakeHead().colliderect(pygame.Rect(self.apple.position.x, self.apple.position.y, self.apple.size, self.apple.size)):
                    pygame.mixer.Sound.play(apple_sound)
                    self.score += 5
                    self.apple.comeback() 
        else:
            if self.big_apple is None:
                self.big_apple = Apple(self, size=80)
            if self.snake.snakeHead().colliderect(pygame.Rect(self.big_apple.position.x, self.big_apple.position.y, self.big_apple.size, self.big_apple.size)):
                pygame.mixer.Sound.play(apple_sound)
                self.score += 10
                self.big_apple = None

    def draw(self, background_images):
        image = pygame.image.load(background_images[self.current_background])
        self.screen.blit(image, (0, 0))

        self.snake.draw(self.screen)
        
        if self.big_apple is None:
            self.apple.draw(self.screen)
        
        if self.big_apple is not None:
            self.big_apple.draw(self.screen)

        custom_font = pygame.font.Font(font, 48)
        score_text = custom_font.render(f"Score: {self.score}", True, (255, 255, 255))
        bestscore_text = custom_font.render(f"Best Score: {self.bestscore}", True, (255, 255, 255))
        self.screen.blit(score_text, (80, 10))
        self.screen.blit(bestscore_text, (550, 10))
