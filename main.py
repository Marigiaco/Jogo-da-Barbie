Barbie Shopping Spree - Jogo Principal

import pygame
import math
import random
import json
import os
from sys import exit
from parametros import *

pygame.init()

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('🎀 Barbie Shopping Spree 🎀')
clock = pygame.time.Clock()

font_small = pygame.font.SysFont('Arial', 24, bold=True)
font_med = pygame.font.SysFont('Arial', 36, bold=True)
font_big = pygame.font.SysFont('Arial', 64, bold=True)
font_huge = pygame.font.SysFont('Arial', 96, bold=True)


def desenhar_cenario(surface):
    """Desenha um fundo rosa com 'passarela' e estrelinhas decorativas."""
    for y in range(HEIGHT):
        t = y / HEIGHT
        r = int(PEARL[0] * (1 - t) + LIGHT_PINK[0] * t)
        g = int(PEARL[1] * (1 - t) + LIGHT_PINK[1] * t)
        b = int(PEARL[2] * (1 - t) + LIGHT_PINK[2] * t)
        pygame.draw.line(surface, (r, g, b), (0, y), (WIDTH, y))


    passarela_w = 280
    passarela_x = WIDTH // 2 - passarela_w // 2
    pygame.draw.rect(surface, HOT_PINK, (passarela_x, 0, passarela_w, HEIGHT))
    # Bordas brancas da passarela
    pygame.draw.rect(surface, WHITE, (passarela_x - 4, 0, 4, HEIGHT))
    pygame.draw.rect(surface, WHITE, (passarela_x + passarela_w, 0, 4, HEIGHT))


    estrelas = [
        (80, 100), (200, 250), (140, 480), (90, 620),
        (1100, 90), (1180, 280), (1140, 500), (1080, 650),
        (380, 180), (380, 540), (900, 160), (900, 560),
    ]
    for ex, ey in estrelas:
        desenhar_brilho(surface, ex, ey, 8, WHITE)
    
class Barbie(pygame.sprite.Sprite):
    """A boneca jogadora. Desenhada por formas geométricas."""

    def __init__(self):
        super().__init__()
        self.pos = pygame.math.Vector2(PLAYER_START_X, PLAYER_START_Y)
        self.speed = PLAYER_SPEED
        self.original_speed = self.speed
        self.radius = PLAYER_RADIUS

        # Vida e estado
        self.max_health = MAX_HEALTH
        self.current_health = MAX_HEALTH
        self.invincible_timer = 0
        self.alive = True
        self.extra_lives = 0
        self.max_extra_lives = 2

        # Power-ups
        self.is_immune = False
        self.immune_until = 0
        self.speed_boost_until = 0
        self.speed_boost_active = False
        self.magnet_until = 0
        self.magnet_active = False

        # "rect" para colisões (usado pelo sprite group)
        self.image = pygame.Surface((self.radius * 2, self.radius * 3), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=self.pos)