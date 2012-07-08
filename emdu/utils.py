"""
Some assorted utility functions.
"""
import os

def delete_cache_file(cache_file):
    """
    Deletes a cache file. Ignores some common, typically harmless errors.

    :param basestring cache_dir: Full path to a cache file to delete.
    """

    try:
        os.unlink(cache_file)
    except (IOError, OSError):
        pass

def empty_cache_dir(cache_dir):
    """
    Given a path to a cache dir, clear it out.

    :param basestring cache_dir: Full path to a cache dir to empty.
    """

    for root, dirs, files in os.walk(cache_dir):
        for cache_file in files:
            delete_cache_file(os.path.join(root, cache_file))