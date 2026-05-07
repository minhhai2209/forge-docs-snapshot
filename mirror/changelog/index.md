# Forge changelog

Hello Marketplace partners,

We're excited to share that the newest improvements to Atlassian’s design language is here, as you may have seen at Team '26!

These build upon on our refreshed visual language that launched last year at Team ’25 (including colour, typography, and iconography that many of you already adopted). It makes it even easier to build modern UI that is cohesive across Atlassian and Marketplace apps, with better visual clarity and accessibility.

These improvements are being shipped as components, design tokens and guidance updates to the Atlassian Design System (ADS) and Forge UI Kit, featuring new/updated:

* Tile system and components (including objects)
* Labelling system and components (for status and categorisation)
* Shape – Border & Radius foundations
* Motion foundations
* Spotlight component

## What's coming soon

The following are in development behind feature gates. To preview the new improvements please find more details on <https://atlassian.design/>.

### 🎨 Tile & Object System

The Tile & Object system replaces inconsistent custom tile-like UI elements — previously scattered across products with mismatched sizes, radii, colours, and naming conventions. We now offer a single, coherent standard for representing tasks, pages, objects, and app icons.

Changes are coming to [Avatar](https://atlassian.design/components/avatar/examples "https://atlassian.design/components/avatar/examples"), [Icon tile](https://atlassian.design/components/icon/icon-tile "https://atlassian.design/components/icon/icon-tile"), [Tile](https://atlassian.design/components/tile/overview "https://atlassian.design/components/tile/overview") and [Object](https://atlassian.design/components/object/object-explorer "https://atlassian.design/components/object/object-explorer") packages to align with the new Tile system. The [Icon object](https://atlassian.design/components/icon-object/icon-explorer "https://atlassian.design/components/icon-object/icon-explorer") package has been deprecated and replaced by [Object](https://atlassian.design/components/object/object-explorer "https://atlassian.design/components/object/object-explorer"). Adoption details are landing soon — stay tuned.

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

### **🏷️ Labelling & Categorization System - Phase 1**

Atlassian's product ecosystem currently lacks a cohesive and standardised approach to object labelling. Each product has developed its own patterns and components for representing status, tags, verification, and classification, leading to inconsistent experiences as products become more integrated.

With our improvements to labelling we have introduced a visual uplift for the components used to label, tag, and categorise content across Atlassian apps: [Lozenges](https://atlassian.design/components/lozenge/lozenge/examples "https://atlassian.design/components/lozenge/lozenge/examples"), [Tags](https://atlassian.design/components/tag/tag/examples "https://atlassian.design/components/tag/tag/examples"), and [Badges](https://atlassian.design/components/badge/examples "https://atlassian.design/components/badge/examples"). We have also introduced a new [Lozenge dropdown variant](https://atlassian.design/components/lozenge/lozenge-dropdown-trigger "https://atlassian.design/components/lozenge/lozenge-dropdown-trigger") and a new [Avatar tag](https://atlassian.design/components/tag/avatar-tag/examples "https://atlassian.design/components/tag/avatar-tag/examples"). Please note that subtle lozenges are deprecated - replaced by tags for non status lozenges. Our aim is to create a unified, extensible labelling system that:

* Powers consistent experiences across the Atlassian ecosystem
* Supports product-specific needs while maintaining coherence
* Facilitates future innovations in work management and discovery
* Reduces implementation effort for product teams
* Reduces cognitive load for customers

This is Phase 1 of a broader labelling system that will enable consistent semantics in Phase 2.

*Updated components: Badge, Lozenge, ad Tag*

*New components: Lozenge Dropdown and Avatar tag*

### **✨ Motion Foundations - Phase 1 (Early access)**

Motion breathes life into every interaction and brand moment within apps, helping users understand spatial relationships, confirms their actions, and carries branded human expression across experiences. Our approach to motion introduces a systematic, shared language, enabling you to make good motion **the easy default**, not an exception.

With this early access release, we will be introducing semantic motion tokens and base tokens as the foundation of the system. Uplifted and new motion in key Atlassian Design System components will be coming as well as an [improved motion primitive](https://atlassian.design/components/motion/motion-primitive/examples "https://atlassian.design/components/motion/motion-primitive/examples") to replace legacy entering components and simplify applying entry and exit transitions in UI.

Check out our [motion foundation guidelines](https://atlassian.design/foundations/motion "https://atlassian.design/foundations/motion") to familiarise yourself with the upcoming changes.

*Motion package before vs after*
