"""
This module contains a simple function to upload an encoded JSON message
to EMDR.
"""

import requests
import zlib

# The headers that we'll send.
UPLOAD_HEADERS = {
    "Content-Encoding": "deflate",
    "User-Agent": "EMDU/git",
}

def upload_message(json_str, scan_endpoint):
    """
    Given an encoded JSON message, upload it to EMDR.

    :param json_str: The encoded order or history message to upload.
    :param string: URL to send the result to.
    """

    # Compressed request
    data = zlib.compress(json_str)

    r = requests.post(
        scan_endpoint,
        data=data,
        headers=UPLOAD_HEADERS,
    )
