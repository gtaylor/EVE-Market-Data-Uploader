import requests
import zlib

UPLOAD_HEADERS = {
    'Content-Encoding': 'deflate'
}

def upload_message(json_str):

    # Compressed request
    data = zlib.compress(json_str)

    r = requests.post(
        'http://secondary.eve-emdr.com/upload/',
        data=data,
        headers=UPLOAD_HEADERS,
    )
    print r.status_code, r.text