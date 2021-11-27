#!/usr/bin/env python3.9
import sys
import os
import time
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame, pygame.freetype
import threading
import random
from time import sleep
import pygame_textinput
import tkinter
from tkinter import simpledialog
from tkinter import *
from macAddress import getMacAddress
import pyrebase

root = tkinter.Tk()
embed = tkinter.Frame(root, width=600, height=600)
embed.grid(columnspan=(600), rowspan=(500))
embed.pack(side=LEFT)
os.environ["SDL_WINDOWID"] = str(embed.winfo_id())

root.update()
root.withdraw()
# set screen size

pygame.display.init()
pygame.freetype.init()
clock = pygame.time.Clock()

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
GAME_FONT_SMALL = pygame.freetype.Font("OpenSans-Regular.ttf", 16)
TITLE_FONT = pygame.freetype.Font("OpenSans-Regular.ttf", 34)
TITLE_FONT_SMALL = pygame.freetype.Font("OpenSans-Regular.ttf", 22)

LEADERBOARD_FONT_TITLE = pygame.freetype.Font("OpenSans-Regular.ttf", 16)
LEADERBOARD_FONT_TEXT = pygame.freetype.Font("OpenSans-Regular.ttf", 11)

WIN_MSG_FONT = pygame.freetype.Font("OpenSans-Regular.ttf", 34)

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

global playerMoveDict
playerMoveDict = {}

global textInput
textInput = ''

global playerOneUsername
playerOneUsername = ''

global playerTwoUsername
playerTwoUsername = ''

global gameOver
gameOver = False


config = {
  "apiKey": "AIzaSyDTcEP5kkVDE1n7n1MjwBuceo3hO3BNV9o",
  "authDomain": "sdd-tictactoe.firebaseapp.com",
  "databaseURL": "https://sdd-tictactoe-default-rtdb.firebaseio.com",
  "storageBucket": "sdd-tictactoe.appspot.com"
}

firebase = pyrebase.initialize_app(config)
database = firebase.database()


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


class gameOverChecker (threading.Thread):
	def run(self):
		global gameOver
		while True:
			if gameOver == True:
				print('\nGame is over! Quitting Tic Tac Toe!')
				sleep(5)
				os._exit(1)
		
gameOverChecker = gameOverChecker()
gameOverChecker.start()



