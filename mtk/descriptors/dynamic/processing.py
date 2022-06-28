
from . import mean_frequency
from . import phase_plane
from . import sway
from . import velocity


def process_dyn_desc(manipulandum):

    # Add 'dynamic' key to the result dictionary
    manipulandum._results.update({
        'dynamic': {}
    })

    # Process dynamic descriptors
    mean_frequency.process(manipulandum)
    phase_plane.process(manipulandum)
    # sway.process(manipulandum)
    velocity.process(manipulandum)

    return
