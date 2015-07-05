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
        r = redis.StrictRedis(host=os.environ['REDIS_PORT_6379_TCP_ADDR'],
                              port=os.environ['REDIS_PORT_6379_TCP_PORT'],
                              db=0,
                              password=os.environ['REDIS_PASSWORD'])
        return r

    def _list_files(self):
        logger.info('list_files')

        r = self._get_redis()
        files = r.get('files')
        if files:
            files = jsonpickle.decode(files)

            for f in files:
                f['uploadTime'] = datetime.datetime.fromtimestamp(
                    f['putTime'] / 1e7)

        return files

    def get_queryset(self):
        return self._list_files()
