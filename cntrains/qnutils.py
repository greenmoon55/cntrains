import qiniu.conf
import qiniu.rs
import qiniu.rsf
import qiniu.io
import sys

import qnconfig

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
uptoken = policy.token()


def upload(key, data):
    ret, err = qiniu.io.put(uptoken, key, data)
    if err is not None:
        sys.stderr.write('error: %s ' % err)
    else:
        return -1
    print ret

def list_all(bucket_name, rs=None, prefix=None, limit=None):
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
    return files

print list_all('cntrains')

#with open('test.txt', 'r') as fd:
#    upload('test2', fd.read())

