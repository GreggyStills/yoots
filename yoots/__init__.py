import sys


def eprint(msg, newline="\n"):
    """Print a message to stderr with a trailing newline."""
    sys.stderr.write("{}{}".format(msg, newline))
