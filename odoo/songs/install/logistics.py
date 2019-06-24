# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import anthem


@anthem.log
def activate_options(ctx):
    """ Activating logistics options """
    employee_group = ctx.env.ref('base.group_user')
    employee_group.write(
        {
            'implied_ids': [
                (4, ctx.env.ref('stock.group_production_lot').id),
                (4, ctx.env.ref('stock.group_locations').id),
                (4, ctx.env.ref('stock.group_adv_location').id),
            ]
        }
    )


@anthem.log
def set_delivery_pick_ship(ctx):
    """ Setting pick-ship on the warehouse """
    ctx.env.ref('stock.warehouse0').delivery_steps = 'pick_ship'


@anthem.log
def main(ctx):
    """ Configuring logistics """
    activate_options(ctx)
    set_delivery_pick_ship(ctx)
