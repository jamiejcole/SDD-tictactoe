moves = [
	'/', '/', '/',
	'/', '/', '/',
	'1', '1', '1'
]

def detectWin():
	for i in range(0, 8, 3):
		if moves[i] == moves[i + 1] and moves[i] == moves[i + 2] and moves[i] != '/':
			#print(i, "horizon")
			return moves[i], i, i + 2

	for i in range(0, 2):
		if moves[i] == moves[i + 3] and moves[i] == moves[i + 6] and moves[i] != '/':
			#print(i, "colm")
			return moves[i], i, i + 6

	if moves[4] == moves[0] and moves[4] == moves[8] and moves[4] != '/':
		#print(i, "diag top-left bottom-right")
		return moves[4], 0, 8
	if moves[4] == moves[2] and moves[4] == moves[6] and moves[4] != '/':
		#print(i, "diag top-right bottom-left")
		return moves[4], 2, 6

# still need to do diagonals

print(detectWin())