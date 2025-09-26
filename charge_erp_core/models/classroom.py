# -*- coding: utf-8 -*-

from odoo import fields, models

class OpClassroom(models.Model):
    _name = 'op.classroom'
    _description = 'Classroom'

    name = fields.Char(string='Name', required=True)
    capacity = fields.Integer(string='Capacity')
    type = fields.Selection([
        ('lecture', 'Lecture Hall'),
        ('lab', 'Lab'),
        ('online', 'Online')
    ], string='Type', default='lecture', required=True)