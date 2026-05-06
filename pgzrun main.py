import pygame
import random
import os
from enum import Enum

# Inicializar pygame
pygame.init()

# ==================== CONFIGURACIÓN ====================
CELL_SIZE = 64
GRID_WIDTH = 13
GRID_HEIGHT = 17
WINDOW_WIDTH = CELL_SIZE * GRID_WIDTH  # 832
WINDOW_HEIGHT = CELL_SIZE * GRID_HEIGHT  # 1088

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
RED = (255, 50, 50)

# FPS
FPS = 80
clock = pygame.time.Clock()

# ==================== CLASE ACTOR ====================
class Actor:
    def __init__(self, image_name, pos=(0, 0), size=(64, 64)):
        self.image_name = image_name
        self.size = size
        self.rect = pygame.Rect(pos[0], pos[1], size[0], size[1])
        self.image = self._load_image(image_name)
        self.health = 100
        self.attack = 5
        self.shield = 0
        
    def _load_image(self, name):
        """Carga imagen desde la carpeta images"""
        image_path = os.path.join("images", f"{name}.png")
        try:
            img = pygame.image.load(image_path)
            img = pygame.transform.scale(img, self.size)
            return img
        except Exception as e:
            surface = pygame.Surface(self.size)
            surface.fill(GRAY)
            return surface
    
    def set_image(self, image_name):
        """Cambia la imagen del actor"""
        self.image_name = image_name
        self.image = self._load_image(image_name)
    
    def draw(self, surface):
        """Dibuja el actor"""
        surface.blit(self.image, self.rect)
    
    def colliderect(self, other):
        """Verifica colisión con otro actor"""
        return self.rect.colliderect(other.rect)
    
    def collidepoint(self, pos):
        """Verifica si un punto colisiona con el actor"""
        return self.rect.collidepoint(pos)
    
    @property
    def x(self):
        return self.rect.x
    
    @x.setter
    def x(self, value):
        self.rect.x = value
    
    @property
    def y(self):
        return self.rect.y
    
    @y.setter
    def y(self, value):
        self.rect.y = value
    
    @property
    def topleft(self):
        return self.rect.topleft
    
    @topleft.setter
    def topleft(self, pos):
        self.rect.topleft = pos
    
    @property
    def center(self):
        return self.rect.center
    
    @center.setter
    def center(self, pos):
        self.rect.center = pos
    
    @property
    def width(self):
        return self.rect.width
    
    @property
    def height(self):
        return self.rect.height

# ==================== ESTADOS DEL JUEGO ====================
class GameState(Enum):
    MENU = "MENU"
    GAME = "GAME"
    GAME_OVER = "GAME_OVER"
    WIN = "WIN"

# ==================== VARIABLES GLOBALES ====================
game_state = GameState.MENU
floor = 1
is_attacking = False
attack_timer = 0
current_attack_enemy_index = -1
current_attack_enemy_list = None
animation_reset_timer = 0
enemy_to_reset = None
enemy_to_reset_list = None
reset_image_name = None

# Listas
enemies = []
enemies2 = []
hearts = []
swords = []

# Enemigos
hp_big_goblin = random.randint(10, 15)
ap_big_goblin = 5
hp_small_goblin = random.randint(5, 10)
ap_small_goblin = 4

a1, a2 = 0, 3
b1, b2 = 0, 5

# ==================== MAPA ====================
my_map = [
    [0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,1,2,1,3,1,2,1,3,1,2,1,0],
    [0,1,1,2,1,1,2,1,1,2,1,1,0],
    [0,3,2,1,1,3,1,3,1,1,2,3,0],
    [0,1,1,1,3,1,2,1,3,1,1,1,0],
    [0,2,1,3,1,2,1,2,1,3,1,2,0],
    [0,1,2,1,1,2,1,2,1,1,2,1,0],
    [0,3,1,1,3,1,3,1,3,1,1,3,0],
    [0,1,3,1,1,3,1,3,1,1,3,1,0],
    [0,2,1,2,1,2,1,2,1,2,1,2,0],
    [0,1,2,1,3,1,2,1,3,1,2,1,0],
    [0,1,1,2,1,1,2,1,1,2,1,1,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0]
]

