import sys
import os
import time
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame, pygame.freetype
import threading
import random
from time import sleep

pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# customs
ORANGE = (255, 190, 118)
LIGHTBLUE = (75, 123, 236)
DARK_ORANGE = (240, 147, 43)
PLAYER1_COL = (34, 166, 179)
PLAYER2_COL = (104, 109, 224)

size = (600, 600)
screen = pygame.display.set_mode(size)
GAME_FONT = pygame.freetype.Font("OpenSans-Regular.ttf", 24)
TITLE_FONT = pygame.freetype.Font("OpenSans-Regular.ttf", 34)
currentPlayer = 1

global gameHasStarted
gameHasStarted = False
global mainMenuDrawn
mainMenuDrawn = False

hasWon = False

global mainMenuClick
mainMenuClick = ''

global quitGame
quitGame = False

global aiMoveNo
aiMoveNo = 1

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

class menuManager (threading.Thread):
	def run(self):
		global mainMenuClick
		while True:
			if mainMenuClick == 'multiplayer':
				doGame()
				print('did multiplarey')
			else:
				print('e')
				sleep(0.5)
		#print('hello')


#menuManager = menuManager()
#menuManager.start()


def doMainMenu():
	global mainMenuDrawn
	global mainMenuClick
	while True:
		if mainMenuDrawn != True:
			def setupMenu():
				screen.fill(LIGHTBLUE)
				text_surface, rect = TITLE_FONT.render("Welcome to Tic Tac Toe!", (0, 0, 0))
				screen.blit(text_surface, (100, 40))

				# Multiplayer rect/text
				pygame.draw.rect(screen, ORANGE, pygame.Rect(200, 200, 200, 50),  2, 14)
				GAME_FONT.render_to(screen, (236, 215), "Multiplayer", (0, 0, 0))

				# Computer easy
				pygame.draw.rect(screen, ORANGE, pygame.Rect(200, 300, 200, 50),  2, 14)
				GAME_FONT.render_to(screen, (256, 315), "AI Easy", (0, 0, 0))

				# Computer hard
				pygame.draw.rect(screen, ORANGE, pygame.Rect(200, 400, 200, 50),  2, 14)
				GAME_FONT.render_to(screen, (256, 415), "AI Hard", (0, 0, 0))



				pygame.display.update()
			setupMenu()
			mainMenuDrawn = True


		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == pygame.MOUSEBUTTONUP:
				pos = pygame.mouse.get_pos()
				mouseClick(pos)
				return

		def mouseClick(pos):
			global mainMenuClick
			x, y = pos[0], pos[1]
			if x >= 200 and x <= 400 and y >= 200 and y <= 250:
				print('clicked Multiplayer')
				mainMenuClick = 'multiplayer'
			elif x >= 200 and x <= 400 and y >= 300 and y <= 350:
				print('clicked ai random')
				mainMenuClick = 'random'
			elif x >= 200 and x <= 400 and y >= 400 and y <= 450:
				print('clicked ai hard')
				mainMenuClick = 'hard'

		#pygame.display.update()


doMainMenu()


##### PLAYER VS PLAYER 
def doGame():
	global gameHasStarted
	while True:
		if gameHasStarted != True:
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
			gameHasStarted = True


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
			pygame.draw.line(screen, BLACK, startCentre, endCentre, 14)


##### RANDOM COMPUTER MOVES #####
def doRandom():
	global gameHasStarted
	while True:
		if gameHasStarted != True:
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
			gameHasStarted = True


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


				pygame.draw.line(screen, PLAYER2_COL, (x1+20, y1+20), (x2-20, y2-20), 7)
				pygame.draw.line(screen, PLAYER2_COL, (x1+20, y2-20), (x2-20, y1+20), 7)
				#else:
				#	xx = x2 - x1
				#	yy = y2 - y1
				#	mid = (xx, yy)
					

				#pygame.display.flip()
				storeMove(tile, currentPlayer)

				
				x = detectWin()
				if x != None:
					print(x)
					drawWin(x[1], x[2])
					
				satisfied = False
				attemptNo = 0
				while satisfied != True:
					randNum = random.randint(0, 8)
					print('rand num: ', randNum)
					if moves[randNum] == '/':
						satisfied = True
						x1 = tiles['t' + str(randNum + 1)][0][0]
						y1 = tiles['t' + str(randNum + 1)][0][1]
						x2 = tiles['t' + str(randNum + 1)][1][0]
						y2 = tiles['t' + str(randNum + 1)][1][1]
						pygame.draw.circle(screen, PLAYER2_COL, (x1+(x2-x1)/2, y1+(y2-y1)/2), 70, 7)
						storeMove('t' + str(randNum + 1), 2)
					else:
						attemptNo += 1
						if attemptNo >= 10:
							return

				#if currentPlayer == 1:
				#	currentPlayer = 2
				#else:
				#	currentPlayer = 1

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
			pygame.draw.line(screen, BLACK, startCentre, endCentre, 14)


