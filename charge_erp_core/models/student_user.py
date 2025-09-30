from odoo import models, api

class Student(models.Model):
    _inherit = "op.student"

    def action_create_user(self):
        """
        Create a portal user linked to the Student record.
        """
        for student in self:
            if not student.user_id:
                user_vals = {
                    'name': student.name,
                    'login': student.email or student.name.lower().replace(" ", "."),
                    'email': student.email,
                    'partner_id': student.partner_id.id,
                }
                # Step 1: Create the user
                user = self.env['res.users'].create(user_vals)
                student.user_id = user.id

                # Step 2: Assign the student group to the user
                student_group = self.env.ref('charge_erp_core.group_op_student')
                user.write({'groups_id': [(4, student_group.id)]})

                # Optional: assign portal access
                portal_group = self.env.ref('base.group_portal')
                user.write({'groups_id': [(4, portal_group.id)]})
