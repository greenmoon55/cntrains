# app/cron.py

import hashlib
import kronos
import random
import requests
import re
import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from lister.models import Version

@kronos.register('0 0 * * *')
def check_update():
    r = requests.get('http://www.smskb.com/soft/html/12.html')
    page = r.text
    match = re.search("http://www.smskb.com/down/\S+rar", page)
    addr = match.group(0)
    filename = re.search("down/(\S+rar)", addr).group(1)
    date_str = re.search("\d+", filename).group(0)
    date = datetime.datetime.strptime(date_str, '%Y%m%d')

    r = requests.get(addr)
    try:
        record = Version.objects.get(release_date=date)
    except ObjectDoesNotExist:
        with open(filename, 'wb') as fd:
            fd.write(r.content)
        m = hashlib.md5()
        m.update(r.content)
        Version.objects.create(release_date=date, update_date=timezone.now(), link=filename, md5_hash=m.hexdigest())


    complaints = [
        "I forgot to migrate our applications's cron jobs to our new server! Darn!",
        "I'm out of complaints! Damnit!"
    ]

    print random.choice(complaints)
