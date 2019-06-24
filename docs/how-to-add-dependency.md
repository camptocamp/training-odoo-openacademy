<!--
This file has been generated with 'invoke project.sync'.
Do not modify. Any manual change will be lost.
Please propose your modification on
https://github.com/camptocamp/odoo-template instead.
-->
# Adding dependencies

## How to add a Python package

The Python dependencies for Odoo are already installed in the base container
(camptocamp/odoo-project:12.0) used for this project. At times, you might need to add an additional dependency required solely for this project, here are the steps.

If the file `odoo/requirements.txt` exists, skip to number 3.

1. Create the file `odoo/requirements.txt`
2. Add the following lines in `odoo/Dockerfile` to instruct Docker to *copy* the requirements in the image and to *install* them with `pip`:

  ```
  COPY ./requirements.txt ./
  RUN pip install -r requirements.txt
  ```

3. Add the Python package in `odoo/requirements.txt`
4. Build again your Docker image: `docker-compose build odoo`

You can also [add dev requirements](./docker-dev.md#extra-dev-packages) which are used on your dev machine but never
committed, or might have to [develop on a python dependency](./docker-dev.md#develop-on-a-python-dependency).

## How to add a Debian package

Edit `odoo/Dockerfile` and add the following lines:

```
RUN set -x; \
        apt-get update \
        && apt-get install -y --no-install-recommends \
        <<name-of-the-package>> \
        && apt-get clean \
        && rm -rf /var/lib/apt/lists/*
```

If a similar command already exists. just add your package in
your list.
The cleanup at the end is important is it reduces the final size of the built image.

Once the package added, you have to build again your local Docker image using `docker-compose build odoo`
