import pygame
import random

# Initialize Pygame
pygame.init()

# Game constants
CELL_SIZE = 30
COLS, ROWS = 10, 20
PREVIEW_WIDTH = 6 * CELL_SIZE  # Extra width for next piece preview and score
WIDTH, HEIGHT = CELL_SIZE * COLS, CELL_SIZE * ROWS
SCREEN_WIDTH = WIDTH + PREVIEW_WIDTH
FPS = 60
BOUJEE_BG = (24, 24, 36)  # Elegant dark background

# Define primary colors for tetrominoes
COLORS = [
    (255, 0, 0),     # Red
    (0, 255, 0),     # Green
    (0, 0, 255),     # Blue
    (255, 255, 0),   # Yellow
    (255, 0, 255),   # Magenta
    (0, 255, 255),   # Cyan
    (255, 255, 255), # White
]

# Tetromino shapes
SHAPES = [
    [[1, 1, 1, 1]],                  # I
    [[1, 1], [1, 1]],                # O
    [[0, 1, 0], [1, 1, 1]],          # T
    [[1, 1, 0], [0, 1, 1]],          # S
    [[0, 1, 1], [1, 1, 0]],          # Z
    [[1, 0, 0], [1, 1, 1]],          # J
    [[0, 0, 1], [1, 1, 1]],          # L
]

# Tetromino class
class Tetromino:
    def __init__(self, x, y, shape, color):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = color
        self.rotation = 0

    @property
    def blocks(self):
        shape = self.shape
        for _ in range(self.rotation % 4):
            # Rotate shape 90 degrees
            shape = [list(row) for row in zip(*shape[::-1])]
        return shape

    def get_cells(self):
        cells = []
        for i, row in enumerate(self.blocks):
            for j, val in enumerate(row):
                if val:
                    cells.append((self.x + j, self.y + i))
        return cells

# Functions
def create_grid(locked):
    grid = [[None for _ in range(COLS)] for _ in range(ROWS)]
    for y in range(ROWS):
        for x in range(COLS):
            if (x, y) in locked:
                grid[y][x] = locked[(x, y)]
    return grid

def valid_space(tetromino, grid):
    for x, y in tetromino.get_cells():
        if x < 0 or x >= COLS or y >= ROWS:
            return False
        if y >= 0 and grid[y][x]:
            return False
    return True

def clear_rows(grid, locked):
    cleared = 0
    for y in range(ROWS-1, -1, -1):
        if all(grid[y][x] for x in range(COLS)):
            cleared += 1
            for x in range(COLS):
                del locked[(x, y)]
            for yy in range(y-1, -1, -1):
                for x in range(COLS):
                    if (x, yy) in locked:
                        locked[(x, yy+1)] = locked.pop((x, yy))
    return cleared

def draw_grid(surface, grid):
    # Draw grid cells
    for y in range(ROWS):
        for x in range(COLS):
            color = grid[y][x]
            rect = pygame.Rect(x*CELL_SIZE, y*CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if color:
                pygame.draw.rect(surface, color, rect, border_radius=8)
                pygame.draw.rect(surface, (255,255,255,30), rect, 2, border_radius=8)
            else:
                pygame.draw.rect(surface, (40, 40, 60), rect, 1)

def draw_tetromino(surface, tetromino):
    for x, y in tetromino.get_cells():
        if y >= 0:
            rect = pygame.Rect(x*CELL_SIZE, y*CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(surface, tetromino.color, rect, border_radius=8)
            pygame.draw.rect(surface, (255,255,255,50), rect, 2, border_radius=8)

def draw_boujee_overlay(surface):
    # Add a subtle gradient overlay for a luxurious feel
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    for y in range(HEIGHT):
        alpha = int(80 * (y / HEIGHT))
        pygame.draw.line(overlay, (255, 215, 0, alpha), (0, y), (WIDTH, y))
    surface.blit(overlay, (0, 0))

def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, HEIGHT))
    pygame.display.set_caption("Boujee Tetris")
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.35

    locked = {}
    grid = create_grid(locked)
    change_piece = False
    run = True

    current = Tetromino(3, -2, random.choice(SHAPES), random.choice(COLORS))
    next_piece = Tetromino(3, -2, random.choice(SHAPES), random.choice(COLORS))

    score = 0

    while run:
        grid = create_grid(locked)
        fall_time += clock.get_rawtime() / 1000
        clock.tick(FPS)

        # Piece falling
        if fall_time > fall_speed:
            current.y += 1
            if not valid_space(current, grid):
                current.y -= 1
                change_piece = True
            fall_time = 0

        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current.x -= 1
                    if not valid_space(current, grid):
                        current.x += 1
                elif event.key == pygame.K_RIGHT:
                    current.x += 1
                    if not valid_space(current, grid):
                        current.x -= 1
                elif event.key == pygame.K_DOWN:
                    current.y += 1
                    if not valid_space(current, grid):
                        current.y -= 1
                elif event.key == pygame.K_UP:
                    current.rotation += 1
                    if not valid_space(current, grid):
                        current.rotation -= 1

        # Lock piece if needed
        if change_piece:
            for x, y in current.get_cells():
                if y < 0:
                    run = False  # Game over
                else:
                    locked[(x, y)] = current.color
            current = next_piece
            next_piece = Tetromino(3, -2, random.choice(SHAPES), random.choice(COLORS))
            change_piece = False
            score += clear_rows(grid, locked) * 100

        # Draw everything
        screen.fill(BOUJEE_BG)
        draw_grid(screen, grid)
        draw_tetromino(screen, current)
        draw_boujee_overlay(screen)

        # Draw next piece preview
        font = pygame.font.SysFont("arial", 20, bold=True)
        label = font.render("Next", True, (255, 255, 255))
        screen.blit(label, (WIDTH + 10, 30))
        for i, row in enumerate(next_piece.shape):
            for j, val in enumerate(row):
                if val:
                    rect = pygame.Rect(WIDTH + 10 + j*CELL_SIZE, 60 + i*CELL_SIZE, CELL_SIZE, CELL_SIZE)
                    pygame.draw.rect(screen, next_piece.color, rect, border_radius=8)
                    pygame.draw.rect(screen, (255,255,255,50), rect, 2, border_radius=8)

        # Draw score
        score_label = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_label, (WIDTH + 10, 200))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
    #ferfdv