def doMainMenu():
	global mainMenuDrawn
	global mainMenuClick
	while True:
		if mainMenuDrawn != True:
			def changeUsername():
				macAddress = getMacAddress()
				#print(macAddress)

				newUsername = simpledialog.askstring('Enter Username', 'Hello! Please enter a new username for your TicTacToe account!', parent=root)
				#print(newUsername)

				currentUsername = getUsername(macAddress)

				print(newUsername)
				if newUsername != None:
					updateUsername(macAddress, newUsername)

			def changeUsernamePlayer2():
				global playerTwoUsername
				newUsername = simpledialog.askstring('Enter Username Player 2', 'Hello! Please enter a username for player 2s tictactoe account!', parent=root)
				playerTwoUsername = newUsername
				print("player 2's username:", playerTwoUsername)
				setupMenu()

			def getUsername(mac):
				users = database.child("users").get()
				#print(type(username))
				userExists = False

				for user in users.each():
					#print('mac:', user.key(), "username:", user.val())
					if mac == user.key():
						#print('User confirmed:', mac, 'username:', user.val())
						userExists = True
						return user.val()
				if userExists != True:
					return False

			def getScore(username):
				scores = database.child("scores").get()
				yourScore = []

				# finding score from name
				for user in scores:
					if user.key() == username:
						yourScore = [user.key(), user.val()]

				# finding position on leaderboard
				userScores = {}
				for user in scores:
					userScores[user.key()] = user.val()	
				sort = sorted(userScores, key=userScores.get, reverse=True)

				for i in sort:
					if i == username:
						position = sort.index(i) + 1
						yourScore.append(position)

				return yourScore



			def updateUsername(mac, username):
				oldUsername = getUsername(mac)
				oldScore = getScore(oldUsername)[2]
				#print(f"oldUsername: {oldUsername}. oldScore: {oldScore}")

				# upadting users table
				database.child("users").child(mac).set(username)
				
				# updating scroes table
				database.child("scores").child(oldUsername).remove()
				database.child("scores").child(username).set(oldScore)

				# resetup menu
				setupMenu()
				return f"updated {mac} to {username}"




			def findTopThree():
				scores = database.child("scores").get()
				userScores = {}
				topThree = {}
				for user in scores:
					userScores[user.key()] = user.val()
				
				sort = sorted(userScores, key=userScores.get, reverse=True)
				topThreePlayers = sort[:3]
				for i in topThreePlayers:
					for user in scores:
						if user.key() == i:
							topThree[i] = user.val()
				return topThree




			def setupMenu():
				global playerOneUsername
				global playerTwoUsername

				screen.fill(LIGHTBLUE)
				# Creates welcome message
				text_surface, rect = TITLE_FONT.render("Welcome to Tic Tac Toe!", (0, 0, 0))
				screen.blit(text_surface, (100, 40))

				# Finds username, and sets it to the screen
				username = getUsername(getMacAddress())
				playerOneUsername = username
				if username != False:
					setName = username
				else:
					setName = ''
				text_surface2, rect = TITLE_FONT_SMALL.render('P1: ' + setName, (0, 0, 0))
				screen.blit(text_surface2, (100, 100))

				# sets player 2 username to screen
				text_surface2, rect = TITLE_FONT_SMALL.render('P2: ' + playerTwoUsername, (0, 0, 0))
				screen.blit(text_surface2, (100, 130))

				# Multiplayer rect/text
				pygame.draw.rect(screen, ORANGE, pygame.Rect(200, 200, 200, 50),  2, 14)
				GAME_FONT.render_to(screen, (236, 215), "Multiplayer", (0, 0, 0))

				# Computer easy
				pygame.draw.rect(screen, ORANGE, pygame.Rect(200, 300, 200, 50),  2, 14)
				GAME_FONT.render_to(screen, (256, 315), "AI Easy", (0, 0, 0))

				# Computer hard
				pygame.draw.rect(screen, ORANGE, pygame.Rect(200, 400, 200, 50),  2, 14)
				GAME_FONT.render_to(screen, (256, 415), "AI Hard", (0, 0, 0))

				# button to change username
				pygame.draw.rect(screen, DARK_ORANGE, pygame.Rect(30, 530, 160, 40),  2, 14)
				GAME_FONT_SMALL.render_to(screen, (38, 540), "Change Username", (255, 255, 255))

				# button to change 2nd players username
				pygame.draw.rect(screen, DARK_ORANGE, pygame.Rect(420, 530, 160, 40),  2, 14)
				GAME_FONT_SMALL.render_to(screen, (428, 540), "Change Player 2", (255, 255, 255))

				### Leaderboard ###
				# Leaderboard title
				LEADERBOARD_FONT_TITLE.render_to(screen, (450, 150), "Leaderboard", (255, 255, 255))
				pygame.draw.line(screen, (255, 255, 255), (450, 165), (550, 165))

				# getting top three players
				topThreePlayers = findTopThree()
				playerOne = [list(topThreePlayers.keys())[0], topThreePlayers[list(topThreePlayers.keys())[0]]]
				playerTwo = [list(topThreePlayers.keys())[1], topThreePlayers[list(topThreePlayers.keys())[1]]]
				playerThree = [list(topThreePlayers.keys())[2], topThreePlayers[list(topThreePlayers.keys())[2]]]
				print(playerOne, playerTwo, playerThree)

				# setting top three players on screen
				LEADERBOARD_FONT_TEXT.render_to(screen, (450, 200), '1 '+ str(playerOne[0]), (255, 255, 255))
				LEADERBOARD_FONT_TEXT.render_to(screen, (470, 220), str(playerOne[1]) + " points", (255, 255, 255))

				LEADERBOARD_FONT_TEXT.render_to(screen, (450, 270), '2 '+ str(playerTwo[0]), (255, 255, 255))
				LEADERBOARD_FONT_TEXT.render_to(screen, (470, 290), str(playerTwo[1]) + " points", (255, 255, 255))

				LEADERBOARD_FONT_TEXT.render_to(screen, (450, 340), '3 '+ str(playerThree[0]), (255, 255, 255))
				LEADERBOARD_FONT_TEXT.render_to(screen, (470, 360), str(playerThree[1]) + " points", (255, 255, 255))

				# setting your score on screen
				try:
					yourScore = getScore(getUsername(getMacAddress()))
					LEADERBOARD_FONT_TEXT.render_to(screen, (450, 430), str(yourScore[2]) + " " + str(yourScore[0]), (255, 255, 255))
					LEADERBOARD_FONT_TEXT.render_to(screen, (470, 450), str(yourScore[1]) + " points", (255, 255, 255))

				except:
					LEADERBOARD_FONT_TEXT.render_to(screen, (450, 430), 'No data found', (255, 255, 255))

				pygame.display.update()
				root.update()

			setupMenu()
			mainMenuDrawn = True

		events = pygame.event.get()


		for event in events:
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == pygame.MOUSEBUTTONUP:
				pos = pygame.mouse.get_pos()
				x = mouseClick(pos)
				if x == 'complete':
					return
			elif event.type == pygame.KEYDOWN:
				pass

				
				#print(x, getMacAddress())

		


		def mouseClick(pos):
			global mainMenuClick
			x, y = pos[0], pos[1]
			if x >= 200 and x <= 400 and y >= 200 and y <= 250:
				print('clicked Multiplayer')
				mainMenuClick = 'multiplayer'
				return 'complete'
			elif x >= 200 and x <= 400 and y >= 300 and y <= 350:
				print('clicked ai random')
				mainMenuClick = 'random'
				return 'complete'
			elif x >= 200 and x <= 400 and y >= 400 and y <= 450:
				print('clicked ai hard')
				mainMenuClick = 'hard'
				return 'complete'
			elif x >= 30 and x <= 190 and y >= 530 and y <= 570:
				print("change username")
				changeUsername()		
			elif x >= 420 and x <= 580 and y >= 530 and y <= 570:
				print("change username for player 2")
				changeUsernamePlayer2()

		

