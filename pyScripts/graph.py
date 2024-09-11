import matplotlib.pyplot as plt
import matplotlib.animation as animation
import stateSpace
import threading

# Initialize the figure and axis
fig, ax = plt.subplots()
x_data, y_data = [], []
line, = ax.plot(x_data, y_data, 'r-')