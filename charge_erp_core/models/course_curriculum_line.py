# -*- coding: utf-8 -*-
from odoo import models, fields

class OpCourseCurriculumLine(models.Model):
    _name = 'op.course.curriculum.line'
    _description = 'Course Curriculum Line'
    _rec_name = 'subject_id'

    course_id = fields.Many2one('op.course', string='Course', required=True)
    subject_id = fields.Many2one('op.subject', string='Subject', required=True)
    semester = fields.Integer(string='Semester', required=True)
    type = fields.Selection([
        ('compulsory', 'Compulsory'),
        ('elective', 'Elective')
    ], string='Type', default='compulsory', required=True)