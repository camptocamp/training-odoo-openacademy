#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file has been generated with 'invoke project.sync'.
# Do not modify. Any manual change will be lost.
# Please propose your modification on
# https://github.com/camptocamp/odoo-template instead.
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from __future__ import print_function

import argparse
import os

import requests

parser = argparse.ArgumentParser()
parser.add_argument('docker_tag', type=str, help="Docker Tag")
parser.add_argument('minion_server', type=str, help="Rancher Minion Server")
parser.add_argument(
    'authorization_token', type=str, help="Minion Server Authorization Token"
)
parser.add_argument(
    'files',
    type=str,
    nargs='+',
    help="Repeat the argument for the different files. "
    "Files needed: 'docker-compose.yml', "
    "'rancher-compose.yml', 'rancher.list'",
)

args = parser.parse_args()

docker_tag = args.docker_tag
url = args.minion_server
token = args.authorization_token
files = args.files

if not url.startswith('https://'):
    print('https:// is mandatory')
    exit(1)

files_content = {
    os.path.basename(path): open(os.path.abspath(path), 'rb') for path in files
}

payload = {
    'docker_tag': docker_tag,
    'branch': os.environ.get('TRAVIS_BRANCH'),
    'commit': os.environ.get('TRAVIS_COMMIT'),
    'commit_message': os.environ.get('TRAVIS_COMMIT_MESSAGE'),
    'build_id': os.environ.get('TRAVIS_BUILD_ID'),
}

response = requests.post(
    url + '/new',
    data=payload,
    files=files_content,
    headers={'Authorization': token},
)
print(response.status_code)
response.raise_for_status()
