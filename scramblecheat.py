#!/usr/bin/python
import sys
import readline
from scheathelpers import *

if len(sys.argv)!=2:
	print "Usage: scramblecheat.py <dictionary file>"
	exit()

words = read_dictionary(filename=sys.argv[1])

if not words:
	exit()

print "\nFor instructions, type 'help'. To exit the program, press the Enter key.\n"
instructions = """Welcome to the Scramble Cheater

To access this instruction again, enter "help".
To exit the program, enter an empty string.
To enter a board, key in the letters on the board in the order from left to right from top to bottom:

For example, if the board is

A B C D
E F G H
I J K L
M N Qu P

key in "abcdefghijklmnqup" or "abcdefghijklmnqp"

Notes:
1) In the case of the "Qu" tiles, the "u" is optional. However, if a "u" follows a "q", the program will take them to mean one tile
2) This program accepts only 4 by 4 and 5 by 5 boards
"""
while True:
	letters = raw_input("Enter a board >> ").strip().lower()
	if letters == "help":
		print instructions
		continue
	
	if not len(letters):
		break
	
	try:
		board,boardsize = createTiles(letters)
	except WrongBoardSizeError:
		print "There must be either 16 tiles or 25 tiles, genius. Cheat with intelligence!\n"
		continue
	except InvalidCharError:
		print "Only alphabets are valid tiles, Einstein. Cheat with intelligence!\n"
		continue
	
	for word in words:
		for tile in board:
			if findWord(word,board,0,tile,len(word)):
				print word.replace("q","qu")
				setUnused(board)
				break

print "Thanks for using the python scramble cheat, you disgusting creature!"
