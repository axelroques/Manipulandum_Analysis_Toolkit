
from scipy.signal import butter, filtfilt
from scipy.signal import find_peaks
import numpy as np


def sway_area_per_second(manipulandum):
    """
    Sway area per second
    """

    column1 = manipulandum.x[1:] * manipulandum.y[:-1]
    column2 = manipulandum.x[:-1] * manipulandum.y[1:]

    return 1/(2*manipulandum.n)*np.sum(np.abs(column1-column2))


def compute_sway_density(manipulandum, radius):

    SD = []
    for i_n, (x_n, y_n) in enumerate(zip(manipulandum.x,
                                         manipulandum.y)):
        SD_pos = 0
        SD_neg = 0

        # SD+
        for x_p, y_p in zip(manipulandum.x[i_n+1:],
                            manipulandum.y[i_n+1:]):
            if np.sqrt((x_p-x_n)**2 + (y_p-y_n)**2) <= radius:
                SD_pos += 1
            else:
                break

        # SD-
        if i_n >= 1:
            for x_p, y_p in zip(manipulandum.x[i_n-1::-1],
                                manipulandum.y[i_n-1::-1]):
                if np.sqrt((x_p-x_n)**2 + (y_p-y_n)**2) <= radius:
                    SD_neg += 1
                else:
                    break

        SD.append((SD_pos+SD_neg)/manipulandum.fs)

    return np.array(SD)


def filtering(SD, fs, fc=2.5):
    """
    fc = Cut-off frequency of the filter
    """
    w = fc / (fs/2)  # Normalize the frequency
    b, a = butter(4, w, 'low')  # Butterworth filter of order 4

    return filtfilt(b, a, SD)


def peaks_sway_density(manipulandum, SD):
    """
    Finds the peaks of sway density
    The sway density signal is first low-pass filtered with a Butterworth filter of
    order 4 (Jacono et al., 2004). The peaks are found using scipy's find_peaks
    """

    # Mean sway density peak
    i_peaks, _ = find_peaks(filtering(SD, manipulandum.fs, fc=2.5))
    peaks = SD[i_peaks]
    mean_peaks = np.mean(peaks)

    # Mean spatial distance between sway density peaks
    dist_peaks_x = np.diff(manipulandum.x[i_peaks])
    dist_peaks_y = np.diff(manipulandum.y[i_peaks])
    mean_dist_peaks = np.sum(
        np.sqrt(dist_peaks_x**2 + dist_peaks_y**2))

    return i_peaks, peaks, mean_peaks, mean_dist_peaks


def process(manipulandum):

    saps = sway_area_per_second(manipulandum)
    SD = compute_sway_density(
        manipulandum, manipulandum.params['descriptors']['dynamic']['sway']['radius'])
    i_peaks, peaks, mean_peaks, mean_dist_peaks = peaks_sway_density(
        manipulandum, SD)

    manipulandum._results['dynamic'].update({
        'sway': {
            'saps': saps,
            'SD': SD,
            'i_peaks': i_peaks,
            'peaks': peaks,
            'mean_peaks': mean_peaks,
            'mean_dist_peaks': mean_dist_peaks
        }
    })

    return
