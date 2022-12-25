FROM python:3.10-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install nginx
RUN apt-get update \
    && apt-get install vim nano telnet nginx bash -y --no-install-recommends \
    && apt-get clean autoclean \
    && apt-get autoremove --yes \
    && rm -rf /var/lib/{apt,dpkg}

RUN groupadd -g 1001 -o sites_crawler \
    && useradd -m -u 1000 -g 1001 -o -s /bin/bash sites_crawler \
    && adduser sites_crawler www-data \
    && adduser www-data sites_crawler

COPY etc/nginx.conf /etc/nginx/sites-available/default
RUN ln -sf /dev/stdout /var/log/nginx/access.log && ln -sf /dev/stderr /var/log/nginx/error.log

# copy source and install dependencies
RUN mkdir -p /opt/app \
    && mkdir -p /opt/app/pip_cache \
    && mkdir -p /opt/app/sites_crawler

COPY etc/gunicorn.conf.py requirements.txt start-server.sh /opt/app/
COPY manage.py /opt/app/manage.py
COPY sites_crawler /opt/app/sites_crawler/
COPY public/media/ /opt/app/public/media/

WORKDIR /opt/app
RUN pip install -r requirements.txt --cache-dir /opt/app/pip_cache  \
    && chown -R www-data:www-data /opt/app

# port where the Django app runs
EXPOSE 8000
# start server
CMD python manage.py runserver


