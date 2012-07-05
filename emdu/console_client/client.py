"""
Very simple console-based uploader client.
"""

import sys
import time
import logging
from multiprocessing import Process, Queue
from emdu.cache_detector import CacheDetector
from emdu.cache_watcher.crude_watcher import CrudeCacheWatcher
from emdu.cachefile_serializer import serialize_cache_file
from emdu.console_client import settings
from emdu.message_uploader import upload_message

logger = logging.getLogger(__name__)
# Any entries in this queue are encoded JSON messages, ready for
# sending to EMDR.
UPLOAD_QUEUE = Queue()

def cache_processor_worker(cache_dirs, upload_queue):
    """
    This is ran as a process. This function checks all detected EVE installation
    cache dirs for modified files. If files of interest are found, their
    contents are serialized and shoved into the upload queue for sending to
    EMDR.

    :param list cache_dirs: A list of cache dir paths to monitor for changes.
    :param multiprocessing.Queue upload_queue: A queue that holds encoded JSON
        messages that are ready to be sent to EMDR.
    """

    # Holds all of the cache watchers we'll need to scan for updates on each
    # detected EVE install.
    cache_watchers = []
    for cache_dir in cache_dirs:
        # Each EVE installation has a cache watcher to monitor it.
        logger.info("Setting up monitor on %s" % cache_dir)
        cache_watchers.append(CrudeCacheWatcher(cache_dir))


    while True:
        # This value should never go below two seconds, and should probably
        # stay above three. This keeps filesystem mtime debauchery to a minimum.
        time.sleep(settings.CACHE_SCAN_INTERVAL)

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
                    logger.debug("Adding message to the queue for upload.")
                    upload_queue.put(message_json)

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
        upload_message(message_json)

def run(additional_eve_dirs=None):
    """
    Fires up the various processes that comprise the client. For each EVE
    install,

    :keyword list additional_eve_dirs: If speficied, append this list of
        additional paths to search for cache dirs.
    """

    global UPLOAD_QUEUE

    # Use the cache detector (OS-dependent) to find EVE installations.
    cache_dirs = CacheDetector().autodetect_caches(additional_eve_dirs=additional_eve_dirs)
    if not cache_dirs:
        logger.error(" ! No cache directories found, exiting.")
        sys.exit(1)

    logger.info("Watching EVE cache dirs:")
    for cache_dir in cache_dirs:
        logger.info(" * %s" % cache_dir)

    # Spawn a process that will monitor all of the EVE installation cache
    # directories for file modification.
    cache_worker_process = Process(
        target=cache_processor_worker,
        args=(cache_dirs, UPLOAD_QUEUE)
    )
    cache_worker_process.start()

    # Another process handles uploading the encoded JSON to EMDR.
    uploader_process = Process(target=upload_worker, args=(UPLOAD_QUEUE,))
    uploader_process.start()
