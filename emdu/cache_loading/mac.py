"""
Cache directory auto-detection for Mac OS.
"""
import os
import pwd
from emdu.cache_loading.base_loader import BaseCacheLoader

class MacCacheLoader(BaseCacheLoader):

    def autodetect_caches(self):
        """
        Auto-detect cache paths on Mac OS.

        :rtype: list
        :returns: A list of cache directory paths.
        """
        home_dir = os.path.expanduser('~/')
        username = pwd.getpwuid(os.getuid())[0]

        # Potential cache dir name possibilities.
        cache_dirname_possibilities = [
            # Found on my machine.
            "c_program_files_ccp_eve_tranquility",
        ]

        # Stores the path to the detected caches.
        caches_found = []

        # This will eventually detect multiple installations, I guess.
        for cache_dir in cache_dirname_possibilities:
            path = os.path.join(
                home_dir,
                "Library/Application Support/EVE Online/p_drive/Local Settings/Application Data/CCP/EVE/%s" % cache_dir
            )
            if os.path.exists(path):
                caches_found.append(path)

        # This will eventually detect multiple installations, I guess.
        return caches_found