import pygame
import numpy as np
from math import sqrt
from pythonsph.config import Config
# Constants
WIDTH, HEIGHT = 800, 600
NUM_PARTICLES = 550
RADIUS = 30
GRAVITY = np.array([0, 0.1])
RELEASE_TIME = 3  # Time in seconds after which the dam breaks
K = 0.005  # Repulsion constant
MIN_DISTANCE = 2 * RADIUS  # Minimum distance for collision
DAMPING = -0.3  # Damping factor to reduce bounciness

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

class Particle:
    def __init__(self, x_pos: float, y_pos: float):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.vel = np.array(vel, dtype=float)
        self.color = (0, 0, 255)  # Start as blue

    def update(self, released, particles):
        if released:
            # Apply gravity
            self.vel += GRAVITY
        
        # Apply repulsion force from other particles
        for particle in particles:
            if particle != self:
                diff = self.pos - particle.pos
                dist = np.linalg.norm(diff)
                if dist < MIN_DISTANCE:
                    # Calculate repulsion force
                    repulsion = K * (MIN_DISTANCE - dist) / dist * diff
                    self.vel += repulsion
                    # Add upward force to mimic water behavior
                    if self.pos[1] > particle.pos[1]:
                        self.vel[1] -= K * (MIN_DISTANCE - dist) / dist

        self.pos += self.vel

        # Boundary conditions
        if self.pos[0] <= RADIUS or self.pos[0] >= WIDTH - RADIUS:
            self.vel[0] *= DAMPING  # Apply damping
            self.pos[0] = np.clip(self.pos[0], RADIUS, WIDTH - RADIUS)

        if self.pos[1] >= HEIGHT - RADIUS:
            self.vel[1] *= DAMPING  # Apply damping
            self.pos[1] = HEIGHT - RADIUS

        # Change color based on velocity (speed)
        speed = np.linalg.norm(self.vel)
        color_intensity = min(255, int(np.nan_to_num(speed) * 10))
        self.color = (color_intensity, 0, 255 - color_intensity)

# Initialize particles on the left side of the screen
particles = [Particle((np.random.rand() * WIDTH * 0.2, np.random.rand() * HEIGHT), (0, 0)) for _ in range(NUM_PARTICLES)]

running = True
released = False
start_time = pygame.time.get_ticks()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Check if it's time to release the particles
    current_time = pygame.time.get_ticks()
    if (current_time - start_time) / 1000 >= RELEASE_TIME:
        released = True

    # Update particles
    for particle in particles:
        particle.update(released, particles)

    # Draw
    screen.fill((0, 0, 0))
    for particle in particles:
        pygame.draw.circle(screen, particle.color, particle.pos.astype(int), RADIUS)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
