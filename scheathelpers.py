#constants
board_side_range = [4, 5] 
max_allowed_wordlen = 8 #maximum allowed word length in scramble
min_allowed_wordlen = 3 #minimum allowed word length in scramble

#function definitions
def read_dictionary(filename='words', words=[]):
	"""Read dictionary file

	This function reads a word list from the dictionary file"""

	max_wordlen = 0
	wordnum = 0
	lines = 0
	print "Trying to read %s..." % filename,
	try:
		dictionaryfile = open(filename)
		for word in dictionaryfile:
			lines += 1
			word = word.strip().lower().replace("qu","q")
			wordlen = scramble_wordlen(word)
			if wordlen < min_allowed_wordlen or wordlen > max_allowed_wordlen:
				continue
			words.append(word)
			if wordlen > max_wordlen:
				max_wordlen = wordlen
			wordnum += 1
		print "done."
		print "%d lines read." % lines
		print "%d words read." % wordnum
		print "Maximum word length: %d" % max_wordlen
	except IOError:
		print "\n%s could not be opened! Exiting..." % filename
		return False
	else:
		dictionaryfile.close()
		return words

def scramble_wordlen(word):
	"Gets the scramble word length of a word"
	return len(word) - word.count("qu") #scramble counts "qu" as one tile

def createTiles(letters):
	"""This function takes in letters and returns a list of tiles based on them"""
	tiles = []
	i=0
	letterslen = len(letters)
	while i<letterslen:
		letter = letters[i]
		if not letter.isalpha():
			raise InvalidCharError
		if letter=='q' and i+1<letterslen and letters[i+1]=='u':
			letter = 'q'
			i+=1
		tiles.append(Tile(letter))
		i+=1
	tileslen = len(tiles)
	for board_side in board_side_range:
		if board_side*board_side==tileslen:
			bs = board_side
			break
	else:
		raise WrongBoardSizeError

	#add adjacent list
	for i in range(tileslen):
		row = i/bs
		col = i%bs
		adj = []

		for j in range(row-1,row+2):
			#we are in top or bottom row
			if j<0 or j>bs-1:
				continue
			for k in range(col-1,col+2):
				#we are in left or right column or this is the tile itself
				if k<0 or k>bs-1 or (k==col and j==row):
					continue
				index = (j*bs)+k
				adj.append(tiles[index])
		tiles[i].setAdjacent(adj)

	return tiles,tileslen

def findWord(word,board,wordpos,tile,wordlen):
	"""Tries to form the word on the board by recursively calling itself"""

	if word[wordpos]==tile.letter and not tile.used:
		tile.used = True
		if wordpos+1==wordlen:
			return True
		for nexttile in tile.adjacent:
			if findWord(word,board,wordpos+1,nexttile,wordlen):
				return True
		tile.used = False
	else:
		return False
		

def setUnused(board):
	"""Sets all tiles back to unused state"""
	for tile in board:
		tile.used = False

#class definitions
class Tile:
	"""Models a scramble tile

	Attributes description:
	1) letter - The letter(s) this tile represents
	2) len - The length of this tile (can only be 1 or 2)
	2) used - Initialized as false, this attribute represents the used state of the tile
	3) adjacent - A list containing the tiles adjacent to this tile
	
	Methods description:
	1) __init__ - Initializes instance of this class. Takes in the letter(s) this tile represents. Sets 'letter', 'len', and 'used' attributes
	2) setAdjacent - Sets the list of adjacent tiles"""

	def __init__(self, letter):
		self.letter = letter
		self.len = len(self.letter)
		self.used = False
	
	def setAdjacent(self, adj):
		self.adjacent = adj

class WrongBoardSizeError(Exception):
	"""Exception raised for wrong board size."""
	pass

class InvalidCharError(Exception):
	"""Exception raised for invalid character."""
	pass
