<!--
This file has been generated with 'invoke project.sync'.
Do not modify. Any manual change will be lost.
Please propose your modification on
https://github.com/camptocamp/odoo-template instead.
-->
# Adding language in Odoo

## Why my language is not installable with my container?

PO files are not added to the docker image.
By default only fr.po and de.po files are preserved when generating
docker images.

This allow us ot optimize the size of the docker images.

To give you an idea of the gain:

```bash
odoo/src
*.po  285 MB
fr.po 1.28 MB
de.po 982 kB
```

## .dockerignore edition

To add a langague edit the `odoo/.dockerignore` file

```
**/i18n/*.po
# installable lang
!**/i18n/de.po
!**/i18n/fr.po
```

`**/i18n/*.po`
filters all files with extension .po that are located
in a `i18n` folder

`!` is to exclude a path definition from ignore list, it is important to
place an exclusion after the main rule or it will have no effect.

See https://docs.docker.com/engine/reference/builder/#dockerignore-file for more details.

Once you edited that file rebuild your image and it will contains your new language.
