# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

class OpFaculty(models.Model):
    _name = "op.faculty"
    _description = "Faculty"
    _inherits = {'res.partner': 'partner_id'}

    partner_id = fields.Many2one(
        'res.partner', string='Partner', required=True, ondelete='cascade'
    )
    image_128 = fields.Image(related='partner_id.image_128', readonly=True)

    # Personal Information
    birth_date = fields.Date('Birth Date', required=True)
    blood_group = fields.Selection([
        ('A+', 'A+ve'), ('B+', 'B+ve'), ('O+', 'O+ve'), ('AB+', 'AB+ve'),
        ('A-', 'A-ve'), ('B-', 'B-ve'), ('O-', 'O-ve'), ('AB-', 'AB-ve')
    ], string='Blood Group')
    gender = fields.Selection([
        ('male', 'Male'), ('female', 'Female')
    ], 'Gender', required=True)
    nationality = fields.Many2one('res.country', string='Nationality')
    lang = fields.Selection(related='partner_id.lang', readonly=False)
    visa_info = fields.Char(string='Visa Info')

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

    # Academic and System Information
    department_id = fields.Many2one('op.department', string='Main Department')
    allowed_department_ids = fields.Many2many(
        'op.department', 'faculty_department_rel',
        'faculty_id', 'department_id', string='Allowed Departments')
    program_id = fields.Many2one('op.program', string='Program')
    subject_ids = fields.Many2many('op.subject', string='Subjects')
    qualifications = fields.Text(string='Qualifications')
    specialization = fields.Text(string='Specialization')
    office_location = fields.Char(string='Office Location')
    employee_id = fields.Many2one('hr.employee', string='Related Employee')
    user_id = fields.Many2one('res.users', string='Related User', related='partner_id.user_ids.user_id', view_load=True)

    # Smart Button relationship fields
    course_ids = fields.Many2many('op.course', 'faculty_course_rel', 'faculty_id', 'course_id', string='Courses')
    session_ids = fields.Many2many(
        'op.session', 'op_session_faculty_rel', 'faculty_id', 'session_id', string="Sessions")

    # Smart Button count fields
    course_count = fields.Integer(string='Course Count', compute='_compute_counts')
    subject_count = fields.Integer(string='Subject Count', compute='_compute_counts')
    session_count = fields.Integer(string='Session Count', compute='_compute_counts')

    @api.depends('course_ids', 'subject_ids', 'session_ids')
    def _compute_counts(self):
        for faculty in self:
            faculty.course_count = len(faculty.course_ids)
            faculty.subject_count = len(faculty.subject_ids)
            faculty.session_count = len(faculty.session_ids)

    # Actions for Smart Buttons
    def action_view_courses(self):
        self.ensure_one()
        return {
            'name': _('Courses'),
            'type': 'ir.actions.act_window',
            'res_model': 'op.course',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', self.course_ids.ids)],
        }

    def action_view_subjects(self):
        self.ensure_one()
        return {
            'name': _('Subjects'),
            'type': 'ir.actions.act_window',
            'res_model': 'op.subject',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', self.subject_ids.ids)],
        }

    def action_view_sessions(self):
        self.ensure_one()
        return {
            'name': _('Sessions'),
            'type': 'ir.actions.act_window',
            'res_model': 'op.session',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', self.session_ids.ids)],
        }

    @api.constrains('birth_date')
    def _check_birthdate(self):
        for record in self:
            if record.birth_date and record.birth_date > fields.Date.today():
                raise ValidationError(_("Birth Date can't be greater than current date!"))