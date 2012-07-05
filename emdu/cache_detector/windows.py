"""
Cache directory auto-detection for Windows OS.
"""

import os
from emdu.cache_detector.base_loader import BaseCacheLoader

class WindowsCacheDetector(BaseCacheLoader):
    """
    Cache detection for Windows.
    """

    def autodetect_caches(self):
        """
        Auto-detect cache paths on Windows OS.

        :rtype: list
        :returns: A list of cache directory paths.
        """
        # This appears to suffice for Mac, whereas it can cause issues on some
        # Linux distros.
        home_dir = os.path.expanduser('~/')
        base_path = os.path.join(
            home_dir,
            "AppData/Local/CCP/EVE/"
        )

        cache_dirname_possibilities = []

        for root, subFolders, files in os.walk(base_path):
            try:
                folder = subFolders.index("CachedMethodCalls")
                cache_dirname_possibilities.append(os.path.join(
                    base_path,
                    root,
                    subFolders[folder]
                ))
            except ValueError:
                pass

        # This will eventually detect multiple installations, I guess.
        return cache_dirname_possibilities

