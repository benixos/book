#!/usr/bin/env python3
"""Build the static site from content/*.md into docs/.

Usage:  python3 -I tools/build.py          (needs the `markdown` and `PyYAML` packages)

The build fails if the output contains anything the public edition must not carry
(see FORBIDDEN) or a local link that does not resolve.
"""
import datetime
import html
import os
import pathlib
import re
import shutil
import sys

import markdown
import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
ASSETS = ROOT / "assets"
OUT = ROOT / "docs"
SITE = "The BenixOS Book"
DOMAIN = "book.benixos.com"
YEAR = os.environ.get("BUILD_YEAR") or str(datetime.date.today().year)
FOOTER = (f"© {YEAR} Lockamy Studios · Cary, NC · We use AI tools to help build and write this "
          "site; a person reviews what we publish.")

# Things that must never reach the public output.
FORBIDDEN = [
    (r"\[\[", "unresolved wikilink"),
    (r"\bDJ\b", "a person's initials"),
    (r"\bDouglas\b", "a person's name"),
    (r"softsurve", "internal hostname"),
    (r"\bwiki/", "internal vault path"),
    (r"\b(messaging-architect|security-engineer|identity-pm|gateway-pm|devicenix-pm|benixos-pm|thunderhead-pm|technical-writer|brand-architect)\b", "internal agent role"),
    (r"\b(LS|DEV|CLUS|SOF|QR|THUN|KAN)-\d+\b", "internal tracker key"),
    (r"\b(venus|jupiter|saturn|amalthea|Proxmox)\b", "internal machine name"),
    (r"\b[Vv]ault\b", "internal vault reference"),
]

GROUPS = {
    "01": "What it is", "02": "What it is",
    "03": "Foundations", "04": "Foundations",
    "05": "The system", "06": "The system", "07": "The system", "08": "The system",
    "09": "The system", "10": "The system",
    "11": "Underneath and on top", "12": "Underneath and on top",
    "13": "Practice", "14": "Practice", "15": "Practice", "16": "Practice",
    "90": "Reference",
}


def split_front(text):
    if text.startswith("---\n"):
        end = text.index("\n---\n", 4)
        return yaml.safe_load(text[4:end]) or {}, text[end + 5:]
    return {}, text


def load_pages():
    pages = []
    for p in sorted(CONTENT.glob("*.md")):
        fm, body = split_front(p.read_text())
        slug = p.stem
        m = re.search(r"^# (.+)$", body, re.M)
        title = fm.get("title") or (m.group(1) if m else slug)
        pages.append({"slug": slug, "title": str(title), "body": body, "num": slug[:2]})
    order = {"index": 0, "about": 999}
    pages.sort(key=lambda x: order.get(x["slug"], int(x["num"]) if x["num"].isdigit() else 500))
    return pages


def render_inline(text):
    return markdown.markdown(text, extensions=["tables", "fenced_code", "sane_lists"])


def callouts(body):
    """Turn Obsidian-style callouts into <div class="callout ...">. Skips fenced code."""
    out, lines, i, fence = [], body.split("\n"), 0, False
    while i < len(lines):
        ln = lines[i]
        if ln.startswith("```"):
            fence = not fence
        if not fence and ln.startswith(">"):
            j = i
            while j < len(lines) and lines[j].startswith(">"):
                j += 1
            block = [re.sub(r"^> ?", "", l) for l in lines[i:j]]
            m = re.match(r"\[!(\w+)\]\s*(.*)$", block[0])
            if m:
                kind, title = m.group(1).lower(), m.group(2).strip()
                inner = render_inline("\n".join(block[1:]))
                out.append(f'\n<div class="callout callout-{kind}">\n<p class="callout-title">{html.escape(title)}</p>\n{inner}\n</div>\n')
            else:
                out.extend(lines[i:j])
            i = j
            continue
        out.append(ln)
        i += 1
    return "\n".join(out)


def link_fixes(body, titles):
    def wl(m):
        slug, label = m.group(1), m.group(2)
        if slug not in titles:
            raise SystemExit(f"unresolved wikilink target: {slug}")
        return f"[{label or titles[slug]}]({slug}.html)"
    body = re.sub(r"\[\[benixos-book/([^\]|]+)(?:\|([^\]]+))?\]\]", wl, body)
    body = re.sub(r"!\[\[([^\]]+\.svg)\]\]", r"![System architecture diagram](assets/\1)", body)
    nums = {t[:2]: s for s, t in ((s, s) for s in titles)}

    def chap(m):
        n = m.group(2)
        slug = nums.get(n.zfill(2))
        return f"[{m.group(1)} {n}]({slug}.html)" if slug else m.group(0)
    parts, fence = [], False
    for ln in body.split("\n"):
        if ln.startswith("```"):
            fence = not fence
        parts.append(ln if fence else re.sub(r"(?<![\[\w])([Cc]hapter) (\d{1,2})\b(?!\])", chap, ln))
    return "\n".join(parts)


