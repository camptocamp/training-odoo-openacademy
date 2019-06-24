<!--
This file has been generated with 'invoke project.sync'.
Do not modify. Any manual change will be lost.
Please propose your modification on
https://github.com/camptocamp/odoo-template instead.
-->
# CUPS Server

## Setup

### CUPS container

In a brand new environment when you do `docker-compose up` you get `cups-server` service automatically.

In an existing environment just do `docker-compose up -d cups-server`.

### Odoo container

If your project relies on CUPS and `base_report_to_printer` then you should already have this.
In any case, make sure you have these requirements in place:

* install `cups` and `libcups2-dev` in `odoo/Dockerfile`
* `/odoo/external-src/report-print-send` in ADDONS_PATH
* `git@github.com:OCA/report-print-send.git` checked out in the path above


## CUPS Configuration

Go to `http://localhost:6631` and type credentials `admin / secr3t`.

Then you have to configure a printer:

1. Go to Administration -> Printers -> click on `Add printer`

.. image:: ./images/cups_administration.png

2. Select `CUPS-PDF` and continue

.. image:: ./images/cups_add_printer1.png

3. Leave printer info as it is and make sure to enable `Share This Printer`

.. image:: ./images/cups_add_printer2.png

4. Select `generic` and continue

.. image:: ./images/cups_set_printer_type1.png

5. Select `Generic CUPS-PDF Printer (en)` and continue

.. image:: ./images/cups_set_printer_type2.png

6. Set default size to `A4` and click on `Set Default Options`

.. image:: ./images/cups_set_printer_options.png


Now you can go to `Printers` and see your brand new printer.

## Odoo Configuration

The final step is to tell Odoo about your printer:

1. Go to Settings -> Printers -> Create
2. Give it a name and set server as `cups-server`, default port `631` is ok
3. Save and click on `Update printers` -> your PDF printer should show up

.. image:: ./images/odoo_printer.png


Your are done now. Every printed document will land into `/tmp/cups-pdf` folder.
