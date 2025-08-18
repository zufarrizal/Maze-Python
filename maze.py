import pygame
import random
import time
import tkinter as tk
from tkinter import messagebox

# Konfigurasi
MAZE_SIZE = 50
WIDTH, HEIGHT = 800, 860
TILE = 800 // MAZE_SIZE
ROWS, COLS = MAZE_SIZE, MAZE_SIZE

# Warna elegan
BG_COLOR = (245, 245, 250)
WALL_COLOR = (180, 180, 200)
PATH_COLOR = (255, 255, 255)
PLAYER_COLOR = (100, 149, 237)
GOAL_COLOR = (144, 238, 144)
TIMER_BG = (230, 230, 240)
TIMER_BORDER = (160, 160, 180)
TEXT_COLOR = (50, 50, 70)
BUTTON_COLOR = (220, 220, 235)
BUTTON_BORDER = (160, 160, 180)

# Inisialisasi
pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Elegan 50x50")

maze = [[1 for _ in range(COLS)] for _ in range(ROWS)]

def generate_maze(x=0, y=0):
    maze[y][x] = 0
    directions = [(0,-2), (0,2), (-2,0), (2,0)]
    random.shuffle(directions)
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < COLS and 0 <= ny < ROWS and maze[ny][nx] == 1:
            maze[y + dy//2][x + dx//2] = 0
            generate_maze(nx, ny)

def draw_maze():
    for y in range(ROWS):
        for x in range(COLS):
            rect = pygame.Rect(x*TILE, y*TILE + 60, TILE, TILE)
            color = PATH_COLOR if maze[y][x] == 0 else WALL_COLOR
            pygame.draw.rect(WIN, color, rect, border_radius=3)
    pygame.draw.rect(WIN, PLAYER_COLOR, (player[0]*TILE, player[1]*TILE + 60, TILE, TILE), border_radius=5)
    pygame.draw.rect(WIN, GOAL_COLOR, (goal[0]*TILE, goal[1]*TILE + 60, TILE, TILE), border_radius=5)

def draw_start_button():
    font = pygame.font.SysFont("Segoe UI", 40)
    text = font.render("START", True, TEXT_COLOR)
    button_rect = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 - 40, 200, 80)
    pygame.draw.rect(WIN, BUTTON_COLOR, button_rect, border_radius=12)
    pygame.draw.rect(WIN, BUTTON_BORDER, button_rect, 2, border_radius=12)
    WIN.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2))
    return button_rect

def draw_timer_box(elapsed):
    box_width, box_height = 220, 45
    box_x = WIDTH // 2 - box_width // 2
    box_y = 10
    pygame.draw.rect(WIN, TIMER_BG, (box_x, box_y, box_width, box_height), border_radius=10)
    pygame.draw.rect(WIN, TIMER_BORDER, (box_x, box_y, box_width, box_height), 2, border_radius=10)

    font = pygame.font.SysFont("Segoe UI", 28, bold=True)
    timer_text = font.render(f"⏱️ Time: {elapsed:.2f}s", True, TEXT_COLOR)
    WIN.blit(timer_text, (WIDTH//2 - timer_text.get_width()//2, box_y + 8))

def show_win_popup(duration):
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo("🎉 Selamat!", f"Kamu menang!\nDurasi: {duration:.2f} detik")
    root.destroy()

# Game state
player = [0, 0]
goal = [COLS - 1, ROWS - 1]
start_game = False
start_time = None

# Generate maze dan validasi goal
generate_maze()
if maze[goal[1]][goal[0]] == 1:
    for y in reversed(range(ROWS)):
        for x in reversed(range(COLS)):
            if maze[y][x] == 0:
                goal = [x, y]
                break
        else:
            continue
        break

# Game loop
clock = pygame.time.Clock()
run = True
while run:
    clock.tick(60)
    WIN.fill(BG_COLOR)

    if not start_game:
        button_rect = draw_start_button()
    else:
        draw_maze()
        elapsed = time.time() - start_time
        draw_timer_box(elapsed)

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if not start_game and event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos):
                start_game = True
                start_time = time.time()

    if start_game:
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[pygame.K_LEFT]: dx = -1
        if keys[pygame.K_RIGHT]: dx = 1
        if keys[pygame.K_UP]: dy = -1
        if keys[pygame.K_DOWN]: dy = 1

        nx, ny = player[0] + dx, player[1] + dy
        if 0 <= nx < COLS and 0 <= ny < ROWS and maze[ny][nx] == 0:
            player = [nx, ny]

        if player == goal:
            duration = time.time() - start_time
            show_win_popup(duration)
            run = False

pygame.quit()
