
from .velocity import compute_mean_velocity
import numpy as np


def mean_dist(manipulandum):

    mean_dist_x = np.mean(np.abs(manipulandum.x))
    mean_dist_y = np.mean(np.abs(manipulandum.y))
    mean_dist_tot = np.mean(np.sqrt(manipulandum.x**2 +
                                    manipulandum.y**2))

    return mean_dist_x, mean_dist_y, mean_dist_tot


def mean_frequency(manipulandum):

    # Mean SPD computation
    _, _, _, spd_x, spd_y, spd_tot = compute_mean_velocity(manipulandum)

    # Mean Dist computation
    mean_dist_x, mean_dist_y, mean_dist = mean_dist(manipulandum)

    # Mean freq x
    mean_freq_x = (1/4/np.sqrt(2))*spd_x/mean_dist_x

    # Mean freq y
    mean_freq_y = (1/4/np.sqrt(2))*spd_y/mean_dist_y

    # Mean freq total
    mean_freq = (1/2/np.pi)*spd_tot/mean_dist

    return mean_freq_x, mean_freq_y, mean_freq


def process(manipulandum):

    mean_dist_x, mean_dist_y, mean_dist_tot = mean_dist(manipulandum)
    mean_freq_x, mean_freq_y, mean_freq = mean_frequency(manipulandum)

    return mean_dist_x, mean_dist_y, mean_dist_tot, \
        mean_freq_x, mean_freq_y, mean_freq
