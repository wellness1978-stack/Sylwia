#!/usr/bin/env python3
"""Pobiera posty z profilu LinkedIn przez aktora Apify i zapisuje je w ujednoliconym formacie.

Bez zewnętrznych zależności (tylko biblioteka standardowa).

Użycie:
  APIFY_TOKEN=... python3 fetch_posts.py https://www.linkedin.com/in/ktos/ --out data/ktos
  python3 fetch_posts.py --from-raw data/ktos/raw.json --out data/ktos      # tylko normalizacja
  python3 fetch_posts.py --from-text data/ktos/manual.txt --out data/ktos   # posty wklejone ręcznie, oddzielone linią ---

Wynik w katalogu --out:
  raw.json    surowa odpowiedź aktora
  posts.json  posty po normalizacji (tekst, data, url, zaangażowanie, media)
  posts.md    to samo w wersji do czytania
  images/     kilka grafik z postów o największym zaangażowaniu (do analizy designu)
"""
import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

DEFAULT_ACTOR = "harvestapi~linkedin-profile-posts"
API = "https://api.apify.com/v2/acts/{actor}/run-sync-get-dataset-items"


def get(d, *paths, default=None):
    """Zwraca pierwszą niepustą wartość spośród ścieżek typu 'a.b.c'."""
    for p in paths:
        cur = d
        ok = True
        for key in p.split("."):
            if isinstance(cur, dict) and key in cur:
                cur = cur[key]
            else:
                ok = False
                break
        if ok and cur not in (None, "", [], {}):
            return cur
    return default


def to_int(v):
    if isinstance(v, (int, float)):
        return int(v)
    if isinstance(v, str):
        digits = re.sub(r"[^\d]", "", v)
        return int(digits) if digits else None
    if isinstance(v, list):
        return len(v)
    return None


def collect_image_urls(item):
    urls = []
    for key in ("postImages", "images", "image", "imageUrls", "media"):
        val = item.get(key)
        if not val:
            continue
        vals = val if isinstance(val, list) else [val]
        for v in vals:
            if isinstance(v, str) and v.startswith("http"):
                urls.append(v)
            elif isinstance(v, dict):
                u = get(v, "url", "src", "imageUrl")
                if isinstance(u, str) and u.startswith("http"):
                    urls.append(u)
    return urls


def media_type(item, images):
    if get(item, "document", "documentUrl", "postDocument", "pdf"):
        return "document"  # karuzela PDF
    if get(item, "video", "postVideo", "videoUrl", "videos"):
        return "video"
    if get(item, "article", "articleUrl", "linkedArticle"):
        return "article"
    if images:
        return "images" if len(images) > 1 else "image"
    return "text"


def is_repost(item):
    t = str(item.get("type", "")).lower()
    return bool(
        t == "repost"
        or item.get("isRepost")
        or item.get("repostedBy")
        or item.get("resharedPost")
        or item.get("repost")
    )


def normalize(item):
    text = get(item, "content", "text", "postText", "commentary", "body", default="") or ""
    date = get(item, "postedAt.date", "postedAt.timestamp", "postedAtISO", "postedAt", "date", "publishedAt")
    if isinstance(date, dict):
        date = None
    images = collect_image_urls(item)
    return {
        "id": str(get(item, "id", "urn", "postId", "entityId", default="")),
        "url": get(item, "linkedinUrl", "url", "postUrl", "shareUrl"),
        "date": str(date) if date is not None else None,
        "text": text.strip(),
        "author": get(item, "author.name", "authorName", "author.fullName"),
        "repost": is_repost(item),
        "media": media_type(item, images),
        "images": images,
        "likes": to_int(get(item, "engagement.likes", "engagement.reactions", "numLikes",
                            "likes", "reactionsCount", "totalReactionCount")),
        "comments": to_int(get(item, "engagement.comments", "numComments", "comments", "commentsCount")),
        "shares": to_int(get(item, "engagement.shares", "numShares", "shares", "repostsCount")),
    }


def run_actor(profile_url, max_posts, actor, token, extra_input):
    body = {"targetUrls": [profile_url], "maxPosts": max_posts}
    body.update(extra_input)
    req = urllib.request.Request(
        API.format(actor=actor) + "?timeout=300",
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=330) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        msg = e.read().decode(errors="replace")[:800]
        sys.exit(f"Błąd Apify HTTP {e.code}: {msg}")
    except urllib.error.URLError as e:
        sys.exit(f"Brak połączenia z Apify: {e.reason}")


