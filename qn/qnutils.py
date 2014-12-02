import jsonpickle
import logging
import qiniu.conf
import qiniu.resumable_io as rio
import qiniu.rs
import qiniu.rsf
import qiniu.io
import os
import redis
import StringIO
import sys

import qnconfig

from datetime import datetime

logger = logging.getLogger(__name__)

class PutPolicy(object):
    scope = None
    expires = 3600
    callbackUrl = None
    callbackBody = None
    returnUrl = None
    returnBody = None
    endUser = None
    asyncOps = None

    def __init__(self, scope):
        self.scope = scope

policy = qiniu.rs.PutPolicy('cntrains')


def upload(key, data):
    uptoken = policy.token()
    extra = rio.PutExtra('cntrains')
    try:
        ret, err = rio.put(uptoken, key, StringIO.StringIO(data), len(data), extra)
        if err is not None:
            logger.warn('upload error: %s ' % err)
    except:
        logger.exception('')

def list_all(bucket_name='cntrains', rs=None, prefix=None, limit=None):
    logger.info('list_all started')
    if rs is None:
        rs = qiniu.rsf.Client()
    marker = None
    err = None
    files = []
    while err is None:
        ret, err = rs.list_prefix(bucket_name, prefix=prefix, limit=limit, marker=marker)
        marker = ret.get('marker', None)
        files += ret['items']
    if err is not qiniu.rsf.EOF:
        pass
    logger.info('got files from qiniu')
    logger.info('connect to redis')
    try:
        r = redis.StrictRedis(host=os.environ['REDIS_PORT_6379_TCP_ADDR'], port=os.environ['REDIS_PORT_6379_TCP_PORT'], db=0)
        r.set('files', jsonpickle.encode(files))
        r.set('files_updated_at', str(datetime.now()))
        logger.info('update to redis')
    except Exception, e:
        logger.info(e)
    return files

def stat(bucket_name, key):
    ret, err = qiniu.rs.Client().stat(bucket_name, key)
    if err is not None:
        sys.stderr.write('error: %s ' % err)
        return
    print ret,
    return ret
