import pygame
import numpy as np
from sklearn import neighbors
from tqdm import tqdm

# Constants
MAX_PARTICLES = 300
DOMAIN_WIDTH = 800
DOMAIN_HEIGHT = 600

PARTICLE_MASS = 3
ISOTROPIC_EXPONENT = 30
BASE_DENSITY = 9
SMOOTHING_LENGTH = 15
DYNAMIC_VISCOSITY = 0.2
DAMPING_COEFFICIENT = -0.999
CONSTANT_FORCE = np.array([[0.0, 1.5]])

TIME_STEP_LENGTH = 0.01
N_TIME_STEPS = 2500
ADD_PARTICLES_EVERY = 2

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
PARTICLE_RADIUS = 15

DOMAIN_X_LIM = np.array([
    SMOOTHING_LENGTH,
    DOMAIN_WIDTH - SMOOTHING_LENGTH,
])
DOMAIN_Y_LIM = np.array([
    SMOOTHING_LENGTH,
    DOMAIN_HEIGHT - SMOOTHING_LENGTH,
])

NORMALIZATION_DENSITY = (
    (315 * PARTICLE_MASS) / (64 * np.pi * SMOOTHING_LENGTH ** 9)
)
NORMALIZATION_PRESSURE_FORCE = (
    -(45 * PARTICLE_MASS) / (np.pi * SMOOTHING_LENGTH ** 6)
)
NORMALIZATION_VISCOUS_FORCE = (
    (45 * DYNAMIC_VISCOSITY * PARTICLE_MASS) / (np.pi * SMOOTHING_LENGTH ** 6)
)

# Initialize Pygame
pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

def add_particles(positions, velocities, n_particles):
    new_positions = np.array([
        [400 + np.random.rand(), DOMAIN_Y_LIM[0]],
        [410 + np.random.rand(), DOMAIN_Y_LIM[0]],
        [390 + np.random.rand(), DOMAIN_Y_LIM[0]],
    ])

    new_velocities = np.array([
        [0.0, -0.0],
        [0.0, -0.0],
        [0.0, -0.0],
    ])

    n_particles += 1

    positions = np.concatenate((positions, new_positions), axis=0)
    velocities = np.concatenate((velocities, new_velocities), axis=0)

    return positions, velocities, n_particles


def calculate_densities(positions, neighbor_ids, distances):
    densities = np.zeros(len(positions))

    for i in range(len(positions)):
        for j_in_list, j in enumerate(neighbor_ids[i]):
            densities[i] += NORMALIZATION_DENSITY * (
                SMOOTHING_LENGTH ** 2 - distances[i][j_in_list] ** 2
            ) ** 3

    return densities

def calculate_forces(positions, velocities, neighbor_ids, distances, densities, pressures):
    forces = np.zeros_like(positions)

    # Drop the element itself
    neighbor_ids = [np.delete(x, 0) for x in neighbor_ids]
    distances = [np.delete(x, 0) for x in distances]

    for i in range(len(positions)):
        for j_in_list, j in enumerate(neighbor_ids[i]):
            # Pressure force
            if j_in_list < len(positions[j]):
                # Avoid division by zero or very small distances
                distance = distances[i][j_in_list]
                if distance > 1e-6:
                    # Repulsive force when particles are too close
                    if distance < SMOOTHING_LENGTH / 2:
                        repulsive_force = NORMALIZATION_PRESSURE_FORCE * (
                            -(positions[j] - positions[i]) / distance
                        ) * (
                            pressures[j] + pressures[i]
                        ) / (2 * densities[j]) * (
                            SMOOTHING_LENGTH - distance
                        ) ** 2
                        forces[i] += repulsive_force

                    # Attractive force when particles are at a certain distance
                    if distance > SMOOTHING_LENGTH / 2:
                        attractive_force = -NORMALIZATION_PRESSURE_FORCE * (
                            -(positions[j] - positions[i]) / distance
                        ) * (
                            pressures[j] + pressures[i]
                        ) / (2 * densities[j]) * (
                            SMOOTHING_LENGTH - distance
                        ) ** 2
                        forces[i] += attractive_force

            # Viscous force
            forces[i] += NORMALIZATION_VISCOUS_FORCE * (
                (velocities[j] - velocities[i]) / densities[j]
            ) * (
                SMOOTHING_LENGTH - distance
            )

    return forces


def enforce_boundary_conditions(positions, velocities):
    out_of_left_boundary = positions[:, 0] < DOMAIN_X_LIM[0]
    out_of_right_boundary = positions[:, 0] > DOMAIN_X_LIM[1]
    out_of_bottom_boundary = positions[:, 1] < DOMAIN_Y_LIM[0]
    out_of_top_boundary = positions[:, 1] > DOMAIN_Y_LIM[1]

    velocities[out_of_left_boundary, 0] *= DAMPING_COEFFICIENT
    positions[out_of_left_boundary, 0] = DOMAIN_X_LIM[0]

    velocities[out_of_right_boundary, 0] *= DAMPING_COEFFICIENT
    positions[out_of_right_boundary, 0] = DOMAIN_X_LIM[1]

    velocities[out_of_bottom_boundary, 1] *= DAMPING_COEFFICIENT
    positions[out_of_bottom_boundary, 1] = DOMAIN_Y_LIM[0]

    velocities[out_of_top_boundary, 1] *= DAMPING_COEFFICIENT
    positions[out_of_top_boundary, 1] = DOMAIN_Y_LIM[1]

    return positions, velocities

def draw_particles(window, positions):
    # Use a surface to blend particles for fluid effect
    fluid_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
    
    for i in range(len(positions)):
        x, y = positions[i]
        if np.isnan(x) or np.isnan(y):
            continue
        if 0 <= x <= WINDOW_WIDTH and 0 <= y <= WINDOW_HEIGHT:
            pygame.draw.circle(fluid_surface, (144, 209, 234, 100), (int(x), int(y)), PARTICLE_RADIUS)
    
    window.blit(fluid_surface, (0, 0))

def main():
    n_particles = 1

    positions = np.ones((n_particles, 2))
    velocities = np.zeros_like(positions)
    forces = np.zeros_like(positions)

    for iter in tqdm(range(N_TIME_STEPS)):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        if iter % ADD_PARTICLES_EVERY == 0 and n_particles < MAX_PARTICLES:
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

        # Clear the window
        window.fill((0, 0, 0))

        # Draw particles
        draw_particles(window, positions)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
