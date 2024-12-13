import pygame
import random
import cairo
import time

# Pengaturan awal
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 400
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
SNAKE_COLOR = (0, 255, 0)
FOOD_COLOR = (255, 0, 0)
BIG_FOOD_COLOR = (255, 165, 0)
BACKGROUND_COLOR = (0, 0, 0)
TEXT_COLOR = (255, 255, 255)
FOOD_SCORE = 10
BIG_FOOD_SCORE = 30
BIG_FOOD_THRESHOLD = 3

# Inisialisasi pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# Fungsi untuk menampilkan teks di layar
def draw_text(surface, text, position, size=36):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, TEXT_COLOR)
    surface.blit(text_surface, position)

def draw_text_cairo(ctx, text, x, y, font_size=30, font_face="Sans", font_slant=cairo.FONT_SLANT_NORMAL, font_weight=cairo.FONT_WEIGHT_NORMAL):
    ctx.select_font_face(font_face, font_slant, font_weight)
    ctx.set_font_size(font_size)
    ctx.move_to(x, y)
    ctx.show_text(text)

# Fungsi animasi sebelum permainan
def start_animation():
    # Countdown
    for i in range(5, 0, -1):
        screen.fill(BACKGROUND_COLOR)
        draw_text(screen, f"Starting in {i}", (SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2), size=48)
        pygame.display.flip()
        time.sleep(1)
    
    # Animasi ular bergerak ke tengah layar
    snake_x = 0
    for step in range(GRID_WIDTH // 2):
        screen.fill(BACKGROUND_COLOR)
        pygame.draw.circle(screen, SNAKE_COLOR, (snake_x * GRID_SIZE + GRID_SIZE // 2, SCREEN_HEIGHT // 2), GRID_SIZE // 2)
        pygame.display.flip()
        snake_x += 1
        clock.tick(10)

    # Tampilkan teks untuk memulai permainan
    screen.fill(BACKGROUND_COLOR)
    draw_text(screen, "Press any key to start!", (SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2))
    pygame.display.flip()

    # Tunggu pemain menekan tombol
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                waiting = False

# Layar untuk memilih level
def choose_level():
    level = None
    pygame.display.set_caption("Choose Level")

    # Membuat surface PyCairo
    surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    cairo_surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, SCREEN_WIDTH, SCREEN_HEIGHT)
    ctx = cairo.Context(cairo_surface)

    # Menggambar latar belakang hitam
    ctx.set_source_rgb(0, 0, 0)  # Warna hitam
    ctx.paint()

    # Menggambar teks pilihan level
    ctx.set_source_rgb(1, 1, 1)  # Warna putih untuk teks
    draw_text_cairo(ctx, "Choose Level:", 100, 100, font_size=40, font_slant=cairo.FONT_SLANT_ITALIC)
    draw_text_cairo(ctx, "1. Easy", 100, 160)
    draw_text_cairo(ctx, "2. Medium", 100, 220)
    draw_text_cairo(ctx, "3. Hard", 100, 280)
    draw_text_cairo(ctx, "4. Exit", 100, 340)

    # Menggambar garis kotak di sekitar pilihan level
    ctx.set_source_rgb(1, 1, 1)  # Warna putih untuk garis kotak
    ctx.set_line_width(2)  # Ketebalan garis

    # Menggambar kotak di sekitar setiap opsi level
    ctx.rectangle(90, 130, 200, 40)   # Kotak untuk "1. Easy"
    ctx.rectangle(90, 190, 240, 40)   # Kotak untuk "2. Medium"
    ctx.rectangle(90, 250, 200, 40)   # Kotak untuk "3. Hard"
    ctx.rectangle(90, 310, 200, 40)   # Kotak untuk "4. Exit"
    ctx.stroke()  # Menampilkan garis kotak

 

    # Menyalin PyCairo ke Pygame Surface
    data = cairo_surface.get_data()
    pygame_surface = pygame.image.frombuffer(data, (SCREEN_WIDTH, SCREEN_HEIGHT), "ARGB")
    surface.blit(pygame_surface, (0, 0))

    # Menampilkan surface ke layar
    screen.blit(surface, (0, 0))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    level = 'Easy'
                    waiting = False
                elif event.key == pygame.K_2:
                    level = 'Medium'
                    waiting = False
                elif event.key == pygame.K_3:
                    level = 'Hard'
                    waiting = False
                elif event.key == pygame.K_4:
                    pygame.quit()
                    quit()
    return level



# Menu setelah game over
def game_over_menu(score, high_score):
    # Membuat surface PyCairo berdasarkan buffer Pygame
    cairo_surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, SCREEN_WIDTH, SCREEN_HEIGHT)
    ctx = cairo.Context(cairo_surface)

    # Mengisi background dengan warna hitam
    ctx.set_source_rgb(0, 0, 0)
    ctx.paint()

    # Menggambar teks Game Over dan informasi skor
    ctx.set_source_rgb(1, 1, 1)  # Warna putih untuk teks
    draw_text_cairo(ctx, f"Game Over! Score: {score}", SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 - 60)
    draw_text_cairo(ctx, f"High Score: {high_score}", SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 - 20)
    draw_text_cairo(ctx, "1. Restart Game", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 40)
    draw_text_cairo(ctx, "2. Main Menu", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 80)

    # Konversi surface PyCairo ke surface Pygame
    data = cairo_surface.get_data()
    pygame_surface = pygame.image.frombuffer(data, (SCREEN_WIDTH, SCREEN_HEIGHT), "ARGB")

    # Blit surface ke layar
    screen.blit(pygame_surface, (0, 0))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return "restart"
                elif event.key == pygame.K_2:
                    return "menu"


# Ular dan makanan
class Snake:
    def __init__(self):
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = (0, -1)
        self.grow = False

    def update(self):
        head_x, head_y = self.positions[0]
        dir_x, dir_y = self.direction
        new_head = (head_x + dir_x, head_y + dir_y)

        if (
            new_head[0] < 0 or new_head[0] >= GRID_WIDTH or
            new_head[1] < 0 or new_head[1] >= GRID_HEIGHT or
            new_head in self.positions
        ):
            return False

        self.positions.insert(0, new_head)
        if not self.grow:
            self.positions.pop()
        self.grow = False
        return True

    def change_direction(self, dir_x, dir_y):
        if (dir_x, dir_y) != (-self.direction[0], -self.direction[1]):
            self.direction = (dir_x, dir_y)

    def eat(self):
        self.grow = True

    def draw(self, surface):
        for i, (x, y) in enumerate(self.positions):
            radius = GRID_SIZE // 2
            pygame.draw.circle(surface, SNAKE_COLOR, (x * GRID_SIZE + radius, y * GRID_SIZE + radius), radius)

class Food:
    def __init__(self):
        self.position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
        self.big_food = False

    def respawn(self, big_food=False):
        self.position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
        self.big_food = big_food

    def draw(self, surface):
        x, y = self.position
        color = BIG_FOOD_COLOR if self.big_food else FOOD_COLOR
        radius = GRID_SIZE // 2 if not self.big_food else GRID_SIZE
        pygame.draw.circle(surface, color, (x * GRID_SIZE + radius, y * GRID_SIZE + radius), radius)


# Inisialisasi permainan
snake = Snake()
food = Food()
score = 0
high_score = 0
food_count = 0

# Pilih level
level = choose_level()
if level == 'Easy':
    game_speed = 5
elif level == 'Medium':
    game_speed = 10
else:
    game_speed = 15

# Jalankan animasi sebelum permainan dimulai
start_animation()

# Game loop
running = True
while running:
    screen.fill(BACKGROUND_COLOR)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.change_direction(0, -1)
            elif event.key == pygame.K_DOWN:
                snake.change_direction(0, 1)
            elif event.key == pygame.K_LEFT:
                snake.change_direction(-1, 0)
            elif event.key == pygame.K_RIGHT:
                snake.change_direction(1, 0)

    if not snake.update():
        high_score = max(high_score, score)
        choice = game_over_menu(score, high_score)
        if choice == "restart":
            snake = Snake()
            food = Food()
            score = 0
            food_count = 0
        elif choice == "menu":
            level = choose_level()
            if level == 'Easy':
                game_speed = 5
            elif level == 'Medium':
                game_speed = 10
            else:
                game_speed = 15
            snake = Snake()
            food = Food()
            score = 0
            food_count = 0

    elif snake.positions[0] == food.position:
        snake.eat()
        score += BIG_FOOD_SCORE if food.big_food else FOOD_SCORE
        food_count = 0 if food.big_food else food_count + 1
        food.respawn(big_food=(food_count >= BIG_FOOD_THRESHOLD))

    snake.draw(screen)
    food.draw(screen)

    draw_text(screen, f"Score: {score}", (10, 10))
    draw_text(screen, f"High Score: {high_score}", (SCREEN_WIDTH - 150, 10))
    pygame.display.flip()
    clock.tick(game_speed)

pygame.quit()
