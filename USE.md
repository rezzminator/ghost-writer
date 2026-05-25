# Using Ghostwriter

Practical guide for generating a style profile and writing with it. For the methodology behind each step, see `SKILL.md` (the router), `functions/generate-profile.md` and `functions/write.md` (the workflows), and the files in `references/`.

The skill works in two halves:

- **Extract** a profile from a corpus of someone's writing (Mode A) — done once per writer, refined over time.
- **Generate / humanize** text with that profile (Mode B) — done whenever you write.

Two scripts make the countable parts deterministic: `scripts/index_corpus.py` (extraction) and `scripts/check_output.py` (generation). Both are dependency-free Python 3.

---

## 1. Prepare a corpus

Collect the writer's real writing into a folder of `.txt`, `.md`, or `.html` files. Aim for:

- **10+ documents across 2+ formats** (blog + email + chat, say). A single-format corpus only captures "that person in that format" — the profile will say so in its Confidence notes.
- **No AI-generated text.** It poisons the extraction — you'd encode Claude's patterns as the writer's.
- **Recent** writing (last ~2 years) weighted over old.
- **A mix of lengths** — short messages and long pieces.

Example layout:

```
corpus/
├── blog/      post1.md  post2.md ...
├── email/     thread1.txt ...
└── chat/      slack-export.txt ...
```

---

## 2. Generate a profile (Mode A)

With Claude Code open in this repo, point it at the skill and your corpus:

```
Read SKILL.md and follow Mode A to extract a style profile for <name> from
the corpus in <path/to/corpus>. Run scripts/index_corpus.py for the computed
layers, save its JSON to profiles/<name>/index.json, extract all four layers,
and save the profile to profiles/<name>/profile.md. Then run Mode A.5 (calibration).
```

What the skill does, in order:

1. **Vets the corpus** against the rules above; flags gaps in Confidence notes.
2. **Runs the indexer** — computes word frequencies, the keyness-ranked distinctive lexicon, function-word table, synonym binaries, spelling variants, punctuation rates, and sentence burstiness. These are *counted*, not estimated.
3. **Reads the four layers** with human judgment on top of the counts:
   - *Mechanical* — sentence rhythm, punctuation, formatting quirks.
   - *Cognitive moves* — how the writer frames problems, tests claims, concludes.
   - *Rhetorical structure* — opening shapes, argument arcs, term-coining, scale-shifts.
   - *Vocabulary* — the distinctive lexicon (split into **voice** vs **topic** by hand — the script ranks distinctiveness but can't tell "merely" (voice) from "startups" (topic)).
4. **Saves** `profiles/<name>/profile.md` plus the `profiles/<name>/index.json` sidecar.
5. **Calibrates (Mode A.5)** — generates a few samples and asks you to tag what's off (`WRONG`, `OVERSTATED`, `MISSING`, `NOT_ME`, etc.). Your tags get applied once.

Depth scales with the corpus: a large corpus should produce a dense, exhaustively-evidenced profile, not a skeleton. If it comes back thin from a big corpus, tell Claude to keep reading — it stopped early.

**Don't hand-edit the profile to make it look better.** Fix it through calibration (Mode A.5) or audit/update (below), so the profile stays a true product of the corpus.

---

## 3. Write with a profile (Mode B)

```
Using profiles/<name>/profile.md, write <the thing you want> in <name>'s voice.
```

The skill reads the profile top-down (bans first, then cognitive moves, then rhetorical structure, then vocabulary), drafts, runs a three-pass self-review — including `scripts/check_output.py` against the profile's index JSON — then hands the draft to a fresh `review` agent that checks it against the profile and sends back any corrections, looping until it passes. The output ends with a short "Rules applied" note so you can see which patterns it leaned on.

Key idea: **every profile inherits the `human` base layer.** Generating as a specific person still strips AI tells — the person's fingerprint sits on top of humanized prose, never on top of default-Claude prose. A documented density (e.g. "em-dash ~1/1000w") is a *ceiling*, not a license, and the literal `--` is never produced.

If you don't name a profile, the skill defaults to `human` — generic-but-human writing with the AI tells removed.

---

## 4. Humanize AI-sounding text

```
Humanize this text with the human profile: <paste text>
```

Uses `profiles/human/profile.md` (the negative profile) to rewrite the text — removing the 29 LLM-isms, the default reasoning shapes, and the literal `--` — without imposing any specific person's voice. To humanize *and* match a person, name their profile instead.

---

## 5. Verify output yourself (optional)

You can run the checker directly on any draft:

```
python3 scripts/check_output.py draft.txt --profile-stats profiles/<name>/index.json
```

It exits non-zero on hard fails (literal `--`, chatbot closers, sycophancy) and warns on AI vocabulary, low burstiness, em-dash-over-ceiling, and synonym-binary inversions. Useful as a git pre-commit gate or a quick check on anything — even text the skill didn't write.

---

## 6. Keep a profile current (Modes C & D)

Writing styles drift. Every 6–8 weeks of active writing, or after a big change (new job, new platform):

```
Audit profiles/<name>/profile.md against these recent pieces: <paths>. Then update it.
```

- **Audit (Mode C)** re-runs the indexer on the new writing and produces a drift report in four buckets — *strong* (rules that hold), *thin* (weakening), *missing* (new patterns), *fix* (decayed). It doesn't change the profile.
- **Update (Mode D)** applies the drift findings, appends a changelog entry, and shows the diff. Profiles compound — each cycle sharpens them.

---

## 7. The scripts at a glance

| Script | When | What it does |
|---|---|---|
| `scripts/index_corpus.py` | Extraction (Mode A) | Counts everything countable: keyness-ranked distinctive lexicon, function words, synonym binaries, spelling variants, punctuation rates, burstiness. Markdown report + JSON. |
| `scripts/check_output.py` | Generation (Mode B) | Verifies a draft against the humanization base layer + a profile's densities. Exit-codes on hard fails. |

```
python3 scripts/index_corpus.py <corpus> --top 200 --json profiles/<name>/index.json
python3 scripts/check_output.py <draft> --profile-stats profiles/<name>/index.json
```

---

## 8. Gotchas

- **Vocabulary = keyness, not raw frequency.** If a profile's top "voice words" are generic ("one", "good", "people", "way"), it used raw counts by mistake. The fingerprint is the words the writer uses *more than baseline English* ("merely", "till"), split from topic words ("startups", "lisp").
- **The indexer counts; the human reads.** They're partners. The script can't tell voice from topic, can't read cognitive moves, can't judge tone. It removes the guesswork from what's countable so judgment goes where it's needed.
- **Single-format corpus → single-format profile.** Patterns from an essays-only corpus mis-fire on email/Slack. The profile flags this; calibrate before cross-format use.
- **Profiles are personal.** Only `profiles/human/profile.md` ships in git; user profiles and their `.index.json` sidecars stay local (see `.gitignore`).
- **Installed-skill path caveat:** when the skill lives in `.claude/skills/gwriter/`, call scripts by their full path, since Claude Code runs bash from the project root. When the repo itself is the working directory, the relative paths in SKILL.md resolve directly.
