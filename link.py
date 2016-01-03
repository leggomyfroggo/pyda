import pygame
from pygame.locals import *
from contentmanager import ContentManager
from globalcomm import GlobalComm
from sprite import Sprite
from sword import Sword

MOVE_SPEED = 75
WALK_ANIM_SPEED = 6
SWING_SPEED = 6

WALK = 'walk'
STAND = 'stand'
SWING = 'swing'

DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'
UP = 'up'

# Load Link's content
ContentManager.LoadImage('link', 'Images/link.png')

class Link(Sprite):
	def __init__(self):
		# Prepare the base
		Sprite.__init__(self, 'link', (16, 16), (14, 14))
		# Prepare Link's state info
		self.direction = DOWN
		self.isSwinging = False
		self.swingTimer = 0.0
		self.zOrder = 1.0
		# Add link's animations
		# Standing
		self.AddAnimation('stand_down', [(0, 0, 0, 0)], 0, True)
		self.AddAnimation('stand_left', [(1, 0, 0, 0)], 0, True)
		self.AddAnimation('stand_up', [(2, 0, 0, 0)], 0, True)
		self.AddAnimation('stand_right', [(3, 1, 0, 0)], 0, True)
		# Walking
		self.AddAnimation('walk_down', [(0, 0, 0, 0), (0, 1, 0, 0)], WALK_ANIM_SPEED, True)
		self.AddAnimation('walk_left', [(1, 0, 0, 0), (1, 1, 0, 0)], WALK_ANIM_SPEED, True)
		self.AddAnimation('walk_up', [(2, 0, 0, 0), (2, 1, 0, 0)], WALK_ANIM_SPEED, True)
		self.AddAnimation('walk_right', [(3, 1, 0, 0), (3, 0, -1, 0)], WALK_ANIM_SPEED, True)
		# Swinging
		self.AddAnimation('swing_down', [(0, 2, 0, 0)], 0, True)
		self.AddAnimation('swing_left', [(1, 2, 0, 0)], 0, True)
		self.AddAnimation('swing_up', [(2, 2, 0, 0)], 0, True)
		self.AddAnimation('swing_right', [(3, 2, 0, 0)], 0, True)
		self.SetAnimation('stand_down')

	def Update(self):
		# Update the base sprite
		Sprite.Update(self)
		# Update movement and get position change
		moved, xChange, yChange = self.Move()
		# Check for and update swing state
		self.Swing()
		# Set an appropriate animation for the current action
		action = SWING if self.isSwinging else (WALK if moved else STAND)
		self.SetAnimation(action + '_' + self.direction)
		# Move Link
		self.position = (self.position[0] + xChange, self.position[1] + yChange)

	def Move(self):
		keyStates = GlobalComm.GetState('key_states')
		dt = GlobalComm.GetState('dt')
		moved = False
		xChange, yChange = 0, 0
		if not self.isSwinging:
			if keyStates[K_RIGHT]:
				xChange = MOVE_SPEED * dt
				self.direction = RIGHT
				moved = True
			elif keyStates[K_LEFT]:
				xChange = -MOVE_SPEED * dt
				self.direction = LEFT
				moved = True
			elif keyStates[K_DOWN]:
				yChange = MOVE_SPEED * dt
				self.direction = DOWN
				moved = True
			elif keyStates[K_UP]:
				yChange = -MOVE_SPEED * dt
				self.direction = UP
				moved = True
		return moved, xChange, yChange

	def Swing(self):
		keyStates = GlobalComm.GetState('key_states')
		sword = GlobalComm.GetState('link_sword')
		dt = GlobalComm.GetState('dt')
		if not self.isSwinging:
			if keyStates[K_a]:
				self.isSwinging = True
				self.swingTimer = 0.0
				sword.ResetForSwing(self.position, self.direction)
		else:
			self.swingTimer += dt * SWING_SPEED
			if self.swingTimer >= 1.0:
				self.isSwinging = False
				# DEACTIVATE SWORD HERE