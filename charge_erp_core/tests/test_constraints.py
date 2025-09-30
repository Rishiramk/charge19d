# -*- coding: utf-8 -*-

from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError

class TestConstraints(TransactionCase):

    def setUp(self):
        super(TestConstraints, self).setUp()
        # Here we will set up some initial data for our tests
        self.Student = self.env['op.student']
        self.Course = self.env['op.course']
        self.Batch = self.env['op.batch']
        self.Department = self.env['op.department']
        self.Subject = self.env['op.subject']
        self.AcademicYear = self.env['op.academic.year']
        self.Session = self.env['op.session']

        # Demo data can be used or created here
        # Common records for tests
        self.course = self.Course.create({'name': 'B.Sc. Computer Science', 'code': 'BCOMP'})
        self.academic_year = self.AcademicYear.create({
            'name': '2025-2026',
            'start_date': '2025-08-01',
            'end_date': '2026-05-31'
        })
        self.program_level = self.env['op.program.level'].create({'name': 'Bachelors'})
        self.program = self.env['op.program'].create({
            'name': 'Bachelor of Science',
            'code': 'BSC',
            'program_level_id': self.program_level.id
        })
        self.demo_student = self.Student.create({
            'first_name': 'John',
            'last_name': 'Doe',
            'roll_number': 'S001',
            'registration_number': 'R001',
        })

    def test_student_uniqueness(self):
        """Test that roll_number and registration_number are unique."""
        with self.assertRaisesRegex(ValidationError, "Roll Number must be unique!"):
            self.Student.create({
                'first_name': 'Jane', 'last_name': 'Doe', 'roll_number': 'S001'})

        with self.assertRaisesRegex(ValidationError, "Registration Number must be unique!"):
            self.Student.create({
                'first_name': 'Jane', 'last_name': 'Smith', 'registration_number': 'R001'})

    def test_course_uniqueness(self):
        """Test that course code is unique."""
        with self.assertRaisesRegex(ValidationError, "Course Code must be unique!"):
            self.Course.create({'name': 'Another Course', 'code': 'BCOMP'})

    def test_batch_constraints(self):
        """Test batch code uniqueness and date validation."""
        self.Batch.create({
            'name': 'CS Batch 1', 'code': 'CSB1', 'start_date': '2025-09-01',
            'end_date': '2026-05-31', 'course_id': self.course.id,
            'program_id': self.program.id, 'academic_year_id': self.academic_year.id
        })
        with self.assertRaisesRegex(ValidationError, "Batch Code must be unique!"):
            self.Batch.create({
                'name': 'CS Batch 2', 'code': 'CSB1', 'start_date': '2025-09-01',
                'end_date': '2026-05-31', 'course_id': self.course.id,
                'program_id': self.program.id, 'academic_year_id': self.academic_year.id
            })
        with self.assertRaisesRegex(ValidationError, "End Date cannot be set before Start Date"):
            self.Batch.create({
                'name': 'CS Batch 3', 'code': 'CSB3', 'start_date': '2026-01-01',
                'end_date': '2025-12-31', 'course_id': self.course.id,
                'program_id': self.program.id, 'academic_year_id': self.academic_year.id
            })

    def test_session_duration(self):
        """Test that session duration cannot be negative."""
        with self.assertRaisesRegex(ValidationError, "The duration cannot be negative"):
            self.Session.create({
                'name': 'Negative Duration Session', 'course_id': self.course.id, 'duration': -10})

    def test_phone_validation(self):
        """Test phone and mobile number validation."""
        with self.assertRaisesRegex(ValidationError, "Phone number can only contain"):
            self.Student.create({'first_name': 'Test', 'last_name': 'User', 'phone': 'abcde'})
        with self.assertRaisesRegex(ValidationError, "Mobile number can only contain"):
            self.Student.create({'first_name': 'Test2', 'last_name': 'User2', 'mobile': 'fghij'})
        # Check that a valid number does not raise an error
        self.Student.create({
            'first_name': 'Valid', 'last_name': 'Student', 'phone': '+1 (555) 123-4567'})

    def test_academic_year_dates(self):
        """Test that academic year end_date is after start_date."""
        with self.assertRaisesRegex(ValidationError, "End Date cannot be set before Start Date"):
            self.AcademicYear.create({
                'name': 'Invalid Year', 'start_date': '2026-01-01', 'end_date': '2025-12-31'})