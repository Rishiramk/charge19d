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
    phone = fields.Char(string='Phone')
    mobile = fields.Char(string='Mobile')
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
    subject_ids = fields.Many2many(
        'op.subject', 'op_faculty_subject_rel',
        'faculty_id', 'subject_id', string='Subjects')
    tag_ids = fields.Many2many('op.tags', string='Tags')

    session_ids = fields.One2many(
        'op.session', 'faculty_id', string="Sessions")
    session_count = fields.Integer(string='Session Count', compute='_compute_session_count')

    def _compute_session_count(self):
        for faculty in self:
            faculty.session_count = len(faculty.session_ids)

    @api.constrains('birth_date')
    def _check_birthdate(self):
        for record in self:
            if record.birth_date and record.birth_date > fields.Date.today():
                raise ValidationError(_("Birth Date can't be greater than current date!"))