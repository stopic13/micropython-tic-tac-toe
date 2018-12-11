# main.py -- put your code here
import pyb
import lcd160cr
from random import randint
from time import sleep
lcd = lcd160cr.LCD160CR('X')

#constants
SCREEN_WIDTH = 128
SCREEN_HEIGHT = 160

VERTICAL_POINT_1 = 50
VERTICAL_POINT_2 = 112

HORIZONTAL_POINT_1 = 42
HORIZONTAL_POINT_2 = 86

X_LENGTH = 8
O_RADIUS = 10
PADDING = 4

#variables
x_turn = True

board = [None,None,None,None,None,None,None,None,None]

sw = pyb.Switch()

def draw_board():
	global x_turn
	global board
	x_turn = True
	board = [None,None,None,None,None,None,None,None,None]
	lcd.erase()
	lcd.line(0,VERTICAL_POINT_1,SCREEN_WIDTH,VERTICAL_POINT_1)
	lcd.line(0,VERTICAL_POINT_2,SCREEN_WIDTH,VERTICAL_POINT_2)
	lcd.line(HORIZONTAL_POINT_1,0,HORIZONTAL_POINT_1,SCREEN_HEIGHT)
	lcd.line(HORIZONTAL_POINT_2,0,HORIZONTAL_POINT_2,SCREEN_HEIGHT)


def draw_piece(x_quad, y_quad):
	x_coord_midpoint = int(HORIZONTAL_POINT_1 * x_quad  + HORIZONTAL_POINT_1 / 2)
	y_coord_midpoint = int(VERTICAL_POINT_1 * y_quad  + VERTICAL_POINT_1 / 2)
	print(x_coord_midpoint, y_coord_midpoint)
	if x_turn:
		draw_x(x_coord_midpoint, y_coord_midpoint)
	else:
		draw_o(x_coord_midpoint, y_coord_midpoint)

def draw_x(x_midpoint, y_midpoint):
	lcd.line(x_midpoint - X_LENGTH, y_midpoint - X_LENGTH, x_midpoint + X_LENGTH, y_midpoint + X_LENGTH)
	lcd.line(x_midpoint + X_LENGTH, y_midpoint - X_LENGTH, x_midpoint - X_LENGTH, y_midpoint + X_LENGTH)


def draw_o(x_midpoint, y_midpoint):
	lcd.line(x_midpoint - 2,            y_midpoint - O_RADIUS + 2, x_midpoint + 2,            y_midpoint - O_RADIUS + 2)
	lcd.line(x_midpoint - 2,            y_midpoint + O_RADIUS - 2, x_midpoint + 2,            y_midpoint + O_RADIUS - 2)
	lcd.line(x_midpoint - O_RADIUS + 2, y_midpoint - 2,            x_midpoint - O_RADIUS + 2, y_midpoint + 2)
	lcd.line(x_midpoint + O_RADIUS - 2, y_midpoint - 2,            x_midpoint + O_RADIUS - 2, y_midpoint + 2)
	
	lcd.set_text_color(lcd.rgb(100,100,100), lcd.rgb(100,100,100))
	lcd.line(x_midpoint - 1,            y_midpoint - O_RADIUS + 1, x_midpoint - O_RADIUS + 1, y_midpoint + 1)
	lcd.line(x_midpoint + 1,            y_midpoint - O_RADIUS + 1, x_midpoint + O_RADIUS - 1, y_midpoint + 1)
	lcd.line(x_midpoint + O_RADIUS - 1, y_midpoint + 1,            x_midpoint + 1,            y_midpoint + O_RADIUS - 1)
	lcd.line(x_midpoint - O_RADIUS + 1, y_midpoint + 1,            x_midpoint - 1,            y_midpoint + O_RADIUS - 1)


	# lcd.set_pixel(int(x_midpoint + O_RADIUS/2), int(y_midpoint + O_RADIUS/2), lcd.rgb(255, 255, 255))
	# lcd.set_pixel(int(x_midpoint + O_RADIUS/2), int(y_midpoint - O_RADIUS/2), lcd.rgb(255, 255, 255))
	# lcd.set_pixel(int(x_midpoint - O_RADIUS/2), int(y_midpoint + O_RADIUS/2), lcd.rgb(255, 255, 255))
	# lcd.set_pixel(int(x_midpoint - O_RADIUS/2), int(y_midpoint - O_RADIUS/2), lcd.rgb(255, 255, 255))

