# Manage roles in Developer Spaces

Roles control what each person can see and do in a Developer Space. Assigning the right role helps your team collaborate securely and ensures only authorized users can manage apps, settings, and billing.

Watch this video for an overview of how to manage roles in a Developer Space.

## Roles and what they can do

Each person can have only one core role (Admin, Developer, or Viewer) in a Developer Space. Additional permissions for Marketplace admin, [Billing admin](https://support.atlassian.com/subscriptions-and-billing/docs/billing-permissions-by-role/), or [app-level roles](https://developer.atlassian.com/platform/forge/contributors/#contributors) are managed separately and may apply alongside the space role.

Each member of a Developer Space is assigned one of three roles:

| Action / Permission | Admin | Developer | Viewer |
| --- | --- | --- | --- |
| View apps | ✓ | ✓\* | ✓ |
| View members | ✓ | ✓ | ✓ |
| Create new Forge apps in the space | ✓ | ✓ |  |
| Assign apps to the space | ✓ | ✓ |  |
| Manage all apps in the space | ✓ | ✓\* |  |
| Edit space settings | ✓\*\* |  |  |
| Assign or remove members | ✓ |  |  |
| Change roles | ✓ |  |  |
| Delete or archive the space (if no apps assigned) | ✓ |  |  |
| Initiate transfer of private apps between spaces | ✓ |  |  |
| View space settings | ✓ | ✓ | ✓ |

\*Developers by default in the user experience can only view or manage apps they have access to or have been assigned the contributor permission at the app level. However, they can be provided an add-on permission to view all apps in the space in the experience.   
\*\* Only before the space is published on the Atlassian Marketplace. After publishing, edit via the [Marketplace Partner Portal](https://marketplace.atlassian.com/).

Developers and Viewers can see the settings page, but all actions are disabled for them. Only Admins can make changes.

## Special roles: Billing and Marketplace admins

Some permissions are managed outside the Developer Space:

* **Billing admin:**
  * The first Admin in a new Developer Space is also made the billing admin for the linked transaction account.
  * Billing admins can view invoices, update payment methods, manage other billing admins, view all Developer Space apps, their resource usage and costs, and both billing and sold-to addresses in the [Billing Console](https://billing.atlassian.com/). For a complete list of their permissions, see [Billing permissions by role](https://support.atlassian.com/subscriptions-and-billing/docs/billing-permissions-by-role/).
  * To manage apps or settings in a Developer Space, a billing admin must also be assigned a core role in the space.
* **Marketplace admin:**
  * Managed in the [Marketplace Partner Portal](https://marketplace.atlassian.com/).
  * Marketplace admins can edit space metadata (name, logo) after the space is published on the Marketplace.
  * To manage apps or settings in a Developer Space, a Marketplace admin must also be assigned a core role in the space.

## Add a team member

Only Admins can assign or change roles for other members.

**To assign a role:**

1. Go to your Developer Space in the **Developer Console**.
2. Select **Members**.
3. Select **Add members**.
4. Enter the email address.
5. Select the role.
6. Select **Add**.

You can have multiple Admins and Developers in a space.

Billings admin can be added to the Developer Space billing account only via the [Billing Console](https://billing.atlassian.com/).

## How to remove a member

Only Admins can remove members from a Developer Space.

**To remove a member:**

1. Go to the **Members** section.
2. Select the user.
3. Select **Remove**.

Removing a member immediately revokes their access to all apps and settings in that space.

Billings admin can be removed from the Developer Space billing account only via the [Billing Console](https://billing.atlassian.com/).

## Automatic app viewer access

When a user is assigned as an admin or a viewer in a Developer Space, they automatically become an [app viewer](https://developer.atlassian.com/platform/forge/contributors/#contributors) for all Forge apps within that space. This viewer access is granted at the space level to ensure admins and viewers always have visibility into all apps for management and support purposes. Developers do not automatically have access to view all apps in the space, but they can be granted an additional permission that allows them to see every app within the Developer Space.

[App admins](https://developer.atlassian.com/platform/forge/contributors/#contributors) on individual apps can't remove Developer Space admins from this viewer role.

Only removing the user from the Developer Space itself will revoke their viewer access to the apps.

## Best practices

* **Always have more than one admin** → Prevents lockout if someone leaves.
* **Review team membership regularly** → Remove users who no longer need access.
* **Assign roles carefully** → Only give full control to trusted team members.
* **Document ownership** → Ensure apps and billing accounts have clear owners.
