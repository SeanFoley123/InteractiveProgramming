import sys, os, random
import pygame
from pygame.locals import *

class Spaceship(object):
	def __init__(self, x, y, length=40):
		self.x, self.y, self.length = x, y, length
	def update(self, background):
		print 'hi'
	def _move(dx, dy):
		self.x += dx
		self.y += dy

def main():
	pygame.init()												#create game window and initialize backend
	pygame.display.set_caption('practice makes purrfect')
	clock = pygame.time.Clock()

	screen = pygame.display.set_mode((800, 800))
	background = pygame.Surface((10000, 10000))
	sizex, sizey = background.get_size()
	screenx, screeny = screen.get_size()

	star_positions = [(random.randint(0, background.get_width()), random.randint(0, background.get_height())) for i in range(random.randint(1000, 2000))]
	for x, y in star_positions:															#put background stars on background
		pygame.draw.circle(background, (255, 255, 255), (x,y), 7, 0)

	# for x in range(sizex):
	# 	for y in range(sizey):
	# 		background.set_at((x, y), (y**2*255/sizey**2, x**2*255/sizex**2, 0))

	uss_greg = Spaceship(screenx/2, screeny/2)

	speed = 10
	movement = {pygame.K_LEFT: (speed, 0), pygame.K_RIGHT: (-speed, 0), pygame.K_UP: (0, speed), pygame.K_DOWN: (0, -speed)}
	key_pressed = []

	running = True
	i = 0
	x, y = 0, 0

	while running:
		clock.tick(60)
		uss_greg.update(background)
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			if event.type == KEYDOWN and event.key in movement:		
				key_pressed.append(event.key)
			if event.type == KEYUP and event.key in movement:		
				key_pressed.remove(event.key)
		for key in key_pressed:
			uss_greg.x += movement[key][0]
			uss_greg.y += movement[key][1]
		screen.blit(background, (uss_greg.x, uss_greg.y))
		pygame.display.flip()
if __name__ == '__main__': main()