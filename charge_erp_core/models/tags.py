# -*- coding: utf-8 -*-

from odoo import fields, models

class OpTags(models.Model):
    _name = 'op.tags'
    _description = 'Student Tags'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')