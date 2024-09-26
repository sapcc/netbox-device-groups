# -------------------------------------------------------------------------------------
# Netbox Plugin Developement Dockerfile Template
# Version: 1.0.0
#
# Plugins that need to add additional steps or packages can do in the section below.
# -------------------------------------------------------------------------------------
# !!! USE CAUTION WHEN MODIFYING LINES BELOW

# Accepts a desired Python version as build argument, default to 3.9
ARG PYTHON_VER="3.9"

FROM python:${PYTHON_VER}-alpine

RUN apk --update --no-progress --no-cache upgrade && \
    apk add --no-cache --virtual .build-deps \
        curl \
        musl-dev \
        openldap-dev \
        freetype-dev
RUN apk --update --no-progress add git zsh postgresql-client

# Install NetBox
# Accepts a desired Netbox version as build argument, default to 3.5.8
ARG NETBOX_VER="3.5.8"
ARG NETBOX_ROOT=/opt/netbox
RUN mkdir -p ${NETBOX_ROOT}
RUN git clone --depth 1 --branch=v${NETBOX_VER} https://github.com/netbox-community/netbox.git ${NETBOX_ROOT}

# Copy in the source code
WORKDIR /app
COPY . /app/
# And install poetry
ARG POETRY_VER="1.7.1"

ENV POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_CREATE=0 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VERSION=${POETRY_VER}
ENV PATH="$POETRY_HOME/bin:$PATH"
RUN curl -sSL https://install.python-poetry.org | python3 -
# install the dependencies
RUN poetry install --no-interaction --no-ansi

# Now clean up the image by removing the gcc/package build dependencies
RUN apk del .build-deps

# Get the development instance of NetBox up and running
COPY development/configuration.py ${NETBOX_ROOT}/netbox/netbox/configuration.py
COPY development/entrypoint.sh /opt/entrypoint.sh
RUN ["chmod", "+x", "/opt/entrypoint.sh"]
ENTRYPOINT ["/opt/entrypoint.sh"]