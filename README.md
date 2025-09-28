# Charge ERP Core Module

Welcome to the Charge ERP Core module. This module provides the foundational features for a comprehensive School Information System (SIS) built on Odoo 19. It includes the core data models, security structure, and user interface for managing students, faculty, courses, and other academic entities.

This module has recently undergone significant development to add a managerial dashboard, enhance data models, and implement advanced, department-based security.

## Key Features

### 1. Managerial Dashboard
A new dashboard is available for users in the "Manager" group, providing at-a-glance insights into key school metrics.
- **KPI Tiles**: See real-time counts of Total Active Students, Total Faculty, and Total Active Courses.
- **Visualizations**:
    - A **bar chart** showing the distribution of students across different departments.
    - A **pie chart** showing the distribution of faculty across different departments.

### 2. Enhanced Data Models
The core models have been enriched to capture more detailed information:
- **Faculty Model**: Now includes fields for Nationality, Visa Info, Qualifications, Specialization, Office Location, and Emergency Contact. It also has a link to an `hr.employee` record (if the HR module is installed).
- **Student Model**: Includes a new field for `previous_education`.
- **Course Model**: Enhanced with fields for `credits`, `course_type` (Core, Elective, Lab), and a rich-text `syllabus`.

### 3. Department-Based Security
A sophisticated security layer has been added to control data visibility based on academic departments.
- **Main & Allowed Departments**: Faculty members now have a "Main Department" and a list of "Allowed Departments."
- **Record Rules**:
    - **Faculty Visibility**: Faculty members can only see the profiles of other faculty who are in their same departments.
    - **Student Visibility**: Faculty members can only see students who are enrolled in a program belonging to one of their assigned departments.
    - **Manager Override**: Managers have full visibility across all departments.

### 4. Improved User Experience
- **Restructured Faculty Form**: The faculty form has been reorganized into two clean tabs: "Personal Information" and "Academic Profile," making it easier to navigate.
- **Smart Buttons**: The faculty form now features smart buttons for **Courses**, **Subjects**, and **Sessions**, providing quick access to related records and showing a count of each.

### 5. Core Architecture
- **Normalized Student Name**: The `res.partner` model has been extended to include granular `first_name`, `middle_name`, and `last_name` fields, ensuring data consistency.
- **Modular Design**: The core module is designed to be lean, serving as a stable foundation for future extension modules (e.g., Fees, Assignments, Attendance).

## Access Control and Security Setup

The security of the Charge ERP Core module is built around a role-based access control system. We have defined three primary roles with specific permissions, in addition to the standard Odoo Administrator.

### Roles and Permissions

1.  **Student (`charge_erp_core.group_op_student`)**
    - **Permissions**: Read-only access.
    - **Description**: This is the most restrictive role, intended for students. Users in this group can view their own information and general academic information like courses and subjects.

2.  **Faculty (`charge_erp_core.group_op_faculty`)**
    - **Permissions**: Read access to academic data, limited by department. Limited write/create access.
    - **Description**: This role is for teachers and other faculty members. Their visibility is restricted to students and other faculty within their assigned departments. They have permission to **create and manage Sessions** and **manage student course enrollments**.

3.  **Manager (`charge_erp_core.group_op_manager`)**
    - **Permissions**: Full Create, Read, Update, Delete (CRUD) access to all models within this module.
    - **Description**: This is the highest-level role within the Charge ERP module. Users in this group, such as administrative staff, have full control over all academic and user data, including access to the new dashboard.

4.  **System Administrator (`base.group_system`)**
    - **Permissions**: Full CRUD access to all models.
    - **Description**: The standard Odoo Administrator group has been granted full permissions for all models in this module.

### How to Assign Roles to Users

To grant users the appropriate permissions, you must assign them to one of the groups listed above. This is done by a System Administrator.

1.  Navigate to **Settings > Users & Companies > Users**.
2.  Select the user you wish to modify.
3.  Click **Edit**.
4.  In the **Access Rights** tab, under the "Charge ERP" section, you will see the available roles (Student, Faculty, Manager).
5.  Check the box next to the desired role for the user. A user can have multiple roles, and they will inherit the highest level of permission granted by their roles.
6.  Click **Save**.