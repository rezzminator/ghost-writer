# Extraction Checklist

A reference used during Mode A (extract) to make sure the corpus is good enough and the analysis covers the dimensions that matter. Read this before beginning extraction; cite specific items by name when you note confidence in the profile.

**Four-layer extraction.** This file covers the **mechanical layer** of extraction — the 8 dimensions of observable surface patterns (sentence structure, formatting, paragraph shape, openers, tone markers, language-specific patterns, LLM-ism scan, plus the broad vocabulary-fingerprint dimension which gets its own deep extraction in `vocabulary-fingerprint.md`). The **cognitive-moves layer** — framing, reasoning, concretization, refusals, conclusion shape, audience assumptions, argument shape — is in `cognitive-moves.md`. The **rhetorical-structure layer** — opening shape, full argument arc, scale-shifts, example-texture mix, reference horizon, self-reference patterns, term-coining propensity, meta-commentary, negation-as-thesis, definition-by-compression, aphorism placement, footnote habit — is in `rhetorical-structure.md`. The **vocabulary-fingerprint layer** — verb preferences, hedge vocabulary, intensifiers, synonym binaries, casualisms, sentence-final and topic-shift vocabulary — is in `vocabulary-fingerprint.md`. Read all four before extracting a non-trivial profile. The mechanical layer alone produces texturally correct prose that argues like a stranger; the cognitive-moves layer alone produces the right thinking in default-Claude prose; the rhetorical-structure layer alone produces the right shape filled with the wrong sentences; the vocabulary-fingerprint layer alone produces the right words assembled by someone with a different mind. You need all four.

## Corpus preparation

Before reading anything, check the corpus against these rules. They came from Sam Dumont's voice-skill methodology and are the difference between capturing a writer's voice and capturing the conventions of one platform they happen to use.

**Minimum bar.** 10+ documents across 2+ formats. A "format" is the medium: blog post, email, Slack message, doc, forum comment, tweet. The diversity is non-negotiable: with one format, you capture the format's conventions (Slack: short, lowercase, emoji-tolerant; email: greeting + sign-off; LinkedIn: line breaks every sentence) and bake them in as personal voice. Done that way, the imitation reads fine in the source medium and obviously wrong everywhere else.

**Authenticity.** AI-generated content in the corpus poisons everything. If the writer used Claude or any LLM to draft a piece, exclude it. Encoding LLM patterns as personal voice is the worst possible failure mode of this skill. When in doubt, ask the user. If a piece reads like default-LLM prose (em-dashes everywhere, "moreover," neat tricolons, balanced paragraph lengths, "ever-evolving landscape"), flag it — the answer matters. See `llm-isms.md` for the detection cues.

**Recency.** Writing styles drift. Samples from the last 2 years are worth more than samples from 5 years ago. Note the date range of the corpus in the profile so future audits (Mode C) can compare apples to apples.

**Length variety.** Voice manifests differently in a 3-sentence Slack message and a 2,000-word essay. Include both. A profile built only on long-form will mis-fire on short-form, and vice versa.

**Single-author.** All samples must be from the writer being profiled. This sounds obvious; it gets violated when "samples I wrote" includes pieces a co-author or editor heavily revised. Ask explicitly.

If the corpus fails any of these rules, the profile will be tentative. Say so explicitly in the profile's Confidence notes section, rather than producing a confident profile from thin material.

## The 8-dimension extraction grid

When you read the corpus, scan along each of these dimensions independently. Patterns in one dimension don't predict patterns in another — a writer can have idiosyncratic vocabulary and totally vanilla sentence structure, or vice versa. Treating each dimension separately catches things a one-pass read misses.

For each dimension, look for **patterns that repeat across the corpus** (not single occurrences). Capture: the rule, a short quoted example, a frequency or density figure, and a VOICE / PLATFORM / BORDERLINE classification.

1. **Sentence patterns.** Average length and standard deviation (call this "burstiness" — a writer running 5- and 35-word sentences alternately has very different rhythm from one running 18 ± 4). Use of fragments. Parenthetical asides. How clauses join — comma splices, em-dashes, semicolons, conjunctions, colons. Where verbs land in the sentence. List handling (inline vs bullet).

2. **Opening patterns.** How does the writer start each format? Blog posts vs. emails vs. Slack messages vs. docs. The first 1–3 sentences of each piece. Look for repeated openers ("So,", "OK,", "Quick q:", lowercase-no-greeting). These are the clearest voice fingerprints in many writers.

