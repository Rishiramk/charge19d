from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

class Session(models.Model):
    _name = 'op.session'
    _description = 'Open Academy Sessions'

    name = fields.Char(required=True)
    start_date = fields.Date()
    duration = fields.Float(digits=(6, 2), help="Duration in days")
    seats = fields.Integer(string="Number of seats")
    classroom_id = fields.Many2one('op.classroom', string='Classroom')
    faculty_ids = fields.Many2many(
        'op.faculty', 'op_session_faculty_rel', 'session_id', 'faculty_id', string="Faculties")
    course_id = fields.Many2one('op.course', ondelete='cascade', string="Course", required=True)
    attendee_ids = fields.Many2many(
        'op.student', 'op_session_student_rel', 'session_id', 'student_id', string="Attendees")
    academic_year_id = fields.Many2one('op.academic.year', string='Academic Year')

    @api.constrains('seats', 'attendee_ids')
    def _check_seats(self):
        for r in self:
            if r.seats < 0:
                raise ValidationError(_(
                    "The number of available seats cannot be negative."))
            if len(r.attendee_ids) > r.seats:
                raise ValidationError(_(
                    "There are more attendees than available seats."))