# ==================== ACTORES ====================
# Tiles del mapa
tile_border = Actor('border', size=(CELL_SIZE, CELL_SIZE))
tile_floor = Actor('floor', size=(CELL_SIZE, CELL_SIZE))
tile_crack = Actor('crack', size=(CELL_SIZE, CELL_SIZE))
tile_bones = Actor('bones', size=(CELL_SIZE, CELL_SIZE))

# Personaje
knight = Actor('knight', (CELL_SIZE, CELL_SIZE), size=(CELL_SIZE, CELL_SIZE))
knight.health = 100
knight.attack = 5
knight.shield = 0

# Botones y UI
play_button = Actor('menu4', (WINDOW_WIDTH // 2 - 225, WINDOW_HEIGHT // 2 - 100), size=(450, 200))
health_bar = Actor('health_bar5', (90, WINDOW_HEIGHT - 50), size=(140, 50))
shield_bar = Actor('shield_bar5', (90, WINDOW_HEIGHT - 100), size=(140, 50))

# Power-ups
chest = None

# ==================== GENERACIÓN DE ENEMIGOS ====================
def generate_enemies():
    global enemies, enemies2, hp_big_goblin, ap_big_goblin
    
    enemies = []
    enemies2 = []
    
    a = random.randint(a1, a2)
    b = random.randint(b1, b2)
    
    # Big Goblin
    for i in range(a):
        x1 = random.randint(1, 7) * CELL_SIZE
        y1 = random.randint(1, 7) * CELL_SIZE
        big_goblin = Actor("big_goblin8", (x1, y1), size=(CELL_SIZE, CELL_SIZE))
        big_goblin.health = hp_big_goblin
        big_goblin.attack = ap_big_goblin
        enemies.append(big_goblin)
    
    # Small Goblin
    for i in range(b):
        x2 = random.randint(1, 7) * CELL_SIZE
        y2 = random.randint(1, 7) * CELL_SIZE
        small_goblin = Actor("small_goblin12", (x2, y2), size=(CELL_SIZE, CELL_SIZE))
        small_goblin.health = hp_small_goblin
        small_goblin.attack = ap_small_goblin
        enemies2.append(small_goblin)

generate_enemies()

# ==================== GENERACIÓN DE COFRE ====================
def generate_chest():
    global chest
    chance = random.randint(1, 10)
    
    if chance <= 2:
        valid_position = False
        while not valid_position:
            z1 = random.randint(1, GRID_WIDTH - 2) * CELL_SIZE
            z2 = random.randint(1, GRID_HEIGHT - 2) * CELL_SIZE
            chest_pos = (z1, z2)
            
            valid_position = not any(
                enemy.rect.topleft == chest_pos for enemy in enemies + enemies2
            )
        
        chest = Actor('chest1', chest_pos, size=(CELL_SIZE, CELL_SIZE))
    else:
        chest = None

# ==================== POWER-UPS ====================
def generate_power_up(enemy):
    """Genera power-ups cuando muere un enemigo"""
    chance = random.randint(1, 10)
    
    if chance <= 3:  # 30% corazón
        new_heart = Actor('heart', enemy.center, size=(32, 32))
        hearts.append(new_heart)
    elif chance <= 6:  # 30% espada
        new_sword = Actor('sword', enemy.center, size=(32, 32))
        swords.append(new_sword)

def check_power_ups():
    """Verifica colisiones con power-ups"""
    # Colisión con corazones
    for heart_item in hearts[:]:
        if knight.colliderect(heart_item):
            if knight.health == 100:
                knight.shield = min(knight.shield + 20, 100)
            else:
                knight.health = min(knight.health + 20, 100)
            hearts.remove(heart_item)
            return
    
    # Colisión con espadas
    for sword_item in swords[:]:
        if knight.colliderect(sword_item):
            knight.attack += 2
            swords.remove(sword_item)
            return

# ==================== COMBATE ====================
def start_attack(enemy_index, enemy_list):
    """Inicia el ataque del caballero"""
    global is_attacking, attack_timer, current_attack_enemy_index, current_attack_enemy_list
    global animation_reset_timer, enemy_to_reset, enemy_to_reset_list, reset_image_name
    
    if is_attacking or enemy_index >= len(enemy_list):
        return
    
    is_attacking = True
    attack_timer = 0
    current_attack_enemy_index = enemy_index
    current_attack_enemy_list = enemy_list
    
    enemy = enemy_list[enemy_index]
    
    # Cambiar imagen según dirección
    if knight.image_name == 'knight':
        knight.set_image('atack-right')
        if enemy_list == enemies:
            enemy.set_image('big_goblin6')
            reset_image_name = 'big_goblin8'
        elif enemy_list == enemies2:
            enemy.set_image('small_goblin14')
            reset_image_name = 'small_goblin12'
    
    elif knight.image_name == 'left':
        knight.set_image('atack-left')
        if enemy_list == enemies:
            enemy.set_image('big_goblin2')
            reset_image_name = 'big_goblin8'
        elif enemy_list == enemies2:
            enemy.set_image('small_goblin2')
            reset_image_name = 'small_goblin12'
    
    # Guardar referencia del enemigo para resetear la animación
    enemy_to_reset = enemy
    enemy_to_reset_list = enemy_list

def apply_damage(enemy_index, enemy_list):
    """Aplica daño al enemigo"""
    global is_attacking, floor, a2, b2, hp_big_goblin, ap_big_goblin, game_state
    
    if enemy_index >= len(enemy_list):
        is_attacking = False
        return
    
    enemy = enemy_list[enemy_index]
    
    # Aplicar daño al caballero
    if knight.shield > 0:
        knight.shield -= enemy.attack
        if knight.shield < 0:
            knight.health += knight.shield
            knight.shield = 0
    else:
        knight.health -= enemy.attack
    
    # Aplicar daño al enemigo
    enemy.health -= knight.attack
    
    # Si el enemigo muere
    if enemy.health <= 0:
        generate_power_up(enemy)
        if enemy in enemy_list:
            enemy_list.remove(enemy)
    
    # Volver a la imagen original del caballero
    if knight.image_name == 'atack-right':
        knight.set_image('knight')
    elif knight.image_name == 'atack-left':
        knight.set_image('left')
    
    is_attacking = False
    
    # Verificar derrota
    if knight.health <= 0:
        game_state = GameState.GAME_OVER
    
    # Verificar victoria
    if floor == 11:
        game_state = GameState.WIN
    
    # Verificar siguiente piso
    if not enemies and not enemies2:
        floor += 1
        knight.health = min(knight.health + 30, 100)
        
        if floor < 3:
            b2 += 1
        
        if floor >= 3 and floor <= 5:
            a2 += 1
            b2 = max(b1, b2 - 1)
            hp_big_goblin += 5
            ap_big_goblin += 3
        
        generate_enemies()
        generate_chest()

# ==================== ACTUALIZAR BARRAS ====================
def update_health_bar():
    """Actualiza la imagen de la barra de vida"""
    if 80 < knight.health <= 100:
        health_bar.set_image('health_bar5')
    elif 60 < knight.health <= 80:
        health_bar.set_image('health_bar1')
    elif 40 < knight.health <= 60:
        health_bar.set_image('health_bar2')
    elif 20 < knight.health <= 40:
        health_bar.set_image('health_bar3')
    elif knight.health <= 0:
        health_bar.set_image('health_bar4')

def update_shield_bar():
    """Actualiza la imagen de la barra de escudo"""
    if 80 < knight.shield <= 100:
        shield_bar.set_image('shield_bar6')
    elif 60 < knight.shield <= 80:
        shield_bar.set_image('shield_bar1')
    elif 40 < knight.shield <= 60:
        shield_bar.set_image('shield_bar2')
    elif 20 < knight.shield <= 40:
        shield_bar.set_image('shield_bar3')
    elif 0 < knight.shield <= 20:
        shield_bar.set_image('shield_bar4')
    elif knight.shield <= 0:
        shield_bar.set_image('shield_bar5')

# ==================== FUENTE ====================
def get_font(size):
    """Obtiene la fuente AmeriGarmnd BT o una alternativa"""
    font_names = ['amerigarmnd bt.ttf', 'amerigarmnd.ttf', 'georgia', 'arial']
    
    for font_name in font_names:
        try:
            return pygame.font.SysFont(font_name, size, bold=True)
        except:
            pass
    
    # Fallback a fuente por defecto
    return pygame.font.Font(None, size)

# ==================== DIBUJO ====================
def draw_map(surface):
    """Dibuja el mapa"""
    for i in range(len(my_map)):
        for j in range(len(my_map[0])):
            if my_map[i][j] == 0:
                tile_border.topleft = (CELL_SIZE * j, CELL_SIZE * i)
                tile_border.draw(surface)
            elif my_map[i][j] == 1:
                tile_floor.topleft = (CELL_SIZE * j, CELL_SIZE * i)
                tile_floor.draw(surface)
            elif my_map[i][j] == 2:
                tile_crack.topleft = (CELL_SIZE * j, CELL_SIZE * i)
                tile_crack.draw(surface)
            elif my_map[i][j] == 3:
                tile_bones.topleft = (CELL_SIZE * j, CELL_SIZE * i)
                tile_bones.draw(surface)

def draw_game(surface):
    """Dibuja el juego"""
    surface.fill(BLACK)
    draw_map(surface)
    
    knight.draw(surface)
    health_bar.draw(surface)
    shield_bar.draw(surface)
    
    if chest:
        chest.draw(surface)
    
    # Fuentes
    font_floor = get_font(120)
    font_stats = get_font(24)
    font_ap = get_font(20)
    
    # Piso (grande, centrado, rojo)
    floor_text = font_floor.render(str(floor), True, RED)
    floor_rect = floor_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 130))
    surface.blit(floor_text, floor_rect)
    
    # HP (izquierda, fuera de la barra)
    hp_text = font_stats.render(f"HP: {knight.health}", True, WHITE)
    surface.blit(hp_text, (20, WINDOW_HEIGHT - 50))
    
    # SP (izquierda, fuera de la barra, arriba del HP)
    sp_text = font_stats.render(f"SP: {knight.shield}", True, WHITE)
    surface.blit(sp_text, (20, WINDOW_HEIGHT - 100))
    
    # AP (derecha abajo)
    ap_text = font_ap.render(f"AP: {knight.attack}", True, WHITE)
    surface.blit(ap_text, (WINDOW_WIDTH - 120, WINDOW_HEIGHT - 50))
    
    # Dibujar enemigos
    for enemy in enemies:
        enemy.draw(surface)
    
    for enemy2 in enemies2:
        enemy2.draw(surface)
    
    # Dibujar power-ups
    for heart_item in hearts:
        heart_item.draw(surface)
    
    for sword_item in swords:
        sword_item.draw(surface)

