# -*- coding: utf-8 -*-
from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    first_name = fields.Char("First Name")
    middle_name = fields.Char("Middle Name")
    last_name = fields.Char("Last Name")

    @api.onchange('first_name', 'middle_name', 'last_name')
    def _onchange_name_parts(self):
        """
        Construct the full name from the name parts, but only for individuals.
        This prevents breaking the logic for company records.
        """
        if self.is_company:
            return

        parts = [self.first_name, self.middle_name, self.last_name]
        self.name = ' '.join(p for p in parts if p)