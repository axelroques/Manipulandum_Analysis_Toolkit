
from .init import *


def Positional(manipulandum):

    radius_signal, cov, avg, mean_dist_x, mean_dist_y, mean_dist_radius_signal, \
        max_x, max_y, max_radius, rms_x, rms_y, rms_radius, \
        range_x, range_y, range_xy, range_ratio, planar_deviation, \
        coeff_sway_direction, confidence_sway_area, principal_sway_direction = dispersion.process(
            manipulandum)

    return
