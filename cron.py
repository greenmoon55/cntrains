import logging
import re
import requests
import sys

from oslo_config import cfg

from qn import qnutils

logger = logging.getLogger(__name__)


def check_update():
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
    check_update()


if __name__ == "__main__":
    main(sys.argv)
