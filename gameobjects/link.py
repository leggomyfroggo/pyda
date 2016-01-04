import pygame
from pygame.locals import *
from helpers.contentmanager import ContentManager
from helpers.globalcomm import GlobalComm
from gameobjects.sprite import Sprite
from gameobjects.sword import Sword

MOVE_SPEED = 75
WALK_ANIM_SPEED = 7
SWING_SPEED = 6

WALK = 'walk'
STAND = 'stand'
SWING = 'swing'

DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'
UP = 'up'

# Load Link's content
ContentManager.LoadImage('link', 'content/images/link.png')

# Generate Link's animations
LINK_ANIMATIONS = [
	# Standing
	('stand_down', [(0, 0, 0, 0)], 0, True),
	('stand_left', [(1, 0, 0, 0)], 0, True),
	('stand_up', [(2, 0, 0, 0)], 0, True),
	('stand_right', [(3, 1, 0, 0)], 0, True),
	# Walking
	('walk_down', [(0, 0, 0, 0), (0, 1, 0, 0)], WALK_ANIM_SPEED, True),
	('walk_left', [(1, 0, 0, 0), (1, 1, 0, 1)], WALK_ANIM_SPEED, True),
	('walk_up', [(2, 0, 0, 0), (2, 1, 0, 0)], WALK_ANIM_SPEED, True),
	('walk_right', [(3, 1, 0, 0), (3, 0, -1, 1)], WALK_ANIM_SPEED, True),
	# Swinging
	('swing_down', [(0, 2, 0, 0)], 0, True),
	('swing_left', [(1, 2, 0, 0)], 0, True),
	('swing_up', [(2, 2, 0, 0)], 0, True),
	('swing_right', [(3, 2, 0, 0)], 0, True)]

class Link(Sprite):
	"""
	Represents the player character Link.
	"""
	def __init__(self):
		"""
		Initializes an instance of Link.
		"""
		# Prepare the base
		Sprite.__init__(self, 'link', (16, 16), (14, 14))
		# Prepare Link's state info
		self.health = 0
		self.direction = DOWN
		self.isSwinging = False
		self.swingTimer = 0.0
		self.zOrder = 1.0
		self.isKnockedBack = False
		self.knockbackTimer = 0.0
		# Add link's animations
		for a in LINK_ANIMATIONS:
			self.AddAnimation(a[0], a[1], a[2], a[3])

	def Update(self):
		"""
		Updates Link's state.
		"""
		# Update the base sprite
		Sprite.Update(self)
		# Update input dependant things only if knockback isn't happening
		if not self.isKnockedBack:
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
		"""
		Moves Link's position based on key and other states.
		"""
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
		"""
		Initiates a swing of Link's sword.
		"""
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

	def ApplyDamage(self, DamageAmount, Direction):
		if not self.isKnockedBack:
			self.health -= DamageAmount
			self.isKnockedBack = True
			self.knockbackTimer = 0.0
			return True