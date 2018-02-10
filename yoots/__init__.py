import sys


def eprint(msg):
    """Print a message to stderr with a trailing newline."""
    sys.stderr.write("{}\n".format(msg))
