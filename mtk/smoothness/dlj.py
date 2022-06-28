
import numpy as np


def dimensionless_jerk(movement, fs):
    """
    Calculates the smoothness metric for the given speed profile using the dimensionless jerk 
    metric.

    Parameters
    ----------
    movement : np.array
               The array containing the movement speed profile.
    fs       : float
               The sampling frequency of the data.

    Returns
    -------
    dl       : float
               The dimensionless jerk estimate of the given movement's smoothness.

    https://github.com/siva82kb/smoothness/blob/master/python/smoothness.py
    """

    # first enforce data into an numpy array.
    movement = np.array(movement)

    # calculate the scale factor and jerk.
    movement_peak = max(abs(movement))
    dt = 1./fs
    movement_dur = len(movement)*dt
    jerk = np.diff(movement, 2)/pow(dt, 2)
    scale = pow(movement_dur, 3)/pow(movement_peak, 2)

    # estimate dj
    return - scale * sum(pow(jerk, 2)) * dt
