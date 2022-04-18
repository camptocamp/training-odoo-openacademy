#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file has been generated with 'invoke project.sync'.
# Do not modify. Any manual change will be lost.
# Please propose your modification on
# https://github.com/camptocamp/odoo-template instead.
# Download submodules from Github archive url
# Keep standard update form private repositories
# listed in `travis/private_repo`
#
from __future__ import print_function

import os
import shutil
import tarfile

import yaml
from git import Repo

try:
    # For Python 3.0 and later
    import urllib.request as requestlib
except ImportError:
    # Fall back to Python 2's urllib2
    import urllib2 as requestlib


SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, os.pardir))
DL_DIR = 'download'
ARCHIVE_PATH = '%s/submodule.tar.gz' % DL_DIR


def git_url(url):
    """ Change an url to https and ending without .git all in lower case
    This to reuse it for archive download and to make it comparable.
    """
    url = url.lower()
    if url.startswith('git@github.com:'):
        url = url.replace('git@github.com:', 'https://github.com/')
    # remove .git
    if url.endswith('.git'):
        url = url[:-4]
    return url


INCONSISTENT_MSG = """
In .gitmodules {path} :\n
    remote url {remote_url} does not match \n
    target url {target_url} \n
in {pending_path}\n
\n
If you added pending merges entries you probably forgot to edit
    target in .gitmodules file to match the fork repository\n
or if your intent is to clean up entries in pending-merges.yml.\n
    something went wrong in that file.\n
    Hint: consider taking a look at specialized `invoke` tasks:\n
`submodule.add-pending <PR>` and `submodule.remove-pending <PR>`
"""


def check_consistency(submodules):
    """Check consistency between .gitmodules and pending merges."""
    for sub in submodules:
        sub_name = os.path.basename(sub.path)
        sub_merges_path = './pending-merges.d/{}.yml'.format(sub_name)
        if not os.path.exists(sub_merges_path):
            continue
        with open(sub_merges_path) as pending_yml:
            pending_merges = yaml.safe_load(pending_yml) or []
        pending = list(pending_merges.values())[0]
        target = pending['target'].split()[0]
        target_remote = pending['remotes'][target]
        assert git_url(target_remote) == git_url(
            sub.url.lower()
        ), INCONSISTENT_MSG.format(
            path=sub.path,
            remote_url=target_remote,
            target_url=sub.url,
            pending_path=sub_merges_path,
        )


def download_submodules(submodules, private_repos):
    """Download submodules, possibly via zip archive url."""
    for sub in submodules:
        print("Getting submodule %s" % sub.path)
        use_archive = sub.path not in private_repos
        if use_archive:
            url = git_url(sub.url)
            filename = "{}.tar.gz".format(sub.hexsha)
            archive_url = "{}/archive/{}".format(url, filename)
            request = requestlib.Request(archive_url)
            with open(ARCHIVE_PATH, 'wb') as f:
                f.write(requestlib.urlopen(request).read())
            try:
                with tarfile.open(ARCHIVE_PATH, "r:gz") as tf:
                    tf.extractall(DL_DIR)
            except tarfile.ExtractError:
                # fall back to standard download
                use_archive = False
                with open(ARCHIVE_PATH) as f:
                    print(
                        "Getting archive failed with error %s. "
                        "Falling back to git clone." % f.read()
                    )
                os.remove(ARCHIVE_PATH)
            except Exception as e:
                use_archive = False
                print(
                    "Getting archive failed with error %s. "
                    "Falling back to git clone." % str(e)
                )
            else:
                if os.path.exists(ARCHIVE_PATH):
                    os.remove(ARCHIVE_PATH)
                if os.path.exists(sub.path):
                    os.removedirs(sub.path)
                submodule_dir = os.listdir(DL_DIR)[0]
                shutil.move(os.path.join(DL_DIR, submodule_dir), sub.path)
        if not use_archive:
            os.system('git submodule update %s' % sub.path)


def _setup_proxy():
    https_proxy = os.environ.get('https_proxy')
    if https_proxy:
        proxy = requestlib.ProxyHandler({'https': https_proxy})
        opener = requestlib.build_opener(proxy)
        requestlib.install_opener(opener)


def _get_private_repos():
    with open('travis/private_repos') as f:
        return f.read()


if __name__ == '__main__':
    _setup_proxy()
    os.chdir(ROOT_DIR)

    if os.path.exists(DL_DIR):  # clean if previous build failed
        shutil.rmtree(DL_DIR)
    os.makedirs(DL_DIR)

    os.system('git submodule init')

    submodules = Repo('.').submodules

    check_consistency(submodules)
    private_repos = _get_private_repos()
    download_submodules(submodules, private_repos)
