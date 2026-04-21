---
name: shopify-app-dev
description: Use this skill when building a Shopify app (public App Store app, custom merchant app, or extension-only app) using the Shopify CLI, Remix template, Polaris, App Bridge, or writing checkout/admin/theme extensions and Shopify Functions. Triggers on "create a Shopify app", "Shopify CLI" with app context, "shopify app generate", "checkout UI extension", "admin UI extension", "Shopify Functions", or imports of @shopify/shopify-app-remix, @shopify/polaris, @shopify/app-bridge-react.
---

# Shopify App Development

Shopify apps extend the platform. Use the CLI, Remix-based template, and the App Bridge/Polaris UI kit.

## App types

| Type | Use case | Distribution |
|---|---|---|
| **Public app** | For many merchants via the App Store | Listed, approved, earns revenue |
| **Custom app** | For specific named merchants | Install link, no approval |
| **Extension-only** | No embedded UI, only extensions | Lighter, often admin/theme/checkout extensions |
| **Private app** (legacy) | Deprecated, pre-2022 stores only | Do not build new private apps |

Unless you explicitly need the App Store, start with a **custom app** — same codebase, fewer approval hoops.

## Quickstart

```bash
npm install -g @shopify/cli@latest
npm init @shopify/app@latest

# Pick Remix template (default, recommended)
# CLI scaffolds: web/ (Remix), extensions/, shopify.app.toml

cd my-app
npm run dev
# Creates a tunnel, installs into your dev store, opens embedded admin
```

`shopify.app.toml` is the source of truth for app config — scopes, URLs, webhooks. Commit it.

## Project structure (Remix template)

```
my-app/
├── app/                     # Remix routes, loaders, actions
│   ├── routes/
│   │   ├── app._index.tsx   # Main embedded admin page
│   │   ├── app.tsx          # Embedded layout (NavMenu, AppBridge)
│   │   ├── webhooks.*.tsx   # Webhook handlers
│   │   └── auth.$.tsx       # OAuth callback
│   ├── shopify.server.ts    # Shopify App object + auth
│   └── db.server.ts         # Prisma session storage
├── extensions/              # CLI-generated extensions
├── prisma/
│   └── schema.prisma        # Session storage schema (SQLite default)
└── shopify.app.toml
```

## Authentication + session

The Remix template handles OAuth automatically via `@shopify/shopify-app-remix`. In loaders/actions:

```typescript
import { authenticate } from "~/shopify.server";

export const loader = async ({ request }: LoaderFunctionArgs) => {
  const { admin, session } = await authenticate.admin(request);
  // admin.graphql(query, { variables }) — auto-authenticated
  const response = await admin.graphql(`#graphql
    query { shop { name email } }`);
  return json(await response.json());
};
```

Session storage: default SQLite via Prisma. For production, swap to Postgres/MySQL by updating `DATABASE_URL` and `prisma/schema.prisma`.

## Embedded admin UI with Polaris + App Bridge

Polaris is Shopify's React component library. Stay in Polaris — merchants expect the look & feel.

```tsx
import { Page, Card, Button, TextField, BlockStack } from "@shopify/polaris";
import { TitleBar, useAppBridge } from "@shopify/app-bridge-react";

export default function Index() {
  const shopify = useAppBridge();
  return (
    <Page>
      <TitleBar title="My App" />
      <Card>
        <BlockStack gap="400">
          <TextField label="Name" autoComplete="off" />
          <Button variant="primary" onClick={() => shopify.toast.show("Saved")}>
            Save
          </Button>
        </BlockStack>
      </Card>
    </Page>
  );
}
```

App Bridge exposes the host admin's APIs: toast, modal, navigation, resource picker, contextual save bar. Use them instead of rolling your own.

## Extensions

Generate with `shopify app generate extension`.

### Theme app extension
Adds blocks to the merchant's storefront theme (without editing theme code).

```
extensions/my-block/
├── blocks/
│   └── app-block.liquid     # The renderable block
├── assets/
└── shopify.extension.toml
```

`app-block.liquid` uses normal Liquid + `{% schema %}`, plus `{{ shop.permanent_domain }}` + Asset URLs scoped to the app.

### Checkout UI extension
Adds functionality to the checkout (Shopify Plus for most placements, any plan for order status/thank you).

