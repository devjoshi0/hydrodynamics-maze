import pygame
import numpy as np
import sys

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("SPH Water Simulation (Side View)")

# Define colors
background_color = (0, 0, 0)
particle_color = (0, 162, 232)

# Set up the clock for managing the frame rate
clock = pygame.time.Clock()

# SPH Parameters
NUM_PARTICLES = 50
PARTICLE_RADIUS = 5
REST_DENSITY = 3000
GAS_CONSTANT = 1500
H = 16  # Kernel radius
H2 = H * H  # H squared for optimization
MASS = 50#65
VISCOSITY = 200#250
GRAVITY = 100 #np.array([0, 5200])
DT = 0.001

# Smoothing kernels
def poly6(r2, h2):
    return 315 / (64 * np.pi * h2**4.5) * (h2 - r2)**3 if r2 < h2 else 0

def spiky_gradient(r, h):
    return -45 / (np.pi * h**6) * (h - r)**2 if r < h else 0

def viscosity_laplacian(r, h):
    return 45 / (np.pi * h**6) * (h - r) if r < h else 0

class Particle:
    def __init__(self, x, y):
        self.position = np.array([x, y], dtype=float)
        self.velocity = np.array([0, 0], dtype=float)
        self.force = np.array([0, 0], dtype=float)
        self.density = 0
        self.pressure = 0

particles = [Particle(np.random.uniform(100, 700), np.random.uniform(100, 200)) for _ in range(NUM_PARTICLES)]

def compute_density_pressure():
    for i in range(NUM_PARTICLES):
        particles[i].density = 0
        for j in range(NUM_PARTICLES):
            r2 = np.sum((particles[i].position - particles[j].position) ** 2)
            particles[i].density += MASS * poly6(r2, H2)
        particles[i].pressure = GAS_CONSTANT * (particles[i].density - REST_DENSITY)

def compute_forces():
    for i in range(NUM_PARTICLES):
        f_pressure = np.zeros(2)
        f_viscosity = np.zeros(2)
        for j in range(NUM_PARTICLES):
            if i != j:
                r_ij = particles[i].position - particles[j].position
                r = np.linalg.norm(r_ij)
                if r < H:
                    f_pressure += -r_ij / r * MASS * (particles[i].pressure + particles[j].pressure) / (2 * particles[j].density) * spiky_gradient(r, H)
                    f_viscosity += VISCOSITY * MASS * (particles[j].velocity - particles[i].velocity) / particles[j].density * viscosity_laplacian(r, H)
        f_gravity = GRAVITY * particles[i].density
        particles[i].force = f_pressure + f_viscosity + f_gravity

def integrate():
    for i in range(NUM_PARTICLES):
        particles[i].velocity += DT * particles[i].force / particles[i].density
        particles[i].position += DT * particles[i].velocity

        # Boundary conditions
        if particles[i].position[0] - PARTICLE_RADIUS < 0:
            particles[i].position[0] = PARTICLE_RADIUS
            particles[i].velocity[0] *= -0.1
        if particles[i].position[0] + PARTICLE_RADIUS > 800:
            particles[i].position[0] = 800 - PARTICLE_RADIUS
            particles[i].velocity[0] *= -0.1
        if particles[i].position[1] - PARTICLE_RADIUS < 0:
            particles[i].position[1] = PARTICLE_RADIUS
            particles[i].velocity[1] *= -0.1
        if particles[i].position[1] + PARTICLE_RADIUS > 600:
            particles[i].position[1] = 600 - PARTICLE_RADIUS
            particles[i].velocity[1] *= -0.1

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(background_color)
    
    compute_density_pressure()
    compute_forces()
    integrate()
    
    for particle in particles:
        pygame.draw.circle(screen, particle_color, particle.position.astype(int), PARTICLE_RADIUS)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
