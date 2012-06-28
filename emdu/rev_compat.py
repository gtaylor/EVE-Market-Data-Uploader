"""
Compat module to assist in choosing between reverence or despair.
"""

import sys

try:
    from reverence import blue
except ImportError:
    try:
        from despair import blue
    except ImportError:
        print("You must either install reverence or despair.")
        sys.exit(1)