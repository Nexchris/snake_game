import pygame

class Snake:
    def __init__(self, game):
        self.size = 40
        self.body = [(game.screen.get_width() // 2, game.screen.get_height() // 2)]
        self.direction = (0, 0)
        self.started = False
        self.game = game

    def movement(self):
        if self.direction != (0, 0):
            head_x, head_y = self.body[0]
            head_x += self.direction[0] * self.size
            head_y += self.direction[1] * self.size
            self.body.insert(0, (head_x, head_y))
            if len(self.body) > self.game.score + 1:
                self.body.pop()

    def change_direction(self, dx, dy):
        if (dx, dy) != (-self.direction[0], -self.direction[1]):
            self.direction = (dx, dy)
            self.started = True

    def draw(self, screen):
        for segment in self.body:
            x, y = segment
            pygame.draw.rect(screen, "white", [x, y, self.size, self.size])

    def snakeHead(self):
        head_x, head_y = self.body[0]
        return pygame.Rect(head_x, head_y, self.size, self.size)

    def wallCollision(self):
        head_x, head_y = self.body[0]
        if head_x < 0 or head_x >= self.game.screen.get_width() or head_y < 0 or head_y >= self.game.screen.get_height():
            return True
        return False

    def selfCollision(self):
        head = self.body[0]
        if head in self.body[1:]:
            return True
        return False
