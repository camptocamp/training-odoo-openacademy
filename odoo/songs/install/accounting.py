# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import anthem
from anthem.lyrics.records import create_or_update


@anthem.log
def activate_multicurrency(ctx):
    """ Activating multi-currency """
    employee_group = ctx.env.ref('base.group_user')
    employee_group.write(
        {'implied_ids': [(4, ctx.env.ref('base.group_multi_currency').id)]}
    )


@anthem.log
def create_bank_accounts(ctx):
    """ Creating bank accounts """
    expense_type = ctx.env.ref('account.data_account_type_expenses')
    records = [
        {
            'xmlid': '__setup__.account_1010',
            'name': 'XXX 00-001285-1',
            'code': '991010',
            'user_type_id': expense_type.id,
        },
        {
            'xmlid': '__setup__.account_1020',
            'name': 'ZZZ BE7400700115500080000',
            'code': '991020',
            'user_type_id': expense_type.id,
        },
        {
            'xmlid': '__setup__.account_1021',
            'name': 'ZZZ BE2300700115500172222',
            'code': '991021',
            'user_type_id': expense_type.id,
        },
    ]
    for record in records:
        xmlid = record.pop('xmlid')
        create_or_update(ctx, 'account.account', xmlid, record)


@anthem.log
def main(ctx):
    """ Configuring accounting """
    activate_multicurrency(ctx)
    create_bank_accounts(ctx)
