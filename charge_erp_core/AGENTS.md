# Agent Instructions for Charge ERP Core

This document provides guidelines and best practices for developers working on the Charge ERP Core module. Following these instructions will ensure consistency, stability, and adherence to Odoo 19 standards.

## 1. Creating Demo Users

Creating users in Odoo 19 via XML data files requires a specific and careful process, especially when distinguishing between internal users (like Faculty) and portal users (like Students). This guide outlines the official, best-practice procedure.

### Core Concepts

*   **`res.partner`**: Every user (`res.users`) **must** be linked to a `res.partner` record. The partner holds contact information like name and email.
*   **Internal vs. Portal Users**:
    *   **Internal (Faculty)**: Standard users who can access the Odoo backend. They are implicitly members of `base.group_user`.
    *   **Portal (Student)**: Special users who cannot access the backend and are restricted to the website portal. This is controlled by the `share` boolean field on `res.users`. A user with `share=True` is a portal user.
*   **Group-Based Permissions**:
    *   **`charge_erp_core.group_op_faculty`**: The designated group for all faculty members. It implies `base.group_user`.
    *   **`charge_erp_core.group_op_student`**: The designated group for all students. It implies `base.group_portal`. All ACLs and Record Rules for students depend on this group. **A student user who is not in this group will not be able to see any school data.**
*   **Idempotency**: Demo data files must be idempotent, meaning they can be re-run without creating duplicate data or errors. For group assignments, this is achieved by using the `(6, 0, [ ... ])` syntax, which replaces the list of users in a group rather than appending to it.

---

### Best Practice for User Creation and Group Assignment

The following process is the approved standard for this project. **It must be followed for all new demo users.**

#### For Faculty Users (Internal)

The process involves creating the `res.partner`, then the `res.users`, and finally adding all faculty users to their group in a single, idempotent operation.

**Step 1: Create `res.partner` and `res.users` Records**
In `faculty_demo.xml`, define the partner and user. Do not assign any groups here.

```xml
<!-- Example: faculty_demo.xml -->
<odoo>
    <!-- Alan Turing -->
    <record id="partner_faculty_alan_turing" model="res.partner">
        <field name="name">Alan Turing</field>
        <field name="email">aturing@school.demo</field>
    </record>

    <record id="user_faculty_alan_turing" model="res.users">
        <field name="name">Alan Turing</field>
        <field name="partner_id" ref="partner_faculty_alan_turing"/>
        <field name="login">aturing</field>
        <field name="password">demo</field>
        <!-- No 'share' field means this is an internal user -->
    </record>

    <!-- ... other faculty records ... -->
</odoo>
```

**Step 2: Assign Users to the Faculty Group (Idempotent)**
At the **end** of `faculty_demo.xml`, add one record to update the faculty group with all demo faculty users.

```xml
<!-- Example: faculty_demo.xml (at the end of the file) -->
<record id="charge_erp_core.group_op_faculty" model="res.groups">
    <field name="user_ids" eval="[(6, 0, [
        ref('user_faculty_alan_turing'),
        ref('user_faculty_ada_lovelace'),
        ref('user_faculty_herodotus')
    ])]"/>
</record>
```

---

#### For Student Users (Portal)

The process is similar, but with the critical addition of the `share` flag and assignment to the student group.

**Step 1: Create `res.partner` and `res.users` Records (with `share=True`)**
In `student_demo.xml`, define the partner and user. You **MUST** include `<field name="share" eval="True"/>`.

```xml
<!-- Example: student_demo.xml -->
<odoo>
    <!-- John Doe -->
    <record id="partner_student_john_doe" model="res.partner">
        <field name="name">John Doe</field>
        <field name="email">jdoe@school.demo</field>
    </record>

    <record id="user_student_john_doe" model="res.users">
        <field name="name">John Doe</field>
        <field name="partner_id" ref="partner_student_john_doe"/>
        <field name="login">jdoe</field>
        <field name="password">demo</field>
        <field name="share" eval="True"/> <!-- CRITICAL for portal users -->
    </record>

    <!-- ... other student records ... -->
</odoo>
```

**Step 2: Assign Users to the Student Group (Idempotent)**
At the **end** of `student_demo.xml`, add one record to update the student group with all demo student users. This is the step that grants them portal access rights.

```xml
<!-- Example: student_demo.xml (at the end of the file) -->
<record id="charge_erp_core.group_op_student" model="res.groups">
    <field name="user_ids" eval="[(6, 0, [
        ref('user_student_john_doe'),
        ref('user_student_jane_smith'),
        ref('user_student_peter_jones')
    ])]"/>
</record>
```

