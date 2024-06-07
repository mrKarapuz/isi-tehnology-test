FROM nginx

RUN mkdir /app

ENV TZ=UTC
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

ADD ./config/ssl/cert.pem /etc/ssl/
ADD ./config/ssl/key.pem /etc/ssl/
ADD ./config/nginx/uwsgi_params /etc/nginx/
ADD ./config/nginx/django.conf /etc/nginx/conf.d/default.conf
