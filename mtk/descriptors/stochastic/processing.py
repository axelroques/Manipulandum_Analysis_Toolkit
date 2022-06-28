
from . import msd


def process_stoch_desc(manipulandum):

    # Add 'stochastic' key to the result dictionary
    manipulandum._results.update({
        'stochastic': {}
    })

    # Process stochastic descriptors
    msd.process(manipulandum)

    return
