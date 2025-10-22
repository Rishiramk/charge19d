/*
    Custom JS for the Student Portal Dashboard - V2
    - Author: Jules
    - Version: 2.0
    - Description: This script adds interactivity to the student dashboard,
                 including tab state management and future chart initializations.
*/
odoo.define('charge_erp_core.portal_dashboard', function (require) {
    "use strict";

    var publicWidget = require('web.public.widget');

    publicWidget.registry.StudentDashboard = publicWidget.Widget.extend({
        selector: '.o_portal_my_home',

        /**
         * @override
         */
        start: function () {
            this._super.apply(this, arguments);
            this._initTabs();
            // In the future, other interactive elements can be initialized here.
            // e.g., this._initCharts();
        },

        /**
         * Initializes the tab functionality, including remembering the last active tab.
         * This enhances user experience by preventing the tab from resetting on reload.
         * @private
         */
        _initTabs: function () {
            var self = this;
            // When a tab is shown, save its ID to localStorage
            this.$('button[data-bs-toggle="tab"]').on('shown.bs.tab', function (e) {
                localStorage.setItem('lastDashboardTab', $(e.target).attr('id'));
            });

            // Get the last active tab ID from localStorage
            var lastTab = localStorage.getItem('lastDashboardTab');
            if (lastTab) {
                // If a last active tab is found, show it.
                // We use a specific selector to ensure we only target the dashboard tabs.
                self.$('#' + lastTab).tab('show');
            }
        },

        /**
         * Placeholder for future chart initializations.
         * @private
         */
        _initCharts: function () {
            // This is where you would initialize charts using a library like Chart.js
            // console.log("Chart initialization would happen here.");
            // Example:
            // var ctx = this.$('.my-performance-chart')[0].getContext('2d');
            // new Chart(ctx, { ... });
        }
    });

    return publicWidget.registry.StudentDashboard;
});
