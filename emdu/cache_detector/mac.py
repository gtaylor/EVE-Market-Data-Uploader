"""
Cache directory auto-detection for Mac OS.
"""

import os, subprocess
from emdu.cache_detector.base_loader import BaseCacheLoader

class MacCacheDetector(BaseCacheLoader):
    """
    Cache detection for Mac. The Mac directories are split up all over the
    place, so this one ends up being kind of wonky.
    """

    def autodetect_caches(self):
        """
        Auto-detect cache paths on Mac OS.

        :rtype: list
        :returns: A list of cache directory paths.
        """

        # Potential cache dir name possibilities.
        cache_dirname_possibilities = [
            # Found on my machine.
            "c_program_files_ccp_eve_tranquility",
        ]

        # Stores the path to the detected caches.
        caches_found = []

        for cache_dir in cache_dirname_possibilities:
            # get user
            # this takes less time searching, and only makes sense searching on the current user, imho.
            # to find under any other user, we should not add this var to the search query
            cuser = os.path.join(os.environ['HOME'], 'Library')

            # this searches in /Users/_username_/Library

            command = ["find", cuser, "-name", cache_dir, "-type", "d"]
            ret = subprocess.Popen(command, stdout=subprocess.PIPE)
            out, err = ret.communicate()
            
            folders = out.splitlines()

            for folder in folders:
                
                # Each EVE install should give you 2 folder paths in here.
                # If the test folder does not exist, continue; that's not the one we want.
                test_folder = os.path.join(folder, 'cache')
                if not os.path.isdir(test_folder):
                    continue

                path = os.path.join(folder, 'cache', 'MachoNet', '87.237.38.200')
                most_recent_version = self.find_latest_cache_version(path)
                if not most_recent_version:
                    # No cache dirs yet, we can't use this.
                    continue
                
                cFolder = os.path.join(path, most_recent_version, 'CachedMethodCalls')
                if os.path.isdir(cFolder):
                    caches_found.append(cFolder)

        # This will eventually detect multiple installations, I guess.
        return caches_found