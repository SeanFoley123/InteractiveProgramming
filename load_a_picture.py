import sys, os
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
	def update(self):
		pass
	# 	self.rect.center = pygame.mouse.get_pos()
	def _move(self, (x, y)):
		self.rect = self.rect.move((x, y))


def main():
	pygame.init()
	pygame.display.set_caption('dogsdogsdogs')
	full_screen = pygame.display.list_modes()
	screen = pygame.display.set_mode(full_screen[0])
	clock = pygame.time.Clock()
	# background = pygame.Surface(screen.get_size())
	# background = background.convert()
	# background.fill((250, 250, 250))
	# screen.blit(background, (0, 0))
	screen.fill((0,0,0))
	pygame.display.flip()
	goofy = Dog()
	allsprites = pygame.sprite.RenderPlain(goofy)
	speed = 5
	movement = {pygame.K_LEFT: (-speed, 0), pygame.K_RIGHT: (speed, 0), pygame.K_UP: (0, -speed), pygame.K_DOWN: (0, speed)}
	key_list = []
	running = True

	while running:
		clock.tick(120)
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			if event.type == KEYDOWN and event.key in movement.keys():
				key_list.append(event.key)
			if event.type == KEYUP and event.key in movement.keys():
				key_list.remove(event.key)
		for key_pressed in key_list:
			goofy._move(movement[key_pressed])
		allsprites.update()
		# screen.blit(background, (0, 0))
		allsprites.draw(screen)
		pygame.display.flip()
        
if __name__ == '__main__': main()