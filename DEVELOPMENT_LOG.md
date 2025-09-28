# Charge ERP Core: Development Log & Summary

## Overview

This document provides a detailed log of the significant development and enhancement cycle for the `charge_erp_core` module. The goal of this cycle was to strengthen the data model, refactor key components for clarity, and dramatically improve the user interface and overall user experience.

All changes were implemented, reviewed, and tested to ensure stability and correctness.

---

## I. Feature Enhancements

The following major features and enhancements were implemented:

### 1. Data Model & Relationship Enhancements

The core data model was strengthened by establishing critical bi-directional relationships between the main academic models. This creates a more logical and interconnected system, paving the way for future features.

-   **Faculty & Sessions:**
    -   **Enhancement:** A `One2many` relationship was established to correctly link a faculty member to their many assigned sessions.
    -   **UI Impact:** A smart button was added to the Faculty form, displaying the session count and providing direct navigation to the sessions.

-   **Faculty & Subjects:**
    -   **Enhancement:** A `ManyToManyField` was created to link faculty and subjects, allowing the system to track which subjects a faculty member is qualified to teach.
    -   **UI Impact:** A "Subjects" tab was added to the Faculty form, and a "Faculties" tab was added to the Subject form, making the relationship fully manageable from the UI.

-   **Courses & Departments:**
    -   **Enhancement:** Courses are now formally linked to their respective academic departments via a `Many2one` relationship.
    -   **UI Impact:** A "Department" field was added to the Course form, and a smart button was added to the Department form to display all associated courses.

-   **Batches, Programs & Academic Years:**
    -   **Enhancement:** Batches are now linked to both a Program and an Academic Year via `Many2one` fields, creating a clear academic hierarchy.
    -   **UI Impact:** The new relationship fields were added to the Batch form, and smart buttons were added to the Program and Academic Year forms for easy navigation.

### 2. Course Enrollment Refactoring

To improve clarity and align with Odoo best practices, the student enrollment system was refactored:

-   **Model Rename:** The ambiguous `op.student.course` model was renamed to `op.course.enrollment`.
-   **Field Rename:** The corresponding `One2many` fields on the student and course models were renamed to the more intuitive `enrollment_ids`.
-   **System-Wide Update:** All references to the old model and fields were updated across the entire module, including in security rules, model definitions, and view files.

### 3. UI/UX Improvements

The user interface was significantly upgraded to be more powerful and user-friendly:

-   **Powerful Search Views:**
    -   **Enhancement:** New search views were added for Students, Faculty, Courses, and Sessions.
    -   **Features:** These views provide robust search fields, pre-defined filters (e.g., "Active Students"), and powerful "Group By" options (e.g., group students by batch, group faculty by department).

-   **Informative Kanban Views:**
    -   **Student Kanban:** The view is now color-coded based on the student's status (Active, On Leave, Graduated) and includes more details like the student's program and email.
    -   **Faculty Kanban:** The view now displays the faculty member's email and phone number directly on the card for quick access.

-   **Refined Form Layouts:**
    -   **Enhancement:** The Student form view was reorganized to be more logical, with all academic information consolidated under a single "Educational" tab.

-   **Enrollment Menu Item:**
    -   **Enhancement:** Added a dedicated "Enrollments" menu item under "Academics > Course Management" to provide direct access to the `op.course.enrollment` model.
    -   **Implementation:** This involved creating new list and form views, a window action, and updating the manifest file to make the model accessible from the UI.

### 4. Enhanced Data Integrity with SQL Constraints

To improve data quality and prevent duplicate records, database-level uniqueness constraints (`_sql_constraints`) were added to several key models. This is a lightweight but powerful enhancement that strengthens the reliability of the core data.

-   **Student:** Enforced uniqueness on `roll_number` and `registration_number`.
-   **Course & Subject:** Enforced uniqueness on the `code` field.
-   **Department, Program & Academic Year:** Enforced uniqueness on the `name` field.
-   **Batch:** Enforced uniqueness on the combination of `name` and `program_id` to allow same-named batches across different programs.

---

## II. Issues Encountered & Bug Fixes

During development, two key issues were identified and resolved.

### Bug 1: Invalid Search View Syntax

-   **Issue:** The initial implementation of the new search views used an invalid `<group expand="0">` tag to define the "Group By" options. This is not a valid structure for search views in Odoo and would have caused rendering errors.
-   **Fix:** The invalid `<group>` wrapper was removed from the search views for Students, Faculty, Courses, and Sessions. The "Group By" filters were placed directly within the `<search>` element, which is the standard and correct Odoo implementation.

### Bug 2: Broken "Sessions" Smart Button on Student Form

-   **Issue:** The "Sessions" smart button on the student form was non-functional. Clicking it would not correctly filter the sessions for that student.
-   **Root Cause Analysis:** The issue was traced to the button's context (`search_default_attendee_ids`), which relies on a filter being defined in the target model's search view. The `op.session` model was missing a search view entirely.
-   **Fix:** A new, comprehensive search view was created for the `op.session` model. Crucially, this new view included a `<field name="attendee_ids" ... />` definition, which enabled the `search_default` context to work correctly. This not only fixed the bug but also added valuable search functionality to the Sessions screen.

### Bug 3: Incorrect Display Name for Course Enrollment

-   **Issue:** When creating a new course enrollment record (e.g., from the Student form), the UI would display a generic system ID like "op.course.enrollment,NewId_..." instead of a human-readable name.
-   **Fix:** A computed `name` field was added to the `op.course.enrollment` model. This field generates a user-friendly name by combining the student's name and the course name (e.g., "John Doe - Introduction to Python"), resolving the display issue.