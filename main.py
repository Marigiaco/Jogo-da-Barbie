import pygame 
import math
import random
import json
import os
from sys import exit
from indices import *
# Importa a biblioteca Pygame e outras bibliotecas utilizadas no código
pygame.init() # Inicializa os módulos do pygame, necessário antes do código
window = pygame.display.set_mode((WIDTH, HEIGHT)) # Cria a aba do jogo com largura e altura definidos em indices.py
pygame.display.set_caption('Barbie Shopping Rush')
clock = pygame.time.Clock() # Cria um Clock que controla os quadros por segundo 
ASSETS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', 'images') # chega nas assets/images,  __file__ é o caminho, join junta com 'assets/images'
# Caminho até a pasta de sons (mesma lógica do ASSETS_DIR, mas pra sons)
SOUNDS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', 'sound')

def carregar_som(nome_arquivo, volume=1.0):
    caminho = os.path.join(SOUNDS_DIR, nome_arquivo)
    som = pygame.mixer.Sound(caminho)
    som.set_volume(volume)  # volume vai de 0.0 (mudo) até 1.0 (máximo)
    return som

# Carrega os efeitos sonoros (volume baixo pra não estourar)
SOM_DANO = carregar_som('dano.mp3', volume=0.4)
SOM_GAME_OVER = carregar_som('game_over.mp3', volume=0.6)

# Carrega a música de fundo (usa mixer.music, que é diferente de Sound — feito pra músicas longas)
pygame.mixer.music.load(os.path.join(SOUNDS_DIR, 'musica_fundo.mp3'))
pygame.mixer.music.set_volume(0.3)  # volume mais baixo pra não atrapalhar os SFX

def carregar_imagem(nome_arquivo, tamanho=None): 
    caminho = os.path.join(ASSETS_DIR, nome_arquivo) # Monta o caminho completo até o arquivo (ex: /Users/.../assets/images/barbie.png)
    img = pygame.image.load(caminho).convert_alpha() # Carrega a imagem do disco e converte pra formato com transparência (alpha)
    if tamanho is not None: # Se foi passado um tamanho, redimensiona a imagem pra esse tamanho
        img = pygame.transform.scale(img, tamanho)
    return img
ITEM_IMAGES = { # Dicionário com as imagens de cada item, todas redimensionadas pra 40x40 pixels
    'bag':      carregar_imagem('bag.png',      (40, 40)),
    'lipstick': carregar_imagem('batom.png', (40, 40)),
    'shoe':     carregar_imagem('shoe.png',     (40, 40)),
    'jewel':    carregar_imagem('jewel.png',    (40, 40)),
    'crown':    carregar_imagem('crown.png',    (40, 40)),
}
POWERUP_IMAGES = {
    'health':     carregar_imagem('pu_health.png',     (60, 60)),
    'immunity':   carregar_imagem('pu_immunity.png',   (60, 60)),
    'speed':      carregar_imagem('pu_speed.png',      (60, 60)),
    'magnet':     carregar_imagem('pu_magnet.png',     (60, 60)),
    'extra_life': carregar_imagem('pu_extra_life.png', (60, 60)),
    'sparkle':    carregar_imagem('pu_sparkle.png',    (60, 60)),
}

TELA_INICIO_IMG = carregar_imagem("tela_inicio.png", (WIDTH, HEIGHT))
BTN_JOGAR_IMG = carregar_imagem("botao_jogar.png", (220,70))
BTN_RANKING_IMG = carregar_imagem("botao_ranking.png", (220,70))
BTN_SAIR_IMG = carregar_imagem("botao_sair.png", (220,70))
font_small = pygame.font.SysFont('Arial', 24, bold=True)
font_med = pygame.font.SysFont('Arial', 36, bold=True)
font_big = pygame.font.SysFont('Arial', 64, bold=True)
font_huge = pygame.font.SysFont('Arial', 96, bold=True)
# Cria as fontes do sistema (Arial em negrito) em tamanhos diferentes pra textos do jogo
BG_IMAGE = carregar_imagem('background.png', (WIDTH, HEIGHT))
BARBIE_IMAGE = carregar_imagem('barbie.png', (70, 160))
DISASTER_IMAGE = carregar_imagem('cloud.png', (80, 60))
def desenhar_cenario(surface):
    surface.blit(BG_IMAGE, (0, 0))


