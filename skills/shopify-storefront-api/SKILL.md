---
name: shopify-storefront-api
description: Use this skill when building headless Shopify experiences — custom storefronts, mobile apps, progressive web apps, or any client that consumes the Storefront API (GraphQL) for products, collections, cart, and checkout. Triggers on "Shopify Hydrogen", "headless Shopify", "Storefront API", "custom storefront", "Shopify Remix", "Shopify mobile app", imports of @shopify/hydrogen or @shopify/storefront-kit-react.
---

# Shopify Storefront API

Public GraphQL API for building customer-facing commerce. Unlike the Admin API (server-to-server, total store access), the Storefront API is safe to call from browsers and mobile apps — read-only for catalog, read/write for cart.

## When to use Storefront API vs. Admin API

| Use case | API |
|---|---|
| Custom storefront (Hydrogen, Next.js) | Storefront |
| Native mobile app | Storefront |
| Cart + checkout in a browser | Storefront |
| Bulk product import | Admin |
| Order fulfillment dashboard | Admin |
| Inventory sync | Admin |
| Customer data admin | Admin |

## Authentication

Two token types:

1. **Public access token** — for client-side (browser, mobile). Read-only catalog + cart. Create via Admin → Apps → Develop apps → Storefront API access.
2. **Private access token** — for server-side. Can access customer data, unpublished products. Never expose to clients.

```typescript
const response = await fetch(
  `https://${shop}.myshopify.com/api/2025-01/graphql.json`,
  {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-Shopify-Storefront-Access-Token": TOKEN,
    },
    body: JSON.stringify({ query, variables }),
  }
);
```

## Hydrogen (Shopify's Remix framework)

Hydrogen is Shopify's official React framework for headless. It bundles: Remix, Oxygen hosting (edge), the Storefront API client, and CLI.

```bash
npm create @shopify/hydrogen@latest

