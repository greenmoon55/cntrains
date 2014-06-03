# app/cron.py

import kronos
import random
import requests

from lister.models import Version

@kronos.register('0 0 * * *')
def check_update():
    r = requests.get('http://www.smskb.com/soft/html/12.html')

    complaints = [
        "I forgot to migrate our applications's cron jobs to our new server! Darn!",
        "I'm out of complaints! Damnit!"
    ]

    print random.choice(complaints)
