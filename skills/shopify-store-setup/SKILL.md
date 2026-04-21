---
name: shopify-store-setup
description: Use this skill when setting up, configuring, or launching a new Shopify store — choosing a plan, connecting domains, configuring payments/taxes/shipping, setting up email/DNS, installing essential apps, and preparing a store for first sale. Triggers on "set up my Shopify store", "launch a Shopify store", "Shopify configuration checklist", "essential Shopify settings", "connect domain to Shopify", "Shopify payments setup".
---

# Shopify Store Setup

End-to-end checklist for taking a store from zero to launch-ready. Order matters — doing steps out of order causes duplicated work (e.g., shipping zones before products = incorrect rates).

## Plan selection

| Plan | Price (USD/mo) | Transaction fee (non-SP) | Best for |
|---|---|---|---|
| Starter | $5 | 5% | Social commerce, no website |
| Basic | $39 | 2% | Solo operators, < $50K/mo |
| Shopify | $105 | 1% | $50K-$500K/mo, small teams |
| Advanced | $399 | 0.5% | $500K-$2M/mo, reports + shipping APIs |
| Plus | $2,300+ | 0.15% | $1M+/mo, enterprise (B2B, wholesale, multi-store) |

**Transaction fees apply only if you don't use Shopify Payments.** With Shopify Payments, fees are 0%. Shopify Payments is available in ~25 countries; if your country isn't supported, factor in the transaction fee when picking a plan.

Start on Basic unless you already have > $50K/mo revenue planned. Upgrade when you hit Shopify's automatic break-even recommendation (admin shows it).

## The launch checklist (ordered)

### 1. Store name + URL
- **Legal name**: for invoices, taxes, payment processing
- **Store name**: shown to customers
- **Store URL**: `yourstore.myshopify.com` — permanent, can't be changed. Use your brand.

