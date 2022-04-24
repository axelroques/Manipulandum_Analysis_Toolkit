
import numpy as np


def RMS(s):
    return np.sqrt(np.mean(s**2))


def compute_phase_plane_parameter(manipulandum):

    # STD SPD x
    mean_vx = np.mean(manipulandum.v_x)
    std_spd_x = np.sqrt(np.mean(manipulandum.v_x-mean_vx))

    # STD SPD y
    mean_vy = np.mean(manipulandum.v_y)
    std_spd_y = np.sqrt(np.mean(manipulandum.v_y-mean_vy))

    # Phase plane x
    phase_plane_x = np.sqrt(RMS(manipulandum.x)**2 + std_spd_x**2)

    # Phase plane y
    phase_plane_y = np.sqrt(RMS(manipulandum.y)**2 + std_spd_y**2)

    return std_spd_x, std_spd_y, phase_plane_x, phase_plane_y


def process(manipulandum):

    std_spd_x, std_spd_y, phase_plane_x, phase_plane_y = compute_phase_plane_parameter(
        manipulandum)

    return std_spd_x, std_spd_y, phase_plane_x, phase_plane_y
