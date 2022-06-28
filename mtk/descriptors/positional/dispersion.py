
from sklearn.decomposition import PCA
from scipy.stats import f
import numpy as np


def generate_radius_signal(manipulandum):

    radius_signal = np.sqrt(manipulandum.x**2 + manipulandum.y**2)

    return radius_signal


def compute_covariance(manipulandum):
    return (1/manipulandum.n) * (manipulandum.x*manipulandum.y).sum()


def compute_average(manipulandum):
    return manipulandum.x.mean(), manipulandum.y.mean


def compute_distance(manipulandum):

    radius_signal = generate_radius_signal(manipulandum)

    mean_dist_x = np.abs(manipulandum.x).mean()
    mean_dist_y = np.abs(manipulandum.y).mean()
    mean_dist_radius_signal = np.abs(radius_signal).mean()

    return mean_dist_x, mean_dist_y, mean_dist_radius_signal


def compute_maximum(manipulandum):

    radius_signal = generate_radius_signal(manipulandum)

    max_x = np.abs(manipulandum.x).max()
    max_y = np.abs(manipulandum.y).max()
    max_radius = radius_signal.max()

    return max_x, max_y, max_radius


def compute_RMS(manipulandum):

    radius_signal = generate_radius_signal(manipulandum)

    rms_x = np.sqrt((1/manipulandum.n)*(manipulandum.x**2).sum())
    rms_y = np.sqrt((1/manipulandum.n)*(manipulandum.y**2).sum())
    rms_radius = np.sqrt((1/manipulandum.n)*(radius_signal**2).sum())

    return rms_x, rms_y, rms_radius


def compute_ranges(manipulandum):

    range_x = manipulandum.x.max() - manipulandum.x.min()
    range_y = manipulandum.y.max() - manipulandum.y.min()

    # Too long to compute, we skip it for now
    # range_xy = np.sqrt(np.max([(manipulandum.x[i]-manipulandum.x[j])**2 + (manipulandum.y[i]-manipulandum.y[j])**2
    #                            for i in range(manipulandum.n) for j in range(i, manipulandum.n)]))

    range_xy = np.nan
    range_ratio = range_x/range_y

    return range_x, range_y, range_xy, range_ratio


def compute_planar_deviation(manipulandum):

    rms_x, rms_y, _ = compute_RMS(manipulandum)
    planar_deviation = np.sqrt(rms_x**2 + rms_y**2)

    return planar_deviation


def compute_sway_direction(manipulandum):

    rms_x, rms_y, _ = compute_RMS(manipulandum)
    cov = compute_covariance(manipulandum)
    coeff_sway_direction = cov/(rms_x*rms_y)

    return coeff_sway_direction


def compute_confidence_sway_area(manipulandum):

    rms_x, rms_y, _ = compute_RMS(manipulandum)
    cov = compute_covariance(manipulandum)

    confidence_sway_area = 2*np.pi*(manipulandum.n-1)/(manipulandum.n-2) * \
        f.ppf(.95, 2, manipulandum.n-2)*np.sqrt(rms_x**2*rms_y**2 - cov**2)

    return confidence_sway_area


def compute_principal_sway_direction(manipulandum):

    pca = PCA(n_components=2)
    X = np.concatenate([manipulandum.x[:, np.newaxis],
                        manipulandum.y[:, np.newaxis]], axis=1)
    pca.fit(X)
    v1, v2 = pca.components_[0]

    principal_sway_direction = np.arccos(
        np.abs(v2)/np.sqrt(v1**2+v2**2))*(180/np.pi)

    return principal_sway_direction


def process(manipulandum):

    cov = compute_covariance(manipulandum)
    avg = compute_average(manipulandum)
    mean_dist_x, mean_dist_y, mean_dist_radius_signal = compute_distance(
        manipulandum)
    max_x, max_y, max_radius = compute_maximum(manipulandum)
    rms_x, rms_y, rms_radius = compute_RMS(manipulandum)
    range_x, range_y, range_xy, range_ratio = compute_ranges(manipulandum)
    planar_deviation = compute_planar_deviation(manipulandum)
    coeff_sway_direction = compute_sway_direction(manipulandum)
    confidence_sway_area = compute_confidence_sway_area(manipulandum)
    principal_sway_direction = compute_principal_sway_direction(manipulandum)

    manipulandum._results['positional'].update({
        'dispersion': {
            'cov': cov,
            'avg': avg,
            'mean_dist_x': mean_dist_x,
            'mean_dist_y': mean_dist_y,
            'mean_dist_radius_signal': mean_dist_radius_signal,
            'max_x': max_x,
            'max_y': max_y,
            'max_radius': max_radius,
            'rms_x': rms_x,
            'rms_y': rms_y,
            'rms_radius': rms_radius,
            'max_x': max_x,
            'max_y': max_y,
            'range_x': range_x,
            'range_y': range_y,
            'range_xy': range_xy,
            'range_ratio': range_ratio,
            'planar_deviation': planar_deviation,
            'coeff_sway_direction': coeff_sway_direction,
            'confidence_sway_area': confidence_sway_area,
            'principal_sway_direction': principal_sway_direction
        }
    })

    return
