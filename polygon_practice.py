import sys, os, random, math
import pygame
from pygame.locals import *
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((500, 500))
screen.fill(pygame.Color('white'))
pygame.draw.polygon(screen, pygame.Color('red'), [(100, 200), (200, 300), (100, 100)], 10)
running = True
while running:
	clock.tick(60)
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()

	pygame.display.flip()