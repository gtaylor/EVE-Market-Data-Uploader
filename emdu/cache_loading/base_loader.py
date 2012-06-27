

class BaseCacheLoader(object):

    def autodetect_possible_caches(self):
        raise NotImplementedError

    def load_caches(self):
        caches = self.autodetect_possible_caches()