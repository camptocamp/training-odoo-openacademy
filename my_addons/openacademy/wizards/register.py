from openerp import models, fields, api


class Register(models.TransientModel):
    _name = 'openacademy.register'

    def _default_session(self):
        session_model = self.env['openacademy.session']
        return session_model.browse(self.env.context.get('active_ids'))

    session_ids = fields.Many2many(
        comodel_name='openacademy.session',
        string="Session",
        required=True,
        default=_default_session,
    )
    attendee_ids = fields.Many2many(
        comodel_name='res.partner',
        string="Attendees",
    )

    @api.multi
    def subscribe(self):
        for session in self.session_ids:
            session.attendee_ids |= self.attendee_ids
        return {}
