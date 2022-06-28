
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def angle_between(vector_a, vector_b):
    """
    Computes the angle between two vectors.
    Returns the angle in deg.
    """

    # If any of the input vector is the null vector, return 0
    if (not np.any(vector_a)) or (not np.any(vector_b)):
        return 0

    else:

        # Before taking the arccos, check if computation falls
        # in the definition domain of arccos
        angle = np.dot(vector_a, vector_b) / \
            (np.linalg.norm(vector_a) *
             np.linalg.norm(vector_b))

        # print('angle =', angle)

        # Manually correct precision errors
        if angle > 1:
            angle = 1
        if angle < -1:
            angle = -1

        return np.round(np.rad2deg(np.arccos(angle)), 2)


def update_data(data, clustered_vector, t):

    data['t'].append(t)
    data['x'].append(data['x'][0]+clustered_vector[0])
    data['y'].append(data['y'][0]+clustered_vector[1])

    return data


def compare_paths(og_x, og_y, simp_x, simp_y):
    """
    Compare two (x, y) paths.
    """

    _, axes = plt.subplots(1, 2, figsize=(15, 8))

    for i, (x, y, ax, c) in enumerate(zip([og_x, simp_x],
                                          [og_y, simp_y],
                                          axes.ravel(),
                                          ['royalblue', 'crimson'])):

        ax.plot(x, y, c=c, alpha=0.5)
        ax.axhline(c='silver', ls='--', alpha=0.4)
        ax.axvline(c='silver', ls='--', alpha=0.4)

        ax.set_title('True path' if i == 0 else 'Simplified path')

    # Plot parameters
    x_max = max(max(og_x, key=abs), max(simp_x, key=abs), key=abs)
    y_max = max(max(og_y, key=abs), max(simp_y, key=abs), key=abs)
    for ax in axes:
        ax.set_xlim((-abs(x_max), abs(x_max)))
        ax.set_ylim((-abs(y_max), abs(y_max)))

    return


def simplify(manipulandum, threshold=45, plot=True):
    """
    From a manipulandum object initialized with 3 numpy 
    arrays t, x and y, cluster successive samples together 
    using an angular deviation threshold.
    """

    # Initialization
    data = {
        't': [manipulandum.t[0]],
        'x': [manipulandum.x[0]],
        'y': [manipulandum.y[0]]
    }
    clustered_vector = np.zeros(2)
    to_append = False

    # Compute vectors from samples
    dx = np.diff(manipulandum.x)
    dy = np.diff(manipulandum.y)
    vectors = np.stack([dx, dy], axis=1)

    # Loop over vectors
    i = 0
    while i < len(vectors)-1:

        # Store new vector
        clustered_vector += vectors[i]

        # Compute angle between vectors
        angle = angle_between(vectors[i], vectors[i+1])

        # Clustering procedure
        if angle < threshold:
            to_append = False
        else:
            to_append = True

        # Append sample coordinates
        if to_append:
            data = update_data(data, clustered_vector, manipulandum.t[i+1])

        i += 1

    # Termination
    clustered_vector += vectors[i]
    data = update_data(data, clustered_vector, manipulandum.t[i+1])

    # Plot
    if plot:
        compare_paths(manipulandum.x, manipulandum.y,
                      data['x'], data['y'])

    manipulandum.t_simplified = data['t']
    manipulandum.x_simplified = data['x']
    manipulandum.y_simplified = data['y']

    return pd.DataFrame(data=data)
