"""
Compat module to assist in choosing between reverence or despair.
"""

import sys

try:
    # First try reverence.
    from reverence import blue
except ImportError:
    # If that fails, try the PyPi-packaged despair.
    try:
        from despair import blue
    except ImportError:
        # Well, we're really screwed now.
        print("You must either install reverence or despair.")
        sys.exit(1)