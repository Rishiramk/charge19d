# -*- coding: utf-8 -*-

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

class OpDepartment(models.Model):
    """
    Represents an academic department within the institution, which can be
    linked to courses, faculties, and subjects.
    """
    _name = "op.department"
    _description = "Department"

    name = fields.Char('Name', required=True)
    code = fields.Char('Code', required=True)
    parent_id = fields.Many2one('op.department', 'Parent Department')

    # Relational Fields
    course_ids = fields.One2many('op.course', 'department_id', string='Courses')
    faculty_ids = fields.One2many('op.faculty', 'department_id', string='Faculties')
    subject_ids = fields.One2many('op.subject', 'department_id', string='Subjects')

    # Count Fields
    course_count = fields.Integer(string='Course Count', compute='_compute_course_count')
    faculty_count = fields.Integer(string='Faculty Count', compute='_compute_faculty_count')
    student_count = fields.Integer(string='Student Count', compute='_compute_student_count')
    subject_count = fields.Integer(string='Subject Count', compute='_compute_subject_count')
    batch_count = fields.Integer(string='Batch Count', compute='_compute_batch_count')

    def _compute_course_count(self):
        for department in self:
            department.course_count = len(department.course_ids)

    def _compute_faculty_count(self):
        for department in self:
            department.faculty_count = len(department.faculty_ids)

    def _compute_subject_count(self):
        for department in self:
            department.subject_count = len(department.subject_ids)

    def _compute_student_count(self):
        for department in self:
            programs = self.env['op.program'].search([('department_id', '=', department.id)])
            department.student_count = self.env['op.student'].search_count([('program_id', 'in', programs.ids)])

    def _compute_batch_count(self):
        for department in self:
            programs = self.env['op.program'].search([('department_id', '=', department.id)])
            department.batch_count = self.env['op.batch'].search_count([('program_id', 'in', programs.ids)])

    @api.constrains('code')
    def _check_unique_code(self):
        """Ensures that the department code is unique."""
        for department in self:
            if department.code:
                domain = [('code', '=', department.code), ('id', '!=', department.id)]
                if self.search_count(domain):
                    raise ValidationError(_('Department Code must be unique!'))

    @api.model
    def create(self, vals_list):
        """
        Overrides the create method to handle a list of creation values.
        It auto-generates a department code from the name if it's not provided.
        """
        for vals in vals_list:
            if vals.get('name') and not vals.get('code'):
                name = vals.get('name')
                # A simple way to generate a code: take the first letter of each word.
                vals['code'] = ''.join(word[0] for word in name.split()).upper()
        return super(OpDepartment, self).create(vals_list)