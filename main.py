import pygame
import math
from indices import *
from sys import exit
import random
import json
import os

pygame.init()

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(‘Barbie shopping’)
clock = pygame.time.Clock()

background = pygame.image.load(r'jogo\imagensons\image\background0.png').convert_alpha()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
game_over_image = pygame.image.load(r'jogo\imagensons\image\game_over.png').convert_alpha()
game_over_image = pygame.transform.scale(game_over_image, (WIDTH, HEIGHT))
start_screen_image = pygame.image.load(r'jogo\imagensons\image\inicio.png').convert_alpha()
start_screen_image = pygame.transform.scale(start_screen_image, (WIDTH, HEIGHT))
start_button_image = pygame.image.load(r'jogo\imagensons\image\Start.png').convert_alpha()
start_button_image = pygame.transform.scale(start_button_image, (200, 100))
character_select_button_image = pygame.image.load(r'jogo\imagensons\image\character_select.png').convert_alpha()
character_select_button_image = pygame.transform.rotozoom(character_select_button_image, 0, 1.2)
character_select_button_image = pygame.transform.scale(character_select_button_image, (200, 100))
ranking_button_image = pygame.image.load(r'jogo\imagensons\image\ranking.png').convert_alpha()
ranking_button_image = pygame.transform.scale(ranking_button_image, (200, 100))

pygame.mixer.music.load(r'jogo\imagensons\sound\apocalypse.mp3')  
pygame.mixer.music.set_volume(0.8)
game_over_music = pygame.mixer.Sound(r'ogo\imagensons\sound\go_effect.mp3') 
game_over_music.set_volume(0.5)
shoot_sound = pygame.mixer.Sound(r'ogo\imagensons/sound\shot.mp3')
shoot_sound.set_volume(0.1)
music_loaded = True

