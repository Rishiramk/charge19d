# -*- coding: utf-8 -*-
from odoo import models, fields, api

class OpCourseEnrollment(models.Model):
    _name = 'op.course.enrollment'
    _description = 'Course Enrollment'
    _rec_name = 'name'

    name = fields.Char(string='Name', compute='_compute_name', store=True)
    student_id = fields.Many2one('op.student', string='Student', required=True)
    course_id = fields.Many2one('op.course', string='Course', required=True)
    academic_year_id = fields.Many2one('op.academic.year', string='Academic Year', required=True)
    status = fields.Selection([
        ('enrolled', 'Enrolled'),
        ('dropped', 'Dropped'),
        ('completed', 'Completed')
    ], string='Status', default='enrolled', required=True)

    @api.depends('student_id', 'course_id')
    def _compute_name(self):
        for enrollment in self:
            if enrollment.student_id and enrollment.course_id:
                enrollment.name = f"{enrollment.student_id.name} - {enrollment.course_id.name}"
            else:
                enrollment.name = "New Enrollment"