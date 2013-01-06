"""
This module reads the cache files and serializes them into a Unified Uploader
format message.
"""

import datetime
from reverence.blue import marshal
from emds.data_structures import MarketOrderList, MarketOrder, MarketHistoryList, MarketHistoryEntry
from emds.formats.unified import encode_to_json
from emds.common_utils import now_dtime_in_utc, enlighten_dtime
from emdu.rev_compat import blue

# Some constants that identify this uploader.
ORDER_GENERATOR = {
    "name": "EMDU", "version": "git"
}
UPLOAD_KEYS = [{
    "name": "EMDU", "version": "sexytime",
}]

def wintime_to_datetime(timestamp):
    """
    Given a funky Windows timestamp, convert it to a UTC datetime object.

    :param int timestamp: The timestamp, in win format.
    :rtype: datetime.datetime
    :returns: The correct UTC-aware timestamp.
    """

    return enlighten_dtime(datetime.datetime.utcfromtimestamp((timestamp-116444736000000000)/10000000))

def serialize_orders(doc_dict, region_data):
    """
    Serializes a GetOrders cache file's contents.

    :param dict doc_dict: The parsed cache document in dict form.
    :rtype: str
    :returns: The UUDIF serialized JSON message.
    """
    order_list = MarketOrderList(
        order_generator=ORDER_GENERATOR,
        upload_keys=UPLOAD_KEYS,
    )
    # timezone-aware datetime.
    generated_at = now_dtime_in_utc()
    region_id = region_data[2]
    type_id = region_data[3]

    for order_item in doc_dict['lret']:
        #print order_item
        for entry in order_item:
            #print entry
            order = MarketOrder(
                order_id=entry['orderID'],
                is_bid=entry['bid'],
                region_id=entry['regionID'],
                solar_system_id=entry['solarSystemID'],
                station_id=entry['stationID'],
                type_id=entry['typeID'],
                price=entry['price'],
                volume_entered=entry['volEntered'],
                volume_remaining=entry['volRemaining'],
                minimum_volume=entry['minVolume'],
                order_issue_date=wintime_to_datetime(entry['issueDate']),
                order_duration=entry['duration'],
                order_range=entry['range'],
                generated_at=generated_at,
            )
            order_list.add_order(order)

    if len(order_list) is 0:
        # There were no orders for this item+region combo.
        order_list.set_empty_region(region_id, type_id, generated_at)

    return encode_to_json(order_list)

def serialize_history(doc_dict, region_data):
    """
    Serializes a GetOldPriceHistory cache file's contents.

    :param dict doc_dict: The parsed cache document in dict form.
    :rtype: str
    :returns: The UUDIF serialized JSON message.
    """
    hist_list = MarketHistoryList(
        order_generator=ORDER_GENERATOR,
        upload_keys=UPLOAD_KEYS,
    )
    # timezone-aware datetime.
    generated_at = now_dtime_in_utc()
    region_id = region_data[2]
    type_id = region_data[3]

    for hist_item in doc_dict['lret']:
        #print hist_item
        entry = MarketHistoryEntry(
            type_id=type_id,
            region_id=region_id,
            historical_date=wintime_to_datetime(hist_item['historyDate']),
            num_orders=hist_item['orders'],
            low_price=hist_item['lowPrice'],
            high_price=hist_item['highPrice'],
            average_price=hist_item['avgPrice'],
            total_quantity=hist_item['volume'],
            generated_at=generated_at,
        )
        hist_list.add_entry(entry)

    if len(hist_list) is 0:
        # There were no orders for this item+region combo.
        hist_list.set_empty_region(region_id, type_id, generated_at)

    return encode_to_json(hist_list)

def serialize_cache_file(cache_file_path):
    """
    Given a cache file, open it and determine whether it's something we can
    upload. If it is, serialize it to JSON, then return the serialized JSON.

    :param str cache_file_path: The full path to a cache file to read and
        potentially serialize.
    :rtype: str or None
    :returns: If the cache file contains something we can upload, return a
        JSON string that will be uploaded to EMDR. Otherwise, return None.
    """

    # Catching missing files between passes, eve can delete cache file
    # before we can read it.
    try:
        fobj = open(cache_file_path, 'rb')
    except (IOError, OSError):
        print "Cache file removed before we got to it"
        return None
    # Parse with either reverence or despair.
    try:
        key, obj = blue.marshal.Load(fobj.read())
    except marshal.UnmarshalError:
        # The file probably wasn't finished writing when EMDU tried to read it.
        return None

    if key[1] == 'GetOrders':
        json_str = serialize_orders(obj, key)
        fobj.close()
        return json_str
    if key[1] == 'GetOldPriceHistory':
        json_str = serialize_history(obj, key)
        fobj.close()
        return json_str

    # This isn't a cache file we can do anything with. Oh bother.
    return None
