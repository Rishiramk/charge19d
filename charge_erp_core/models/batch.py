# -*- coding: utf-8 -*-

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

class OpBatch(models.Model):
    _name = "op.batch"
    _description = "Batch"

    name = fields.Char('Name', size=32, required=True)
    code = fields.Char('Code', size=16, required=True)
    start_date = fields.Date(
        'Start Date', required=True, default=fields.Date.today())
    end_date = fields.Date('End Date', required=True)
    course_id = fields.Many2one('op.course', 'Course', required=True)
    program_id = fields.Many2one('op.program', 'Program', required=True)
    academic_year_id = fields.Many2one(
        'op.academic.year', 'Academic Year', required=True)
    coordinator_id = fields.Many2one('op.faculty', string='Coordinator')
    student_ids = fields.One2many('op.student', 'batch_id', string='Students')
    active = fields.Boolean(default=True)

    @api.constrains('code')
    def _check_unique_code(self):
        for batch in self:
            if batch.code:
                domain = [('code', '=', batch.code), ('id', '!=', batch.id)]
                if self.search_count(domain):
                    raise ValidationError(_('Batch Code must be unique!'))

    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        for record in self:
            if record.start_date and record.end_date and record.start_date > record.end_date:
                raise ValidationError(
                    _("End Date cannot be set before Start Date."))
