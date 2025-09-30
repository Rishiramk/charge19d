from odoo import models

class Student(models.Model):
    _inherit = "op.student"

    def action_create_user(self):
        for student in self:
            if not student.user_id:
                user_vals = {
                    'name': student.name,
                    'login': student.email or student.name.lower().replace(" ", "."),
                    'email': student.email,
                    'partner_id': student.partner_id.id,
                }
                user = self.env['res.users'].sudo().create(user_vals)
                student.user_id = user.id

                # Assign student group
                student_group = self.env.ref('charge_erp_core.group_op_student')
                user.sudo().write({'groups_id': [(4, student_group.id)]})

                # Optional: assign portal access
                portal_group = self.env.ref('base.group_portal')
                user.sudo().write({'groups_id': [(4, portal_group.id)]})
