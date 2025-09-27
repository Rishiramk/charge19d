# -*- coding: utf-8 -*-
from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = "res.partner"

    first_name = fields.Char("First Name")
    last_name = fields.Char("Last Name")
    middle_name = fields.Char("Middle Name")

    @api.depends('first_name', 'middle_name', 'last_name')
    def _compute_name(self):
        for rec in self:
            parts = [rec.first_name, rec.middle_name, rec.last_name]
            rec.name = " ".join(p for p in parts if p)

    # Re-defining the name field to be computed and stored
    name = fields.Char(compute="_compute_name", store=True, readonly=False)