<!--
This file has been generated with 'invoke project.sync'.
Do not modify. Any manual change will be lost.
Please propose your modification on
https://github.com/camptocamp/odoo-template instead.
-->
# Working on the project as developers

## Pre-requisite

Be sure to [install Docker and docker-compose](prerequisites.md) before going any further.

Before starting, be aware of [the documentation of the core
image](https://github.com/camptocamp/docker-odoo-project).

## Starting, git submodules

1. Clone the project

        git clone git@github.com:camptocamp/demo_odoo.git demo

2. Submodules

    To get submodule use:

    ```bash
    invoke submodule.update
    ```

    This will sync the submodules and get them one by one.

    Tip: Install [Git-autoshare](how-to-setup-git-autoshare.md#Installation) to copy from local host instead to reduce download.

## Docker

### Build of the image

In a development environment, building the image is rarely necessary. The
production images are built by Travis. Furthermore, In the development
environment we share the local (source code) folders with the container using
`volumes` so we don't need to `COPY` the files in the container.

Building the image is required when:

* you start to work on the project
* the base image (`camptocamp/odoo-project:14.0`) has been updated and you need
  the new version
* the local Dockerfile has been modified (for example when dependency or addons
  repository is added)

Building the image is a simple command:

```bash
# build the docker image locally (--pull pulls the base images before building the local image)
docker-compose build --pull
```

You could also first pull the base images, then run the build:

```bash
docker-compose pull
docker-compose build
```

### Usage

When you need to launch the services of the composition, you can either run them in foreground or in background.

```bash
docker-compose up
```
Will run the services (postgres, odoo, nginx) in foreground, mixing the logs of all the services.

```bash
docker-compose up -d
```
Will run the services (postgres, odoo, nginx) in background.

When it is running in background, you can show the logs of one service or all of them (mixed):

```bash
docker-compose logs odoo      # show logs of odoo
docker-compose logs postgres  # show logs of postgres
docker-compose logs nginx     # show logs of nginx
docker-compose logs           # show all logs
```

And you can see the details of the running services with:

```bash
docker-compose ps
```

In the default configuration, the Odoo port changes each time the service is
started.  Some prefer to always have the same port, if you are one of them, you
can create your own configuration file or adapt the default one locally.

To know the port of the running Odoo, you can use the command `docker ps` that
shows information about all the running containers or the subcommand `port`:

```bash
docker ps
docker-compose port odoo 8069  # for the service 'odoo', ask the corresponding port for the container's 8069 port
```

This command can be used to open directly a browser which can be nicely aliased (see later).

```bash
export BROWSER="chromium-browser --incognito" # or firefox --private-window
$BROWSER $(docker-compose port odoo 8069)
```

Last but not least, we'll see other means to run Odoo, because `docker-compose
up` is not really good when it comes to real development with inputs and
interactions such as `pdb`.

**docker-compose exec** allows to *enter* in a already running container, which
can be handy to inspect files, check something, ...

```bash
# show odoo configuration file (the container name is found using 'docker ps')
docker-compose exec odoo cat /etc/odoo.cfg
# run bash in the running odoo container
docker exec odoo bash
```

**docker run** spawns a new container for a given service, allowing the
interactive mode, which is exactly what we want to run Odoo with pdb.
This is probably the command you'll use the most often.

The `--rm` option drops the container after usage, which is usually what we
want.

```bash
# start Odoo (use workers=0 for dev)
docker-compose run --rm odoo odoo --workers=0 ... additional arguments
# start Odoo and expose the port 8069 to the host on the port 80
docker-compose run --rm -p 80:8069 odoo odoo
# open an odoo shell
docker-compose run --rm odoo odoo shell
```

`workers=0` let you use your `pdb` interactive mode without trouble otherwise
you will have to deal with one trace per worker that catched a breakpoint.
Plus, it will stop the annoying `bus is not available` errors.

### Handy aliases

Finally, a few aliases suggestions:

```bash
alias doco='docker-compose'
alias docu='docker-compose up -d'
alias docl='docker-compose logs'
alias docsh='docker-compose run --rm odoo odoo shell'
alias dood='docker-compose run --rm odoo odoo'
alias bro='chromium-browser --incognito $(docker-compose port odoo 8069)'
# run anthem song. Just run `dood_anthem songs.install.foo::baz`
alias dood_anthem='docker-compose run --rm odoo anthem'
# run odoo w/ connector jobrunner. Just run `dood_conn` instead of dood (connector v9)
alias dood_conn='docker-compose run --rm odoo odoo --workers=0 --load=web,connector'
# run odoo w/ queue_job jobrunner. Just run `dood_queue` instead of dood (connector v10)
alias dood_queue='docker-compose run --rm odoo odoo --workers=0 --load=web,queue_job'
# run odoo without marabunta migration. Just run `dood_nomig`
alias dood_nomig='docker-compose run --rm -e MIGRATE=False odoo odoo --workers=0'
```

and to speed up your testing sessions (see [core images' test doc](https://github.com/camptocamp/docker-odoo-project#running-tests)):

```bash
# setup test database. Just run `dood_test_setup`
alias dood_test_setup='docker-compose run --rm -e DB_NAME=testdb odoo testdb-gen -i base'
# reuse testdb and install or update modules on demand. Just run `dood_test_update -i/u something`
alias dood_test_update='docker-compose run --rm -e DB_NAME=testdb odoo testdb-update'
# run tests using pytest. Just run `dood_test_run path/to/your/module`
# NOTE: you need to run dood_test_update 1st IF xml or models have been updated
alias dood_test_run='docker-compose run --rm -e DB_NAME=testdb odoo pytest -s'
# run tests using std odoo test machinery (eg: you need an HttpCase). Just run `dood_test_run_odoo -u module`
alias dood_test_run_odoo='docker-compose run --rm -e DEMO=True -e DB_NAME=testdb -e MIGRATE=False odoo odoo --workers=0 --test-enable --stop-after-init'
```

Usage of the aliases / commands:
```bash

# Start all the containers in background
docu

# Show status of containers
doco ps

# show logs of odoo or postgres
docl odoo
docl db

# run a one-off command in a container
doco run --rm odoo bash

# open a chromium browser on the running odoo
bro

# stop all the containers
doco stop

# upgrade module and or run tests
dood -u my_module [--test-enable]

# if you are using the `connector` remember to pass the `load` attribute
dood --load=web,connector
```

### Working with several databases

This section has been moved to : [working-with-several-databases](docker-and-databases.md#working-with-several-databases).


### Extra dev docker composition

You might want to customize your docker composition like adding a container or setting specific ports.
For this use `docker-compose.override.yml` file which will always be loaded unless `-f` option of docker-compose
is used.

Example:

```
# content of docker-compose.override.yml
version: '2'

services:
  odoo:
    environment:
      WORKERS=0
```


### Extra dev packages

You might want to use additional python packages while developing (eg: pdbpp, ipdb, etc).
You can easily add them in `odoo/dev_requirements.txt` and build again odoo container:

```bash
echo "pdbpp" >> odoo/dev_requirements.txt
doco build odoo
```

### Develop on a python dependency

For some odoo addons, you might have to do changes in their python dependencies, and
 you obviously don't want to rebuild your image for every change you did in this
 package, nor keep the sources inside of your project or add it as a submodule.
The only thing to do is to define a Docker volume to override the initial installation
 by pypi with your local copy.

Let's assume your python dependency is called PyExample and you have a local clone on
 your machine at `/home/user/dev/pyexample`.

Create a symlink inside your project to the package's path

```bash
cd odoo
ln -s /home/user/dev/pyexample
```

Then get the path of the package installation inside the container

```bash
docker-compose run --rm odoo python -c "import pyexample; print(pyexample)"
(...)
<module 'pyexample' from '/usr/local/lib/python2.7/dist-packages/pyexample/__init__.pyc'>
```

With the path in hand, you can now define a new volume in `docker-compose.override.yml`.

```yaml
- "./odoo/pyexample/:/usr/local/lib/python2.7/dist-packages/pyexample"
```

### Troubleshooting

```
pkg_resources.DistributionNotFound: The 'odoo==10.0' distribution was not found and is required by the application
```

This error can happen after switching Odoo version in the same project.
You should then manually delete the `.egg-info` and `__pycache__` folders :

```
sudo rm -rf 'find -name *.egg-info'
sudo rm -rf 'find -name __pycache__'
```
