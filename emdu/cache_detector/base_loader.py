import os

class BaseCacheLoader(object):
    """
    Base cache loader class that implements an interface and some generally
    useful methods for all or most OS-specific loaders.
    """

    def autodetect_caches(self):
        """
        Override this in your detector's sub-class. Auto-detects cache paths.

        :rtype: list
        :returns: A list of cache directory paths.
        """

        raise NotImplementedError

    def find_latest_cache_version(self, path):
        """
        Given a server's MachoNet sub-dir, pick out the highest versioned
        cache directory and return it.

        :param str path: Full path to an EVE server's MachoNet sub-dir.
            For Tranquility, this is [...]/87.237.38.200.
        :rtype: str or None
        :returns: The most recent MachoNet server cache dir. If no directories
            are found, return None.
        """
        # Convert all cache dirs to ints.
        # TODO: Handle failure here in case someone does some goofy shit with
        # their directories. Or maybe we just let them suffer. Har.
        cache_versions = [int(x) for x in os.listdir(path)]
        if not cache_versions:
            return None

        cache_versions.sort()
        return str(cache_versions[-1])
