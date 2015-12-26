import pygame
from pygame.locals import *

class Sprite:
	def __init__(self, Image, TileSize, Padding):
		self.image = pygame.image.load(Image)
		self.position = (0, 0)
		self.animations = {}
		self.frame = 0
		self.frameTimer = 0.0
		self.currentAnimation = None
		self.tileSize = TileSize 
		self.frameSize = (TileSize[0] + Padding[0], TileSize[1] + Padding[1])
		self.isAnimPaused = False

	def AddAnimation(self, Name, Animation, Speed, Loop):
		self.animations[Name] = (Speed, Loop, Animation, Name)

	def SetAnimation(self, Name):
		newAnimation = self.animations[Name]
		if newAnimation is not self.currentAnimation:
			self.frame = 0
			self.currentAnimation = self.animations[Name]

	def PauseAnimation(self, Pause):
		self.isAnimPaused = Pause

	def Update(self, DT, Events):
		if self.currentAnimation is not None:
			if not self.isAnimPaused:
				self.frameTimer += DT * self.currentAnimation[0]
				if self.frameTimer >= 1.0:
					self.frameTimer = 0.0
					self.frame = (self.frame + 1) % len(self.currentAnimation[2])

	def Render(self, Screen):
		if self.currentAnimation is not None:
			# This is a four-tuple (X, Y, X-offset, Y-offset)
			currentFrame = self.currentAnimation[2][self.frame]
			startX = currentFrame[0] * self.frameSize[0]
			startY = currentFrame[1] * self.frameSize[1]
			adjustedPosition = (self.position[0] + currentFrame[2], self.position[1] + currentFrame[3])
			Screen.blit(self.image, adjustedPosition, (startX, startY, self.tileSize[0], self.tileSize[1]))