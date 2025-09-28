# -*- coding: utf-8 -*-

from odoo import models, fields
from odoo.models import Constraint

class OpProgramLevel(models.Model):
    _name = "op.program.level"
    _description = "Program Level"

    name = fields.Char('Name', required=True, translate=True)

    _constraints = [
        Constraint('unique_level_name', 'unique(name)', 'Name should be unique per Program level!')
    ]
