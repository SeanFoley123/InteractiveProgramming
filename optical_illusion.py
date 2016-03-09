import pygame
from pygame.locals import *
import random, math
pygame.init()
screen1 = pygame.display.set_mode((400, 400))
blah = pygame.Surface((100, 150))
for x in range(100):
	for y  in range(150):
		blah.set_at((x, y), (int(127*math.sin(math.pi*y/80)+127), int(127*math.cos(math.pi*y/80)+127), int(127*math.sin(math.pi*y/80+math.pi)+127)))
screen1.blit(blah, (100, 100))
running = True
while running:
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
	pygame.display.update()