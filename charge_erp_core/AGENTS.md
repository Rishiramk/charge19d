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