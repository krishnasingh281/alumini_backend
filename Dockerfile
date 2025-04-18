FROM python:3.9-alpine3.18
LABEL maintainer="alumini.com"

ENV PYTHONUNBUFFERED=1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./scripts /scripts
COPY ./app /app
WORKDIR /app
EXPOSE 8000

ARG DEV=false
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache mysql-client mariadb-connector-c && \
    apk add --update --no-cache --virtual .tmp-build-deps \
        build-base mariadb-dev musl-dev linux-headers && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ "$DEV" = "true" ]; then \
        /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    rm -rf /tmp && \
    apk del .tmp-build-deps && \
    # Install bash
    apk add --no-cache bash && \
    # Add non-root user
    adduser \
        --disabled-password \
        --no-create-home \
        django-user && \
    chmod -R +x /scripts

ENV PATH="/scripts:/py/bin:$PATH"

RUN mkdir -p /vol/web/static && \
    mkdir -p /vol/web/media && \
    chmod -R 755 /vol/web && \
    chown -R django-user:django-user /vol/web

USER django-user

CMD ["run.sh"]