import sys, os, random, math
import pygame
from pygame.locals import *
def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Cannot load image:', fullname
        raise SystemExit, message
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()

class Dog(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image, self.rect = load_image('dog.jpg', -1)
		self.vx, self.vy = 0, 0
		self.mass = 1000.0
	def update(self):
		print self.vx, self.vy
		self.rect = self.rect.move((self.vx, self.vy))
	def _move(self, (x, y)):
		self.rect = self.rect.move((x, y))
	def _accelerate(self, force):
		if abs(self.vx)<30 and abs(self.vy)<30:
			self.vx += force[0]/self.mass 					
			self.vy += force[1]/self.mass

class Star(object):
	def __init__(self, (x,y), mass):
		self.centerx, self.centery = x, y
		self.mass = mass

def force(object1, object2, screen):
	distance = math.sqrt((object1.rect.centerx-object2.centerx)**2 + (object1.rect.centery-object2.centery)**2)
	x_hat, y_hat = (object2.centerx-object1.rect.centerx)/distance, (object2.centery-object1.rect.centery)/distance
	total_force = object1.mass*object2.mass/distance**2
	pygame.draw.line(screen, (255, 255, 255), (object1.rect.centerx, object1.rect.centery), (object1.rect.centerx+distance*x_hat, object1.rect.centery+distance*y_hat))
	return (total_force*x_hat, total_force*y_hat)

def main():
	pygame.init()												#create game window and initialize backend
	pygame.display.set_caption('dogsdogsdogs')
	clock = pygame.time.Clock()

	full_screen = pygame.display.list_modes()					#make background
	screen = pygame.display.set_mode(full_screen[0])
	background = pygame.Surface(screen.get_size())
	background = background.convert()
	background.fill((0, 0, 0))

	star_positions = [(random.randint(0, background.get_width()), random.randint(0, background.get_height())) for i in range(random.randint(10, 20))]
	for x, y in star_positions:															#put background stars on background
		pygame.draw.circle(background, (255, 255, 255), (x,y), 7, 0)
	screen.blit(background, (0, 0))
	new_star = Star((800, 800), 8000)
	
	goofy = Dog()
	
	allsprites = pygame.sprite.RenderPlain(goofy)
	speed = 100
	movement = {pygame.K_LEFT: (-speed, 0), pygame.K_RIGHT: (speed, 0), pygame.K_UP: (0, -speed), pygame.K_DOWN: (0, speed)}
	key_list = []
	running = True
	while running:
		clock.tick(60)
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			if event.type == KEYDOWN and event.key in movement.keys():
				key_list.append(event.key)
			if event.type == KEYUP and event.key in movement.keys():
				key_list.remove(event.key)
		for key_pressed in key_list:
			goofy._accelerate(movement[key_pressed])
		screen.blit(background, (0, 0))
		# pygame.draw.circle(background, (goofy.rect.centerx, ))
		goofy._accelerate(force(goofy, new_star, screen))
		allsprites.update()
		allsprites.draw(screen)
		pygame.display.flip()
        
if __name__ == '__main__': main()