class Barbie(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.pos = pygame.math.Vector2(PLAYER_START_X, PLAYER_START_Y)
        self.speed = PLAYER_SPEED
        self.original_speed = self.speed
        self.radius = PLAYER_RADIUS

        self.max_health = MAX_HEALTH
        self.current_health = MAX_HEALTH
        self.invincible_timer = 0
        self.alive = True
        self.extra_lives = 0
        self.max_extra_lives = 2

        self.is_immune = False
        self.immune_until = 0
        self.speed_boost_until = 0
        self.speed_boost_active = False
        self.magnet_until = 0
        self.magnet_active = False

        self.image = BARBIE_IMAGE
        self.rect = self.image.get_rect(center=self.pos)

    def desenhar(self, surface):
        if not self.alive:
            return

        if self.invincible_timer > 0 and (self.invincible_timer // 5) % 2 == 0:
            return

        self.rect.center = (int(self.pos.x), int(self.pos.y))
        surface.blit(self.image, self.rect) 

        x, y = int(self.pos.x), int(self.pos.y)
        if self.is_immune:
            pygame.draw.circle(surface, MINT, (x, y), self.radius + 15, 3)
        if self.speed_boost_active:
            pygame.draw.circle(surface, GOLD, (x, y), self.radius + 20, 2)

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
        self.pos.x = max(self.radius, min(self.pos.x, WIDTH - self.radius))
        self.pos.y = max(self.radius + 20, min(self.pos.y, HEIGHT - self.radius - 20))

    def levar_dano(self, percent=DISASTER_DAMAGE):
        if self.invincible_timer > 0 or not self.alive or self.is_immune:
            return
        SOM_DANO.play()
        self.current_health -= self.max_health * percent
        self.invincible_timer = INVINCIBLE_FRAMES
        if self.current_health <= 0:
            if self.extra_lives > 0:
                self.extra_lives -= 1
                self.current_health = self.max_health
            else:
                self.current_health = 0
                self.alive = False
                SOM_GAME_OVER.play()
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

TIPOS_ITEM = ['bag', 'lipstick', 'shoe', 'jewel', 'crown']

PESOS_ITEM = [50, 25, 15, 8, 2]

SCORE_POR_TIPO = {
    'bag': SCORE_BAG,
    'lipstick': SCORE_LIPSTICK,
    'shoe': SCORE_SHOE,
    'jewel': SCORE_JEWEL,
    'crown': SCORE_CROWN,
}

class Item(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.tipo = random.choices(TIPOS_ITEM, weights=PESOS_ITEM, k=1)[0]
        self.radius = ITEM_RADIUS
        self.pos = pygame.math.Vector2(
            random.randint(50, WIDTH - 50),
            random.randint(-300, -50)
        )
        self.speed = ITEM_FALL_SPEED + random.uniform(0, 1.5)
        self.fase = random.uniform(0, 2 * math.pi)

        self.image = ITEM_IMAGES[self.tipo]
        self.rect = self.image.get_rect(center=self.pos)
    def desenhar(self, surface):
        surface.blit(self.image, self.image.get_rect(center=(int(self.pos.x), int(self.pos.y))))

    def update(self):
        self.pos.y += self.speed
        self.fase += 0.05
        self.pos.x += math.sin(self.fase) * 0.6
        self.rect.center = (int(self.pos.x), int(self.pos.y))

        if barbie_ref[0] is not None and barbie_ref[0].magnet_active and barbie_ref[0].alive:
            alvo = pygame.math.Vector2(barbie_ref[0].pos)
            direcao = alvo - self.pos
            if direcao.length() < 250 and direcao.length() > 0:
                direcao = direcao.normalize() * 6
                self.pos += direcao

        if self.pos.y > HEIGHT + 50:
            self.kill()

barbie_ref = [None]

class FashionDisaster(pygame.sprite.Sprite):
    def __init__(self, posicao):
        super().__init__()
        self.pos = pygame.math.Vector2(posicao)
        self.radius = DISASTER_RADIUS
        self.speed = DISASTER_SPEED + random.uniform(0, 0.8)
        self.fase = random.uniform(0, 2 * math.pi)
        self.image = DISASTER_IMAGE
        self.rect = self.image.get_rect(center=self.pos)
    def desenhar(self, surface):
        surface.blit(self.image, self.image.get_rect(center=(int(self.pos.x), int(self.pos.y))))
    def perseguir(self, alvo_pos):
        direcao = pygame.math.Vector2(alvo_pos) - self.pos
        if direcao.length() > 0:
            direcao = direcao.normalize()
            self.pos += direcao * self.speed
        self.fase += 0.1
        self.pos.y += math.sin(self.fase) * 0.3
        self.rect.center = (int(self.pos.x), int(self.pos.y))

    def update(self):
        if barbie_ref[0] is not None and barbie_ref[0].alive:
            self.perseguir(barbie_ref[0].pos)

def spawn_disasters(grupo, quantidade):
    for _ in range(quantidade):
        lado = random.choice(['top', 'bottom', 'left', 'right'])
        if lado == 'top':
            pos = (random.randint(0, WIDTH), -50)
        elif lado == 'bottom':
            pos = (random.randint(0, WIDTH), HEIGHT + 50)
        elif lado == 'left':
            pos = (-50, random.randint(0, HEIGHT))
        else:
            pos = (WIDTH + 50, random.randint(0, HEIGHT))
        grupo.add(FashionDisaster(pos))

TIPOS_POWERUP = ['health', 'immunity', 'speed', 'magnet', 'extra_life', 'sparkle']

class PowerUp(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.tipo = random.choice(TIPOS_POWERUP)
        self.radius = POWERUP_RADIUS
        self.pos = pygame.math.Vector2(
            random.randint(80, WIDTH - 80),
            random.randint(80, HEIGHT - 80)
        )
        self.criado_em = pygame.time.get_ticks()
        self.duracao_na_tela = 10000  # some depois de 10s se ninguém pegar
        self.fase = 0
        self.image = POWERUP_IMAGES[self.tipo]
        self.rect = self.image.get_rect(center=self.pos)

    def desenhar(self, surface):
    
        x, y = int(self.pos.x), int(self.pos.y)

    
        self.fase += 0.1
        escala = 1 + 0.15 * math.sin(self.fase)


        img_base = POWERUP_IMAGES[self.tipo]

        nova_largura = int(img_base.get_width() * escala)
        nova_altura = int(img_base.get_height() * escala)

        img_escalada = pygame.transform.scale(img_base, (nova_largura, nova_altura))
 
        rect = img_escalada.get_rect(center=(x, y))
        surface.blit(img_escalada, rect)

  
        pygame.draw.circle(surface, WHITE, (x, y), int(self.radius + 4 * escala), 2)

    def update(self):
        if pygame.time.get_ticks() - self.criado_em > self.duracao_na_tela:
            self.kill()

def desenhar_hud(surface, barbie, score, wave):
    barra_x, barra_y, barra_w, barra_h = 20, 20, 300, 24
    pygame.draw.rect(surface, DARK_PINK, (barra_x - 3, barra_y - 3, barra_w + 6, barra_h + 6), border_radius=8)
    pygame.draw.rect(surface, WHITE, (barra_x, barra_y, barra_w, barra_h), border_radius=6)
    frac = max(0, barbie.current_health / barbie.max_health)
    pygame.draw.rect(surface, RED, (barra_x, barra_y, int(barra_w * frac), barra_h), border_radius=6)
    txt = font_small.render(f"Vida: {int(barbie.current_health)}/{barbie.max_health}", True, BLACK)
    surface.blit(txt, (barra_x + 8, barra_y + 1))

    score_text = font_med.render(f"💎 {score}", True, DARK_PINK)
    surface.blit(score_text, (WIDTH - score_text.get_width() - 30, 20))

    wave_text = font_small.render(f"Onda {wave}", True, DARK_PINK)
    surface.blit(wave_text, (WIDTH - wave_text.get_width() - 30, 65))

    icone_vida = pygame.transform.scale(POWERUP_IMAGES['health'], (28, 28))
    for i in range(barbie.extra_lives):
        surface.blit(icone_vida, (20 + i * 35, HEIGHT - 45))



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

def salvar_ranking(ranking):
    try:
        with open(RANKING_FILE, 'w') as f:
            json.dump(ranking, f, indent=2)
    except OSError:
        pass  

def adicionar_ao_ranking(nome, score):
    ranking = carregar_ranking()
    ranking.append({'nome': nome, 'score': score})
    ranking.sort(key=lambda r: r['score'], reverse=True)
    ranking = ranking[:10]
    salvar_ranking(ranking)
    return ranking



def tela_inicio():
    # Cria os rects (área retangular) de cada botão centralizados horizontalmente
    # Os números do y (450, 540, 630) você ajusta dependendo de onde quer que apareçam
    btn_jogar_rect   = BTN_JOGAR_IMG.get_rect(center=(WIDTH // 2, 450))
    btn_ranking_rect = BTN_RANKING_IMG.get_rect(center=(WIDTH // 2, 540))
    btn_sair_rect    = BTN_SAIR_IMG.get_rect(center=(WIDTH // 2, 630))

    while True:
        # Pega a posição atual do mouse (pra efeito de hover, opcional)
        mouse_pos = pygame.mouse.get_pos()

        # Trata os eventos (clique, fechar janela, etc)
        for event in pygame.event.get():
            # Fechou a janela no X
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            # Clicou com o botão esquerdo do mouse
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Se o clique caiu DENTRO do rect do botão Jogar...
                if btn_jogar_rect.collidepoint(event.pos):
                    return NAME_SCREEN  # ou GAMEPLAY, dependendo da sua máquina de estados
                if btn_ranking_rect.collidepoint(event.pos):
                    return RANKING_SCREEN
                if btn_sair_rect.collidepoint(event.pos):
                    pygame.quit()
                    exit()

        # Desenha a imagem de fundo da tela (cobre tudo)
        window.blit(TELA_INICIO_IMG, (0, 0))

        # Desenha os 3 botões por cima
        window.blit(BTN_JOGAR_IMG, btn_jogar_rect)
        window.blit(BTN_RANKING_IMG, btn_ranking_rect)
        window.blit(BTN_SAIR_IMG, btn_sair_rect)

        # Atualiza a tela e mantém o FPS
        pygame.display.flip()
        clock.tick(FPS)

    while True:
        desenhar_cenario(window)

        # Título
        titulo = font_huge.render("Barbie", True, DARK_PINK)
        sub = font_big.render("Shopping Spree", True, HOT_PINK)
        window.blit(titulo, (WIDTH // 2 - titulo.get_width() // 2, 80))
        window.blit(sub, (WIDTH // 2 - sub.get_width() // 2, 180))

        # Botões
        for rect, label, cor in [
            (btn_play, "JOGAR", HOT_PINK),
            (btn_rank, "RANKING", BARBIE_PINK),
            (btn_quit, "SAIR", DARK_PINK),
        ]:
            pygame.draw.rect(window, cor, rect, border_radius=20)
            pygame.draw.rect(window, WHITE, rect, 3, border_radius=20)
            txt = font_med.render(label, True, WHITE)
            window.blit(txt, (rect.centerx - txt.get_width() // 2,
                              rect.centery - txt.get_height() // 2))

        dica = font_small.render("Use WASD ou setas para mover. Colete itens, evite as nuvens cinzas!", True, DARK_PINK)
        window.blit(dica, (WIDTH // 2 - dica.get_width() // 2, HEIGHT - 60))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_play.collidepoint(event.pos):
                    return GET_PLAYER_NAME
                if btn_rank.collidepoint(event.pos):
                    return SHOW_RANKING
                if btn_quit.collidepoint(event.pos):
                    pygame.quit()
                    exit()

        pygame.display.update()
        clock.tick(FPS)

def tela_nome():
    nome = ""
    input_rect = pygame.Rect(WIDTH // 2 - 200, HEIGHT // 2, 400, 60)
    btn_ok = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 90, 200, 60)

    while True:
        desenhar_cenario(window)
        titulo = font_big.render("Qual é o seu nome?", True, DARK_PINK)
        window.blit(titulo, (WIDTH // 2 - titulo.get_width() // 2, HEIGHT // 3))

        pygame.draw.rect(window, WHITE, input_rect, border_radius=12)
        pygame.draw.rect(window, DARK_PINK, input_rect, 3, border_radius=12)
        txt = font_med.render(nome + "|", True, BLACK)
        window.blit(txt, (input_rect.x + 12, input_rect.y + 12))

        pygame.draw.rect(window, HOT_PINK, btn_ok, border_radius=16)
        pygame.draw.rect(window, WHITE, btn_ok, 3, border_radius=16)
        ok = font_med.render("COMEÇAR", True, WHITE)
        window.blit(ok, (btn_ok.centerx - ok.get_width() // 2,
                         btn_ok.centery - ok.get_height() // 2))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return START_SCREEN, ""
                if event.key == pygame.K_RETURN and nome.strip():
                    return GAME_ACTIVE, nome.strip()
                if event.key == pygame.K_BACKSPACE:
                    nome = nome[:-1]
                else:
                    if len(nome) < 15 and event.unicode.isprintable():
                        nome += event.unicode
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_ok.collidepoint(event.pos) and nome.strip():
                    return GAME_ACTIVE, nome.strip()

        pygame.display.update()
        clock.tick(FPS)




def tela_ranking():
    btn_back = pygame.Rect(WIDTH // 2 - 100, HEIGHT - 80, 200, 50)
    while True:
        desenhar_cenario(window)
        titulo = font_big.render("Top 10 Fashionistas", True, DARK_PINK)
        window.blit(titulo, (WIDTH // 2 - titulo.get_width() // 2, 60))
        ranking = carregar_ranking()
        if not ranking:
            msg = font_med.render("Nenhuma pontuação ainda. Seja a primeira!", True, DARK_PINK)
            window.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2))
        else:
            for i, r in enumerate(ranking[:10]):
                linha = font_med.render(f"{i + 1}. {r['nome']}  -  {r['score']}", True, DARK_PINK)
                window.blit(linha, (WIDTH // 2 - 200, 150 + i * 40))
        pygame.draw.rect(window, HOT_PINK, btn_back, border_radius=12)
        pygame.draw.rect(window, WHITE, btn_back, 3, border_radius=12)
        bt = font_small.render("VOLTAR", True, WHITE)
        window.blit(bt, (btn_back.centerx - bt.get_width() // 2,
                         btn_back.centery - bt.get_height() // 2))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return START_SCREEN
            if event.type == pygame.MOUSEBUTTONDOWN and btn_back.collidepoint(event.pos):
                return START_SCREEN

        pygame.display.update()
        clock.tick(FPS)



def tela_game_over(score, nome):
    if nome:
        adicionar_ao_ranking(nome, score)

    btn_again = pygame.Rect(WIDTH // 2 - 220, HEIGHT // 2 + 80, 200, 60)
    btn_menu = pygame.Rect(WIDTH // 2 + 20, HEIGHT // 2 + 80, 200, 60)

    while True:
        desenhar_cenario(window)

        # Overlay rosa escuro
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((100, 0, 50, 120))
        window.blit(overlay, (0, 0))

        titulo = font_huge.render("Game Over", True, WHITE)
        window.blit(titulo, (WIDTH // 2 - titulo.get_width() // 2, HEIGHT // 4))

        sc = font_big.render(f"Pontuação: {score}", True, GOLD)
        window.blit(sc, (WIDTH // 2 - sc.get_width() // 2, HEIGHT // 2 - 20))

        if nome:
            tag = font_small.render(f"Salvo no ranking como '{nome}'", True, WHITE)
            window.blit(tag, (WIDTH // 2 - tag.get_width() // 2, HEIGHT // 2 + 40))

        pygame.draw.rect(window, HOT_PINK, btn_again, border_radius=16)
        pygame.draw.rect(window, WHITE, btn_again, 3, border_radius=16)
        txt = font_small.render("JOGAR DE NOVO", True, WHITE)
        window.blit(txt, (btn_again.centerx - txt.get_width() // 2,
                          btn_again.centery - txt.get_height() // 2))

        pygame.draw.rect(window, DARK_PINK, btn_menu, border_radius=16)
        pygame.draw.rect(window, WHITE, btn_menu, 3, border_radius=16)
        txt2 = font_small.render("MENU", True, WHITE)
        window.blit(txt2, (btn_menu.centerx - txt2.get_width() // 2,
                           btn_menu.centery - txt2.get_height() // 2))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return START_SCREEN
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_again.collidepoint(event.pos):
                    return GET_PLAYER_NAME
                if btn_menu.collidepoint(event.pos):
                    return START_SCREEN

        pygame.display.update()
        clock.tick(FPS)

def spawn_itens(grupo, quantidade):
    for _ in range(quantidade):
        grupo.add(Item())
def colisao_circulos(a, b, ra, rb):
    return a.distance_to(b) < (ra + rb)
def rodar_partida(nome_jogador):
   
    barbie = Barbie()
    barbie_ref[0] = barbie
    pygame.mixer.music.play(-1)
    itens = pygame.sprite.Group()
    disasters = pygame.sprite.Group()
    powerups = pygame.sprite.Group()
    score = 0
    wave = 1
    spawn_itens(itens, BASE_ITEMS_PER_WAVE)
    spawn_disasters(disasters, BASE_DISASTERS_PER_WAVE)
    ultimo_powerup_spawn = pygame.time.get_ticks()

    morte_em = None

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.mixer.music.stop()
                return score

        desenhar_cenario(window)

        agora = pygame.time.get_ticks()
        if (agora - ultimo_powerup_spawn > POWERUP_SPAWN_INTERVAL
                and len(powerups) == 0 and barbie.alive):
            ultimo_powerup_spawn = agora
            powerups.add(PowerUp())

        itens.update()
        for item in itens:
            item.desenhar(window)
            if barbie.alive and colisao_circulos(item.pos, barbie.pos, item.radius, barbie.radius):
                score += SCORE_POR_TIPO[item.tipo]
                item.kill()

        disasters.update()
        for d in disasters:
            d.desenhar(window)
            if barbie.alive and colisao_circulos(d.pos, barbie.pos, d.radius, barbie.radius):
                barbie.levar_dano()

        powerups.update()
        for p in powerups:
            p.desenhar(window)
            if barbie.alive and colisao_circulos(p.pos, barbie.pos, p.radius, barbie.radius):
                if p.tipo == 'sparkle':
                    for d in list(disasters):
                        d.kill()
                else:
                    barbie.ativar_powerup(p.tipo)
                p.kill()

        barbie.update()
        barbie.desenhar(window)
        desenhar_hud(window, barbie, score, wave)

        nome_txt = font_small.render(f"Jogadora: {nome_jogador}", True, DARK_PINK)
        window.blit(nome_txt, (20, HEIGHT - 60))

        if len(itens) == 0 and barbie.alive:
            wave += 1
            spawn_itens(itens, BASE_ITEMS_PER_WAVE + wave * 2)
            spawn_disasters(disasters, BASE_DISASTERS_PER_WAVE + wave)

        if not barbie.alive:
            if morte_em is None:
                morte_em = pygame.time.get_ticks()
            elif pygame.time.get_ticks() - morte_em > 1200:
                pygame.mixer.music.stop()
                return score

        pygame.display.update()
        clock.tick(FPS)



def main():
    estado = START_SCREEN
    nome_jogador = ""
    ultimo_score = 0
    pygame.mixer.music.play(-1)

    while True:
        if estado == START_SCREEN:
            estado = tela_inicio()
        elif estado == GET_PLAYER_NAME:
            estado, nome_jogador = tela_nome()
        elif estado == GAME_ACTIVE:
            ultimo_score = rodar_partida(nome_jogador)
            estado = GAME_OVER
        elif estado == GAME_OVER:
            estado = tela_game_over(ultimo_score, nome_jogador)
        elif estado == SHOW_RANKING:
            estado = tela_ranking()


if __name__ == '__main__':
    main()
