# -*- coding: utf-8 -*-

from datetime import date
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

class OpFaculty(models.Model):
    _name = "op.faculty"
    _description = "Faculty"
    _inherits = {'res.partner': 'partner_id'}

    partner_id = fields.Many2one(
        'res.partner', string='Partner', required=True, ondelete='cascade'
    )

    employee_id = fields.Char(string='Employee ID')
    mobile = fields.Char(string='Mobile')

    birth_date = fields.Date('Birth Date', required=True)
    age = fields.Integer(string='Age', compute='_compute_age')
    blood_group = fields.Selection([
        ('A+', 'A+ve'), ('B+', 'B+ve'), ('O+', 'O+ve'), ('AB+', 'AB+ve'),
        ('A-', 'A-ve'), ('B-', 'B-ve'), ('O-', 'O-ve'), ('AB-', 'AB-ve')
    ], string='Blood Group')
    gender = fields.Selection([
        ('male', 'Male'), ('female', 'Female')
    ], 'Gender', required=True)
    nationality = fields.Many2one('res.country', 'Nationality')
    active = fields.Boolean(default=True)
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
