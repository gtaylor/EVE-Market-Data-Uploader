import unittest
import platform

class LoaderTests(unittest.TestCase):
    """
    Tests for the auto-detection and loading of EVE cache directories.
    """

    def setUp(self):
        """
        Determine the correct loader class to use.
        """
        platform_name = platform.system()

        if platform_name == 'Linux':
            from emdu.cache_loading import linux
            self.loader_class = linux.LinuxCacheLoader
        elif platform_name == 'Darwin':
            from emdu.cache_loading import mac
            self.loader_class = mac.MacCacheLoader
        elif platform_name == 'Windows':
            from emdu.cache_loading import windows
            self.loader_class = windows.WindowsCacheLoader
        else:
            raise Exception("Un-recognized platform: %s" % platform_name)

    def test_detect(self):
        """
        Tests the most basic case of auto cache detection. Uses the appropriate
        auto-discovery module for the OS the tests are ran on.
        """

        loader = self.loader_class()
        caches = loader.autodetect_caches()
        # Should have found at least one.
        self.assertNotEqual(0, len(caches),
            "No %s caches detected." % platform.system())

        #for cache in caches:
        #    eve = blue.EVE(cache)
        #    c.getcachemgr()


    def test_load(self):
        loader = self.loader_class()
        print "CACHES", loader.load_caches()