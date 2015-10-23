# Training Odoo OpenAcademy

Based on https://www.odoo.com/documentation/8.0/howtos/backend.html

## Prerequisite

Install dependencies (debian/ubuntu):

    sudo apt-get install libxml2-dev libxslt1-dev python-dev \
      libpq-dev libjpeg-dev zlib1g-dev libsasl2-dev \
      libldap2-dev postgresql

## Installation:

Steps:

1. Clone the github repository

        git clone git@github.com:camptocamp/training-odoo-openacademy.git

1. Go in the folder and bootstrap

        ./bootstrap.sh

1. Build

        bin/buildout

## Start Odoo:

For development:

    $ bin/start_openerp -d <db_name> 

Run the tests:

    $ bin/test_openerp -d <db_name> -u <module_to_test>

Start as a service:

    $ bin/supervisord
