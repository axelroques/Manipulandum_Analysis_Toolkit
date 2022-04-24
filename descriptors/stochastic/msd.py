
import numpy as np


def MSD(signal, n, lag):
    """
    Mean square displacement
    """

    msd = 0
    for i in range(2, n-lag-2):
        msd += (signal[i+lag]-signal[i])**2

    return msd/(n-lag)


def generate_MSDs(manipulandum):

    params = {'min_lag': 1, 'max_lag': 1000, 'n_lags': 50}
    for key in params.keys():
        if manipulandum.params['descriptors']['stochastic']['msd'][key]:
            params[key] = manipulandum.params['descriptors']['stochastic']['msd'][key]

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

    return lags_MSD, MSDs


def process(manipulandum):

    lags_MSD, MSDs = generate_MSDs(manipulandum)

    return lags_MSD, MSDs
