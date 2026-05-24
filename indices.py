
# --- Tela ---
WIDTH = 1000
HEIGHT = 720
FPS = 60

# --- Cores (paleta Barbie) ---
BARBIE_PINK = (255, 105, 180)       # Rosa Barbie clássico
HOT_PINK = (255, 20, 147)           # Rosa choque
LIGHT_PINK = (255, 182, 193)        # Rosa claro
PEARL = (255, 240, 245)             # Branco perolado
GOLD = (255, 215, 0)                # Dourado (coroa)
PURPLE = (186, 85, 211)             # Roxo (joia)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_PINK = (199, 21, 133)          # Texto/sombras
MINT = (152, 255, 204)              # Detalhes
RED = (220, 20, 60)                 # Coração / vida

# --- Barbie (jogadora) ---
PLAYER_START_X = WIDTH // 2
PLAYER_START_Y = HEIGHT // 2
PLAYER_SPEED = 7
PLAYER_RADIUS = 28                  # Raio para colisão

# --- Itens coletáveis ---
ITEM_FALL_SPEED = 3                 # Velocidade que os itens "caem" da sacola mágica
ITEM_RADIUS = 22

# Pontuação por tipo de item
SCORE_BAG = 100                     # Sacola comum
SCORE_LIPSTICK = 150                # Batom
SCORE_SHOE = 200                    # Sapato
SCORE_JEWEL = 350                   # Joia
SCORE_CROWN = 1000                  # Coroa (raro)

# --- "Fashion disasters" (obstáculos) ---
DISASTER_SPEED = 2.5
DISASTER_RADIUS = 26
DISASTER_DAMAGE = 0.2               # 20% de vida por toque

# --- Power-ups ---
POWERUP_SPAWN_INTERVAL = 18000      # ms entre power-ups
POWERUP_DURATION = 8000             # ms de duração dos efeitos temporários
POWERUP_RADIUS = 24

# --- Sistema de ondas ---
BASE_ITEMS_PER_WAVE = 8             # itens na onda 1
BASE_DISASTERS_PER_WAVE = 3         # obstáculos na onda 1

# --- Vida ---
MAX_HEALTH = 100
INVINCIBLE_FRAMES = 60              # quadros de invencibilidade após levar dano