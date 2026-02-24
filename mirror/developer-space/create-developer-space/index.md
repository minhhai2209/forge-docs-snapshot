# Create a Developer Space

A Developer Space is required for building, managing, and billing Forge apps. Every new Forge app must be created in a Developer Space, and all existing private apps must be assigned to one. This page explains how to create a Developer Space and what to expect during setup.

Watch this video for an introduction to creating a Developer Space.

## Who can create a Developer Space?

Anyone with an Atlassian account and access to the Developer Console or Forge CLI can create a Developer Space.

* The first person to create a Developer Space becomes the space admin.
* For new spaces, the first admin is also assigned as the billing admin for the linked transaction account in the Billing Console. Once the first space admin with billing admin permissions is assigned, they will be able to add more members with [developer space roles](/platform/forge/developer-space/developer-space-roles/) in the [developer console](https://developer.atlassian.com/console/myapps/) and [billing admin role](https://developer.atlassian.com/platform/forge/developer-space/developer-space-roles/#special-roles--billing-and-marketplace-admins) in the billing account respectively.
* If you are a Marketplace partner, your existing Marketplace vendor account will be automatically ported into Developer Spaces and will be visible in the Developer Console. This is the same account you use on the Marketplace, and all your published apps on the Marketplace are automatically linked to your Developer Space.

![](https://dac-static.atlassian.com/platform/forge/images/developer_space_mp_admin.png?_v=1.5800.1875)

The Marketplace admin can nominate the first space admin who also becomes the billing admin for the **initial setup only**. Once the first space admin with billing admin permissions is nominated, they will be able to add more members with [developer space roles](/platform/forge/developer-space/developer-space-roles/) in the [developer console](https://developer.atlassian.com/console/myapps/) and [billing admin role](https://developer.atlassian.com/platform/forge/developer-space/developer-space-roles/#special-roles--billing-and-marketplace-admins) in the billing account respectively.

## Before you start

## How to create a Developer Space

### Using the Developer Console

1. Go to <https://developer.atlassian.com/>.
2. Select your profile icon in the top-right corner and select **Developer Console**.
3. In the Developer Console, select **Create Developer Space** from the space switcher at the top left.  
   You may also see a banner at the top of the Developer Console that lets you create a Developer Space directly from there.
4. Enter a name for your Developer Space.  
   See [Naming your Developer Space](/platform/forge/developer-space/create-developer-space/#naming-your-developer-space) for rules and tips.
5. Confirm your details.
6. Select **Create**.

After creation, you will see your new Developer Space. You will be the space admin and, if this is a new space, also the billing admin for the linked transaction account.

### Using the Forge CLI

You can also create a Developer Space using the Forge CLI.  
Refer to the [Forge CLI](https://developer.atlassian.com/platform/forge/cli-reference/) for detailed instructions.

### Naming your Developer Space

* Allowed characters: letters, numbers, spaces, dashes (-), and underscores (\_).
* Names are case-insensitive.
* HTML tags and special characters are not allowed.
* Choose a name that clearly identifies your team, project, or organization.

## After creation

Once your space is created:

* You’ll see a confirmation message: **Your Developer Space has been created.**
* You’ll land in your new (empty) space.
  * The empty state will guide you to create a new app, assign an existing app, or transfer a private app from another space.

As the admin, you’ll be responsible for managing access and paying for any usage charges. You can add teammates and assign roles later.

## Next steps

## FAQ

* **Who can create a developer space?**
  Anyone with an Atlassian account and access to the Developer Console or Forge CLI can create a Developer Space.
* **Do I need a space to build apps?**
  Yes, all apps must belong to a space.
* **How do I delete a space?**
  If no apps are assigned, you can delete it. See [Manage Developer Space settings](/platform/forge/developer-space/manage-developer-space/)
* **What if I am a Marketplace partner?**
  The Marketplace admin can access the Developer Space and nominate the first space admin, who will also become the billing admin for the linked transaction account.
* **How is the billing admin assigned?**
  The first admin of a new Developer Space is also assigned as the billing admin for the linked transaction account. Additional billing admins are managed in the [Billing Console](https://admin.atlassian.com/billing).
