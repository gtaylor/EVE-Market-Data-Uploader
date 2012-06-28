import unittest
import platform
from emdu.cache_detector import CacheDetector

class CacheDetectorTests(unittest.TestCase):
    """
    Tests for the auto-detection and loading of EVE cache directories.
    """

    def test_detect(self):
        """
        Tests the most basic case of auto cache detection. Uses the appropriate
        auto-discovery module for the OS the tests are ran on.
        """

        detector = CacheDetector()
        caches = detector.autodetect_caches()

        # Should have found at least one.
        self.assertNotEqual(0, len(caches),
            "No %s caches detected." % platform.system())