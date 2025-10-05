# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager


class SchoolPortal(CustomerPortal):

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

    def _prepare_portal_layout_values(self):
        values = super()._prepare_portal_layout_values()
        student = self._get_student()
        faculty = self._get_faculty()

        course_count = 0
        session_count = 0
        library_count = 0

        if student:
            course_count = request.env['op.course.enrollment'].search_count([('student_id', '=', student.id)])
            session_count = request.env['op.session'].search_count([('student_ids', 'in', [student.id])])
            library_count = request.env['op.book.issue'].search_count([('student_id', '=', student.id), ('state', '=', 'issue')])
        elif faculty:
            course_count = request.env['op.course'].search_count([('faculty_ids', 'in', [faculty.id])])
            session_count = request.env['op.session'].search_count([('faculty_id', '=', faculty.id)])
            library_count = request.env['op.book.issue'].search_count([('faculty_id', '=', faculty.id), ('state', '=', 'issue')])

        values.update({
            'course_count': course_count,
            'schedule_count': session_count,
            'library_count': library_count,
        })
        return values

    @http.route(['/my/profile'], type='http', auth="user", website=True)
    def portal_my_profile(self, **kw):
        student = self._get_student()
        faculty = self._get_faculty()

        if not student and not faculty:
            return request.redirect('/my')

        values = {
            'student': student,
            'faculty': faculty,
            'page_name': 'profile',
        }
        return request.render("charge_erp_core.portal_my_profile", values)

    @http.route(['/my/courses', '/my/courses/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_courses(self, page=1, **kw):
        student = self._get_student()
        faculty = self._get_faculty()

        if student:
            domain = [('student_id', '=', student.id)]
            enrollments = request.env['op.course.enrollment'].search(domain)
            courses = enrollments.mapped('course_id')
        elif faculty:
            domain = [('faculty_ids', 'in', [faculty.id])]
            courses = request.env['op.course'].search(domain)
        else:
            return request.redirect('/my')

        pager = portal_pager(
            url="/my/courses",
            total=len(courses),
            page=page,
            step=self._items_per_page
        )

        offset = pager['offset']
        courses = courses[offset: offset + self._items_per_page]

        values = self._prepare_portal_layout_values()
        values.update({
            'courses': courses,
            'page_name': 'courses',
            'pager': pager,
        })
        return request.render("charge_erp_core.portal_my_courses", values)

    @http.route(['/my/schedule', '/my/schedule/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_schedule(self, page=1, **kw):
        student = self._get_student()
        faculty = self._get_faculty()

        if student:
            domain = [('student_ids', 'in', [student.id])]
        elif faculty:
            domain = [('faculty_id', '=', faculty.id)]
        else:
            return request.redirect('/my')

        session_count = request.env['op.session'].search_count(domain)
        pager = portal_pager(
            url="/my/schedule",
            total=session_count,
            page=page,
            step=self._items_per_page
        )

        sessions = request.env['op.session'].search(domain, limit=self._items_per_page, offset=pager['offset'])

        values = self._prepare_portal_layout_values()
        values.update({
            'sessions': sessions,
            'page_name': 'schedule',
            'pager': pager,
        })
        return request.render("charge_erp_core.portal_my_schedule", values)

    @http.route(['/my/library', '/my/library/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_library(self, page=1, **kw):
        student = self._get_student()
        faculty = self._get_faculty()

        if student:
            domain = [('student_id', '=', student.id), ('state', '=', 'issue')]
        elif faculty:
            domain = [('faculty_id', '=', faculty.id), ('state', '=', 'issue')]
        else:
            return request.redirect('/my')

        library_count = request.env['op.book.issue'].search_count(domain)
        pager = portal_pager(
            url="/my/library",
            total=library_count,
            page=page,
            step=self._items_per_page
        )

        issued_books = request.env['op.book.issue'].search(domain, limit=self._items_per_page, offset=pager['offset'])

        values = self._prepare_portal_layout_values()
        values.update({
            'issued_books': issued_books,
            'page_name': 'library',
            'pager': pager,
        })
        return request.render("charge_erp_core.portal_my_library", values)