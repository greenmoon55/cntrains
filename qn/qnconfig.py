import qiniu.conf

from oslo_config import cfg

opts = [
    cfg.StrOpt('access_key', required=True, secret=True),
    cfg.StrOpt('secret_key', required=True, secret=True),
]

CONF = cfg.CONF
CONF.register_cli_opts(opts)

qiniu.conf.ACCESS_KEY = CONF.access_key
qiniu.conf.SECRET_KEY = CONF.secret_key
qiniu.conf.UP_HOST = "up.qiniug.com"
