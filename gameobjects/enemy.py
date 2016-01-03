import pygame
from pygame.locals import *
from helpers.globalcomm import GlobalComm
from helpers.contentmanager import ContentManager
from gameobjects.sprite import Sprite

# Load enemy content
ContentManager.LoadImage('enemies', 'content/images/enemies.png')

class Enemy(Sprite):
	"""
	Represents the abstract concept of an enemy.
	"""
	def __init__(self, Health, TileSize, Padding):
		"""
		Initializes an enemy with its basic attributes.

		Args:
			Health:		The amount of health the Enemy will have.
			TileSize:	A 2-tuple (w, h) representing the size of the Enemy's graphic tiles.
			Padding:	A 2-tuple (px, py) representing the amount of padding between tiles.
		"""
		# Prepare the base
		Sprite.__init__(self, 'enemies', TileSize, Padding)
		# Basic enemy properties
		self.health = Health
		self.destroyed = False
		self.isKnockedBack = False
		self.knockbackTimer = 0.0

	def Update(self):
		"""
		Updates the Enemy's state.
		"""
		# Update the base
		Sprite.Update(self)
		# Remove this enemy from the game if it has been destroyed
		if self.destroyed:
			GlobalComm.GetState('game_objects').remove(self)

	def ApplyDamage(self, DamageAmount, Direction):
		"""
		Applies damage to the Enemy and returns if this was successful. This should be overridden
		by inheriting classes but the base method called in the following manner:

			if Enemy.ApplyDamage(self, DamageAmount, Direction):
				# Class specific code here

		This ensures that damage is dealt in a consistent manner across Enemy types.

		Args:
			DamageAmount:	The amount of damage to deal to the Enemy.
			Direction:		The direction in which to apply damage.
		"""
		if not self.isKnockedBack:
			self.health -= DamageAmount
			self.isKnockedBack = True
			self.knockbackTimer = 0.0
			return True
		return False