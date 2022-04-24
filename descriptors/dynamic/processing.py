
from .init import *


def Dynamic(manipulandum):

    mean_dist_x, mean_dist_y, mean_dist_tot, \
        mean_freq_x, mean_freq_y, mean_freq = mean_frequency.process(
            manipulandum)

    std_spd_x, std_spd_y, \
        phase_plane_x, phase_plane_y = phase_plane.process(manipulandum)

    saps, SD, i_peaks, peaks, mean_peaks, mean_dist_peaks = sway.process(
        manipulandum)

    zc, sl_x, sl_y, sl_tot, spd_x, spd_y, spd_tot, \
        peak_x_vel_pos, peak_x_vel_neg, peaks_x_vel, \
        peak_y_vel_pos, peak_y_vel_neg, peaks_y_vel = velocity.process(
            manipulandum)

    return
