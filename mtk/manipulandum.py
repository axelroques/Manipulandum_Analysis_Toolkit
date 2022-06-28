
from .descriptors import *
from .smoothness import *
from .path import *

from scipy.signal import savgol_filter
from collections.abc import Mapping
import numpy as np


class Manipulandum():

    PARAMS = {
        'descriptors': {
            'dynamic': {
                'sway': {
                    'radius': 3
                }
            },
            'frequency': {
                'welch': {
                    'n_window': 2048
                }
            },
            'positional': {},
            'stochastic': {
                'msd': {
                    'min_lag': 1,
                    'max_lag': 1000,
                    'n_lags': 50
                }
            }
        },
        'smoothness': {
            'sparc': {
                'padlevel': 4,
                'fc': 10,
                'amp_th': 0.05
            },
            'dlj': {},
            'ldlj': {}
        },
        'path': {
            'simplify': {
                'simplify_path': True,
                'threshold': 44,
                'plot': True
            },
            'directions': {
                'bin_size': 5,
                'n_min': None,
                'plot': True
            }
        }
    }

    def __init__(self, df, params=PARAMS):

        # Signal variables
        self.raw = df
        self.t = df.iloc[:, 0].to_numpy()
        self.n = len(df)
        self.fs = int(1/np.diff(self.t).mean())

        # Center the signals
        self.x = (df.iloc[:, 1] - df.iloc[:, 1].mean()).to_numpy()
        self.y = (df.iloc[:, 2] - df.iloc[:, 2].mean()).to_numpy()

        # Parameters
        if params:
            self.params = self._update_params(self.PARAMS, params)
        else:
            self.params = self.PARAMS

        # Filter data and also compute velocities
        self._filter()

        # Result dictionary
        self._results = {}

    @staticmethod
    def _update_params(source, override):
        """
        Update the params dictionary with every pair (key(s), values) of parameter in PARAMS 
        that is not present in params.
        """

        for key, value in override.items():
            if isinstance(value, Mapping):
                source[key] = Manipulandum._update_params(
                    source.get(key, {}), value)
            else:
                source[key] = value
        return source

    def _filter(self):
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
        """
        Descriptors according to Quijoux et. al.
        """

        # print('- Processing dynamic descriptors...')
        process_dyn_desc(self)
        # print('\t Done')

        # print('- Processing frequency descriptors...')
        # process_freq_desc(self)
        # print('\t Done')

        # print('- Processing positional descriptors...')
        process_pos_desc(self)
        # print('\t Done')

        # print('- Processing stochastic descriptors...')
        # process_stoch_desc(self)
        # print('\t Done')

        return

    def process_path(self, simplify_path):
        """
        Path descriptors.
        """

        process_path_desc(self, simplify_path)

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

    def get_results(self):
        """
        Return results dictionary.
        """
        return self._results
