Charge ERP Core Module
This module contains the core models and functionality for the Charge ERP system, designed for educational institutions.

Features
As of the current version, this module includes the following features:

A central SIS (Student Information System) menu to manage all school-related operations.

Core Models:

Student Management (op.student): A comprehensive student model that inherits from res.partner. It includes personal details, contact information, family information (parent_ids), and academic details.
Faculty Management (op.faculty): A model to manage faculty members, including their personal details and a link to the sessions they teach.
Course Management (op.course): A model to define courses offered by the institution.
Session Management (op.session): A robust session model to schedule and manage individual course sessions. Key features include:
Start date, duration, and number of available seats.
Support for multiple faculty members per session.
A dedicated attendee list for each session.
Academic Structure: Models for managing Batches, Programs, Departments, Academic Terms, and Academic Years.
Attendee Management:

An "Add Attendees" wizard on the session form to easily register multiple students to a session at once.
Automatic seat validation to prevent overbooking sessions.
Enhanced User Interface:

Smart Buttons: The Course, Faculty, and Student forms include smart buttons that display a count of related sessions and provide one-click access to them.
Calendar View: A calendar view for sessions, providing a clear visual schedule.
Organized Forms: Student and Faculty forms are organized with tabs for better readability and data management.
Access Control:

A complete set of access rights for all models, ensuring that users can only access and modify data according to their roles.
How to Deploy
To deploy this module, please follow these steps:

Ensure you have a running Odoo 19 instance.
Add this module to your addons path. Place the charge_erp_core directory into the addons directory of your Odoo installation.
Restart your Odoo server. This is necessary for Odoo to recognize the new module.
Activate Developer Mode. In your Odoo instance, go to Settings -> General Settings and click on Activate the developer mode.
Update the Apps List. Go to Apps in the main menu and click on Update Apps List in the secondary menu. You will be prompted to confirm the update.
Install the Module. Search for Charge ERP Core in the Apps list (you may need to remove the default "Apps" filter to see it). Click the "Install" button on the module.
Once the installation is complete, you will see a new "SIS" menu in your Odoo instance where you can manage the new models.
