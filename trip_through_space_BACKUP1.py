import sys, os, random, math
import pygame
from pygame.locals import *

class Model(object):
	def __init__(self, world_size, screen_size):
		""" Populate a world of size world_size with all the stars and spaceships you want, and set initial variables.
		"""
		self.ship = space_ship(world_size[0]/2, world_size[1]/2, 20, 100)

		how_many = 15
		radius = [random.randint(75, 240) for i in range(how_many)]
		self.stars_list = [Star(random.choice([random.randint(500, world_size[0]/2 - 5.0/8*screen_size[0]), random.randint(world_size[0]/2 + 5.0/8*screen_size[0],
		world_size[0]-500)]), random.choice([random.randint(500, world_size[1]/2 - 5.0/8*screen_size[1]), random.randint(world_size[1]/2 + 5.0/8*screen_size[1],
		world_size[1]-500)]), 3-6*random.random(), 3-6*random.random(), radius[i]*50, radius[i]) for i in range(how_many)]

		self.shrooms = False
		self.death = True						#Do you die if you hit stars?
		self.dead = False						#Are you currently dead?
		self.split_star_list = []

	def force_stars(self, star, other_star):
		"""Calculate the force between star and other_star, move star, and check if star and other_star collide and therefore need to be combined.
		"""
		dx, dy = other_star.x - star.x, other_star.y - star.y
		distance = math.sqrt(dx**2 + dy**2)
		if distance < star.r + other_star.r:
			if star in self.new_star_list and other_star in self.new_star_list:
				self.combine(star, other_star)
		elif distance > 3000:
			pass
		else:
			force = other_star.mass/(distance**2)
			if dy >= 0:
				angle = math.acos(dx/distance)
			else:
				angle = 2*math.pi - math.acos(dx/distance)
			star._accelerate(force, angle)

	def _update(self):
		"""Checks for gravity between each star and between the ship and each star, and calls the update function of each instance of star and ship.
		"""
		self.new_star_list = list(self.stars_list)
		for index, star in enumerate(self.stars_list):
			for other_star in self.stars_list:
				if not star is other_star:
					self.force_stars(star, other_star)
			if star.r >= 500 and star in self.new_star_list:
				print 'split'
				self.new_star_list.remove(star)
				x_pos = star.x
				y_pos = star.y
				self.split(star)

				for index, new_star in enumerate(self.split_star_list):
					theta = index*2*math.pi/len(self.split_star_list)
					new_star.x = x_pos + .75*star.r * math.cos(theta)
					new_star.y = y_pos + .75*star.r * math.sin(theta)
					new_star.vx =  random.randint(14, 14) * math.cos(theta)
					new_star.vy =  random.randint(14, 14) * math.sin(theta)
					self.new_star_list.append(new_star)
				self.split_star_list = []
			if self.shrooms:
				star.change_color()
			star._update()
		self.stars_list = self.new_star_list
		for star in self.stars_list:
			dx = star.x - self.ship.x
			dy = star.y - self.ship.y
			distance = math.sqrt(dx**2 + dy**2)
			if distance <= star.r + self.ship.r/2:
				self.dead = self.death
			if dy >= 0:
				angle = math.acos(dx/distance)
			else:
				angle = 2*math.pi - math.acos(dx/distance)
			self.ship._accelerate(star.mass/(distance/2)**2, angle)
		self.ship._update()
		

	def combine(self, star, other_star):
		"""Takes two stars, destroys them and adds a mixture to Model's new_star_list
		"""
		if star in self.new_star_list:
			self.new_star_list.remove(star)
		if other_star in self.new_star_list:
			self.new_star_list.remove(other_star)
		if star.mass == other_star.mass:
			new_vx = random.choice([star.vx, other_star.vx])
			new_vy = random.choice([star.vy, other_star.vy])
		else:
			new_vx = (star.vx*star.mass + other_star.vx*other_star.mass)/(star.mass + other_star.mass)
			new_vy = (star.vy*star.mass + other_star.vy*other_star.mass)/(star.mass + other_star.mass)
		if star > other_star:
			biggest = star
			smaller = other_star
		elif star < other_star:
			biggest = other_star
			smaller = star
		else:
			biggest = star
			smaller = other_star

		new_star = Star((biggest.mass*biggest.x + smaller.x*smaller.mass)/(biggest.mass + smaller.mass), (biggest.mass*biggest.y + smaller.y*smaller.mass)/(biggest.mass + smaller.mass), new_vx, new_vy, (star.mass + other_star.mass), star.r + other_star.r)
		self.new_star_list.append(new_star)

	def split(self, star):
		""" If star is of certain size, is called, removes star from list and creates new stars that are then added to list.
		"""
		max_r = 150
		min_r = 50
		if star.r < min_r:
			pass
		elif min_r <= star.r <= max_r:
			self.split_star_list.append(star)
		elif star.r > max_r:
			new_star_r = random.randint(min_r, max_r)
			new_star = Star(0, 0, 0, 0, new_star_r*100, new_star_r)
			self.split_star_list.append(new_star)

			remainder_star_r = star.r - new_star_r
			remainder_star = Star(star.x, star.y, star.vx, star.vy, remainder_star_r*100, remainder_star_r)
			self.split(remainder_star)


