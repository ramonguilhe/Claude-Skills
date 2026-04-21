---
name: shopify-product-research
description: Use this skill when researching, validating, or sourcing products for a Shopify store — finding winning dropshipping products, evaluating demand, analyzing competition, or comparing suppliers. Triggers on "find winning products", "product research for my store", "is this product a winner", "analyze this product", "AliExpress sourcing", "CJ dropshipping", "TikTok trending products".
---

# Shopify Product Research

Systematic approach to finding and validating products that will sell. Most dropshippers lose money by picking products based on gut feel. This skill gives a data-driven framework.

## The Winning Product Criteria (6 gates)

A product should pass all 6 before you commit:

1. **Demand**: > 5,000 monthly searches globally (Google Trends rising curve over 90 days)
2. **Margin**: Minimum 3x markup (sell at $29, cost $9, leaves room for ads + returns)
3. **Not saturated**: Fewer than 50 active Facebook ads on the exact product (Meta Ad Library)
4. **Wow factor**: Solves a problem visibly OR is visually unique enough for a 5-second video hook
5. **Lightweight + non-fragile**: Under 2 kg, not glass/ceramic (shipping + damage math kills margin)
6. **Not restricted**: Not in Meta's restricted categories (weapons, supplements, adult, medical claims, before/after)

If it fails any gate, skip it. There are millions of products — don't force one that doesn't fit.

## Research tools (free → paid)

### Free
- **Meta Ad Library** (https://www.facebook.com/ads/library) — search by keyword or page, see active ads, duration, creative. If an ad has been running > 30 days, it's working.
- **TikTok Creative Center** (https://ads.tiktok.com/business/creativecenter) — top ads, trending products, hashtag insights.
- **Google Trends** — 12-month + 5-year curves. Avoid products in clear decline.
- **Amazon Movers & Shakers / Best Sellers** — validated demand at scale. Filter by category.
- **AliExpress Dropshipping Center** — "Hot products" tab + order count filter.
- **Reddit** (r/BuyItForLife, r/Shutupandtakemymoney, niche subs) — organic demand signals.

### Paid (worth it if you're running ads)
- **Minea** ($49/mo) — scrapes Meta + TikTok ads, filters by performance signals.
- **PiPiAds** ($77/mo) — TikTok-specific ad spy tool.
- **Helium 10 / Jungle Scout** ($79-99/mo) — Amazon demand data (useful for Shopify too).
- **Dropship.io** ($49/mo) — tracks top Shopify stores' bestsellers.
- **Sell The Trend** ($40/mo) — aggregates AliExpress + Shopify + TikTok signals.

## The 5-minute validation flow

For any product candidate:

```
1. Meta Ad Library → search product name
   - Zero ads? Either untested or restricted. Skip unless you're the one testing.
   - 1-5 active ads > 14 days old? Green light for a test.
   - 50+ ads? Saturated. Only proceed with a differentiated angle.

2. Google Trends → past 12 months
   - Rising or stable = good
   - Seasonal spike coming = perfect (enter 30 days before peak)
   - Declining post-peak = avoid

3. AliExpress → sort by orders
   - > 1,000 orders = demand validated
   - Check review count + star rating (> 4.5, > 500 reviews)
   - Note shipping time (ePacket 10-15d, Choice 7-12d)

4. Amazon → same product search
   - BSR (Best Sellers Rank) < 10,000 in its category = strong
   - Read 1-3 star reviews for pain points → use them in your ad copy

5. Margin check
   - AliExpress cost + shipping → 3x minimum for selling price
   - If you can't hit 3x at a psychologically acceptable price, skip
```

## Supplier comparison

| Supplier | Shipping | MOQ | Quality | Best for |
|---|---|---|---|---|
| AliExpress | 10-25 days | 1 | Variable | Starting out, testing |
| CJ Dropshipping | 7-15 days (US warehouse) | 1 | Better QC | Scaling, custom branding |
| Zendrop | 5-12 days | 1 | US-filtered catalog | Beginners, speed |
| Spocket | 2-5 days (US/EU) | 1 | Vetted | Premium products |
| Printful / Printify | 3-7 days | 1 | Consistent | POD (apparel, mugs, posters) |
| Alibaba | 30-60 days | 100-500 | Varies | Bulk once validated |

Rule of thumb: test with AliExpress/Zendrop → once hitting $100/day, move to CJ for faster shipping → once at $1000/day, custom order from Alibaba + 3PL warehouse.

## Product types by difficulty

**Beginner-friendly**: gadgets, pet accessories, home organization, kitchen tools, fitness accessories, beauty tools. Cheap, easy to demo, broad audience.

**Intermediate**: fashion accessories, jewelry, home decor, hobby tools. Requires stronger branding + photography.

**Advanced**: apparel (sizing returns), electronics (warranty claims), supplements (regulations), anything fragile.

## Red flags to avoid

- Trademarked/branded items (Disney, sports teams, Pokemon) — account ban risk
- Medical claims ("cures", "heals", "FDA approved") — ad account ban
- Weapons, vapes, CBD, adult — Meta ban
- Unrealistic before/after photos — account ban
- Counterfeit designer goods — legal liability
- Products that look dangerous in videos (lasers, sharp blades) — ad rejection

## Using AI for research

Ask an LLM with web access:

```
Research trending products in the [NICHE] niche for Shopify dropshipping.
For each product, provide:
1. Name + 1-sentence description
2. Estimated AliExpress cost + shipping
3. Recommended retail price (3x markup minimum)
4. 3 recent Meta ads targeting this product (URLs if possible)
5. Google Trends direction (rising/stable/declining)
6. One risk or concern

Give me 10 candidates, ranked by potential.
```

Then run each through the 5-minute validation flow manually. Don't trust LLM output blind — LLMs hallucinate competitor ads and market data.

## Testing methodology

Once you pick a product:

1. **Budget**: $50-100/day for 3 days per product test = $150-300 min
2. **Creatives**: 3-5 video ads, 15-30 seconds, strong hook in first 2 seconds
3. **Landing page**: single product page (not collection), above-fold CTA, 5-star reviews
4. **KPIs at day 3**:
   - CTR > 1.5%
   - CPC < $1.50
   - Add-to-cart cost < $10
   - Break-even ROAS calculated: `Selling Price / (Selling Price - COGS - Shipping)` — need to hit that

If you can't hit break-even ROAS with tight ad optimization, kill the product. Don't nurse losers.
