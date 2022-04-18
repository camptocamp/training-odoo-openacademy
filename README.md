[![Build Status](https://travis-ci.com/camptocamp/demo_odoo.svg?token=3A3ZhwttEcmdqp7JzQb7&branch=14.0-training)](https://travis-ci.com/camptocamp/demo_odoo)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

# demo Odoo

This project uses Docker.

To get a working instance, initialize the required submodules:

  $ git submodule add -b 14.0 git@github.com:OCA/OCB.git ./odoo/src
  $ git submodule add -b 14.0 git@github.com:OCA/server-env.git ./odoo/external-src/server-env
  $ git submodule add -b 14.0 git@github.com:OCA/server-ux.git ./odoo/external-src/server-ux
  $ git submodule add -b 14.0 git@github.com:OCA/web.git ./odoo/external-src/web

When a container starts, the database is automatically created and the
migration scripts automatically run.

## Project maintenance

Please keep this project up-to-date by:

* ensure the `FROM` image in `odoo/Dockerfile` is the latest release
* run regularly `invoke project.sync` to retrieve the last template's changes

## Links

* [General documentation](./docs/README.md)
* [Local documentation](./docs/README.local.md)
* [Changelog](HISTORY.rst).
* [Minions](https://demo.odoo-test.camptocamp.ch)
* [Base image documentation](https://github.com/camptocamp/docker-odoo-project)
