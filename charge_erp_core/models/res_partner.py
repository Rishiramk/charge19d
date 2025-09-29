# -*- coding: utf-8 -*-
from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = "res.partner"

    title = fields.Many2one('res.partner.title', string='Title')
    first_name = fields.Char("First Name")
    last_name = fields.Char("Last Name")
    middle_name = fields.Char("Middle Name")

    # This is the correct implementation to ensure the name is always computed
    name = fields.Char(compute="_compute_name", store=True, readonly=False)

    @api.depends('first_name', 'middle_name', 'last_name')
    def _compute_name(self):
        """
        Computes the full name from the parts for all records.
        This ensures the name is always set, even for backend creations.
        """
        for rec in self:
            # For companies, the name is not composed of parts.
            # We check if the record is a company and if the name is already set.
            # If so, we don't recompute it from the (empty) parts.
            if rec.is_company and rec.name:
                continue

            parts = [rec.first_name, rec.middle_name, rec.last_name]
            rec.name = " ".join(p for p in parts if p)