# -*- coding: utf-8 -*-
from odoo import models, fields

class OpStudentCourse(models.Model):
    _name = 'op.student.course'
    _description = 'Student Course'

    student_id = fields.Many2one('op.student', string='Student', required=True)
    course_id = fields.Many2one('op.course', string='Course', required=True)
    academic_year_id = fields.Many2one('op.academic.year', string='Academic Year', required=True)
    status = fields.Selection([
        ('enrolled', 'Enrolled'),
        ('dropped', 'Dropped'),
        ('completed', 'Completed')
    ], string='Status', default='enrolled', required=True)