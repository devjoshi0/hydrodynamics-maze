import pygame
from pygame.locals import *
import numpy as np
from sph_simulation import (
    add_particles, calculate_densities, calculate_forces,
    enforce_boundary_conditions, draw_particles, SMOOTHING_LENGTH, ISOTROPIC_EXPONENT,
    BASE_DENSITY, CONSTANT_FORCE, TIME_STEP_LENGTH, MAX_PARTICLES
)
from sklearn import neighbors

pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PARTICLE_RADIUS = 5  # To match the radius in the SPH simulation

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Water Particle Simulation with Maze')

# Example maze structure (2D array)
maze = [
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]




]


# Define block size and maze dimensions
block_size = 15
maze_width = len(maze[0])
maze_height = len(maze)

# Calculate the offset to center the maze on the screen
maze_offset_x = (SCREEN_WIDTH - maze_width * block_size) // 2
maze_offset_y = (SCREEN_HEIGHT - maze_height * block_size) // 2

# Create a list to store wall rectangles
walls = []

# Initialize wall rectangles
for y in range(maze_height):
    for x in range(maze_width):
        if maze[y][x] == 1:
            rect = pygame.Rect(maze_offset_x + x * block_size, maze_offset_y + y * block_size, block_size, block_size)
            walls.append(rect)

# Function to draw the maze
def draw_maze():
    for wall in walls:
        pygame.draw.rect(screen, BLACK, wall)

# Function to check particle-maze collisions using Pygame's collision system
def enforce_maze_boundary_conditions(positions, velocities):
    for i in range(len(positions)):
        particle_rect = pygame.Rect(positions[i][0] - PARTICLE_RADIUS, positions[i][1] - PARTICLE_RADIUS, PARTICLE_RADIUS * 2, PARTICLE_RADIUS * 2)
        
        for wall in walls:
            if particle_rect.colliderect(wall):
                overlap_x = min(wall.right - particle_rect.left, particle_rect.right - wall.left)
                overlap_y = min(wall.bottom - particle_rect.top, particle_rect.bottom - wall.top)

                if overlap_x < overlap_y:
                    # Horizontal collision
                    if particle_rect.centerx < wall.centerx:
                        positions[i][0] = wall.left - PARTICLE_RADIUS
                    else:
                        positions[i][0] = wall.right + PARTICLE_RADIUS
                    velocities[i][0] *= -0.5  # Bounce back horizontally, reduce speed

                else:
                    # Vertical collision
                    if particle_rect.centery < wall.centery:
                        positions[i][1] = wall.top - PARTICLE_RADIUS
                    else:
                        positions[i][1] = wall.bottom + PARTICLE_RADIUS
                    velocities[i][1] *= -0.5  # Bounce back vertically, reduce speed

    return positions, velocities


# Initialize SPH simulation variables
n_particles = 1
positions = np.ones((n_particles, 2))
velocities = np.zeros_like(positions)
forces = np.zeros_like(positions)

# Main game loop
running = True
mouse_pressed = False
clock = pygame.time.Clock()
iter_count = 0

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    # Update the SPH simulation
    if iter_count % 50 == 0 and n_particles < MAX_PARTICLES:
        positions, velocities, n_particles = add_particles(positions, velocities, n_particles)

    neighbor_ids, distances = neighbors.KDTree(
        positions,
    ).query_radius(
        positions,
        SMOOTHING_LENGTH,
        return_distance=True,
        sort_results=True,
    )

    densities = calculate_densities(positions, neighbor_ids, distances)
    pressures = ISOTROPIC_EXPONENT * (densities - BASE_DENSITY)

    forces = calculate_forces(positions, velocities, neighbor_ids, distances, densities, pressures)

    # Force due to gravity
    forces += CONSTANT_FORCE

    velocities = velocities + TIME_STEP_LENGTH * forces / densities[:, np.newaxis]
    positions = positions + TIME_STEP_LENGTH * velocities

    positions, velocities = enforce_boundary_conditions(positions, velocities)
    positions, velocities = enforce_maze_boundary_conditions(positions, velocities)

    # Drawing everything
    screen.fill(WHITE)
    draw_maze()  # Draw the maze first
    draw_particles(screen, positions)  # Draw the particles
    pygame.display.flip()
    clock.tick(60)
    iter_count += 1

pygame.quit()
