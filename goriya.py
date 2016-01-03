import pygame
from pygame.locals import *
from globalcomm import GlobalComm
from enemy import Enemy

MOVE_SPEED = 30
WALK_ANIM_SPEED = 6
DIR_SWITCH_TIME = 1.5

WALK = 'walk'
STAND = 'stand'

DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'
UP = 'up'

KNOCKBACK_DURATION = 0.25
KNOCKBACK_SPEED = 90
KNOCKBACK_ANIM_SPEED = 30

class Goriya(Enemy):
	def __init__(self, Position):
		# Prepare the base
		Enemy.__init__(self, 3, (16, 16), (14, 14))
		self.position = Position
		self.direction = DOWN
		# AI stuff
		self.dirSwitchTimer = 0.0
		self.speed = (0, 0)
		self.oldSpeed = (0, 0)
		# Setup the animations
		# Walking
		self.AddAnimation('walk_down', [(0, 2, 0, 0), (0, 3, 0, 0)], WALK_ANIM_SPEED, True)
		self.AddAnimation('walk_left', [(1, 2, 0, 0), (1, 3, 0, 0)], WALK_ANIM_SPEED, True)
		self.AddAnimation('walk_up', [(2, 2, 0, 0), (2, 3, 0, 0)], WALK_ANIM_SPEED, True)
		self.AddAnimation('walk_right', [(3, 2, 0, 0), (3, 3, 0, 0)], WALK_ANIM_SPEED, True)
		self.SetAnimation('walk_down')
		# Flashing
		self.AddAnimation('knockback_spin', [(4, 2, 0, 0), (1, 2, 0, 0), (6, 2, 0, 0), (3, 2, 0, 0)], KNOCKBACK_ANIM_SPEED, True)
	def Update(self):
		self.MoveAround()
		# Update the base enemy
		Enemy.Update(self)

	def MoveAround(self):
		dt = GlobalComm.GetState('dt')
		# Only run AI if knockback isn't happening
		if not self.isKnockedBack:
			self.dirSwitchTimer += dt
			if self.dirSwitchTimer >= DIR_SWITCH_TIME:
				self.dirSwitchTimer = 0.0
				newDirection = pygame.time.get_ticks() % 4
				if newDirection == 0:
					self.direction = DOWN
					self.speed = (0, MOVE_SPEED)
				elif newDirection == 1:
					self.direction = LEFT
					self.speed = (-MOVE_SPEED, 0)
				elif newDirection == 2:
					self.direction = RIGHT
					self.speed = (MOVE_SPEED, 0)
				else:
					self.direction = UP
					self.speed = (0, -MOVE_SPEED)
				self.SetAnimation('walk_' + self.direction)
		else:
			self.knockbackTimer += dt
			if self.knockbackTimer >= KNOCKBACK_DURATION:
				self.isKnockedBack = False
				print self.oldSpeed
				self.speed = self.oldSpeed
				self.SetAnimation('walk_' + self.direction)
		self.position = (self.position[0] + self.speed[0] * dt, self.position[1] + self.speed[1] * dt)

	def ApplyDamage(self, DamageAmount, Direction):
		if Enemy.ApplyDamage(self, DamageAmount, Direction):
			self.oldSpeed = self.speed
			if Direction == DOWN:
				self.speed = (0, KNOCKBACK_SPEED)
			elif Direction == LEFT:
				self.speed = (-KNOCKBACK_SPEED, 0)
			elif Direction == RIGHT:
				self.speed = (KNOCKBACK_SPEED, 0)
			else:
				self.speed = (0, -KNOCKBACK_SPEED)
			self.SetAnimation('knockback_spin')