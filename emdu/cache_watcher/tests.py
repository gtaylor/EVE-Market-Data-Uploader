import unittest
import tempfile
import shutil
import os.path
import time
from emdu.cache_watcher.crude_watcher import CrudeCacheWatcher

class CacheWatcherTests(unittest.TestCase):
    """
    Tests for cache watchers, which monitor for modified/new cache files.
    """

    def setUp(self):
        """
        Mocks up a fake cache directory to watch.
        """
        # Creates a named temporary dir to watch.
        self.cache_path = tempfile.mkdtemp()

    def tearDown(self):
        """
        Cleans up the cache dir.
        """
        shutil.rmtree(self.cache_path)

    def _create_fake_cache_file(self, file_name):
        """
        Utility to create a fake cache file.
        """
        fobj = open(os.path.join(self.cache_path, file_name), 'w')
        fobj.close()

    def test_watcher(self):
        """
        Tests the most basic case of auto cache detection. Uses the appropriate
        auto-discovery module for the OS the tests are ran on.
        """

        watcher = CrudeCacheWatcher(self.cache_path)
        updated = watcher.scan_for_updated_files()
        # No files exist yet, make sure we don't error or anything goofy.
        self.assertEqual(updated, [])
        # os.stat()'s st_mtime isn't very accurate much of the time. We sleep
        # here to make sure the last scanned time is less than the newly
        # created file's st_mtime. Test fails without it.
        time.sleep(0.2)
        # Create a test cache file.
        self._create_fake_cache_file('test.cache')
        # Scan for updated files.
        updated = watcher.scan_for_updated_files()
        # We should see our newly created file.
        self.assertEqual(len(updated), 1)
        # Scan again.
        updated = watcher.scan_for_updated_files()
        # We've already seen test.cache, so nothing should come back.
        self.assertEqual(len(updated), 0)
        # Sleep again, for the same reason as before.
        time.sleep(0.2)
        # Create some more files.
        self._create_fake_cache_file('test2.cache')
        self._create_fake_cache_file('test3.cache')
        updated = watcher.scan_for_updated_files()
        # Should see the two new ones.
        self.assertEqual(len(updated), 2)

