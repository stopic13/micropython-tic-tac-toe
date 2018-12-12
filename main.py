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

X_LENGTH = 10
O_RADIUS = 10
PADDING = 4

X_WIN = ["X", "X", "X"]
O_WIN = ["O", "O", "O"]

PINK  = (255, 204, 255)
BLUE  = (153, 153, 255)
GRAY  = (242, 242, 242)
BLACK = (0, 0, 0)
GREEN = (102, 255, 153)


#variables
x_turn = True

board = [["FREE"],["FREE"],["FREE"],["FREE"],["FREE"],["FREE"],["FREE"],["FREE"],["FREE"]]
sw = pyb.Switch()

def draw_board():
	global x_turn
	global board
	x_turn = True
	board = [["FREE"],["FREE"],["FREE"],["FREE"],["FREE"],["FREE"],["FREE"],["FREE"],["FREE"]]
	lcd.erase()
	lcd.set_pen(lcd.rgb(GRAY[0], GRAY[1], GRAY[2]), lcd.rgb(BLACK[0], BLACK[1], BLACK[2]))
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
	lcd.set_pen(lcd.rgb(PINK[0], PINK[1], PINK[2]), lcd.rgb(BLACK[0], BLACK[1], BLACK[2]))
	lcd.line(x_midpoint - X_LENGTH, y_midpoint - X_LENGTH, x_midpoint + X_LENGTH, y_midpoint + X_LENGTH)
	lcd.line(x_midpoint + X_LENGTH, y_midpoint - X_LENGTH, x_midpoint - X_LENGTH, y_midpoint + X_LENGTH)


def draw_o(x_midpoint, y_midpoint):
	lcd.set_pen(lcd.rgb(BLUE[0], BLUE[1], BLUE[2]), lcd.rgb(BLACK[0], BLACK[1], BLACK[2]))

	lcd.line(x_midpoint - 2,            y_midpoint - O_RADIUS + 2, x_midpoint + 2,            y_midpoint - O_RADIUS + 2)
	lcd.line(x_midpoint - 2,            y_midpoint + O_RADIUS - 2, x_midpoint + 2,            y_midpoint + O_RADIUS - 2)
	lcd.line(x_midpoint - O_RADIUS + 2, y_midpoint - 2,            x_midpoint - O_RADIUS + 2, y_midpoint + 2)
	lcd.line(x_midpoint + O_RADIUS - 2, y_midpoint - 2,            x_midpoint + O_RADIUS - 2, y_midpoint + 2)
	
	lcd.set_text_color(lcd.rgb(100,100,100), lcd.rgb(100,100,100))
	lcd.line(x_midpoint - 1,            y_midpoint - O_RADIUS + 1, x_midpoint - O_RADIUS + 1, y_midpoint + 1)
	lcd.line(x_midpoint + 1,            y_midpoint - O_RADIUS + 1, x_midpoint + O_RADIUS - 1, y_midpoint + 1)
	lcd.line(x_midpoint + O_RADIUS - 1, y_midpoint + 1,            x_midpoint + 1,            y_midpoint + O_RADIUS - 1)
	lcd.line(x_midpoint - O_RADIUS + 1, y_midpoint + 1,            x_midpoint - 1,            y_midpoint + O_RADIUS - 1)


	lcd.set_pixel(int(x_midpoint + O_RADIUS/2), int(y_midpoint + O_RADIUS/2), lcd.rgb(BLUE[0], BLUE[1], BLUE[2]))
	lcd.set_pixel(int(x_midpoint + O_RADIUS/2), int(y_midpoint - O_RADIUS/2), lcd.rgb(BLUE[0], BLUE[1], BLUE[2]))
	lcd.set_pixel(int(x_midpoint - O_RADIUS/2), int(y_midpoint + O_RADIUS/2), lcd.rgb(BLUE[0], BLUE[1], BLUE[2]))
	lcd.set_pixel(int(x_midpoint - O_RADIUS/2), int(y_midpoint - O_RADIUS/2), lcd.rgb(BLUE[0], BLUE[1], BLUE[2]))

def announce_winner(winner):
	sleep(1)
	lcd.erase()
	lcd.set_font(0, scale=2)
	lcd.set_text_color(lcd.rgb(GREEN[0],GREEN[1],GREEN[2]), lcd.rgb(0,0,0))
	for x in range(0,20):
		lcd.erase()
		lcd.set_pos(x, int(SCREEN_HEIGHT/2))
		lcd.write(winner + " wins!")
		sleep(0.05)
	for i in range(4000):
		x = randint(0, SCREEN_WIDTH)
		y = randint(0, SCREEN_HEIGHT)
		r = randint(0, 255)
		g = randint(0, 255)
		b  = randint(0, 255)
		lcd.set_pixel(x, y, lcd.rgb(r,g,b))
		sleep(0.001)
	lcd.erase()
	lcd.set_pos(10, 50)
	lcd.set_font(0, scale=1)
	lcd.write("Press USR")
	lcd.set_pos(10, 70)
	lcd.write("to play again")

