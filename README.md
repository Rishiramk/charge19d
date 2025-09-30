# Charge ERP Core Module

Welcome to the Charge ERP Core module. This module provides the foundational features for a comprehensive School Information System (SIS) built on Odoo 19. It includes the core data models, security structure, and user interface for managing students, faculty, courses, and other academic entities.

This module has recently undergone a major "Phase 1" refactoring to establish a robust and secure foundation for future development.

## Key Features & Recent Improvements

- **Modular Architecture**: Designed to be lean and stable, serving as the core for future extension modules (e.g., Fees, Assignments, Attendance).
- **Normalized Data Models**:
    - **Student Name**: The `res.partner` model has been extended to include granular `first_name`, `middle_name`, and `last_name` fields, ensuring data consistency. The full name is constructed automatically.
    - **Student Category**: The student category is a relational `Many2one` field, allowing for better management and filtering.
- **Restructured UI**: The user interface has been reorganized for clarity, with menus grouped into logical sections:
    - **People**: For managing Students and Faculty.
    - **Academics**: For managing Sessions, Courses, Batches, and Subjects.
    - **Academics > Configuration**: For less-frequently accessed settings like Academic Years, Programs, and Departments.

- **Comprehensive Faculty Management**: The faculty form has been completely redesigned with a tabbed interface to provide a 360-degree view. Key enhancements include:
    - **Detailed Tabs**: Information is now organized into logical tabs: Personal Information, Academics, Subjects Detail, Sessions, Library Detail, Health Details, and an HR Link for managers.
    - **Rich Data Fields**: Added extensive fields for personal details (visa info, languages), academic history (qualifications, experience), and health information.
    - **HR Integration**: A new tab allows managers to link a faculty record to an `hr.employee` record and create one directly from the form.
    - **Smart Buttons**: Quick access to related records like Sessions, Subjects, Library items, and the linked Employee profile.

- **Role-Based Access Control**: A granular security system has been implemented to control user permissions.

- **Extensibility**: Both the student and faculty forms now include placeholder "smart buttons" and tabs for future modules (e.g., Assignments, Fees, Attendance, Library, Health), ensuring a seamless upgrade path.

## Access Control and Security Setup

The security of the Charge ERP Core module is built around a role-based access control system. We have defined three primary roles with specific permissions, in addition to the standard Odoo Administrator.

### Roles and Permissions

1.  **Student (`charge_erp_core.group_op_student`)**
    - **Permissions**: Read-only access.
    - **Description**: This is the most restrictive role, intended for students. Users in this group can view their own information, as well as general academic information like courses and subjects, but cannot create or modify any records.

2.  **Faculty (`charge_erp_core.group_op_faculty`)**
    - **Permissions**: Read access to most academic data, with limited write/create access.
    - **Description**: This role is for teachers and other faculty members. They can view student profiles and academic structures. Crucially, they have permission to **create and manage Sessions** and **manage student course enrollments**, but they cannot create new students or courses.

3.  **Manager (`charge_erp_core.group_op_manager`)**
    - **Permissions**: Full Create, Read, Update, Delete (CRUD) access to all models within this module.
    - **Description**: This is the highest-level role within the Charge ERP module. Users in this group, such as administrative staff, have full control over all academic and user data. They can create new students, faculty, courses, and configure all academic settings.

4.  **System Administrator (`base.group_system`)**
    - **Permissions**: Full CRUD access to all models.
    - **Description**: The standard Odoo Administrator group has been granted full permissions for all models in this module. Any user in this group (like the `devops` user) will have complete access, including the ability to see all "New" buttons.

### Record-Level Security

In addition to the role-based permissions, the module now includes **record rules** to enforce row-level security, ensuring users can only access the data relevant to them:

-   **For Students**: A student who logs into the system can only view their own student profile. They cannot see the records of other students.
-   **For Faculty**: A faculty member can only view and manage their own faculty profile and the sessions they are assigned to teach. They can also view the profiles of students who are enrolled in their sessions, but not other students.

These rules provide a more secure environment and protect sensitive student and faculty data.

### How to Assign Roles to Users

To grant users the appropriate permissions, you must assign them to one of the groups listed above. This is done by a System Administrator.

1.  Navigate to **Settings > Users & Companies > Users**.
2.  Select the user you wish to modify.
3.  Click **Edit**.
4.  In the **Access Rights** tab, under the "Charge ERP" section, you will see the available roles (Student, Faculty, Manager).
5.  Check the box next to the desired role for the user. A user can have multiple roles, and they will inherit the highest level of permission granted by their roles.
6.  Click **Save**.

The user's permissions will be updated immediately. For example, to give a user the ability to create new students, you would add them to the **Manager** group.