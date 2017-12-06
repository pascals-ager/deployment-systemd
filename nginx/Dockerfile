FROM nginx:1.12
MAINTAINER Advith Nagappa <advith.nagappa@gmail.com>

RUN rm /usr/share/nginx/html/*

COPY configs/nginx.conf /etc/nginx/nginx.conf
COPY configs/default.conf /etc/nginx/conf.d/default.conf

COPY certs/python-flask-nginx-example.crt /etc/ssl/certs/python-flask-nginx-example.crt
COPY certs/python-flask-nginx-example.key /etc/ssl/private/python-flask-nginx-example.key
COPY certs/dhparam.pem /etc/ssl/private/dhparam.pem

COPY docker-entrypoint /
RUN chmod +x /docker-entrypoint
ENTRYPOINT ["/docker-entrypoint"]

CMD ["nginx", "-g", "daemon off;"]
