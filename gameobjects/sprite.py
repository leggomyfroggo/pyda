import pygame
from pygame.locals import *
from helpers.globalcomm import GlobalComm
from helpers.contentmanager import ContentManager

class Sprite:
	"""
	Represents a drawable game object with animation support.
	"""
	def __init__(self, ImageKey, TileSize, Padding):
		"""
		Initializes an instance of Sprite.

		Args:
			ImageKey:	The key of an image loaded by the contentmanager to be used for this sprite.
			TileSize:	A 2-tuple (w, h) representing he size of the tiles used for this sprite.
			Padding: 	A 2-tuple (px, py) representing the padding between tiles on the sprite sheet.
		"""
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
		"""
		Sets the position of the sprite.

		Args:
			Position:	A 2-tuple (x, y) to set the Sprite position to.
		"""
		self.position = Position

	def AddAnimation(self, Name, Animation, Speed, Loop):
		"""
		Adds an animation to the sprite.

		Args:
			Name:		The name to give the animation.
			Animation:	A list containing a sequence of 4-tuples (indexx, indexy, offsetx, offsety)
						which represent the frames in the animation.
			Speed:		The speed of the animation in frames per second.
			Loop:		A boolean expressing whether or not the animation loops.
		"""
		self.animations[Name] = (Speed, Loop, Animation, Name)

	def SetAnimation(self, Name):
		"""
		Sets the current animation on the Sprite.

		Args:
			Name:	The name of a previously added animation to a set as current.
		"""
		newAnimation = self.animations[Name]
		if newAnimation is not self.currentAnimation:
			self.frame = 0
			self.currentAnimation = self.animations[Name]

	def ResetAnimation(self):
		"""
		Resets the current animation.
		"""
		self.frame = 0
		self.frameTimer = 0.0
		self.isAnimPaused = False

	def SetAnimationState(self, Pause=None):
		"""
		Sets whether or not the current animation should be paused.

		Keyword-args:
			Pause:	A boolean expressing the desired pause state of the animation.
					Ommitting this value will toggle the current state.
		"""
		self.isAnimPaused = not self.isAnimPaused if Pause is None else Pause

	def Update(self):
		"""
		Updates the current state of the Sprite. Classes inheriting from Sprite should override
		this method to perform any class specific logic. In this case, the base Update must be
		called for animations to be updated.
		"""
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
						self.__OnAnimationFinished()
						break

	def Render(self):
		"""
		Renders the sprite in its current state. Classes inheriting from Sprite should override
		this method to perform any class specific rendering. In this case, the base Render must be
		called for animations to be rendered.
		"""
		if self.currentAnimation is not None:
			# This is a four-tuple (X, Y, X-offset, Y-offset)
			currentFrame = self.currentAnimation[2][self.frame]
			startX = currentFrame[0] * self.frameSize[0]
			startY = currentFrame[1] * self.frameSize[1]
			adjustedPosition = (self.position[0] + currentFrame[2], self.position[1] + currentFrame[3])
			GlobalComm.GetState('draw_surface').blit(self.image, adjustedPosition, (startX, startY, self.tileSize[0], self.tileSize[1]))

	def GetHitbox(self):
		"""
		Returns the current hitbox of the sprite.

		Returns:
			A 4-tuple (x, y, w, h) representing the current hitbox of the sprite.
		"""
		currentFrame = self.currentAnimation[2][self.frame]
		return (self.position[0] + currentFrame[2], self.position[1] + currentFrame[3], self.tileSize[0], self.tileSize[1])

	def IsCollidingWithSprite(self, Sprite2):
		"""
		Checks if the Sprite is colliding with another sprite through a basic hitbox check.

		Args:
			Sprite2: A Sprite object to check for a collision with.

		Returns:
			A boolean representing the collision state between the two objects.
		"""
		selfBox = self.GetHitbox()
		sprite2Box = Sprite2.GetHitbox()
		cond1 = selfBox[0] > (sprite2Box[0] + sprite2Box[2])
		cond2 = selfBox[1] > (sprite2Box[1] + sprite2Box[3])
		cond3 = (selfBox[0] + selfBox[2]) < sprite2Box[0]
		cond4 = (selfBox[1] + selfBox[3]) < sprite2Box[1]
		return not cond1 and not cond2 and not cond3 and not cond4

	def __OnAnimationFinished(self):
		"""
		Called upon completion of a non-looping animation.
		"""
		pass