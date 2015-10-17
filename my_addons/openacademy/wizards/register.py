from openerp import models, fields, api

class Register(models.TransientModel):
    _name = 'openacademy.register'

    session_ids = fields.Many2many(
        comodel_name='openacademy.session',
        string="Session",
        required=True,
    )
    attendee_ids = fields.Many2many(
        comodel_name='res.partner',
        string="Attendees",
    )
