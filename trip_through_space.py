import sys, os, random, math
import pygame
from pygame.locals import *

class Model(object):
	def __init__(self, world_size, screen_size):
		self.ship = space_ship(world_size[0]/2, world_size[1]/2, 20, 100)
		star_positions = []
		i = 0
		while i < 10:
			x = random.choice([random.randint(500, world_size[0]/2 - 5.0/8*screen_size[0]), random.randint(world_size[0]/2 + 5.0/8*screen_size[0], world_size[0]-500)])
			y = random.choice([random.randint(500, world_size[1]/2 - 5.0/8*screen_size[1]), random.randint(world_size[1]/2 + 5.0/8*screen_size[1], world_size[1]-500)])
			flag = False
			for x1, y1 in star_positions:
				if x1-500 < x < x1 + 500 or y1-500 < y < y1+500:
					flag = True
					break
			if flag:
				continue
			else:
				star_positions.append((x,y))
				i+=1
		radius = [random.randint(75, 240) for i in range(len(star_positions))]
		self.stars_list = [Star(star_positions[i][0], star_positions[i][1], 3-6*random.random(), 3-6*random.random(), radius[i]*50, radius[i]) for i in range(len(star_positions))]
		self.split_star_list = []
		for star in self.stars_list:
			print star
		self.shrooms = False
		self.dead = False

	def force_stars(self, star, other_star):
		dx, dy = other_star.x - star.x, other_star.y - star.y
		distance = math.sqrt(dx**2 + dy**2)
		if distance < star.r + other_star.r:
			if star in self.new_star_list and other_star in self.new_star_list:
				self.combine(star, other_star)
		elif distance > 1000:
			pass
		else:
			force = other_star.mass/(distance**2)
			if dy >= 0:
				angle = math.acos(dx/distance)
			else:
				angle = 2*math.pi - math.acos(dx/distance)
			star._accelerate(force, angle)

	def _update(self):
		self.new_star_list = list(self.stars_list)
<<<<<<< HEAD
		#check for split
		#new_star_list has 5 stars - all at 0,0 w/ vx, vy = 0, 0
		#for star in new_star_list
=======
		
>>>>>>> 3e847e07ddef97ac4b7c9f502a0579116a11c275
		for star in self.stars_list:
			if star.mass > 50000:
				self.stars_list.remove(star)
				x_pos = star.x
				y_pos = star.y
				self.split_star_list = []
				self.split(star)

				for new_star in self.split_star_list:
					theta = self.split_star_list.index(new_star)*2*math.pi/len(self.split_star_list)
					new_star.x = x_pos + 2 * new_star.r * math.cos(theta)
					new_star.y = y_pos + 2 * new_star.r * math.sin(theta)
					new_star.vx =  random.randit(0, 3) * math.cos(theta)
					new_star.vy =  random.randint(0,3) * math.sin(theta)

			for other_star in self.stars_list:
				if not star is other_star:
					self.force_stars(star, other_star)
			star._update()
			if self.shrooms:
				star.change_color()
		for star in self.stars_list:
			dx = star.x - self.ship.x
			dy = star.y - self.ship.y
			distance = math.sqrt(dx**2 + dy**2)
			if distance <= star.r + self.ship.r/2:
				self.dead = True
			if dy >= 0:
				angle = math.acos(dx/distance)
			else:
				angle = 2*math.pi - math.acos(dx/distance)
			self.ship._accelerate(star.mass/(distance/2)**2, angle)
		self.ship._update()
		self.stars_list = self.new_star_list
		self.stars_list.extend(self.split_star_list)

	def combine(self, star, other_star):
		
		self.new_star_list.remove(star)
		self.new_star_list.remove(other_star)
		if star.mass == other_star.mass:
			new_vx = random.choice(star.vx, other_star.vx)
			new_vy = random.choice(star.vy, other_star.vy)
		else:
			new_vx = (star.vx*star.mass + other_star.vx*other_star.mass)/(star.mass + other_star.mass)
			new_vy = (star.vy*star.mass + other_star.vy*other_star.mass)/(star.mass + other_star.mass)
		if star > other_star:
			biggest = star
		elif star < other_star:
			biggest = other_star
		else:
			biggest = random.choice([star, other_star])
		new_star = Star((star.x + other_star.x)/2, (star.y + other_star.y)/2, new_vx, new_vy, int(.75*(star.mass + other_star.mass)), star.r + other_star.r)
		self.new_star_list.append(new_star)

	def split(self, star):
		print 'split'
		max_m = 15000
		min_m = 5000

		if star.mass < min_m:
			pass
		elif min_m <= star.mass <= max_m:
			self.split_star_list.append(star)
		elif star.mass > max_m:
			new_star_mass = random.randint(min_m, max_m)
			new_star = Star(0, 0, 0, 0, new_star_mass, new_star_mass/100)
			self.split_star_list.append(new_star)

			remainder_star_mass = random.randint(min_m, max_m - new_star_mass)
			remainder_star = Star(star.x, star.y, star.vx, star.vy, remainder_star_mass, remainder_star_mass/100)
			split(remainder_star)


