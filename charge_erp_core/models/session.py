from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

class Session(models.Model):
    """
    Represents a specific teaching session for a course, led by a faculty member.
    It includes details about the schedule, duration, and attendees.
    """
    _name = 'op.session'
    _description = 'Open Academy Sessions'

    name = fields.Char(required=True)
    start_datetime = fields.Datetime(string="Start Time", default=fields.Datetime.now)
    duration = fields.Float(digits=(6, 2), help="Duration in days")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ], string='Status', default='draft', required=True)
    seats = fields.Integer(string="Number of seats")
    faculty_id = fields.Many2one('op.faculty', string="Faculty")
    course_id = fields.Many2one('op.course', ondelete='cascade', string="Course", required=True)
    attendee_ids = fields.Many2many(
        'op.student', 'op_session_student_rel', 'session_id', 'student_id', string="Attendees")
    student_partner_ids = fields.Many2many(
        'res.partner',
        string="Student Partners",
        compute='_compute_student_partner_ids',
        store=True)
    academic_year_id = fields.Many2one('op.academic.year', string='Academic Year')

    @api.depends('attendee_ids.partner_id')
    def _compute_student_partner_ids(self):
        for session in self:
            session.student_partner_ids = session.attendee_ids.mapped('partner_id')

    @api.constrains('seats', 'attendee_ids')
    def _check_seats(self):
        """
        Validates that the number of seats is not negative and that the number
        of attendees does not exceed the available seats.
        """
        for r in self:
            if r.seats < 0:
                raise ValidationError(_(
                    "The number of available seats cannot be negative."))
            if len(r.attendee_ids) > r.seats:
                raise ValidationError(_(
                    "There are more attendees than available seats."))

    @api.constrains('duration')
    def _check_duration(self):
        """Ensures the session duration is not a negative value."""
        for r in self:
            if r.duration < 0:
                raise ValidationError(_("The duration cannot be negative."))

    def action_start_session(self):
        self.write({'state': 'in_progress'})

    def action_mark_completed(self):
        self.write({'state': 'completed'})

    def action_cancel(self):
        self.write({'state': 'cancelled'})

    def action_reset_to_draft(self):
        self.write({'state': 'draft'})