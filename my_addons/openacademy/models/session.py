# -*- coding: utf-8 -*-
from openerp import models, fields, api, exceptions, _


class Session(models.Model):
    _name = 'openacademy.session'

    name = fields.Char(required=True)
    start_date = fields.Date(default=fields.Date.today)
    duration = fields.Float(digits=(6, 2), help="Duration in days")
    seats = fields.Integer(string="Number of seats")
    instructor_id = fields.Many2one(
        comodel_name='res.partner',
        string="Instructor",
        domain=['|', ('instructor', '=', True),
                     ('category_id.name', 'ilike', "Formateur")],
    )
    course_id = fields.Many2one(comodel_name='openacademy.course',
                                ondelete='cascade',
                                string='Course',
                                required=True)
    attendee_ids = fields.Many2many(comodel_name='res.partner',
                                    string="Attendees")
    taken_seats = fields.Float(string="Taken seats",
                               compute='_compute_taken_seats')
    active = fields.Boolean(default=True)
    state = fields.Selection(
        selection='_selection_state',
        readonly=True,
        default='draft',
    )

    @api.model
    def _selection_state(self):
        return [('draft', "Draft"),
                ('confirmed', "Confirmed"),
                ('done', "Done")]

    @api.depends('seats', 'attendee_ids')
    def _compute_taken_seats(self):
        for r in self:
            if not r.seats:
                r.taken_seats = 0.0
            else:
                r.taken_seats = 100.0 * len(r.attendee_ids) / r.seats

    @api.constrains('instructor_id', 'attendee_ids')
    def _check_instructor_not_in_attendees(self):
        for r in self:
            if r.instructor_id and r.instructor_id in r.attendee_ids:
                raise exceptions.ValidationError(
                    _("A session's instructor can't be an attendee")
                )

    @api.onchange('seats', 'attendee_ids')
    def _verify_valid_seats(self):
        if self.seats < 0:
            return {
                'warning': {
                    'title': _("Incorrect 'seats' value"),
                    'message': _("The number of available seats "
                                 "may not be negative"),
                },
            }
        if self.seats < len(self.attendee_ids):
            return {
                'warning': {
                    'title': _("Too many attendees"),
                    'message': _("Increase seats or remove excess attendees"),
                },
            }

    @api.multi
    def action_draft(self):
        self.write({'state': 'draft'})

    @api.multi
    def action_confirm(self):
        self.write({'state': 'confirmed'})

    @api.multi
    def action_done(self):
        self.write({'state': 'done'})
