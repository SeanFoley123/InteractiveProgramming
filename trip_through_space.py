import sys, os, random, math
import pygame
from pygame.locals import *

class Model(object):
	def __init__(self):
		self.ship = space_ship(100, 300, 50, 20, 100)
		self.stars_list = [star(500, 500, 500, 100, pygame.Color('white'))]

	def force(self, space_ship, star):
		dx, dy = star.x - space_ship.x, star.y - space_ship.y
		distance = math.sqrt(dx**2 + dy**2)
		force = space_ship.mass*star.mass/distance**2
		if dx>=0:
			angle = math.asin(dy/distance)
		else:
			angle = math.pi - math.asin(dy/distance)
		space_ship._accelerate(force, angle)

	def _update(self):
		self.ship._update()


class space_ship(object):
	def __init__(self, x, y, width, height, mass, v = 0, angle = 0):
		self.rect = pygame.Rect(x-width/2, y-height/2, width, height)
		self.mass, self.v, self.angle = mass, v, angle
		self.x, self.y = x, y
		self.vx, self.vy = v*math.cos(angle), v*math.sin(angle)             #FIIIIIIIIIIIIIIX
		self.acceleration_list, self.turn, self.go = [], 0, 0

	def _update(self):
		# for acceleration in self.acceleration_list:									#Each element is a tuple of force and direction
		# 	self._accelerate(acceleration[0], acceleration[1])
		self.v = math.sqrt(self.vx**2+self.vy**2)
		if self.v != 0:
			if self.vy >=0:
				self.angle = math.acos(self.vx/self.v)
			else:
				self.angle = 2*math.pi - math.acos(self.vx/self.v)
		self._turn(self.turn)
		self._accelerate(self.go, self.angle)
		self._move()
		self.rect.centerx, self.rect.centery = self.x, self.y
		self.acceleration_list = []
		

	def _move(self):
		self.x += self.vx
		self.y += self.vy

	def _turn(self, how_much):
		if self.v > 0:
			self.vx += -how_much * abs(self.vy)
			self.vy += how_much * abs(self.vx)
		else:
			self.angle += how_much
		
		

	def _accelerate(self, force, force_angle):
		""" Takes in a scalar force and its direction, updates vx and vy 
		"""
		if self.v < 20:
			if self.v + force >= 0:
				self.vx += force*math.cos(force_angle)
				self.vy += force*math.sin(force_angle)
			else:
				self.vx, self.vy = 0, 0
		else:
			print "hi"


class star(object):
	def __init__(self, x, y, mass, r, color):
		self.x, self.y, self.mass, self.r, self.color = x, y, mass, r, color
		self.rect = pygame.Rect(x-r/math.sqrt(2), y-r/math.sqrt(2), 2*r/math.sqrt(2), 2*r/math.sqrt(2))


class Controller(object):
	def __init__(self):
		pass
	def _update(self, events, model):
		speed = .1
		angle_turn = (math.pi/2)/60
		for event in events:

		
			if event.type == QUIT:
				pygame.quit()
				sys.exit()

			if event.type == KEYDOWN and event.key == pygame.K_RIGHT:
				model.ship.turn += angle_turn
			if event.type == KEYUP and event.key == pygame.K_RIGHT:
				model.ship.turn -= angle_turn
			if event.type == KEYDOWN and event.key == pygame.K_LEFT:
				model.ship.turn -= angle_turn
			if event.type == KEYUP and event.key == pygame.K_LEFT:
				model.ship.turn += angle_turn


			if event.type == KEYDOWN and event.key == pygame.K_UP:
				model.ship.go += speed
			if event.type == KEYUP and event.key == pygame.K_UP:
				model.ship.go -= speed
			if event.type == KEYDOWN and event.key == pygame.K_DOWN:
				model.ship.go -= speed
			if event.type == KEYUP and event.key == pygame.K_DOWN:
				model.ship.go += speed




class View(object):
	def __init__(self, screen_size, world_size, model):
		self.screen = pygame.display.set_mode(screen_size)
		self.background = pygame.Surface(world_size)
		self.background.fill(pygame.Color('black'))
		star_positions = [(random.randint(0, self.background.get_width()), random.randint(0, self.background.get_height())) for i in range(random.randint(10, 20))]
		for x, y in star_positions:															#put background stars on background
			pygame.draw.circle(self.background, (255, 255, 255), (x,y), 7, 0)
		self.screen.blit(self.background, (-model.ship.x, -model.ship.y))
		# point_list = 
		pygame.draw.rect(self.screen, pygame.Color('red'), model.ship.rect)
		pygame.display.update()
		
	def _update(self, model):
		self.screen.blit(self.background, (-model.ship.x, -model.ship.y))
		pygame.draw.line(self.screen, pygame.Color('white'), (model.ship.x, model.ship.y), (model.ship.x - 30*math.cos(model.ship.angle), model.ship.y - 30*math.sin(model.ship.angle)), 4)
		pygame.draw.circle(self.screen, pygame.Color('red'), (int(model.ship.x), int(model.ship.y)), 20)
		
		pygame.display.update()


def main():
	pygame.init()
	clock = pygame.time.Clock()
	model = Model()
	controller = Controller()
	view = View((1000, 1000), (1500, 1500), model)
	running = True
	while running:
		clock.tick(60)
		controller._update(pygame.event.get(), model)
		model._update()
		view._update(model)

if __name__ == '__main__': main()