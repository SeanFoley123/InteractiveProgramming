import pygame
from pygame.locals import *
import random, math
from pickle import load, dump
pygame.init()
screen1 = pygame.display.set_mode((400, 400))
load(open('edges'))[0]
# for x in range(blah.get_width()):
# 	for y  in range(blah.get_height()):
# 		blah.set_at((x, y), (int(127*math.sin(math.pi*y/80)+127), int(127*math.cos(math.pi*y/80)+127), int(127*math.sin(math.pi*y/80+math.pi)+127)))
screen1.blit(blah, (100, 100))
running = True
while running:
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
	pygame.display.update()