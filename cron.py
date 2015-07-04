import logging
import qiniu.conf
import re
import requests
import sys

from oslo_config import cfg

from qn import qnutils

logger = logging.getLogger(__name__)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
logger.addHandler(ch)

opts = [
    cfg.StrOpt('access_key', required=True, secret=True),
    cfg.StrOpt('secret_key', required=True, secret=True),
]

CONF = cfg.CONF
CONF.register_cli_opts(opts)
qiniu.conf.UP_HOST = "up.qiniug.com"


def _check_update():
    logger.info('check_update')
    r = requests.get('http://www.smskb.com/soft/html/12.html')
    logger.info('get page from smskb.com')
    page = r.text
    match = re.search("http://www.smskb.com/down/\S+rar", page)
    addr = match.group(0)
    filename = re.search("down/(\S+rar)", addr).group(1)

    r = requests.get(addr)
    logger.info('qnutils.stat')
    if not qnutils.stat('cntrains', filename):
        logger.info('qnutils.upload')
        qnutils.upload(filename, r.content)
        logger.info('uploaded')
    qnutils.list_all()
    logger.info('check_update finished')


def main(argv):
    cfg.CONF(argv[1:])
    qiniu.conf.ACCESS_KEY = cfg.CONF.access_key
    qiniu.conf.SECRET_KEY = cfg.CONF.secret_key
    _check_update()


if __name__ == "__main__":
    main(sys.argv)
