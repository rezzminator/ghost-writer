#!/usr/bin/env python3
"""
index_corpus.py — compute a writer's statistical fingerprint from a corpus.

The point of this script is to make extraction DETERMINISTIC. Instead of
eyeballing a corpus and estimating "the writer uses 'use' a lot", you run this
once and get exact counts: every word indexed, top-200 content words, function-
word frequencies, synonym-binary tallies, punctuation rates, sentence
burstiness, and more. The skill (Mode A) reads the output and transcribes the
numbers into the profile rather than guessing.

Dependency-free (Python 3 stdlib only) so it runs in any sandbox.

Usage:
    python3 index_corpus.py <path>            # dir (recursive), file, or glob
    python3 index_corpus.py <path> --top 200  # how many content words to list
    python3 index_corpus.py <path> --json out.json   # also write JSON

Outputs a human-readable markdown report to stdout. With --json, also writes
the full machine-readable stats. Reads .txt, .md (markdown stripped), and
.html (tags stripped).
"""

import argparse
import glob
import html
import json
import math
import os
import re
import sys
from collections import Counter

# ---------------------------------------------------------------------------
# Word lists
# ---------------------------------------------------------------------------

# Function words / stopwords — the stylometric layer. These are SEPARATED from
# content words in the report, because their relative frequencies are one of the
# strongest authorship signals (the Federalist Papers method).
FUNCTION_WORDS = set("""
a an the this that these those
i me my mine myself we us our ours ourselves you your yours yourself yourselves
he him his himself she her hers herself it its itself they them their theirs themselves
who whom whose which what
and or but nor so yet for because as if then than though although while whereas unless until
of in on at by to from with without within into onto upon over under above below between among through
about against during before after around near off out up down
is am are was were be been being do does did doing have has had having
will would shall should can could may might must ought
not no nor none never
very too so just only also even still much many more most less least
here there where when why how
all any both each few other some such own same one ones another
i'm you're he's she's it's we're they're i've you've we've they've i'd you'd
i'll you'll he'll she'll we'll they'll don't doesn't didn't won't wouldn't can't couldn't
isn't aren't wasn't weren't hasn't haven't hadn't shouldn't mustn't that's there's what's let's
""".split())

# Hedges — count specific ones, not just "hedges a lot".
HEDGES = ["probably", "maybe", "perhaps", "possibly", "likely", "i think",
          "i guess", "i'd say", "sort of", "kind of", "kinda", "sorta",
          "honestly", "to be fair", "it seems", "seems to", "might be",
          "could be", "i suppose", "presumably", "arguably", "potentially"]

# Intensifiers — same logic.
INTENSIFIERS = ["really", "very", "super", "extremely", "totally", "absolutely",
                "completely", "quite", "fairly", "pretty", "rather", "somewhat",
                "too", "so", "much", "almost", "especially", "incredibly",
                "remarkably", "considerably", "exceedingly"]

# Synonym binaries — the diagnostic table. Each entry is a label plus the word
# families on each side. We count every inflected form. The plain side is
# listed first by convention.
SYNONYM_BINARIES = [
    ("use / utilize", ["use", "uses", "used", "using"],
                      ["utilize", "utilizes", "utilized", "utilizing", "utilise", "utilises", "utilised", "utilising"]),
    ("help / assist", ["help", "helps", "helped", "helping"],
                      ["assist", "assists", "assisted", "assisting"]),
    ("but / however", ["but"], ["however"]),
    ("also / additionally / furthermore / moreover", ["also"],
                      ["additionally", "furthermore", "moreover"]),
    ("make / create / produce / craft", ["make", "makes", "made", "making"],
                      ["create", "creates", "created", "creating",
                       "produce", "produces", "produced", "producing",
                       "craft", "crafts", "crafted", "crafting"]),
    ("show / demonstrate", ["show", "shows", "showed", "shown", "showing"],
                      ["demonstrate", "demonstrates", "demonstrated", "demonstrating"]),
    ("find / discover", ["find", "finds", "found", "finding"],
                      ["discover", "discovers", "discovered", "discovering"]),
    ("big / large", ["big", "bigger", "biggest"], ["large", "larger", "largest"]),
    ("probably / perhaps", ["probably"], ["perhaps"]),
    ("very / quite", ["very"], ["quite"]),
    ("strange / weird", ["strange"], ["weird"]),
    ("get / obtain", ["get", "gets", "got", "getting", "gotten"],
                     ["obtain", "obtains", "obtained", "obtaining"]),
    ("about / regarding / concerning", ["about"], ["regarding", "concerning"]),
    ("because / due to", ["because"], ["due to"]),
    ("start / commence", ["start", "starts", "started", "starting"],
                         ["commence", "commences", "commenced", "commencing"]),
    ("buy / purchase", ["buy", "buys", "bought", "buying"],
                       ["purchase", "purchases", "purchased", "purchasing"]),
]

