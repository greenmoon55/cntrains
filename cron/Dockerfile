FROM greenmoon55/pip:latest
MAINTAINER greenmoon55

ADD . /src
RUN cd /src; pip install -r requirements.txt -i https://pypi.mirrors.ustc.edu.cn/simple/

ENV ACCESS_KEY access_key
ENV SECRET_KEY secret_key

ADD cron /etc/cron.d/cntrains

RUN chmod 0644 /etc/cron.d/cntrains

RUN touch /var/log/cron.log

# To run on Daocloud...
EXPOSE 55

CMD env > /root/env.txt && cron && tail -f /var/log/cron.log
