"""
Very simple console-based uploader client.
"""
import time
from multiprocessing import Process, Queue
from emdu.cache_detector import CacheDetector
from emdu.cache_watcher.crude_watcher import CrudeCacheWatcher
from emdu.cachefile_serializer import serialize_cache_file
from emdu.console_client import settings
from emdu.message_uploader import upload_message

upload_queue = Queue()

def cache_worker(cache_dir, upload_queue):
    """
    Do work, son.
    """
    cache_watcher = CrudeCacheWatcher(cache_dir)
    while True:
        time.sleep(settings.CACHE_SCAN_INTERVAL)
        updated_files = cache_watcher.scan_for_updated_files()

        for cache_file in updated_files:
            print(" $ Checking %s" % cache_file)
            message_json = serialize_cache_file(cache_file)
            if message_json:
                upload_queue.put(message_json)

def upload_worker(upload_queue):
    while True:
        message_json = upload_queue.get()
        print "UPLOAD", message_json
        upload_message(message_json)

def run():
    """
    The beginning of the line for the client.
    """
    cache_detector = CacheDetector()
    print("Watching EVE cache dirs:")
    cache_dirs = cache_detector.autodetect_caches()
    for cache_dir in cache_dirs:
        print(" * %s" % cache_dir)
        cache_worker_process = Process(
            target=cache_worker,
            args=(cache_dir, upload_queue)
        )
        cache_worker_process.start()

    uploader_process = Process(target=upload_worker, args=(upload_queue,))
    uploader_process.start()