By following this refined approach, our demo users are created correctly, have the exact permissions they need, and the demo data setup is clean, safe, and repeatable.

## 2. Extending the School Portal

The school portal is designed to be easily extensible. To add a new section (e.g., "My Fees," "My Attendance"), follow this five-step pattern. This ensures consistency with the existing portal structure and maintains security.

### Step 1: Add a Controller Route

Open `charge_erp_core/controllers/portal.py` and add a new route for your page. The route should:
- Fetch the user's student or faculty record using the `_get_student()` or `_get_faculty()` helpers.
- Query the relevant data for that user.
- Render your new QWeb template, passing the data to it.
- Include pagination (`portal_pager`) if you are displaying a list of records.

**Example: Adding a `/my/attendance` route:**
```python
@http.route(['/my/attendance', '/my/attendance/page/<int:page>'], type='http', auth="user", website=True)
def portal_my_attendance(self, page=1, **kw):
    student = self._get_student()
    if not student:
        return request.redirect('/my')

    domain = [('student_id', '=', student.id)]
    attendance_count = request.env['op.attendance'].search_count(domain)

    pager = portal_pager(
        url="/my/attendance",
        total=attendance_count,
        page=page,
        step=self._items_per_page
    )

    attendance_records = request.env['op.attendance'].search(domain, limit=self._items_per_page, offset=pager['offset'])

    values = self._prepare_portal_layout_values()
    values.update({
        'attendance_records': attendance_records,
        'page_name': 'attendance',
        'pager': pager,
    })
    return request.render("charge_erp_core.portal_my_attendance_template", values)
```

### Step 2: Add a Homepage Tile

Open `charge_erp_core/views/portal_templates.xml` and add a new tile to the `portal_my_home_school` template.
- Use the standard `o_portal_my_home_entry` structure for consistency.
- Wrap the tile in a `t-if` condition to control its visibility (e.g., only show to students). You can use the count variables passed from `_prepare_portal_layout_values`.

**Example: Adding a tile for "My Attendance":**
```xml
<!-- My Attendance -->
<div t-if="attendance_count" class="col-12 col-md-6">
    <a class="o_portal_my_home_entry d-block p-3 border rounded" t-att-href="'/my/attendance'">
        <i class="fa fa-check-square-o fa-2x float-start me-3 text-primary"/>
        <div class="o_portal_my_home_entry_desc">
            <h5>My Attendance</h5>
            <span>View your attendance records.</span>
        </div>
    </a>
</div>
```
*Don't forget to add `attendance_count` to the `_prepare_portal_layout_values` method in the controller.*

### Step 3: Create the Detail Page Template

In the same `portal_templates.xml` file, create the new QWeb template that will render your page.
- The template ID must match the one you specified in your controller's `request.render()` call.
- Inherit from `portal.portal_layout` to maintain a consistent look and feel.
- Include breadcrumbs for easy navigation.
- Display the data passed from the controller, typically in a table.

**Example: Template for "My Attendance":**
```xml
<!-- My Attendance Page -->
<template id="portal_my_attendance_template" name="My Attendance">
    <t t-call="portal.portal_layout">
        <t t-set="breadcrumbs" t-value="[('Home', '/my'), ('My Attendance', '/my/attendance')]"/>
        <t t-call="portal.portal_searchbar">
            <t t-set="title">My Attendance</t>
        </t>
        <div t-if="attendance_records" class="table-responsive">
            <table class="table table-hover">
                <!-- Table headers and rows to display attendance data -->
            </table>
        </div>
        <div t-if="pager" class="o_portal_pager"><t t-call="portal.pager"/></div>
    </t>
</template>
```

### Step 4: Grant Model Access (ACL)

If you are exposing a new model, you **must** grant access to the appropriate user group. Open `charge_erp_core/security/ir.model.access.csv` and add a new line.

**Example: Granting students access to `op.attendance`:**
```csv
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_op_attendance_student,op.attendance.student,model_op_attendance,charge_erp_core.group_op_student,1,0,0,0
```

### Step 5: Enforce Record-Level Security

To ensure users can only see their own data, you **must** add a record rule. Open `charge_erp_core/security/security.xml` and add a new rule for your model.

**Example: Rule to restrict students to their own attendance records:**
```xml
<record id="op_attendance_rule_student" model="ir.rule">
    <field name="name">Student can only see their own attendance records</field>
    <field name="model_id" ref="model_op_attendance"/>
    <field name="groups" eval="[(4, ref('group_op_student'))]"/>
    <field name="domain_force">[('student_id.user_id', '=', user.id)]</field>
</record>
```
By following these five steps, you can seamlessly and securely extend the portal with new features.