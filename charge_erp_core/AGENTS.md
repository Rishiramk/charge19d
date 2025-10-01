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

In Odoo 19, you **cannot** write directly to the `groups_id` field on a `res.users` record via XML. This will cause a `ValueError`. The correct method is to modify the `res.groups` record itself.

There are two primary methods for this, each with a specific use case.

##### Best Practice for Demo Data: Replace the User List

For demo data, it is crucial that the data is **idempotent**. This means that no matter how many times you install or update the module, the result is always the same clean, predictable set of demo users.

To achieve this, use the `(6, 0, [IDs])` command. This command **replaces** the entire list of users in a group with the new list you provide.

*   **Syntax:** `eval="[(6, 0, [ref('user_one'), ref('user_two')])]"`

```xml
<!--
  BEST PRACTICE:
  This replaces all users in the group with our demo users, ensuring a
  clean state every time the module is loaded.
-->
<record id="charge_erp_core.group_op_faculty" model="res.groups">
    <field name="user_ids" eval="[(6, 0, [
        ref('user_faculty_alan_turing'),
        ref('user_faculty_ada_lovelace'),
        ref('user_faculty_herodotus')
        <!-- ... more users ... -->
    ])]"/>
</record>
```

##### Alternative Method: Append Users to a Group

In some cases, you may want to **add** users to a group without removing existing members. This is useful when you are adding users to a standard Odoo group (like `base.group_user`) that might already contain other important users.

To do this, use the `(4, ID)` command for each user you want to add.

*   **Syntax:** `eval="[(4, ref('user_one')), (4, ref('user_two'))]"`

```xml
<!--
  This appends users to a group. Use this when you do not want to
  remove existing members from the group.
-->
<record id="some_existing_group" model="res.groups">
    <field name="user_ids" eval="[
        (4, ref('user_to_add_one')),
        (4, ref('user_to_add_two'))
    ]"/>
</record>
```

By understanding and using the correct method for your specific needs, you ensure that users are managed cleanly, correctly, and without unintended side effects.