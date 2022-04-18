<!--
This file has been generated with 'invoke project.sync'.
Do not modify. Any manual change will be lost.
Please propose your modification on
https://github.com/camptocamp/odoo-template instead.
-->
# How to run a test server, the short way

This method is mostly for project managers or functional testers because it uses the pre-generated Docker images. Developers will prefer to use [Docker in development mode](docker-dev.md).

## Pre-requisite

Be sure to [install Docker and docker-compose](prerequisite.md) before going any further.

## Steps

1. Clone the project

        git clone git@github.com:camptocamp/demo_odoo.git demo

2. Login to Github Packages (create an token on your [github account](https://docs.github.com/en/free-pro-team@latest/github/authenticating-to-github/creating-a-personal-access-token) 
        
        export CR_PAT=<YourToken>
        echo $CR_PAT | docker login ghcr.io -u $USER --password-stdin

3. Start the composition

        cd demo
        docker-compose -f test.yml pull
        docker-compose -f test.yml up

4. Open a browser on http://localhost (only one odoo instance at a time can be
   started because it uses the port 80, this can be changed in the
   configuration file if needed)

4. In `test.yml` you might want to adapt the odoo `image` version (so replace `latest` by a specific tag or branch).

5. If you want to drop your database, run:

        docker-compose -f test.yml run --rm odoo dropdb odoodb
