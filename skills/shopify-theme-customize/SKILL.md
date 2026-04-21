---
name: shopify-theme-customize
description: Use this skill when customizing, editing, or building a Shopify storefront theme — modifying theme.liquid, sections, section blocks, snippets, or theme settings schema. Triggers on "edit Shopify theme", "customize Dawn theme", "modify my theme", "add a section to my theme", "theme.liquid", "settings_schema.json", "section blocks in a theme", "shopify theme dev", "theme push/pull", or any work with Online Store 2.0 theme files.
---

# Shopify Theme Customization

Edit Online Store 2.0 themes: Dawn (reference), Sense, Craft, Origin, Spotlight, and third-party themes. OS 2.0 themes use JSON templates + section groups, enabling drag-and-drop customization in the theme editor.

## Theme directory structure

```
theme/
├── assets/          # CSS, JS, images, fonts (flat — no subfolders)
├── config/
│   ├── settings_schema.json   # Global theme settings UI
│   └── settings_data.json     # Saved setting values (generated)
├── layout/
│   ├── theme.liquid           # Master wrapper (html/head/body)
│   └── password.liquid        # Password page wrapper
├── locales/         # en.default.json, pt-BR.json, etc.
├── sections/        # Reusable modular components with schema
├── snippets/        # Liquid partials (no schema)
├── blocks/          # OS 2.0 theme blocks (new, 2024+)
└── templates/
    ├── index.json             # JSON = editable in theme editor
    ├── product.json
    └── customers/account.liquid   # .liquid = code-only
```

**Rule**: JSON templates are editable by merchants in the theme editor; Liquid templates are code-only. Prefer JSON for merchant-facing pages.

## Local dev with Shopify CLI

```bash
npm install -g @shopify/cli @shopify/theme
shopify theme dev --store=mystore.myshopify.com
# Serves theme at http://127.0.0.1:9292, hot reloads on save
# Preview URL syncs your local theme live without uploading
```

Useful commands:
- `shopify theme pull` — download current published theme
- `shopify theme push --unpublished` — upload as a new unpublished theme
- `shopify theme check` — lint Liquid + JSON (uses Theme Check)

## Section schema pattern

Every `sections/*.liquid` file ends with a `{% schema %}` JSON block:

```liquid
<section class="featured-product">
  <h2>{{ section.settings.heading }}</h2>
  {% for block in section.blocks %}
    {% case block.type %}
      {% when 'text' %}
        <p {{ block.shopify_attributes }}>{{ block.settings.body }}</p>
      {% when 'image' %}
        {{ block.settings.image | image_url: width: 800 | image_tag }}
    {% endcase %}
  {% endfor %}
</section>

{% schema %}
{
  "name": "Featured product",
  "tag": "section",
  "class": "section",
  "settings": [
    { "type": "text", "id": "heading", "label": "Heading", "default": "Featured" }
  ],
  "blocks": [
    { "type": "text", "name": "Text", "settings": [
      { "type": "richtext", "id": "body", "label": "Body" }
    ]},
    { "type": "image", "name": "Image", "settings": [
      { "type": "image_picker", "id": "image", "label": "Image" }
    ]}
  ],
  "presets": [{ "name": "Featured product" }]
}
{% endschema %}
```

**Critical**: `shopify_attributes` on block wrappers enables the editor click-to-select. Without it, blocks aren't interactive in the theme editor.

## Setting types cheat sheet

| Type | Use for |
|---|---|
| `text`, `textarea` | Short/long text |
| `richtext` | HTML with basic formatting |
| `image_picker` | Uploaded image (returns image object) |
| `url` | Link (page, collection, product, external) |
| `collection`, `product`, `blog`, `page`, `article` | Resource pickers |
| `color`, `color_scheme` | Colors (prefer `color_scheme` in OS 2.0) |
| `range` | Numeric slider (`min`, `max`, `step`, `unit`) |
| `select`, `radio`, `checkbox` | Discrete choices |
| `font_picker` | Font with `style` + `weight` access |
| `video`, `video_url` | Video resource or external URL |

## Asset URLs & performance

```liquid
{{ 'theme.css' | asset_url | stylesheet_tag }}
{{ 'theme.js' | asset_url | script_tag }}

{# Responsive image — use image_url with width, let browser pick #}
{{ product.featured_image | image_url: width: 1200 | image_tag:
   loading: 'lazy',
   widths: '300, 600, 900, 1200',
   sizes: '(min-width: 750px) 50vw, 100vw' }}
```

Never inline large images as base64; always use `image_url` filter with explicit widths.

## Accessing global objects

Shopify exposes these objects in any Liquid context:

- `shop` — name, currency, domain, email
- `cart` — line items, total
- `customer` — logged-in customer (nil if not logged in)
- `product`, `collection`, `article`, `blog`, `page` — contextual objects on their template
- `request` — path, design_mode, locale
- `settings` — values from `settings_schema.json`
- `routes` — URL paths (`routes.cart_url`, `routes.search_url`)
- `predictive_search` — for instant-search widgets

Check `request.design_mode` to show editor-only UI:
```liquid
{% if request.design_mode %}
  <p>Configure me in the editor →</p>
{% endif %}
```

## Section groups (OS 2.0 header/footer)

`sections/header-group.json` + `sections/footer-group.json` let merchants add/reorder sections in the header and footer via the editor. Reference them in `layout/theme.liquid`:

```liquid
{% sections 'header-group' %}
{{ content_for_layout }}
{% sections 'footer-group' %}
```

## Theme blocks (2024+)

New `/blocks` folder defines reusable blocks available across sections. Reference in a section's schema:

```json
"blocks": [{ "type": "@app" }, { "type": "@theme" }]
```

`@theme` accepts any block from `/blocks`; `@app` accepts blocks from installed apps.

## Common pitfalls

- **Liquid doesn't have async** — every request is sequential. For dynamic data, use Section Rendering API (`?sections=header` via JS fetch) or the Storefront API.
- **`{% javascript %}` / `{% stylesheet %}` inside sections** — code only loads when that section is on the page. Great for isolation, bad for shared logic.
- **`settings_data.json` is auto-generated** — do not hand-edit in production. Changes via the theme editor regenerate it.
- **Metafields**: expose them via `Settings → Custom data` first, then access as `product.metafields.namespace.key`.
- **Locales**: use `{{ 'key' | t }}` for all user-facing strings. Never hardcode English.

## Theme Check (lint)

`.theme-check.yml`:
```yaml
extends: :theme_app_extension
ignore:
  - "assets/vendor-*.js"
```

Run `shopify theme check` — catches undefined Liquid objects, unused snippets, oversized assets, missing alt text, etc.

## Performance targets

Shopify's theme store requires:
- Lighthouse Performance ≥ 60 (mobile)
- No render-blocking resources > 300ms
- Total JS bundle < 16KB (gzipped) on critical path

Use `{% render %}` (not `{% include %}` — deprecated) for snippets. `render` is cached and has isolated scope.
