import numpy as np
from scipy import signal
from scipy.linalg import expm
from control import *
import matplotlib.pyplot    as     plt
from   matplotlib.animation import FuncAnimation
from funciones import calculate_rise_time

# Utilizar una señal cuadrada de 10Hz como señal de referencia. 
# Sin aplicar control, obtener la respuesta al escalon del sistema a lazo abierto. 
# Medir el tiempo de subida, tr. El tiempo de subida se calcula como el tiempo que tarda la señal en ir del 10% al 90% de su valor (tr = t90% − t10%).
# Mostrar los graficos que se generan. 
# Para visualizar los datos, enviar por puerto serie las mediciones y realizar un grafico en Python de los resultados.


#Genero una señal de onda cuadrada de f01 (1 Hz) sampleada a fs (100 Hz) for 1 second
f01 = 1
fs = 1000
t = np.linspace(0, 1, fs, endpoint=False)
s_ref = (signal.square(2 * np.pi * f01 * t) + 1 ) / 2

plt.xlabel('Tiempo') 
plt.ylabel('Amplitud') 
plt.plot(t,s_ref,'ro-')

N = fs
y = np.zeros((N ,), dtype=float)
with open('salida.txt', 'r') as G:
    stxt = G.read()
    stxt = stxt.lstrip('[')
    stxt = stxt.rstrip(']\n')
    stxt = stxt.split(',')

x = np.array(stxt)
y = x.astype(np.float64)
y = y/100
# centro la señal leída con la entrada
j = 445
s_out = np.zeros((N ,), dtype=float)
for i in range(N):
    s_out[i] = y[j]
    j = j + 1
    if j == N :
        j = 0

t = np.linspace(0, 1, N, endpoint=True)
plt.plot(t,s_out,'bo-')
plt.show()

print("tiempo de subida calculado")
print (calculate_rise_time (s_out , t ))
