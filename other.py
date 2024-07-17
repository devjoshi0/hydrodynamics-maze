import pygame
import numpy as np

# Constants
WIDTH, HEIGHT = 600, 800
NUM_PARTICLES = 100
RADIUS = 50
GRAVITY = np.array([0, 100])

K = 0.08  # Increase the repulsion constant
MIN_DISTANCE = 0.5 * RADIUS  # Decrease the minimum distance for collision
DAMPING = -0.001  # Damping factor to reduce bounciness

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

class Particle:
    def __init__(self, pos, vel):
        self.pos = np.array(pos, dtype=float)
        self.vel = np.array(vel, dtype=float)
        self.color = (0, 0, 255)  # Start as blue
        self.density = 0  # Particle density
        self.pressure = 0  # Particle pressure
        self.force = np.array([0, 0], dtype=float)  # Particle force

    def update(self, released, particles):
        if released:
            # Apply gravity
            self.vel += GRAVITY
        
        # Apply repulsion force from other particles
        for particle in particles:
            if particle != self:
                diff = self.pos - particle.pos
                dist = np.linalg.norm(diff)
                if dist < MIN_DISTANCE and dist != 0:
                    # Calculate repulsion force
                    repulsion = K * (MIN_DISTANCE - dist) / dist * diff
                    self.vel += repulsion
                    particle.vel -= repulsion**2

        self.pos += self.vel

        # Calculate density and pressure
        self.density = 0
        for particle in particles:
            if particle != self:
                diff = self.pos - particle.pos
                dist = np.linalg.norm(diff)
                if dist < MIN_DISTANCE and dist != 0:
                    self.density += (MIN_DISTANCE - dist) ** 2

        self.pressure = K * self.density

        # Calculate force
        self.force = np.array([0, 0], dtype=float)
        for particle in particles:
            if particle != self:
                diff = self.pos - particle.pos
                dist = np.linalg.norm(diff)
                if dist < MIN_DISTANCE and dist != 0:
                    # Calculate pressure force
                    pressure_force = -K * (MIN_DISTANCE - dist) / dist * diff
                    self.force += pressure_force**2

                    # Calculate viscosity force
                    viscosity_force = DAMPING * (particle.vel - self.vel)
                    self.force += viscosity_force

        self.vel += self.force

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
particles = []
for i in range(NUM_PARTICLES):
      # Add a delay of 100 milliseconds between each particle creation
    particles.append(Particle((np.random.rand() * WIDTH * 0.2, np.random.rand() * HEIGHT), (0, 0)))
   

running = True
released = False
start_time = pygame.time.get_ticks()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


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
