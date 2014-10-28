import re;
import requests;

def get(addr, content_type=None):
    r = requests.get(addr, verify=False)
    if content_type == 'json':
        return r.json()
    else:
        return r.text

def get_station_name():
    raw_data = get('https://kyfw.12306.cn/otn/resources/js/framework/station_name.js')
    match = re.search('\'(.*)\'', raw_data)
    content = match.group(1)
    stations = content.split('@')

def query_station(from_station, to_station, date=None):
    url = 'https://kyfw.12306.cn/otn/lcxxcx/query?purpose_codes=ADULT&queryDate=2014-11-01&from_station=%s&to_station=%s' % (from_station, to_station)
    raw_data = get(url, 'json')
    data = raw_data["data"]["datas"]
    return data

def query_by_train_no(train_no, from_station_telecode, to_station_telecode, date=None):
    url = 'https://kyfw.12306.cn/otn/czxx/queryByTrainNo?train_no=%s&from_station_telecode=%s&to_station_telecode=%s&depart_date=2014-11-01' % (train_no, from_station_telecode, to_station_telecode)
    raw_data = get(url, 'json')
    data = raw_data["data"]["data"]
    return data

if __name__ == "__main__":
    trains = query_station('JLL', 'BJP')
    train = trains[0]
    detail = query_by_train_no(train['train_no'], train['start_station_telecode'], train['end_station_telecode'])
    for item in detail[1:-1]:
        print item['station_name']
