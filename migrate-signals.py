#!/usr/bin/env python3
"""
Migrate signals to wh-signals/wh-signals/

Sources:
  1. wayward-house/src/content/signals/*.mdx  (Astro short-form, issues 011-012)
  2. waywardhouse-site/articles/system-signals-*.qmd  (old long-form, issues 001-004)

Output:
  wh-signals/wh-signals/issue-NNN.qmd  (vanilla Quarto front matter)
"""

import re
import shutil
from pathlib import Path

REPO_ROOT  = Path(__file__).parent.parent
MDX_SRC    = REPO_ROOT / "wayward-house/src/content/signals"
QMD_SRC    = REPO_ROOT / "waywardhouse-site/articles"
IMAGES_SRC = REPO_ROOT / "waywardhouse-site/assets/images"
OUT_DIR    = REPO_ROOT / "wh-signals/wh-signals"
IMAGES_OUT = OUT_DIR / "assets/images"

SIGNALS_IMAGE = "assets/images/signals.webp"


def parse_front_matter(text: str) -> tuple[dict, str]:
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text
    fm_raw = text[3:end].strip()
    body = text[end + 4:].lstrip("\n")

    lines = fm_raw.splitlines()
    result = {}
    current_key = None
    list_items = []
    in_inline_list = False

    for line in lines:
        # Inline list: bullets: ["item1", "item2", ...]
        m_inline = re.match(r'^(\S[^:]*?):\s*\[(.*)\]', line)
        if m_inline:
            key = m_inline.group(1).strip()
            items_raw = m_inline.group(2)
            items = [i.strip().strip('"').strip("'") for i in items_raw.split('",')]
            items = [re.sub(r'^"', '', i).strip().strip('"') for i in items]
            # re-split on ," to handle quoted items
            items = re.findall(r'"([^"]+)"', items_raw)
            if not items:
                items = [i.strip().strip('"') for i in items_raw.split(',') if i.strip()]
            result[key] = items
            current_key = None
            list_items = []
            continue

        if line.startswith("  - ") or (line.startswith("- ") and current_key):
            item = re.sub(r"^\s*-\s*", "", line).strip().strip('"').strip("'")
            list_items.append(item)
            continue

        m = re.match(r'^(\S[^:]*?):\s*(.*)', line)
        if m:
            if current_key and list_items:
                result[current_key] = list_items
                list_items = []
            current_key = m.group(1).strip()
            val = m.group(2).strip().strip('"').strip("'")
            if val in (">", "|", ">-", "|-"):
                val = ""
            if val:
                result[current_key] = val
        elif line.startswith("  ") and current_key and not list_items:
            existing = result.get(current_key, "")
            result[current_key] = (existing + " " + line.strip()).strip()

    if current_key and list_items:
        result[current_key] = list_items

    return result, body


def serialise_fm(d: dict) -> str:
    lines = ["---"]
    for k, v in d.items():
        if isinstance(v, list):
            lines.append(f"{k}:")
            for item in v:
                lines.append(f'  - "{item}"')
        elif isinstance(v, bool):
            lines.append(f"{k}: {str(v).lower()}")
        else:
            sv = str(v)
            if k in ("description", "subtitle") and len(sv) > 80:
                lines.append(f"{k}: >")
                words = sv.split()
                buf = "  "
                for w in words:
                    if len(buf) + len(w) + 1 > 74:
                        lines.append(buf.rstrip())
                        buf = "  " + w + " "
                    else:
                        buf += w + " "
                if buf.strip():
                    lines.append(buf.rstrip())
            elif any(c in sv for c in [':', '#', '[', ']', '{', '}']):
                lines.append(f'{k}: "{sv}"')
            else:
                lines.append(f"{k}: {sv}")
    lines.append("---")
    return "\n".join(lines)


def build_slug(issue_num: int) -> str:
    return f"issue-{issue_num:03d}"


