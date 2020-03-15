#!/usr/bin/python

from subprocess import *
import os

FIFO_PATH = '/tmp/my_fifo'

if os.path.exists(FIFO_PATH):
    os.unlink(FIFO_PATH)

if not os.path.exists(FIFO_PATH):
    os.mkfifo(FIFO_PATH)
    with open('File.txt', 'a+') as file:
        file.write("my_fifo:")
    #my_fifo = open(FIFO_PATH, 'w')
    #print("my_fifo:", my_fifo)

#pipe = Popen('/bin/date', shell=False, stdin=PIPE, stdout=my_fifo, stderr=PIPE)
with open('File.txt', 'a+') as file:
    print(file.readline())

os.unlink(FIFO_PATH)