##### MINIMAX COMPUTER MOVES #####
def doHard():
	global gameHasStarted
	while True:
		if gameHasStarted != True:
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
			gameHasStarted = True


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
			global aiMoveNo
			if checkTile(tile, currentPlayer):
				x1 = tiles[tile][0][0]
				y1 = tiles[tile][0][1]
				x2 = tiles[tile][1][0]
				y2 = tiles[tile][1][1]


				pygame.draw.line(screen, PLAYER2_COL, (x1+20, y1+20), (x2-20, y2-20), 7)
				pygame.draw.line(screen, PLAYER2_COL, (x1+20, y2-20), (x2-20, y1+20), 7)
				storeMove(tile, currentPlayer)
				
				x = detectWin()
				if x != None:
					print(x)
					drawWin(x[1], x[2])
					

				def drawCircle(circleTile):
					x1 = tiles['t' + str(circleTile + 1)][0][0]
					y1 = tiles['t' + str(circleTile + 1)][0][1]
					x2 = tiles['t' + str(circleTile + 1)][1][0]
					y2 = tiles['t' + str(circleTile + 1)][1][1]
					pygame.draw.circle(screen, PLAYER2_COL, (x1+(x2-x1)/2, y1+(y2-y1)/2), 70, 7)
					storeMove('t' + str(circleTile + 1), 2)

				def detectTwoInARow():
					for i in range(0, 8, 3):
						if moves[i] == moves[i + 1] and moves[i + 2] == '/' and moves[i] != '/' or moves[i + 1] == moves[i + 2] and moves[i] == '/' and moves[i + 1] != '/':
							#print(i, "horizon")
							if moves[i] == moves[i + 1] and moves[i + 2] == '/' and moves[i] != '/':
								return i + 2
							elif moves[i + 1] == moves[i + 2] and moves[i] == '/' and moves[i + 1] != '/':
								return i

					for i in range(0, 3):
						if moves[i] == moves[i + 3] and moves[i + 6] == '/' and moves[i] != '/' or moves[i + 3] == moves[i + 6] and moves[i] == '/' and moves[i + 3] != '/':
							#print(i, "colm")
							if moves[i] == moves[i + 3] and moves[i + 6] == '/' and moves[i] != '/':
								return i + 6
							elif moves[i + 3] == moves[i + 6] and moves[i] == '/' and moves[i + 3] != '/':
								return i

					if moves[4] == moves[0] and moves[8] == '/' and moves[4] != '/' or moves[4] == moves[8] and moves[0] == '/' and moves[4] != '/':
						#print(i, "diag top-left bottom-right")
						if moves[4] == moves[0] and moves[8] == '/' and moves[4] != '/':
							return 8
						elif moves[4] == moves[8] and moves[0] == '/' and moves[4] != '/':
							return 0
					if moves[4] == moves[2] and moves[6] == '/' and moves[4] != '/'or moves[4] == moves[6] and moves[2] == '/'  and moves[4] != '/':
						#print(i, "diag top-right bottom-left")
						if moves[4] == moves[2] and moves[6] == '/' and moves[4] != '/':
							return 6
						elif moves[4] == moves[6] and moves[2] == '/'  and moves[4] != '/':
							return 2
					return 'no'

				satisfied = False
				attemptNo = 0
				while satisfied != True:
					if aiMoveNo == 1:
						if moves[4] == '1':
							print('player 1 went in centre tile')
							corners = [0, 2, 6, 8]
							drawCircle(random.choice(corners))
							aiMoveNo += 1
							break
						elif moves[4] == '/':
							print('player 1 didnt go in centre tile')
							drawCircle(4)
							aiMoveNo += 1
							break
					elif aiMoveNo == 2:
						x = detectTwoInARow()
						print(x)
						if x != 'no':
							drawCircle(x)
						elif x == 'no':
							print('2nd move, no two xs in a line...')
							checked = False
							while checked != True:
								corners = [0, 2, 6, 8]
								choice = random.choice(corners)
								if moves[choice] == '/':
									checked = True
									drawCircle(choice)
						aiMoveNo += 1
						break
					elif aiMoveNo == 3:
						x = detectTwoInARow()
						print(x)
						if x != 'no':
							drawCircle(x)
						elif x == 'no':
							print('cry')




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
			pygame.draw.line(screen, BLACK, startCentre, endCentre, 14)

if mainMenuClick == 'multiplayer':
	doGame()
elif mainMenuClick == 'random':
	doRandom()
elif mainMenuClick == 'hard':
	doHard()