# Attribute-based access control (ABAC) in Unity Catalog is in Public Preview

> date: 2026-06-09

Attribute-based access control (ABAC) for Unity Catalog is now in Public
Preview. ABAC lets you govern access to data using policies that reference
attributes — tags on securable objects and properties of the requesting
principal — instead of granting permissions object by object.

With ABAC you can:

- Write policies that apply automatically to any table tagged with a
  classification such as `pii` or `restricted`.
- Enforce column masking and row filtering based on principal attributes.
- Centralize governance so new tables inherit the right controls on creation.

Prerequisites:

- Unity Catalog enabled workspace.
- Tag-based governance enabled for the metastore.

Limitations:

- Policy evaluation currently supports a subset of SQL predicate functions.
- ABAC policies are not yet enforced for Delta Sharing recipients.

Use cases: scaling data governance across thousands of tables, enforcing
regulatory classifications, and reducing manual grant management. Enable the
preview in account settings, tag your securables, author a policy, and test it
against a sample principal.
