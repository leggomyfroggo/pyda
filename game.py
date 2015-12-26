import pygame
from pygame.locals import *
from link import Link

FRAMES_PER_SECOND = 60


def Init():
	# Setup the screen and clock
	screen = pygame.display.set_mode((256, 224), DOUBLEBUF)
	clock = pygame.time.Clock()

	# Start the game loop
	GameLoop(screen, clock)

def GameLoop(Screen, Clock):
	# A list of game objects
	gameObjects = []

	# Add a temp sprite
	testLink = Link()
	gameObjects += [testLink]

	# Loop until the stop condition is met
	shouldRun = True
	while shouldRun:
		# Stop until the next frame
		dt = Clock.tick(FRAMES_PER_SECOND) / 1000.0

		# Do update logic here
		Update(dt, gameObjects)

		# Render everything
		Screen.fill((0, 0, 0))
		Render(gameObjects, Screen)

def Update(DT, GameObjects):
	# Get all events
	events = pygame.event.get()

	# Update all game objects
	for x in GameObjects:
		x.Update(DT, events)

def Render(GameObjects, Screen):
	# Render all game objects
	for x in GameObjects:
		x.Render(Screen)

	# Draw to the screen
	pygame.display.flip()

# Init the game
Init()