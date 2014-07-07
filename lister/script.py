import requests
import re
import datetime
import time

def download():
    day = datetime.timedelta(days=1)
    date = datetime.datetime(2013, 11, 3)
    while True:
        time.sleep(5)
        date = date - day
        date_str = date.strftime('%Y%m%d')
        link = "http://www.smskb.com/down/smsk%s.rar" % date_str
        print link
        r = requests.get(link)
        if r.status_code == 200:
            print "file found"
            local_file = '/home/greenmoon55/static/smsk%s.rar' % date_str
            with open(local_file, 'wb') as fd:
                fd.write(r.content)

if __name__=="__main__":
    download()
