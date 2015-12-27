import pygame
from pygame.locals import *
from sprite import Sprite

DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'
UP = 'up'

class Sword(Sprite):
	def __init__(self):
		# Prepare the base
		Sprite.__init__(self, 'Images/link.png', (16, 16), (14, 14))

		# Set an initial direction to prevent things from breaking
		self.direction = DOWN

		# Add the sword animations
		self.AddAnimation('down', [(0, 6.5, 1, (x + 1) * 2) for x in range(7)] + [(0, 6.5, 1, 14 - (x + 1) * 2) for x in range(7)], 84, True)
		self.AddAnimation('left', [(1, 6.5, (x + 1) * -2, 2) for x in range(7)] + [(1, 6.5, -14 + (x + 1) * 2, 2) for x in range(7)], 84, True)
		self.AddAnimation('up', [(2, 6.5, -1, (x + 1) * -2) for x in range(7)] + [(2, 6.5, -1, -14 + (x + 1) * 2) for x in range(7)], 84, True)
		self.AddAnimation('right', [(3, 6.5, (x + 1) * 2, 2) for x in range(7)] + [(3, 6.5, 14 - (x + 1) * 2, 2) for x in range(7)], 84, True)
		self.SetAnimation('down')

	def Update(self, DT, Events):
		# Update the base sprite
		Sprite.Update(self, DT, Events)

	def ResetForSwing(self, Direction):
		self.direction = Direction
		self.SetAnimation(self.direction)
		self.ResetAnimation()