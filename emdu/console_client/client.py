"""
Very simple console-based uploader client.
"""

import sys
import time
import logging
from multiprocessing import Process, Queue
import traceback
from emdu.cache_detector import CacheDetector
from emdu.cache_watcher import CacheWatcher
from emdu.cachefile_serializer import serialize_cache_file
from emdu.message_uploader import upload_message
from emdu.utils import empty_cache_dir, delete_cache_file

logger = logging.getLogger(__name__)
# Any entries in this queue are encoded JSON messages, ready for
# sending to EMDR.
UPLOAD_QUEUE = Queue(maxsize=200)

def cache_processor_worker(cache_dirs, upload_queue, delete_cache,
                           cache_scan_interval):
    """
    This is ran as a process. This function checks all detected EVE installation
    cache dirs for modified files. If files of interest are found, their
    contents are serialized and shoved into the upload queue for sending to
    EMDR.

    :param list cache_dirs: A list of cache dir paths to monitor for changes.
    :param multiprocessing.Queue upload_queue: A queue that holds encoded JSON
        messages that are ready to be sent to EMDR.
    :param bool delete_cache: If True, delete cache files after reading them.
    :param float cache_scan_interval: Interval (in seconds) to scan the caches.
    """

    # Holds all of the cache watchers we'll need to scan for updates on each
    # detected EVE install.
    cache_watchers = []
    for cache_dir in cache_dirs:
        if delete_cache:
            # If cache deletion is enabled, start by clearing out all of the old gunk.
            logger.info("Clearing old entries from cache.")
            empty_cache_dir(cache_dir)

        # Each EVE installation has a cache watcher to monitor it.
        cache_watchers.append(CacheWatcher(cache_dir))

    while True:
        # This value should never go below two seconds, and should probably
        # stay above three. This keeps filesystem mtime debauchery to a minimum.
        time.sleep(cache_scan_interval)

        # Each cache watcher represents a separate EVE install.
        for cache_watcher in cache_watchers:
            # print "Scanning for files"
            updated_files = cache_watcher.scan_for_updated_files()

            for cache_file in updated_files:
                # print(" $ Checking %s" % cache_file)
                # If this spits anything non-None out, we know it needs
                # to be uploaded to EMDR.
                message_json = serialize_cache_file(cache_file)
                if message_json:
                    # Toss the encoded JSON into the upload queue, where the
                    # upload_worker process will get it.
                    try:
                        upload_queue.put(message_json)
                        logger.debug("Message pushed to the queue for upload.")
                    except Queue.Full:
                        # Their connection probably hung, or is too slow.
                        logger.error("No room for message in upload queue. Discarding.")

                if delete_cache:
                    # If cache file deletion is enabled, trash the file.
                    delete_cache_file(cache_file)

def upload_worker(upload_queue):
    """
    This worker process watches the upload queue for new messages to upload.
    Each entry in the upload queue is an encoded, read-to-upload-to-EMDR
    message.

    :param multiprocessing.Queue upload_queue: A queue that holds encoded JSON
        messages that are ready to be sent to EMDR.
    """

    while True:
        message_json = upload_queue.get()

        try:
            upload_message(message_json)
        except Exception:
            # I hate hate hate hate to do this, but if we run into an
            # un-caught exception, this worker process dies and the queue
            # continues to fill up.
            logger.error(traceback.format_exc())

def run(additional_eve_dirs, delete_cache, cache_scan_interval,
        upload_workers):
    """
    Fires up the various processes that comprise the client. For each EVE
    install,

    :param list additional_eve_dirs: If specified, append this list of
        additional paths to search for cache dirs.
    :param bool delete_cache: If True, delete cache files after reading.
    :param float cache_scan_interval: Interval (in seconds) to scan the caches.
    :param int upload_workers: The number of upload worker processes to spawn.
    """

    global UPLOAD_QUEUE

    # Use the cache detector (OS-dependent) to find EVE installations.
    cache_dirs = CacheDetector().autodetect_caches(additional_eve_dirs=additional_eve_dirs)
    if not cache_dirs:
        logger.error(" ! No cache directories found, exiting.")
        sys.exit(1)

    # Spawn a process that will monitor all of the EVE installation cache
    # directories for file modification.
    cache_worker_process = Process(
        target=cache_processor_worker,
        args=(cache_dirs, UPLOAD_QUEUE, delete_cache, cache_scan_interval)
    )
    cache_worker_process.start()

    # Another process handles uploading the encoded JSON to EMDR.
    for proc in range(upload_workers):
        logger.info("Spawning upload process.")
        uploader_process = Process(target=upload_worker, args=(UPLOAD_QUEUE,))
        uploader_process.start()
