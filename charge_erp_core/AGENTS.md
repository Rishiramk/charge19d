# Agent Instructions for Charge ERP Core

This document provides guidelines and best practices for developers working on the Charge ERP Core module. Following these instructions will ensure consistency, stability, and adherence to Odoo 19 standards.

## 1. Creating Demo Users

Creating users in Odoo 19 via XML data files requires a specific and careful process, especially when distinguishing between internal users (like Faculty) and portal users (like Students).

### Best Practice for User and Group Assignment

The following three-step process is the approved standard for this project.

#### Step 1: Create the `res.partner` Record

Every user (`res.users`) must be linked to a partner (`res.partner`). Always create the partner record first.

```xml
<!-- Example: Creating a partner for a faculty member -->
<record id="partner_faculty_alan_turing" model="res.partner">
    <field name="name">Alan Turing</field>
    <field name="email">aturing@school.demo</field>
</record>
```

#### Step 2: Create the `res.users` Record

Next, create the user record and link it to the partner from Step 1. This is the **most critical step** for defining the user type.

*   **For Internal Users (e.g., Faculty):**
    Create a standard `res.users` record. They will automatically be part of the `base.group_user` group, giving them backend access.

    ```xml
    <!-- Example: Creating an internal user for Alan Turing -->
    <record id="user_faculty_alan_turing" model="res.users">
        <field name="name">Alan Turing</field>
        <field name="partner_id" ref="partner_faculty_alan_turing"/>
        <field name="login">aturing</field>
        <field name="password">demo</field>
    </record>
    ```

*   **For Portal Users (e.g., Students):**
    You **MUST** include `<field name="share" eval="True"/>`. This flag is what makes the user a portal user, restricting their access to the frontend portal only. Forgetting this will create them as an internal user, which is a security risk and may violate licensing terms.

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

#### Step 3: Add Users to Security Groups

In Odoo 19, you **cannot** write directly to the `groups_id` field on a `res.users` record via XML. This will cause a `ValueError`.

The correct method is to modify the `res.groups` record itself and add the users to its `user_ids` field. This should be done in a single block after all users have been created.

*   **Syntax:** Use `eval="[(4, ref('user_xml_id'))]"` to **append** a user to the group. The number `4` signifies the "link to" command.

```xml
<!-- Example: Adding all demo faculty to the Faculty group -->
<record id="charge_erp_core.group_op_faculty" model="res.groups">
    <field name="user_ids" eval="[
        (4, ref('user_faculty_alan_turing')),
        (4, ref('user_faculty_ada_lovelace')),
        (4, ref('user_faculty_herodotus'))
        <!-- ... more users ... -->
    ]"/>
</record>

<!-- Example: Adding all demo students to the Student group -->
<record id="charge_erp_core.group_op_student" model="res.groups">
    <field name="user_ids" eval="[
        (4, ref('user_student_john_doe')),
        (4, ref('user_student_jane_smith'))
        <!-- ... more users ... -->
    ]"/>
</record>
```

By following this three-step process, you ensure that users are created correctly, assigned the right type (internal vs. portal), and added to their respective security groups without errors.