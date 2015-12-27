import pygame
from pygame.locals import *
from sprite import Sprite
from sword import Sword

MOVE_SPEED = 75
WALK_ANIM_SPEED = 8
SWING_SPEED = 6

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

		# Prepare Link's state info
		self.direction = DOWN
		self.isSwinging = False
		self.swingTimer = 0.0

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
		self.AddAnimation('swing_down', [(0, 2, 0, 0)], 0, True)
		self.AddAnimation('swing_left', [(1, 2, 0, 0)], 0, True)
		self.AddAnimation('swing_up', [(2, 2, 0, 0)], 0, True)
		self.AddAnimation('swing_right', [(3, 2, 0, 0)], 0, True)
		self.SetAnimation('stand_down')
		
		# Create Link's sword
		self.sword = Sword()

	def Update(self, DT, Events):
		# Update the base sprite
		Sprite.Update(self, DT, Events)

		# Grab current keyboard state
		keyStates = pygame.key.get_pressed()

		# Update movement and get position change
		moved, xChange, yChange = self.Move(DT, keyStates)

		# Check for and update swing state
		self.Swing(DT, keyStates)

		# Set an appropriate animation for the current action
		action = SWING if self.isSwinging else (WALK if moved else STAND)
		self.SetAnimation(action + '_' + self.direction)

		# Move Link
		self.position = (self.position[0] + xChange, self.position[1] + yChange)

		# Update the sword
		self.sword.Update(DT, Events)

	def Render(self, Screen):
		# Only render the sword if link is swinging
		if self.isSwinging:
			self.sword.SetPosition(self.position)
			self.sword.Render(Screen)
		# Render Link's sprite
		Sprite.Render(self, Screen)

	def Move(self, DT, KeyStates):
		moved = False
		xChange, yChange = 0, 0
		if not self.isSwinging:
			if KeyStates[K_RIGHT]:
				xChange = MOVE_SPEED * DT
				self.direction = RIGHT
				moved = True
			elif KeyStates[K_LEFT]:
				xChange = -MOVE_SPEED * DT
				self.direction = LEFT
				moved = True
			elif KeyStates[K_DOWN]:
				yChange = MOVE_SPEED * DT
				self.direction = DOWN
				moved = True
			elif KeyStates[K_UP]:
				yChange = -MOVE_SPEED * DT
				self.direction = UP
				moved = True
		return moved, xChange, yChange

	def Swing(self, DT, KeyStates):
		if not self.isSwinging:
			if KeyStates[K_a]:
				self.isSwinging = True
				self.swingTimer = 0.0
				self.sword.ResetForSwing(self.direction)
		else:
			self.swingTimer += DT * SWING_SPEED
			if self.swingTimer >= 1.0:
				self.isSwinging = False