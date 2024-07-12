import os
import random
from maze import *
from wall import *
import pygame

WHITE = (255,255,255)
GREY = (20,20,20)
BLACK = (0,0,0)
PURPLE = (128,0,128)
RED = (255,0,0)
BLUE = (0,0,255)

size = 701,701


    

def main():
    pygame.init()
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Maze Game')
    screen.fill((255,255,255))

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