def check_win():
	print(board)
	# check horizontal
	for i in range(3):
		if board[i*3+0] + board[i*3+1] + board[i*3+2] == X_WIN:
			print("horiz win for x with i=", i)
			return("X")
		elif board[i*3+0] + board[i*3+1] + board[i*3+2] == O_WIN:
			print("horizontal win for o with i=", i)
			return("O")
		#check vertical
		elif board[i+0] + board[i+3] + board[i+6] == X_WIN:
			print("vertical win for x with i=", i)
			return("X")
		elif board[i+0] + board[i+3] + board[i+6] == O_WIN:
			print("vertical win for o with i=", i)
			return("O")
       #check horizontal
	if board[0] + board[4] + board[8] == X_WIN:
		return("X")
	elif board[0] + board[4] + board[8] == O_WIN:
		return("O")
	if board[2] + board[4] + board[6] == X_WIN:
		return("X")
	elif board[2] + board[4] + board[6] == O_WIN:
		return("O")

def start():
	draw_board()
	while True:
		coords = lcd.get_touch()
		if (sw()):
			draw_board()
		elif coords[0] == 1:
	 		valid_square_selected = False
	 		global board
	 		global x_turn
	 		#coords = lcd.get_touch()
	 		x = coords[1]
	 	   	y = coords[2]
	 	   	print(coords)
	 		if x < HORIZONTAL_POINT_1:
				if y < VERTICAL_POINT_1 - PADDING:
					print("box 1")
					if board[0] == ["FREE"]:
						board[0] = ["X"] if x_turn else ["O"]
						draw_piece(0,0)
						valid_square_selected = True
				elif y > VERTICAL_POINT_1 + PADDING and y < VERTICAL_POINT_2 - PADDING:
					print("box 4")
					if board[3] == ["FREE"]:
						board[3] = ["X"] if x_turn else ["O"]
						draw_piece(0,1)
						valid_square_selected = True
				elif y > VERTICAL_POINT_2 + PADDING:
					if board[6] == ["FREE"]:
						board[6] = ["X"] if x_turn else ["O"]
						print("box 7")
						draw_piece(0,2)
						valid_square_selected = True
			elif x > HORIZONTAL_POINT_1 + PADDING and x < HORIZONTAL_POINT_2 - PADDING:
				if y < VERTICAL_POINT_1 - PADDING:
					print("box 2")
					if board[1] == ["FREE"]:
						board[1] = ["X"] if x_turn else ["O"]
						draw_piece(1,0)
						valid_square_selected = True
				elif y > VERTICAL_POINT_1 + PADDING and y < VERTICAL_POINT_2 - PADDING:
					print("box 5")
					if board[4] == ["FREE"]:
						board[4] = ["X"] if x_turn else ["O"]
						draw_piece(1,1)
						valid_square_selected = True
				elif y > VERTICAL_POINT_2 + PADDING:
					print("box 8")
					if board[7] == ["FREE"]:
						board[7] = ["X"] if x_turn else ["O"]
						draw_piece(1,2)
						valid_square_selected = True
			elif x > HORIZONTAL_POINT_2 + PADDING:
				if y < VERTICAL_POINT_1 - PADDING:
					print("box 3")
					if board[2] == ["FREE"]:
						board[2] = ["X"] if x_turn else ["O"]
						draw_piece(2,0)
						valid_square_selected = True
				elif y > VERTICAL_POINT_1 + PADDING and y < VERTICAL_POINT_2 - PADDING:
					print("box 6")
					if board[5] == ["FREE"]:
						board[5] = ["X"] if x_turn else ["O"]
						draw_piece(2,1)
						valid_square_selected = True
				elif y > VERTICAL_POINT_2 + PADDING:
					print("box 9")
					if board[8] == ["FREE"]:
						board[8] = ["X"] if x_turn else ["O"]
						draw_piece(2,2)
						valid_square_selected = True
			if valid_square_selected:
				x_turn = not x_turn
				winner = check_win()
				if winner == "X":
					print("x win")
					announce_winner("X")
				elif winner == "O":
					print("o win")
					announce_winner("O")
		sleep(0.05)

start()
