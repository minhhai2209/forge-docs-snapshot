# Work with apps in Developer Spaces

Developer Spaces are required for building, managing, and billing Forge apps. All apps, including Marketplace and private apps, must be assigned to a Developer Space. This page explains how to view, assign, create, and transfer apps within Developer Spaces.

Watch this video for an overview of how to view and assign apps to a Developer Space.

## Viewing apps in a Developer Space

When you open the Developer Console, you can view all apps you have access to.

* Use the space switcher at the top left to select a specific Developer Space and see only the apps assigned to that space.
* If you have unassigned apps, an **Assign** button appears in the Developer Space column, and a banner will also show, prompting you to assign them to a Developer Space.

## Assigning apps to a Developer Space

All apps must be assigned to a Developer Space for management and billing.

**To assign an app:**

1. In the Developer Console, locate the app in your list of all app.
2. Select **Assign** in the Developer Space column.

3. Select the target Developer Space from the list.
4. Confirm the assignment.

**Notes:**

* Only Admins and Developers in a Developer Space can assign or manage apps for which they have the admin role.
* Viewers can see apps but can't make changes.
* If you don't have permission to assign an app, contact a space Admin.

**If you have unassigned apps:**  
A banner will appear at the top of the Developer Console prompting you to assign your apps.

## Transferring apps between Developer Spaces

The process for transferring apps between Developer Spaces depends on whether your app is a Private app or a Marketplace app.

**Private apps:**

* Transfers of private apps between Developer Spaces currently require support intervention.
* Contact [Atlassian support](https://developer.atlassian.com/support) and provide details about the app and the spaces involved. Include the app name, app ID, current Developer Space ID, and the target Developer Space ID.

**Marketplace apps:**

The process for transferring apps is subject to change. We’ll update this documentation as soon as a self-serve or automated transfer flow becomes available in the Developer Console.

## Creating new apps in a Developer Space

All new Forge apps must be created within a Developer Space.

**To create a new app:**

1. Open your terminal and use the Forge CLI.
2. Run the `forge create` command (or a similar command).
3. During the process, you will be prompted to select the Developer Space where you want to create the app. You can also choose to create a new Developer Space at this step.
4. Follow the prompts to complete app creation.

For more details, see the [Forge CLI reference](/platform/forge/cli-reference/).

## Troubleshooting and common issues

* **Cannot assign app:** Ensure you have Admin or Developer permissions in the target Developer Space, as well as admin permissions for the app you are assigning.
* **No available spaces:** Create a new Developer Space before assigning or creating apps.
* **Assignment errors:**
  * If you don't have permission to assign an app to a space, you will be prompted to contact an Admin.
  * Assignment may fail if there are billing or compliance issues. Follow the on-screen instructions or contact support if you need assistance.
* **Need to transfer an app:** Contact [Atlassian support](https://developer.atlassian.com/support) for assistance with app transfers.
