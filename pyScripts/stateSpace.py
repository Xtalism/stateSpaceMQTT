import scipy.integrate as spi
import numpy as np
import threading
import time
import readSerial

# Parameters
R = 2.0
L = 0.5
Kt = 0.1
Kb = 0.1
J = 0.01
Fr = 0.001

# Time step
dt = 0.01

current = 0.0 
omega = 0.0  
integral_omega = 0.0 

A = np.array([[-R/L, -Kb/L], [Kt/J, -Fr/J]])
B = np.array([[1/L], [0]])
x = np.array([current, omega], dtype=float)  # Ensure x is of type float

omega_values = [omega]
time_values = [0]

# Shared variable and lock
y = None
y_lock = threading.Lock()
info = None
info_lock = threading.Lock()

def stateSpaceCalculation():
    global x, y, info
    t = 0
    while readSerial.data is None:
        pass

    try:
        while not readSerial.stop_event.is_set():
            if readSerial.data is not None:
                try:
                    voltage_str = readSerial.data.split(':')[1].strip()
                    voltage = float(voltage_str)
                except (IndexError, ValueError):
                    continue

                dx = A @ x + B.flatten() * voltage
                x += dx * dt

                current = x[0]
                omega = x[1]

                omega_values.append(omega)
                time_values.append(t)
                t += dt

                integral_omega = spi.cumulative_trapezoid(omega_values, time_values, initial=0)[-1]

                with y_lock:
                    y = omega

                with info_lock:
                    info = f"\nOmega: {float(omega)},\nVoltage: {float(voltage)},\nIntegral of Omega: {float(integral_omega)}"
                
                print(info)
                
                time.sleep(1)
    except KeyboardInterrupt:
        readSerial.stop_event.set()