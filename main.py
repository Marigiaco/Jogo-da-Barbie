import pygame
import random

from parametros import *

pygame.init()

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Barbie Shopping Rush")

clock = pygame.time.Clock()

background = pygame.image.load("assets/images/background.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

barbie_img = pygame.image.load("assets/images/barbie.png")
bag_img = pygame.image.load("assets/images/bag.png")
coffee_img = pygame.image.load("assets/images/coffee.png")


class Barbie(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()

        self.image = pygame.transform.scale(barbie_img, (120, 120))

        self.rect = self.image.get_rect()

        self.rect.center = (WIDTH//2, HEIGHT-100)

        self.speed = BARBIE_SPEED

    def move(self):

        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rect.x -= self.speed

        if keys[pygame.K_d]:
            self.rect.x += self.speed

        if self.rect.left < 0:
            self.rect.left = 0

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

    def update(self):
        self.move()
        

class Coffee(pygame.sprite.Sprite):

    def _init_(self):
        super()._init_()

        self.image = pygame.transform.scale(coffee_img, (70, 70))

        self.rect = self.image.get_rect()

        self.rect.x = random.randint(50, WIDTH-50)
        self.rect.y = -100

        self.speed = ITEM_SPEED + 2

    def move(self):

        self.rect.y += self.speed

        if self.rect.top > HEIGHT:
            self.kill()

    def update(self):
        self.move()
        