# This file has been generated with 'invoke project.sync'.
# Do not modify. Any manual change will be lost.
# Please propose your modification on
# https://github.com/camptocamp/odoo-template instead.
# Copyright 2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)


from odoo import SUPERUSER_ID, api, fields, models

from ..utils import create_index, install_trgm_extension


class IrAttachment(models.Model):
    _inherit = 'ir.attachment'

    # Overloaded to add an index in order to boost performance.
    # store_fname is used to filter attachments in some SQL queries from
    # Odoo 9.0 to 11.0, and by the 'base_attachment_object_storage' module
    # (camptocamp/odoo-cloud-platform repository).
    store_fname = fields.Char(index=True)

    def init(self):
        env = api.Environment(self._cr, SUPERUSER_ID, {})
        self._init_indexes(env)

    def _init_indexes(self, env):
        """ Add index on ir_attachment.url to speed up the initial request
            made each time a page is (re)loaded :
            `select id from ir_attachment where url like '/web/content%'`
        """
        trgm_installed = install_trgm_extension(env)
        env.cr.commit()

        if trgm_installed:
            index_name = 'ir_attachment_url_trgm_index'
            create_index(
                env.cr, index_name, self._table, 'USING gin (url gin_trgm_ops)'
            )
