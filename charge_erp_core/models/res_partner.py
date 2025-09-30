# -*- coding: utf-8 -*-
import re
from odoo import _, models, fields, api
from odoo.exceptions import ValidationError

class ResPartner(models.Model):
    _inherit = "res.partner"

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

    @api.constrains('phone', 'mobile')
    def _check_phone_numbers(self):
        for partner in self:
            if partner.phone and not re.match(r'^[0-9\s+-]*$', partner.phone):
                raise ValidationError(
                    _("Phone number can only contain digits, spaces, '+', or '-'."))
            if partner.mobile and not re.match(r'^[0-9\s+-]*$', partner.mobile):
                raise ValidationError(
                    _("Mobile number can only contain digits, spaces, '+', or '-'."))