# -*- coding: utf-8 -*-

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

class OpAcademicYear(models.Model):
    """
    Represents an academic year, defined by a name and a start and end date.
    It serves as a container for academic terms, batches, and other
    time-sensitive records.
    """
    _name = 'op.academic.year'
    _description = "Academic Year"

    name = fields.Char('Name', required=True)
    start_date = fields.Date('Start Date', required=True)
    end_date = fields.Date('End Date', required=True)
    term_structure = fields.Selection([('two_sem', 'Two Semesters'),
                                       ('two_sem_qua', 'Two Semesters subdivided by Quarters'),
                                       ('two_sem_final', 'Two Semesters subdivided by Quarters and Final Exams'),
                                       ('three_sem', 'Three Trimesters'),
                                       ('four_Quarter', 'Four Quarters'),
                                       ('final_year', 'Final Year Grades subdivided by Quarters'),
                                       ('others', 'Other(overlapping terms, custom schedules)')],
                                      string='Term Structure', default='two_sem', required=True)
    academic_term_ids = fields.One2many('op.academic.term', 'academic_year_id', string='Academic Terms')
    batch_ids = fields.One2many('op.batch', 'academic_year_id', string='Batches')
    batch_count = fields.Integer(string='Batch Count', compute='_compute_batch_count')
    active = fields.Boolean(default=True)

    def _compute_batch_count(self):
        for academic_year in self:
            academic_year.batch_count = len(academic_year.batch_ids)

    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        """Validates that the start date is not after the end date."""
        for record in self:
            if record.start_date and record.end_date and record.start_date > record.end_date:
                raise ValidationError(
                    _("End Date cannot be set before Start Date."))