# Spelling / dialect / archaism variants — highly diagnostic of an individual
# (till vs until, toward vs towards, -ize vs -ise, -or vs -our). Each pair is
# (label, [variant-A forms], [variant-B forms]); we report which side the writer
# uses and by how much.
SPELLING_VARIANTS = [
    ("till / until", ["till"], ["until"]),
    ("toward / towards", ["toward"], ["towards"]),
    ("among / amongst", ["among"], ["amongst"]),
    ("while / whilst", ["while"], ["whilst"]),
    ("gray / grey", ["gray"], ["grey"]),
    ("learned / learnt", ["learned"], ["learnt"]),
    ("-ize / -ise", ["realize", "realizes", "realized", "organize", "organized",
                     "recognize", "recognized", "analyze", "analyzed", "emphasize"],
                    ["realise", "realises", "realised", "organise", "organised",
                     "recognise", "recognised", "analyse", "analysed", "emphasise"]),
    ("-or / -our", ["color", "colors", "behavior", "favor", "favorite", "honor",
                    "labor", "neighbor", "flavor"],
                   ["colour", "colours", "behaviour", "favour", "favourite",
                    "honour", "labour", "neighbour", "flavour"]),
    ("ok / okay", ["ok"], ["okay"]),
    ("anyway / anyways", ["anyway"], ["anyways"]),
]

# Common verb families to surface a plain-vs-elevated picture (best-effort, no
# POS tagger). These are counted as families and reported under "verb signal".
PLAIN_VERBS = ["use", "make", "do", "get", "have", "go", "take", "give", "show",
               "find", "say", "think", "know", "want", "need", "try", "ask",
               "tell", "see", "look", "help", "work", "put", "keep", "let"]

CONTRACTION_RE = re.compile(r"\b\w+'(?:t|s|re|ve|ll|d|m)\b", re.IGNORECASE)

# Web/source boilerplate to exclude from the content lexicon and keyness — these
# leak from URL headers, footers, and markup in source files and are never voice.
BOILERPLATE = set("""
http https www com html htm org net php url href mailto co uk
""".split())

