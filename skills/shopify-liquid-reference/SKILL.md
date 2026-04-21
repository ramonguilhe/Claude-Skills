---
name: shopify-liquid-reference
description: Use this skill when writing, debugging, or reviewing Liquid code for Shopify themes, email templates, or checkout extensions. Covers objects, tags, filters, control flow, and Shopify-specific idioms. Triggers on ".liquid" files, "{% ... %}", "{{ ... }}" syntax, or questions about Liquid filters/tags/drops.
---

# Liquid Reference (Shopify Dialect)

Liquid is a template language created by Shopify (open source). Shopify extends it with store-specific objects, filters, and tags. This covers the Shopify dialect — Jekyll/GitHub Pages use a reduced subset.

## Syntax basics

- `{{ ... }}` — output (interpolate)
- `{% ... %}` — tag (logic, no output)
- `{{- ... -}}`, `{%- ... -%}` — trim whitespace

## Variables & assignment

```liquid
{% assign name = 'World' %}
{% assign total = cart.total_price | divided_by: 100.0 %}

{% capture greeting %}
  Hello, {{ name }}! Total: ${{ total }}
{% endcapture %}

{{ greeting }}
```

`capture` builds a string from nested Liquid. `assign` stores a single value.

## Control flow

```liquid
{% if product.available and product.price < 5000 %}
  Buy now
{% elsif product.available %}
  Premium item
{% else %}
  Sold out
{% endif %}

{% case variant.inventory_quantity %}
  {% when 0 %}Sold out
  {% when 1, 2, 3 %}Low stock
  {% else %}In stock
{% endcase %}

{% unless customer %}
  <a href="/account/login">Log in</a>
{% endunless %}
```

Operators: `==`, `!=`, `>`, `<`, `>=`, `<=`, `and`, `or`, `contains` (string or array membership).

## Iteration

```liquid
{% for item in cart.items %}
  {{ forloop.index }}. {{ item.product.title }} — {{ item.quantity }}
  {% if forloop.last %}(final item){% endif %}
{% else %}
  Cart is empty
{% endfor %}

{% for i in (1..5) %}{{ i }}{% endfor %}  {# 12345 #}
```

`forloop` helpers: `index` (1-based), `index0`, `first`, `last`, `length`, `rindex`.

Limit & offset:
```liquid
{% for product in collection.products limit: 4 offset: 8 %} ... {% endfor %}
```

Break & continue:
```liquid
{% for item in items %}
  {% if item.disabled %}{% continue %}{% endif %}
  {% if item.limit_reached %}{% break %}{% endif %}
{% endfor %}
```

## Filters (most useful)

### String
```liquid
{{ 'hello' | upcase }}                  {# HELLO #}
{{ 'Hello World' | downcase }}          {# hello world #}
{{ 'hello world' | capitalize }}        {# Hello world #}
{{ product.title | truncate: 20 }}
{{ product.description | strip_html | truncatewords: 30 }}
{{ 'a/b/c' | split: '/' }}              {# ['a','b','c'] #}
{{ ' foo ' | strip }}
{{ product.title | handleize }}         {# URL-safe slug #}
{{ 'text' | replace: 'text', 'new' }}
```

### Math
```liquid
{{ 10 | plus: 5 }} {{ 10 | minus: 3 }} {{ 10 | times: 2 }} {{ 10 | divided_by: 3 }}
{{ 10.5 | round: 0 }} {{ 10.5 | ceil }} {{ 10.5 | floor }}
{{ -5 | abs }} {{ 3 | at_least: 5 }} {{ 10 | at_most: 5 }}
```

### Money (Shopify-specific)
```liquid
{{ product.price | money }}                 {# $19.99 #}
{{ product.price | money_with_currency }}   {# $19.99 USD #}
{{ product.price | money_without_trailing_zeros }}  {# $20 #}
```

All Shopify prices are in **cents** (integer). Always filter through `money` for display.

### Array
```liquid
{{ collection.products | size }}
{{ array | first }} {{ array | last }}
{{ array | join: ', ' }}
{{ products | sort: 'price' | reverse }}
{{ products | where: 'available', true }}
{{ products | map: 'title' }}
{{ array | uniq }}
```

### Date
```liquid
{{ article.published_at | date: '%b %d, %Y' }}   {# Jan 15, 2025 #}
{{ 'now' | date: '%Y-%m-%d' }}
```

