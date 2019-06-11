FROM alpine:3.9
MAINTAINER FAN VINGA<fanalcest@gmail.com>

ADD . /app
WORKDIR /app
EXPOSE 80

RUN apk add --no-cache py3-pip py3-gevent libmagic  && \
    pip3 install --upgrade --no-cache-dir pip       && \
    pip3 install --no-cache-dir -r requirements.txt && \
    mkdir -p uploads && python3 init.py 

CMD gunicorn  --reload -c gunicorn.conf index:app;