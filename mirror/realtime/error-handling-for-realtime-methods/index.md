# Error handling for Realtime methods

Forge Realtime is now available as Preview capability. Preview capabilities are deemed stable; however, they remain under active development and may be subject to shorter deprecation windows. Preview capabilities are suitable for early adopters in production environments.

We release preview features so partners and developers can study, test, and integrate them prior to General Availability (GA). For more details, see [Forge EAP, Preview, and GA](/platform/forge/whats-coming/#preview).

Expected errors are the same between the associated [Realtime events API](/platform/forge/runtime-reference/realtime-events-api/) and [Realtime bridge API](/platform/forge/apis-reference/ui-api-bridge/realtime/) operations. Each operation (`publish`, `subscribe` and `signRealtimeToken`) has a different error pattern:

* **publish** — returns a `PublishResult` object. On error, `eventId` and `eventTimestamp` will be `null` and `errors` will return a list of errors. This is the same for **publishGlobal**.

  ```
  1
  2
  3
  4
  5
  interface PublishResult {
    eventId: string | null;
    eventTimestamp: string | null;
    errors: RealtimeError[];
  }
  ```

  ```
  1
  2
  3
  4
  const result = await realtime.publish('my-channel', 'my-payload');
  if (result.errors.length > 0) {
    console.error('Publish failed:', result.errors.map(e => e.message));
  }
  ```
* **subscribe** — returns a rejected `Promise` on error. This is the same for **subscribeGlobal**.

  ```
  1
  2
  3
  4
  5
  try {
    const subscription = await realtime.subscribe('my-channel', onEvent);
  } catch (error) {
    console.error('Subscription failed:', error.message);
  }
  ```
* **signRealtimeToken** — returns a `TokenResult` object. On error, `token` and `expiresAt` will be `null` and `errors` will return a list of errors.

  ```
  ```
  1
  2
  ```



  ```
  interface TokenResult {
    token: string | null;
    expiresAt: number | null;
    errors: RealtimeError[];
  }
  ```
  ```

  ```
  ```
  1
  2
  ```



  ```
  const result = await signRealtimeToken('my-channel', customClaims);
  if (result.errors.length > 0) {
    console.error('Token signing failed:', result.errors.map(e => e.message));
  }
  ```
  ```

## Rate limit exceeded error

Rate limits are applicable for all Realtime methods. See [Realtime limits](/platform/forge/limits-realtime/) for the applied rates.

This limit will be enforced starting 26 June 2026.

| error.message | Description |
| --- | --- |
| `RATE_LIMIT_EXCEEDED` | The number of Realtime operations for this app installation has exceeded the allowed limit. Apps are required to handle retries. We recommend using a retry backoff strategy when re-attempting failed requests. |

## Forge Realtime token pre-validation error

These errors occur when a provided Realtime token fails validation before the operation is executed. Operations that return a prevalidation error are **not** counted towards rate limiting. See [Realtime token API](/platform/forge/runtime-reference/realtime-events-api/#using-the-token-argument-to-secure-channel-context) for how to sign and use a token to secure your channel.

The following error messages apply to `publish` and `subscribe` methods:

| error.message | Description |
| --- | --- |
| `Realtime token validation failed: INVALID_TOKEN` | The provided Realtime token is malformed or could not be verified. Ensure the token was generated using `signRealtimeToken` and has not been modified. |
| `Realtime token validation failed: TOKEN_EXPIRED` | The provided Realtime token has expired. Generate a new token before retrying. |
| `Realtime token validation failed: CHANNEL_NAME_MISMATCH` | The token was signed for a different channel. Ensure the channel name in `signRealtimeToken` matches the channel name used in the publish or subscribe call. |

## Other errors

These errors occur when an operation is rejected after passing token prevalidation. Unlike prevalidation errors, these operations **are** still counted towards rate limiting.

| Applicable methods | error.message | Description |
| --- | --- | --- |
| all | `Unauthorized request` | The current user or app installation may not have the required permissions to perform this operation on the channel. Verify that the app has the correct scopes and that the user has access to the channel context. |
| `publish` | `Error publishing event to channel` | The event could not be published. Verify that the current user has the required permissions and that the app has the correct scopes to publish to the channel. |
| `signRealtimeToken` | `Error signing realtime token` | The token could not be signed. Verify that the `channel` and `claims` arguments are valid and that the app has the required permissions to sign tokens. |
