#!python3
import numpy as np
import matplotlib.pyplot as plt
from   matplotlib.animation import FuncAnimation
import os
import io
import serial

N = 500
size = 4
puerto = "COM5" 
baudrate = 460800
sample = serial.Serial(port=puerto, baudrate=baudrate,timeout=None)

y = np.zeros((N ,), dtype=float)
for t in range(N):
        raw = sample.read(1)
        while( len(raw) < size):
            raw+=sample.read(1)
        y [t] = (int.from_bytes(raw,"little",signed=True))

sample.close()

with open('salida.txt', 'w', encoding="utf-8") as f:
    f.write('[\n') 
    for  i in range(N-1):
        f.write(str(y[i]))
        f.write(',\n')
    f.write(str(y[N-1]))
    f.write("]\n")
    f.close()

