import pygame
from pygame.locals import *
from helpers.globalcomm import GlobalComm
from helpers.contentmanager import ContentManager
from gameobjects.sprite import Sprite

# Load enemy content
ContentManager.LoadImage('enemies', 'content/images/enemies.png')

class Enemy(Sprite):
	def __init__(self, Health, TileSize, Padding):
		# Prepare the base
		Sprite.__init__(self, 'enemies', TileSize, Padding)
		# Basic enemy properties
		self.health = Health
		self.destroyed = False
		self.isKnockedBack = False
		self.knockbackTimer = 0.0

	def Update(self):
		# Update the base
		Sprite.Update(self)
		# Remove this enemy from the game if it has been destroyed
		if self.destroyed:
			GlobalComm.GetState('game_objects').remove(self)

	def ApplyDamage(self, DamageAmount, Direction):
		if not self.isKnockedBack:
			self.health -= DamageAmount
			self.isKnockedBack = True
			self.knockbackTimer = 0.0
			return True
		return False