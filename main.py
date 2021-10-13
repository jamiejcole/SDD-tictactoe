import sys
import time
import pygame, pygame.freetype

pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

size = (700, 500)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("TicTacToe")

font = pygame.freetype.Font("opensans.ttf", 30)

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

	screen.fill(RED)
	
	textSurface = font.render("Hello there", (0, 0, 0))
	screen.blit(textSurface, (0, 0))


	pygame.display.update()