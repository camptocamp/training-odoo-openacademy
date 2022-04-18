FROM ghcr.io/camptocamp/odoo-project:14.0-4.4.3
LABEL maintainer="Camptocamp"

# Steps are grouped by dependency
# and ordered by compromizing cost and frequency

## Base requirements (Libs and packages)
# frequency: rarely
# cost:      high

COPY ./*requirements.txt /odoo/
# Install additional debian and python packages if needed
RUN set -x; \
        apt-get update \
        && apt-get install -y --no-install-recommends \
        parallel libmagic1 \
        # if you need some dev packages for python packages, you need to clean them afterwards
        python3-dev build-essential \
        && cd /odoo \
        && find . -maxdepth 1 -name "*requirements.txt" ! -name src_requirements.txt ! -name base_requirements.txt | xargs -I{} pip install -r {} \
        # cleaning of dev packages
        && apt-get remove -y build-essential python3-dev \
        # && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false -o APT::AutoRemove::SuggestsImportant=false \
        && apt-get clean \
        && rm -rf /var/lib/apt/lists/*


## Tools of odoo-template
# frequency: seldom
# cost:      light

# Entrypoints
COPY ./before-migrate-entrypoint.d/* /before-migrate-entrypoint.d/
COPY ./start-entrypoint.d/* /start-entrypoint.d/
RUN chmod +x /before-migrate-entrypoint.d/* \
    && chmod +x /start-entrypoint.d/*
# CSV Loader
# `parallel` + `importer.sh` are needed to load heavy files
COPY ./bin/importer.sh /odoo-bin/

## Prepare pip install
# frequency: never
# cost     : very light
COPY ./setup.py /odoo/

## Main activity
# frequency: always
# costs:     very high to very light
COPY ./src /odoo/src
COPY ./external-src /odoo/external-src
COPY ./local-src /odoo/local-src
COPY ./data /odoo/data
COPY ./songs /odoo/songs
COPY ./VERSION /odoo/
COPY ./migration.yml /odoo/

# depends on ./setup.py ./src, ./songs and ./VERSION
RUN cd /odoo && pip install -r src_requirements.txt


## PLATFORM: Add this line to ADDONS_PATH if hosting is on cloud platform
# /odoo/external-src/odoo-cloud-platform, \

## Environment
# frequency: sometimes
# cost:      very light
ENV ADDONS_PATH="/odoo/src/addons, \
  /odoo/external-src/server-env, \
  /odoo/external-src/server-ux, \
  /odoo/external-src/web, \
  /odoo/local-src" \
  LIMIT_TIME_CPU=86400 \
  LIMIT_TIME_REAL=86400 \
  LIMIT_MEMORY_SOFT=1342177280 \
  LIMIT_MEMORY_HARD=1610612736 \
  ODOO_DATA_PATH=/odoo/data