def nav_html(pages, cur):
    items, last = [], None
    for p in pages:
        if p["slug"] == "index":
            continue
        grp = GROUPS.get(p["num"]) if p["num"].isdigit() else None
        if p["slug"] == "about":
            grp = "Reference"
        if grp != last and grp:
            items.append(f'<li class="grp">{html.escape(grp)}</li>')
            last = grp
        cur_attr = ' aria-current="page"' if p["slug"] == cur else ""
        items.append(f'<li><a href="{p["slug"]}.html"{cur_attr}>{html.escape(p["title"])}</a></li>')
    home = ' aria-current="page"' if cur == "index" else ""
    return (f'<nav class="side" aria-label="Chapters"><a class="brand" href="index.html"{home}>{SITE}</a>'
            f'<details id="nav" open><summary>Chapters</summary><ul>{"".join(items)}</ul></details></nav>')


def page_html(pages, i, body_html, has_mermaid):
    p = pages[i]
    prev_p = pages[i - 1] if i > 0 and p["slug"] not in ("index", "404") else None
    next_p = pages[i + 1] if i + 1 < len(pages) and p["slug"] not in ("index", "404") else None
    if prev_p and prev_p["slug"] == "index":
        prev_p = None
    desc = re.sub(r"<[^>]+>", "", re.search(r"<p>(.*?)</p>", body_html, re.S).group(1)) if "<p>" in body_html else SITE
    desc = html.escape(re.sub(r"\s+", " ", desc).strip()[:200])
    pager = ""
    if prev_p or next_p:
        l = f'<a href="{prev_p["slug"]}.html" rel="prev">← {html.escape(prev_p["title"])}</a>' if prev_p else "<span></span>"
        r = f'<a href="{next_p["slug"]}.html" rel="next">{html.escape(next_p["title"])} →</a>' if next_p else "<span></span>"
        pager = f'<div class="pager">{l}{r}</div>'
    title = SITE if p["slug"] == "index" else f'{p["title"]} · {SITE}'
    mer = '<script src="assets/vendor/mermaid.min.js" defer></script>' if has_mermaid else ""
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{desc}">
<link rel="stylesheet" href="assets/site.css">
</head><body><div class="wrap">
{nav_html(pages, p["slug"])}
<main>
{body_html}
{pager}
<footer>{FOOTER}</footer>
</main></div>
{mer}<script src="assets/site.js" defer></script>
</body></html>
"""


def check(out_dir):
    problems = []
    names = {f.name for f in out_dir.glob("*.html")}
    for f in sorted((out_dir / "assets").glob("*.svg")):
        for pat, why in FORBIDDEN:
            for m in re.finditer(pat, f.read_text()):
                problems.append(f"assets/{f.name}: {why}")
    for f in sorted(out_dir.glob("*.html")):
        t = f.read_text()
        visible = re.sub(r"<(script|style)\b.*?</\1>", "", t, flags=re.S)
        for pat, why in FORBIDDEN:
            for m in re.finditer(pat, visible):
                problems.append(f"{f.name}: {why}: {visible[max(0, m.start() - 30):m.end() + 30]!r}")
        for href in re.findall(r'(?:href|src)="([^"#]+)', t):
            if re.match(r"(https?:|mailto:)", href):
                continue
            target = href.split("#")[0]
            if target in names or (out_dir / target).exists():
                continue
            problems.append(f"{f.name}: broken local link {href}")
    return problems


def main():
    pages = load_pages()
    titles = {p["slug"]: p["title"] for p in pages}
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    shutil.copytree(ASSETS, OUT / "assets")
    for i, p in enumerate(pages):
        body = link_fixes(p["body"], titles)
        body = callouts(body)
        body_html = markdown.markdown(body, extensions=["tables", "fenced_code", "sane_lists", "toc"])
        body_html = re.sub(r"(<table>.*?</table>)", r'<div class="tablewrap">\1</div>', body_html, flags=re.S)
        has_mermaid = "language-mermaid" in body_html
        (OUT / f"{p['slug']}.html").write_text(page_html(pages, i, body_html, has_mermaid))
    (OUT / "404.html").write_text(page_html(
        [{"slug": "404", "title": "Not found", "num": "00"}] + [p for p in pages if p["slug"] != "index"], 0,
        "<h1>Page not found</h1><p>Go to the <a href=\"index.html\">contents</a>.</p>", False))
    (OUT / "CNAME").write_text(DOMAIN + "\n")
    (OUT / ".nojekyll").write_text("")
    problems = check(OUT)
    if problems:
        print("BUILD FAILED:", *problems, sep="\n  ")
        sys.exit(1)
    print(f"built {len(pages)} pages into {OUT.relative_to(ROOT)}/")


if __name__ == "__main__":
    main()
