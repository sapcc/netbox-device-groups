FROM python:3.10-alpine

ENV POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_CREATE=0 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VERSION=1.3.1

ENV PATH="$POETRY_HOME/bin:$PATH"

RUN apk --update --no-progress --no-cache upgrade && \
    apk add --no-cache --virtual .build-deps \
        curl \
        musl-dev \
        openldap-dev \
        freetype-dev
RUN apk --update --no-progress add git zsh postgresql-client
# Copy in the source code ans install poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
WORKDIR /app
COPY . /app/

RUN poetry config virtualenvs.create false
# install the dependencies
RUN poetry install --no-interaction --no-ansi


# Install NetBox
RUN mkdir -p /opt/netbox \
    && git clone --depth 1 --branch=v3.5.9 https://github.com/netbox-community/netbox.git /opt/netbox/
COPY development/sap_netbox_dev.svg /opt/netbox/netbox/project-static/img/netbox_logo.svg
# Now clean up the image by remving the gcc/package build dependencies
RUN apk del .build-deps


# Get the development instance of NetBox up and running
COPY development/configuration.py /opt/netbox/netbox/netbox/configuration.py
COPY development/entrypoint.sh /opt/entrypoint.sh
RUN ["chmod", "+x", "/opt/entrypoint.sh"]
ENTRYPOINT ["/opt/entrypoint.sh"]