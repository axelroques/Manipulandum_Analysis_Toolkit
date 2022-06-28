
from . import dispersion


def process_pos_desc(manipulandum):

    # Add 'positional' key to the result dictionary
    manipulandum._results.update({
        'positional': {}
    })

    # Process positional descriptors
    dispersion.process(manipulandum)

    return