def check_win():
	print(board)
	# check horizontal
	for i in range(3):
		if board[i*3+0] and board[i*3+1] and board[i*3+2]:
			print("horiz win for x with i=", i)
			return("X")
		elif board[i*3+0] == False and board[i*3+1] == False and board[i*3+2] == False:
			print("horizontal win for o with i=", i)
			return("O")
		#check vertical
		elif board[i+0] and board[i+3] and board[i+6]:
			print("vertical win for x with i=", i)
			return("X")
		elif board[i+0] == False and board[i+6] == False and board[i+5] == False:
			print("vertical win for o with i=", i)
			return("O")
       #check horizontal
	if board[0] and board[4] and board[8]:
		return("X")
	elif board[0] == False and board[4] == False and board[8] == False:
		return("O")
	if board[2] and board[4] and board[6]:
		return("X")
	elif board[2] == False and board[4] == False and board[6] == False:
		return("O")

def start():
	draw_board()
	while True:
		if (sw()):
			draw_board()
	 	elif (lcd.is_touched()):
	 		valid_square_selected = False
	 		global board
	 		global x_turn
	 		coords = lcd.get_touch()
	 		x = coords[1]
	 	   	y = coords[2]
	 	   	print(coords)
	 		if x < HORIZONTAL_POINT_1:
				if y < VERTICAL_POINT_1 - PADDING:
					print("box 1")
					if board[0] is None:
						board[0] = x_turn
						draw_piece(0,0)
						valid_square_selected = True
				elif y > VERTICAL_POINT_1 + PADDING and y < VERTICAL_POINT_2 - PADDING:
					print("box 4")
					if board[3] is None:
						board[3] = x_turn
						draw_piece(0,1)
						valid_square_selected = True
				elif y > VERTICAL_POINT_2 + PADDING:
					if board[6] is None:
						board[6] = x_turn
						print("box 7")
						draw_piece(0,2)
						valid_square_selected = True
			elif x > HORIZONTAL_POINT_1 + PADDING and x < HORIZONTAL_POINT_2 - PADDING:
				if y < VERTICAL_POINT_1 - PADDING:
					print("box 2")
					if board[1] is None:
						board[1] = x_turn
						draw_piece(1,0)
						valid_square_selected = True
				elif y > VERTICAL_POINT_1 + PADDING and y < VERTICAL_POINT_2 - PADDING:
					print("box 5")
					if board[4] is None:
						board[4] = x_turn
						draw_piece(1,1)
						valid_square_selected = True
				elif y > VERTICAL_POINT_2 + PADDING:
					print("box 8")
					if board[7] is None:
						board[7] = x_turn
						draw_piece(1,2)
						valid_square_selected = True
			elif x > HORIZONTAL_POINT_2 + PADDING:
				if y < VERTICAL_POINT_1 - PADDING:
					print("box 3")
					if board[2] is None:
						board[2] = x_turn
						draw_piece(2,0)
						valid_square_selected = True
				elif y > VERTICAL_POINT_1 + PADDING and y < VERTICAL_POINT_2 - PADDING:
					print("box 6")
					if board[5] is None:
						board[5] = x_turn
						draw_piece(2,1)
						valid_square_selected = True
				elif y > VERTICAL_POINT_2 + PADDING:
					print("box 9")
					if board[8] is None:
						board[8] = x_turn
						draw_piece(2,2)
						valid_square_selected = True
			if valid_square_selected:
				x_turn = not x_turn
				winner = check_win()
				if winner == "X":
					print("x win")
				elif winner == "O":
					print("o win")
		sleep(0.1)

start()

