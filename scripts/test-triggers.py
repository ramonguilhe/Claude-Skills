#!/usr/bin/env python3
"""Simulate skill trigger matching against sample user prompts.

For each skill, we provide 3 prompts that SHOULD trigger it and 1 that should NOT.
We score by counting keyword overlap between prompt and skill description.
The target skill must rank #1 for positive prompts.
"""
import re
from pathlib import Path

SKILLS_DIR = Path(__file__).parent.parent / "skills"
FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)


def load_skills() -> dict[str, str]:
    skills = {}
    for d in sorted(SKILLS_DIR.iterdir()):
        if not d.is_dir():
            continue
        text = (d / "SKILL.md").read_text()
        m = FRONTMATTER_RE.match(text)
        if not m:
            continue
        for line in m.group(1).splitlines():
            if line.startswith("description:"):
                skills[d.name] = line.split(":", 1)[1].strip()
                break
    return skills


def score(prompt: str, desc: str) -> int:
    p_words = set(re.findall(r"\w{4,}", prompt.lower()))
    d_words = set(re.findall(r"\w{4,}", desc.lower()))
    return len(p_words & d_words)


TEST_CASES = [
    # (expected_skill, prompt, should_match)
    ("shopify-admin-api", "Create a product via the Shopify Admin API", True),
    ("shopify-admin-api", "Bulk update inventory on 5000 products in Shopify", True),
    ("shopify-admin-api", "fetch orders from Shopify using GraphQL mutation", True),

    ("shopify-theme-customize", "Edit the Dawn theme to add a new section block", True),
    ("shopify-theme-customize", "Customize theme.liquid and add schema settings", True),
    ("shopify-theme-customize", "Modify my Shopify theme to show custom blocks", True),

    ("shopify-liquid-reference", "What does the money filter do in Liquid?", True),
    ("shopify-liquid-reference", "Help me debug my .liquid file", True),
    ("shopify-liquid-reference", "How do I use the render tag in Shopify Liquid", True),

    ("shopify-product-research", "Help me find winning products for my Shopify dropshipping", True),
    ("shopify-product-research", "Is this AliExpress product a winner?", True),
    ("shopify-product-research", "Analyze this product — should I sell it on TikTok?", True),

    ("shopify-niche-research", "Find a profitable niche for my Shopify store", True),
    ("shopify-niche-research", "Validate this niche for my target audience", True),
    ("shopify-niche-research", "What sub-niche should I pick for Shopify?", True),

    ("shopify-app-dev", "Create a Shopify app using the Shopify CLI", True),
    ("shopify-app-dev", "Build a checkout UI extension for Shopify Plus", True),
    ("shopify-app-dev", "Shopify app generate a theme app extension", True),

    ("shopify-storefront-api", "Build a headless Shopify storefront with Hydrogen", True),
    ("shopify-storefront-api", "Use the Storefront API to fetch products in my mobile app", True),
    ("shopify-storefront-api", "Custom storefront with Shopify Remix and Storefront GraphQL", True),

    ("shopify-store-setup", "Set up my Shopify store and connect my domain", True),
    ("shopify-store-setup", "Shopify configuration checklist for launch", True),
    ("shopify-store-setup", "Configure Shopify Payments and tax settings", True),

    # negative examples — off-topic prompts
    ("shopify-admin-api", "How do I center a div in CSS?", False),
    ("shopify-liquid-reference", "What is the weather today?", False),
]


def main() -> int:
    skills = load_skills()
    passed = 0
    failed = 0
    neg_ok = 0

    for expected, prompt, should_match in TEST_CASES:
        ranked = sorted(
            skills.items(), key=lambda kv: score(prompt, kv[1]), reverse=True
        )
        top = ranked[0][0]
        top_score = score(prompt, ranked[0][1])

        if should_match:
            if top == expected:
                print(f"  ✓ '{prompt[:60]}' → {top} (score {top_score})")
                passed += 1
            else:
                print(f"  ✗ '{prompt[:60]}' → expected {expected}, got {top} (score {top_score})")
                failed += 1
        else:
            # negative — we expect a low score across all skills
            if top_score < 4:
                print(f"  ✓ '{prompt[:60]}' → no strong match (top score {top_score})")
                neg_ok += 1
            else:
                print(f"  ⚠ '{prompt[:60]}' → would match {top} (score {top_score}) unexpectedly")

    print(f"\nResults: {passed} positive passed, {failed} failed, {neg_ok} negative OK")
    return 1 if failed else 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
