import datetime
from emds.data_structures import MarketOrderList, MarketOrder
from emds.formats.unified import encode_to_json
from emdu.rev_compat import blue

ORDER_GENERATOR = {
    "name": "EMDU", "key": "git"
}
UPLOAD_KEYS = [{
    "name": "EMDU", "key": "sexytime",
}]

def wintime_to_datetime(timestamp):
    return datetime.datetime.utcfromtimestamp((timestamp-116444736000000000)/10000000)

def serialize_orders(obj):
    order_list = MarketOrderList(
        order_generator=ORDER_GENERATOR,
        upload_keys=UPLOAD_KEYS,
    )
    generated_at = datetime.datetime.now()

    for history_item in obj['lret']:
        for entry in history_item:
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

    if len(order_list) > 0:
        return encode_to_json(order_list)
    else:
        return None

def serialize_cache_file(cache_file_path):
    fobj = open(cache_file_path, 'r')
    key, obj = blue.marshal.Load(fobj.read())

    print key[1]
    if key[1] == 'GetOrders':
        json_str = serialize_orders(obj)
        fobj.close()
        return json_str
