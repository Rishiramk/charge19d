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