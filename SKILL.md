---
name: ghostwriter
version: "1.2.0"
repo: "https://github.com/mreza0100/ghost-writer"
description: Use when the user wants to extract a reusable writing-style profile from a corpus, generate text in a specific person's style, audit or update an existing voice profile, or humanize AI-sounding text via the bundled human profile. Trigger on phrases like "match my writing style", "write like this", "make it sound like me", "voice profile", "voice DNA", "audit/update my style profile", or when the user pastes a substantial sample and asks for new text in the same voice. Do not use for generic copyediting, grammar cleanup, or broad tone shifts; this skill is for evidence-grounded reproduction of a writer's mechanical fingerprint, cognitive moves, rhetorical structure, and vocabulary.
---

# Ghostwriter

Capture how someone writes from a corpus of their writing, generate new text that reproduces it, and maintain the profile as their habits drift. The corpus is the **source of truth** — every rule comes from evidence in the corpus, never from priors about good writing.

This file is a **router**. It carries the cross-cutting rules that apply to everything, then dispatches to the function file for the task at hand. The detailed workflows live in `functions/` so they only load when needed.

## Router — which function to read

| The user wants to… | Mode | Read this |
|---|---|---|
| Extract a profile from a corpus; calibrate it; audit it for drift; update it | A / A.5 / C / D | **`functions/generate-profile.md`** |
| Write something in a profiled voice; humanize AI-sounding text | B | **`functions/use.md`** |

Routing notes:

- "Study how I write" / "build a voice profile" / "learn my style" / "here's my writing" → **generate-profile**.
- "Write X like me" / "in the style of [person]" / "make it sound like me" / "humanize this" → **use**.
- **Chained request** ("here's my writing, now draft X in my voice") → generate-profile (Mode A) first, then use (Mode B), in the same response.
- If the user just asks for writing and names no profile → **use**, defaulting to the `human` profile.

Read the matching function file in full before starting. Don't try to execute from this router alone — it has the principles, not the steps.

## What this skill captures (four layers)

Every layer is evidence-grounded: every rule needs at least two quoted instances from the corpus.

1. **Mechanical fingerprint** — sentence rhythm, punctuation density, formatting quirks.
2. **Cognitive moves** — the operations the writer performs on an idea before assembling words: how they frame problems, test claims, concretize, refuse, conclude.
3. **Rhetorical structure** — the essay-scale shape: opening pattern, argument arc, scale-shifts, example-texture, reference horizon, self-reference, term-coining, negation-as-thesis, aphorism placement, footnotes.
4. **Vocabulary fingerprint** — the specific words the writer reaches for when alternatives exist: verb preferences, hedges, intensifiers, synonym binaries, spelling variants, casualisms.

This is **not** a persona-direction skill. It captures observable, quotable mechanics — not worldview, opinions, or vibe descriptors ("warm", "snarky"). A cognitive move ("reflexively asks 'compared to what?'") is in scope because you can quote it; a vibe label ("is skeptical") is out because you'd have to argue it. If output still feels off after all four layers are dialed in, the remaining gap is persona — pair this skill with a separate persona prompt.

## Cross-cutting principles (apply in every mode)

- **Corpus is the source of truth.** If you can't quote it, it isn't a rule. Under-claiming beats over-claiming.
- **Density, not presence.** Capture the *rate* ("em-dash ~1/1000w"), not the fact. A documented rate is also a *ceiling* for generation, never a license.
- **Compute, don't estimate.** The countable layers come from `scripts/index_corpus.py` at extraction and are verified by `scripts/check_output.py` at generation. Counting beats guessing; the scripts caught real bugs that eyeballing missed.
- **`human` is a base layer every profile inherits.** Generation is always `human` (strip LLM tells) + the person's fingerprint on top — never the fingerprint bolted onto default-Claude prose. The literal `--`, chatbot closers, and sycophancy stay banned for every profile. (Full treatment in `functions/use.md`.)
- **Depth scales with the corpus.** A 500-word sample → a short tentative profile; a 500k-word corpus → a dense reference document. A thin profile from a big corpus means you stopped reading too early. (Full treatment in `functions/generate-profile.md`.)

## Bundled references (read as needed)

- `references/llm-isms.md` — 29-pattern catalog of LLM-tells. Used in corpus sanity-checks, the `LLM_ISM` calibration tag, and the generation self-check.
- `references/extraction-checklist.md` — corpus-prep rules + the 8-dimension mechanical extraction grid.
- `references/cognitive-moves.md` — the idea-level layer: framing, reasoning, concretization, rejections, conclusion shape, audience assumptions, argument shape.
- `references/rhetorical-structure.md` — the essay-arc layer: opening shape, arc, scale-shifts, example-texture, reference horizon, self-reference, term-coining, meta-commentary, negation-as-thesis, definition-by-compression, aphorism placement, footnotes.
- `references/vocabulary-fingerprint.md` — the lexical layer: distinctive (keyness) lexicon, verbs, hedges, intensifiers, synonym binaries, spelling variants, casualisms.

## Bundled scripts

- `scripts/index_corpus.py` — corpus indexer (extraction). Computes word frequencies, the **keyness-ranked distinctive lexicon** (not raw frequency), function-word table, synonym binaries, spelling variants, punctuation rates (incl. `—` vs `--`), burstiness. `python3 scripts/index_corpus.py <corpus> --top 200 --json profiles/<name>/index.json`. Save the JSON next to the profile.
- `scripts/check_output.py` — output verifier (generation). Checks a draft against the `human` base layer + a profile's densities; exit-codes on hard fails. `python3 scripts/check_output.py draft.txt --profile-stats profiles/<name>/index.json`.

## Built-in profile: `human`

`profiles/human/profile.md` is the negative profile and the default fallback — it bans the LLM-ism catalog and default-LLM moves/vocabulary instead of capturing one writer. Use it directly to humanize text or for generic-but-human writing, and as the base layer under every person profile. Don't run calibration (A.5) or audit (C) on it — there's no corpus to drift from.

## Version & updates

**Current:** 1.2.0 · **Repo:** https://github.com/mreza0100/ghost-writer

- **1.2.0** — The indexer and verifier scripts (`scripts/index_corpus.py`, `scripts/check_output.py`) and the `functions/` router targets are now bundled in the repo (previously described in the changelog but not shipped). Added a standalone `USE.md` quickstart and polished the reference layers (extraction-checklist, llm-isms, vocabulary-fingerprint). `.gitignore` now excludes generated index JSON and `.bak` backups.
- **1.1.1** — Indexer hardening for scraped/exported corpora: strip per-record metadata (`Source:`/timestamp/URL lines) and social-export attribution bylines (`— Name (@handle) date`) before tokenizing, so the index is reproducible without manual cleaning (these were polluting multi-format runs with `t`/`source`/`@handle` tokens and inflating the em-dash rate). Added median sentence length alongside σ, robust to pasted-list outliers.
- **1.1.0** — Split into router + `functions/generate-profile.md` + `functions/use.md` for progressive disclosure (router stays cheap on every trigger; heavy workflows load only when needed). Added keyness-ranked distinctive lexicon and spelling-variant detection to the indexer.
- **1.0.0** — Four-layer architecture, five modes (A/A.5/B/C/D), built-in human profile, compute-don't-estimate scripts.

To update: `git pull` the repo, then re-copy `SKILL.md`, `functions/`, `references/`, `scripts/`, and `profiles/human/profile.md` into your installed skill directory.
