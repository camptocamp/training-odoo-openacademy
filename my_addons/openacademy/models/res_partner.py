# -*- coding: utf-8 -*-
from openerp import fields, models


class Partner(models.Model):
    _inherit = 'res.partner'

    instructor = fields.Boolean("Instructor", default=False)
    session_ids = fields.Many2many(comodel_name='openacademy.session',
                                   string="Attended Sessions",
                                   readonly=True)
