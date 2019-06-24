# This file has been generated with 'invoke project.sync'.
# Do not modify. Any manual change will be lost.
# Please propose your modification on
# https://github.com/camptocamp/odoo-template instead.
#  Copyright 2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, http
from odoo.exceptions import UserError
from odoo.http import request


class CamptocampVersionController(http.Controller):
    @http.route(
        '/web/camptocamp/tools/versions',
        type='http',
        auth='user',
        website=False,
    )
    def camptocamp_versions(self, *args, **kwargs):
        if not request.env.user.has_group('base.group_no_one'):
            raise UserError(
                _("Only users with Technical Features activated are allowed.")
            )
        sql = """SELECT number, date_done
                 FROM marabunta_version
                 ORDER BY date_done DESC;"""
        request.env.cr.execute(sql)
        res = request.env.cr.dictfetchall()
        values = {'versions': res}
        return request.render(
            'camptocamp_tools.camptocamp_versions_template', values
        )
