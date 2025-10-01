from odoo import models

class Student(models.Model):
    _inherit = "op.student"

    def action_create_user(self):
        for student in self:
            if not student.user_id:
                # 1. Create the user record
                user_vals = {
                    'name': student.name,
                    'login': student.email or student.name.lower().replace(" ", "."),
                    'email': student.email,
                    'partner_id': student.partner_id.id,
                }
                user = self.env['res.users'].sudo().create(user_vals)
                student.user_id = user.id

                # 2. Grant portal access. This is the correct and safe way
                # to create a portal user in Odoo 19.
                user.sudo().write({'share': True})