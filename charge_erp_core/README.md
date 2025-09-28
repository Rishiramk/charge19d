# Charge ERP Core Module

This module contains the core models and functionality for the Charge ERP system.

## Features

As of the current version, this module includes the following features:
- A `School` menu in the Odoo interface.
- Core models for managing: Students, Courses, Faculties, Subjects, Batches, Programs, Departments, and Academic Years.
- Bi-directional relationships between all major academic models.
- Enhanced views (List, Form, Kanban, Search) for all core models.
- Role-based access control for Students, Faculty, and Managers.

## Core Enhancements (Recent Development Cycle)

This module has undergone a significant enhancement cycle to improve data integrity, usability, and functionality.

### 1. Data Model & Relationship Enhancements

The core data model has been strengthened by establishing critical bi-directional relationships:

- **Faculty & Sessions:** A `One2many` relationship now correctly links faculty to their assigned sessions. A smart button on the Faculty form displays the session count and provides direct navigation.
- **Faculty & Subjects:** A `ManyToManyField` now links faculty and subjects, allowing the system to track which subjects a faculty can teach and which faculty are available for a given subject.
- **Courses & Departments:** Courses are now linked to their respective academic departments via a `Many2one` relationship, with a smart button on the Department form to show all associated courses.
- **Batches, Programs & Academic Years:** Batches are now formally linked to both a Program and an Academic Year, creating a clear academic hierarchy. Smart buttons have been added to the Program and Academic Year forms for easy navigation.

### 2. Course Enrollment Refactoring

To improve clarity and align with best practices, the student enrollment system was refactored:
- **Model Rename:** The ambiguous `op.student.course` model has been renamed to `op.course.enrollment`.
- **Field Rename:** The corresponding `One2many` fields on the student and course models have been renamed to the more intuitive `enrollment_ids`.
- **Security & Views:** All related security rules and views have been updated to reflect the new model name.

### 3. UI/UX Improvements

The user interface has been significantly upgraded to be more powerful and user-friendly:

- **Powerful Search Views:** New search views have been added for Students, Faculty, Courses, and Sessions. These views provide robust search fields, pre-defined filters (e.g., "Active Students"), and powerful "Group By" options (e.g., group students by batch, group faculty by department).
- **Informative Kanban Views:**
    - The **Student Kanban** view is now color-coded based on status (Active, On Leave, Graduated) and includes more details like the student's program and email.
    - The **Faculty Kanban** view now displays the faculty member's email and phone number directly on the card.
- **Refined Form Layouts:** The Student form view has been reorganized to be more logical, with all academic information consolidated under a single "Educational" tab.

### 4. Bug Fixes

- **Search View Syntax:** A bug in the initial implementation of the new search views (related to an invalid `<group>` tag) was identified and corrected across all affected views.
- **Smart Button Action:** A critical bug preventing the Student "Sessions" smart button from working was fixed by adding the required search view for the Session model.

## How to Deploy

To deploy this module, please follow these steps:

1.  **Ensure you have a running Odoo 19 instance.**
2.  **Add this module to your addons path.** Place the `charge_erp_core` directory into the `addons` directory of your Odoo installation.
3.  **Restart your Odoo server.** This is necessary for Odoo to recognize the new module.
4.  **Activate Developer Mode.** In your Odoo instance, go to `Settings` -> `General Settings` and click on `Activate the developer mode`.
5.  **Update the Apps List.** Go to `Apps` in the main menu and click on `Update Apps List` in the secondary menu. You will be prompted to confirm the update.
6.  **Install or Upgrade the Module.** Search for `Charge ERP Core` in the Apps list (you may need to remove the default "Apps" filter to see it). Click the "Install" or "Upgrade" button on the module.

Once the installation is complete, you will see a new "School" menu in your Odoo instance where you can manage the new models.