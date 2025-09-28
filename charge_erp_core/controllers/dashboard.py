# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request

class DashboardController(http.Controller):

    @http.route('/charge_erp/kpi_data', type='json', auth='user')
    def get_kpi_data(self):
        """
        Provides data for the main KPI boxes on the dashboard.
        """
        student_count = request.env['op.student'].search_count([('status', '=', 'active')])
        faculty_count = request.env['op.faculty'].search_count([])
        course_count = request.env['op.course'].search_count([('active', '=', True)])

        return {
            'total_students': student_count,
            'total_faculty': faculty_count,
            'total_courses': course_count,
        }

    @http.route('/charge_erp/students_by_department', type='json', auth='user')
    def get_students_by_department(self):
        """
        Provides data for the 'Students by Department' bar chart.
        """
        # We group by the department linked through the program
        student_groups = request.env['op.student'].read_group(
            [('program_id.department_id', '!=', False)],
            ['program_id'],
            ['program_id']
        )

        # We need to process this to group by department, not program
        department_map = {}
        for group in student_groups:
            program = request.env['op.program'].browse(group['program_id'][0])
            department_name = program.department_id.name
            if department_name not in department_map:
                department_map[department_name] = 0
            department_map[department_name] += group['program_id_count']

        return {
            'labels': list(department_map.keys()),
            'data': list(department_map.values()),
        }

    @http.route('/charge_erp/faculty_by_department', type='json', auth='user')
    def get_faculty_by_department(self):
        """
        Provides data for the 'Faculty by Department' pie chart.
        """
        faculty_groups = request.env['op.faculty'].read_group(
            [('department_id', '!=', False)],
            ['department_id'],
            ['department_id']
        )
        return {
            'labels': [g['department_id'][1] for g in faculty_groups],
            'data': [g['department_id_count'] for g in faculty_groups],
        }