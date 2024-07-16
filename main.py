import pygame
from pygame.locals import *

pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAVITY = 0.5  # Gravity strength

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Water Particle Simulation with Maze')

# Example maze structure (2D array)
maze = [
    [1, 0, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1, 1, 0, 1],
    [1, 0, 1, 0, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 1, 0, 1, 1],
    [1, 0, 0, 0, 1, 0, 1, 1],
    [1, 0, 0, 0, 1, 0, 1, 1],
    [1, 1, 1, 1, 1, 0, 1, 1]
]

# Define block size and maze dimensions
block_size = 30
maze_width = len(maze[0])
maze_height = len(maze)

# Calculate the offset to center the maze on the screen
maze_offset_x = (SCREEN_WIDTH - maze_width * block_size) // 2
maze_offset_y = (SCREEN_HEIGHT - maze_height * block_size) // 2

class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 2
        self.color = (0, 0, 255)  # Blue color for water
        self.y_velocity = 0  # Initial velocity

    def update(self):
        # Apply gravity
        self.y_velocity += GRAVITY
        self.y += self.y_velocity

        # Check for collisions with maze walls
        for y in range(maze_height):
            for x in range(maze_width):
                if maze[y][x] == 1:
                    wall_rect = pygame.Rect(maze_offset_x + x * block_size, maze_offset_y + y * block_size, block_size, block_size)
                    if wall_rect.collidepoint(self.x, self.y):
                        # Particle hits the wall, adjust its position
                        if self.y_velocity > 0:  # Moving downward
                            self.y = wall_rect.top - self.radius
                            self.y_velocity = 0  # Stop downward movement

    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

particles = []

# Function to draw the maze
def draw_maze():
    for y in range(maze_height):
        for x in range(maze_width):
            if maze[y][x] == 1:
                rect = pygame.Rect(maze_offset_x + x * block_size, maze_offset_y + y * block_size, block_size, block_size)
                pygame.draw.rect(screen, BLACK, rect)

# Main game loop
running = True
mouse_pressed = False
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == MOUSEBUTTONDOWN and event.button == 1:
            mouse_pressed = True
        elif event.type == MOUSEBUTTONUP and event.button == 1:
            mouse_pressed = False

    # Continuous particle spawning while mouse button is held down
    if mouse_pressed:
        mouse_pos = pygame.mouse.get_pos()
        particle = Particle(mouse_pos[0], mouse_pos[1])
        particles.append(particle)

    # Update particles
    for particle in particles:
        particle.update()

    # Drawing everything
    screen.fill(WHITE)
    draw_maze()  # Draw the maze first
    for particle in particles:
        particle.draw()  # Draw particles on top of the maze
    pygame.display.flip()

pygame.quit()
