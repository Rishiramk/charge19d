# -*- coding: utf-8 -*-
from odoo import http, fields
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal


class StudentPortal(CustomerPortal):

    def _get_student(self):
        """Helper to get the student record for the current user."""
        return request.env['op.student'].search([
            ('user_id', '=', request.env.user.id)
        ], limit=1)

    def _get_faculty(self):
        """Helper to get the faculty record for the current user."""
        return request.env['op.faculty'].search([
            ('user_id', '=', request.env.user.id)
        ], limit=1)

    @http.route(['/my', '/my/home'], type='http', auth="user", website=True)
    def home(self, **kw):
        """
        Overrides the default portal homepage to render the new, enhanced
        student dashboard.

        This single method fetches all data required for the dashboard
        cards and passes it to the custom QWeb template.
        """
        values = self._prepare_portal_layout_values()

        student = self._get_student()
        faculty = self._get_faculty()

        if student:
            # Fetch enrolled courses
            courses = request.env['op.course.enrollment'].search([('student_id', '=', student.id)]).mapped('course_id')

            # Fetch the next 5 upcoming sessions
            sessions = request.env['op.session'].search([
                ('attendee_ids', 'in', [student.id]),
                ('start_datetime', '>=', fields.Datetime.now())
            ], order='start_datetime asc', limit=5)

            # Fetch issued library books
            issued_books = request.env['op.book.issue'].search([('student_id', '=', student.id)])

            values.update({
                'student': student,
                'courses': courses,
                'sessions': sessions,
                'issued_books': issued_books,
            })

        elif faculty:
            # Fallback for faculty users, can be enhanced later
            courses = request.env['op.course'].search([('faculty_ids', 'in', [faculty.id])])
            sessions = request.env['op.session'].search([('faculty_id', '=', faculty.id)])
            issued_books = request.env['op.book.issue'].search([('faculty_id', '=', faculty.id)])

            values.update({
                'faculty': faculty,
                'courses': courses,
                'sessions': sessions,
                'issued_books': issued_books,
            })

        return request.render("charge_erp_core.portal_student_dashboard", values)