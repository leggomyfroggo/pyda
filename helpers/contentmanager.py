import pygame
from pygame.locals import *

class __ContentManager:
	"""
	A class used for managing the loading of content which can be accessed globally.
	"""
	def __init__(self):
		"""
		Initializes the ContentManager.
		"""
		self.imagesForKey = {}
		self.keysForImage = {}

	def LoadImage(self, Key, ImagePath):
		"""
		Attempts to load an image.

		Args:
			Key:		The key to associate with the image being loaded.
			ImagePath:	The path of the image to load.
		"""
		if not self.imagesForKey.get(Key):
			if not self.keysForImage.get(ImagePath):
				self.imagesForKey[Key] = pygame.image.load(ImagePath)
				self.keysForImage[ImagePath] = Key
			else:
				self.imagesForKey[Key] = self.imagesForKey[self.keysForImage[ImagePath]]
		else:
			print 'Warning: Image with key', Key, 'already exists.'

	def GetImageForKey(self, Key):
		"""
		Gets an image that has been previously loaded.

		Args:
			Key: The key of the image to get.

		Returns:
			A pygame Image representing the requested image.
		"""
		image = self.imagesForKey.get(Key)
		if image is None:
			print 'Warning: No image for key', Key
		return image

ContentManager = __ContentManager()