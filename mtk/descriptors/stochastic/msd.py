
import numpy as np


def MSD(signal, n, lag):
    """
    Mean square displacement.
    """

    msd = 0
    for i in range(2, n-lag-2):
        msd += (signal[i+lag]-signal[i])**2

    return msd/(n-lag)


def generate_MSDs(manipulandum):

    params = manipulandum.params['descriptors']['stochastic']['msd']

    log_mini = np.round(np.log10(params['min_lag']))
    log_maxi = np.round(np.log10(params['max_lag']))

    log_lags = np.linspace(log_mini, log_maxi, params['n_lags'])
    lags = np.round(10**log_lags)
    new_lags = (list(set(lags)))
    new_lags.sort()
    lags_MSD = new_lags
    params['n_lags'] = len(new_lags)

    MSDs = np.zeros((2, params['n_lags']))

    for count, lag in enumerate(new_lags):
        MSDs[0, count] = MSD(manipulandum.x, manipulandum.n, int(lag))
        MSDs[1, count] = MSD(manipulandum.y, manipulandum.n, int(lag))

    return np.array(lags_MSD), MSDs


def process(manipulandum):

    lags_MSD, MSDs = generate_MSDs(manipulandum)

    manipulandum._results['stochastic'].update({
        'msd': {
            'lags_MSD': lags_MSD,
            'MSDs': MSDs
        }
    })

    return
