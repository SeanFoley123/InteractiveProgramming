from pickle import load, dump
import math
import pygame
from pygame.locals import *
edge_horizontal = pygame.Surface((10000 + 2000, 1000))
edge_vertical = pygame.Surface((1000, 10000 + 2000))
for x in range(edge_horizontal.get_width()):
	for y  in range(edge_horizontal.get_height()):
		edge_horizontal.set_at((x, y), (int(127*math.sin(math.pi*y/80)+127), int(127*math.cos(math.pi*y/80)+127), int(127*math.sin(math.pi*y/80+math.pi)+127)))
print 'hi'
for x in range(edge_vertical.get_width()):
	for y  in range(edge_vertical.get_height()):
		edge_vertical.set_at((x, y), (int(127*math.sin(math.pi*y/80)+127), int(127*math.cos(math.pi*y/80)+127), int(127*math.sin(math.pi*y/80+math.pi)+127)))				
dump((edge_horizontal, edge_vertical), open('edges', 'w'))