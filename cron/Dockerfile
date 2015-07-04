FROM greenmoon55/pip:latest
MAINTAINER greenmoon55

ADD . /src
RUN cd /src; pip install -r requirements.txt -i https://pypi.mirrors.ustc.edu.cn/simple/

ENV ACCESS_KEY access_key
ENV SECRET_KEY secret_key

RUN touch /etc/cron.d/cntrains

RUN chmod 0644 /etc/cron.d/cntrains

RUN touch /var/log/cron.log

CMD echo "* * * * * root python /src/main.py --access_key=$ACCESS_KEY --secret_key=$SECRET_KEY >> /var/log/cron.log 2>&1" >> /etc/cron.d/cntrains; cron && tail -f /var/log/cron.log
