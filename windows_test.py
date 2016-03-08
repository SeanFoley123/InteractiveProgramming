import pygame
from pygame.locals import *
pygame.init()
screen1 = pygame.display.set_mode((400, 400))
screen2 = pygame.display.set_mode((600, 400))
running = True
while running:
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
	pygame.display.update()