### 2. General settings (Settings → General)
- Store contact email + sender email
- Store industry (affects tax + app recommendations)
- Primary currency (locks into Payments, can't be changed easily)
- Time zone
- Weight unit (kg for most of the world, lb for US)

### 3. Billing
- Pick plan
- Add payment method
- Confirm billing currency (some plans offer local currencies)

### 4. Shopify Payments setup
- Add business details: legal name, tax ID, address
- Connect bank account (2-3 day verification)
- Enable accelerated checkouts: **Shop Pay, Apple Pay, Google Pay, PayPal** (PayPal is a separate integration)
- Set payout schedule (daily for most countries)

**Shop Pay converts ~1.72x higher than guest checkout.** Enable it.

### 5. Tax settings (Settings → Taxes and duties)
- Register where required (Shopify calculates nexus automatically in the US)
- **US**: enable Shopify Tax, register in collection-required states
- **EU**: VAT ID required if selling in EU; use OSS scheme for cross-border
- **BR**: NFe configuration needs a certified app like Hublow or Bling
- **UK**: VAT required above £90K turnover
- Collect duties for international orders (Shopify Markets DDP)

Never "estimate" tax yourself in Liquid or apps — use Shopify Tax or a certified third-party (Avalara, TaxJar).

### 6. Shipping (Settings → Shipping and delivery)
**Order matters**:
1. Set up **shipping profiles** (one per product group if rates differ)
2. Define **zones** (countries/regions you ship to)
3. Create **rates** per zone: flat, calculated (carrier real-time), or free over $X
4. Create **packages** (box sizes + weights)
5. If fulfilling from multiple locations, set up **locations** first (Settings → Locations)

Free shipping over $75 (or your AOV × 1.3) lifts AOV by ~20% on average. Build it into your pricing.

### 7. Checkout (Settings → Checkout)
- **Customer accounts**: Optional (most dropshippers), Required (subscriptions), or Off (guests only — worse for LTV)
- **Abandoned cart emails**: turn on, edit to brand voice
- **Tipping**: off unless service business
- **Address collection**: first name + last name required; phone optional (mandatory in some countries)
- **Order processing**: "Automatically fulfill the order's line items" → off, so you control timing

### 8. Policies (Settings → Policies)
Required before selling: **Refund, Privacy, Terms of Service, Shipping**. Shopify auto-generates templates — edit the `[Business name]` placeholders, add specifics for your niche.

Extra for apparel/electronics: **Return policy window** (30 days minimum is standard).

### 9. Domain (Settings → Domains)
Two options:
- **Buy through Shopify**: auto-configured, costs $15-20/year, no DNS hassle
- **Connect existing**: Add 2 records to your DNS:
  - `A` record: `@` → `23.227.38.65`
  - `CNAME`: `www` → `shops.myshopify.com`

Make your chosen domain **primary**, enable "Redirect all traffic to this domain". SSL auto-provisions in 48h.

### 10. Email (Settings → Notifications)
- Customize order confirmation, shipping, cancellation emails with logo + brand colors
- Set up a **custom sender** (`orders@yourbrand.com`) — requires DNS: SPF, DKIM, DMARC records from Shopify, added to your domain
- Without SPF/DKIM, emails go to spam at ~30% rate

### 11. Products (add in this order)
1. **Collections first** (e.g., "New Arrivals", "Sale", "Men", "Women")
2. **Products**: use Shopify's bulk CSV import for > 20 products, or manual for hand-curated
3. **Per product**: title, description (short + long), price, compare-at price, weight, images (min 5, 2000x2000, on white), variants, SEO title & meta description, tags
4. **Collections: automated rules** (e.g., "All products with tag 'new'") save work at scale
5. **Navigation**: Settings → Navigation → add collections to Main Menu

### 12. Theme (Online Store → Themes)
- Start with **Dawn** (free, fast, OS 2.0, official). Avoid heavy premium themes for the first launch.
- Upload logo (SVG preferred, 300x90 fallback PNG)
- Set brand colors (Settings → Brand) — propagates to theme, checkout, emails
- Pages: About, Contact, Size Guide (if apparel), FAQ
- Blog: optional; only start if you'll write 2+ posts/month

### 13. Essential apps (install last)
Don't install apps until you have products. Recommendations:

| Category | Free option | Paid option |
|---|---|---|
| Reviews | Shopify Inbox + Judge.me (free tier) | Yotpo, Okendo |
| Email/SMS | Shopify Email (free 10K/mo) | Klaviyo, Omnisend |
| Upsell | ReConvert free tier | Zipify OCU |
| SEO | Google + YouTube channel (free) | Yoast SEO Shopify |
| Support | Shopify Inbox (free) | Gorgias |
| Analytics | Shopify analytics + GA4 | Triple Whale |

**Anti-pattern**: installing 20 apps pre-launch. Each app adds JS weight, slows the site, and eats margin. Start with ≤ 5.

### 14. Pixel + analytics
- **Google Analytics 4**: Customer events → GA4 → paste Measurement ID (G-XXXXX). Shopify auto-sends events.
- **Meta Pixel**: Settings → Customer events → Meta channel → connect (server-side preferred for iOS 14+)
- **TikTok Pixel**: TikTok channel app → auto-installs
- **Google Ads conversion**: Settings → Customer events → Google channel

Use **Shopify's customer events** (server-side) instead of pasting pixel script tags in theme code — faster, works with iOS tracking restrictions.

### 15. Test orders
Place 2-3 test orders with Shopify Bogus Gateway (Settings → Payments → dev mode) before enabling real payments:
- Confirmation email arrives
- Order appears in Admin
- Shipping label flow works
- Cancellation + refund work
- Pixels fire (check Meta Events Manager live view)

### 16. Go live
- Remove password protection (Online Store → Preferences → Uncheck "Enable password")
- Submit sitemap to Google Search Console: `https://yourstore.com/sitemap.xml`
- Share preview links to 3 friends; ask for the first 5 things they notice — fix them before paid ads

## Post-launch first week

Day 1-2: Traffic quality check — bounce rate < 70%, avg session > 30s, at least 1 add-to-cart per 100 sessions.

Day 3-4: First abandoned cart? Check flow triggers. First order? Unbox workflow works? Shipping label prints?

Day 5-7: Look at Shopify Analytics → Acquisition → top sources. Scale what works, cut what doesn't.

## Common mistakes

- **No shipping rates set** → checkout says "no rates available", you lose orders silently
- **Test Shopify Payments account not fully verified** → first payout fails
- **Forgot to remove password** → paid traffic lands on password gate, 100% bounce
- **Store currency changed after first order** → causes accounting drift forever
- **Collections without smart rules** → products drop out of sight when new ones are added
- **No policy pages** → Shopify Payments held; Meta/TikTok reject ads
- **Oversized images (> 500KB)** → kills LCP, ad accounts flag the landing page

## Verification commands

Once live, verify externally:

```bash
# SSL
curl -I https://yourstore.com | grep -i strict-transport

# SPF/DKIM/DMARC
dig TXT yourstore.com
dig TXT _dmarc.yourstore.com

# Sitemap
curl https://yourstore.com/sitemap.xml | head -20

# Robots
curl https://yourstore.com/robots.txt
```