doMainMenu()


##### PLAYER VS PLAYER 
def doGame():
	global gameHasStarted
	global gameOver
	hasBeenAwardedPoints = False
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
					displayWin(x[0])
					if hasBeenAwardedPoints == False:
						awardPoints(x[0])
						hasBeenAwardedPoints = True
						gameOver = True


		pygame.display.update()
		root.update()

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

		def displayWin(winner):
			print("winner:", winner)
			global playerOneUsername
			global playerTwoUsername
			player1 = playerOneUsername
			player2 = playerTwoUsername

			if winner == '1':
				WIN_MSG_FONT.render_to(screen, (250, 250), f"{player1} wins!", (0, 0, 0))
			elif winner == '2':
				if player2 != '':
					WIN_MSG_FONT.render_to(screen, (250, 250), f"{player2} wins!", (0, 0, 0))
				else:
					WIN_MSG_FONT.render_to(screen, (250, 250), f"(no name) wins!", (0, 0, 0))


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

		def awardPoints(player):
			global playerOneUsername
			global playerTwoUsername
			player1 = playerOneUsername
			player2 = playerTwoUsername
			winner = ''

			if player == '1':
				winner = playerOneUsername
			elif player == '2':
				if playerTwoUsername != '':
					winner = playerTwoUsername
				else:
					winner = "EmptyPlayer2"

			try:
				curScore = database.child("scores").child(winner).get().val()
				database.child("scores").child(winner).set(curScore + 10)
			except:
				pass

##### RANDOM COMPUTER MOVES #####
def doRandom():
	global gameHasStarted
	global gameOver
	hasBeenAwardedPoints = False
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
					displayWin(x[0])
					if hasBeenAwardedPoints == False:
						awardPoints(x[0])
						hasBeenAwardedPoints = True
						gameOver = True


		pygame.display.update()
		root.update()

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

		def displayWin(winner):
			print("winner:", winner)
			global playerOneUsername
			global playerTwoUsername
			player1 = playerOneUsername
			player2 = playerTwoUsername

			if winner == '1':
				WIN_MSG_FONT.render_to(screen, (250, 250), f"{player1} wins!", (0, 0, 0))
			elif winner == '2':
				WIN_MSG_FONT.render_to(screen, (250, 250), f"Bot wins!", (0, 0, 0))


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

		def awardPoints(player):
			global playerOneUsername
			player1 = playerOneUsername
			winner = ''
			points = 0

			if player == '1':
				winner = playerOneUsername
				points = 10
			elif player == '2':
				winner = playerOneUsername
				points = -10

			curScore = database.child("scores").child(winner).get().val()
			database.child("scores").child(winner).set(curScore + points)


