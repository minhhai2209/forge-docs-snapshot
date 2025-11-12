# Logging guidelines for app developers

|  |  |  |
| --- | --- | --- |
| Name | No | This is a direct identifier. |
| User ID - Email Address | No | This is a direct identifier. |
| User ID - Username | No | This is a direct identifier. |
| Session ID | No | This is an indirect identifier which could be used, in association with other data, to identify a user. |
| User Generated Content | No | This is content that could include personal data or confidential customer data. |
| Source IP Address / Dest IP | Log with caution | This is an indirect identifier which could be used, in association with other data, to identify a user. |
| X-Forwarded-For | Log with caution | This is an indirect identifier which could be used, in association with other data, to identify a user. |
| URL path and query string | Log with caution | This is an indirect identifier which could be used, in association with other data, to identify a user. Avoid passing usernames or other non-arbitrary identifiers in URL paths or query strings. |
| User Agents | Log with caution | This is an indirect identifier which could be used, in association with other data, to identify a user. |
| AaID (Atlassian Account ID) | Log with caution | This is an indirect identifier which could be used, in association with other data, to identify a user. |
| Nickname | Log with caution | This is an indirect identifier which could be used, in association with other data, to identify a user. |
| User ID | Log with caution | This is an indirect identifier which could be used, in association with other data, to identify a user. |
| Member ID | Log with caution | This is an indirect identifier which could be used, in association with other data, to identify a user. |
| Site ID | Log with caution | This is an indirect identifier which could be used, in association with other data, to identify a user. |
| Cloud ID | Log with caution | This is an indirect identifier which could be used, in association with other data, to identify a user. |
| Tenant ID | Log with caution | This is an indirect identifier which could be used, in association with other data, to identify a user. |
| Tenant Name | Log with caution | This is an indirect identifier which could be used, in association with other data, to identify a user. |