# Baseline general-English frequencies (approx. occurrences per million words),
# for KEYNESS: how much MORE the writer uses a word than normal English. Raw
# frequency surfaces generic words ("one", "good", "people") that every writer
# uses; keyness surfaces the words that are distinctive to THIS writer. Values
# are approximate (COCA/SUBTLEX-ish) — keyness ranking is robust to rough
# baselines. Words not listed are assumed rare in English (DEFAULT_BASELINE_PM),
# so a word common in the corpus but absent here scores as distinctive.
DEFAULT_BASELINE_PM = 15.0
BASELINE_FREQ_PM = {
    # generic high-frequency content words (these SHOULD score low keyness)
    "people": 1900, "time": 1500, "like": 1500, "good": 1200, "work": 800,
    "year": 1000, "way": 900, "day": 900, "man": 700, "thing": 800, "things": 600,
    "woman": 400, "life": 600, "child": 500, "world": 600, "school": 450,
    "state": 500, "family": 400, "student": 350, "group": 350, "country": 400,
    "problem": 350, "hand": 500, "part": 450, "place": 450, "case": 400,
    "week": 350, "company": 350, "system": 350, "program": 250, "question": 300,
    "government": 350, "number": 300, "night": 350, "point": 350, "home": 400,
    "water": 300, "room": 350, "mother": 300, "area": 250, "money": 350,
    "story": 300, "fact": 350, "month": 250, "lot": 400, "right": 600,
    "study": 250, "book": 300, "eye": 400, "job": 300, "word": 300,
    "business": 300, "issue": 250, "side": 300, "kind": 350, "head": 400,
    "house": 350, "service": 250, "friend": 300, "father": 250, "power": 300,
    "hour": 250, "game": 300, "line": 300, "end": 400, "member": 250,
    "law": 250, "car": 300, "city": 300, "community": 200, "name": 350,
    "team": 250, "minute": 250, "idea": 250, "ideas": 150, "body": 300,
    "information": 250, "parent": 200, "face": 350, "level": 250, "office": 250,
    "door": 300, "health": 200, "person": 300, "art": 200, "war": 250,
    "history": 200, "party": 250, "result": 200, "change": 300, "morning": 250,
    "reason": 300, "research": 200, "girl": 350, "guy": 300, "moment": 250,
    "air": 250, "teacher": 200, "force": 200, "education": 200, "sense": 250,
    "market": 200, "plan": 200, "college": 150, "interest": 200, "course": 350,
    "someone": 350, "something": 600, "anything": 300, "everything": 300,
    "nothing": 350, "everyone": 250, "bit": 200, "sort": 250, "stuff": 250,
    # generic adjectives
    "new": 900, "first": 800, "last": 600, "long": 500, "great": 700,
    "little": 600, "own": 500, "old": 500, "big": 500, "high": 500,
    "different": 400, "small": 400, "large": 350, "next": 350, "early": 300,
    "young": 350, "important": 350, "public": 300, "bad": 350, "same": 500,
    "able": 300, "best": 400, "better": 500, "true": 300, "whole": 350,
    "sure": 400, "hard": 350, "real": 400, "full": 300, "simple": 250,
    "clear": 250, "easy": 300, "free": 300, "wrong": 300, "common": 250,
    # generic verbs
    "get": 1100, "make": 800, "go": 1300, "know": 1100, "take": 700,
    "see": 900, "come": 700, "think": 900, "look": 700, "want": 600,
    "give": 500, "use": 500, "used": 300, "find": 500, "tell": 400, "ask": 400,
    "seem": 350, "seems": 250, "feel": 400, "try": 400, "leave": 350,
    "call": 450, "called": 250, "need": 500, "become": 350, "mean": 400,
    "means": 200, "keep": 350, "start": 400, "started": 250, "show": 400,
    "hear": 300, "play": 350, "run": 350, "move": 300, "live": 350,
    "believe": 300, "bring": 300, "happen": 350, "write": 350, "writing": 200,
    "sit": 300, "stand": 250, "lose": 250, "pay": 300, "meet": 300,
    "include": 250, "continue": 200, "set": 350, "learn": 250, "lead": 250,
    "understand": 300, "watch": 300, "follow": 250, "stop": 300, "create": 250,
    "speak": 250, "read": 300, "spend": 250, "grow": 200, "open": 350,
    "walk": 300, "win": 250, "talk": 350, "turn": 400, "put": 600,
    "going": 500, "make": 800, "made": 400, "makes": 200, "making": 250,
    "getting": 200, "got": 400, "thought": 350, "saying": 150, "said": 700,
    # generic adverbs / hedges (handled elsewhere but keep baseline)
    "really": 600, "very": 700, "too": 500, "also": 500, "well": 600,
    "even": 700, "back": 700, "now": 900, "then": 800, "here": 500,
    "there": 1000, "only": 600, "more": 1200, "most": 500, "much": 600,
    "still": 500, "never": 400, "always": 350, "often": 250, "again": 400,
    "ever": 300, "far": 250, "away": 350, "almost": 250, "enough": 300,
    "probably": 200, "actually": 300, "perhaps": 150, "instead": 200,
    "rather": 200, "quite": 200, "especially": 150, "usually": 200,
}


