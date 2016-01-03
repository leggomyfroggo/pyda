import pygame
from pygame.locals import *
from gameobjects.link import Link
from gameobjects.sword import Sword
from gameobjects.goriya import Goriya
from helpers.globalcomm import GlobalComm

FRAMES_PER_SECOND = 60
DRAW_SURFACE_SIZE = (256, 224)
SCREEN_SIZE = (512, 448)

class Game():
	"""
	Represents the entire pyda game.
	"""
	def __init__(self):
		"""
		Initializes pyda.
		"""
		self.clock = pygame.time.Clock()
		self.screen = pygame.display.set_mode(SCREEN_SIZE, DOUBLEBUF)
		self.drawSurface = pygame.Surface(DRAW_SURFACE_SIZE)
		GlobalComm.SetState('draw_surface', self.drawSurface)
		self.gameObjects = []
		GlobalComm.SetState('game_objects', self.gameObjects)
		self.destroyedObjects = []
		GlobalComm.SetState('destroyed_objects', self.destroyedObjects)

	def StartGame(self):
		"""
		Starts the game.
		"""
		self.InitGameState()
		self.GameLoop()

	def InitGameState(self):
		"""
		Initializes the state of the game.
		"""
		self.gameObjects += [GlobalComm.SetState('link', Link())]
		self.gameObjects += [GlobalComm.SetState('link_sword', Sword())]
		# Test enemies
		self.gameObjects += [Goriya((128, 64))]

	def GameLoop(self):
		"""
		Runs all game and render logic in a loop.
		"""
		# Loop until the stop condition is met
		shouldRun = True
		while shouldRun:
			# Stop until the next frame
			GlobalComm.SetState('dt', self.clock.tick(FRAMES_PER_SECOND) / 1000.0)
			# Do update logic here
			self.Update()
			# Render everything
			self.drawSurface.fill((0, 0, 0))
			self.Render()

	def Update(self):
		"""
		Runs the primary game logic. Called once per frame during the game loop.
		"""
		# Get all events
		GlobalComm.SetState('events', pygame.event.get())
		GlobalComm.SetState('key_states', pygame.key.get_pressed())
		# Update all game objects
		for x in self.gameObjects:
			x.Update()
		# Get rid of destroyed objects
		for x in self.destroyedObjects:
			self.gameObjects.remove(x)

	def Render(self):
		"""
		Renders the game. Called once per frame during the game loop.
		"""
		# Sort and render all game objects by ascending z-order
		self.gameObjects.sort(key=lambda o: o.zOrder)
		for x in self.gameObjects:
			x.Render()
		# Scale the screen
		pygame.transform.scale(self.drawSurface, SCREEN_SIZE, self.screen)
		# Draw to the screen
		pygame.display.flip()

# Start the game
Game().StartGame()