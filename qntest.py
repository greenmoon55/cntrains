import qiniu.conf
import qiniu.rs
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


ret, err = qiniu.io.put_file(uptoken, 'test', 'qiniu.txt')
if err is not None:
    sys.stderr.write('error: %s ' % err)
print ret
