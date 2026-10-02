# Forge changelog

**What's changing**

The Forge `rovo:skill` module has progressed from the Early Access Program (EAP) to Preview. This module lets you package reusable instructions, supporting reference files, and optional Rovo action dependencies that Forge Rovo agents can load for specialized tasks.

Rovo skills are now available to all Forge developers without an EAP sign-up and are suitable for early adopters in production environments. You can use skills to keep an agent’s main prompt focused while moving task-specific procedures, multi-step action orchestration, validation, and error-recovery guidance into reusable `SKILL.md` files.

During Preview:

* Apps that declare `rovo:skill` can be deployed to development, staging, and production environments.
* Skill-to-skill dependencies aren't supported.
* Executable skill sources, including scripts, aren't supported.
* Agents select skills based on their descriptions and the user’s request; explicit invocation by skill name isn't supported.

**What you need to do**

If you already use Rovo skills through the EAP, no manifest changes are required. Redeploy your app to the environment where you want to use it.

To add a skill to a Forge Rovo agent:

1. Create a skill directory containing a `SKILL.md` file that follows the [Agent skills specification](https://developer.atlassian.com/platform/forge/manifest-reference/modules/rovo-skill/ "https://developer.atlassian.com/platform/forge/manifest-reference/modules/rovo-skill/").
2. Declare the directory in a `rovo:skill` module and list any Forge actions it depends on.
3. Add the skill module key to the `skills` property of your [rovo:agent module](https://developer.atlassian.com/platform/forge/manifest-reference/modules/rovo-agent/ "https://developer.atlassian.com/platform/forge/manifest-reference/modules/rovo-agent/").
4. Deploy and test the app in your target environment.