def parse_manual(path):
    chunks = re.split(r"^\s*-{3,}\s*$", Path(path).read_text(encoding="utf-8"), flags=re.M)
    return [{"id": f"manual-{i}", "content": c.strip()} for i, c in enumerate(chunks, 1) if c.strip()]


def engagement(p):
    return (p["likes"] or 0) + 3 * (p["comments"] or 0) + 2 * (p["shares"] or 0)


def download_images(posts, out, limit):
    if limit <= 0:
        return 0
    img_dir = out / "images"
    img_dir.mkdir(exist_ok=True)
    n = 0
    for p in sorted(posts, key=engagement, reverse=True):
        for i, url in enumerate(p["images"][:2]):
            if n >= limit:
                return n
            target = img_dir / f"{re.sub(r'[^A-Za-z0-9_-]', '_', p['id'])[:40]}_{i}.jpg"
            try:
                req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
                with urllib.request.urlopen(req, timeout=30) as r:
                    target.write_bytes(r.read())
                p.setdefault("image_files", []).append(str(target))
                n += 1
            except Exception as e:  # grafiki są opcjonalne
                print(f"  pominięto grafikę ({e})", file=sys.stderr)
    return n


def write_markdown(posts, path):
    lines = [f"# Posty ({len(posts)})\n"]
    for i, p in enumerate(posts, 1):
        meta = [p["date"] or "brak daty", f"media: {p['media']}",
                f"👍 {p['likes']}", f"💬 {p['comments']}", f"🔁 {p['shares']}"]
        lines.append(f"## Post {i} | id: {p['id']}\n")
        lines.append(" · ".join(str(m) for m in meta) + "\n")
        if p["url"]:
            lines.append(f"{p['url']}\n")
        lines.append("```text\n" + p["text"] + "\n```\n")
    path.write_text("\n".join(lines), encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("profile_url", nargs="?")
    ap.add_argument("--out", required=True)
    ap.add_argument("--max-posts", type=int, default=60)
    ap.add_argument("--actor", default=os.environ.get("APIFY_ACTOR", DEFAULT_ACTOR))
    ap.add_argument("--extra-input", default="{}", help="dodatkowe pola wejścia aktora jako JSON")
    ap.add_argument("--download-images", type=int, default=8)
    ap.add_argument("--from-raw", help="pomiń Apify, znormalizuj istniejący raw.json")
    ap.add_argument("--from-text", help="pomiń Apify, użyj postów wklejonych ręcznie")
    ap.add_argument("--keep-reposts", action="store_true")
    a = ap.parse_args()

    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)

    if a.from_text:
        raw = parse_manual(a.from_text)
    elif a.from_raw:
        raw = json.loads(Path(a.from_raw).read_text(encoding="utf-8"))
    else:
        if not a.profile_url:
            sys.exit("Podaj link do profilu LinkedIn.")
        token = os.environ.get("APIFY_TOKEN")
        if not token:
            sys.exit("Brak APIFY_TOKEN. Ustaw: export APIFY_TOKEN=twój_token (apify.com → Settings → API & Integrations).")
        print(f"Pobieram do {a.max_posts} postów z {a.profile_url} (aktor {a.actor})...", file=sys.stderr)
        raw = run_actor(a.profile_url, a.max_posts, a.actor, token, json.loads(a.extra_input))

    if isinstance(raw, dict):  # niektóre aktory zwracają {items: [...]}
        raw = raw.get("items") or raw.get("data") or [raw]
    (out / "raw.json").write_text(json.dumps(raw, ensure_ascii=False, indent=2), encoding="utf-8")

    posts = [normalize(x) for x in raw if isinstance(x, dict)]
    total = len(posts)
    if not a.keep_reposts:
        posts = [p for p in posts if not p["repost"]]
    posts = [p for p in posts if len(p["text"]) >= 40]
    if not posts:
        sys.exit(f"Brak postów z tekstem (surowych rekordów: {total}). Sprawdź raw.json: może aktor zmienił nazwy pól.")

    n_img = download_images(posts, out, a.download_images)
    (out / "posts.json").write_text(json.dumps(posts, ensure_ascii=False, indent=2), encoding="utf-8")
    write_markdown(posts, out / "posts.md")
    print(f"OK: {len(posts)} postów (z {total} rekordów), {n_img} grafik → {out}", file=sys.stderr)


if __name__ == "__main__":
    main()
