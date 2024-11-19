import pygame
import time
import random

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()

pygame.mixer.music.load('countdown.mp3')
game_music = pygame.mixer.Sound('gamemusic.mp3')
apple_sound = pygame.mixer.Sound("coin.mp3")

white = (255, 255, 255)
black = (0, 0, 0)

font = pygame.font.Font("bitfont.TTF", 32)
title = pygame.image.load('title.png')

background = pygame.image.load('background.png')
background_images = ['galaxy1.jpg', 'galaxy2.jpg', 'galaxy3.png', 'galaxy4.jpg', 'galaxy5.webp']
current_background = 0

class Snake:
    def __init__(self, game):
        self.size = 40 # Taille du Serpent
        self.body = [(screen.get_width() // 2, screen.get_height() // 2)] # Le corps du serpent apparait au millieu de l'ecran
        self.direction = (0, 0)
        self.started = False # Le Serpent ne se dirige nulle part ( sans direction )
        self.game = game

    def movement(self):
        if self.direction != (0, 0):
            head_x, head_y = self.body[0] # Incarne le Snakehead ou la partie central du snake, la tete.
            head_x += self.direction[0] * self.size
            head_y += self.direction[1] * self.size

            # Insérer la nouvelle position de la tête, segement supplementaire.
            self.body.insert(0, (head_x, head_y))
            if len(self.body) > self.game.score + 1:
                self.body.pop() # Retire le segment à chaque deplacement de la tete si il ne mange pas de pomme

    def change_direction(self, dx, dy):
        # Changer la direction du serpent
        # Empêcher de faire demi-tour
        if (dx, dy) != (-self.direction[0], -self.direction[1]):
            self.direction = (dx, dy)
            self.started = True # Le serpent bouge à present :)

    def draw(self, screen):
        for segment in self.body: 
            x, y = segment
            pygame.draw.rect(screen, "white", [x, y, self.size, self.size]) # Dessine autant de segment qui se trouve dans le self.body

    def snakeHead(self):
        head_x, head_y = self.body[0]  # Permet de définir le snake[0] comme la tete du serpent
        return pygame.Rect(head_x, head_y, self.size, self.size)

    def wallCollision(self):
        head_x, head_y = self.body[0]
        if head_x < 0 or head_x >= screen.get_width() or head_y < 0 or head_y >= screen.get_height(): # Si la tete, self.body 0 est egale ou depasse à la taille de l'ecran, jz retourne False
            return True
        return False

    def selfCollision(self):
        head = self.body[0]
        if head in self.body[1:]: # Si la tete du serpent se trouve dans une position ou se trouve deja un segment du serpent, je retourne False
            return True
        return False
    

class Apple:
    def __init__(self, size=40):
        self.size = size
        self.position = self.applePosition()
    
    def applePosition(self):
        margin = 300 # Variable que j'ai crée afin d'empecher l'apple d'etre trop proche des bordures.
        x = random.randint(margin // 40, (screen.get_width() - margin) // 40) * 40 # Poisiton random x en divisant la largeur de l'ecran avec un margin de 300
        y = random.randint(margin // 40, (screen.get_height() - margin) // 40) * 40
        return pygame.Vector2(x, y)

    def draw(self, screen, color="red"):
        pygame.draw.rect(screen, color, [self.position.x, self.position.y, self.size, self.size]) # Dessin de la pomme

    def comeback(self):
        self.position = self.applePosition() # Lorsque que Comebacj est activé, il reactive l'Appleposition qui permet d'afficher une pomme

class Game:
    def __init__(self):
        self.score = 0
        self.bestscore = 0
        self.current_background = 0
        self.snake = Snake(self)
        self.apple = Apple(size=40)
        self.big_apple = None

    def reset(self):
        self.score = 0
        self.snake = Snake(self)
        self.apple.comeback()
        self.big_apple = None

    def update_background(self):
        if self.score % 5 == 0 and self.score != 0:
            self.current_background = (self.score // 5) % len(background_images)

    def check_collisions(self):
        if self.snake.wallCollision() or self.snake.selfCollision():
            print("Game Over ")
            if self.score > self.bestscore:
                self.bestscore = self.score
            self.reset()

    def handle_apple_collision(self):
        if self.score < 20:
            if self.snake.snakeHead().colliderect(pygame.Rect(self.apple.position.x, self.apple.position.y, self.apple.size, self.apple.size)):
                pygame.mixer.Sound.play(apple_sound)
                self.score += 5
                self.apple.comeback()
        else:
            if self.big_apple is None:
                self.big_apple = Apple(size=80)
            if self.snake.snakeHead().colliderect(pygame.Rect(self.big_apple.position.x, self.big_apple.position.y, self.big_apple.size, self.big_apple.size)):
                pygame.mixer.Sound.play(apple_sound)
                self.score += 10
                self.big_apple = None

    def draw(self):
        image = pygame.image.load(background_images[self.current_background])
        screen.blit(image, (0, 0))

        self.snake.draw(screen)
        if self.score < 20:
            self.apple.draw(screen)
        if self.big_apple is not None:
            self.big_apple.draw(screen)

        custom_font = pygame.font.Font("bitfont.TTF", 48)
        score_text = custom_font.render(f"Score: {self.score}", True, white)
        bestscore_text = custom_font.render(f"Best Score: {self.bestscore}", True, white)
        screen.blit(score_text, (80, 10))
        screen.blit(bestscore_text, (550, 10))

def countdown():
    count = 10
    pygame.mixer.music.play()
    game_music.play()
    while count >= 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
                
        screen.fill(black)
        screen.blit(background, (0, 0))
        screen.blit(title, (150, -40))

        countdown_text = font.render(f"Start in {count} seconds", True, black)
        text_rect = countdown_text.get_rect(center=(screen.get_width() // 2, 680))
        screen.blit(countdown_text, text_rect)
        
        pygame.display.flip()
        time.sleep(1)
        count -= 1

    pygame.mixer.music.stop()
    return True

def game_loop():
    game = Game()
    running = True
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

        game.update_background()
        game.snake.movement()
        game.handle_apple_collision()
        game.check_collisions()
        game.draw()

        if game.score >= 20:
            clock.tick(25)
        else:
            clock.tick(20)

        pygame.display.flip()

    pygame.quit()

if countdown():
    game_loop()
