from django.core.management.base import BaseCommand, CommandError
from lister.models import Version
from os import listdir
import datetime
import re
import hashlib
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

class Command(BaseCommand):
    help = 'update db'

    def handle(self, *args, **options):
        file_dir = '/home/greenmoon55/static/'
        files = listdir(file_dir)
        for f in files:
            date_str = re.search("\d+", f).group(0)
            date = datetime.datetime.strptime(date_str, '%Y%m%d')
            try:
                record = Version.objects.get(release_date=date)
            except ObjectDoesNotExist:
                f_content = ''
                with open(file_dir + f, 'r') as fd:
                    f_content = fd.read()
                m = hashlib.md5()
                m.update(f_content)
                Version.objects.create(release_date=date, update_date=timezone.now(), link=f, md5_hash=m.hexdigest())
