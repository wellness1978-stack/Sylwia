#!/usr/bin/env python3
"""Liczy twarde metryki stylu z posts.json, żeby analiza opierała się na liczbach, a nie na wrażeniach.

Użycie: python3 stats.py data/ktos/posts.json > data/ktos/stats.md
"""
import json
import re
import statistics as st
import sys
from collections import Counter
from datetime import datetime

EMOJI = re.compile(
    "[\U0001F300-\U0001FAFF\U00002600-\U000027BF\U0001F1E6-\U0001F1FF⭐⬆↔-⇿✅❌]"
)
UNICODE_BOLD = re.compile("[\U0001D400-\U0001D7FF]")
HASHTAG = re.compile(r"#[\wąćęłńóśźżĄĆĘŁŃÓŚŹŻ]+")
MENTION = re.compile(r"@[\wąćęłńóśźż]+")
LIST_MARK = re.compile(r"^\s*(?:[-•▪️▫️→➡️✅✔️❌👉🔹🔸◾]|\d+[.)/])\s*", re.M)
PL_WORDS = {"i", "w", "nie", "się", "jest", "to", "na", "że", "jak", "co", "ale", "z", "do", "czy", "mnie"}
EN_WORDS = {"the", "and", "is", "to", "of", "a", "in", "that", "it", "you", "i", "for", "this", "but", "my"}
AI_TELLS = ["—", "w dzisiejszym", "dynamicznym świecie", "let's dive", "game-changer", "game changer",
            "unlock", "delve", "kluczowe jest", "warto pamiętać", "in today's", "it's not just"]


def lang(text):
    t = text.lower()
    words = re.findall(r"[a-ząćęłńóśźż]+", t)
    pl = sum(w in PL_WORDS for w in words) + 3 * len(re.findall("[ąćęłńśźż]", t))
    en = sum(w in EN_WORDS for w in words)
    return "pl" if pl > en else "en"


def pct(n, d):
    return f"{(100 * n / d):.0f}%" if d else "-"


def q(vals):
    if not vals:
        return "-"
    vals = sorted(vals)
    p = lambda x: vals[min(len(vals) - 1, int(x * len(vals)))]
    return f"mediana {st.median(vals):.0f} (p25 {p(.25)}, p75 {p(.75)}, min {vals[0]}, max {vals[-1]})"


def sentences(text):
    return [s for s in re.split(r"(?<=[.!?…])\s+|\n+", text) if len(s.strip()) > 1]


def paragraphs(text):
    return [p for p in re.split(r"\n\s*\n", text) if p.strip()]


TEXT_EMOTICON = re.compile(r"(?<!\w)[:;]-?[)(DPp]|xD|XD")
CAPS_WORD = re.compile(r"\b[A-ZĄĆĘŁŃÓŚŹŻ]{4,}\b")
NOISE_PAR = re.compile(r"^\s*(?:(?:#\S+|https?://\S+|-{3,}|\W+)\s*)+$")


def content_paragraphs(text):
    """Akapity bez samych hashtagów, linków i separatorów (żeby wykryć prawdziwe zakończenie)."""
    return [p for p in paragraphs(text) if not NOISE_PAR.match(p.strip())]