Format: strftime syntax. `%Y`=year, `%m`=month, `%d`=day, `%H:%M`=time.

### URL & image
```liquid
{{ product | within: collection }}            {# preserves collection in URL #}
{{ 'logo.png' | asset_url }}
{{ product.featured_image | image_url: width: 800, crop: 'center' }}
{{ product.featured_image | image_tag: loading: 'lazy', widths: '400,800' }}
{{ 'cart.checkout' | t }}                     {# translate locale key #}
```

### HTML
```liquid
{{ '<strong>safe</strong>' | escape }}        {# &lt;strong&gt;... #}
{{ product.description }}                     {# Liquid auto-escapes vars, but HTML fields render as-is #}
{{ block.settings.html | newline_to_br }}
```

## Tags reference

### Content
- `{% render 'snippet', arg: value %}` — render `/snippets/snippet.liquid` with isolated scope. **Use this, not `include`.**
- `{% section 'name' %}` — render a section from `/sections/`.
- `{% sections 'group-name' %}` — render a section group (OS 2.0).
- `{% content_for 'block' %}` — render a theme block.
- `{% liquid %}...{% endliquid %}` — multi-line block without `{%%}` wrappers per line.

### Forms (Shopify-specific)
```liquid
{% form 'product', product %}
  <input name="quantity" type="number" value="1">
  <button type="submit">Add to cart</button>
{% endform %}
```

Form types: `product` (add-to-cart), `contact`, `customer`, `customer_login`, `customer_register`, `create_customer`, `recover_customer_password`, `reset_customer_password`, `activate_customer_password`, `cart`, `new_comment`, `storefront_password`.

### Paginate
```liquid
{% paginate collection.products by 24 %}
  {% for product in collection.products %} ... {% endfor %}
  {{ paginate | default_pagination }}
{% endpaginate %}
```

Max `by` is 50. `paginate.pages` gives total page count.

### Assign & Increment
```liquid
{% assign counter = 0 %}
{% increment counter %}  {# prints 0, 1, 2, ... — note: ignores assign #}
{% decrement counter %}
```

`increment`/`decrement` maintain their own state per render and don't affect `assign`.

## Shopify object highlights

### `product`
- `id`, `handle`, `title`, `description`, `vendor`, `type`, `tags`
- `available`, `price`, `price_min`, `price_max`, `compare_at_price`
- `variants` (array), `first_available_variant`, `selected_or_first_available_variant`
- `featured_image`, `images`, `media` (videos + 3D models)
- `url`, `collections`, `metafields.namespace.key`

### `variant`
- `id`, `title`, `sku`, `barcode`, `price`, `compare_at_price`
- `available`, `inventory_quantity`, `inventory_management`, `inventory_policy`
- `featured_image`, `option1`, `option2`, `option3`

### `cart`
- `item_count`, `items` (line items), `total_price`, `original_total_price`
- `total_discount`, `discount_applications`, `currency`, `note`, `attributes`

### `customer`
- `id`, `first_name`, `last_name`, `email`, `orders_count`, `total_spent`
- `addresses`, `default_address`, `tags`

### `shop`
- `name`, `domain`, `email`, `currency`, `money_format`, `locale`

## Common idioms

**Default value fallback:**
```liquid
{{ product.title | default: 'Untitled product' }}
```

**Check metafield existence:**
```liquid
{% if product.metafields.custom.ingredients != blank %}
  <p>{{ product.metafields.custom.ingredients }}</p>
{% endif %}
```

**Debug:**
```liquid
<pre>{{ product | json }}</pre>
```

`json` filter serializes for inspection or for passing to JS.

**Selected variant from URL (?variant=12345):**
```liquid
{{ product.selected_or_first_available_variant.price | money }}
```

## Gotchas

- **`include` is deprecated** — use `render`. `render` is scoped; parent variables aren't visible unless passed as arguments.
- **`assign` inside `for` leaks** — variables persist after the loop ends.
- **Liquid renders on every request** — no persistent state. Use the Section Rendering API for JS-driven updates.
- **Money values are cents** — `product.price` is `1999` (meaning $19.99), never `19.99`.
- **Arrays are 0-indexed for `[n]` access, 1-indexed for `forloop.index`.**
- **No negative array indexing** — `array[-1]` doesn't work; use `array | last`.
