FROM greenmoon55/django:20140803


ADD requirements.txt /src/requirements.txt
RUN cd /src; pip install -r requirements.txt

ADD . /src

EXPOSE 80
CMD ["python", "/src/manage.py", "runserver", "0.0.0.0:80"]


