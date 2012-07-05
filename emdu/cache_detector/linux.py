"""
Cache directory auto-detection for Linux.
"""

import os
import pwd
from emdu.cache_detector.base_loader import BaseCacheLoader

class LinuxCacheDetector(BaseCacheLoader):
    """
    Cache detection for Linux. Looks in the user's Wine home.
    """

    def _get_eve_dirs(self):
        """
        Platform-specific searching for EVE installation directories.

        :rtype: generator
        :returns: A generator of path strings to EVE installations.
        """

        home_dir = os.path.expanduser('~/')
        username = pwd.getpwuid(os.getuid())[0]

        # With Linux, most are going to keep the default path. Though, due
        # to their nerdyness, Linux nerds can put these installs all over
        # the place, so we probably don't have much of a reason to get too
        # detailed with this.
        default_path = os.path.join(home_dir, ".wine/drive_c/users", username,
            "Local Settings/Application Data/CCP/EVE/")

        if os.path.exists(default_path):
            yield default_path