def draw_menu(surface):
    """Dibuja el menú"""
    surface.fill(BLACK)
    play_button.draw(surface)

def draw_game_over(surface):
    """Dibuja pantalla de derrota"""
    surface.fill(BLACK)
    font = get_font(80)
    text = font.render("GAME OVER", True, RED)
    text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
    surface.blit(text, text_rect)

def draw_win(surface):
    """Dibuja pantalla de victoria"""
    surface.fill(BLACK)
    font = get_font(80)
    text = font.render("¡GANASTE!", True, (0, 255, 0))
    text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
    surface.blit(text, text_rect)

# ==================== INPUT ====================
def handle_key_press(key):
    """Maneja entrada de teclado"""
    global game_state
    
    if game_state != GameState.GAME:
        return
    
    original_position = (knight.x, knight.y)
    new_x, new_y = knight.x, knight.y
    
    # Movimiento
    if key == pygame.K_RIGHT and knight.x + CELL_SIZE < WINDOW_WIDTH - CELL_SIZE:
        new_x += CELL_SIZE
        knight.set_image('knight')
    elif key == pygame.K_LEFT and knight.x - CELL_SIZE >= CELL_SIZE:
        new_x -= CELL_SIZE
        knight.set_image('left')
    elif key == pygame.K_DOWN and knight.y + CELL_SIZE < WINDOW_HEIGHT - CELL_SIZE:
        new_y += CELL_SIZE
    elif key == pygame.K_UP and knight.y - CELL_SIZE >= CELL_SIZE:
        new_y -= CELL_SIZE
    
    # Validar posición en mapa
    map_x = int(new_x // CELL_SIZE)
    map_y = int(new_y // CELL_SIZE)
    
    if (0 <= map_y < len(my_map) and 0 <= map_x < len(my_map[0]) and 
        my_map[map_y][map_x] != 0):
        knight.x, knight.y = new_x, new_y
    else:
        knight.x, knight.y = original_position
    
    # Colisión con enemigos grandes
    for i, enemy in enumerate(enemies):
        if knight.colliderect(enemy):
            knight.x, knight.y = original_position
            start_attack(i, enemies)
            break
    
    # Colisión con enemigos pequeños
    for i, enemy2 in enumerate(enemies2):
        if knight.colliderect(enemy2):
            knight.x, knight.y = original_position
            start_attack(i, enemies2)
            break
    
    check_power_ups()
    update_health_bar()
    update_shield_bar()

def handle_mouse_click(pos):
    """Maneja clics del ratón"""
    global game_state, chest
    
    if game_state == GameState.MENU and play_button.collidepoint(pos):
        game_state = GameState.GAME
    
    if game_state == GameState.GAME and chest and chest.collidepoint(pos):
        knight.health = 100
        knight.shield = 100
        chest = None

# ==================== LOOP PRINCIPAL ====================
def main():
    global is_attacking, game_state, attack_timer, current_attack_enemy_index, current_attack_enemy_list
    global animation_reset_timer, enemy_to_reset, enemy_to_reset_list, reset_image_name
    
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Warders")
    
    running = True
    
    while running:
        clock.tick(FPS)
        
        # Manejo de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                handle_key_press(event.key)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                handle_mouse_click(event.pos)
        
        # Timer de ataque
        if is_attacking:
            attack_timer += 1
            # Aproximadamente 0.2 segundos a 80 FPS = 16 frames
            if attack_timer >= 16:
                if current_attack_enemy_index >= 0 and current_attack_enemy_list:
                    apply_damage(current_attack_enemy_index, current_attack_enemy_list)
                attack_timer = 0
                current_attack_enemy_index = -1
                current_attack_enemy_list = None
        
        # Timer de reseteo de animación del enemigo
        if enemy_to_reset and enemy_to_reset in (enemies + enemies2):
            animation_reset_timer += 1
            # 0.4 segundos a 80 FPS = 32 frames
            if animation_reset_timer >= 32:
                if reset_image_name and enemy_to_reset in (enemies + enemies2):
                    enemy_to_reset.set_image(reset_image_name)
                animation_reset_timer = 0
                enemy_to_reset = None
                enemy_to_reset_list = None
                reset_image_name = None
        
        # Dibujar según estado
        if game_state == GameState.MENU:
            draw_menu(screen)
        elif game_state == GameState.GAME:
            draw_game(screen)
        elif game_state == GameState.GAME_OVER:
            draw_game_over(screen)
        elif game_state == GameState.WIN:
            draw_win(screen)
        
        pygame.display.flip()
    
    pygame.quit()

if __name__ == "__main__":
    main()
