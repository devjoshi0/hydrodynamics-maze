import pygame

# Initialize Pygame
pygame.init()

# Set up the display
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Maze Game")

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Define the maze
maze = [
    "11111111111111111111",
    "10000000000000000001",
    "10111011111111111101",
    "10101000000000000101",
    "10101111111011110101",
    "10101000000001000101",
    "10101011111010110101",
    "10101010000000100101",
    "10101010111111110101",
    "10101010100000000101",
    "10101010101111110101",
    "10101010101000000101",
    "10101010101011110101",
    "10101010101010000101",
    "10101010101010110101",
    "10101010101010100101",
    "10101010101010101001",
    "10101010101010101001",
    "10101010101010101001",
    "11111111111111111111"
]

# Define the player
player_size = 20
player_x = 40
player_y = 40
player_speed = 5

# Game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move the player
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x -= player_speed
    if keys[pygame.K_RIGHT]:
        player_x += player_speed
    if keys[pygame.K_UP]:
        player_y -= player_speed
    if keys[pygame.K_DOWN]:
        player_y += player_speed

    # Check for collisions with walls
    for row in range(len(maze)):
        for col in range(len(maze[row])):
            if maze[row][col] == "1":
                wall_rect = pygame.Rect(col * player_size, row * player_size, player_size, player_size)
                player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
                if player_rect.colliderect(wall_rect):
                    # Handle collision
                    print("Collision detected!")

    # Draw the maze
    screen.fill(BLACK)
    for row in range(len(maze)):
        for col in range(len(maze[row])):
            if maze[row][col] == "1":
                pygame.draw.rect(screen, WHITE, (col * player_size, row * player_size, player_size, player_size))

    # Draw the player
    pygame.draw.rect(screen, WHITE, (player_x, player_y, player_size, player_size))

    # Update the display
    pygame.display.flip()

# Quit the game
pygame.quit()
