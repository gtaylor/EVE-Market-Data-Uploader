import os

class BaseCacheLoader(object):
    """
    Base cache loader class that implements an interface and some generally
    useful methods for all or most OS-specific loaders.
    """

    def autodetect_caches(self, additional_eve_dirs=None):
        """
        High-level auto-detection method. In your sub-classes, override
        the other methods referenced here with platform-specific behavior.

        :keyword list additional_eve_dirs: If speficied, append this list of
            additional paths to search for cache dirs.
        :rtype: list
        :returns: A list of cache directory paths.
        """

        # Stores the path to the detected caches.
        caches_found = []
        eve_dirs = self._get_eve_dirs()
        if additional_eve_dirs:
            eve_dirs += additional_eve_dirs

        for eve_dir in eve_dirs:
            for tranq_dir in self._find_tranquility_dirs(eve_dir):

                most_recent_version = self.find_latest_cache_version(tranq_dir)
                if not most_recent_version:
                    # No cache dirs yet, we can't use this.
                    continue

                path = os.path.join(tranq_dir, most_recent_version, "CachedMethodCalls")
                if not os.path.exists(path):
                    # Doesn't exist, can't use it.
                    continue

                caches_found.append(path)

            return caches_found

    def _get_eve_dirs(self):
        """
        Looks at a number of different locations that EVE installations can
        live, based on the platform. Verifies their existence before yielding
        the paths.

        :rtype: list
        :returns: A list of path strings to EVE installations.
        """
        raise NotImplementedError

    def _find_tranquility_dirs(self, path):
        """
        Given a base path, os.walk through it to find all Tranquility
        (87.237.38.200) directories.

        :param basestring path: The path to start searching for Tranq cache
            dirs from. The higher this is up the hierarchy, the longer this
            may take.
        :rtype: generator
        :returns: A generator of Tranquility cache paths.
        """
        for root, subfolders, files in os.walk(path):
            if '87.237.38.200' in subfolders:
                yield os.path.join(root, '87.237.38.200')

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
