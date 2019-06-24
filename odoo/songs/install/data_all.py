# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)
""" Data loaded in all modes

The data loaded here will be loaded in the 'sample' and
'full' modes.
"""

import anthem


@anthem.log
def main(ctx):
    """ Loading data """
