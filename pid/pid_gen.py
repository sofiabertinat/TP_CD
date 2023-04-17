import numpy as np
from scipy import signal
from scipy.linalg import expm
from control import *
import matplotlib.pyplot    as     plt
from   matplotlib.animation import FuncAnimation
from funciones import calculate_rise_time

#print("tiempo de subida teórico")
#tr_teo = calculate_rise_time ( hs_out, t )
#print (tr_teo)

#Genero una señal de onda cuadrada de f01 (1 Hz) sampleada a fs (100 Hz) for 1 second
f01 = 1
fs = 250
t = np.linspace(0, 1, fs, endpoint=False)
s_ref = (signal.square(2 * np.pi * f01 * t) + 1 ) / 2

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

