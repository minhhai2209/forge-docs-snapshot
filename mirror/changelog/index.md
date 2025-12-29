# Forge changelog

We have fixed an issue in how compute usage was calculated for async events and scheduled triggers in Forge apps.

This change was rolled out progressively between Dec 17, 2025 and Dec 19, 2025. As a result, affected apps may now report higher compute usage than before. This reflects more accurate tracking of the resources consumed; there is no change to the actual behavior or performance of your apps.

If you have alerts, monitoring, or internal reports based on Forge usage metrics, you may want to review them to account for this correction.
