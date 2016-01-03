import pygame
from pygame.locals import *
from helpers.contentmanager import ContentManager
from helpers.globalcomm import GlobalComm
from gameobjects.sprite import Sprite
from gameobjects.enemy import Enemy

DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'
UP = 'up'

# Load the sword's content
ContentManager.LoadImage('sword', 'content/images/link.png')

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

	def Update(self):
		Sprite.Update(self)
		# Check for collisions with enemies if the animation is going
		if not self.isAnimPaused:
			enemies = [x for x in GlobalComm.GetState('game_objects') if isinstance(x, Enemy)]
			for x in enemies:
				if self.IsCollidingWithSprite(x):
					x.ApplyDamage(1, self.direction)

	def Render(self):
		if not self.isAnimPaused:
			Sprite.Render(self)