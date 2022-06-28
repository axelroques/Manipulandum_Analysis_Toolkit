
from .direction import compute_directions
from .simplify import simplify


def process_path_desc(manipulandum, simplify_path):

    # Add 'path' key to the result dictionary
    manipulandum._results.update({
        'path': {}
    })

    # Process path descriptors
    if simplify_path:
        simplify(manipulandum, **manipulandum.params['path']['simplify'])

    compute_directions(manipulandum,
                       **manipulandum.params['path']['directions'])

    return
