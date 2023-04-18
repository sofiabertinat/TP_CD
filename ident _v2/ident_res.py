import numpy as np
from scipy import signal
from scipy.linalg import expm
from control import *
import matplotlib.pyplot    as     plt
from   matplotlib.animation import FuncAnimation

N = 500
y = np.zeros((N ,), dtype=float)
with open('salida_signals.txt', 'r') as G:
    stxt = G.read()
    stxt = stxt.lstrip('[')
    stxt = stxt.rstrip(']\n')
    stxt = stxt.split(',')

x = np.array(stxt)
y = x.astype(np.float64)
y = y/100

u_1 = np.zeros((250 ,), dtype=float)
u_2 = np.zeros((250 ,), dtype=float)
i = 0
j = 0
while i < 250 :
    u_1[i]=y[j]
    u_2[i]=y[j+1]
    i = i + 1
    j = j + 2

t = np.linspace(0, 1, 250, endpoint=True)
plt.plot(t,u_1,'bo-')
plt.plot(t,u_2,'go-')
plt.show()


