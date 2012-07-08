"""
BaseCacheWatcher is mostly just used as an interface for other cache watcher
classes.
"""

class BaseCacheWatcher(object):
    """
    A base cache watcher class. Sub-class this with the implementation-specific
    BS.
    """

    def scan_for_updated_files(self):
        """
        Scans the cache folder for updates. Override this in your base class!

        .. warning:: Due to varying levels of st_mtime
            on each filesystem, you'll want to avoid calling this in intervals
            of less than two seconds. Three seconds and up is highly recommended.

        :rtype: list
        :returns: A list of full paths to cache files that have changed since
            the last time this method was ran.
        """
        raise NotImplementedError