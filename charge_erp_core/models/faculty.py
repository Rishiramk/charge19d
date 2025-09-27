# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

class OpFaculty(models.Model):
    _name = "op.faculty"
    _description = "Faculty"
    _inherits = {'res.partner': 'partner_id'}

    partner_id = fields.Many2one(
        'res.partner', string='Partner', required=True, ondelete='cascade'
    )

    first_name = fields.Char('First Name', required=True)
    middle_name = fields.Char('Middle Name')
    last_name = fields.Char('Last Name', required=True)

    name = fields.Char(
        compute='_compute_name',
        store=True,
        readonly=False,
    )

    birth_date = fields.Date('Birth Date', required=True)
    blood_group = fields.Selection([
        ('A+', 'A+ve'), ('B+', 'B+ve'), ('O+', 'O+ve'), ('AB+', 'AB+ve'),
        ('A-', 'A-ve'), ('B-', 'B-ve'), ('O-', 'O-ve'), ('AB-', 'AB-ve')
    ], string='Blood Group')
    gender = fields.Selection([
        ('male', 'Male'), ('female', 'Female')
    ], 'Gender', required=True)
    department_id = fields.Many2one('op.department', string='Department')
    program_id = fields.Many2one('op.program', string='Program')
    subject_ids = fields.Many2many('op.subject', string='Subjects')

    session_ids = fields.Many2many(
        'op.session', 'op_session_faculty_rel', 'faculty_id', 'session_id', string="Sessions")
    session_count = fields.Integer(string='Session Count', compute='_compute_session_count')

    def _compute_session_count(self):
        for faculty in self:
            faculty.session_count = len(faculty.session_ids)

    @api.depends('first_name', 'middle_name', 'last_name')
    def _compute_name(self):
        for record in self:
            parts = [record.first_name, record.middle_name, record.last_name]
            record.name = " ".join(filter(None, parts)) or _("Unnamed Faculty")

    @api.constrains('birth_date')
    def _check_birthdate(self):
        for record in self:
            if record.birth_date and record.birth_date > fields.Date.today():
                raise ValidationError(_("Birth Date can't be greater than current date!"))

    # 🔑 Ensure partner.name is always filled at creation
    @api.model
    def create(self, vals):
        # Build a name if not explicitly given
        fname = vals.get("first_name") or ""
        mname = vals.get("middle_name") or ""
        lname = vals.get("last_name") or ""
        full_name = " ".join(filter(None, [fname, mname, lname])) or _("Unnamed Faculty")

        # inject into partner
        if "partner_id" not in vals:
            partner_vals = {
                "name": full_name,
                "is_company": False,
            }
            partner = self.env["res.partner"].create(partner_vals)
            vals["partner_id"] = partner.id
        else:
            # if partner exists but no name set, force update
            partner = self.env["res.partner"].browse(vals["partner_id"])
            if not partner.name:
                partner.name = full_name

        return super(OpFaculty, self).create(vals)
