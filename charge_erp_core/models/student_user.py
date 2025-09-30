from odoo import models, api

class Student(models.Model):
    _inherit = "op.student"

    def action_create_user(self):
        """Create Odoo User linked with Student"""
        for student in self:
            if not student.user_id:
                user_vals = {
                    'name': student.name,
                    'login': student.email or student.name.lower().replace(" ", "."),
                    'groups_id': [(6, 0, [self.env.ref('charge_erp_core.group_op_student').id])],
                }
                user = self.env['res.users'].create(user_vals)
                student.user_id = user.id

