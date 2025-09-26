# Charge ERP Core Module

This module contains the core models and functionality for the Charge ERP system.

## Features

As of the current version, this module includes the following features:
- A `School` menu in the Odoo interface.
- Basic models for managing:
    - Students (`op.student`)
    - Courses (`op.course`)
    - Faculties (`op.faculty`)
    - Subjects (`op.subject`)
    - Batches (`op.batch`)
    - Program Levels (`op.program.level`)
    - Programs (`op.program`)
    - Departments (`op.department`)
    - Academic Terms (`op.academic.term`)
    - Academic Years (`op.academic.year`)
- Basic views (list and form) and menu items for each of the above models.
- Basic access rights for all new models.

## Detailed Development Log

### Student Management Enhancements

The student management system has been significantly enhanced to provide a more robust and user-friendly experience.

#### 1. Category Management (`op.category`)

- **New Model**: A new model, `op.category`, has been created to allow for the centralized management of student categories.
- **Refactored Field**: The `category` field on the `op.student` model has been changed from a simple text field to a `Many2one` relationship with the new `op.category` model. This ensures data consistency and allows for easier filtering and reporting.

#### 2. Course Enrollment (`op.student.course`)

- **New Model**: A new model, `op.student.course`, has been introduced to track student enrollments in different courses across academic years.
- **"Courses" Tab**: A "Courses" tab has been added to the student form view. This tab contains an editable list view that displays all the courses a student is enrolled in, along with the academic year and the status of the enrollment (e.g., "enrolled," "dropped," "completed").

#### 3. UI/UX Improvements

- **Status Bar**: The status bar on the student form now includes the `on_leave` state, providing a complete visual representation of all possible student statuses.
- **Portal Access Tab**: The `user_id` field has been moved to a new "Portal Access" tab for better organization and clarity.
- **Kanban View**: A new Kanban view has been implemented for students, providing a more visual and at-a-glance overview. Each Kanban card displays the student's photo, name, batch, and status.

### Faculty Management Enhancements

The faculty management system has been refactored to align with Odoo best practices and provide more detailed academic information.

#### 1. Inheritance from `res.partner`

- **Refactored Model**: The `op.faculty` model now inherits from `res.partner` using the `_inherits` mechanism. This simplifies the model by leveraging the built-in fields of `res.partner` (e.g., address, contact information) and ensures consistency with other models in the system.
- **Granular Name Fields**: The `first_name`, `middle_name`, and `last_name` fields have been preserved on the faculty model to allow for detailed name management. A computed `name` field automatically concatenates these fields into the main `name` field inherited from `res.partner`.

#### 2. Academic Information

- **New Fields**: The `op.faculty` model now includes the following fields to store more detailed academic information:
    - `department_id` (Many2one to `op.department`)
    - `program_id` (Many2one to `op.program`)
    - `subject_ids` (Many2many to `op.subject`)
- **Updated Views**: The faculty form and list views have been updated to include these new fields, providing a more comprehensive overview of each faculty member.

#### 3. Link to Sessions

- **Refactored Relationship**: The `op.session` model has been updated to use a `faculty_id` `Many2one` field instead of a `Many2many` field. This establishes a clear, one-to-one link between a session and its assigned faculty member.

### Bug Fixes

- **Odoo 19 View Compatibility**: This development cycle included fixes for several view rendering errors specific to Odoo 19. This involved:
    - Replacing a deprecated `<tree>` tag with `<list>` for an inline list view definition.
    - Correcting the Kanban view image rendering by replacing the deprecated `kanban_image()` function with a direct reference to the image field's raw value (`record.image_128.raw_value`).
    - Resolving a "Missing 'card' template" error by renaming the Kanban QWeb template to `card`.

## How to Deploy

To deploy this module, please follow these steps:

1.  **Ensure you have a running Odoo 19 instance.**
2.  **Add this module to your addons path.** Place the `charge_erp_core` directory into the `addons` directory of your Odoo installation.
3.  **Restart your Odoo server.** This is necessary for Odoo to recognize the new module.
4.  **Activate Developer Mode.** In your Odoo instance, go to `Settings` -> `General Settings` and click on `Activate the developer mode`.
5.  **Update the Apps List.** Go to `Apps` in the main menu and click on `Update Apps List` in the secondary menu. You will be prompted to confirm the update.
6.  **Install or Upgrade the Module.** Search for `Charge ERP Core` in the Apps list (you may need to remove the default "Apps" filter to see it). Click the "Install" or "Upgrade" button on the module.

Once the installation is complete, you will see a new "School" menu in your Odoo instance where you can manage the new models.