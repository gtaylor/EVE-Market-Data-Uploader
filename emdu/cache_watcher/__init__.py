"""
Import this module and refer to its ``CacheWatcher`` variable for a watcher class
to use.
"""

# First try to use the watchdog based watcher, which uses OS-specific filesystem
# monitoring. If the watchdog module is absent, fall back to a really naive,
# inefficient crude watcher.

try:
    #noinspection PyPackageRequirements
    #noinspection PyUnresolvedReferences
    import watchdog
    from emdu.cache_watcher.watchdog_watcher import WatchdogCacheWatcher as CacheWatcher
except ImportError:
    from emdu.cache_watcher.crude_watcher import CrudeCacheWatcher as CacheWatcher