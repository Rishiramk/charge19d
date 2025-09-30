# -*- coding: utf-8 -*-

from odoo import _, models, fields, api
from odoo.exceptions import ValidationError

class OpSubject(models.Model):
    """
    Represents an academic subject that can be taught as part of a course.
    Each subject has a unique code and can be classified by type (e.g., theory,
    practical) and its role in the curriculum (e.g., compulsory, elective).
    """
    _name = "op.subject"
    _description = "Subject"

    name = fields.Char('Name', size=128, required=True)
    code = fields.Char('Code', size=256, required=True)
    grade_weightage = fields.Float('Grade Weightage')
    type = fields.Selection(
        [('theory', 'Theory'), ('practical', 'Practical'),
         ('both', 'Both'), ('other', 'Other')],
        'Type', default="theory", required=True)
    subject_type = fields.Selection(
        [('compulsory', 'Compulsory'), ('elective', 'Elective')],
        'Subject Type', default="compulsory", required=True)
    department_id = fields.Many2one('op.department', string='Department')
    active = fields.Boolean(default=True)
    faculty_ids = fields.Many2many(
        'op.faculty', 'op_faculty_subject_rel',
        'subject_id', 'faculty_id', string='Faculties')

    @api.constrains('code')
    def _check_unique_code(self):
        """Ensures that the subject code is unique across all subjects."""
        for subject in self:
            if subject.code:
                domain = [('code', '=', subject.code), ('id', '!=', subject.id)]
                if self.search_count(domain):
                    raise ValidationError(_('Subject Code must be unique!'))
