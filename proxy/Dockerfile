FROM nginxinc/nginx-unprivileged:1.25.2-alpine
LABEL maintainer="alumini.com"

COPY ./default.conf.tpl /etc/nginx/default.conf.tpl
COPY ./uwsgi_params /etc/nginx/uwsgi_params
COPY ./run.sh /run.sh

ENV LISTEN_PORT=8000
ENV APP_HOST=app
ENV APP_PORT=9000

USER root

RUN apk add --no-cache dos2unix && \
    mkdir -p /vol/static && \
    chmod 755 /vol/static && \
    touch /etc/nginx/conf.d/default.conf && \
    chown nginx:nginx /etc/nginx/conf.d/default.conf && \
    dos2unix /run.sh && \
    chmod +x /run.sh

VOLUME /vol/static

USER nginx

CMD ["sh", "/run.sh"]