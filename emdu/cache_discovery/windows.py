"""
Cache directory auto-detection for Mac OS.
"""
import os
import pwd

path = os.path.expanduser('~/Library/Application Support/EVE Online/p_drive/Local Settings/Application Data/CCP/EVE/c_program_files_ccp_eve_tranquility/')

def autodetect_caches():
    """
    Auto-detect cache paths on Mac OS.

    :rtype: list
    :returns: A list of cache directory paths.
    """
    # This appears to suffice for Mac, whereas it can cause issues on some
    # Linux distros.
    home_dir = os.path.expanduser('~/')

    # Potential cache dir name possibilities.
    cache_dirname_possibilities = [
        # Found on my machine.
        "c_program_files_ccp_eve_tranquility",
    ]

    # Stores the path to the detected caches.
    caches_found = []

    # This will eventually detect multiple installations, I guess.
    for cache_dir in cache_dirname_possibilities:
        path = os.path.join(
            home_dir,
            "Library/Application Support/EVE Online/p_drive/Local Settings/Application Data/CCP/EVE/%s" % cache_dir
        )
        if os.path.exists(path):
            caches_found.append(path)

    # This will eventually detect multiple installations, I guess.
    return caches_found