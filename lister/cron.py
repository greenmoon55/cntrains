# app/cron.py

import kronos
import random
import requests
import re

# from lxml import html
from lister.models import Version

@kronos.register('0 0 * * *')
def check_update():
    r = requests.get('http://www.smskb.com/soft/html/12.html')
    page = r.text
    match = re.search("http://www.smskb.com/down/\S+rar", page)
    addr = match.group(0)
    filename = re.search("down/(\S+rar)", addr).group(1)
    r = requests.get(addr)
    with open(filename, 'wb') as fd:
        fd.write(r.content)

    complaints = [
        "I forgot to migrate our applications's cron jobs to our new server! Darn!",
        "I'm out of complaints! Damnit!"
    ]

    print random.choice(complaints)