```tsx
import { reactExtension, Banner, useApi } from "@shopify/ui-extensions-react/checkout";

export default reactExtension("purchase.checkout.block.render", () => <App />);

function App() {
  const { lines } = useApi();
  return <Banner>You have {lines.current.length} items</Banner>;
}
```

Extension targets are discovery-based — see `shopify.extension.toml` for available placements.

### Admin UI extension
Adds custom UI blocks to the admin (product page, order page, customer page).

```tsx
import { reactExtension, AdminBlock, Text } from "@shopify/ui-extensions-react/admin";

export default reactExtension("admin.product-details.block.render", () => <App />);

function App() {
  return <AdminBlock title="My Block"><Text>Hello</Text></AdminBlock>;
}
```

### Functions (Shopify Functions)
Run serverless Wasm on Shopify's infra to customize checkout behavior: discounts, shipping, payment customizations, delivery method sort. Written in Rust or JavaScript.

```bash
shopify app generate extension --template=product_discounts --name=my-discount
```

## Webhooks

Register in `shopify.app.toml`:

```toml
[webhooks]
api_version = "2025-01"

[[webhooks.subscriptions]]
topics = ["orders/create", "orders/paid"]
uri = "/webhooks"

[[webhooks.subscriptions]]
topics = ["app/uninstalled"]
uri = "/webhooks/app-uninstalled"
```

Handler pattern:
```typescript
export const action = async ({ request }: ActionFunctionArgs) => {
  const { topic, shop, payload } = await authenticate.webhook(request);
  switch (topic) {
    case "ORDERS_PAID":
      // do work
      break;
  }
  return new Response();
};
```

**GDPR webhooks are required** for public apps: `customers/data_request`, `customers/redact`, `shop/redact`. Must respond 200 OK, actual data deletion within 30 days.

## Billing API

```typescript
import { authenticate } from "~/shopify.server";

const { billing } = await authenticate.admin(request);
await billing.require({
  plans: ["Pro"],
  isTest: true,
  onFailure: async () => billing.request({ plan: "Pro" }),
});
```

Plans defined in `app/shopify.server.ts`:
```typescript
billing: {
  "Pro": {
    amount: 29,
    currencyCode: "USD",
    interval: BillingInterval.Every30Days,
    trialDays: 7,
  },
}
```

Shopify takes 0% for the first $1M in app revenue (per developer per year), then 15%. This is the most generous platform take rate in commerce.

## Scopes (permissions)

In `shopify.app.toml`:
```toml
[access_scopes]
scopes = "write_products,read_orders,read_customers"
```

Request the minimum needed — App Store reviewers reject over-scoped apps. If you add scopes later, existing installs re-prompt the merchant for consent.

## App Store submission checklist

1. **Performance**: Lighthouse score ≥ 60 on storefront impact pages (if you inject scripts)
2. **Webhooks**: GDPR endpoints configured and responding 200
3. **Uninstall cleanup**: Listen for `app/uninstalled`, remove session
4. **Embedded**: Must work inside Shopify admin iframe (no X-Frame-Options blocks)
5. **Polaris**: Embedded UI uses Polaris
6. **Pricing page**: Clear plans + trial details
7. **Listing**: Screenshots, demo video, clear value prop
8. **Test store**: Reviewer gets credentials to a test store with the app installed

Approval takes 2-4 weeks. Have a reviewer's-eye demo ready.

## Tools to know

- **`shopify app dev`** — tunnel + HMR
- **`shopify app deploy`** — bumps extension versions, deploys
- **`shopify app info`** — current app config, URLs
- **`shopify app config use`** — switch between multiple `shopify.app.*.toml` (dev/staging/prod)
- **`shopify app generate`** — scaffolds extensions, webhooks
- **`@shopify/polaris`** — UI components
- **`@shopify/app-bridge-react`** — admin context (toast, modal, resource picker)
- **`@shopify/shopify-app-remix`** — Remix auth + session

## Common pitfalls

- **Don't manually handle OAuth** — use the template's `authenticate.admin()`. Custom OAuth breaks session rotation.
- **Don't store access tokens in env vars** — sessions per shop live in the DB.
- **Test with `isTest: true` billing** — real charges aren't made, but the flow is identical.
- **Embedded apps need iframe-friendly CSP** — `frame-ancestors https://admin.shopify.com https://*.myshopify.com`.
- **App URLs change with each `dev` run** (tunnel-based). For stable dev, use `shopify app dev --tunnel-url=https://your-ngrok.ngrok.io`.
