from reverence import blue

fobj = open('/Users/gtaylor/Library/Application Support/EVE Online/p_drive/Local Settings/Application Data/CCP/EVE/c_program_files_ccp_eve_tranquility/cache/MachoNet/87.237.38.200/330/CachedMethodCalls/2df4.cache', 'r').read()
key, obj = blue.marshal.Load(fobj)

if key[1]=="GetOrders":
    print key
    item = key[3]
    region = key[2]

    print "Processing %s [%s]... \n" % (item, region)
    print obj
    for history_item in obj['lret']:
        for entry in history_item:
            print {'OrderID': entry['orderID'],
                    'TypeID': entry['typeID'],
                    'VolEnt': entry['volEntered'],
                    'VolRem': entry['volRemaining'],
                    'Price': entry['price'],
                    'MinVolume': entry['minVolume'],
                    'Duration': entry['duration'],
                    'StationID': entry['stationID'],
                    'Range': entry['range'],
                    'Jumps': entry['jumps']}