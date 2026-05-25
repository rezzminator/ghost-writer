#!/usr/bin/env python3
"""
check_output.py — verify generated text against the humanization base layer and
(optionally) a specific writer's profile. The deterministic half of the
self-review: instead of asking the model to notice its own leaks, count them.

Two layers of checks:

  1. Universal `human` base layer (always runs, no profile needed). Catches the
     LLM tells every profile inherits: the em-dash `—` and the literal `--`
     double-hyphen (both banned in all output), AI vocabulary
     (delve/utilize/leverage/...), banned transitions
     (moreover/furthermore/additionally), chatbot closers, sycophancy,
     negation-parallelism, and low burstiness (uniform sentence lengths).

  2. Profile-aware checks (when given --profile-stats or --profile). Compares the
     draft's measured densities to the profile's documented ceilings, flags
     banned words from the profile, and catches synonym-binary inversions
     (the draft picking "utilize" when the writer always picks "use").

Usage:
    python3 check_output.py draft.txt
    python3 check_output.py draft.txt --profile-stats profile_index.json
    python3 check_output.py draft.txt --profile profiles/paul-graham/profile.md
    cat draft.txt | python3 check_output.py -

Exit code: 0 if no FAIL-level issues, 1 if any FAIL. (WARN does not fail.)
Dependency-free (Python 3 stdlib).
"""

import argparse
import json
import math
import re
import sys
from collections import Counter

# ---------------------------------------------------------------------------
# Universal LLM-tell lists (the `human` base layer)
# ---------------------------------------------------------------------------

AI_VOCAB = [
    "delve", "utilize", "leverage", "robust", "seamless", "holistic",
    "comprehensive", "intricate", "vital", "crucial", "pivotal",
    "transformative", "groundbreaking", "cutting-edge", "navigate", "foster",
    "bolster", "underscore", "showcase", "unlock", "harness", "elevate",
    "empower", "spearhead", "multifaceted", "nuanced", "paramount", "testament",
    "realm", "tapestry", "beacon", "embark", "unleash", "unveil", "myriad",
    "plethora", "endeavor", "facilitate", "commence", "ascertain",
]

BANNED_TRANSITIONS = ["moreover", "furthermore", "additionally"]

PHRASE_TELLS = [
    "it's not just", "not just a", "in today's", "fast-paced", "ever-evolving",
    "at its core", "it's worth noting", "it is important to note",
    "when it comes to", "in conclusion", "in the realm of", "a testament to",
    "plays a crucial role", "rich tapestry", "navigating the complexities",
    "the world of", "needle in a haystack", "game-changer", "game changer",
]

CLOSERS = ["i hope this helps", "let me know if", "feel free to reach",
           "happy to help", "hope this helps", "if you have any questions"]

SYCOPHANCY = ["great question", "you're absolutely right", "you are absolutely right",
              "excellent point", "great point", "what a thoughtful"]

NEGATION_PARALLEL = re.compile(
    r"\bit'?s not just\b.*?\bit'?s\b|"
    r"\bnot only\b.*?\bbut also\b|"
    r"\bisn'?t (?:about|just)\b.*?\bit'?s\b", re.IGNORECASE)

# Synonym binaries (plain side first) for the universal default check.
DEFAULT_BINARIES = [
    ("use", ["utilize", "utilise"]),
    ("help", ["assist"]),
    ("but", ["however"]),       # only flagged sentence-initially below
    ("also", ["additionally", "furthermore", "moreover"]),
    ("make", ["craft"]),
    ("show", ["demonstrate"]),
    ("get", ["obtain", "acquire"]),
    ("about", ["regarding", "concerning"]),
    ("because", ["due to the fact"]),
    ("to", ["in order to"]),
    ("now", ["at this point in time"]),
]

# ---------------------------------------------------------------------------
# Text analysis (shared shape with index_corpus.py)
# ---------------------------------------------------------------------------

WORD_RE = re.compile(r"[A-Za-z]+(?:'[A-Za-z]+)?")
SENT_SPLIT_RE = re.compile(r"[.!?]+(?:\s+|$)")

def tokenize(text):
    return [w.lower() for w in WORD_RE.findall(text)]

def pstdev(xs):
    if len(xs) < 2:
        return 0.0
    m = sum(xs) / len(xs)
    return math.sqrt(sum((x - m) ** 2 for x in xs) / len(xs))

