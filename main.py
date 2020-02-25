import pyb
import lcd160cr
from random import randint, choice
from time import sleep
lcd = lcd160cr.LCD160CR('X')

#constants
SCREEN_WIDTH = 128
SCREEN_HEIGHT = 160

VERTICAL_POINT_1 = 53
VERTICAL_POINT_2 = 106

HORIZONTAL_POINT_1 = 42
HORIZONTAL_POINT_2 = 84

PADDING = 4
X_OFFSET = 7 
Y_OFFSET = 12

X_WIN = ["X", "X", "X"]
O_WIN = ["O", "O", "O"]

PINK  = lcd.rgb(255, 204, 255)
BLUE  = lcd.rgb(153, 153, 255)
GRAY  = lcd.rgb(242, 242, 242)
BLACK = lcd.rgb(0, 0, 0)
GREEN = lcd.rgb(102, 255, 153)


#variables
x_turn = choice([True, False])

board = [["FREE"],["FREE"],["FREE"],["FREE"],["FREE"],["FREE"],["FREE"],["FREE"],["FREE"]]
sw = pyb.Switch()

def draw_board():
	global x_turn
	global board
	x_turn = choice([True, False])

	lcd.erase()
	lcd.set_text_color(GRAY, BLACK)
	lcd.set_font(2, scale=0)
	lcd.set_pos(20, 50)
	if x_turn: 
		lcd.write("X goes first")
	else:
		lcd.write("O goes first")
	sleep(1)
	board = [["FREE"],["FREE"],["FREE"],["FREE"],["FREE"],["FREE"],["FREE"],["FREE"],["FREE"]]
	lcd.erase()
	lcd.set_pen(GRAY, BLACK)
	lcd.line(0,VERTICAL_POINT_1,SCREEN_WIDTH,VERTICAL_POINT_1)
	lcd.line(0,VERTICAL_POINT_2,SCREEN_WIDTH,VERTICAL_POINT_2)
	lcd.line(HORIZONTAL_POINT_1,0,HORIZONTAL_POINT_1,SCREEN_HEIGHT)
	lcd.line(HORIZONTAL_POINT_2,0,HORIZONTAL_POINT_2,SCREEN_HEIGHT)


def draw_piece(x_quad, y_quad):
	x = int(HORIZONTAL_POINT_1 * x_quad)
	y = int(VERTICAL_POINT_1 * y_quad)
	if x_turn:
		draw_x(x, y)
	else:
		draw_o(x, y)

def draw_x(x, y):
	lcd.set_font(2, scale=2, bold=1, trans=1)
	lcd.set_text_color(PINK, BLACK)
	lcd.set_pos(x + X_OFFSET, y + Y_OFFSET)
	lcd.write("X")

def draw_o(x, y):
	lcd.set_font(2, scale=2,bold=1, trans=1)
	lcd.set_text_color(BLUE, BLACK)
	lcd.set_pos(x + X_OFFSET, y + Y_OFFSET)
	lcd.write("O")

def announce_winner(winner, offset):
	sleep(1)
	lcd.erase()
	if "TIE" in winner:
		lcd.set_font(2, scale=0, scroll=1)
	else:
		lcd.set_font(2, scale=1, scroll=1)
	
	lcd.set_text_color(GREEN, BLACK)
	for x in range(0,offset):
		lcd.erase()
		lcd.set_pos(x, int(SCREEN_HEIGHT/2))
		lcd.write(winner)
		sleep(0.05)
	for i in range(5000):
		x = randint(0, SCREEN_WIDTH)
		y = randint(0, SCREEN_HEIGHT)
		r = randint(0, 255)
		g = randint(0, 255)
		b  = randint(0, 255)
		lcd.set_pixel(x, y, lcd.rgb(r,g,b))
		sleep(0.0005)
	lcd.erase()
	lcd.set_pos(10, 50)
	lcd.set_font(2, scale=0, scroll=0)
	lcd.write("Press USR")
	lcd.set_pos(10, 70)
	lcd.write("to play again")

def check_win():
	print(board)
	# check horizontal
	for i in range(3):
		if board[i*3+0] + board[i*3+1] + board[i*3+2] == X_WIN:
			return("X")
		elif board[i*3+0] + board[i*3+1] + board[i*3+2] == O_WIN:
			return("O")
		#check vertical
		elif board[i+0] + board[i+3] + board[i+6] == X_WIN:
			return("X")
		elif board[i+0] + board[i+3] + board[i+6] == O_WIN:
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
	#check tie
	if not ["FREE"] in board:
		return("TIE")

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
	 		x = coords[1]
	 	   	y = coords[2]
	 		if x < HORIZONTAL_POINT_1:
				if y < VERTICAL_POINT_1 - PADDING:
					if board[0] == ["FREE"]:
						board[0] = ["X"] if x_turn else ["O"]
						draw_piece(0,0)
						valid_square_selected = True
				elif y > VERTICAL_POINT_1 + PADDING and y < VERTICAL_POINT_2 - PADDING:
					if board[3] == ["FREE"]:
						board[3] = ["X"] if x_turn else ["O"]
						draw_piece(0,1)
						valid_square_selected = True
				elif y > VERTICAL_POINT_2 + PADDING:
					if board[6] == ["FREE"]:
						board[6] = ["X"] if x_turn else ["O"]
						draw_piece(0,2)
						valid_square_selected = True
			elif x > HORIZONTAL_POINT_1 + PADDING and x < HORIZONTAL_POINT_2 - PADDING:
				if y < VERTICAL_POINT_1 - PADDING:
					if board[1] == ["FREE"]:
						board[1] = ["X"] if x_turn else ["O"]
						draw_piece(1,0)
						valid_square_selected = True
				elif y > VERTICAL_POINT_1 + PADDING and y < VERTICAL_POINT_2 - PADDING:
					if board[4] == ["FREE"]:
						board[4] = ["X"] if x_turn else ["O"]
						draw_piece(1,1)
						valid_square_selected = True
				elif y > VERTICAL_POINT_2 + PADDING:
					if board[7] == ["FREE"]:
						board[7] = ["X"] if x_turn else ["O"]
						draw_piece(1,2)
						valid_square_selected = True
			elif x > HORIZONTAL_POINT_2 + PADDING:
				if y < VERTICAL_POINT_1 - PADDING:
					if board[2] == ["FREE"]:
						board[2] = ["X"] if x_turn else ["O"]
						draw_piece(2,0)
						valid_square_selected = True
				elif y > VERTICAL_POINT_1 + PADDING and y < VERTICAL_POINT_2 - PADDING:
					if board[5] == ["FREE"]:
						board[5] = ["X"] if x_turn else ["O"]
						draw_piece(2,1)
						valid_square_selected = True
				elif y > VERTICAL_POINT_2 + PADDING:
					if board[8] == ["FREE"]:
						board[8] = ["X"] if x_turn else ["O"]
						draw_piece(2,2)
						valid_square_selected = True
			if valid_square_selected:
				x_turn = not x_turn
				winner = check_win()
				if winner == "X":
					announce_winner("X Wins", 25)
				elif winner == "O":
					announce_winner("O Wins", 25)
				elif winner == "TIE":
					announce_winner("It's a TIE", 7)
		sleep(0.05)

start()
