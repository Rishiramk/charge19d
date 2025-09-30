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
                # Step 1: Create the user, linking them to the student's partner
                user = self.env['res.users'].create(user_vals)
                student.user_id = user.id

                # Step 2: Assign the student to the portal/student group
                student_group = self.env.ref('charge_erp_core.group_op_student')
                student_group.write({'users': [(4, user.id)]})
