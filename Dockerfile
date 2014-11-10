# Use phusion/baseimage as base image. To make your builds reproducible, make
# sure you lock down to a specific version, not to `latest`!
# See https://github.com/phusion/baseimage-docker/blob/master/Changelog.md for
# a list of version numbers.
FROM phusion/baseimage:0.9.15

# Set correct environment variables.
ENV HOME /root

# Regenerate SSH host keys. baseimage-docker does not contain any, so you
# have to do that yourself. You may also comment out this instruction; the
# init system will auto-generate one during boot.
#RUN /etc/my_init.d/00_regen_ssh_host_keys.sh

# Use baseimage-docker's init system.
CMD ["/sbin/my_init"]

# ...put your own build instructions here...
ADD docker/sources.list /etc/apt/sources.list
RUN apt-get update
RUN apt-get install -y python-pip
ADD requirements.txt /src/requirements.txt
RUN cd /src; pip install -r requirements.txt


ADD . /src
ADD secrets /src

RUN cd /src; python manage.py installtasks

RUN mkdir /etc/service/django
ADD docker/startup.sh /etc/service/django/run
RUN chmod +x /etc/service/django/run

EXPOSE 80

# Clean up APT when done.
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

CMD ["/sbin/my_init"]
