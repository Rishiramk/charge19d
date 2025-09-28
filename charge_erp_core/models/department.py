# -*- coding: utf-8 -*-

from odoo import api, fields, models

class OpDepartment(models.Model):
    _name = "op.department"
    _description = "Department"

    name = fields.Char('Name', required=True)
    code = fields.Char('Code', required=True)
    parent_id = fields.Many2one('op.department', 'Parent Department')
    course_ids = fields.One2many('op.course', 'department_id', string='Courses')
    course_count = fields.Integer(string='Course Count', compute='_compute_course_count')

    def _compute_course_count(self):
        for department in self:
            department.course_count = len(department.course_ids)

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