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

        # An eventual list of cache version ints.
        cache_versions = []

        # Convert all cache dirs to ints.
        for version_dir in os.listdir(path):
            try:
                version_num = int(version_dir)
            except (TypeError, ValueError):
                # This was probably .DS_Store, or some other non-relevant dir.
                continue
            cache_versions.append(version_num)

        if not cache_versions:
            return None

        cache_versions.sort()
        return str(cache_versions[-1])
