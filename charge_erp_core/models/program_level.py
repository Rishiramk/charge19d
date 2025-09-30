# -*- coding: utf-8 -*-

from odoo import _, api, models, fields
from odoo.exceptions import ValidationError

class OpProgramLevel(models.Model):
    """
    Represents the level of an academic program, such as "Bachelors",
    "Masters", or "Doctorate". This provides a way to categorize programs.
    """
    _name = "op.program.level"
    _description = "Program Level"

    name = fields.Char('Name', required=True, translate=True)

    @api.constrains('name')
    def _check_unique_name(self):
        """Ensures that the program level name is unique."""
        for level in self:
            if level.name:
                domain = [('name', '=', level.name), ('id', '!=', level.id)]
                if self.search_count(domain):
                    raise ValidationError(_('Program Level name must be unique!'))
