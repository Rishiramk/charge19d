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

    # Contact Information
    phone = fields.Char(related='partner_id.phone_sanitized', readonly=False)
    mobile = fields.Char(related='partner_id.phone', readonly=False)
    email = fields.Char(related='partner_id.email', readonly=False)
    street = fields.Char(related='partner_id.street', readonly=False)
    street2 = fields.Char(related='partner_id.street2', readonly=False)
    city = fields.Char(related='partner_id.city', readonly=False)
    state_id = fields.Many2one('res.country.state', related='partner_id.state_id', readonly=False)
    zip = fields.Char(related='partner_id.zip', readonly=False)
    country_id = fields.Many2one('res.country', related='partner_id.country_id', readonly=False)

    # Academic Information
    department_id = fields.Many2one('op.department', string='Department')
    program_id = fields.Many2one('op.program', string='Program')
    subject_ids = fields.Many2many('op.subject', string='Subjects')
    qualifications = fields.Text(string='Qualifications')
    specialization = fields.Text(string='Specialization')
    office_location = fields.Char(string='Office Location')

    session_ids = fields.Many2many(
        'op.session', 'op_session_faculty_rel', 'faculty_id', 'session_id', string="Sessions")
    session_count = fields.Integer(string='Session Count', compute='_compute_session_count')

    def _compute_session_count(self):
        for faculty in self:
            faculty.session_count = len(faculty.session_ids)

    @api.constrains('birth_date')
    def _check_birthdate(self):
        for record in self:
            if record.birth_date and record.birth_date > fields.Date.today():
                raise ValidationError(_("Birth Date can't be greater than current date!"))