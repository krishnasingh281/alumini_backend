FROM python:3.9-alpine3.13
LABEL maintainer="alumini.com"

ENV PYTHONUNBUFFERED=1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./app /app
WORKDIR /app
EXPOSE 8000

ARG DEV=false
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache mysql-client mariadb-connector-c-dev && \
    apk add --update --no-cache --virtual .tmp-build-deps \
        build-base mariadb-dev musl-dev && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ "$DEV" = "true" ]; then \
        /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    rm -rf /tmp && \
    apk del .tmp-build-deps && \
    # Install bash and make it available to all users
    apk add --no-cache bash && \
    chmod +x /bin/bash && \
    # Add non-root user
    adduser \
        --disabled-password \
        --no-create-home \
        django-user

ENV PATH="/py/bin:$PATH"

USER django-user

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]