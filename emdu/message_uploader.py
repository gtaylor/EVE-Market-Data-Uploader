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

def upload_message(json_str):
    """
    Given an encoded JSON message, upload it to EMDR.

    :param json_str: The encoded order or history message to upload.
    """

    # Compressed request
    data = zlib.compress(json_str)

    r = requests.post(
        'http://upload.eve-emdr.com/upload/',
        data=data,
        headers=UPLOAD_HEADERS,
    )