def measure(text):
    tokens = tokenize(text)
    total = max(len(tokens), 1)
    sentences = [s for s in SENT_SPLIT_RE.split(text) if s.strip()]
    lengths = [len(tokenize(s)) for s in sentences]
    lengths = [n for n in lengths if n > 0]
    per1000 = lambda n: round(n / total * 1000, 2)
    return {
        "words": total,
        "sentences": len(lengths),
        "mean_sentence_len": round(sum(lengths) / len(lengths), 2) if lengths else 0,
        "burstiness": round(pstdev(lengths), 2),
        "em_dash_char": text.count("—"),
        "double_hyphen": len(re.findall(r"--", text)),
        "semicolon_per_1000": per1000(text.count(";")),
        "colon_per_1000": per1000(text.count(":")),
        "em_dash_per_1000": per1000(text.count("—")),
        "tokens": tokens,
        "freq": Counter(tokens),
        "sentences_raw": sentences,
    }

# ---------------------------------------------------------------------------
# Checks
# ---------------------------------------------------------------------------

class Report:
    def __init__(self):
        self.items = []  # (level, message)
    def fail(self, msg): self.items.append(("FAIL", msg))
    def warn(self, msg): self.items.append(("WARN", msg))
    def ok(self, msg):   self.items.append(("PASS", msg))
    def has_fail(self):  return any(l == "FAIL" for l, _ in self.items)

def universal_checks(text, m, rep):
    low = " " + text.lower() + " "

    # 1. Em-dash —: banned in all output, any profile.
    if m["em_dash_char"]:
        rep.fail(f"Em-dash `—` appears {m['em_dash_char']}x. "
                 f"Banned in all output — recast with commas, periods, or parentheses.")
    else:
        rep.ok("No em-dash `—`.")

    # 1b. Literal -- double-hyphen: banned in all output, any profile.
    if m["double_hyphen"]:
        rep.fail(f"Literal `--` appears {m['double_hyphen']}x. "
                 f"Banned — recast with commas, periods, or parentheses.")
    else:
        rep.ok("No literal `--` double-hyphen.")

    # 2. AI vocabulary
    hits = [(w, m["freq"].get(w, 0)) for w in AI_VOCAB if m["freq"].get(w, 0)]
    # catch hyphenated/lemma variants not in token freq
    for w in AI_VOCAB:
        if "-" in w and w in text.lower():
            hits.append((w, text.lower().count(w)))
    if hits:
        rep.warn("AI-vocabulary words present (confirm against profile; default is to cut): "
                 + ", ".join(f'{w}×{c}' for w, c in sorted(set(hits), key=lambda x: -x[1])))
    else:
        rep.ok("No flagged AI-vocabulary words.")

    # 3. Banned transitions
    bt = [(w, low.count(" " + w + " ")) for w in BANNED_TRANSITIONS if low.count(" " + w + " ")]
    if bt:
        rep.warn("LLM transition words: " + ", ".join(f'"{w}"×{c}' for w, c in bt)
                 + ' — prefer "but"/"and"/"so" or no transition.')

    # 4. Phrase tells
    pt = [p for p in PHRASE_TELLS if p in low]
    if pt:
        rep.warn("LLM phrase tells: " + ", ".join(f'"{p}"' for p in pt))

    # 5. Closers / sycophancy: hard fails (chat residue)
    cl = [p for p in CLOSERS if p in low]
    if cl:
        rep.fail("Chatbot closer(s): " + ", ".join(f'"{p}"' for p in cl) + " — delete.")
    sy = [p for p in SYCOPHANCY if p in low]
    if sy:
        rep.fail("Sycophancy: " + ", ".join(f'"{p}"' for p in sy) + " — delete.")

    # 6. Negation parallelism
    if NEGATION_PARALLEL.search(text):
        rep.warn('Negation-parallelism construction ("it\'s not just X, it\'s Y" / '
                 '"not only ... but also") — state the point directly.')

    # 7. Burstiness floor (human base layer): sigma >= 7
    if m["sentences"] >= 4:
        if m["burstiness"] < 7:
            rep.warn(f"Burstiness σ={m['burstiness']} is below the human floor (~7). "
                     f"Sentence lengths too uniform — mix in short sentences. "
                     f"(mean len {m['mean_sentence_len']}, {m['sentences']} sentences)")
        else:
            rep.ok(f"Burstiness σ={m['burstiness']} (≥7 human floor).")

