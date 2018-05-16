# Odoo Demos

This repository contains Odoo Demos. They are built using our project template and can be deployed to minions
Each branch is a different demo. 

## Create a new demo

1. Create a new branch

Branch naming: <version>-<description>. Example: 9.0-ddmrp

2. Remove the README and generate a project from the template (https://github.com/camptocamp/odoo-template)

```
rm README.md
cookiecutter git@github.com:camptocamp/odoo-template.git
```

Answer to the following questions:

```
You've cloned /home/gbaconnier/.cookiecutters/odoo-template before. Is it okay to delete and re-clone it? [yes]: yes
customer_name [Customer]: demo
Select odoo_version:
1 - 9.0
2 - 10.0
3 - 11.0
Choose from 1, 2, 3 [1]: 3  # (pick the one you want)
customer_shortname [demo]: demo
repo_name [demo]: generated
project_name [demo_odoo]: demo_odoo
project_id [0000]:
odoo_company_name [demo]:
Select platform_name:
1 - none
2 - fr
3 - ch
Choose from 1, 2, 3 [1]: 1
```

3. Move the generated template to the root folder, and commit

```
mv generated/{.,}* .
rm -rf generated
git add .
git commit -m"generated demo from template"
```

4. Change the password for the admin user, in `odoo/songs/install/pre.py`:

```
@anthem.log
def admin_user_password(ctx):
    """ Changing admin password """
    # ... snip ...
    if os.environ.get('RUNNING_ENV') == 'dev':
        ctx.log_line('Not changing password for dev RUNNING_ENV')
        return
    # Change the assignment by this one:
    # the corresponding entry in lastpass already exists as:
    # Shared-C2C-Odoo-External\demo_odoo\[odoo-test] demo test admin user (minions)
    ctx.env.user.password_crypt = (
        '$pbkdf2-sha512$12000$VIqR0nrvfe.dc855r9Wa0w$EWEE/QrBE8U3xTn5cgRs9'
        'w/srmpuVcn7Jude0j/bnNizbj1mOgvM9gpd4sD37WkNWKwDq7KQhMOrCpRlBcjvUw'
    )
```

5. You might want to activate the Odoo's demo data, to do so, add:

In docker-compose.yml in the root directory:

```
  odoo:
    environment:
    - DEMO=True
```

In travis/minion-files/rancher.list, set `DEMO` to `True`.


6. Customize the demo. Minions should be created automatically on https://demo.odoo-test.camptocamp.ch