class space_ship(object):
	""" Represents position/velocity of user's spaceship.
	"""
	def __init__(self, x, y, r, mass, v = 4, angle = -math.pi/2):
		self.rect = pygame.Rect(x-r/math.sqrt(2), y-r/math.sqrt(2), 2*r/math.sqrt(2), 2*r/math.sqrt(2))
		self.mass, self.v, self.angle = mass, v, angle
		self.x, self.y = x, y
		self.r = r
		self.vx, self.vy = v*math.cos(angle), v*math.sin(angle)             #FIIIIIIIIIIIIIIX
		self.acceleration_list, self.turn, self.go = [], 0, 0

	def _update(self):
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
		if self.x + self.vx + self.r >= 10000:
			self.vx -= .75
		if  self.x + self.vx - self.r <= 0:
			self.vx += .75
		if self.y + self.vy + self.r >= 10000:
			self.vy -= .75
		if  self.y + self.vy - self.r <= 0:
			self.vy += .75
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


class Star(object):
	"""Represents position/velocity/other attributes of star.
	"""
	def __init__(self, x, y, vx, vy, mass, r):
		color_letters = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 'A', 'B', 'C', 'D', 'E', 'F']
		self.color = pygame.Color('#{}{}{}{}{}{}'.format(random.choice(color_letters), random.choice(color_letters), random.choice(color_letters), random.choice(color_letters), random.choice(color_letters), random.choice(color_letters)))
		self.x, self.y, self.mass, self.r = x, y, mass, r
		self.rect = pygame.Rect(x-r/math.sqrt(2), y-r/math.sqrt(2), 2*r/math.sqrt(2), 2*r/math.sqrt(2))
		self.vx, self.vy = vx, vy
		self.v = math.sqrt(self.vx**2 + self.vy**2)

	def _update(self):
		self.v = math.sqrt(self.vx**2 + self.vy**2) 
		if  self.v > 3*math.sqrt(2):
			if self.vy >=0:
				theta = math.acos(self.vx/self.v)
			else:
				theta = 2*math.pi - math.acos(self.vx/self.v)
			self.vx -= .05*math.cos(theta)
			self.vy -= .05*math.sin(theta)
		self._move()
		self.rect.centerx, self.rect.centery = self.x, self.y

	def _accelerate(self, force, force_angle):
		self.vx += force*math.cos(force_angle)
		self.vy += force*math.sin(force_angle)

	def _move(self):
		if self.x + self.vx + self.r > 10000 or self.x + self.vx - self.r < 0:
			self.vx = - self.vx
		if self.y + self.vy + self.r > 10000 or self.y + self.vy - self.r < 0:
			self.vy = - self.vy
		self.x += self.vx
		self.y += self.vy

	def change_color(self):
		color_letters = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 'A', 'B', 'C', 'D', 'E', 'F']
		self.color = pygame.Color('#{}{}{}{}{}{}'.format(random.choice(color_letters), random.choice(color_letters), random.choice(color_letters), random.choice(color_letters), random.choice(color_letters), random.choice(color_letters)))

	def __str__(self):
		return '{} mass star at {}, {}'.format(self.mass, self.x, self.y)

	def __cmp__(self, other):
		return self.r - other.r


