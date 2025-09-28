# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError

class OpStudent(models.Model):
    _name = 'op.student'
    _description = 'Student'
    _inherits = {'res.partner': 'partner_id'}

    # Link to res.partner
    partner_id = fields.Many2one(
        'res.partner', string='Partner', required=True, ondelete='cascade'
    )
    image_128 = fields.Image(related='partner_id.image_128', readonly=True)

    # Personal Information
    lang = fields.Selection(related='partner_id.lang', readonly=False)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], string='Gender')
    status = fields.Selection([
        ('active', 'Active'),
        ('graduated', 'Graduated'),
        ('on_leave', 'On Leave')
    ], string='Status', default='active', required=True)
    birth_date = fields.Date(string='Birth Date')
    blood_group = fields.Selection([
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('O+', 'O+'), ('O-', 'O-'),
        ('AB+', 'AB+'), ('AB-', 'AB-')
    ], string='Blood Group')
    nationality = fields.Many2one('res.country', string='Nationality')
    visa_info = fields.Char(string='Visa Info')
    is_an_alumni = fields.Boolean(string='Is an Alumni?')
    id_number = fields.Char(string='ID Card Number')

    # Contact Information
    address_type = fields.Selection(related='partner_id.type', string="Address Type", readonly=False)
    phone = fields.Char(string='Phone')
    mobile = fields.Char(string='Mobile')
    email = fields.Char(related='partner_id.email', readonly=False)
    street = fields.Char(related='partner_id.street', readonly=False)
    street2 = fields.Char(related='partner_id.street2', readonly=False)
    city = fields.Char(related='partner_id.city', readonly=False)
    state_id = fields.Many2one('res.country.state', related='partner_id.state_id', readonly=False)
    zip = fields.Char(related='partner_id.zip', readonly=False)
    country_id = fields.Many2one('res.country', related='partner_id.country_id', readonly=False)
    emergency_contact_id = fields.Many2one(
        'res.partner', string='Emergency Contact', ondelete='set null')
    parent_ids = fields.Many2many(
        'res.partner', 'op_student_parent_rel', 'student_id', 'parent_id', string='Parents')

    # Other Information
    roll_number = fields.Char(string='Roll Number')
    registration_number = fields.Char(string='Registration Number')
    library_card = fields.Char(string='Library Card')
    badge_id = fields.Char(string='Badge ID')
    pin = fields.Char(string='PIN', help="PIN for Kiosk Mode")
    category_id = fields.Many2one('op.category', string='Category')
    user_id = fields.Many2one('res.users', string='User')
    batch_id = fields.Many2one('op.batch', string='Batch')
    program_id = fields.Many2one('op.program', string='Program')
    miscellaneous = fields.Text(string='Miscellaneous')
    enrollment_ids = fields.One2many(
        'op.course.enrollment', 'student_id', string='Enrollments')
    session_ids = fields.Many2many(
        'op.session', 'op_session_student_rel', 'student_id', 'session_id', string="Sessions")
    session_count = fields.Integer(string='Session Count', compute='_compute_session_count')
    assignment_count = fields.Integer(string='Assignment Count', compute='_compute_assignment_count')
    fee_due_count = fields.Integer(string='Fee Due Count', compute='_compute_fee_due_count')
    attendance_count = fields.Integer(string='Attendance Count', compute='_compute_attendance_count')
    color = fields.Integer(string='Color', compute='_compute_color')

    @api.constrains('roll_number', 'registration_number')
    def _check_unique_student_identifiers(self):
        for student in self:
            if student.roll_number:
                domain = [('roll_number', '=', student.roll_number), ('id', '!=', student.id)]
                if self.search_count(domain):
                    raise ValidationError(_('The Roll Number must be unique.'))
            if student.registration_number:
                domain = [('registration_number', '=', student.registration_number), ('id', '!=', student.id)]
                if self.search_count(domain):
                    raise ValidationError(_('The Registration Number must be unique.'))

    def _compute_color(self):
        for student in self:
            if student.status == 'active':
                student.color = 2  # Green
            elif student.status == 'on_leave':
                student.color = 5  # Yellow
            elif student.status == 'graduated':
                student.color = 7  # Red
            else:
                student.color = 0  # Default

    def _compute_session_count(self):
        for student in self:
            student.session_count = len(student.session_ids)

    def _compute_assignment_count(self):
        for student in self:
            student.assignment_count = 0

    def _compute_fee_due_count(self):
        for student in self:
            student.fee_due_count = 0

    def _compute_attendance_count(self):
        for student in self:
            student.attendance_count = 0

    def action_view_assignments(self):
        raise UserError("The 'Assignments' module is not yet installed.")

    def action_view_fees(self):
        raise UserError("The 'Fees' module is not yet installed.")

    def action_view_attendance(self):
        raise UserError("The 'Attendance' module is not yet installed.")