# Scaffolds: Remix app, Tailwind, TypeScript, Shopify CLI integration
cd my-store
npm run dev  # localhost:3000 connected to your Shopify
```

Hydrogen gives you:
- Automatic caching of Storefront API responses (edge cached)
- `useLoaderData`, `useFetcher` for data flow
- `createStorefrontClient` helper
- Deploy to Oxygen (free with your Shopify plan)

Example route:
```typescript
export async function loader({ context, params }: LoaderFunctionArgs) {
  const { storefront } = context;
  const { product } = await storefront.query(PRODUCT_QUERY, {
    variables: { handle: params.handle },
    cache: storefront.CacheLong(),
  });
  return json({ product });
}
```

## Core queries

### Product by handle
```graphql
query Product($handle: String!) {
  product(handle: $handle) {
    id
    title
    description
    featuredImage { url altText width height }
    images(first: 10) { nodes { url altText } }
    priceRange { minVariantPrice { amount currencyCode } }
    variants(first: 100) {
      nodes {
        id
        title
        availableForSale
        price { amount currencyCode }
        selectedOptions { name value }
      }
    }
  }
}
```

### Collection with pagination
```graphql
query Collection($handle: String!, $cursor: String) {
  collection(handle: $handle) {
    title
    products(first: 24, after: $cursor) {
      pageInfo { hasNextPage endCursor }
      nodes { id handle title featuredImage { url } }
    }
  }
}
```

### Search
```graphql
query Search($query: String!) {
  products(first: 20, query: $query) {
    nodes { id title handle }
  }
}
```

Query syntax supports: `title:shoes`, `vendor:Nike`, `tag:sale`, `price:>10`, combined with `AND`/`OR`.

## Cart (the new way)

The cart API replaced the deprecated "checkout" API in 2023. All carts are persistent — you get an ID, store it (cookie/localStorage), and update it across sessions.

### Create cart
```graphql
mutation CreateCart($input: CartInput!) {
  cartCreate(input: $input) {
    cart { id checkoutUrl totalQuantity cost { totalAmount { amount } } }
    userErrors { field message }
  }
}
```

Input example:
```json
{ "lines": [{ "merchandiseId": "gid://shopify/ProductVariant/123", "quantity": 1 }] }
```

### Add to cart
```graphql
mutation CartLinesAdd($cartId: ID!, $lines: [CartLineInput!]!) {
  cartLinesAdd(cartId: $cartId, lines: $lines) {
    cart { id totalQuantity lines(first: 50) { nodes { id quantity merchandise { ... on ProductVariant { title } } } } }
    userErrors { message }
  }
}
```

### Update / remove
```graphql
cartLinesUpdate(cartId: $cartId, lines: [{ id: "...", quantity: 2 }])
cartLinesRemove(cartId: $cartId, lineIds: ["..."])
```

### Checkout
Don't build your own checkout. Redirect to `cart.checkoutUrl` — Shopify's hosted checkout handles payment, shipping, tax, fraud, 3DS. It's also the only way to support Shop Pay (1-tap checkout, 1.72x conversion vs. guest).

## Customer accounts (new API)

The new **Customer Account API** (2024+) replaced the old Storefront customer queries. Uses OAuth + OIDC, gives customers a unified login across your store and `shop.app`.

```
https://shopify.com/authentication/{shop_id}/oauth/authorize
```

Hydrogen template handles this flow via `createCustomerAccountClient`.

For reads: `customer` query gives orders, addresses, profile. For writes: `customerUpdate`, `customerAddressCreate`, etc.

## Caching strategy

Storefront API responses can be heavily cached — products rarely change. In Hydrogen:

```typescript
storefront.query(QUERY, {
  cache: storefront.CacheLong(),   // 1 hour, SWR 1 day
  cache: storefront.CacheShort(),  // 1 second, SWR 10 seconds
  cache: storefront.CacheNone(),   // no cache (use for cart, customer)
  cache: storefront.CacheCustom({ mode: "public", maxAge: 60, staleWhileRevalidate: 600 }),
});
```

Rule of thumb:
- Collections, products, pages → CacheLong
- Search results → CacheShort
- Cart, customer, inventory checks → CacheNone

## Localization

The Storefront API uses context directives for country + language:

```graphql
query ProductLocalized @inContext(country: BR, language: PT_BR) {
  product(handle: "shirt") {
    title
    priceRange { minVariantPrice { amount currencyCode } }
  }
}
```

Shopify Markets automatically handles pricing, currency, tax, and shipping based on `@inContext`. Your job is to pass the right context per buyer.

## Metaobjects & metafields

Surface custom content without hardcoding. Define metaobjects in Admin → Settings → Custom data, then query:

```graphql
{
  metaobjects(type: "testimonial", first: 10) {
    nodes { id fields { key value } }
  }
  product(handle: "x") {
    metafield(namespace: "custom", key: "ingredients") { value }
  }
}
```

Expose metafields to Storefront API explicitly — they default to private.

## Common pitfalls

- **CORS**: Shopify's Storefront endpoint supports CORS for your app's origin once you add it in app config. Custom domains need explicit allowlisting.
- **Rate limits**: Storefront API is throttled per IP (60 RPS burst). Client-side calls with public tokens are fine; server-side aggregation should use Admin API with proper auth.
- **Don't reimplement checkout** — every custom checkout breaks Shop Pay, loses 20-40% conversion, and fails PCI compliance.
- **Variant IDs are GIDs** — `gid://shopify/ProductVariant/12345`. Pass them as-is; don't strip to numeric.
- **Prices are decimal strings** — `"19.99"`, not cents. Unlike Liquid.
- **Availability**: `product.availableForSale` is overall; `variant.availableForSale` is per-variant. Check the right one.

## Hydrogen vs. Next.js vs. other

| | Hydrogen | Next.js | SvelteKit + API |
|---|---|---|---|
| Official | Yes | No (community) | No |
| Hosting | Oxygen (free on Shopify) | Vercel/Netlify | Self |
| Caching primitives | Built-in | Custom | Custom |
| Best for | Pure commerce | Content + commerce hybrid | Small stores, lean |

If the store is commerce-first, use Hydrogen. If you need CMS-heavy content with commerce as a section, Next.js + Sanity/Contentful + Storefront API works well.
