import sys
import os
import time
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame, pygame.freetype
import threading
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
currentPlayer = 1

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

moves = [
	'/', '/', '/',
	'/', '/', '/',
	'/', '/', '/'
]



def setupBoard():
	# drawing the board
	screen.fill(ORANGE)
	pygame.draw.rect(screen, DARK_ORANGE, (0, 200, 600, 10))
	pygame.draw.rect(screen, DARK_ORANGE, (0, 400, 600, 10))
	pygame.draw.rect(screen, DARK_ORANGE, (200, 0, 10, 600))
	pygame.draw.rect(screen, DARK_ORANGE, (400, 0, 10, 600))

	# drawing each point on each tile to verify coords
	#for i in tiles:
	#	pygame.draw.circle(screen, BLUE, tiles[i][0], 5)
	#	pygame.draw.circle(screen, BLUE, tiles[i][1], 5)


setupBoard()


hasWon = False

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		elif event.type == pygame.MOUSEBUTTONUP:
			pos = pygame.mouse.get_pos()
			mouseClick(pos)
			x = detectWin()
			if x != None:
				print(x)
				drawWin(x[1], x[2])


	pygame.display.update()

	def mouseClick(pos):
		x, y = pos[0], pos[1]
		for i in tiles:
			if x >= tiles[i][0][0] and x < tiles[i][1][0]:
				if y >= tiles[i][0][1] and y < tiles[i][1][1]:
					drawTile(i)
					return

	def drawTile(tile):
		global currentPlayer
		if checkTile(tile, currentPlayer):
			x1 = tiles[tile][0][0]
			y1 = tiles[tile][0][1]
			x2 = tiles[tile][1][0]
			y2 = tiles[tile][1][1]

			if currentPlayer == 1:
				pygame.draw.line(screen, PLAYER2_COL, (x1+20, y1+20), (x2-20, y2-20), 7)
				pygame.draw.line(screen, PLAYER2_COL, (x1+20, y2-20), (x2-20, y1+20), 7)
			else:
				xx = x2 - x1
				yy = y2 - y1
				mid = (xx, yy)
				pygame.draw.circle(screen, PLAYER2_COL, (x1+(x2-x1)/2, y1+(y2-y1)/2), 70, 7)

			#pygame.display.flip()
			storeMove(tile, currentPlayer)

			if currentPlayer == 1:
				currentPlayer = 2
			else:
				currentPlayer = 1

	def checkTile(tile, player):
		global hasWon
		print('has won:', hasWon)
		x = tile[1]
		return True if (moves[int(x) - 1] == '/' and hasWon == False) else False

	def storeMove(tile, currentPlayer):
		x = tile[1]
		moves[int(x) - 1] = str(currentPlayer)
		#printBoard()

	def printBoard():
		for i, j in enumerate(moves):
			print(moves[i], end='')
			if i % 3 == 2:
				print('\n')
		print('\n\n')

	def detectWin():
		global hasWon
		for i in range(0, 8, 3):
			if moves[i] == moves[i + 1] and moves[i] == moves[i + 2] and moves[i] != '/':
				#print(i, "horizon")
				hasWon = True, moves[i]
				return moves[i], i, i + 2

		for i in range(0, 3):
			if moves[i] == moves[i + 3] and moves[i] == moves[i + 6] and moves[i] != '/':
				#print(i, "colm")
				hasWon = True, moves[i]
				return moves[i], i, i + 6

		if moves[4] == moves[0] and moves[4] == moves[8] and moves[4] != '/':
			#print(i, "diag top-left bottom-right")
			hasWon = True, moves[i]
			return moves[4], 0, 8
		if moves[4] == moves[2] and moves[4] == moves[6] and moves[4] != '/':
			#print(i, "diag top-right bottom-left")
			hasWon = True, moves[i]
			return moves[4], 2, 6



	def drawWin(pos1, pos2):
		print(pos1, pos2)
		tileStart = tiles['t' + str(pos1 + 1)]  # ((0, 210), (200, 400))
		tileEnd = tiles['t' + str(pos2 + 1)]   # ((0, 210), (200, 400))

		# grabbing the centre of each tile
		sx1 = tileStart[0][0]
		sy1 = tileStart[0][1]
		sx2 = tileStart[1][0]
		sy2 = tileStart[1][1]

		ex1 = tileEnd[0][0]
		ey1 = tileEnd[0][1]
		ex2 = tileEnd[1][0]
		ey2 = tileEnd[1][1]

		startCentre = (sx1+(sx2-sx1)/2, sy1+(sy2-sy1)/2)
		endCentre = (ex1+(ex2-ex1)/2, ey1+(ey2-ey1)/2)
		pygame.draw.line(screen, BLUE, startCentre, endCentre, 14)





















