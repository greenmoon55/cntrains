from django.views import generic

import datetime
import jsonpickle
import logging
import os
import qn.qnutils
import redis

logger = logging.getLogger(__name__)

class IndexView(generic.ListView):
    template_name = 'lister/index.html'
    context_object_name = 'version_list'

    def list_files(self):
        logger.info('list_files')

        r = redis.StrictRedis(host=os.environ['REDIS_PORT_6379_TCP_ADDR'], port=os.environ['REDIS_PORT_6379_TCP_PORT'], db=0)
        files_redis = r.get('files')
        if files_redis:
            files = jsonpickle.decode(files_redis)
        else:
            files = qn.qnutils.list_all(cache=True)

        for f in files:
            f['uploadTime'] = datetime.datetime.fromtimestamp(f['putTime'] / 1e7)

        return files

    def get_queryset(self):
        return self.list_files()
