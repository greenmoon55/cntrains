from django.views import generic

import datetime
import jsonpickle
import logging
import os
import redis

logger = logging.getLogger(__name__)


class IndexView(generic.ListView):
    template_name = 'lister/index.html'
    context_object_name = 'version_list'

    def _get_redis(self):
        password = os.environ.get('REDIS_PASSWORD', None)
        if password:
            r = redis.StrictRedis(host=os.environ['REDIS_PORT_6379_TCP_ADDR'],
                                  port=os.environ['REDIS_PORT_6379_TCP_PORT'],
                                  db=0,
                                  password=password)
        else:
            r = redis.StrictRedis(host=os.environ['REDIS_PORT_6379_TCP_ADDR'],
                                  port=os.environ['REDIS_PORT_6379_TCP_PORT'],
                                  db=0)
        return r

    def get_queryset(self):
        logger.info('list_files')

        r = self._get_redis()
        files = r.get('files')
        if files:
            files = jsonpickle.decode(files)

            for f in files:
                f['uploadTime'] = datetime.datetime.fromtimestamp(
                    f['putTime'] / 1e7)
            files = sorted(files, key=lambda f: f['uploadTime'], reverse=True)

        return files
