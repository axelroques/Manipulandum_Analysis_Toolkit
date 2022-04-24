
from scipy.signal.windows import bartlett
from scipy.signal import welch


def welch_periodogram(manipulandum):
    """
    Uses a Bartlett (triangular) window of size 2048 
    """

    n_window = 2048
    window = bartlett(n_window)

    f, Pxx_x = welch(x=manipulandum.x,
                     fs=manipulandum.fs,
                     window=window)

    _, Pxx_y = welch(x=manipulandum.y,
                     fs=manipulandum.fs,
                     window=window)

    return f, Pxx_x, Pxx_y


def process(manipulandum):

    f, Pxx_x, Pxx_y = welch_periodogram(manipulandum)

    return f, Pxx_x, Pxx_y
