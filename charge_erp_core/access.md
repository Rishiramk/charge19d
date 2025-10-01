# Odoo Access Rights Configuration

This document explains how to configure access rights in Odoo, focusing on security groups and record rules. We will use the example of restricting faculty members to see only students from their own department.

## 1. Security Groups

Security groups are used to grant access to different parts of the system (e.g., menus, models, fields). Users are added to groups to give them specific permissions.

### Defining a Security Group

Security groups are defined in XML files, typically within the `security/` directory of a module.

**Example: `charge_erp_core/security/security.xml`**

```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <data noupdate="1">

        <!-- Category for the security groups -->
        <record model="ir.module.category" id="module_category_charge_erp">
            <field name="name">Charge ERP</field>
            <field name="description">Helps you manage your school</field>
            <field name="sequence">20</field>
        </record>

        <!-- Faculty Security Group -->
        <record id="group_op_faculty" model="res.groups">
            <field name="name">Faculty</field>
            <field name="category_id" ref="module_category_charge_erp"/>
            <field name="implied_ids" eval="[(4, ref('base.group_user'))]"/>
        </record>

    </data>
</odoo>
```

**Explanation:**

*   **`ir.module.category`**: This creates a category in the `Settings > Users & Companies > Groups` menu to organize your groups.
*   **`res.groups`**: This defines the actual security group.
    *   `id`: A unique XML ID for the group.
    *   `name`: The human-readable name of the group (e.g., "Faculty").
    *   `category_id`: Links the group to the category defined above.
    *   `implied_ids`: This group will inherit all the access rights from the groups listed here. In this case, `group_op_faculty` inherits from `base.group_user`, which is the standard user group in Odoo.

## 2. Model Access Control (ir.model.access.csv)

After defining groups, you need to specify which models they can access and what operations they can perform (create, read, write, delete). This is done in the `security/ir.model.access.csv` file.

**Example: `charge_erp_core/security/ir.model.access.csv`**

```csv
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_op_student_faculty,op.student.faculty,model_op_student,charge_erp_core.group_op_faculty,1,0,0,0
```

**Explanation:**

*   **`id`**: A unique ID for this access rule.
*   **`name`**: A descriptive name.
*   **`model_id:id`**: The model this rule applies to (e.g., `model_op_student` for the `op.student` model).
*   **`group_id:id`**: The security group this rule applies to (e.g., `charge_erp_core.group_op_faculty`).
*   **`perm_read`, `perm_write`, `perm_create`, `perm_unlink`**: `1` for allow, `0` for deny. In this example, faculty can read student records but cannot write, create, or delete them.

## 3. Record Rules

Record rules are used to restrict access to specific records within a model. This is where you define row-level security.

### Defining a Record Rule

Record rules are also defined in XML files, typically in `security/security.xml`.

**Example: `charge_erp_core/security/security.xml`**

Here is the record rule we implemented to restrict faculty to see only students in their department.

```xml
<record id="op_student_rule_faculty" model="ir.rule">
    <field name="name">Faculty can only see students in their department</field>
    <field name="model_id" ref="model_op_student"/>
    <field name="groups" eval="[(4, ref('group_op_faculty'))]"/>
    <field name="domain_force">[('program_id.department_id', 'in', user.env['op.faculty'].search([('user_id','=',user.id)]).mapped('department_id').ids)]</field>
    <field name="perm_read" eval="1"/>
    <field name="perm_write" eval="0"/>
    <field name="perm_create" eval="0"/>
    <field name="perm_unlink" eval="0"/>
</record>
```

**Explanation:**

*   **`id`**: A unique XML ID for the rule.
*   **`name`**: A descriptive name for the rule.
*   **`model_id`**: The model this rule applies to (`model_op_student`).
*   **`groups`**: The security group(s) this rule applies to. `eval="[(4, ref('group_op_faculty'))]"` links this rule to our "Faculty" group.
*   **`domain_force`**: This is the core of the record rule. It's an Odoo domain that filters the records. Only records that match this domain will be visible to the user.
    *   `user` is a special variable available in domain rules that refers to the current user's `res.users` record.
    *   `user.env['op.faculty'].search([('user_id','=',user.id)])` finds the faculty record linked to the current user.
    *   `.mapped('department_id').ids` gets the ID(s) of the department(s) associated with that faculty member.
    *   `('program_id.department_id', 'in', ...)` filters the students, showing only those whose program's department is in the list of the faculty's departments.
*   **`perm_...`**: These flags specify if the rule applies to read, write, create, or delete operations. If a flag is not set, the rule does not apply to that operation.

