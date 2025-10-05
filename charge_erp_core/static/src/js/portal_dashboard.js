/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component, onMounted, useRef } from "@odoo/owl";
import { loadJS } from "@web/core/assets";

class AcademicChart extends Component {
    static template = "charge_erp_core.AcademicChart";

    setup() {
        this.chart = null;
        this.chartRef = useRef("academicChart");

        onMounted(async () => {
            await loadJS("/web/static/lib/Chart/Chart.js");
            this.renderChart();
        });
    }

    renderChart() {
        // Placeholder data - this should be fetched from the server
        const data = {
            labels: ['CS101', 'HIST101', 'PHY101', 'DS501', 'CHEM101'],
            datasets: [{
                label: 'Your Grades',
                data: [85, 92, 78, 88, 95],
                backgroundColor: 'rgba(54, 162, 235, 0.2)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 2,
                tension: 0.4,
                fill: true,
            }]
        };

        const config = {
            type: 'radar', // Using a radar chart as inspired by the design
            data: data,
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false,
                    },
                },
                scales: {
                    r: {
                        angleLines: {
                            display: true,
                        },
                        suggestedMin: 50,
                        suggestedMax: 100,
                    },
                },
            },
        };

        this.chart = new Chart(this.chartRef.el, config);
    }
}

registry.category("public_components").add("academic_chart", AcademicChart);