##### MINIMAX COMPUTER MOVES #####
def doHard():
	global gameHasStarted
	global gameOver
	hasBeenAwardedPoints = False
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
					displayWin(x[0])
					if hasBeenAwardedPoints == False:
						awardPoints(x[0])
						hasBeenAwardedPoints = True
						gameOver = True


		pygame.display.update()
		root.update()

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
			global playerMoveDict
			if checkTile(tile, currentPlayer):
				x1 = tiles[tile][0][0]
				y1 = tiles[tile][0][1]
				x2 = tiles[tile][1][0]
				y2 = tiles[tile][1][1]


				pygame.draw.line(screen, PLAYER2_COL, (x1+20, y1+20), (x2-20, y2-20), 7)
				pygame.draw.line(screen, PLAYER2_COL, (x1+20, y2-20), (x2-20, y1+20), 7)
				storeMove(tile, currentPlayer)

				#Adding the player's move to the playerMove dictionary
				playerMoveDict[len(playerMoveDict) + 1] = int(tile[1]) - 1
				print(playerMoveDict)
				
				x = detectWin()
				if x != None:
					#print(x)
					drawWin(x[1], x[2])
					return
					

				def drawCircle(circleTile):
					print('circletile: ' , circleTile)
					x1 = tiles['t' + str(circleTile + 1)][0][0]
					y1 = tiles['t' + str(circleTile + 1)][0][1]
					x2 = tiles['t' + str(circleTile + 1)][1][0]
					y2 = tiles['t' + str(circleTile + 1)][1][1]
					pygame.draw.circle(screen, PLAYER2_COL, (x1+(x2-x1)/2, y1+(y2-y1)/2), 70, 7)
					storeMove('t' + str(circleTile + 1), 2)

				def findAdjacent(tile):
					print("finding adjacent tile in tile", tile)
					adjacentTiles = {
						0: (1, 3),
						2: (1, 5),
						6: (3, 7),
						8: (7, 5),
						1: (0, 2),
						3: (0, 6),
						5: (2, 8),
						7: (6, 8)
					}

					if tile not in list(adjacentTiles.keys()):
						return 'no'
					else:
						for i in adjacentTiles[tile]:
							if moves[i] == '/':
								return i
						return 'no'

				def detectTwoInARow():
					for i in range(0, 8, 3):
						if moves[i] == moves[i + 1] and moves[i + 2] == '/' and moves[i] != '/' or moves[i] == moves[i + 2] and moves[i + 1] == '/' and moves[i] != '/' or moves[i + 1] == moves[i + 2] and moves[i] == '/' and moves[i + 1] != '/':
							#print(i, "horizon")
							if moves[i] == moves[i + 1] and moves[i + 2] == '/' and moves[i] != '/':
								print('yeeman 1')
								return i + 2, moves[i]
							elif moves[i + 1] == moves[i + 2] and moves[i] == '/' and moves[i + 1] != '/':
								print('yeeman 2')
								return i, moves[i + 1]
							elif moves[i] == moves[i + 2] and moves[i + 1] == '/' and moves[i] != '/':
								print('yeeman 3')
								return i + 1, moves[i]

					for i in range(0, 3):
						print('MOVESI: ', moves[i], 'I:', i)
						if moves[i] == moves[i + 3] and moves[i + 6] == '/' and moves[i] != '/' or moves[i] == moves[i + 6] and moves[i + 3] == '/' and moves[i] != '/' or moves[i + 3] == moves[i + 6] and moves[i] == '/' and moves[i + 3] != '/':
							#print(i, "colm")
							print('MOVESI2: ', moves[i], 'I:', i)
							if moves[i] == moves[i + 3] and moves[i + 6] == '/' and moves[i] != '/':
								return i + 6, moves[i]
								print('cs1 ')
							elif moves[i + 3] == moves[i + 6] and moves[i] == '/' and moves[i + 3] != '/':
								return i, moves[i + 3]
								print('cs2 ')
							elif moves[i] == moves[i + 6] and moves[i + 3] == '/' and moves[i] != '/':
								print('cs3 ')
								return i + 3, moves[i]
						

					if moves[4] == moves[0] and moves[8] == '/' and moves[4] != '/' or moves[4] == moves[8] and moves[0] == '/' and moves[4] != '/':
						#print(i, "diag top-left bottom-right")
						if moves[4] == moves[0] and moves[8] == '/' and moves[4] != '/':
							return 8, moves[4]
						elif moves[4] == moves[8] and moves[0] == '/' and moves[4] != '/':
							return 0, moves[4]
					if moves[4] == moves[2] and moves[6] == '/' and moves[4] != '/'or moves[4] == moves[6] and moves[2] == '/'  and moves[4] != '/':
						#print(i, "diag top-right bottom-left")
						if moves[4] == moves[2] and moves[6] == '/' and moves[4] != '/':
							return 6, moves[4]
						elif moves[4] == moves[6] and moves[2] == '/'  and moves[4] != '/':
							return 2, moves[4]
					return 'no'

				satisfied = False
				attemptNo = 0
				while satisfied != True:
					if aiMoveNo == 1:
						if moves[4] == '1':
							#print('player 1 went in centre tile')
							corners = [0, 2, 6, 8]
							drawCircle(random.choice(corners))
							aiMoveNo += 1
							break
						elif moves[4] == '/':
							#print('player 1 didnt go in centre tile')
							drawCircle(4)
							aiMoveNo += 1
							break
					elif aiMoveNo == 2:
						x = detectTwoInARow()
						print(x)
						if x != 'no':
							#print('FOUND RTHE TWO IN A ROW: ', x)
							#print('x=', x)
							drawCircle(x[0])
						elif x == 'no':
							#print('DID NOT FOUND RTHE TWO IN A ROW: ', x)
							#print('2nd move, no two xs in a line...')
							# Adjacent: means next to not in a corner
							#choice = findAdjacent()
							
							#drawCircle(choice)
							lastPlayerMove = playerMoveDict[next(reversed(playerMoveDict.keys()))]
							#print('last player move:', lastPlayerMove)

							adjacentPos = findAdjacent(lastPlayerMove)
							#print("ADJACENT:", adjacentPos)

							drawCircle(adjacentPos)

							# checked = False
							# while checked != True:
							# 	corners = [0, 2, 6, 8] # Adjacent: means next to not in a corner
							# 	choice = random.choice(corners)
							# 	if moves[choice] == '/':
							# 		checked = True
							# 		drawCircle(choice)
						aiMoveNo += 1
						print('got here')
						break
					elif aiMoveNo > 2:
						print('got here 2')
						x = detectTwoInARow()
						print('newx6969:', x)
						if x != 'no' and x[1] == '1':
							print('IFSTATEMENT 1')
							drawCircle(x[0])
						elif x != 'no' and x[1] == '2':
							print('IFSTATEMENT 2')
							drawCircle(x[0])
						else:
							print('IFSTATEMENT 3')
							checked = False
							checkedNos = []
							while checked != True and len(checkedNos) < 9:
								choice = random.randint(0, 8)
								#print('tried position: ', choice)
								if moves[choice] == '/' and choice not in checkedNos:
									checked = True
									drawCircle(choice)
								else: 
									#print('position ', choice, ' contains ', moves[choice])
									if choice not in checkedNos:
										checkedNos.append(choice)
							print('DRAW!')
						aiMoveNo += 1
						break 
						# so, so, many bugs.
						# 1. will randomly decide its a draw
						# 2. when there is an obvious move for computer to make
						#    to win, it doesn't go, a line with a gap in 
						#    the middle.
						# 3. program crashes when there are 2 xs in a row and 
						#    then user goes in the 3rd spot in the row...




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


		def displayWin(winner):
			print("winner:", winner)
			global playerOneUsername
			global playerTwoUsername
			player1 = playerOneUsername
			player2 = playerTwoUsername

			if winner == '1':
				WIN_MSG_FONT.render_to(screen, (250, 250), f"{player1} wins!!", (0, 0, 0))
			elif winner == '2':
				WIN_MSG_FONT.render_to(screen, (250, 250), f"AI wins!", (0, 0, 0))

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

		def awardPoints(player):
			global playerOneUsername
			player1 = playerOneUsername
			winner = ''
			points = 0

			if player == '1':
				winner = playerOneUsername
				points = 200
			elif player == '2':
				winner = playerOneUsername
				points = -5

			curScore = database.child("scores").child(winner).get().val()
			database.child("scores").child(winner).set(curScore + points)

if mainMenuClick == 'multiplayer':
	doGame()
elif mainMenuClick == 'random':
	doRandom()
elif mainMenuClick == 'hard':
	doHard()