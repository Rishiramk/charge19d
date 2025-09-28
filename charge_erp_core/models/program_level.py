# -*- coding: utf-8 -*-

from odoo import models, fields, _
from odoo.models import Constraint

class OpProgramLevel(models.Model):
    _name = "op.program.level"
    _description = "Program Level"

    name = fields.Char('Name', required=True, translate=True)

    _constraints = [
        Constraint(
            name="unique_level_name",
            type="unique",
            fields=["name"],
            message=_("Name should be unique per Program level!"),
        )
    ]
