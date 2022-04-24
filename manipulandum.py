
from .init import *

from scipy.signal import savgol_filter
import numpy as np


class Manipulandum():

    def __init__(self, df, params):

        self.raw = df
        self.params = params
        self.t = df.iloc[:, 0]
        self.n = len(df)
        self.fs = int(1/self.t.diff().mean())

        # Center the signals
        self.x = (df.iloc[:, 1] - df.iloc[:, 1].mean()).to_numpy()
        self.y = (df.iloc[:, 2] - df.iloc[:, 2].mean()).to_numpy()

        # Compute velocities
        self.filter()

    def filter(self):
        """
        We use a low-pass filter to remove the high  frequency components of the noise.
        We use a Savitsky–Golay filter with a polynomial of order 3 and a filter window of length 5
        because we do not know the threshold that separates the noise from real-world measurements.

        NaN values have to be removed. Here they are simply replaced by zeros.
        """

        # Filter
        x_filt = savgol_filter(np.nan_to_num(self.x),
                               window_length=5,
                               polyorder=3)
        y_filt = savgol_filter(np.nan_to_num(self.y),
                               window_length=5,
                               polyorder=3)

        # Compute velocity
        dt = np.diff(self.t)
        self.v_x = np.diff(x_filt)/dt
        self.v_y = np.diff(y_filt)/dt

        return

    def process_descriptors(self):

        return

    def process_smoothness(self, method='sparc', windowed=True, window_size=20):
        """
        window_size in s
        """

        if method == 'sparc':
            if not(windowed):
                return spectral_arclength(self.v_x, self.v_y, self.fs,
                                          **self.params['smoothness']['sparc'])

            # If windowed option is chosen, returned the mean of SPARC on each window
            s_to_samples = window_size//self.fs
            smoothness_values = []
            for i in range(0, len(self.t), s_to_samples):
                v_x = self.v_x[i:i+s_to_samples]
                v_y = self.v_y[i:i+s_to_samples]
                smoothness_values.append(spectral_arclength(v_x, v_y, self.fs,
                                                            **self.params['smoothness']['sparc']))
            return np.mean(smoothness_values)

        elif method == 'dlj':
            raise NotImplementedError
        elif method == 'ldlj':
            raise NotImplementedError
        else:
            print("Uknown method. Choose from 'sparc', 'dlj' or 'ldlj'.")

        return