## Summary of Changes

To implement the "Faculty can only see students in their department" feature, we ensured the following were in place:

1.  A security group for faculty (`group_op_faculty`).
2.  An access control rule in `ir.model.access.csv` granting read access to the student model for the faculty group.
3.  A record rule (`op_student_rule_faculty`) with a `domain_force` that filters students based on the faculty member's department.

This combination provides a powerful way to control not just *what* users can see (models), but also *which specific records* they can see.

---

## 4. Managing Access Rights from the Odoo User Interface (UI)

While the most robust way to manage access rights is through the module's code (as described above), you can also view and modify these settings directly from the Odoo UI. This is especially useful for testing or for making small adjustments without changing the code.

### Activating Developer Mode

To access the technical settings, you first need to activate developer mode:
1.  Go to the **Settings** menu.
2.  Scroll down and click on **Activate the developer mode**.

### Managing Security Groups from the UI

1.  **Navigate to Groups:** Once in developer mode, go to **Settings > Users & Companies > Groups**.
2.  **Find the Group:** Use the search bar to find the group you want to inspect, for example, `Faculty`.
3.  **View and Modify:**
    *   You can see the users assigned to this group under the **Users** tab.
    *   You can see which menus, views, and access rights are associated with this group.
    *   You can add or remove users from the group by clicking **Add a line** in the Users tab.

### Managing Record Rules from the UI

1.  **Navigate to Record Rules:** In developer mode, go to **Settings > Technical > Security > Record Rules**.
2.  **Find the Rule:** Use the search bar to find the rule you want to inspect. For our example, search for `Faculty can only see students in their department`.
3.  **View and Modify:**
    *   **Model:** You can see which model the rule applies to (e.g., `op.student`).
    *   **Domain:** The **Domain** field shows the filtering logic. For our rule, it will be `[('program_id.department_id', 'in', user.env['op.faculty'].search([('user_id','=',user.id)]).mapped('department_id').ids)]`. You can modify this domain directly in the UI for testing purposes, but be aware that changes will be overridden the next time the module is updated.
    *   **Groups:** The **Groups** tab shows which security groups this rule applies to (e.g., `charge_erp_core.group_op_faculty`).
    *   **Permissions:** The `Apply for Read`, `Apply for Write`, `Apply for Create`, and `Apply for Delete` checkboxes correspond to the `perm_read`, `perm_write`, `perm_create`, and `perm_unlink` flags in the XML file.

**Important Note:** Changes made in the UI are not saved in your module's code. If you update the `charge_erp_core` module, any changes you made to the record rules or security groups via the UI will be reset to what is defined in the XML files. The UI is best used for inspection and temporary testing. For permanent changes, it's always best to update the XML files in your module.

---

## 5. Bulk Importing Faculty Users

To import a large number of faculty members at once (e.g., 100 users), you can use Odoo's built-in import tool. This is a two-step process that involves creating the user accounts first, and then creating the detailed faculty profiles.

Template files for this process are located in the `charge_erp_core/import_templates/` directory.

### Step 1: Import the User Accounts

1.  **Prepare your data:** Use the `faculty_users_template.csv` as a reference. Fill it with the data for all the users you want to create. The key columns are:
    *   `Name`: The full name of the user.
    *   `Login`: A unique login/username for the user.
    *   `Email`: The user's email address.
    *   `Access Rights/Groups`: To assign the user to the faculty group, use the value `Charge ERP / Faculty`.

2.  **Import the file:**
    *   In Odoo, navigate to **Settings > Users & Companies > Users**.
    *   Click the "Favorites" icon (the star) and select **Import records**.
    *   Upload your completed CSV file.
    *   Click **Test** to ensure the data is valid, then click **Import**.

### Step 2: Import the Faculty Profiles

1.  **Prepare your data:** Use the `faculty_profiles_template.csv` as a reference. This file contains a comprehensive set of columns for the faculty profile.
    *   **Crucial Link:** The **`User/ID`** column is the most important. You must use the **Login** value from the user file you imported in Step 1 to link the faculty profile to the correct user account.
    *   Fill in the other details like `First Name`, `Last Name`, `Department/ID`, etc.

2.  **Import the file:**
    *   Navigate to the **Faculty** menu.
    *   Click **Favorites > Import records**.
    *   Upload your completed faculty profile CSV file.
    *   Click **Test** to validate, and then **Import**.

This two-step process ensures that both the user accounts and the detailed faculty profiles are created and correctly linked in the system.