import numpy as np
from scipy import signal
from scipy.linalg import expm
import control.matlab as co
import matplotlib.pyplot    as     plt
from   matplotlib.animation import FuncAnimation

#TRANSFERENCIA TEORICA
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
s = co.tf('s')
hs_C = 1 / ((r_1*c_1*r_2*c_2)*s*s + (r_1*c_1+r_1*c_2+r_2*c_2)*s + 1)
num_c, den_c = co.tfdata(hs_C)
print(num_c)
print(den_c)
# Respuesta al escalon
hC, tC = co.step(hs_C)
plt.ylabel('Amplitud')
plt.xlabel('Tiempo') 
plt.title('Respuesta al escalon')
plt.plot(tC, hC, 'r')


#TRANSFERENCIA IDENTIFICADA
num = [0.145, 0.029]
den = [ 0.114, 0.940, 0.121]
hs_I = co.tf(np.array(num), np.array(den))
hI, tI = co.step(hs_I)
plt.plot(tI, hI,'b')
plt.show()