class Controller(object):
	"""Takes action based on user input.
	"""
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
			if event.type == KEYDOWN and event.key == pygame.K_CAPSLOCK:
				if model.shrooms:                        #SHROOMS!!!
					model.shrooms = False
				else:
					model.shrooms = True

			if event.type == KEYDOWN and event.key == pygame.K_UP:
				model.ship.go += speed
			if event.type == KEYUP and event.key == pygame.K_UP:
				model.ship.go -= speed
			if event.type == KEYDOWN and event.key == pygame.K_DOWN:
				model.ship.go -= speed
			if event.type == KEYUP and event.key == pygame.K_DOWN:
				model.ship.go += speed



class View(object):
	"""Visual representation of model.
	"""
	def __init__(self, screen_size, world_size, model):
		pygame.mouse.set_visible(False)
		self.x, self.y = model.ship.x - screen_size[0]/2, model.ship.y - screen_size[1]/2
		self.screen = pygame.display.set_mode(screen_size)
		#make background
		self.background = pygame.Surface((world_size[0], world_size[1]))
		self.background.fill(pygame.Color('black'))
		#put background stars on background
		star_positions = [(random.randint(0, self.background.get_width()), random.randint(0, self.background.get_height())) for i in range(5000)]
		for x, y in star_positions:															
			pygame.draw.circle(self.background, (255, 255, 255), (x,y), random.choice(range(1, 8)), 0)

		self.screen.blit(self.background, (-model.ship.x, -model.ship.y))

		pygame.draw.circle(self.screen, pygame.Color('red'), (self.screen.get_size()[0]/2, self.screen.get_size()[1]/2), model.ship.r)
		for star in model.stars_list:
			pygame.draw.circle(self.screen, star.color, (star.x, star.y), star.r)
		pygame.display.update()
		
	def _update(self, model):
		self.x, self.y = int(model.ship.x) - self.screen.get_width()/2, int(model.ship.y) - self.screen.get_height()/2
		self.screen.blit(self.background, (-self.x, -self.y))
		pygame.draw.line(self.screen, pygame.Color('white'), (self.screen.get_width()/2, self.screen.get_height()/2), (self.screen.get_width()/2 - 30*math.cos(model.ship.angle), self.screen.get_height()/2 - 30*math.sin(model.ship.angle)), 4)
		pygame.draw.circle(self.screen, pygame.Color('red'), (self.screen.get_width()/2, self.screen.get_height()/2), 20)

		for star in model.stars_list:
			pygame.draw.circle(self.screen, star.color, (int(star.x) - self.x, int(star.y) - self.y), star.r)


		pygame.display.update()


def main():
	pygame.init()
	clock = pygame.time.Clock()
	world_size = (10000, 10000)
	view_size = pygame.display.list_modes()[0]
	model = Model(world_size, view_size)
	controller = Controller()
	view = View(view_size, world_size, model)
	running = True
	i = 1
	while running:              #update everything 60 times per second
		clock.tick(60)
		controller._update(pygame.event.get(), model)
		model._update()
		view._update(model)
		if model.dead:
			view.screen.fill(pygame.Color('red'))
			pygame.display.update()
			pygame.quit()
			sys.exit()
		i += 1

if __name__ == '__main__': main()