---
name: shopify-admin-api
description: Use this skill when reading or writing store data via the Shopify Admin API (REST or GraphQL) — create or update a product, manage orders, customers, inventory, metafields, or register webhooks programmatically. Triggers on "Shopify Admin API", "create a product via API", "GraphQL Admin mutation", "productCreate", "fetch orders from Shopify", "bulk update inventory", "Shopify webhook HMAC verify", or code that hits /admin/api/ endpoints or imports shopify-api / @shopify/shopify-api.
---

# Shopify Admin API

Use the Admin API to read and write every aspect of a Shopify store programmatically: products, variants, inventory, orders, customers, fulfillments, discounts, metafields, collections, draft orders, etc.

## Choosing REST vs GraphQL

**GraphQL is the default for new work** — Shopify has frozen REST and is actively deprecating endpoints. Use REST only for legacy integrations or when a GraphQL equivalent is missing.

| | REST | GraphQL |
|---|---|---|
| Endpoint | `/admin/api/2025-01/*.json` | `/admin/api/2025-01/graphql.json` |
| Rate limit | 2 calls/sec leaky bucket | Query cost-based (50 points/sec restore) |
| Bulk ops | Paginated, no bulk | `bulkOperationRunQuery` / `bulkOperationRunMutation` |
| Deprecation | Frozen (no new features) | Actively developed |

## Authentication

Three options depending on use case:

1. **Custom app tokens** (easiest, single store) — generate in Admin → Apps → Develop apps. Use `X-Shopify-Access-Token` header.
2. **OAuth** (public/distributable apps) — required for App Store or multi-store installs. Use `@shopify/shopify-api` library.
3. **Private app** (deprecated, pre-2022 only) — basic auth with API key + password.

```javascript
// Custom app — simplest
const response = await fetch(
  `https://${shop}.myshopify.com/admin/api/2025-01/graphql.json`,
  {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-Shopify-Access-Token": process.env.SHOPIFY_ADMIN_TOKEN,
    },
    body: JSON.stringify({ query, variables }),
  }
);
```

## Rate limiting

GraphQL uses **calculated query cost** returned in `extensions.cost`:

```json
"cost": {
  "requestedQueryCost": 52,
  "actualQueryCost": 3,
  "throttleStatus": { "maximumAvailable": 1000, "currentlyAvailable": 997, "restoreRate": 50 }
}
```

Pattern: read `throttleStatus.currentlyAvailable`, back off if below your query cost, sleep for `(needed - available) / restoreRate` seconds. Shopify Plus stores get higher limits (2000 points, 100/sec).

REST: watch `X-Shopify-Shop-Api-Call-Limit: 39/40` header. Back off at 80%.

## GraphQL essentials

Product create:
```graphql
mutation productCreate($input: ProductInput!) {
  productCreate(input: $input) {
    product { id title variants(first: 5) { nodes { id price } } }
    userErrors { field message }
  }
}
```

**Always read `userErrors`** — mutations can return HTTP 200 with business-logic errors inside.

Pagination uses Relay cursor connections:
```graphql
products(first: 50, after: $cursor) {
  pageInfo { hasNextPage endCursor }
  nodes { id title }
}
```

## Bulk operations

For > 1000 records, use Bulk Operations instead of pagination — runs async, returns a JSONL file URL:

```graphql
mutation {
  bulkOperationRunQuery(query: """
    { products { edges { node { id title variants { edges { node { id sku } } } } } } }
  """) { bulkOperation { id status } userErrors { message } }
}
```

Poll `currentBulkOperation` until `status: COMPLETED`, then download `url` (JSONL).

Only one bulk op per type (query/mutation) runs at a time per shop.

## Webhooks

Register via GraphQL `webhookSubscriptionCreate` or the Admin UI. Always verify HMAC:

```javascript
import crypto from "crypto";
const hmac = req.headers["x-shopify-hmac-sha256"];
const digest = crypto.createHmac("sha256", SHOPIFY_API_SECRET)
  .update(rawBody).digest("base64");
if (digest !== hmac) return res.status(401).end();
```

Topics to know: `orders/create`, `orders/paid`, `products/update`, `app/uninstalled`, `customers/data_request` (GDPR — required for public apps).

## Common pitfalls

- **`id` format**: GraphQL uses GIDs (`gid://shopify/Product/123`), REST uses numeric IDs. Convert with `shopify-api` helpers or string splitting.
- **Metafields**: Use `metafieldsSet` mutation (bulk, upsert semantics) rather than create/update individually.
- **Inventory**: Inventory belongs to `InventoryLevel`, not the variant. Update via `inventoryAdjustQuantity` or `inventorySetQuantities`.
- **Images**: Use `productCreateMedia` (async) — poll the `Media.status` until `READY`.
- **Currency**: Money fields return `{ amount: "12.00", currencyCode: "USD" }` — never do math on strings; parse to number first.

## API version policy

Shopify ships a new API version quarterly (`YYYY-MM`). Each version is supported for 12 months. Pin the version explicitly in the URL — do not use `/admin/api/unstable/`.

## Libraries

- **Node**: `@shopify/shopify-api` (official, handles OAuth + session storage)
- **Ruby**: `shopify_api` gem
- **PHP**: `shopify/shopify-api`
- **Python**: `ShopifyAPI` package (community, less maintained — consider raw `httpx`)