def section(title, posts):
    n = len(posts)
    out = [f"\n## {title} (n={n})\n"]
    if not n:
        return out
    texts = [p["text"] for p in posts]
    first_lines = [t.split("\n", 1)[0].strip() for t in texts]
    last_par = [content_paragraphs(t)[-1] if content_paragraphs(t) else "" for t in texts]
    sent_len = [len(s.split()) for t in texts for s in sentences(t)]
    para_lines = [len(pg.split("\n")) for t in texts for pg in paragraphs(t)]
    emojis = Counter(e for t in texts for e in EMOJI.findall(t))
    tags = Counter(h.lower() for t in texts for h in HASHTAG.findall(t))

    lines_all = [l.strip() for t in texts for l in t.splitlines() if l.strip()]
    has_digit = sum(bool(re.search(r"\d", f)) for f in first_lines)
    starts_i = sum(bool(re.match(r"(ja|i|my|we)\b", f.lower())) for f in first_lines)
    hook_alone = sum(bool(re.match(r"[^\n]+\n\s*\n", t)) for t in texts)
    you = sum(bool(re.search(r"\b(ty|ci|cię|twój|twoje|wy|was|you|your)\b", t.lower())) for t in texts)
    emoji_line = sum(bool(EMOJI.match(l)) for l in lines_all)

    out += [
        "- Długość (znaki): " + q([len(t) for t in texts]),
        "- Długość (słowa): " + q([len(t.split()) for t in texts]),
        "- Akapity na post: " + q([len(paragraphs(t)) for t in texts]),
        "- Linie w akapicie: " + q(para_lines),
        "- Słowa w zdaniu: " + q(sent_len),
        "- Hook, czyli pierwsza linia (słowa): " + q([len(f.split()) for f in first_lines]),
        "- Hook kończy się '?': %s; zawiera liczbę: %s; zaczyna się od Ja/I/My/We: %s"
        % (pct(sum(f.endswith("?") for f in first_lines), n), pct(has_digit, n), pct(starts_i, n)),
        "- Hook jest osobnym akapitem (po nim pusta linia): " + pct(hook_alone, n),
        "- Ostatni akapit zawiera pytanie (CTA): " + pct(sum("?" in lp for lp in last_par), n),
        "- Posty z emoji: %s; emoji na post: %s"
        % (pct(sum(bool(EMOJI.search(t)) for t in texts), n), q([len(EMOJI.findall(t)) for t in texts])),
        "- Top emoji: " + (" ".join("%s×%d" % ec for ec in emojis.most_common(15)) or "brak"),
        "- Linie zaczynające się od emoji: %s linii" % pct(emoji_line, len(lines_all)),
        "- Posty z listą/punktorami: " + pct(sum(bool(LIST_MARK.search(t)) for t in texts), n),
        "- Posty z pogrubieniem unicode: " + pct(sum(bool(UNICODE_BOLD.search(t)) for t in texts), n),
        "- Posty z hashtagami: %s; hashtagi na post: %s"
        % (pct(sum(bool(HASHTAG.search(t)) for t in texts), n), q([len(HASHTAG.findall(t)) for t in texts])),
        "- Top hashtagi: " + (" ".join("%s×%d" % hc for hc in tags.most_common(12)) or "brak"),
        "- Posty ze wzmianką @: " + pct(sum(bool(MENTION.search(t)) for t in texts), n),
        "- Posty z linkiem: " + pct(sum("http" in t for t in texts), n),
        "- Zwracanie się do czytelnika (ty/you): " + pct(you, n),
        "- Myślnik pauza '—' w postach: " + pct(sum("—" in t for t in texts), n),
        "- Wykrzykniki na post: " + q([t.count("!") for t in texts]),
        "- Emotikony tekstowe :) ;-) :D: w %s postów; top: %s" % (
            pct(sum(bool(TEXT_EMOTICON.search(t)) for t in texts), n),
            " ".join("%s×%d" % ec for ec in Counter(e for t in texts for e in TEXT_EMOTICON.findall(t)).most_common(6)) or "brak"),
        "- Dywiz ze spacjami ' - ' jako myślnik: " + pct(sum(" - " in t for t in texts), n),
        "- Półpauza '–': " + pct(sum("–" in t for t in texts), n),
        "- Wtrącenia w nawiasach (...) na post: " + q([len(re.findall(r"\([^)]{3,}\)", t)) for t in texts]),
        "- Słowa WIELKIMI LITERAMI (akcent, 4+ litery): w %s postów; np. %s" % (
            pct(sum(bool(CAPS_WORD.search(t)) for t in texts), n),
            ", ".join(sorted({w for t in texts for w in CAPS_WORD.findall(t)})[:15]) or "brak"),
        "- Wielokropki na post: " + q([t.count("...") + t.count("…") for t in texts]),
        "- 'Link w (pierwszym) komentarzu': " + pct(sum(bool(re.search(r"(link|namiary).{0,45}komentarz|link in (the )?(first )?comment", t.lower())) for t in texts), n),
    ]
    tells = {k: sum(k in t.lower() for t in texts) for k in AI_TELLS}
    found = ", ".join("'%s'×%d" % kv for kv in tells.items() if kv[1])
    out.append("- Frazy typowe dla AI (ile postów): " + (found or "brak"))
    return out


def main():
    posts = json.load(open(sys.argv[1], encoding="utf-8"))
    for p in posts:
        p["lang"] = lang(p["text"])
    eng = lambda p: (p.get("likes") or 0) + 3 * (p.get("comments") or 0) + 2 * (p.get("shares") or 0)

    out = ["# Statystyki stylu\n", f"Postów: {len(posts)}"]
    langs = Counter(p["lang"] for p in posts)
    out.append("Języki: " + ", ".join(f"{k}: {v}" for k, v in langs.items()))
    out.append("Media: " + ", ".join(f"{k}: {v}" for k, v in Counter(p["media"] for p in posts).most_common()))

    dates = []
    for p in posts:
        try:
            dates.append(datetime.fromisoformat(str(p["date"]).replace("Z", "+00:00")))
        except (TypeError, ValueError):
            pass
    if len(dates) > 1:
        dates.sort()
        gaps = [(b - a).days for a, b in zip(dates, dates[1:])]
        days = Counter(d.strftime("%a") for d in dates)
        hours = Counter(d.hour for d in dates)
        out.append(f"Zakres: {dates[0].date()} → {dates[-1].date()}; odstęp między postami (dni): {q(gaps)}")
        out.append("Dni tygodnia: " + ", ".join(f"{k}:{v}" for k, v in days.most_common()))
        out.append("Godziny UTC: " + ", ".join(f"{k}:{v}" for k, v in hours.most_common(5)))

    out += section("Wszystkie posty", posts)
    for code in ("pl", "en"):
        if 0 < langs.get(code, 0) < len(posts):
            out += section(f"Tylko {code.upper()}", [p for p in posts if p["lang"] == code])

    if len(posts) >= 10 and any(eng(p) for p in posts):
        ranked = sorted(posts, key=eng, reverse=True)
        k = max(3, len(posts) // 5)
        out += section(f"Top {k} wg zaangażowania", ranked[:k])
        out += section(f"Najsłabsze {k}", ranked[-k:])
        out.append("\n## Ranking (id: zaangażowanie = likes + 3×komentarze + 2×udostępnienia)\n")
        for p in ranked:
            hook = p["text"].splitlines()[0][:80]
            out.append("- %s: %d · %s · %s · „%s”" % (p["id"], eng(p), p["media"], p["lang"], hook))

    print("\n".join(out))


if __name__ == "__main__":
    main()