def keyness(corpus_freq, total_words, min_count=20, top=120):
    """Rank content words by over-representation vs baseline English.
    Returns [(word, corpus_count, per_million, keyness_ratio), ...]."""
    out = []
    for w, c in corpus_freq.items():
        if c < min_count:
            continue
        pm = c / total_words * 1_000_000
        base = BASELINE_FREQ_PM.get(w, DEFAULT_BASELINE_PM)
        ratio = pm / base
        out.append((w, c, round(pm, 1), round(ratio, 1)))
    out.sort(key=lambda x: -x[3])
    return out[:top]

# ---------------------------------------------------------------------------
# Text loading
# ---------------------------------------------------------------------------

def strip_html(text):
    text = re.sub(r"(?is)<(script|style).*?>.*?</\1>", " ", text)
    text = re.sub(r"(?s)<[^>]+>", " ", text)
    return html.unescape(text)

def strip_markdown(text):
    text = re.sub(r"```.*?```", " ", text, flags=re.S)   # code fences
    text = re.sub(r"`[^`]*`", " ", text)                  # inline code
    text = re.sub(r"^#{1,6}\s*", "", text, flags=re.M)    # headers
    text = re.sub(r"[*_>#]", "", text)                    # emphasis/quote marks
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)  # links -> text
    return text

# Per-record metadata that scraped/exported corpora carry (HN comment headers,
# forum post chrome, etc.). Left in, it pollutes the index: "Source: https://
# news.ycombinator.com/item?id=…" injects source/news/ycombinator/id/item, and
# ISO timestamps inject a stray "t" (from the "T" in 2021-05-20T12:00). Strip
# whole metadata lines and inline timestamps/URLs before tokenizing so the
# indexer is reproducible without manual cleaning.
META_LINE_RE = re.compile(
    r"^\s*(?:source|url|permalink|link|posted|date|time|author|by|via|score|"
    r"points?|comments?|reply|parent|context|id|item|user|submitted)\s*[:=]",
    re.IGNORECASE)
URL_LINE_RE = re.compile(r"^\s*<?https?://\S+>?\s*$", re.IGNORECASE)
ISO_TS_RE = re.compile(
    r"\b\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}(?::\d{2})?(?:\.\d+)?(?:Z|[+\-]\d{2}:?\d{2})?\b")
# Social-export attribution bylines, e.g. "— Paul Graham (@paulg) January 24, 2022".
# A dash-led line carrying an @handle is chrome, not the writer's prose — and its
# em-dash would otherwise inflate the em-dash rate (the exact tell we care about most).
ATTRIB_LINE_RE = re.compile(r"^\s*[—–\-]\s.*@\w")

def strip_metadata(text):
    text = ISO_TS_RE.sub(" ", text)                 # kill inline timestamps (the stray "t")
    text = re.sub(r"https?://\S+", " ", text)        # kill inline URLs
    kept = [ln for ln in text.splitlines()
            if not META_LINE_RE.match(ln)
            and not URL_LINE_RE.match(ln)
            and not ATTRIB_LINE_RE.match(ln)]
    return "\n".join(kept)

def collect_files(path):
    if os.path.isdir(path):
        files = []
        for root, _, names in os.walk(path):
            for n in names:
                if n.lower().endswith((".txt", ".md", ".html", ".htm")):
                    files.append(os.path.join(root, n))
        return sorted(files)
    if any(c in path for c in "*?["):
        return sorted(glob.glob(path, recursive=True))
    return [path]

def load_text(path):
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        raw = f.read()
    low = path.lower()
    if low.endswith((".html", ".htm")):
        text = strip_html(raw)
    elif low.endswith(".md"):
        text = strip_markdown(raw)
    else:
        text = raw
    return strip_metadata(text)

# ---------------------------------------------------------------------------
# Analysis
# ---------------------------------------------------------------------------

