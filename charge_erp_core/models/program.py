# -*- coding: utf-8 -*-

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

class OpProgram(models.Model):
    _name = "op.program"
    _description = "Program"

    name = fields.Char('Name', required=True, translate=True)
    code = fields.Char('Code', size=16, required=True, translate=True)
    max_unit_load = fields.Float("Maximum Unit Load")
    min_unit_load = fields.Float("Minimum Unit Load")
    active = fields.Boolean(default=True)
    image_1920 = fields.Image('Image', attachment=True)
    department_id = fields.Many2one('op.department', string='Department')
    program_level_id = fields.Many2one(
        'op.program.level', 'Program Level', required=True)
    batch_ids = fields.One2many('op.batch', 'program_id', string='Batches')
    batch_count = fields.Integer(string='Batch Count', compute='_compute_batch_count')

    def _compute_batch_count(self):
        for program in self:
            program.batch_count = len(program.batch_ids)

    @api.constrains('name', 'code')
    def _check_unique_name_code(self):
        for program in self:
            if self.search_count([('name', '=', program.name), ('id', '!=', program.id)]):
                raise ValidationError(_('The Program Name must be unique.'))
            if self.search_count([('code', '=', program.code), ('id', '!=', program.id)]):
                raise ValidationError(_('The Program Code must be unique.'))
