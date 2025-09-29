# -*- coding: utf-8 -*-
from odoo import models, fields

class OpBookIssue(models.Model):
    _name = 'op.book.issue'
    _description = 'Book Issue'

    name = fields.Char('Book Title', required=True)
    faculty_id = fields.Many2one('op.faculty', 'Faculty')
    student_id = fields.Many2one('op.student', 'Student')
    issue_date = fields.Date('Issue Date', default=fields.Date.today())
    due_date = fields.Date('Due Date')