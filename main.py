# main.py -- put your code here
import pyb
import lcd160cr
from random import randint
from time import sleep
lcd = lcd160cr.LCD160CR('X')


def draw_board():
	lcd.erase()
	lcd.line(0,50,128,50)
	lcd.line(0,112,128,112)
	lcd.line(42,0,42,160)
	lcd.line(86,0,86,160)


def start():
	draw_board()
	while True:
	 	if (lcd.is_touched()):
	 		coords = lcd.get_touch()
	 		x = coords[1]
	 	   	y = coords[2]
	 		if x < 42:
				if y < 50:
					print("box 1")
				elif y > 50 and y < 112:
					print("box 4")
				elif y > 112:
					print("box 7")
			elif x > 42 and x < 86:
				if y < 50:
					print("box 2")
				elif y > 50 and y < 112:
					print("box 5")
				elif y > 112:
					print("box 8")
			elif x > 86:
				if y < 50:
					print("box 3")
				elif y > 50 and y < 112:
					print("box 6")
				elif y > 112:
					print("box 9")
		sleep(0.1)

start()
