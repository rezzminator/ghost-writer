---
name: ghostwriter
version: "1.4.2"
repo: "https://github.com/mreza0100/ghost-writer"
description: Use when the user wants to extract a reusable writing-style profile from a corpus, generate text in a specific person's style, audit or update an existing voice profile, or humanize AI-sounding text via the bundled human profile. Trigger on phrases like "match my writing style", "write like this", "make it sound like me", "voice profile", "voice DNA", "audit/update my style profile", or when the user pastes a substantial sample and asks for new text in the same voice. Do not use for generic copyediting, grammar cleanup, or broad tone shifts.
---

# Ghostwriter

This file is a **router**: it carries the cross-cutting rules, then dispatches to the function file for the task. Detailed workflows live in `functions/`, loaded when needed.

## Router — which function to read

| The user wants to…                                                           | Mode            | Read this                           |
| ---------------------------------------------------------------------------- | --------------- | ----------------------------------- |
| Extract a profile from a corpus; calibrate it; audit it for drift; update it | A / A.5 / C / D | **`functions/generate-profile.md`** |
| Write something in a profiled voice; humanize AI-sounding text               | B               | **`functions/write.md`**            |

Routing notes:

- "Study how I write" / "build a voice profile" / "learn my style" / "here's my writing" → **generate-profile**.
- "Write X like me" / "in the style of [person]" / "make it sound like me" / "humanize this" → **write**.
- **Chained request** ("here's my writing, now draft X in my voice") → generate-profile (Mode A) first, then write (Mode B), in the same response.
- If the user just asks for writing and names no profile → **write**, defaulting to the `human` profile.

Read the matching function file in full before starting — this router has the principles, not the steps.

## What this skill captures (four layers)

Every layer is evidence-grounded: every rule needs at least two quoted instances from the corpus.

1. **Mechanical fingerprint** — sentence rhythm, punctuation density, formatting quirks.
2. **Cognitive moves** — the operations the writer performs on an idea before assembling words: how they frame problems, test claims, concretize, refuse, conclude.
3. **Rhetorical structure** — the essay-scale shape: opening pattern, argument arc, scale-shifts, example-texture, reference horizon, self-reference, term-coining, negation-as-thesis, aphorism placement, footnotes.
4. **Vocabulary fingerprint** — the specific words the writer reaches for when alternatives exist: verb preferences, hedges, intensifiers, synonym binaries, spelling variants, casualisms.

This is **not** a persona-direction skill — it captures observable, quotable mechanics, not vibe descriptors. A cognitive move ("reflexively asks 'compared to what?'") is in scope because you can quote it; a vibe label ("is skeptical") is out because you'd have to argue it. If output still feels off after all four layers are dialed in, the remaining gap is persona — pair with a separate persona prompt.

## Cross-cutting principles (apply in every mode)

- **Corpus is the source of truth.** If you can't quote it, it isn't a rule. Under-claiming beats over-claiming.
- **Density, not presence.** Capture the _rate_ ("semicolons ~4/1000w"), not the fact. A documented rate is also a _ceiling_ for generation, never a license.
- **Compute, don't estimate.** The countable layers come from `scripts/index_corpus.py` at extraction and are verified by `scripts/check_output.py` at generation. Counting beats guessing; the scripts caught real bugs that eyeballing missed.
- **`human` is a base layer every profile inherits.** Generation is always `human` (strip LLM tells) + the person's fingerprint on top — never the fingerprint bolted onto default-Claude prose. The em-dash `—`, the literal `--`, chatbot closers, and sycophancy stay banned for every profile. (Full treatment in `functions/write.md`.)
- **Depth scales with the corpus.** A 500-word sample → a short tentative profile; a 500k-word corpus → a dense reference document. A thin profile from a big corpus means you stopped reading too early. (Full treatment in `functions/generate-profile.md`.)
- **Write in a fresh agent, then gate on an independent review.** Mode B writing happens in a freshly-spawned sub-agent that loads the profile + references first, never inline in the caller's accumulated context. The draft then passes an independent `review` agent that checks it against the profile; the writer fixes and re-submits until review passes. (Full treatment in `functions/write.md`.)

## Bundled references (read as needed)

- `references/llm-isms.md` — 29-pattern catalog of LLM-tells. Used in corpus sanity-checks, the `LLM_ISM` calibration tag, and the generation self-check.
- `references/extraction-checklist.md` — corpus-prep rules + the 8-dimension mechanical extraction grid.
- `references/cognitive-moves.md` — the idea-level layer (layer 2): framing, reasoning, concretization, rejections, conclusion shape.
- `references/rhetorical-structure.md` — the essay-arc layer (layer 3): opening, arc, scale-shifts, term-coining, negation-as-thesis, footnotes.
- `references/vocabulary-fingerprint.md` — the lexical layer (layer 4): keyness lexicon, verbs, hedges, synonym binaries, spelling variants.

## Bundled scripts

- `scripts/index_corpus.py` — corpus indexer (extraction). Strips per-record metadata (`Source:`/timestamp/URL) and social-export bylines (`— Name (@handle) date`) before tokenizing, so it's reproducible on scraped corpora. Computes word frequencies, the **keyness-ranked distinctive lexicon** (not raw frequency), function-word table, synonym binaries, spelling variants, punctuation rates (`—` vs `--`), burstiness, and median sentence length + σ. `python3 scripts/index_corpus.py <corpus> --top 200 --json profiles/<name>/index.json`. Save the JSON next to the profile.
- `scripts/check_output.py` — output verifier (generation). Checks a draft against the `human` base layer + a profile's densities; exit-codes on hard fails. `python3 scripts/check_output.py draft.txt --profile-stats profiles/<name>/index.json`.

## Built-in profile: `human`

`profiles/human/profile.md` is the negative profile and the default fallback — it bans the LLM-ism catalog and default-LLM moves/vocabulary instead of capturing one writer. Use it directly to humanize text or for generic-but-human writing, and as the base layer under every person profile. Don't run calibration (A.5) or audit (C) on it — there's no corpus to drift from.

## Version & updates

To update: `git pull` the repo (in frontmatter), then re-copy `SKILL.md`, `functions/`, `references/`, `scripts/`, and `profiles/human/profile.md` into the installed skill directory.
