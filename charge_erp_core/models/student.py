# -*- coding: utf-8 -*-
from datetime import date
from odoo import api, models, fields

class OpStudent(models.Model):
    _name = 'op.student'
    _description = 'Student'
    _inherits = {'res.partner': 'partner_id'}

    # Link to res.partner
    partner_id = fields.Many2one(
        'res.partner', string='Partner', required=True, ondelete='cascade'
    )

    # Personal Information
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], string='Gender')
    birth_date = fields.Date(string='Birth Date')
    age = fields.Integer(string='Age', compute='_compute_age')
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
    mobile = fields.Char("Mobile")
    emergency_contact_id = fields.Many2one(
        'res.partner', string='Emergency Contact Partner', ondelete='set null')
    parent_ids = fields.Many2many(
        'res.partner', 'op_student_parent_rel', 'student_id', 'parent_id', string='Parents')

    # Other Information
    student_id = fields.Char(string='Student ID')
    registration_number = fields.Char(string='Registration Number')
    library_card = fields.Char(string='Library Card')
    badge_id = fields.Char(string='Badge ID')
    category = fields.Char(string='Category')
    user_id = fields.Many2one('res.users', string='User')
    batch_id = fields.Many2one('op.batch', string='Batch')
    program_id = fields.Many2one('op.program', string='Program')
    miscellaneous = fields.Text(string='Miscellaneous')
    session_ids = fields.Many2many(
        'op.session', 'op_session_student_rel', 'student_id', 'session_id', string="Sessions")
    session_count = fields.Integer(string='Session Count', compute='_compute_session_count')

    def _compute_session_count(self):
        for student in self:
            student.session_count = len(student.session_ids)

    @api.depends('birth_date')
    def _compute_age(self):
        for record in self:
            if record.birth_date:
                today = date.today()
                record.age = today.year - record.birth_date.year - \
                    ((today.month, today.day) <
                     (record.birth_date.month, record.birth_date.day))
            else:
                record.age = 0