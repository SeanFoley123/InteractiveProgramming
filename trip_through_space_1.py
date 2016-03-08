import sys, os, random, math
import pygame
from pygame.locals import *

class Model(object):
	def __init__(self, world_size):
		self.ship = space_ship(world_size[0]/2, world_size[1]/2, 20, 100)
		self.stars_list = [star(3000, 3000, 10000, 100, pygame.Color('yellow')), star(3700, 3000, 15000, 150, pygame.Color('blue'))]

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
		for star in self.stars_list:
			dx = star.x - self.ship.x
			dy = star.y - self.ship.y
			distance = math.sqrt(dx**2 + dy**2)
			if dy >= 0:
				angle = math.acos(dx/distance)
			else:
				angle = 2*math.pi - math.acos(dx/distance)
			self.ship._accelerate(star.mass/(distance/2)**2, angle)
		self.ship._update()

	def check_collide(self):
		for star in self.stars_list:
			if self.ship.rect.colliderect(star.rect):
				return True
		return False


class space_ship(object):
	def __init__(self, x, y, r, mass, v = 4, angle = 0):
		self.rect = pygame.Rect(x-r/math.sqrt(2), y-r/math.sqrt(2), 2*r/math.sqrt(2), 2*r/math.sqrt(2))
		self.mass, self.v, self.angle = mass, v, angle
		self.x, self.y = x, y
		self.r = r
		self.vx, self.vy = v*math.cos(angle), v*math.sin(angle)             #FIIIIIIIIIIIIIIX
		self.acceleration_list, self.turn, self.go = [], 0, 0

	def _update(self):
		# for acceleration in self.acceleration_list:									#Each element is a tuple of force and direction
		# 	self._thrust(acceleration[0], acceleration[1])
		self.v = math.sqrt(self.vx**2+self.vy**2)
		if self.v != 0:
			if self.vy >=0:
				self.angle = math.acos(self.vx/self.v)
			else:
				self.angle = 2*math.pi - math.acos(self.vx/self.v)
		self._turn(self.turn)
		self._thrust(self.go)
		self._move()
		self.rect.centerx, self.rect.centery = self.x, self.y
		self.acceleration_list = []
		

	def _move(self):
		self.x += self.vx
		self.y += self.vy

	def _turn(self, how_much):
		if self.v > 0:
			self.vx += -how_much * self.vy
			self.vy += how_much * self.vx
		else:
			self.angle += 2*how_much

	def _thrust(self, force):
		""" Takes in a scalar force and its direction, updates vx and vy 
		"""
		if force > 0 and self.v < 10:
			self.vx += force*math.cos(self.angle)
			self.vy += force*math.sin(self.angle)
		if force < 0 and self.v + force >= 4:
			self.vx += force*math.cos(self.angle)
			self.vy += force*math.sin(self.angle)

	def _accelerate(self, force, force_angle):
		""" Takes in a scalar force and its direction, updates vx and vy 
		"""
		self.vx += force*math.cos(force_angle)
		self.vy += force*math.sin(force_angle)			


class star(object):
	def __init__(self, x, y, vx, vy, mass, r, color):
		self.x, self.y, self.mass, self.r, self.color = x, y, mass, r, color
		self.rect = pygame.Rect(x-r/math.sqrt(2), y-r/math.sqrt(2), 2*r/math.sqrt(2), 2*r/math.sqrt(2))
		self.vx, self.vy = vx, vy

	def _update(self):
		pass

	def _accelerate(self, force, force_angle):
		self.vx += force*math.cos(force_angle)
		self.vy += force*math.sin(force_angle)


class Controller(object):
	def __init__(self):
		pass
	def _update(self, events, model):
		speed = .1
		angle_turn = (math.pi/2)/60
		for event in events:
			if event.type == QUIT or event.type == KEYDOWN and event.key == pygame.K_ESCAPE:
				pygame.quit()
				sys.exit()
			if event.type == KEYDOWN and event.key == pygame.K_F1:
				pygame.display.toggle_fullscreen()
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
		#put background stars on background
		star_positions = [(random.randint(0, self.background.get_width()), random.randint(0, self.background.get_height())) for i in range(5000)]
		for x, y in star_positions:															
			pygame.draw.circle(self.background, (255, 255, 255), (x,y), random.choice(range(1, 8)), 0)
		#Draw stars
		for star in model.stars_list:
			pygame.draw.circle(self.background, star.color, (star.x, star.y), star.r)
			# pygame.draw.rect(self.background, pygame.Color('red'), star.rect, 2)
		pygame.draw.line(self.background, pygame.Color('white'), (0, 0), (self.background.get_size()[0], 0), 2)
		pygame.draw.line(self.background, pygame.Color('white'), (0, 0), (0, self.background.get_size()[1]), 2)
		pygame.draw.line(self.background, pygame.Color('white'), (0, self.background.get_size()[1]-2), (self.background.get_size()[0]-2, self.background.get_size()[1]-2), 2)
		pygame.draw.line(self.background, pygame.Color('white'), (self.background.get_size()[0]-1, 0), (self.background.get_size()[0]-2, self.background.get_size()[1]-2), 2)

		self.screen.blit(self.background, (-model.ship.x, -model.ship.y))
		# point_list = 
		pygame.draw.circle(self.screen, pygame.Color('red'), (self.screen.get_size()[0]/2, self.screen.get_size()[1]/2), model.ship.r)
		pygame.display.update()
		
	def _update(self, model):
		self.screen.blit(self.background, (self.screen.get_size()[0]/2-model.ship.x, self.screen.get_size()[1]/2-model.ship.y))
		pygame.draw.line(self.screen, pygame.Color('white'), (self.screen.get_width()/2, self.screen.get_height()/2), (self.screen.get_width()/2 - 30*math.cos(model.ship.angle), self.screen.get_height()/2 - 30*math.sin(model.ship.angle)), 4)
		pygame.draw.circle(self.screen, pygame.Color('red'), (self.screen.get_width()/2, self.screen.get_height()/2), 20)
		# pygame.draw.rect(self.screen, pygame.Color('red'), model.ship.rect, 1)
		
		pygame.display.update()


def main():
	pygame.init()
	clock = pygame.time.Clock()
	world_size = (10000, 10000)
	view_size = pygame.display.list_modes()[0]
	model = Model(world_size)
	controller = Controller()
	view = View(view_size, world_size, model)
	running = True
	i = 1
	while running:
		clock.tick(60)
		controller._update(pygame.event.get(), model)
		model._update()
		if i%3 > 0:
			view._update(model)
			i = 0
		if model.check_collide():
			view._update(model)
			pygame.quit()
			sys.exit()
		i += 1

if __name__ == '__main__': main()