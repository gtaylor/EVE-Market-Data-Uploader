"""
This module implements cache detectors for each of the platforms EVE runs
on (Windows, Mac, and Linux). The ``base_loader`` module contains the basic
interface, while the ``windows``, ``mac``, and ``linux`` modules contain the
platform-specific goodies.

To use the cache detector, implement the ``CacheDetector`` class defined
in this __init__ module. For example::

    from emdu.cache_detector import CacheDetector
    detector = CacheDetector()
    cache_dirs = detector.autodetect_caches()
"""

import platform

platform_name = platform.system()

# Given the platform name, define CacheDetector accordingly. Import and use
# this CacheDetector.
if platform_name == 'Linux':
    from emdu.cache_detector import linux
    CacheDetector = linux.LinuxCacheDetector
elif platform_name == 'Darwin':
    from emdu.cache_detector import mac
    CacheDetector = mac.MacCacheDetector
elif platform_name == 'Windows':
    from emdu.cache_detector import windows
    CacheDetector = windows.WindowsCacheDetector
else:
    raise Exception("Un-recognized platform: %s" % platform_name)