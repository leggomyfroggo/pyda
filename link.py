import pygame
from pygame.locals import *
from sprite import Sprite

MOVE_SPEED = 75
WALK_ANIM_SPEED = 8

WALK = 'walk'
STAND = 'stand'
SWING = 'swing'

DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'
UP = 'up'

class Link(Sprite):
	def __init__(self):
		# Prepare the base
		Sprite.__init__(self, 'Images/link.png', (16, 16), (14, 14))
		self.direction = DOWN
		# Add link's animations
		# Standing
		self.AddAnimation('stand_down', [(0, 0, 0, 0)], 0, True)
		self.AddAnimation('stand_left', [(1, 0, 0, 0)], 0, True)
		self.AddAnimation('stand_up', [(2, 0, 0, 0)], 0, True)
		self.AddAnimation('stand_right', [(3, 0, -1, 0)], 0, True)
		# Walking
		self.AddAnimation('walk_down', [(0, 0, 0, 0), (0, 1, 0, 0)], WALK_ANIM_SPEED, True)
		self.AddAnimation('walk_left', [(1, 0, 0, 0), (1, 1, 0, 0)], WALK_ANIM_SPEED, True)
		self.AddAnimation('walk_up', [(2, 0, 0, 0), (2, 1, 0, 0)], WALK_ANIM_SPEED, True)
		self.AddAnimation('walk_right', [(3, 0, -1, 0), (3, 1, 0, 0)], WALK_ANIM_SPEED, True)
		# Swinging
		self.AddAnimation('swing_down', [(0, 2, 0, 0)], WALK_ANIM_SPEED, True)
		self.AddAnimation('swing_left', [(1, 2, 0, 0)], WALK_ANIM_SPEED, True)
		self.AddAnimation('swing_up', [(2, 2, 0, 0)], WALK_ANIM_SPEED, True)
		self.AddAnimation('swing_right', [(3, 2, 0, 0)], WALK_ANIM_SPEED, True)
		self.SetAnimation('stand_down')
		# Set links initial direction

	def Update(self, DT, Events):
		# Update the base sprite
		Sprite.Update(self, DT, Events)
		# Check for movement control stuff
		keyStates = pygame.key.get_pressed()
		moved = True
		swung = False
		xChange, yChange = 0, 0
		if keyStates[K_RIGHT]:
			xChange = MOVE_SPEED * DT
			self.direction = RIGHT
		elif keyStates[K_LEFT]:
			xChange = -MOVE_SPEED * DT
			self.direction = LEFT
		elif keyStates[K_DOWN]:
			yChange = MOVE_SPEED * DT
			self.direction = DOWN
		elif keyStates[K_UP]:
			yChange = -MOVE_SPEED * DT
			self.direction = UP
		else:
			moved = False
		action = WALK if moved else (SWING if swung else STAND)
		self.SetAnimation(action + '_' + self.direction)

		self.position = (self.position[0] + xChange, self.position[1] + yChange)
