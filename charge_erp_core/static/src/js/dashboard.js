/** @odoo-module **/

import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
const { Component, onWillStart, onMounted, useRef } = owl;

export class SchoolDashboard extends Component {
    setup() {
        this.orm = useService("orm");
        this.rpc = useService("rpc");

        this.kpiData = {};
        this.studentsByDept = {};
        this.facultyByDept = {};

        this.studentsChartRef = useRef("studentsByDepartmentChart");
        this.facultyChartRef = useRef("facultyByDepartmentChart");

        onWillStart(async () => {
            await this.fetchData();
        });

        onMounted(() => {
            this.renderCharts();
        });
    }

    async fetchData() {
        this.kpiData = await this.rpc("/charge_erp/kpi_data");
        this.studentsByDept = await this.rpc("/charge_erp/students_by_department");
        this.facultyByDept = await this.rpc("/charge_erp/faculty_by_department");
    }

    renderCharts() {
        // Students by Department Bar Chart
        new Chart(this.studentsChartRef.el, {
            type: 'bar',
            data: {
                labels: this.studentsByDept.labels,
                datasets: [{
                    label: 'Number of Students',
                    data: this.studentsByDept.data,
                    backgroundColor: 'rgba(54, 162, 235, 0.6)',
                    borderColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });

        // Faculty by Department Pie Chart
        new Chart(this.facultyChartRef.el, {
            type: 'pie',
            data: {
                labels: this.facultyByDept.labels,
                datasets: [{
                    label: 'Number of Faculty',
                    data: this.facultyByDept.data,
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.6)',
                        'rgba(54, 162, 235, 0.6)',
                        'rgba(255, 206, 86, 0.6)',
                        'rgba(75, 192, 192, 0.6)',
                        'rgba(153, 102, 255, 0.6)',
                        'rgba(255, 159, 64, 0.6)'
                    ],
                }]
            }
        });
    }
}

SchoolDashboard.template = "charge_erp_core.dashboard";

registry.category("actions").add("charge_erp_core.dashboard", SchoolDashboard);