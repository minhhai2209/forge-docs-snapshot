# Manage app contributors

When managing contributors of your app, you must first ensure you're that happy with the
[roles and permissions](/platform/forge/contributors/#roles-and-permissions)
you’re giving them access to.

This page explains how to [add contributors](#add-contributors),
[edit roles of contributors](#edit-the-roles-of-contributors),
[view contributor history](#view-contributor-history),
[view deployment history](#view-deployment-history),
[manage app environments](#manage-environments),
and [transfer app ownership](#transfer-app-ownership) in the developer console.

* Only app admins can [add, edit, and remove contributors](/platform/forge/contributors/#roles-and-permissions).
* Contributors will receive an email notification when they are added to or removed from an app.
* Contributors are able to see the public name of other contributors in the developer
  console. They can also see their email address, depending on the contributor’s
  [privacy settings](https://id.atlassian.com/manage-profile/profile-and-visibility).
* Contributors are able to see their role in the
  [Contributors panel](/platform/forge/manage-your-apps/#view-forge-app-details) of the Overview page.

## View contributors

To view the contributors of an app:

1. Access the [developer console](/console/myapps).
2. Select the relevant Forge app.
3. Select **Contributors** in the left menu.

   ![Contributors list screen](https://dac-static.atlassian.com/platform/forge/images/dev-console-role-permissions/contributors_list.svg?_v=1.5800.1801)

## Add contributors

When adding a contributor to an app, the contributor will gain permissions to access the app via
the Forge CLI and developer console, depending on the role selected for them.

To add a contributor to your app:

1. Access the [developer console](/console/myapps).
2. Select the relevant Forge app.
3. Select **Contributors** in the left menu.
4. Select **Add contributors** above the table.
5. Enter the **email address** of the contributor you're adding to the app.
6. Select the **role** that you want to set for the contributor.
7. Select **Add**.

* You can also add multiple contributors by adding and separating their email addresses with a comma.
  Only 10 contributors can be added to an app at a time.
* When selecting a role for multiple contributors, note that you're setting the same role for
  *all* contributors. If you want the contributors to have different roles, we recommend
  adding them individually.
* You can optionally provide the advanced permission **view production logs** to a contributor
  of the *viewer*, *deployer*, or *developer* role. See
  [app monitoring activities](/platform/forge/contributors/#app-monitoring-activities) to know more.

## Edit the roles of contributors

To edit the role of a contributor:

1. Access the [developer console](/console/myapps).
2. Select the relevant Forge app.
3. Select **Contributors** in the left menu.
4. Select the **More actions (⋯)** menu for the contributor whose role you're editing.
5. Select **Edit role**.
6. In the popup that appears, select the **new role**.
7. Select **Save changes**.

* You can edit the roles of multiple contributors by selecting the checkboxes of the relevant
  contributors and selecting **Edit role**.
* When selecting a role for multiple contributors, note that you're setting the same role for
  *all* contributors. If you want the contributors to have different roles, we recommend
  editing them individually.
* You can optionally provide the advanced permission **view production logs** to a contributor of the
  *viewer*, *deployer*, or *developer* role. See
  [app monitoring activities](/platform/forge/contributors/#app-monitoring-activities) to know more.

## Remove contributors

To remove a contributor from an app:

1. Access the [developer console](/console/myapps).
2. Select the relevant Forge app.
3. Select **Contributors** in the left menu.
4. Select the **More actions (⋯)** menu for the contributor whose role you're editing.
5. Select **Remove**.
6. In the popup that appears, confirm the removal by selecting **Remove**.

You can remove multiple contributors by selecting the checkboxes of the relevant contributors
and selecting **Remove**. In the popup that appears, confirm the removal by selecting **Remove**.

## View contributor history

Only app admins can
[view contributor history](/platform/forge/contributors/#app-monitoring-activities)
and [manage contributors](/platform/forge/contributors/#app-and-contributor-management-activities).

To see which contributors have been added, edited, or removed from your app:

1. Access the [developer console](/console/myapps).
2. Select the relevant Forge app.
3. Select **Contributors** in the left menu.
4. Select the **Activity** tab.

![Contributors activity screen](https://dac-static.atlassian.com/platform/forge/images/dev-console-role-permissions/contributor_activity.svg?_v=1.5800.1801)

The screen shows when contributors have been added, changed, removed, or changed to app owner.
It also shows who completed the action.

You can narrow the list down using the filters above the table.

* By default, the table is sorted by Date/Time (UTC), with the most recent actions appearing at the top.
* The **contributor name or email** filter only shows contributors who have been added or removed
  since this functionality was released. You can work around this limitation by removing and adding the
  contributors again - they will then appear in the filter.

## View deployment history

To view the deployment history for your app:

1. Access the [developer console](/console/myapps).
2. Select the relevant Forge app.
3. Select **Deployments** in the left menu.

![Deployments screen](https://dac-static.atlassian.com/platform/forge/images/dev-console-role-permissions/deployments-screen.svg?_v=1.5800.1801)

The screen shows a list of recent deployments, across all contributors, as well as
[environments and versions](/platform/forge/environments-and-versions/).
You can narrow the list down using the filters and search bar above the table.

## Manage environments

When you add a contributor, a new development environment is created for them.

To view the environments for all contributors:

1. Access the [developer console](/console/myapps).
2. Select the relevant Forge app.
3. Select **Environments** in the left menu.

![Environments screen](https://dac-static.atlassian.com/platform/forge/images/dev-console-role-permissions/environments-screen.svg?_v=1.5800.1801)

To delete an environment, select **Delete** under the Actions column.

## Transfer app ownership

To transfer ownership of your app:

1. Access the developer console.
2. Select the relevant Forge app.
3. Select **Contributors** in the left menu.
4. In the **Actions** column next to your name, select **Change owner**.
5. Follow the instructions to select a new owner.

   ![Transfer app ownership modal](https://dac-static.atlassian.com/platform/forge/images/transfer-app-ownership-step2.png?_v=1.5800.1801)
6. If you’re happy with the new owner, select **Confirm transfer**.

   ![Transfer app ownership modal confirmation](https://dac-static.atlassian.com/platform/forge/images/transfer-app-ownership-step3.png?_v=1.5800.1801)

* You can also transfer ownership from the **Settings** screen of the app.
* If the app owner is deactivated or unavailable, contact
  [Atlassian support](https://ecosystem.atlassian.net/servicedesk/customer/portal/34/group/3534/create/4180).
  to assist you with transferring app ownership.
* If a contributor’s Atlassian account gets deactivated or deleted, they will still remain a contributor
  of the app. The app owner will have to manually remove them as a contributor.
