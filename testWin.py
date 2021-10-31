moves = [
	'1', '1', '1',
	'1', '/', '/',
	'1', '/', '/'
]

def detectWin():
	for i in range(0, 8, 3):
		#print(i)
		if moves[i] == moves[i + 1] and moves[i] == moves[i + 2] and moves[i] != '/':
			print(i, "horizon")

	for i in range(0, 2):
		if moves[i] == moves[i + 3] and moves[i] == moves[i + 6] and moves[i] != '/':
			print(i, "colm")

# still need to do diagonals

detectWin()