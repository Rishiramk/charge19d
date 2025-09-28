# -*- coding: utf-8 -*-

from odoo import fields, models

class OpAcademicYear(models.Model):
    _name = 'op.academic.year'
    _description = "Academic Year"

    _sql_constraints = [
        ('name_unique', 'unique(name)', 'Academic Year Name must be unique!'),
    ]

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
