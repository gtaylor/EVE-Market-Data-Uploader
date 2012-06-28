import os
import time
from emdu.cache_watcher.base_watcher import BaseCacheWatcher

class CrudeCacheWatcher(BaseCacheWatcher):
    """
    A basic cross-platform cache monitor. Not the most efficient, but this
    should run on basically anything.

    .. note:: Due to the reliance on os.stat() and st_mtime, this watcher
        can periodically miss new cache calls if your user's filesystem isn't
        very precise. This is particularly the case with FAT32.
    """

    def __init__(self, cache_dir_path):
        """
        :param str cache_dir_path: Absolute path to the directory to
            monitor for modification.
        """

        self.cache_dir_path = cache_dir_path
        self.last_scanned = 0

    def scan_for_updated_files(self):
        """
        Scans the cache folder for updates.

        .. warning:: Due to varying levels of st_mtime
            on each filesystem, you'll want to avoid calling this in intervals
            of less than two seconds. Three seconds and up is highly recommended.

        :rtype: list
        :returns: A list of full paths to cache files that have changed since
            the last time this method was ran.
        """

        updated = []
        for cache_file in os.listdir(self.cache_dir_path):
            full_cache_file_path = os.path.join(self.cache_dir_path, cache_file)
            # We do this to get the file's last modified time.
            stat_result = os.stat(full_cache_file_path)
            # File's last modified time.
            cache_mtime = stat_result.st_mtime

            if cache_mtime > self.last_scanned:
                # This file was modified since the last time we ran this method.
                # Stick it on the list to return.
                updated.append(full_cache_file_path)

        # Move the chains.
        self.last_scanned = time.time()
        return updated