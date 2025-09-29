# -*- coding: utf-8 -*-
from odoo import models, fields

class OpHealthDetails(models.Model):
    _name = 'op.health.details'
    _description = 'Health Details'

    name = fields.Char('Condition', required=True)
    faculty_id = fields.Many2one('op.faculty', 'Faculty')
    student_id = fields.Many2one('op.student', 'Student')
    medical_conditions = fields.Text('Medical Conditions')
    allergies = fields.Text('Allergies')
    emergency_instructions = fields.Text('Emergency Instructions')