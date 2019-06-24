<!--
This file has been generated with 'invoke project.sync'.
Do not modify. Any manual change will be lost.
Please propose your modification on
https://github.com/camptocamp/odoo-template instead.
-->
# How to test SMTP

## MailHog

In the development environment, a [MailHog](https://github.com/mailhog/MailHog) container is started alongside odoo.

This service is published by default on http://localhost:8025

The default server environment file configuration for `dev` is configured to use this MailHog container as SMTP server. As soon as Odoo sends an email, it will be trapped in the MailHog server and can be viewed on http://localhost:8025

## Add setup on an existing project

If the container does not exist on this project because it's older than this, you'll need to:

* Add the container in docker-compose.yml
* Add the `server_environment_file` config in the `dev` profile

Using this commit as reference: https://github.com/guewen/odoo-template/commit/0645e82ac104c444015ba54fbe9706dce4c4d2bf

## MailTrap

In integration and test environment, [mailtrap.io](https://mailtrap.io) is used.

To create a new account for a project, use the email address that can be found on the specific project page (tab "Other Info") of our Odoo instance and a random password.

The confirmation email of mailtrap.io will appear in the tasks of the corresponding project in Odoo.

Don't forget to add an entry in lastpass.
