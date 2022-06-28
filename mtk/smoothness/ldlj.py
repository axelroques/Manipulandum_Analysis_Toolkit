
from .dlj import dimensionless_jerk
import numpy as np


def log_dimensionless_jerk(movement, fs):
    """
    Calculates the smoothness metric for the given speed profile using the log dimensionless jerk 
    metric.

    Parameters
    ----------
    movement : np.array
               The array containing the movement speed profile.
    fs       : float
               The sampling frequency of the data.

    Returns
    -------
    ldl      : float
               The log dimensionless jerk estimate of the given movement's smoothness.

    https://github.com/siva82kb/smoothness/blob/master/python/smoothness.py
    """

    return -np.log(abs(dimensionless_jerk(movement, fs)))
