import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
MAZE_SIZE = 21  # This will make a 21x21 grid to ensure odd dimensions
GRID_SIZE = 20
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Set up display
win = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Random Maze Generator")

# Button setup
EASY_BUTTON = pygame.Rect(50, WINDOW_HEIGHT - 50, 100, 40)
MEDIUM_BUTTON = pygame.Rect(200, WINDOW_HEIGHT - 50, 100, 40)
HARD_BUTTON = pygame.Rect(350, WINDOW_HEIGHT - 50, 100, 40)

# Font
font = pygame.font.SysFont('Arial', 20)

def draw_button(win, button, text):
    pygame.draw.rect(win, WHITE, button)
    label = font.render(text, True, BLACK)
    win.blit(label, (button.x + (button.width - label.get_width()) // 2,
                     button.y + (button.height - label.get_height()) // 2))

def generate_maze(size, complexity):
    maze = [[1 for _ in range(size)] for _ in range(size)]
    
    def create_path(x, y):
        maze[y][x] = 0
        directions = [(2, 0), (-2, 0), (0, 2), (0, -2)]
        random.shuffle(directions)
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < size and 0 <= ny < size and maze[ny][nx] == 1:
                maze[ny][nx] = 0
                maze[y + dy // 2][x + dx // 2] = 0
                create_path(nx, ny)

    def create_guaranteed_path():
        x, y = 1, 1
        maze[y][x] = 0
        while y < size - 2:
            if x < size - 2 and random.choice([True, False]):
                x += 2
            else:
                y += 2
            maze[y][x] = 0
            maze[y - 1][x] = 0

        # Make sure there's a final connection to the bottom row
        if x != size - 2:
            maze[size - 2][x] = 0
            maze[size - 2][x + 1] = 0
            maze[size - 2][x + 2] = 0

    create_guaranteed_path()
    create_path(1, 1)

    # Enclose the maze with walls except for the entrance and exit
    for i in range(size):
        maze[i][0] = 1
        maze[i][size-1] = 1
        maze[0][i] = 1
        maze[size-1][i] = 1

    maze[0][1] = 0  # Entrance
    maze[size-1][size-2] = 0  # Exit

    return maze

def draw_maze(win, maze, offset_x, offset_y):
    for y in range(len(maze)):
        for x in range(len(maze[0])):
            color = WHITE if maze[y][x] == 1 else BLACK
            pygame.draw.rect(win, color, (offset_x + x * GRID_SIZE, offset_y + y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

def main():
    run = True
    maze = generate_maze(MAZE_SIZE, 0)
    offset_x = (WINDOW_WIDTH - MAZE_SIZE * GRID_SIZE) // 2
    offset_y = (WINDOW_HEIGHT - MAZE_SIZE * GRID_SIZE) // 2
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if EASY_BUTTON.collidepoint(event.pos):
                    maze = generate_maze(MAZE_SIZE, 0)
                if MEDIUM_BUTTON.collidepoint(event.pos):
                    maze = generate_maze(MAZE_SIZE, 1)
                if HARD_BUTTON.collidepoint(event.pos):
                    maze = generate_maze(MAZE_SIZE, 2)

        win.fill(BLACK)
        
        draw_button(win, EASY_BUTTON, "Easy")
        draw_button(win, MEDIUM_BUTTON, "Medium")
        draw_button(win, HARD_BUTTON, "Hard")
        draw_maze(win, maze, offset_x, offset_y)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
