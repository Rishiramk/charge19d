# -*- coding: utf-8 -*-
from odoo import models, fields

class OpStudentSubjectEnrollment(models.Model):
    _name = 'op.student.subject.enrollment'
    _description = 'Student Subject Enrollment'
    _rec_name = 'student_id'

    student_id = fields.Many2one('op.student', string='Student', required=True)
    subject_id = fields.Many2one('op.subject', string='Subject', required=True)
    academic_term_id = fields.Many2one('op.academic.term', string='Academic Term', required=True)
    status = fields.Selection([
        ('enrolled', 'Enrolled'),
        ('dropped', 'Dropped'),
        ('completed', 'Completed'),
        ('failed', 'Failed')
    ], string='Status', default='enrolled', required=True)