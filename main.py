import sys
import os
import time
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame, pygame.freetype
from time import sleep

pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# customs
ORANGE = (255, 190, 118)
DARK_ORANGE = (240, 147, 43)
PLAYER1_COL = (34, 166, 179)
PLAYER2_COL = (104, 109, 224)

size = (600, 600)
screen = pygame.display.set_mode(size)

# setting the min and max positions for each tile
tiles = {
	"t1": ((0, 0), (200, 200)),
	"t2": ((210, 0), (400, 200)),
	"t3": ((410, 0), (600, 200)),
	"t4": ((0, 210), (200, 400)),
	"t5": ((210, 210), (400, 400)),
	"t6": ((410, 210), (600, 400)),
	"t7": ((0, 410), (200, 600)),
	"t8": ((210, 410), (400, 600)),
	"t9": ((410, 410), (600, 600)),
}

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		elif event.type == pygame.MOUSEBUTTONUP:
			pos = pygame.mouse.get_pos()
			print(pos)

	# drawing the board
	screen.fill(ORANGE)
	pygame.draw.rect(screen, DARK_ORANGE, (0, 200, 600, 10))
	pygame.draw.rect(screen, DARK_ORANGE, (0, 400, 600, 10))
	pygame.draw.rect(screen, DARK_ORANGE, (200, 0, 10, 600))
	pygame.draw.rect(screen, DARK_ORANGE, (400, 0, 10, 600))

	# drawing each point on each tile to verify coords
	for i in tiles:
		pygame.draw.circle(screen, BLUE, tiles[i][0], 5)
		pygame.draw.circle(screen, BLUE, tiles[i][1], 5)

	pygame.display.update()