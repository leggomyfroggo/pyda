import pygame
from pygame.locals import *
from contentmanager import ContentManager
from sprite import Sprite

DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'
UP = 'up'

# Load the sword's content
ContentManager.LoadImage('sword', 'Images/link.png')

class Sword(Sprite):
	def __init__(self):
		# Prepare the base
		Sprite.__init__(self, 'sword', (16, 16), (14, 14))
		# Set an initial direction to prevent things from breaking
		self.direction = DOWN
		self.zOrder = 0.99
		# Add the sword animations
		self.AddAnimation('down', [(0, 6.5, 1, (x + 1) * 2) for x in range(7)] + [(0, 6.5, 1, 14 - (x + 1) * 2) for x in range(7)], 84, False)
		self.AddAnimation('left', [(1, 6.5, (x + 1) * -2, 2) for x in range(7)] + [(1, 6.5, -14 + (x + 1) * 2, 2) for x in range(7)], 84, False)
		self.AddAnimation('up', [(2, 6.5, -1, (x + 1) * -2) for x in range(7)] + [(2, 6.5, -1, -14 + (x + 1) * 2) for x in range(7)], 84, False)
		self.AddAnimation('right', [(3, 6.5, (x + 1) * 2, 2) for x in range(7)] + [(3, 6.5, 14 - (x + 1) * 2, 2) for x in range(7)], 84, False)
		self.SetAnimation('down')

	def ResetForSwing(self, Position, Direction):
		self.position = Position
		self.direction = Direction
		self.SetAnimation(self.direction)
		self.ResetAnimation()

	def Render(self):
		print self.isAnimPaused
		if not self.isAnimPaused:
			Sprite.Render(self)

	def OnAnimationFinished(self):
		print 'oh god'