# Agent Instructions for Charge ERP Core

This document provides guidelines and best practices for developers working on the Charge ERP Core module. Following these instructions will ensure consistency, stability, and adherence to Odoo 19 standards.

## 1. Creating Demo Users

Creating users in Odoo 19 via XML data files requires a specific and careful process, especially when distinguishing between internal users (like Faculty) and portal users (like Students).

### Analysis of Security Configuration

*   **`security.xml`**: This file defines our application-specific groups: `group_op_student` and `group_op_faculty`.
    *   `group_op_student` correctly implies `base.group_portal`, which is the standard Odoo method for creating a specific *type* of portal user. Any user added to `group_op_student` will automatically be treated as a portal user.
    *   `group_op_faculty` implies `base.group_user`, correctly making them full internal users.
    *   This file also contains record rules that properly restrict data visibility, for instance, ensuring faculty can only see students within their own department.
*   **`ir.model.access.csv`**: This file is critical. It grants the actual permissions (read, write, create, delete) for each model to our specific groups.
    *   Access for students to models like `op.student`, `op.course`, etc., is granted specifically to `charge_erp_core.group_op_student`.
    *   This confirms that adding a student user to `base.group_portal` alone would be insufficient. **They must be members of `group_op_student` to see any of the school's data.**

### Best Practice for User and Group Assignment

The following process is the approved standard for this project.

#### For Faculty Users (Internal)

1.  **Create the `res.partner` Record**: Every user (`res.users`) must be linked to a partner (`res.partner`). Always create the partner record first.

    ```xml
    <!-- Example: Creating a partner for a faculty member -->
    <record id="partner_faculty_alan_turing" model="res.partner">
        <field name="name">Alan Turing</field>
        <field name="email">aturing@school.demo</field>
    </record>
    ```

2.  **Create the `res.users` Record**: Create a standard `res.users` record. They will automatically be part of the `base.group_user` group, giving them backend access.

    ```xml
    <!-- Example: Creating an internal user for Alan Turing -->
    <record id="user_faculty_alan_turing" model="res.users">
        <field name="name">Alan Turing</field>
        <field name="partner_id" ref="partner_faculty_alan_turing"/>
        <field name="login">aturing</field>
        <field name="password">demo</field>
    </record>
    ```

3.  **Assign to Group**: In a separate demo record, target the `charge_erp_core.group_op_faculty` group. Use `eval="[(6, 0, [ref('demo_faculty_user_id')])]"` on its `user_ids` field. This is idempotent (it replaces the group's user list every time).

    ```xml
    <record id="charge_erp_core.group_op_faculty" model="res.groups">
        <field name="user_ids" eval="[(6, 0, [
            ref('user_faculty_alan_turing'),
            ref('user_faculty_ada_lovelace')
        ])]"/>
    </record>
    ```

#### For Student Users (Portal)

1.  **Create the `res.partner` Record**: As with internal users, create the partner first.

2.  **Create the `res.users` Record with `share` Flag**: You **MUST** include `<field name="share" eval="True"/>`. This flag is what makes the user a portal user, restricting their access to the frontend portal only. Forgetting this will create them as an internal user, which is a security risk and may violate licensing terms.

    ```xml
    <!-- Example: Creating a portal user for a student -->
    <record id="user_student_john_doe" model="res.users">
        <field name="name">John Doe</field>
        <field name="partner_id" ref="partner_student_john_doe"/>
        <field name="login">johndoe</field>
        <field name="password">demo</field>
        <field name="share" eval="True"/> <!-- CRITICAL for portal users -->
    </record>
    ```

3.  **Assign to Group**: Add the student user to the `charge_erp_core.group_op_student` group using the same idempotent `eval="[(6, 0, [ref('demo_student_user_id')])]"` method. Adding them to `group_op_student` is sufficient because it implies `base.group_portal` (making them a portal user) and grants them all the necessary read permissions defined in `ir.model.access.csv`.

    ```xml
    <record id="charge_erp_core.group_op_student" model="res.groups">
        <field name="user_ids" eval="[(6, 0, [
            ref('user_student_john_doe')
        ])]"/>
    </record>
    ```

By following this refined approach, our demo users are created correctly, have the exact permissions they need, and the demo data setup is clean and repeatable.

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