WORD_RE = re.compile(r"[A-Za-z]+(?:'[A-Za-z]+)?")
SENT_SPLIT_RE = re.compile(r"[.!?]+(?:\s+|$)")

def tokenize(text):
    return [w.lower() for w in WORD_RE.findall(text)]

def analyze(texts, top_n):
    full = "\n\n".join(texts)
    tokens = tokenize(full)
    total = len(tokens)
    if total == 0:
        raise SystemExit("No words found in corpus.")

    per1000 = lambda n: round(n / total * 1000, 2)

    # Word frequencies
    freq = Counter(tokens)
    content = Counter({w: c for w, c in freq.items()
                       if w not in FUNCTION_WORDS and w not in BOILERPLATE and len(w) > 1})
    func = Counter({w: c for w, c in freq.items() if w in FUNCTION_WORDS})

    # n-grams (candidate pet phrases / multi-word units)
    bigrams = Counter(zip(tokens, tokens[1:]))
    trigrams = Counter(zip(tokens, tokens[1:], tokens[2:]))

    # Sentences + burstiness
    sentences = [s for s in SENT_SPLIT_RE.split(full) if s.strip()]
    sent_lengths = [len(tokenize(s)) for s in sentences]
    sent_lengths = [n for n in sent_lengths if n > 0]
    mean_len = round(sum(sent_lengths) / len(sent_lengths), 2) if sent_lengths else 0
    stdev = round(statistics_pstdev(sent_lengths), 2) if len(sent_lengths) > 1 else 0
    # Median is robust to pasted-list / no-punctuation outliers that inflate σ.
    median_len = (sorted(sent_lengths)[len(sent_lengths) // 2] if sent_lengths else 0)

    # Paragraphs (per-document, split on blank lines)
    para_lengths = []
    for t in texts:
        for para in re.split(r"\n\s*\n", t):
            n_sent = len([s for s in SENT_SPLIT_RE.split(para) if s.strip()])
            if n_sent:
                para_lengths.append(n_sent)
    mean_para = round(sum(para_lengths) / len(para_lengths), 2) if para_lengths else 0

    # Punctuation (counted on the raw full text, not tokens)
    punct = {
        "em_dash_char (—)": full.count("—"),
        "double_hyphen (--)": full.count("--"),
        "semicolon (;)": full.count(";"),
        "colon (:)": full.count(":"),
        "ellipsis (… or ...)": full.count("…") + len(re.findall(r"\.\.\.", full)),
        "exclamation (!)": full.count("!"),
        "question (?)": full.count("?"),
    }
    punct_per_1000 = {k: per1000(v) for k, v in punct.items()}

    # Contractions
    contractions = len(CONTRACTION_RE.findall(full))
    nt = len(re.findall(r"\bn't\b|\w+n't\b", full.lower()))
    not_count = freq.get("not", 0)
    contraction_nt_rate = (round(nt / (nt + not_count) * 100, 1)
                           if (nt + not_count) else 0.0)

    # Hedges / intensifiers (phrase-aware)
    low_full = " " + full.lower() + " "
    hedge_counts = {h: low_full.count(" " + h + " ") for h in HEDGES}
    hedge_counts = {k: v for k, v in sorted(hedge_counts.items(), key=lambda x: -x[1]) if v}
    intens_counts = {i: freq.get(i, 0) for i in INTENSIFIERS}
    intens_counts = {k: v for k, v in sorted(intens_counts.items(), key=lambda x: -x[1]) if v}

    # Sentence-initial connectors
    sent_initial = Counter()
    for s in sentences:
        toks = tokenize(s)
        if toks:
            sent_initial[toks[0]] += 1

    # Synonym binaries
    binaries = []
    for label, plain_forms, elev_forms in SYNONYM_BINARIES:
        p = sum(freq.get(w, 0) for w in plain_forms)
        e = sum(freq.get(w, 0) for w in elev_forms)
        if p or e:
            pick = "plain" if p >= e else "ELEVATED"
            binaries.append({"binary": label, "plain": p, "elevated": e, "writer_picks": pick})

    # Spelling / dialect / archaism variants
    variants = []
    for label, a_forms, b_forms in SPELLING_VARIANTS:
        a = sum(freq.get(w, 0) for w in a_forms)
        b = sum(freq.get(w, 0) for w in b_forms)
        if a or b:
            variants.append({"variant": label, "a": a, "b": b,
                             "picks": label.split("/")[0].strip() if a >= b
                                      else label.split("/")[-1].strip()})

    # Plain verb signal
    verb_signal = {v: freq.get(v, 0) for v in PLAIN_VERBS}
    verb_signal = {k: v for k, v in sorted(verb_signal.items(), key=lambda x: -x[1]) if v}

    # Type-token ratio
    first500 = tokens[:500]
    ttr_500 = round(len(set(first500)) / len(first500), 3) if first500 else 0
    ttr_all = round(len(set(tokens)) / total, 3)

    distinctive = keyness(content, total)

    return {
        "totals": {"words": total, "unique_words": len(freq),
                   "sentences": len(sent_lengths), "documents": len(texts)},
        "distinctive_vocabulary": distinctive,
        "top_content_words": content.most_common(top_n),
        "top_function_words": func.most_common(40),
        "top_bigrams": [(" ".join(b), c) for b, c in bigrams.most_common(40)],
        "top_trigrams": [(" ".join(t), c) for t, c in trigrams.most_common(30)],
        "sentence": {"mean_length": mean_len, "median_length": median_len,
                     "burstiness_stdev": stdev,
                     "min": min(sent_lengths) if sent_lengths else 0,
                     "max": max(sent_lengths) if sent_lengths else 0},
        "paragraph": {"mean_sentences": mean_para},
        "punctuation_counts": punct,
        "punctuation_per_1000w": punct_per_1000,
        "contractions": {"count": contractions, "per_1000w": per1000(contractions),
                         "nt_vs_not_rate_pct": contraction_nt_rate},
        "hedges": hedge_counts,
        "hedge_rate_per_1000w": per1000(sum(hedge_counts.values())),
        "intensifiers": intens_counts,
        "sentence_initial_connectors": sent_initial.most_common(15),
        "synonym_binaries": binaries,
        "spelling_variants": variants,
        "plain_verb_signal": verb_signal,
        "type_token_ratio": {"first_500_words": ttr_500, "overall": ttr_all},
    }

def statistics_pstdev(xs):
    m = sum(xs) / len(xs)
    return math.sqrt(sum((x - m) ** 2 for x in xs) / len(xs))

# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------

def md_report(stats, top_n):
    t = stats["totals"]
    out = []
    out.append(f"# Corpus index\n")
    out.append(f"- Documents: {t['documents']}")
    out.append(f"- Words: {t['words']:,}  |  Unique: {t['unique_words']:,}  |  Sentences: {t['sentences']:,}\n")

    s = stats["sentence"]
    out.append("## Quantitative layer (transcribe into profile Section 5)\n")
    out.append(f"- Avg sentence length: {s['mean_length']} words (median {s['median_length']}); **burstiness (σ): {s['burstiness_stdev']}** (min {s['min']}, max {s['max']}). If σ ≫ mean, a few no-punctuation outliers (pasted lists) are inflating it — trust the median.")
    out.append(f"- Avg paragraph length: {stats['paragraph']['mean_sentences']} sentences")
    out.append(f"- Type-token ratio: first-500w {stats['type_token_ratio']['first_500_words']}, overall {stats['type_token_ratio']['overall']}")
    for k, v in stats["punctuation_per_1000w"].items():
        out.append(f"- {k} per 1000w: {v}  (raw {stats['punctuation_counts'][k]})")
    c = stats["contractions"]
    out.append(f"- Contractions: {c['count']} ({c['per_1000w']}/1000w); n't-vs-not rate ~{c['nt_vs_not_rate_pct']}%")
    out.append(f"- Hedge rate: {stats['hedge_rate_per_1000w']}/1000w")
    out.append("- Top sentence-initial connectors: " +
               ", ".join(f'"{w}" ({c})' for w, c in stats["sentence_initial_connectors"][:10]) + "\n")

    out.append("## Distinctive vocabulary — keyness-ranked (USE THIS for Section 6.1)\n")
    out.append("Words ranked by how much MORE the writer uses them than baseline English "
               "(ratio in parens). This is the vocabulary fingerprint — raw frequency below "
               "is generic. **Then split these by hand into VOICE (travels across topics: "
               "e.g. 'merely', 'till') vs TOPIC (subject-bound: e.g. 'startups', 'lisp').** "
               "The script can rank distinctiveness but can't tell voice from topic — that's "
               "the human-judgment step.\n")
    out.append(", ".join(f'{w} ×{c} ({r}×)' for w, c, pm, r in stats["distinctive_vocabulary"]) + "\n")

    out.append(f"## Top {top_n} content words by RAW frequency (reference only — generic, do not use as the fingerprint)\n")
    out.append(", ".join(f'{w} ({c})' for w, c in stats["top_content_words"]) + "\n")

    out.append("## Top function words (Section 6.2 — stylometric signal)\n")
    out.append(", ".join(f'{w} ({c})' for w, c in stats["top_function_words"]) + "\n")

    out.append("## Synonym binaries (Section 6.6 — the diagnostic table)\n")
    for b in stats["synonym_binaries"]:
        flag = "" if b["writer_picks"] == "plain" else "  ⚠ picks elevated"
        out.append(f"- {b['binary']} → plain {b['plain']} vs elevated {b['elevated']} ({b['writer_picks']}){flag}")
    out.append("")

    if stats.get("spelling_variants"):
        out.append("## Spelling / dialect / archaism variants (Section 6 — highly diagnostic)\n")
        for v in stats["spelling_variants"]:
            out.append(f"- {v['variant']} → picks \"{v['picks']}\" ({v['a']} vs {v['b']})")
        out.append("")

    out.append("## Hedge vocabulary (Section 6.4)\n")
    out.append(", ".join(f'"{h}" ({c})' for h, c in list(stats["hedges"].items())[:12]) + "\n")

    out.append("## Intensifier vocabulary (Section 6.5)\n")
    out.append(", ".join(f'"{i}" ({c})' for i, c in list(stats["intensifiers"].items())[:12]) + "\n")

    out.append("## Plain-verb signal (Section 6.3)\n")
    out.append(", ".join(f'{v} ({c})' for v, c in list(stats["plain_verb_signal"].items())[:20]) + "\n")

    out.append("## Candidate pet phrases — top trigrams (Section 6 pet phrases)\n")
    out.append(", ".join(f'"{t}" ({c})' for t, c in stats["top_trigrams"][:20]) + "\n")

    out.append("---")
    out.append("These numbers are computed, not estimated. Transcribe them into the profile "
               "verbatim, then add the qualitative rules (cognitive moves, rhetorical structure, "
               "voice quirks) that require human judgment on top.")
    return "\n".join(out)

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description="Index a writer's corpus into computed style stats.")
    ap.add_argument("path", help="Corpus directory, single file, or glob")
    ap.add_argument("--top", type=int, default=200, help="How many content words to list (default 200)")
    ap.add_argument("--json", metavar="FILE", help="Also write full JSON stats to FILE")
    args = ap.parse_args()

    files = collect_files(args.path)
    if not files:
        raise SystemExit(f"No .txt/.md/.html files found at: {args.path}")

    texts = []
    for fp in files:
        try:
            texts.append(load_text(fp))
        except Exception as e:  # noqa
            print(f"warning: skipped {fp}: {e}", file=sys.stderr)

    stats = analyze(texts, args.top)
    if args.json:
        with open(args.json, "w", encoding="utf-8") as f:
            json.dump(stats, f, indent=2)
        print(f"(wrote JSON to {args.json})\n", file=sys.stderr)
    print(md_report(stats, args.top))

if __name__ == "__main__":
    main()
