import pygame
import random

class Apple:
    def __init__(self, game, size=40):
        self.size = size
        self.game = game
        self.position = self.applePosition()

    def applePosition(self):
        margin = 300
        x = random.randint(margin // 40, (self.game.screen.get_width() - margin) // 40) * 40
        y = random.randint(margin // 40, (self.game.screen.get_height() - margin) // 40) * 40
        return pygame.Vector2(x, y)

    def draw(self, screen, color="red"):
        pygame.draw.rect(screen, color, [self.position.x, self.position.y, self.size, self.size])

    def comeback(self):
        self.position = self.applePosition()
