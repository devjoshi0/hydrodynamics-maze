import pygame
from pygame.locals import *
import math

pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAVITY = 0.5  # Gravity strength
PARTICLE_RADIUS = 5
PARTICLE_COLOR = (0, 0, 255)  # Blue color for water

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
        self.radius = PARTICLE_RADIUS
        self.color = PARTICLE_COLOR
        self.y_velocity = 0  # Initial velocity
        self.collided = False  # Flag to prevent multiple collisions per frame

    def update(self, particles):
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

        # Check for collisions with other particles
        for particle in particles:
            if particle is not self and not particle.collided:
                distance = math.sqrt((self.x - particle.x)**2 + (self.y - particle.y)**2)
                if distance <= self.radius + particle.radius:
                    # Collision detected
                    self.collide_with_particle(particle)
                    particle.collide_with_particle(self)
                    particle.collided = True

    def collide_with_particle(self, other):
        # Adjust velocities upon collision
        total_mass = math.pi * (self.radius**2) + math.pi * (other.radius**2)
        new_y_velocity = (self.y_velocity * (math.pi * (self.radius**2)) + other.y_velocity * (math.pi * (other.radius**2))) / total_mass

        # Update properties of current particle
        self.y_velocity = new_y_velocity

    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), int(self.radius))

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
clock = pygame.time.Clock()
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
        particle.update(particles)
        particle.collided = False  # Reset collided flag for the next frame

    # Drawing everything
    screen.fill(WHITE)
    draw_maze()  # Draw the maze first
    for particle in particles:
        particle.draw()  # Draw particles on top of the maze
    pygame.display.flip()

    clock.tick(60)  # Limit frame rate to 60 FPS

pygame.quit()
