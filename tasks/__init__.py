# -*- coding: utf-8 -*-
# This file has been generated with 'invoke project.sync'.
# Do not modify. Any manual change will be lost.
# Please propose your modification on
# https://github.com/camptocamp/odoo-template instead.

import os
import importlib

from invoke import Collection

ns = Collection()


for filename in os.listdir(os.path.dirname(os.path.realpath(__file__))):
    if filename.endswith('.py') and not filename.startswith('__'):
        modname = filename[:-3]
        mod = importlib.import_module('.' + modname, package='tasks')
        ns.add_collection(mod)
