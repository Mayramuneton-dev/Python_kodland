import pygame
import random
import math

# Inicialización de PyGame
pygame.init()

# Configuración de la pantalla
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Aventura de Caza")

# Configuración de FPS
clock = pygame.time.Clock()

# Cargar y redimensionar las imagenes
hunterImg = pygame.image.load('Cazador.png')
hunterImg = pygame.transform.scale(hunterImg, (150, 150))
bulletImg = pygame.image.load('bala.png')
bulletImg = pygame.transform.scale(bulletImg, (10, 15))
BirdImg = []
for i in range(6):
    img = pygame.image.load('Pajaro.png')
    img = pygame.transform.scale(img, (40, 40))
    BirdImg.append(img)

# Posición inicial del cazador
hunterX = (screen.get_width() - hunterImg.get_width()) // 2
hunterY = screen.get_height() - hunterImg.get_height() - 20
hunterX_change = 0

# Cargar fondos del juego tanto para el menu y el juego
try:
    background = pygame.image.load('fondo.png')
    background = pygame.transform.scale(background, (screen.get_width(), screen.get_height()))
    background = background.convert()
except Exception:
    background = None
try:
    menu_background = pygame.image.load('fondomenu.png')
    menu_background = pygame.transform.scale(menu_background, (screen.get_width(), screen.get_height()))
    menu_background = menu_background.convert()
except Exception:
    menu_background = None

# Posición inicial del Pajaro
BirdX = []
BirdY = []
BirdX_change = []
BirdY_change = []
num_of_birds = 6

# Inicializar posiciones de los pájaros 
for i in range(num_of_birds):
    BirdX.append(random.randint(0, 736))
    BirdY.append(random.randint(50, 150))
    BirdX_change.append(2)
    BirdY_change.append(40)

# Estado inicial de la bala
bulletX = 0
bulletY = hunterY
bulletY_change = 5
bullet_state = "ready"  

# Función para el cazador
def hunter(x, y):
    screen.blit(hunterImg, (x, y))

# Función para disparar
def fire_bullet(x, y):
    global bullet_state, bulletX, bulletY
    bullet_state = "fire"
    screen.blit(bulletImg, (x, y - bulletImg.get_height()))

# Función para los pájaros
def Bird(x, y, i):
    screen.blit(BirdImg[i], (x, y))

# Función para detectar colisiones
def isCollision(BirdX, BirdY, bulletX, bulletY):
    distance = math.sqrt(math.pow(BirdX - bulletX, 2) + math.pow(BirdY - bulletY, 2))
    return distance < 27

# Función para detectar colisión entre pájaro y cazador
def isCollisionhunter(bX, bY, pX, pY, bird_index=0):
    if BirdImg[bird_index]:
        bw = BirdImg[bird_index].get_width()
        bh = BirdImg[bird_index].get_height()
    else:
        bw = 50
        bh = 50
    pw = hunterImg.get_width()
    ph = hunterImg.get_height()

    bird_cx = bX + bw / 2
    bird_cy = bY + bh / 2
    hunter_cx = pX + pw / 2
    hunter_cy = pY + ph / 2

    distance = math.hypot(bird_cx - hunter_cx, bird_cy - hunter_cy)
    # umbral proporcional a tamaños 
    threshold = (pw + bw) / 2
    return distance < threshold

# Función para el menú
def game_menu():
    menu_running = True
    while menu_running:
        if menu_background:
            screen.blit(menu_background, (0, 0))
        elif background:
            screen.blit(background, (0, 0))
        else:
            screen.fill((0, 0, 0)) 
        
        show_text("Pulsa 1 iniciar ", 40, 460)
        show_text("Pulsa 2 instrucciones de caza", 40, 500)
        show_text("Pulsa x salir del juego", 40, 540)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu_running = False
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    menu_running = False 
                if event.key == pygame.K_2:
                    instructions()
                if event.key == pygame.K_x:
                    menu_running = False
                    pygame.quit()
                    quit()

# Función para mostrar texto en pantalla
def show_text(text, x, y):
    font = pygame.font.Font('freesansbold.ttf', 18)
    rendered_text = font.render(text, True, (255, 255, 255))
    screen.blit(rendered_text, (x, y))

# Función para mostrar instrucciones
def instructions():
    instructions_running = True
    while instructions_running:
        if background:
            screen.blit(background, (0, 0))
        else:
            screen.fill((0, 0, 0)) 
        
        show_text("Instrucciones:", 340, 230)
        show_text("Usa las flechas para desplazarte", 260, 300)
        show_text("Pulsa espacio para disparar", 280, 340)
        show_text("Pulsa z para retroceder", 300, 380)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                instructions_running = False
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:
                    instructions_running = False

# Función Game Over 
def show_game_over():
    font = pygame.font.Font('freesansbold.ttf', 64)
    if background:
        screen.blit(background, (0, 0))
    else:
        screen.fill((0, 0, 0))
    text = font.render("GAME OVER", True, (255, 0, 0))
    screen.blit(text, (screen.get_width()//2 - text.get_width()//2, 200))
    pygame.display.update()
    pygame.time.wait(1500)
    return

# Bucle principal del juego
if __name__ == "__main__":
    game_menu()  # Muestra el menú al iniciar

    running = True
    while running:
        if background:
            screen.blit(background, (0, 0))
        else:
            screen.fill((0, 0, 0)) 
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Controles del cazador
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    hunterX_change = -3
                if event.key == pygame.K_RIGHT:
                    hunterX_change = 3
                if event.key == pygame.K_SPACE:
                    if bullet_state == "ready":
                        bulletX = hunterX + hunterImg.get_width() // 2 - bulletImg.get_width() // 2
                        bulletY = hunterY
                        fire_bullet(bulletX, bulletY)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    hunterX_change = 0

        # Actualizar la posición del cazador
        hunterX += hunterX_change
        if hunterX <= 0:
            hunterX = 0
        elif hunterX >= screen.get_width() - hunterImg.get_width():
            hunterX = screen.get_width() - hunterImg.get_width()

        # Movimiento del pajaro
        for i in range(num_of_birds):
            BirdX[i] += BirdX_change[i]
            if BirdX[i] <= 0:
                BirdX_change[i] = 2
                BirdY[i] += BirdY_change[i]
            elif BirdX[i] >= 736:
                BirdX_change[i] = -2
                BirdY[i] += BirdY_change[i]

            # Detectar colisión
            collision = isCollision(BirdX[i], BirdY[i], bulletX, bulletY)
            if collision:
                bulletY = hunterY
                bullet_state = "ready"
                BirdX[i] = random.randint(0, 736)
                BirdY[i] = random.randint(50, 150)

            # Detectar colisión entre pájaro y cazador
            if isCollisionhunter(BirdX[i], BirdY[i], hunterX, hunterY, i):
                show_game_over()
                running = False
            Bird(BirdX[i], BirdY[i], i)

        # Movimiento de la bala
        if bullet_state == "fire":
            fire_bullet(bulletX, bulletY)
            bulletY -= bulletY_change

        if bulletY <= 0:
            bulletY = hunterY
            bullet_state = "ready"

        hunter(hunterX, hunterY)
        pygame.display.update()
        clock.tick(60)  # Controlar la tasa de fotogramas
