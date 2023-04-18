import numpy as np
from scipy import signal
from scipy.linalg import expm
from control import *
import matplotlib.pyplot    as     plt
from   matplotlib.animation import FuncAnimation

N = 200
y = np.zeros((N ,), dtype=float)
with open('out.txt', 'r') as G:
    stxt = G.read()
    stxt = stxt.lstrip('[')
    stxt = stxt.rstrip(']\n')
    stxt = stxt.split(',')

x = np.array(stxt)
y = x.astype(np.float64)
y = y/100
# centro la señal leída con la entrada
j = 170
s_out = np.zeros((N ,), dtype=float)
for i in range(N):
    s_out[i] = y[j]
    j = j + 1
    if j == np.size(y) :
        j = 0

t = np.linspace(0, 1, N, endpoint=True)
plt.plot(t,s_out,'bo-')

y_a = np.zeros((N ,), dtype=float)
with open('in.txt', 'r') as G:
    stxt_a = G.read()
    stxt_a = stxt_a.lstrip('[')
    stxt_a = stxt_a.rstrip(']\n')
    stxt_a = stxt_a.split(',')

x_a = np.array(stxt_a)
y_a = x_a.astype(np.float64)
y_a = y_a/100
# centro la señal leída con la entrada
j = 1
s_out_a = np.zeros((N ,), dtype=float)
for i in range(N):
    s_out_a[i] = y_a[j]
    j = j + 1
    if j == N :
        j = 0

t = np.linspace(0, 1, N, endpoint=True)
plt.plot(t,s_out_a,'go-')
plt.show()


