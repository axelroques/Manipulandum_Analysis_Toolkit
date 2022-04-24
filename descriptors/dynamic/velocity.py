
import numpy as np


def zero_crossing(manipulandum):
    """
    Finds the zero crossings (of velocity)
    Returns the position right after the zero crossing
    """

    # Zero crossing x
    zeros_x = np.where(np.diff(np.signbit(manipulandum.v_x)))[0] + 1

    # Zero crossing y
    zeros_y = np.where(np.diff(np.signbit(manipulandum.v_y)))[0] + 1

    return np.sum(zeros_x), np.sum(zeros_y)


def compute_mean_velocity(manipulandum):
    """
    Sway length and sway path computations
    """

    ###############
    # Sway length #
    ###############
    sl_x = np.sum(np.diff(manipulandum.v_x))
    sl_y = np.sum(np.diff(manipulandum.v_y))
    sl_tot = np.sum(np.sqrt(np.diff(manipulandum.v_x)**2 +
                            np.diff(manipulandum.v_y)**2))

    #############
    # Sway path #
    #############
    spd_x = sl_x/manipulandum.n
    spd_y = sl_y/manipulandum.n
    spd_tot = sl_tot/manipulandum.n

    return sl_x, sl_y, sl_tot, spd_x, spd_y, spd_tot


def velocity_peak(manipulandum):
    """
    Finds peaks in the velocity signals
    """

    zeros_x = np.where(np.diff(np.signbit(manipulandum.v_x)))[0] + 1
    zeros_y = np.where(np.diff(np.signbit(manipulandum.v_y)))[0] + 1

    ###############
    # x component #
    ###############
    peaks_x = []
    for i1, i2 in zip(zeros_x[:-1], zeros_x[1:]):
        # Cut velocity dataframe
        cut = manipulandum.v_x[i1+1:i2]
        # Get peak
        if len(cut) == 0:
            continue
        peaks_x.append(max(cut, key=abs))

    # Positive peaks
    peaks_pos = np.array(peaks_x)[np.where(np.array(peaks_x) > 0)]
    peak_x_vel_pos = np.mean(peaks_pos)

    # Negative peaks
    peaks_neg = np.array(peaks_x)[np.where(np.array(peaks_x) < 0)]
    peak_x_vel_neg = np.mean(peaks_neg)

    # All peaks
    peaks_x_vel = np.mean(peaks_x)

    ###############
    # y component #
    ###############
    peaks_y = []
    for i1, i2 in zip(zeros_y[:-1], zeros_y[1:]):
        # Cut velocity dataframe
        cut = manipulandum.v_y[i1+1:i2]
        # Get peak
        if len(cut) == 0:
            continue
        peaks_y.append(max(cut, key=abs))

    # Positive peaks
    peaks_pos = np.array(peaks_y)[np.where(np.array(peaks_y) > 0)]
    peak_y_vel_pos = np.mean(peaks_pos)

    # Negative peaks
    peaks_neg = np.array(peaks_y)[np.where(np.array(peaks_y) < 0)]
    peak_y_vel_neg = np.mean(peaks_neg)

    # All peaks
    peaks_y_vel = np.mean(peaks_y)

    return peak_x_vel_pos, peak_x_vel_neg, peaks_x_vel, \
        peak_y_vel_pos, peak_y_vel_neg, peaks_y_vel


def process(manipulandum):

    zc = zero_crossing(manipulandum)
    sl_x, sl_y, sl_tot, spd_x, spd_y, spd_tot = compute_mean_velocity(
        manipulandum)
    peak_x_vel_pos, peak_x_vel_neg, peaks_x_vel, \
        peak_y_vel_pos, peak_y_vel_neg, peaks_y_vel = velocity_peak(
            manipulandum)

    return zc, sl_x, sl_y, sl_tot, spd_x, spd_y, spd_tot, \
        peak_x_vel_pos, peak_x_vel_neg, peaks_x_vel, \
        peak_y_vel_pos, peak_y_vel_neg, peaks_y_vel
