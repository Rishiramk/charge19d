# -*- coding: utf-8 -*-
from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    first_name = fields.Char("First Name")
    middle_name = fields.Char("Middle Name")
    last_name = fields.Char("Last Name")

    # Make name a computed field that is stored and has an inverse
    name = fields.Char(index=True, compute='_compute_name', inverse='_inverse_name', store=True)

    @api.depends('first_name', 'middle_name', 'last_name')
    def _compute_name(self):
        """ Computes the full name from the parts. """
        for partner in self:
            parts = [partner.first_name, partner.middle_name, partner.last_name]
            partner.name = ' '.join(p for p in parts if p)

    def _inverse_name(self):
        """ Attempts to split the full name back into parts. """
        for partner in self:
            if not partner.name:
                partner.first_name = ''
                partner.middle_name = ''
                partner.last_name = ''
                continue

            parts = partner.name.strip().split(' ', 2)
            partner.first_name = parts[0]
            if len(parts) > 2:
                partner.middle_name = parts[1]
                partner.last_name = parts[2]
            elif len(parts) > 1:
                partner.middle_name = ''
                partner.last_name = parts[1]
            else:
                partner.middle_name = ''
                partner.last_name = ''