class space_ship(object):
	def __init__(self, x, y, r, mass, v = 4, angle = -math.pi/2):
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
	def __init__(self, x, y, vx, vy, mass, r):
		color_letters = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 'A', 'B', 'C', 'D', 'E', 'F']
		self.color = pygame.Color('#{}{}{}{}{}{}'.format(random.choice(color_letters), random.choice(color_letters), random.choice(color_letters), random.choice(color_letters), random.choice(color_letters), random.choice(color_letters)))
		self.x, self.y, self.mass, self.r = x, y, mass, r
		self.rect = pygame.Rect(x-r/math.sqrt(2), y-r/math.sqrt(2), 2*r/math.sqrt(2), 2*r/math.sqrt(2))
		self.vx, self.vy = vx, vy

	def _update(self):
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
		return '{} color star at {}, {}'.format(self.color, self.x, self.y)

	def __cmp__(self, other):
		return self.r - other.r


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
			if event.type == KEYDOWN and event.key == pygame.K_CAPSLOCK:
				if model.shrooms:
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
	def __init__(self, screen_size, world_size, model):
		pygame.mouse.set_visible(False)
		self.x, self.y = model.ship.x - screen_size[0]/2, model.ship.y - screen_size[1]/2
		self.screen = pygame.display.set_mode(screen_size)
		#make background
		self.background = pygame.Surface((world_size[0]+screen_size[0], world_size[1] + screen_size[1]))
		self.background.fill(pygame.Color('black'))
		#put background stars on background
		star_positions = [(random.randint(0, self.background.get_width()), random.randint(0, self.background.get_height())) for i in range(5000)]
		for x, y in star_positions:															
			pygame.draw.circle(self.background, (255, 255, 255), (x,y), random.choice(range(1, 8)), 0)
		#Draw stars
			# pygame.draw.rect(self.background, pygame.Color('red'), star.rect, 2)
		# pygame.draw.line(self.background, pygame.Color('white'), (0, 0), (self.background.get_size()[0], 0), 2)
		# pygame.draw.line(self.background, pygame.Color('white'), (0, 0), (0, self.background.get_size()[1]), 2)
		# pygame.draw.line(self.background, pygame.Color('white'), (0, self.background.get_size()[1]-2), (self.background.get_size()[0]-2, self.background.get_size()[1]-2), 2)
		# pygame.draw.line(self.background, pygame.Color('white'), (self.background.get_size()[0]-1, 0), (self.background.get_size()[0]-2, self.background.get_size()[1]-2), 2)

		self.screen.blit(self.background, (-model.ship.x, -model.ship.y))

		# point_list = 
		pygame.draw.circle(self.screen, pygame.Color('red'), (self.screen.get_size()[0]/2, self.screen.get_size()[1]/2), model.ship.r)
		for star in model.stars_list:
			pygame.draw.circle(self.screen, star.color, (star.x, star.y), star.r)
		pygame.display.update()
		
	def _update(self, model):
		self.x, self.y = int(model.ship.x) - self.screen.get_width()/2, int(model.ship.y) - self.screen.get_height()/2
		self.screen.blit(self.background, (-self.x, -self.y))
		pygame.draw.line(self.screen, pygame.Color('white'), (self.screen.get_width()/2, self.screen.get_height()/2), (self.screen.get_width()/2 - 30*math.cos(model.ship.angle), self.screen.get_height()/2 - 30*math.sin(model.ship.angle)), 4)
		pygame.draw.circle(self.screen, pygame.Color('red'), (self.screen.get_width()/2, self.screen.get_height()/2), 20)
		# pygame.draw.rect(self.screen, pygame.Color('red'), model.ship.rect, 1)
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
	while running:
		clock.tick(60)
		controller._update(pygame.event.get(), model)
		model._update()
		view._update(model)
		if model.dead:
			pygame.quit()
			sys.exit()
		i += 1

if __name__ == '__main__': main()