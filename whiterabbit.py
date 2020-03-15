#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import socket
import os
import signal
import sys

from bdffont import *
from matrixbuffer import *
from weather import *

# matrix rows and cols in pixels
MATRIX_ROWS = 8
MATRIX_COLS = 32
RPI_HOSTNAME = "jdpi"
FIFO_PATH = "/tmp/matrix.fifo"

# define colors
COLOR_BLACK = (0,0,0)
COLOR_BLUE = (0,0,1)
COLOR_GREEN = (0,1,0)
COLOR_AQUA = (0,1,1)
COLOR_RED = (1,0,0)
COLOR_PURPLE = (1,0,1)
COLOR_YELLOW = (1,1,0)
COLOR_WHITE = (1,1,1)

print(f'Detect terminal or neopixel')
# set display wrapper to either terminal or neopixel based on hostname
if socket.gethostname() == RPI_HOSTNAME:
	from neopixelwrapper import *
	display_wrapper = NeopixelWrapper()
else:
	from terminalwrapper import *
	display_wrapper = TerminalWrapper()

font = BDFFont("fonts/5x5.bdf")
mb = MatrixBuffer(MATRIX_ROWS, MATRIX_COLS, font, display_wrapper)
weather = Weather()

print(f'Create FIFO pipe...')
# create fifo pipe
try:
	os.mkfifo(FIFO_PATH, 0o666)
except OSError:
	pass

fifo=open(FIFO_PATH, "r")

print(f'FIFO is open.')
# capture kill signal
def signal_term_handler(signal, frame):
	mb.clear()
	mb.show()
	fifo.close()
	sys.exit(0)
 
signal.signal(signal.SIGTERM, signal_term_handler)

while True:

	try:
		print(f'Start of main loop.')
		mb.clear()
		print(f'Write temperature...')
		# current temperature
		mb.write_string(weather.get_current_temperature(), COLOR_YELLOW, mb.ALIGN_RIGHT)
		print(f'Write Hi/Low temperatures')
		# today high and low
		high, low = weather.get_today_forecast()
		if high != "" and low !="":
			mb.write_string(high + "/" + low + "F", COLOR_YELLOW, mb.ALIGN_LEFT)
		print(f'Write time...')
		mb.write_string(time.strftime("%-I:%M:%S"), COLOR_WHITE, mb.ALIGN_CENTER)
		print(f'Show display...')
		mb.show()
		
		time.sleep(1)

		# check if there are any messages in queue
		# scroll if found
		print(f'check FIFO and display any text...')
		line = fifo.readline()
		if line.strip() != "":
			mb.scroll_string(line[:256], COLOR_GREEN)
			time.sleep(1)

	except KeyboardInterrupt:
		mb.clear()
		mb.show()
		fifo.close()
		break
	
	except:
		pass

