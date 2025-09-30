# -*- coding: utf-8 -*-

from odoo import _, api, models, fields
from odoo.exceptions import ValidationError

class OpProgram(models.Model):
    """
    Represents an academic program, such as a Bachelor of Science or Master
    of Arts. It groups together related courses and batches under a single
    academic track.
    """
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

    @api.constrains('code')
    def _check_unique_code(self):
        """Ensures that the program code is unique."""
        for program in self:
            if program.code:
                domain = [('code', '=', program.code), ('id', '!=', program.id)]
                if self.search_count(domain):
                    raise ValidationError(_('Program Code must be unique!'))
