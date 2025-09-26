# -*- coding: utf-8 -*-
from odoo import models, fields

class OpCategory(models.Model):
    _name = 'op.category'
    _description = 'Category'

    name = fields.Char(string='Name', required=True)
    code = fields.Char(string='Code', required=True)