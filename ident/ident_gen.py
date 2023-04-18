import numpy as np
from scipy import signal
from scipy.linalg import expm
from control import *
import matplotlib.pyplot    as     plt
from   matplotlib.animation import FuncAnimation

# Determinar el valor de los polos del sistema mediante identificacion, considerando al sistema como una caja gris. G(s) = Y (s)/U(s)
# Se selecciona la identificacion LS, graficos de la entrada aplicada y la salida obtenida
# Explicacion de como se diseño la entrada.
# Incluir el resultado los valores de los parametros identificados segun el modelo elegido para el ajuste y el error asociado.

#Genero una señal de onda cuadrada de f01 (1 Hz) sampleada a fs (100 Hz) for 1 second
cant_pulsos = 5
f01 = 1
fs = 40
t = np.linspace(0, cant_pulsos, cant_pulsos*fs, endpoint=False)
s_ref = np.zeros(cant_pulsos*fs,)
i = 0
for i in range(cant_pulsos-1):
    cant =  np.random.randint(5,15)
    j = 0
    m =  np.random.randint(0,100) 
    while(j<cant):
        s_ref[j+(i*40)] = m
        j = j + 1

j = 160
while(j<180):
    s_ref[j] = 100
    j = j + 1

# guardo la señal generada en un archivo
N = np.size(s_ref)
with open('entrada.h', 'w', encoding="utf-8") as f:
    f.write('float h[]={\n') 
    for  i in range(N-1):
        f.write(str(s_ref[i]))
        f.write(',\n')
    f.write(str(s_ref[N-1]))
    f.write("};\n")
    f.close()

plt.xlabel('Tiempo') 
plt.ylabel('Amplitud') 
plt.plot(t,s_ref,'ro-')
plt.show()