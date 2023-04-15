import numpy as np
from scipy import signal
from scipy.linalg import expm
from control import *
import matplotlib.pyplot    as     plt
from   matplotlib.animation import FuncAnimation
from funciones import calculate_rise_time

# Valores parametros circuito
r_1 = 2e3
r_2 = 1e3
c_1 = 10e-6
c_2 = 10e-6

# u(t) =  R1 [C2 dy(t)/dt + C1 dvc1(t)/dt] + vc1(t)
# vc1(t) = R2 C2 dy(t)/dt + y(t)
# => u(t) = R1 [C2 dy(t)/dt + C1 [R2 C2 d^2y(t)/dt + y(t)]] + R2 C2 dy(t)/dt + y(t)
# => u(t) = y(t) + [R1 C2 + R1 C1 + R2 C2] dy(t)/dt + R1 C1 R2 C2 d^2y(t)/dt
# => u(s) = Y(s) [1+ (R1 C2 + R1 C1 + R2 C2) s + R1 C1 R2 C2 s^2]
s = tf('s')
hs = 1 / ((r_1*c_1*r_2*c_2)*s*s + (r_1*c_1+r_1*c_2+r_2*c_2)*s + 1)
num_1, den_1 = tfdata(hs)

# Respuesta al escalon
t, hs_out = step_response(hs)
plt.ylabel('Amplitud')
plt.xlabel('Tiempo') 
plt.title('Respuesta al escalon teorica')
plt.plot(t, hs_out)
plt.show()

print("tiempo de subida teórico")
tr_teo = calculate_rise_time ( hs_out, t )
print (tr_teo)

#Genero una señal de onda cuadrada de f01 (1 Hz) sampleada a fs (100 Hz) for 1 second
f01 = 1
fs = 1000
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

