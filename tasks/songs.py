# -*- coding: utf-8 -*-
# This file has been generated with 'invoke project.sync'.
# Do not modify. Any manual change will be lost.
# Please propose your modification on
# https://github.com/camptocamp/odoo-template instead.
# This file has been generated with 'invoke project.sync'.
# Do not modify. Any manual change will be lost.
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)
import io
import zipfile

from invoke import task

from .common import exit_msg

try:
    # Python 2
    from urlparse import urlparse
except ImportError:
    # Python 3
    from urllib.parse import urlparse
try:
    import requests
except ImportError:
    print('Missing python `requests` from requirements')
    print('Please run `pip install -r tasks/requirements.txt`')


def odoo_login(base_url, login, password, db):
    """ Get a session_id from Odoo """
    url = "%s/web/session/authenticate" % base_url

    data = {
        'jsonrpc': '2.0',
        'params': {
            'context': {},
            'db': db,
            'login': login,
            'password': password,
        },
    }

    headers = {'Content-type': 'application/json'}

    resp = requests.post(url, json=data, headers=headers)
    r_data = resp.json()
    return r_data['result']['session_id']


@task(name='rip')
def rip(
    ctx,
    location,
    login='admin',
    password='admin',
    db='odoodb',
    dryrun=False,
    data_path='./odoo/data',
):
    """Open or download a zipfile containing songs.

    Unzip and copy the files into current project path.

    :param location: compilation URL or file path
    :param login: odoo username required if location is an URL
    :param password: odoo username password required if location is an URL
    :param odoodb: odoo database required if location is an URL
    :param dry_run: just print the compilation content
        do not add files to project.
    """
    if not location:
        exit_msg(
            "You must provide a value for --location\n"
            "It can be an url or a local path\n\n"
            "invoke songs.rip /tmp/songs.zip\n"
            "invoke songs.rip "
            "http://project:8888/dj/download/compilation/account-default-1"
        )
    zipdata = None
    # download file from url
    if location.startswith('http'):
        url = urlparse(location)
        base_url = "{}://{}".format(url.scheme, url.netloc)
        session_id = odoo_login(base_url, login, password, db)
        cookies = {"session_id": session_id}
        resp = requests.get(location, cookies=cookies)
        resp.raise_for_status()
        zipdata = io.BytesIO()
        zipdata.write(resp.content)
    else:
        zipdata = location
    handle_zip_data(zipdata, dryrun=dryrun, data_path=data_path)


def handle_zip_data(zipdata, dryrun=False, data_path='./odoo/data'):
    if dryrun:
        print("Dry-run mode activated: no file will be extracted.")
    zf = zipfile.ZipFile(zipdata)

    # Unzip file and push files at the right path
    readme_path = None
    for path in zf.namelist():
        if dryrun:
            print(path)
        # Ignore dj metadata zip file
        if path.endswith('zip'):
            continue
        if 'DEV_README.rst' in path:
            readme_path = path
        else:
            if not dryrun:
                dest_path = data_path[:]
                if path.startswith('songs'):
                    # TODO: we assume songs path
                    # is on the same level of data path
                    dest_path = '/'.join(data_path.split('/')[:2])
                print("Extracting {}/{}".format(dest_path, path))
                zf.extract(path, dest_path)

    print('-' * 79)
    # Print README file
    readme_content = zf.open(readme_path).read()
    readme_content = readme_content.decode('utf-8')
    print(readme_content)
