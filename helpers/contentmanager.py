import pygame
from pygame.locals import *

class __ContentManager__:
	def __init__(self):
		self.imagesForKey = {}
		self.keysForImage = {}

	def LoadImage(self, Key, ImagePath):
		if not self.imagesForKey.get(Key):
			if not self.keysForImage.get(ImagePath):
				self.imagesForKey[Key] = pygame.image.load(ImagePath)
				self.keysForImage[ImagePath] = Key
			else:
				self.imagesForKey[Key] = self.imagesForKey[self.keysForImage[ImagePath]]
		else:
			print 'Warning: Image with key', Key, 'already exists.'

	def GetImageForKey(self, Key):
		image = self.imagesForKey.get(Key)
		if image is None:
			print 'Warning: No image for key', Key
		return image

ContentManager = __ContentManager__()