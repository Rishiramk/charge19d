from odoo import models, api

class Student(models.Model):
    _inherit = "op.student"

    def action_create_user(self):
        """
        Create Odoo User linked with Student.

        This method follows a two-step process to comply with Odoo's
        security requirements for user creation:
        1. Create the user with basic details.
        2. Assign the appropriate security group in a separate write call.
        """
        for student in self:
            if not student.user_id:
                user_vals = {
                    'name': student.name,
                    'login': student.email or student.name.lower().replace(" ", "."),
                    'email': student.email,
                }
                # Step 1: Create the user without groups_id
                user = self.env['res.users'].create(user_vals)
                student.user_id = user.id

                # Step 2: Assign the group after creation
                student_group = self.env.ref('charge_erp_core.group_op_student')
                student_group.users = [(4, user.id)]
