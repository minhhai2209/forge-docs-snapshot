# Forge changelog

EDITED 8 May 2026

Hello Marketplace partners,

We're excited to share that the newest improvements to Atlassian’s design language is here, as you may have seen at Team '26!

These build upon on our refreshed visual language that launched last year at Team ’25 (including colour, typography, and iconography that many of you already adopted). It makes it even easier to build modern UI that is cohesive across Atlassian and Marketplace apps, with better visual clarity and accessibility.

We will be shipping these improvements to components, design tokens and guidance as part of the Atlassian Design System (ADS), and Forge UI Kit will also receive updates.

The following are in development behind feature gates. To preview the new improvements, please see [Atlassian Design System documentation](https://atlassian.design/design-system "https://atlassian.design/design-system"). We will share adoption and migration details once they are ready for use in your apps.

## 🎨 Tile & Object system

The Tile & Object system replaces inconsistent custom tile-like UI elements — previously scattered across products with mismatched sizes, radii, colours, and naming conventions. We now offer a single, coherent standard for representing tasks, pages, objects, and app icons.

Changes are coming to [Avatar](https://atlassian.design/components/avatar/examples "https://atlassian.design/components/avatar/examples"), [Icon tile](https://atlassian.design/components/icon/icon-tile "https://atlassian.design/components/icon/icon-tile"), [Tile](https://atlassian.design/components/tile/overview "https://atlassian.design/components/tile/overview") and [Object](https://atlassian.design/components/object/object-explorer "https://atlassian.design/components/object/object-explorer") packages to align with the new Tile system. The [Icon-object](https://atlassian.design/components/icon-object/icon-explorer "https://atlassian.design/components/icon-object/icon-explorer") package has been deprecated and replaced by [Object](https://atlassian.design/components/object/object-explorer "https://atlassian.design/components/object/object-explorer").

*Before/After of Tile System in Jira*

### **💡 Spotlight Component**

We are introducing a modernised onboarding component for product tours and user engagement flows consistent with our improved design language. The new [Spotlight](https://atlassian.design/components/spotlight "https://atlassian.design/components/spotlight") replaces the deprecated [Onboarding](https://atlassian.design/components/onboarding/examples "https://atlassian.design/components/onboarding/examples") component.

*Before: Onboarding Component*

*After: Spotlight Component*

### **📦 Shape Foundations: Border & Radius**

New design tokens for border widths and corner radii bring consistency to the shape language across Atlassian UI. Atlassian Design System components will be updated as well as the `@atlaskit/tokens` package.

Together, these foundations ensure components feel more unified and polished — rounded corners and border styles will follow a consistent system rather than being defined ad-hoc per component. For more information on whats to come, check out our [border width](https://atlassian.design/foundations/border "https://atlassian.design/foundations/border") and [radius](https://atlassian.design/foundations/radius "https://atlassian.design/foundations/radius") docs.

*New radius tokens*

*New border width tokens*

### **🏷️ Labelling system (for status and categorisation)**

We’re introducing a more intuitive, accessible, and scalable labelling system that standardises consistent presentation of statuses and categorisation, supporting app-specific needs while maintaining coherence and visual clarity.

We’ve updated the visual appearance of [Lozenges](https://atlassian.design/components/lozenge/lozenge/examples "https://atlassian.design/components/lozenge/lozenge/examples"), [Tags](https://atlassian.design/components/tag/tag/examples "https://atlassian.design/components/tag/tag/examples"), and [Badges](https://atlassian.design/components/badge/examples "https://atlassian.design/components/badge/examples") to have the right level of prominence in the UI, and look and feel harmonious in every context they show up. Lozenges can now included a trailing metric, and we are introducing a new [Lozenge dropdown variant](https://atlassian.design/components/lozenge/lozenge-dropdown-trigger "https://atlassian.design/components/lozenge/lozenge-dropdown-trigger"), as well as a new [Avatar tag](https://atlassian.design/components/tag/avatar-tag/examples "https://atlassian.design/components/tag/avatar-tag/examples") to represent individuals, teams, or AI agents.

Additionally, to provide greater visual distinction and hierarchy between Lozenge and Tag, subtle Lozenge will be deprecated and need to be migrated to the new default Lozenge appearance, or where applicable to Tag instead.

*Updated components: Badge, Lozenge, ad Tag*

*New components: Lozenge Dropdown and Avatar tag*

### **✨ Motion Foundations - Phase 1 (Early access)**

Motion breathes life into every interaction and brand moment within apps, helping users understand spatial relationships, confirms their actions, and carries branded human expression across experiences. Our approach to motion introduces a systematic, shared language, enabling you to make good motion the easy default, not an exception.

In the initial release, we will be introducing semantic motion tokens and base tokens as the foundation of the system. Uplifted and new motion in key Atlassian Design System components are coming, as well as an [improved motion primitive](https://atlassian.design/components/motion/motion-primitive/examples "https://atlassian.design/components/motion/motion-primitive/examples") to replace legacy entering components and simplify applying entry and exit transitions in UI.  
  
Learn more about how we think about motion on [atlassian.design](https://atlassian.design/foundations/motion "https://atlassian.design/foundations/motion").

*Motion package before vs after*

## Questions or feedback?

We'd love to hear from you — please share on the [Atlassian Developer Community](https://community.developer.atlassian.com/c/atlassian-ecosystem-design/21 "https://community.developer.atlassian.com/c/atlassian-ecosystem-design/21")!
