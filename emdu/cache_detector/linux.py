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

    def autodetect_caches(self):
        """
        Auto-detect cache paths on Linux.

        :rtype: list
        :returns: A list of cache directory paths.
        """

        home_dir = os.path.expanduser('~/')
        username = pwd.getpwuid(os.getuid())[0]

        # Potential cache dir name possibilities.
        cache_dirname_possibilities = [
            # This may be old and no longer used.
            "d_eve_tranquility",
            # Found on my machine.
            "c_program_files_(x86)_ccp_eve_tranquility",
        ]

        # Stores the path to the detected caches.
        caches_found = []

        # This will eventually detect multiple installations, I guess.
        for cache_dir in cache_dirname_possibilities:
            path = os.path.join(
                home_dir,
                ".wine/drive_c/users",
                username,
                "Local Settings/Application Data/CCP/EVE/%s/cache/MachoNet/87.237.38.200/" % cache_dir
            )
            if not os.path.exists(path):
                # Can't find a match for this path.
                continue

            most_recent_version = self.find_latest_cache_version(path)
            if not most_recent_version:
                # No cache dirs yet, we can't use this.
                continue

            path = os.path.join(path, most_recent_version, "CachedMethodCalls")
            if not os.path.exists(path):
                # Doesn't exist, can't use it.
                continue

            caches_found.append(path)

        return caches_found