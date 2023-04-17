import numpy as np
from scipy import signal
from scipy.linalg import expm
from control import *
import matplotlib.pyplot    as     plt
from   matplotlib.animation import FuncAnimation

def calculate_rise_time ( signal , time , ref_value =1):
    # Find the index where the signal first crosses the start threshold
    start_index = np.argmax ( signal >= 0.1 * ref_value )
    # Find the index where the signal crosses the end threshold
    end_index = np.argmax( signal >= 0.9 * ref_value )
    # Calculate the rise time as the difference between the two indices
    rise_time = time [ end_index ] - time [ start_index ]
    return rise_time

