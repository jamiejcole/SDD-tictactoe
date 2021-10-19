moves = [
	'1', '2', '3',
	'4', '5', '6',
	'7', '8', '9'
]

def printBoard():
	for i, j in enumerate(moves):
		print(moves[i], end='')
		if i % 3 == 2:
			print('\n')

printBoard()


# --- OLD ---
# def printBoard():
# 	print(moves, '\n')
# 	x = 0
# 	for i in moves:
# 		if x <= 2:
# 			print(moves[int(i) - 1], moves[int(i)], moves[int(i) + 1])
# 			x+= 1
# 		else:
# 			x = 0

