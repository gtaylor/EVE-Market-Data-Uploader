import os
import time
import logging
from collections import OrderedDict
from emdu.cache_watcher.base_watcher import BaseCacheWatcher

logger = logging.getLogger(__name__)

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

        logger.info("Starting crude cache watcher for: %s" % cache_dir_path)
        # When the class was instantiated.
        self.start_time = time.time()
        # Full path to the cache dir being watched.
        self.cache_dir_path = cache_dir_path
        # keys are file paths, values are timestamps.
        self.cache_file_tracker = OrderedDict()
        # Max number of keys in the tracker before we start popping.
        self.cache_file_tracker_max_keys = 10000
        # Counter for current number of keys, so we can avoid the expensive
        # len(dict) operation.
        self.cache_file_tracker_keys = 0

    def see_if_file_has_new_data(self, path):
        """
        Given a file path, determine whether we should read/send it.

        :rtype: bool
        :returns: ``True`` if the file should be read, ``False`` if not.
        """

        # Catching file removal by eve before we can read the mtime from the file
        try:
            stat_result = os.stat(path)
        except (IOError, OSError):
            logger.error("Caught error from missing cache file")
            return False
            # File's last modified time.
        cache_mtime = stat_result.st_mtime

        if cache_mtime < self.start_time:
            # This file was modified before the uploader was started.
            return False

        # Not interested in files past five minutes staleness.
        cutoff = time.time() - (60 * 5)

        if cache_mtime < cutoff:
            # File is too stale to even consider.
            return False

        last_read = self.cache_file_tracker.get(path)
        if not last_read:
            # No key found, we need to read this file.
            return True

        # We've got a key, let's see if the mtimes match.
        if cache_mtime > last_read:
            # Modified time is greater than the time of our last recorded
            # reading of this file.
            return True

        return False

    def mark_file_as_read(self, path):
        """
        Given a cache file path, update its last read time in our cache file
        tracker.

        :param basestring path: The path that was read.
        """
        if self.cache_file_tracker_keys > self.cache_file_tracker_max_keys:
            # We've passed our max key count, prune the oldest entry.
            self.cache_file_tracker.popitem(last=False)
        else:
            # Still growing, keep the count updated.
            self.cache_file_tracker_keys += 1

        self.cache_file_tracker[path] = time.time()

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

        updated = set()
        for cache_file in os.listdir(self.cache_dir_path):
            full_cache_file_path = os.path.join(self.cache_dir_path, cache_file)

            if self.see_if_file_has_new_data(full_cache_file_path):
                # This file was modified since the last time we ran this method.
                # Stick it on the list to return.
                updated.add(full_cache_file_path)
                self.mark_file_as_read(full_cache_file_path)

        return updated
