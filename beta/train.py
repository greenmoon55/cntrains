import marshal;
import re;
import requests;

train_no_dict = {}

def get(addr, content_type=None):
    r = requests.get(addr, verify=False)
    if content_type == 'json':
        return r.json()
    else:
        return r.text

def get_station_name():
    try:
        with open('stations.txt', 'r') as f:
            stations = marshal.load(f)
            return stations
    except IOError:
        pass
    raw_data = get('https://kyfw.12306.cn/otn/resources/js/framework/station_name.js')
    match = re.search('\'(.*)\'', raw_data)
    content = match.group(1)
    stations = content.split('@')
    with open('stations.txt', 'wb') as f:
        marshal.dump(stations, f)
    return stations

def query_station(from_station, to_station, date=None):
    url = 'https://kyfw.12306.cn/otn/lcxxcx/query?purpose_codes=ADULT&queryDate=2014-11-10&from_station=%s&to_station=%s' % (from_station, to_station)
    raw_data = get(url, 'json')
    data = raw_data["data"]["datas"]
    return data

def query_by_train_no(train_no, from_station_telecode, to_station_telecode, date=None):
    url = 'https://kyfw.12306.cn/otn/czxx/queryByTrainNo?train_no=%s&from_station_telecode=%s&to_station_telecode=%s&depart_date=2014-11-10' % (train_no, from_station_telecode, to_station_telecode)
    raw_data = get(url, 'json')
    data = raw_data["data"]["data"]
    return data

def get_trains_between_two_stations(from_station, to_station, date=None):
    data = query_station(from_station, to_station, date)
    for train in data:
        train_no_dict[train['station_train_code']] = True

if __name__ == "__main__":
#    trains = query_station('JLL', 'BJP')
#    train = trains[0]
#    detail = query_by_train_no(train['train_no'], train['start_station_telecode'], train['end_station_telecode'])
#    for item in detail[1:-1]:
#        print item['station_name']
#    get_trains_between_two_stations('JLL', 'BJP')
    print get_station_name()
    #print train_no_dict