def profile_stats_checks(m, stats, rep):
    """Compare against an index_corpus.py JSON (the clean path)."""
    # Burstiness vs profile
    try:
        pb = stats["sentence"]["burstiness_stdev"]
        if m["sentences"] >= 5 and m["burstiness"] < pb * 0.6:
            rep.warn(f"Burstiness σ={m['burstiness']} is well below the writer's "
                     f"σ≈{pb}. Output reads more uniform than the writer.")
    except Exception:
        pass
    # Synonym binaries from computed stats
    for b in stats.get("synonym_binaries", []):
        if b.get("writer_picks") == "plain":
            # writer prefers plain; flag elevated forms appearing in the draft
            label = b["binary"]
            elevated = label.split("/")[-1].strip().split()[0]
            if m["freq"].get(elevated.lower(), 0):
                rep.warn(f'Binary inversion: draft uses "{elevated}" but the writer '
                         f'picks the plain side ({label}).')

def profile_md_checks(m, md_text, rep):
    """Best-effort parse of a markdown profile (the convenient path)."""
    # Banned words from Section 1
    banned = set()
    for line in md_text.splitlines():
        if "banned word" in line.lower() or "banned-by-omission" in line.lower():
            banned.update(w.lower() for w in re.findall(r'"([a-zA-Z\- ]+)"', line))
    banned.discard("")
    present = [w for w in banned if m["freq"].get(w, 0) or (" " in w and w in " ".join(m["tokens"]))]
    if present:
        rep.fail("Profile-banned words present: " + ", ".join(f'"{w}"' for w in present))
    elif banned:
        rep.ok(f"None of the {len(banned)} profile-banned words appear.")
    # Synonym binaries: lines like "use / utilize → ... use ..." with the plain pick bolded
    for line in md_text.splitlines():
        mobj = re.match(r"\s*-\s*([a-z]+)\s*/\s*([a-z/ ]+?)\s*(?:→|->|—)", line.strip(), re.IGNORECASE)
        if mobj:
            plain = mobj.group(1).lower()
            elevated_side = mobj.group(2).lower()
            # if the line indicates plain is the pick, flag elevated tokens
            for elev in re.findall(r"[a-z]+", elevated_side):
                if elev != plain and m["freq"].get(elev, 0) and "plain" in line.lower():
                    rep.warn(f'Possible binary inversion: draft uses "{elev}"; '
                             f'profile lists plain pick "{plain}".')

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description="Check generated text against humanization + a profile.")
    ap.add_argument("draft", help="Draft text file, or '-' for stdin")
    ap.add_argument("--profile-stats", metavar="JSON", help="index_corpus.py JSON for the writer (clean comparison)")
    ap.add_argument("--profile", metavar="MD", help="Profile markdown (best-effort parse for banned words / binaries)")
    args = ap.parse_args()

    text = sys.stdin.read() if args.draft == "-" else open(args.draft, encoding="utf-8", errors="ignore").read()
    if not text.strip():
        raise SystemExit("Empty draft.")

    m = measure(text)
    rep = Report()

    universal_checks(text, m, rep)

    if args.profile_stats:
        try:
            stats = json.load(open(args.profile_stats, encoding="utf-8"))
            profile_stats_checks(m, stats, rep)
        except Exception as e:
            rep.warn(f"Could not read --profile-stats: {e}")
    if args.profile:
        try:
            profile_md_checks(m, open(args.profile, encoding="utf-8", errors="ignore").read(), rep)
        except Exception as e:
            rep.warn(f"Could not read --profile: {e}")

    # ---- report ----
    print(f"# Output check — {m['words']} words, {m['sentences']} sentences, "
          f"burstiness σ={m['burstiness']}\n")
    order = {"FAIL": 0, "WARN": 1, "PASS": 2}
    icon = {"FAIL": "✗ FAIL", "WARN": "! WARN", "PASS": "✓ PASS"}
    for level, msg in sorted(rep.items, key=lambda x: order[x[0]]):
        print(f"{icon[level]}  {msg}")

    fails = sum(1 for l, _ in rep.items if l == "FAIL")
    warns = sum(1 for l, _ in rep.items if l == "WARN")
    print(f"\n{'='*60}")
    if fails:
        print(f"RESULT: {fails} FAIL, {warns} WARN — fix the FAILs before delivering.")
    elif warns:
        print(f"RESULT: 0 FAIL, {warns} WARN — review warnings against the profile.")
    else:
        print("RESULT: clean. No humanization or profile violations detected.")
    sys.exit(1 if fails else 0)

if __name__ == "__main__":
    main()