3. **Vocabulary fingerprint.** Pet phrases that recur 2+ times verbatim. Register (casual / formal / technical / clinical / chatty). Domain jargon — does the writer define terms, assume them, or alternate? Code-switching patterns (across languages or registers). Words the writer demonstrably avoids (the **never-say** list — important and often missed).

4. **Structural patterns.** How does information get ordered in a piece? Top-line first vs. buildup? Headers and how the writer uses them (or doesn't)? Bullet density. Use of bold / italics / inline code. Visual aids (tables, code blocks, images).

5. **Tone markers.** Formality per format. Humor mechanisms (deadpan, hyperbole, self-deprecation, callbacks, none). Directness vs. hedging. How the writer handles disagreement — softens, escalates, ignores. Emotional register: is there one, is it suppressed, does it spike in specific contexts?

6. **Formatting habits.** Capitalization (sentence-initial caps, ALL-CAPS for emphasis, lowercase-everywhere, Title Case headers). Punctuation preferences (em-dash density per 1000w, semicolon presence, ellipsis use, exclamation rate, Oxford comma). Curly vs. straight quotes. Spelling consistency and tolerated typos. Markdown habits.

7. **Language-specific patterns.** Code-switching across languages. Greeting and sign-off conventions. Spelling variants (American / British / regional). Loan words and how they're rendered. (For multilingual writers, voice often travels across languages but vocabulary fingerprint partially resets.)

8. **LLM-ism scan.** Does the corpus already show AI-tells? See `llm-isms.md` for the 29-pattern catalog. If the corpus has clusters of catalog patterns — em-dash overuse, "moreover" / "furthermore," neat tricolons, balanced paragraph lengths — pause and verify with the user before encoding any of them as personal voice.

## Quantitative numbers to record

**Run `scripts/index_corpus.py` to get all of these exactly — do not estimate them by reading.** The indexer computes every item below in one pass, plus the em-dash-vs-`--` split, the question rate, and the full vocabulary tables. Hand-estimation is the old way and it's unreliable; the script exists precisely so these numbers are counts, not impressions.

The numbers it produces (the diagnostic baseline for Mode C audit — drift shows up here first):

- **Average sentence length** (words/sentence) and **standard deviation (= burstiness)**
- **Average paragraph length** in sentences
- **Type-token ratio** (first 500 words) — vocabulary diversity
- **Em-dash `—`, double-hyphen `--`, semicolon, colon, ellipsis rates per 1000 words** (the `—`/`--` split matters: a profile that counts only `—` undercounts dash usage and the model then leaks `--`). Measure both, but note: the em-dash and `--` are banned at generation regardless of the measured rate — the count is corpus data, not a license to reproduce.
- **Contraction rate**
- **Hedge-word rate** per 1000 words, with the specific hedges ranked
- **Top sentence-initial connectors** with counts
- **Exclamation and question rates / 1000 words**

Only fall back to manual counting when the corpus can't be reached as files (e.g. pasted samples). In that case say "rough estimates from a small corpus" and round generously. Don't fake precision.

## What human review catches that automated extraction misses

After the first-pass profile is drafted, set aside automated reasoning and ask: would the writer read this profile and recognize themselves?

The patterns automated extraction reliably misses (per Dumont):

- **One-time tics misclassified as patterns.** A single occurrence of "ahah" once isn't a rule. Three occurrences in three separate pieces is.
- **Patterns that need format conditioning.** "Uses lowercase sentence starts" — but only in Slack and Reddit, not in emails to clients. The rule should be conditional, not blanket.
- **Negative rules that are louder than positive rules.** "Never says 'utilize'" or "never starts emails with 'I hope this finds you well'" can be more diagnostic than what they do say.
- **The shape of disagreement and pushback.** Most corpora bias toward neutral writing; the writer's voice in conflict is often invisible from a generic sample set. If possible, include at least one piece where the writer disagrees with someone.
- **Cross-language carry-over.** For multilingual writers, certain habits (punctuation conventions, sentence rhythm) carry across languages while vocabulary doesn't. This is hard to spot without explicitly looking.

The Mode A.5 calibration round exists to surface these. The 7-tag feedback (`WRONG / OVERSTATED / UNDERSTATED / MISSING / NEEDS_NUANCE / LLM_ISM / NOT_ME`) maps directly to fixes — see `functions/generate-profile.md`.
