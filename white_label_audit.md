# Phase 0: White-Label Audit Report

This report documents all occurrences of Odoo branding strings found within the repository. Each entry includes the original string, a proposed replacement, and a risk assessment.

**Note:** Many occurrences are part of the Odoo framework's core syntax (e.g., Python imports, XML tags, JS module definitions) and are marked as "High Risk" or "Do Not Change" because modifying them would break the application. Phase 1 will focus only on low-risk, user-facing branding.

| File | Old String | Proposed Replacement | Risk | Notes |
| :--- | :--- | :--- | :--- | :--- |
| `README.md` | Odoo 19 | Charge ERP (Odoo 19 CE) | Low | Update product name in project description. |
| `README.md` | Odoo | Charge ERP | Low | Replace general references to the platform. |
| `README.md` | odoo-bin | odoo-bin | None | This is an executable name and should not be changed. |
| `DEVELOPMENT_LOG.md` | Odoo | Charge ERP | Low | Replace general references in development logs. |
| `charge_erp_core/AGENTS.md` | Odoo 19 | Charge ERP (Odoo 19 CE) | Low | Update product name in agent instructions. |
| `charge_erp_core/models/**/*.py` | `from odoo import ...` | No Change | **High** | Core Odoo framework import. Cannot be changed. |
| `charge_erp_core/tests/**/*.py` | `from odoo.tests...` | No Change | **High** | Core Odoo framework import for tests. Cannot be changed. |
| `charge_erp_core/views/**/*.xml` | `<odoo>` | No Change | **High** | Root XML tag for Odoo views. Cannot be changed. |
| `charge_erp_core/demo/**/*.xml` | `<odoo>` | No Change | **High** | Root XML tag for Odoo demo files. Cannot be changed. |
| `charge_erp_core/security/**/*.xml`| `<odoo>` | No Change | **High** | Root XML tag for Odoo security files. Cannot be changed. |
| `charge_erp_core/wizard/**/*.xml` | `<odoo>` | No Change | **High** | Root XML tag for Odoo wizard views. Cannot be changed. |
| `charge_erp_core/static/src/js/portal_dashboard.js` | `odoo.define(...)` | No Change | **High** | Core Odoo JavaScript module definition. Cannot be changed. |
