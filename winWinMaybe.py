moves = [
	'1', '1', '1',
	'/', '/', '/',
	'/', '/', '/'
]

def detectWin():
	if moves[0] == moves[1] and moves [0] == moves[2]:
		return moves[0], 0, 2

	elif moves[0] == player and moves[6] == player:
		return tiles[0], tiles[6]

	elif moves[0] == player and moves[8] == player:
		return tiles[0], tiles[8]
	elif moves[1] == player and moves[7] == player:
		return tiles[1], tiles[7]
	elif moves[2] == player and moves[6] == player:
		return tiles[2], tiles[6]
	elif moves[3] == player and moves[5] == player:
		return tiles[3], tiles[5]

	elif moves[2] == player and moves[8] == player:
		return moves[2], moves[8]

	elif moves[6] == player and moves[8] == player:
		return moves[6], moves[8]
else:
	#print('hasnt won yet')
	return False
	print('\n\n')



	