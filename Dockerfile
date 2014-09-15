FROM greenmoon55/django:20140803


ADD requirements.txt /src/requirements.txt
RUN cd /src; pip install -r requirements.txt


ADD . /src
ADD secrets /src

RUN cd /src; python manage.py installtasks
RUN apt-get install cron -y

EXPOSE 80
CMD ["/bin/bash", "/src/docker/startup.sh"]
#CMD ["python", "/src/manage.py", "runserver", "0.0.0.0:80"]

#sudo docker run -d -p 80:80  9f1923
