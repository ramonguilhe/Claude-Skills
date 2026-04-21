#!/usr/bin/env python3
"""Validate Claude skills: YAML frontmatter, uniqueness, description quality."""
import re
import sys
from pathlib import Path

SKILLS_DIR = Path(__file__).parent.parent / "skills"
FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)

errors: list[str] = []
warnings: list[str] = []
skills: list[dict] = []


def parse_frontmatter(text: str) -> dict:
    m = FRONTMATTER_RE.match(text)
    if not m:
        return {}
    fm = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip()
    return fm


def validate_skill(skill_dir: Path) -> None:
    skill_md = skill_dir / "SKILL.md"
    rel = skill_dir.name

    if not skill_md.exists():
        errors.append(f"[{rel}] missing SKILL.md")
        return

    text = skill_md.read_text()

    # 1. frontmatter present
    fm = parse_frontmatter(text)
    if not fm:
        errors.append(f"[{rel}] missing YAML frontmatter (--- ... ---)")
        return

    # 2. required fields
    if "name" not in fm:
        errors.append(f"[{rel}] frontmatter missing 'name'")
    if "description" not in fm:
        errors.append(f"[{rel}] frontmatter missing 'description'")

    # 3. name matches dir
    if fm.get("name") != rel:
        errors.append(
            f"[{rel}] name '{fm.get('name')}' doesn't match directory '{rel}'"
        )

    # 4. description quality
    desc = fm.get("description", "")
    if len(desc) < 80:
        warnings.append(f"[{rel}] description is short ({len(desc)} chars) — triggers may be weak")
    if len(desc) > 1024:
        errors.append(f"[{rel}] description > 1024 chars ({len(desc)}) — model instructions truncate")
    if "Use this skill" not in desc and "Use when" not in desc and "Triggers" not in desc:
        warnings.append(f"[{rel}] description lacks explicit trigger guidance")

    # 5. body has content
    body = FRONTMATTER_RE.sub("", text, count=1)
    if len(body.strip()) < 500:
        warnings.append(f"[{rel}] body is short ({len(body.strip())} chars)")

    # 6. H1 or similar heading present
    if not re.search(r"^#\s+\S+", body, re.MULTILINE):
        warnings.append(f"[{rel}] body missing top-level heading")

    skills.append({"name": fm.get("name"), "desc": desc, "body_len": len(body), "path": str(skill_md)})


def check_name_collisions() -> None:
    names = [s["name"] for s in skills]
    dupes = {n for n in names if names.count(n) > 1}
    for d in dupes:
        errors.append(f"duplicate skill name: '{d}'")


def check_description_overlap() -> None:
    """Descriptions should not collide — each should have distinct triggers."""
    for i, a in enumerate(skills):
        for b in skills[i + 1 :]:
            a_words = set(re.findall(r"\w{5,}", a["desc"].lower()))
            b_words = set(re.findall(r"\w{5,}", b["desc"].lower()))
            overlap = a_words & b_words
            # words common to all Shopify skills are expected
            expected_common = {"shopify", "skill", "store", "triggers"}
            unique_overlap = overlap - expected_common
            if len(unique_overlap) > 15:
                warnings.append(
                    f"high description overlap between '{a['name']}' and '{b['name']}' "
                    f"({len(unique_overlap)} shared keywords) — triggers may conflict"
                )


def main() -> int:
    if not SKILLS_DIR.exists():
        print(f"no skills dir at {SKILLS_DIR}")
        return 1

    skill_dirs = sorted(d for d in SKILLS_DIR.iterdir() if d.is_dir())
    if not skill_dirs:
        print("no skills found")
        return 1

    print(f"Found {len(skill_dirs)} skills in {SKILLS_DIR}\n")

    for d in skill_dirs:
        validate_skill(d)

    check_name_collisions()
    check_description_overlap()

    print(f"{'='*60}")
    print(f"Skills validated: {len(skills)}")
    print(f"Errors:   {len(errors)}")
    print(f"Warnings: {len(warnings)}")
    print(f"{'='*60}\n")

    if errors:
        print("ERRORS:")
        for e in errors:
            print(f"  ✗ {e}")
        print()

    if warnings:
        print("WARNINGS:")
        for w in warnings:
            print(f"  ⚠ {w}")
        print()

    print("SKILL SUMMARY:")
    for s in sorted(skills, key=lambda x: x["name"]):
        trig_preview = s["desc"][:80].replace("\n", " ")
        print(f"  ✓ {s['name']:32s}  body={s['body_len']:>5}  {trig_preview}...")

    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
