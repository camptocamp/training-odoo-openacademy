# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import anthem


@anthem.log
def do_something(ctx):
    pass


@anthem.log
def main(ctx):
    do_something(ctx)
