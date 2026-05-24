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
     def desenhar(self, surface):
        if not self.alive:
            return

        # Pisca quando invencível
        if self.invincible_timer > 0 and (self.invincible_timer // 5) % 2 == 0:
            return

        x, y = int(self.pos.x), int(self.pos.y)

        # Vestido (triângulo rosa)
        pygame.draw.polygon(surface, HOT_PINK, [
            (x, y + 8),
            (x - 30, y + 40),
            (x + 30, y + 40)
        ])
        # Detalhe do vestido (cinturinha)
        pygame.draw.rect(surface, DARK_PINK, (x - 14, y + 6, 28, 6))


        pygame.draw.rect(surface, (255, 220, 190), (x - 4, y - 6, 8, 12))

        pygame.draw.circle(surface, GOLD, (x, y - 18), 22)
        pygame.draw.rect(surface, GOLD, (x - 22, y - 18, 44, 32))


        pygame.draw.circle(surface, (255, 220, 190), (x, y - 18), 16)


        pygame.draw.circle(surface, BLACK, (x - 6, y - 20), 2)
        pygame.draw.circle(surface, BLACK, (x + 6, y - 20), 2)

        pygame.draw.arc(surface, DARK_PINK,
                        (x - 5, y - 16, 10, 8), math.pi, 2 * math.pi, 2)


        pygame.draw.polygon(surface, GOLD, [
            (x - 10, y - 32), (x - 6, y - 38),
            (x - 2, y - 33), (x + 2, y - 38),
            (x + 6, y - 33), (x + 10, y - 38),
            (x + 10, y - 30), (x - 10, y - 30)
        ])


        if self.is_immune:
            pygame.draw.circle(surface, MINT, (x, y + 10), 45, 3)

        if self.speed_boost_active:
            pygame.draw.circle(surface, GOLD, (x, y + 10), 50, 2)


        self.rect.center = (x, y + 10)

   
    def processar_input(self):
        if not self.alive:
            return

        keys = pygame.key.get_pressed()
        dx = dy = 0
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            dy = -1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dy = 1
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            dx = -1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dx = 1

        if dx != 0 and dy != 0:
            dx *= 0.7071
            dy *= 0.7071

        self.pos.x += dx * self.speed
        self.pos.y += dy * self.speed

        # Limites da tela
        self.pos.x = max(self.radius, min(self.pos.x, WIDTH - self.radius))
        self.pos.y = max(self.radius + 20, min(self.pos.y, HEIGHT - self.radius - 20))


    def levar_dano(self, percent=DISASTER_DAMAGE):
        if self.invincible_timer > 0 or not self.alive or self.is_immune:
            return
        self.current_health -= self.max_health * percent
        self.invincible_timer = INVINCIBLE_FRAMES
        if self.current_health <= 0:
            if self.extra_lives > 0:
                self.extra_lives -= 1
                self.current_health = self.max_health
            else:
                self.current_health = 0
                self.alive = False

    # ------ Power-ups ------
    def ativar_powerup(self, tipo):
        agora = pygame.time.get_ticks()
        if tipo == 'health':
            self.current_health = self.max_health
        elif tipo == 'immunity':
            self.is_immune = True
            self.immune_until = agora + POWERUP_DURATION
        elif tipo == 'speed':
            self.speed = self.original_speed * 1.7
            self.speed_boost_active = True
            self.speed_boost_until = agora + POWERUP_DURATION
        elif tipo == 'magnet':
            self.magnet_active = True
            self.magnet_until = agora + POWERUP_DURATION
        elif tipo == 'extra_life':
            if self.extra_lives < self.max_extra_lives:
                self.extra_lives += 1

    def update(self):
        if not self.alive:
            return
        self.processar_input()
        agora = pygame.time.get_ticks()
        if self.is_immune and agora > self.immune_until:
            self.is_immune = False
        if self.speed_boost_active and agora > self.speed_boost_until:
            self.speed_boost_active = False
            self.speed = self.original_speed
        if self.magnet_active and agora > self.magnet_until:
            self.magnet_active = False
        if self.invincible_timer > 0:
            self.invincible_timer -= 1
        
def desenhar_hud(surface, barbie, score, wave):
    # Barra de vida
    barra_x, barra_y, barra_w, barra_h = 20, 20, 300, 24
    pygame.draw.rect(surface, DARK_PINK, (barra_x - 3, barra_y - 3, barra_w + 6, barra_h + 6), border_radius=8)
    pygame.draw.rect(surface, WHITE, (barra_x, barra_y, barra_w, barra_h), border_radius=6)
    frac = max(0, barbie.current_health / barbie.max_health)
    pygame.draw.rect(surface, RED, (barra_x, barra_y, int(barra_w * frac), barra_h), border_radius=6)
    txt = font_small.render(f"Vida: {int(barbie.current_health)}/{barbie.max_health}", True, BLACK)
    surface.blit(txt, (barra_x + 8, barra_y + 1))

    # Score
    score_text = font_med.render(f"💎 {score}", True, DARK_PINK)
    surface.blit(score_text, (WIDTH - score_text.get_width() - 30, 20))

    # Wave
    wave_text = font_small.render(f"Onda {wave}", True, DARK_PINK)
    surface.blit(wave_text, (WIDTH - wave_text.get_width() - 30, 65))

    # Vidas extras (coração no canto inferior esquerdo)
    for i in range(barbie.extra_lives):
        cx = 30 + i * 35
        cy = HEIGHT - 30
        desenhar_coracao(surface, cx, cy, 12, RED)


def desenhar_coracao(surface, x, y, tamanho, cor):
    """Desenha um coração simples (dois círculos + triângulo)."""
    pygame.draw.circle(surface, cor, (x - tamanho // 2, y - tamanho // 3), tamanho // 2)
    pygame.draw.circle(surface, cor, (x + tamanho // 2, y - tamanho // 3), tamanho // 2)
    pygame.draw.polygon(surface, cor, [
        (x - tamanho, y - tamanho // 3),
        (x + tamanho, y - tamanho // 3),
        (x, y + tamanho)
    ])

START_SCREEN = 0
GAME_ACTIVE = 1
GAME_OVER = 2
GET_PLAYER_NAME = 3
SHOW_RANKING = 4
RANKING_FILE = 'ranking.json'
def carregar_ranking():
    if not os.path.exists(RANKING_FILE):
        return []
    try:
        with open(RANKING_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return []
