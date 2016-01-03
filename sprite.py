import pygame
from pygame.locals import *
from globalcomm import GlobalComm
from contentmanager import ContentManager

class Sprite:
	def __init__(self, ImageKey, TileSize, Padding):
		self.image = ContentManager.GetImageForKey(ImageKey)
		self.position = (0, 0)
		self.animations = {}
		self.frame = 0
		self.frameTimer = 0.0
		self.currentAnimation = None
		self.tileSize = TileSize 
		self.frameSize = (TileSize[0] + Padding[0], TileSize[1] + Padding[1])
		self.isAnimPaused = False
		self.zOrder = 0.0

	def SetPosition(self, Position):
		self.position = Position

	def AddAnimation(self, Name, Animation, Speed, Loop):
		self.animations[Name] = (Speed, Loop, Animation, Name)

	def SetAnimation(self, Name):
		newAnimation = self.animations[Name]
		if newAnimation is not self.currentAnimation:
			self.frame = 0
			self.currentAnimation = self.animations[Name]

	def ResetAnimation(self):
		self.frame = 0
		self.frameTimer = 0.0
		self.isAnimPaused = False

	def PauseAnimation(self, Pause):
		self.isAnimPaused = Pause

	def Update(self):
		dt = GlobalComm.GetState('dt')
		if self.currentAnimation is not None:
			if not self.isAnimPaused:
				self.frameTimer += dt * self.currentAnimation[0]
				while self.frameTimer >= 1.0:
					if self.currentAnimation[1] or self.frame < (len(self.currentAnimation[2]) - 1):
						self.frameTimer -= 1.0
						self.frame = (self.frame + 1) % len(self.currentAnimation[2])
					else:
						self.isAnimPaused = True
						self.OnAnimationFinished()
						break

	def Render(self):
		if self.currentAnimation is not None:
			# This is a four-tuple (X, Y, X-offset, Y-offset)
			currentFrame = self.currentAnimation[2][self.frame]
			startX = currentFrame[0] * self.frameSize[0]
			startY = currentFrame[1] * self.frameSize[1]
			adjustedPosition = (self.position[0] + currentFrame[2], self.position[1] + currentFrame[3])
			GlobalComm.GetState('draw_surface').blit(self.image, adjustedPosition, (startX, startY, self.tileSize[0], self.tileSize[1]))

	def OnAnimationFinished(self):
		pass

	def GetHitbox(self):
		currentFrame = self.currentAnimation[2][self.frame]
		return (self.position[0] + currentFrame[2], self.position[1] + currentFrame[3], self.tileSize[0], self.tileSize[1])

	def IsCollidingWithSprite(self, Sprite2):
		selfBox = self.GetHitbox()
		sprite2Box = Sprite2.GetHitbox()
		cond1 = selfBox[0] > (sprite2Box[0] + sprite2Box[2])
		cond2 = selfBox[1] > (sprite2Box[1] + sprite2Box[3])
		cond3 = (selfBox[0] + selfBox[2]) < sprite2Box[0]
		cond4 = (selfBox[1] + selfBox[3]) < sprite2Box[1]
		return not cond1 and not cond2 and not cond3 and not cond4