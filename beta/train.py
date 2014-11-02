import itertools;
from models.station import Station;
from models.train import Train;
import pickle;
import re;
import requests;
import time;

def get(addr, content_type=None):
    r = None
    for i in xrange(10):
        try:
            r = requests.get(addr, timeout=10, verify=False)
        except requests.exceptions.RequestException:
            print 'exception %d' % i
            time.sleep(2**i)
            continue
        break

    if content_type == 'json':
        return r.json()
    else:
        return r.text

def get_all_stations():
    try:
        with open('stations.txt', 'r') as f:
            stations = pickle.load(f)
            return stations
    except IOError:
        pass
    raw_data = get('https://kyfw.12306.cn/otn/resources/js/framework/station_name.js')
    match = re.search('\'(.*)\'', raw_data)
    content = match.group(1)
    raw_stations = content.split('@')
    stations = []
    for station in raw_stations:
        if not station:
            continue
        sta_attrs = station.split('|')
        station_obj = Station(sta_attrs[1], sta_attrs[2], sta_attrs[3])
        stations.append(station_obj)

    with open('stations.txt', 'wb') as f:
        pickle.dump(stations, f)
    return stations

def query_station(from_station, to_station, date=None):
    url = 'https://kyfw.12306.cn/otn/lcxxcx/query?purpose_codes=ADULT&queryDate=2014-11-10&from_station=%s&to_station=%s' % (from_station, to_station)
    raw_data = get(url, 'json')
    trains = []
    if raw_data == -1:
        return trains
    try:
        data = raw_data["data"]["datas"]
    except KeyError:
        return trains
    for train_data in data:
        train_obj = Train(train_data['train_no'], train_data['start_station_name'], train_data['end_station_name'], train_data['start_station_telecode'], train_data['end_station_telecode'])
        trains.append(train_obj)
    return trains

def query_by_train_no(train_no, from_station_telecode, to_station_telecode, date=None):
    url = 'https://kyfw.12306.cn/otn/czxx/queryByTrainNo?train_no=%s&from_station_telecode=%s&to_station_telecode=%s&depart_date=2014-11-10' % (train_no, from_station_telecode, to_station_telecode)
    raw_data = get(url, 'json')
    data = raw_data["data"]["data"]
    return data

def get_trains_between_two_stations(from_station, to_station, date=None):
    data = query_station(from_station, to_station, date)
    for train in data:
        train_no_dict[train['station_train_code']] = True

def get_all_trains(stations):
    train_dict = {}
    for station_from in stations:
        for station_to in stations:
            if station_from == station_to:
                continue
            print station_from.name, station_to.name
            #time.sleep(5)
            trains = query_station(station_from.telecode, station_to.telecode)
            for train in trains:
                train_dict[train.no] = train
            for key in sorted(train_dict):
                train = train_dict[key]
                #print "%s %10s %10s" % (train.no, train.from_station, train.to_station)
            with open('trains.txt', 'wb') as f:
                pickle.dump(train_dict, f)
            

if __name__ == "__main__":
    stations = get_all_stations()
    trains = get_all_trains(stations)
    
#    trains = query_station('JLL', 'BJP')
#    import pdb; pdb.set_trace()
#    train = trains[0]
#    detail = query_by_train_no(train['train_no'], train['start_station_telecode'], train['end_station_telecode'])
#    for item in detail[1:-1]:
#        print item['station_name']
#    get_trains_between_two_stations('JLL', 'BJP')
    #print get_station_name()
    #print train_no_dict
