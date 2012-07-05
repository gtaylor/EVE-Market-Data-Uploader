"""
Various signal handlers.
"""

import signal, sys

def sigint_handler(signum, frame):
    """
    SIGINT is, by default, sent when a Keyboard interrupt is done by the user.
    This tends to be CTRL+C.
    """
    print("EMDU stopped.")
    sys.exit(1)

signal.signal(signal.SIGINT, sigint_handler)