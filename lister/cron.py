import hashlib
import kronos
import random
import requests
import re
import datetime

from django.conf import settings
from django.utils import timezone
from qn import qnutils

@kronos.register('15 * * * *')
def check_update():
    r = requests.get('http://www.smskb.com/soft/html/12.html')
    page = r.text
    match = re.search("http://www.smskb.com/down/\S+rar", page)
    addr = match.group(0)
    filename = re.search("down/(\S+rar)", addr).group(1)
    date_str = re.search("\d+", filename).group(0)
    date = datetime.datetime.strptime(date_str, '%Y%m%d')

    r = requests.get(addr)
    if not qnutils.stat('cntrains', filename):
        qnutils.upload(filename, r.content)
    qnutils.list_all(cache=True)
