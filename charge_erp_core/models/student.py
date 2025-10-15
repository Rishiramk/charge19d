# -*- coding: utf-8 -*-
from odoo import _, models, fields, api
from odoo.exceptions import UserError, ValidationError


class OpStudent(models.Model):
    """
    Represents a student in the system. This model inherits from `res.partner`
    to leverage its contact and address management features, while adding
    student-specific academic and personal information.
    """
    _name = 'op.student'
    _description = 'Student'
    _inherits = {'res.partner': 'partner_id'}

    # Link to res.partner
    partner_id = fields.Many2one(
        'res.partner', string='Partner', required=True, ondelete='cascade'
    )
    image_128 = fields.Image(related='partner_id.image_128', readonly=True)

    # Personal Information
    lang = fields.Selection(related='partner_id.lang', readonly=False)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], string='Gender')
    status = fields.Selection([
        ('active', 'Active'),
        ('graduated', 'Graduated'),
        ('on_leave', 'On Leave')
    ], string='Status', default='active', required=True)
    birth_date = fields.Date(string='Birth Date')
    blood_group = fields.Selection([
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('O+', 'O+'), ('O-', 'O-'),
        ('AB+', 'AB+'), ('AB-', 'AB-')
    ], string='Blood Group')
    nationality = fields.Many2one('res.country', string='Nationality')
    is_an_alumni = fields.Boolean(string='Is an Alumni?')
    id_number = fields.Char(string='ID Card Number')

    # Aadhar Information
    aadhar_number = fields.Char(
        string='Aadhar Number', size=12,
        help='Enter 12-digit Aadhar number')
    aadhar_verified = fields.Boolean(string='Aadhar Verified')
    aadhar_document = fields.Binary(string='Aadhar Document')

    # Contact Information
    address_type = fields.Selection(related='partner_id.type', string="Address Type", readonly=False)
    phone = fields.Char(string='Phone')
    mobile = fields.Char(string='Mobile')
    email = fields.Char(related='partner_id.email', readonly=False)
    street = fields.Char(related='partner_id.street', readonly=False)
    street2 = fields.Char(related='partner_id.street2', readonly=False)
    city = fields.Char(related='partner_id.city', readonly=False)
    state_id = fields.Many2one('res.country.state', related='partner_id.state_id', readonly=False)
    zip = fields.Char(related='partner_id.zip', readonly=False)
    country_id = fields.Many2one('res.country', related='partner_id.country_id', readonly=False)
    emergency_contact_id = fields.Many2one(
        'res.partner', string='Emergency Contact', ondelete='set null')
    parent_ids = fields.Many2many(
        'res.partner', 'op_student_parent_rel', 'student_id', 'parent_id', string='Parents')

    # Other Information
    roll_number = fields.Char(string='Roll Number')
    registration_number = fields.Char(string='Registration Number')
    library_card = fields.Char(string='Library Card')
    badge_id = fields.Char(string='Badge ID')
    category_id = fields.Many2one('op.category', string='Category')
    user_id = fields.Many2one('res.users', string='User')
    batch_id = fields.Many2one('op.batch', string='Batch')
    program_id = fields.Many2one('op.program', string='Program')
    department_id = fields.Many2one(
        'op.department', string='Department',
        related='program_id.department_id', store=True)
    miscellaneous = fields.Text(string='Miscellaneous')
    enrollment_ids = fields.One2many(
        'op.course.enrollment', 'student_id', string='Enrollments')
    session_ids = fields.Many2many(
        'op.session', 'op_session_student_rel', 'student_id', 'session_id', string="Sessions")
    tag_ids = fields.Many2many('op.tags', string='Tags')
    session_count = fields.Integer(string='Session Count', compute='_compute_session_count')
    assignment_count = fields.Integer(string='Assignment Count', compute='_compute_assignment_count')
    fee_due_count = fields.Integer(string='Fee Due Count', compute='_compute_fee_due_count')
    attendance_count = fields.Integer(string='Attendance Count', compute='_compute_attendance_count')
    color = fields.Integer(string='Color', compute='_compute_color')

    @api.constrains('aadhar_number')
    def _check_aadhar_number(self):
        for record in self:
            if record.aadhar_number and (not record.aadhar_number.isdigit() or len(record.aadhar_number) != 12):
                raise ValidationError(_("Aadhar number must be a 12-digit numeric value."))

    @api.constrains('roll_number', 'registration_number')
    def _check_unique_identifiers(self):
        """
        Validates that the roll number and registration number are unique across
        all students in the system.
        """
        for student in self:
            if student.roll_number:
                domain = [('roll_number', '=', student.roll_number), ('id', '!=', student.id)]
                if self.search_count(domain):
                    raise ValidationError(_('Roll Number must be unique!'))
            if student.registration_number:
                domain = [('registration_number', '=', student.registration_number), ('id', '!=', student.id)]
                if self.search_count(domain):
                    raise ValidationError(_('Registration Number must be unique!'))

    def _compute_color(self):
        for student in self:
            if student.status == 'active':
                student.color = 2  # Green
            elif student.status == 'on_leave':
                student.color = 5  # Yellow
            elif student.status == 'graduated':
                student.color = 7  # Red
            else:
                student.color = 0  # Default

    def _compute_session_count(self):
        for student in self:
            student.session_count = len(student.session_ids)

    def _compute_assignment_count(self):
        for student in self:
            student.assignment_count = 0

    def _compute_fee_due_count(self):
        for student in self:
            student.fee_due_count = 0

    def _compute_attendance_count(self):
        for student in self:
            student.attendance_count = 0

    def action_view_assignments(self):
        raise UserError("The 'Assignments' module is not yet installed.")

    def action_view_fees(self):
        raise UserError("The 'Fees' module is not yet installed.")

    def action_view_attendance(self):
        raise UserError("The 'Attendance' module is not yet installed.")

    def action_create_user(self):
        """
        Creates a new portal user for each student in the recordset.
        This method is idempotent and follows Odoo 19 best practices.
        """
        for student in self.filtered(lambda s: not s.user_id):
            # Step 1: Create the user correctly in a single step.
            # Setting 'share': True ensures Odoo creates a portal user,
            # automatically adding them to 'base.group_portal' and
            # removing them from 'base.group_user'.
            user = self.env['res.users'].create({
                'name': student.name,
                'login': student.email or student.name.lower().replace(' ', '.'),
                'partner_id': student.partner_id.id,
                'share': True,
            })

            # Step 2: Add the student-specific application group.
            student_group = self.env.ref('charge_erp_core.group_op_student')
            user.write({'group_ids': [(4, student_group.id)]})

            # Step 3: Link the new user back to the student record.
            student.user_id = user.id