def migrate_mdx(path: Path) -> tuple[str, str]:
    """Short-form MDX signal → .qmd with bullets/sources as body sections."""
    text = path.read_text(encoding="utf-8")
    fm, body = parse_front_matter(text)

    issue_num = int(fm.get("issue", 0))
    slug = build_slug(issue_num)

    out_fm = {}
    out_fm["title"] = fm.get("title", f"System Signals No. {issue_num}")
    out_fm["subtitle"] = fm.get("summary", fm.get("topic", ""))
    out_fm["date"] = fm.get("pubDate", fm.get("date", ""))
    out_fm["issue"] = issue_num
    topic = fm.get("topic", "")
    if topic:
        out_fm["categories"] = [topic]
    out_fm["image"] = SIGNALS_IMAGE
    out_fm["toc"] = True

    # Build body: existing body + key points + sources
    sections = [body.strip()] if body.strip() else []

    bullets = fm.get("bullets", [])
    if bullets:
        sections.append("## Key points\n")
        for b in bullets:
            sections.append(f"- {b}")

    sources = fm.get("sources", [])
    if sources:
        sections.append("\n## Sources\n")
        for s in sources:
            sections.append(f"- {s}")

    full_body = "\n\n".join(sections)
    return slug, serialise_fm(out_fm) + "\n\n" + full_body.strip() + "\n"


def migrate_qmd(path: Path) -> tuple[str, str]:
    """Long-form QMD signal → .qmd with cleaned front matter."""
    text = path.read_text(encoding="utf-8")
    fm, body = parse_front_matter(text)

    # Extract issue number from article-sequence or filename
    issue_num = int(fm.get("article-sequence", 0))
    if issue_num == 0:
        m = re.search(r'(\d+)', path.stem)
        if m:
            issue_num = int(m.group(1))
    slug = build_slug(issue_num)

    out_fm = {}
    out_fm["title"] = fm.get("title", f"System Signals No. {issue_num}")
    sub = fm.get("subtitle", "")
    if sub:
        out_fm["subtitle"] = sub
    out_fm["date"] = fm.get("date", fm.get("pubDate", ""))
    out_fm["issue"] = issue_num
    desc = fm.get("description", "")
    if desc:
        out_fm["description"] = desc
    raw_topics = fm.get("topics", [])
    if isinstance(raw_topics, str):
        raw_topics = re.findall(r'[\w\s\-]+', raw_topics)
    cats = [t.strip().strip('"').strip("'") for t in raw_topics if t.strip()]
    if cats:
        out_fm["categories"] = cats
    out_fm["image"] = SIGNALS_IMAGE
    out_fm["toc"] = True

    return slug, serialise_fm(out_fm) + "\n\n" + body.strip() + "\n"


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    IMAGES_OUT.mkdir(parents=True, exist_ok=True)

    # Copy shared signals image
    sig_img = IMAGES_SRC / "signals.webp"
    if sig_img.exists():
        shutil.copy2(sig_img, IMAGES_OUT / "signals.webp")
        print(f"  [img] copied signals.webp")
    else:
        print(f"  [img] WARNING: signals.webp not found in source")

    written = []

    # ── Canonical source: old site QMD signals only ───────────────────────────
    # Astro hub MDX signals (issue-011, issue-012) are filler — do NOT use them.
    print("=== Migrating QMD signals from waywardhouse-site ===")
    for qmd in sorted(QMD_SRC.glob("system-signals-*.qmd")):
        slug, content = migrate_qmd(qmd)
        out_path = OUT_DIR / f"{slug}.qmd"
        out_path.write_text(content, encoding="utf-8")
        print(f"  {slug}.qmd  ← {qmd.name}")
        written.append(slug)

    print(f"\n✓ Done. {len(written)} issues written to {OUT_DIR}")
    for s in sorted(written):
        print(f"  {s}")


if __name__ == "__main__":
    main()
