"""
Cache directory auto-detection for Mac OS.
"""

import os
from emdu.cache_detector.base_loader import BaseCacheLoader

class WindowsCacheDetector(BaseCacheLoader):
    """
    Cache detection for Windows.
    """

    def autodetect_caches(self):
        """
        Auto-detect cache paths on Mac OS.

        :rtype: list
        :returns: A list of cache directory paths.
        """
        # This appears to suffice for Mac, whereas it can cause issues on some
        # Linux distros.
        home_dir = os.path.expanduser('~/')

        # Potential cache dir name possibilities.
        cache_dirname_possibilities = [
            # Found on my machine.
            # C:\Users\Snipa\AppData\Local\CCP
            # C:\Users\Snipa\AppData\Local\CCP\EVE\c_program_files_(x86)_ccp_eve_tranquility\cache\MachoNet\87.237.38.200\330\CachedMethodCalls
            "c_program_files_ccp_eve_tranquility/cache/MachoNet/87.237.38.200/",
            "c_program_files_(x86)_ccp_eve_tranquility/cache/MachoNet/87.237.38.200/",


        ]

        # Stores the path to the detected caches.
        caches_found = []

        # This will eventually detect multiple installations, I guess.
        for cache_dir in cache_dirname_possibilities:
            path = os.path.join(
                home_dir,
                "AppData/Local/CCP/EVE/%s" % cache_dir
            )
            print path
            if os.path.exists(path):
                dirs = os.listdir(path)
                dirs.sort()
                caches_found.append(os.path.join(path, "%s/CachedMethodCalls" % dirs.pop()))

        # This will eventually detect multiple installations, I guess.
        return caches_found
