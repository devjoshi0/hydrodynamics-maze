import os
from maze import *
import pygame


WINSIZE = [640, 480]

def main():
    pygame.init()
    screen = pygame.display.set_mode(WINSIZE)
    screen_info = pygame.display.Info()
    pygame.display.set_caption('Maze Game')
    screen.fill((0,0,0))

    clock = pygame.time.Clock()
    

    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        pygame.display.update()
        clock.tick()

if __name__ == '__main__':
    main()