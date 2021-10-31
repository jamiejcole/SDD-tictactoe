moves = [
	'/', '/', '/',
	'/', '/', '/',
	'/', '/', '/'
]

def detectWin():
	#if moves[0] == moves[1] and moves [0] == moves[2]:
		#return moves[0], 0, 2

	for i in range(0, 8, 3):
		#print(i)
		if moves[i] == moves[i + 1] and moves [i] == moves[i + 2] and moves[i] != '/':
			print(i, "yeeman")

# still need to do columns in the for loop
# and diagonals




detectWin()