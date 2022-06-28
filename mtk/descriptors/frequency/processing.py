
from . import welch


def process_freq_desc(manipulandum):

    # Add 'frequency' key to the result dictionary
    manipulandum._results.update({
        'frequency': {}
    })

    # Process frequency descriptors
    welch.process(manipulandum)

    return
