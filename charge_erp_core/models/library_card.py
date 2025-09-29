# -*- coding: utf-8 -*-
from odoo import models, fields

class OpLibraryCard(models.Model):
    _name = 'op.library.card'
    _description = 'Library Card'
    _rec_name = 'name'

    name = fields.Char('Card Number', required=True)
    faculty_id = fields.Many2one('op.faculty', 'Faculty')
    student_id = fields.Many2one('op.student', 'Student')