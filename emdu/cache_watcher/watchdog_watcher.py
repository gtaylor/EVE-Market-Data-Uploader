import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from emdu.cache_watcher.base_watcher import BaseCacheWatcher

logger = logging.getLogger(__name__)

class WatchdogCacheWatcher(BaseCacheWatcher):
    """
    Uses the watchdog Python module to monitor for changes. Much more efficient
    and accurate than :py:mod:`crude_watcher`.

    .. note:: This watcher requires watchdog (available at
        http://pypi.python.org/pypi/watchdog/), and is automatically used
        if present.
    """

    def __init__(self, cache_dir_path):
        """
        :param str cache_dir_path: Absolute path to the directory to
            monitor for modification.
        """

        self.modified_files = set()
        logger.info("Starting watchdog cache watcher for: %s" % cache_dir_path)
        event_handler = EVECacheEventHandler(watcher=self)
        observer = Observer()
        observer.schedule(event_handler, path=cache_dir_path, recursive=False)
        observer.start()

    def scan_for_updated_files(self):
        """
        Fakes a scan of the cache dir by simply returning the created/modified
        files since the last time this method was ran.

        :rtype: set
        :returns: A set of full paths to cache files that have changed since
            the last time this method was ran.
        """

        # Create a copy so we can empty the set on this instance before returning.
        to_announce = self.modified_files.copy()
        # Nuke it so we start clean for the next call of this method.
        self.modified_files = set()
        return to_announce


class EVECacheEventHandler(FileSystemEventHandler):
    """
    This is somewhat of a nasty hacked handler that tosses any modified or
    created files into a set on the WatchdogCacheWatcher instance, for
    later reporting by scan_for_updated_files().
    """

    def __init__(self, *args, **kwargs):
        # A reference back to the watcher. We'll use this to get at the
        # watcher.modified_files set.
        self.watcher = kwargs['watcher']

    def _report_change(self, event):
        """
        Hacky method used to report that a cache file has been created/modified.

        :param watchdog.events.FileSystemEvent event: The event that was fired.
        """

        is_file = not event.is_directory
        # We're only interested in files.
        if not is_file:
            return

        # Adds the created/modified cache file to the set of files that
        # have changed since the last scan.
        self.watcher.modified_files.add(event.src_path)

    def on_created(self, event):
        super(EVECacheEventHandler, self).on_created(event)

        self._report_change(event)

    def on_modified(self, event):
        super(EVECacheEventHandler, self).on_modified(event)

        self._report_change(event)