"""
Cache directory auto-detection for Windows OS.
"""

import os
from emdu.cache_detector.base_loader import BaseCacheLoader

class WindowsCacheDetector(BaseCacheLoader):
    """
    Cache detection for Windows.
    """

    def _get_eve_dirs(self):
        """
        Platform-specific searching for EVE installation directories.

        :rtype: generator
        :returns: A generator of path strings to EVE installations.
        """

        # The install locations are pretty consistent with Windows, since
        # there's an official installer.fd
        home_dir = os.path.expanduser('~/')
        default_path = os.path.join(
            home_dir,
            "AppData/Local/CCP/EVE/"
        )

        if os.path.exists(default_path):
            yield default_path

