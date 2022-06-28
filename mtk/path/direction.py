
import matplotlib.pyplot as plt
import numpy as np


def plot_polar(theta, bin_size=5):
    """
    Plots the polar histogram for the directions of movement of the manipulandum.

    bin_size = size of the bins (in deg)
    """

    _, ax = plt.subplots(subplot_kw={'projection': 'polar'},
                         figsize=(8, 8))

    # Binning parameters
    n_bins = 360 // bin_size
    bins = np.linspace(-np.pi, np.pi, n_bins+1)

    # Shift bins to center them on the cardinal directions
    bins += abs(bins[1]-bins[0])/2

    # Binning computation
    bin_values, _ = np.histogram(theta, bins, density=True)

    # Histogram plot
    bin_width = 2*np.pi/n_bins
    ax.bar(bins[:-1], bin_values*100*bin_width, width=bin_width,
           align='edge', color='crimson', alpha=0.5)

    ax.set_rticks(range(5, int(max(bin_values*100*bin_width)), 5))

    plt.show()

    return


def compute_directions(manipulandum, bin_size=5, n_min=None, plot=True):
    """
    Computes the angle formed by (x, y) and the positive x-axis.
    """

    try:
        dt = np.diff(manipulandum.t_simplified)
        dx = np.diff(manipulandum.x_simplified)
        dy = np.diff(manipulandum.y_simplified)

    except AttributeError:
        print('Use the simplify function to simplify the path and get better results.')
        dt = np.diff(manipulandum.t)
        dx = np.diff(manipulandum.x)
        dy = np.diff(manipulandum.y)

    # Compute directions of the vectors with regards to the horizontal
    theta = np.arctan2(dy, dx)

    # Optionally select a subset of angles for longer motions, as
    # defined by parameter n_min
    if n_min:
        theta = theta[np.where(dt > n_min * (1/manipulandum.fs))]
        print(
            f'Criteria n_min={n_min} selected {len(theta)/len(dt):.1%} of the data.')

    if plot:
        plot_polar(theta, bin_size=bin_size)

    # Update results dictionary
    manipulandum._results['path'].update({
        'direction': {
            'theta': theta
        }
    })

    return
