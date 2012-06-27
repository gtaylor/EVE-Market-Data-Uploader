import unittest
import platform

class DiscoveryTests(unittest.TestCase):
    """
    Tests for the auto-detection of EVE cache directories.
    """

    def setUp(self):
        """
        Determine the correct discovery module to use.
        """
        platform_name = platform.system()

        if platform_name == 'Linux':
            from emdu.cache_discovery import linux
            self.detector = linux
        elif platform_name == 'Darwin':
            from emdu.cache_discovery import mac
            self.detector = mac
        elif platform_name == 'Windows':
            from emdu.cache_discovery import windows
            self.detector = windows
        else:
            raise Exception("Un-recognized platform: %s" % platform_name)

    def test_detect(self):
        """
        Tests the most basic case of auto cache detection. Uses the appropriate
        auto-discovery module for the OS the tests are ran on.
        """

        caches = self.detector.autodetect_caches()
        # Should have found at least one.
        self.assertNotEqual(0, len(caches),
            "No %s caches detected." % platform.system())

