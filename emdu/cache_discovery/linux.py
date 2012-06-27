"""
Cache directory auto-detection for Linux.
"""
import os
import pwd

def autodetect_caches():
    """
    Auto-detect cache paths on Linux.

    :rtype: list
    :returns: A list of cache directory paths.
    """
    home_dir = os.path.expanduser('~/')
    username = pwd.getpwuid(os.getuid())[0]

    # Potential cache dir name possibilities.
    cache_dirname_possibilities = [
        # This may be old and no longer used.
        "d_eve_tranquility",
        # Found on my machine.
        "c_program_files_(x86)_ccp_eve_tranquility",
    ]

    # Stores the path to the detected caches.
    caches_found = []

    # This will eventually detect multiple installations, I guess.
    for cache_dir in cache_dirname_possibilities:
        path = os.path.join(
            home_dir,
            ".wine/drive_c/users",
            username,
            "Local Settings/Application Data/CCP/EVE/%s" % cache_dir
        )
        if os.path.exists(path):
            caches_found.append(path)

    return caches_found