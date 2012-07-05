"""
Cache directory auto-detection for Mac OS.
"""

import os
from emdu.cache_detector.base_loader import BaseCacheLoader

class MacCacheDetector(BaseCacheLoader):
    """
    Cache detection for Mac. The Mac directories are split up all over the
    place, so this one ends up being kind of wonky.
    """

    def _get_eve_dirs(self):
        """
        Platform-specific searching for EVE installation directories.

        :rtype: generator
        :returns: A generator of path strings to EVE installations.
        """

        home_dir = os.path.expanduser('~/')

        # Mac has an official installer that puts things in a very
        # consistent location. We'll pick up the default location.
        default_path = os.path.join(
            home_dir,
            "Library/Application Support/EVE Online/p_drive/Local Settings/Application Data/CCP/EVE/")

        if os.path.exists(default_path):
            yield default_path