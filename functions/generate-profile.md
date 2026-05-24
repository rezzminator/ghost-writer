# Function: Generate / maintain a profile

Loaded by `SKILL.md` when the task is **authoring or maintaining** a profile — extracting a new one (Mode A), calibrating it (A.5), auditing it for drift (C), or updating it (D). For *using* a profile to write, see `functions/use.md` instead.

This file is long on purpose. Extraction happens once per writer (and occasionally for maintenance), so depth here costs nothing on the frequent path. Read it fully before extracting a non-trivial profile.

Read alongside the references this points to: `extraction-checklist.md`, `cognitive-moves.md`, `rhetorical-structure.md`, `vocabulary-fingerprint.md`, `llm-isms.md`. Run the bundled `scripts/index_corpus.py`.

---

## Extraction principles

These govern everything below. (The router carries the short version; this is the full treatment.)

### The corpus is the source of truth

Every rule must be grounded in evidence. Attach a short quoted example AND a frequency to each rule — not "uses em-dashes" but "em-dash ~3 per 1000 words; e.g., 'and then — without warning — it stopped'". If you can't find a quote that demonstrates the rule, the rule isn't really there. Drop it. **Under-claiming beats over-claiming.** The alternative — a confident-sounding profile of generic "good writing" rules — makes generated text sound like default-Claude prose with a costume on, not the actual person.

### Density, not presence

For every recurring quirk, capture **the rate**. "Em-dashes ~3/1000w", not "uses em-dashes". The indexer computes these; transcribe them. A documented rate is also a *ceiling* for generation — see `functions/use.md`.

### VOICE vs PLATFORM vs BORDERLINE

Before recording any rule, classify it. Mark the bucket in the profile.

- **VOICE** — a personal pattern that travels with the writer across formats ("starts paragraphs with 'so'").
- **PLATFORM** — a convention of the medium the corpus came from, not the writer (Slack: short single-sentence messages; academic: passive voice and hedging).
- **BORDERLINE** — could be either; flag and ask, or note low-confidence.

If you encode platform conventions as personal voice, the imitation reads fine in the original medium and wrong everywhere else. With a single-medium corpus, default ambiguous patterns to PLATFORM unless the pattern is clearly the writer's own.

### What NOT to capture

- **Opinions, beliefs, values.** Downstream of cognitive moves; read fake when ported.
- **Subject matter / topics.** A corpus about cooking → "writes about food" is not a style rule.
- **Voice / tone / personality descriptors** ("warm", "snarky", "earnest"). Subjective labels. The cognitive-moves layer captures the *moves* that produce these impressions, with quotes; the labels themselves are out.
- **Coarse cognitive archetypes** ("thinks like an engineer"). Too broad; quote specific moves.
- **Generic good-writing virtues** ("uses active voice"). Only if the corpus shows them as *distinctively* present, with numbers or two quotes.
- **Platform conventions** confused as personal voice.
- **LLM-isms in the corpus.** If the corpus clusters patterns from `llm-isms.md`, verify with the user before encoding any of them.

The line: a move is something you can quote two distinct instances of. A vibe descriptor is something you'd have to *argue* the writer demonstrates. If you're arguing, it's not in scope.

---

## Mode A: Extract a style profile

### Step 1: Vet the corpus

Read `references/extraction-checklist.md` for full rules. Short version:

- **10+ documents, 2+ formats** is the floor. Single-format corpora encode the format's conventions as voice.
- **No AI-generated content.** AI in the corpus poisons extraction.
- **Recency:** prefer the last 2 years. **Length variety:** short and long. **Single author.**

If the corpus fails any rule, say so explicitly in *Confidence notes*. A tentative profile from a thin corpus is honest; a confident one is a lie.

### Step 2: Run the corpus indexer (compute, don't estimate)

Before reading anything by hand:

```bash
python3 scripts/index_corpus.py <corpus-dir-or-file> --top 200 --json profiles/<name>/index.json
```

Dependency-free (Python 3 stdlib); reads `.txt`/`.md`/`.html`. It computes — exactly, not by estimate — everything countable:

- **The quantitative layer (Section 5):** totals, avg sentence length and burstiness (σ), avg paragraph length, type-token ratio, punctuation rates per 1000w (**`—` and the literal `--` separately** — the split that catches the em-dash leak), contraction rate, hedge rate, question rate, sentence-initial connectors.
- **The vocabulary tables (Sections 6.1–6.6):** the **keyness-ranked distinctive lexicon** (use this, NOT raw frequency — see Step 3c), the top function words, the plain-verb signal, ranked hedges and intensifiers, the **synonym-binaries table** computed across all inflections, and **spelling/dialect variants** (till/until, among/amongst, -ize/-ise…).
- **Candidate pet phrases:** top bigrams and trigrams.

**Transcribe the indexer's numbers verbatim.** Save the JSON next to the profile as `profiles/<name>/index.json` (same folder) — `functions/use.md`'s checker reads it later. For a corpus the indexer can't reach (pasted samples), fall back to careful manual counting and mark numbers as estimates.

### Step 3: Read the four layers (the human-judgment work)

The indexer counts; you read. Run these passes, each grounded in two-quote evidence:

**Step 3 — 8 mechanical dimensions** (`extraction-checklist.md`): sentence patterns, opening patterns, vocabulary, structural patterns, tone markers, formatting habits, language-specific patterns, LLM-ism scan. The countable parts are done; this pass is for what needs a reader.

**Step 3a — cognitive moves** (`cognitive-moves.md`): framing, reasoning, concretization, reflexive rejections, conclusion shape, audience assumptions, argument shape. Use the file's extraction prompts. A move is a rule only if you can quote two distinct moments.

**Step 3b — rhetorical structure** (`rhetorical-structure.md`): opening shape, argument arc, scale-shifts, example-texture mix, reference horizon, self-reference pattern, term-coining, meta-commentary, negation-as-thesis, definition-by-compression, aphorism placement, footnote habit. Two high-leverage prompts: classify 10+ openings for the dominant shape; trace the full arc of 5 pieces. This is the most-often-missed layer — a profile that nails mechanics and vocabulary but skips it produces right sentences in the wrong arc.

**Step 3c — vocabulary fingerprint** (`vocabulary-fingerprint.md`): the countable parts (function words, verbs, hedges, intensifiers, synonym binaries, spelling variants) come from the indexer. **For Section 6.1 (the lexicon), use the indexer's keyness-ranked "Distinctive vocabulary" output, NOT raw frequency.** Raw frequency surfaces generic words every writer shares ("one", "good", "people"); keyness surfaces what's distinctive ("merely", "till"). Then do the judgment the script can't: split the keyness list into **voice** (travels across topics) vs **topic** (subject-bound — exclude) vs residual names/boilerplate (drop). This split is the clearest case where the indexer gives a candidate set and a human still has to read. Then add the categories the indexer can't compute: casualisms, profanity-in-context, sentence-final shape, topic-shift habits, question shape, pet-phrase selection.

### Step 4: Classify, rate, and scale depth to the corpus

For each rule: quoted example, density figure, VOICE / PLATFORM / BORDERLINE, confidence (high / medium / tentative).

**Depth scales with the corpus.** A 500-word sample supports a short tentative profile. A 500k-word corpus across 200+ pieces supports a *dense reference document* — producing a thin one wastes the signal. For a large corpus (50k+ words), aim for:

- **Distinctive lexicon:** 40–60 voice words from the keyness list (split from topic), not a handful.
- **Synonym binaries + spelling variants:** every pair the indexer surfaces with data.
- **Cognitive moves:** 2–4 per category, each with 2+ quoted instances — keep reading until moves repeat.
- **Rhetorical structure:** openings classified across 15–20 samples; the full coined-terms catalog; multiple negation-as-thesis and definition-by-compression examples.
- **Quirks and pet phrases:** exhaustive from the n-gram tables.

The discipline doesn't change — every rule still needs evidence; depth means *more evidenced rules*, never padding. If a large corpus yields a thin profile, you stopped reading too early. Calibration (A.5) and audit/update (C/D) deepen it further over time.

### Step 5: Save the profile

Default path: `profiles/<name>/profile.md`. If not writeable, fall back to the outputs folder. Show the rules in chat too.

### Profile template

Position matters. **Banned-words and never-say lists go first** — Claude reads top-down and earlier constraints bind generation hardest. Format-specific modes go last so they don't bleed across formats.

```markdown
# Style Profile: <name or context>

Source corpus: ~<word count> words across <N> documents in <list formats>. Date range: <YYYY-MM> to <YYYY-MM>.
Profile created: <YYYY-MM-DD>. Last audit: —.

## 1. Banned words & phrases (never-say list)
- **Banned words:** "<word>" (0 occurrences in <N> words; the writer uses "<alternative>" instead)
- **Banned phrases:** "<phrase>"
- **Banned constructions:** <pattern, e.g., "rule-of-three lists with parallel structure">
- **Rendering tell, never allowed:** the literal `--` double-hyphen (render `—` only, at the §5 ceiling).
Source: explicit absences in the corpus + LLM-ism patterns from `llm-isms.md` confirmed absent.

## 2. Anti-performative rules
- One-time usages are NOT signature moves. Don't manufacture catchphrases from a single occurrence.
- Don't announce the writing ("Let's dive in"). Don't perform casualness. Match densities; don't crank.

## 3. Cognitive moves & frames
(each rule: two quoted instances + move-type. See cognitive-moves.md)
### Framing moves
- [VOICE | high] <Move>. Type: <reframe / reject / steelman / concretize / zoom-out / reduce>. Instances: "<q1>" / "<q2>"
### Reasoning moves
- [VOICE | …] <Move>. Type: <counterexample / comparison / inversion / incentives / falsification / mechanism / constraint>. Instances: "<q1>" / "<q2>"
### Concretization tendencies
- [VOICE | …] <Pattern + density>. Instances: "<q1>" / "<q2>"
### Reflexive rejections
- [VOICE | …] <Refusal>. Two cases where the writer had the option and didn't: "<c1>" / "<c2>"
### Shape of conclusion
- [VOICE | …] <Shape>. Closing sentences: "<c1>" / "<c2>"
### Audience assumptions
- [VOICE | …] <What's left unexplained>. Evidence: <…>
### Argument shape
- [VOICE | …] <Shape>. Two pieces: <p1> / <p2>

## 4. Rhetorical structure & essay arc
(see rhetorical-structure.md; each rule: 2 instances or a density)
### 4.1 Opening shape — Dominant: <…>; Runner-up: <…>; Instances: "<a>" / "<b>"
### 4.2 Argument arc — Dominant: <…>; Alternates: <…>; Instances: <p1> / <p2>
### 4.3 Scale-shifts — Rate /1000w: <N>; Direction: <…>; Samples: "<x>" / "<y>"
### 4.4 Example-texture mix — anecdote <%>, historical <%>, named-company <%>, dated <%>, hypothetical <%>, data <%>, domain-transfer <%>; dominant: <…>
### 4.5 Reference horizon — Temporal span: <…>; Domain span: <…>; Domains: <…>
### 4.6 Self-reference pattern — "I" freq: <N>; distribution: assertion <%>, anecdote <%>, uncertainty <%>, procedural <%>, opinion <%>
### 4.7 Term-coining — per 10kw: <N>; examples: "<t>"…; slot: <…>
### 4.8 Meta-commentary — per 10kw: <N>; examples: "<q>" (or none)
### 4.9 Negation-as-thesis — % of theses leading with negation: <%>; examples: "<t>"
### 4.10 Definition-by-compression — per 10kw: <N>; examples: "<X is Y>"
### 4.11 Aphorism placement — Dominant slot: <…>; samples: <p1> / <p2>
### 4.12 Footnote habit (long-form only) — density/1000w: <N>; function: <…>; tonal contrast: <…> (or N/A)

## 5. Quantitative layer (computed by index_corpus.py — transcribe verbatim)
- Avg sentence length: <N>w; **burstiness (σ): <N>**
- Avg paragraph length: <N> sentences; Type-token ratio (first 500w): <N>
- Em-dash `—`/1000w: <N>; literal `--`/1000w: <N> (render only `—`); semicolons: <N>; colons: <N>; ellipses: <N>
- Contraction rate: <N>/1000w; Hedge rate: <N>/1000w; Exclamation: <N>/1000w; Question: <N>/1000w
- Top sentence-initial connectors: "<x>" (Nx), …

## 6. Vocabulary fingerprint
### 6.1 Distinctive lexicon (KEYNESS-ranked, not raw frequency)
- **Voice words (the fingerprint):** "<w>" (<keyness>×), … (40–60 for a large corpus)
- **Topic words (excluded from generation):** "<w>", …
- **Dropped boilerplate/names:** "<w>", …
### 6.2 Function-word patterns — "<ratio observation>"; pronoun preferences <…>
### 6.3 Verb preferences — top verbs <…>; plain-to-elevated ratio <…>
### 6.4 Hedge vocabulary — "<hedge>" (Nx), …; avoided: "<…>"
### 6.5 Intensifier vocabulary — "<word>" (Nx), …; avoided: "<…>"
### 6.6 Synonym binaries (computed) — <plain>/<elevated> → "<plain>" (N vs N); … (all the indexer surfaces)
### 6.6b Spelling / dialect / archaism variants (computed) — till/until → "<…>" (N vs N); -ize/-ise → "<…>"; …
### 6.7 Casualism / internet markers — "<marker>" at <density>, or "none observed"
### 6.8 Profanity — rate + words, or "none in corpus"
### 6.9 Sentence-final vocabulary — dominant shape: <…>; samples
### 6.10 Topic-shift vocabulary — most-used: "<word>" (Nx), or "paragraph break alone"
### 6.11 Question vocabulary — dominant shape(s): "<…>"
### 6.12 Banned-by-omission (lexical) — "<word>", …
### Pet phrases — "<phrase>" (Nx), … (split voice vs topic)

## 7. Sentence structure & rhythm
- [VOICE | …] <Rule>. Example: "<quote>"  · Paragraph shape: <…>

## 8. Quirks & idiosyncrasies
- [VOICE | …] <Rule, with rate>. Example: "<quote>"

## 9. Negative rules (patterns demonstrably absent)
- <e.g., "0 'utilize' in N words; uses 'use'.">

## 10. Default mode — <informational / narrative / mixed> + why

## 11. Format-specific modes — blog / email / chat / social register notes

## 12. Voice in action (prompt-ready examples)
- Long-form opening (~50w): <example>  · Email (~3 sentences): <example>  · Chat (~1–2 sentences): <example>

## 13. Confidence notes
- <tentative rules, coverage gaps, open questions>

## Changelog
- <YYYY-MM-DD> Created from <source>. <N> docs, <list formats>.
```

---

## Mode A.5: Calibration round (run after first extraction)

Extraction misses things humans only notice in fresh output. Run this every time after Mode A.

1. Generate **3 short calibration samples** — one per most-likely-use format (blog opener + email reply + chat message). Show them.
2. Ask the user to tag each issue: `WRONG` (rule's wrong), `OVERSTATED` / `UNDERSTATED` (density off), `MISSING` (real pattern not captured), `NEEDS_NUANCE` (true sometimes), `LLM_ISM` (default-Claude leaking — cross-ref `llm-isms.md`), `NOT_ME` (whole sample feels off).
3. Apply: WRONG/OVERSTATED/UNDERSTATED/NEEDS_NUANCE → revise the rule's density or condition; MISSING → add a rule with the user's example as evidence; LLM_ISM → add the catalog pattern to Section 1; NOT_ME → re-run extraction (structural miss).
4. Log the change in the changelog. Re-render once. Stop after one revision unless the user wants another pass — convergence, not perfection.

Dumont's profile grew 333 → 510 lines through three calibration rounds; most growth was rules automated extraction missed because they only become visible in fresh output.

---

## Mode C: Audit a profile against recent writing

Use when a profile exists and the user wants to know if it still fits. Cadence: every 6–8 weeks of active writing, or after a major shift.

1. Read the profile. 2. Read N recent pieces (≥3). Treat as a fresh corpus. 3. Re-run the indexer on the new corpus. 4. For each rule, check: does it still hold? Sample a quote. 5. Look for new patterns. 6. Produce a drift report in the **4-bucket structure**:

```markdown
# Drift Report: <profile name>
Compared profile dated <YYYY-MM-DD> against <N> recent pieces (~<word count>).

## Numbers, then vs. now
| Metric | Profile | Recent | Δ |
|---|---|---|---|
| Avg sentence length / Burstiness / Em-dashes per 1000w / … | … | … | … |

## Strong (rules that still hold) — <Rule>. Recent example: "<quote>"
## Thin (weakening evidence) — <Rule>. Was [high], now [medium]/absent. Counter-example: "<quote>"
## Missing (new patterns) — <Rule>. Recent example: "<quote>"
## Fix (decayed/shifted, with proposed edit) — <Rule>. Was X, now Y. Proposed: <revised rule>.

## Recommendation — <update / no update / partial with these edits>
```

The 4 buckets (strong / thin / missing / fix) make it obvious what's actionable. Don't auto-update in Mode C — surfacing is the audit's job; updating is Mode D.

## Mode D: Update an existing profile

Triggered by a Mode C drift report, A.5 calibration feedback, or fresh user notes.

1. Open the profile. 2. Apply changes — adjust densities, update/remove decayed rules, add new patterns with evidence. 3. **Append a changelog entry** (date + one-line summary — this is how profiles compound and how you revert an overshoot). 4. Show the diff. 5. Optionally re-run an A.5 calibration pass.

---

## Output format

- **Mode A:** the profile (saved + shown). Optionally followed by A.5.
- **Mode A.5:** calibration samples + tag request; after feedback, revised profile + diff.
- **Mode C:** the 4-bucket drift report (saved + shown).
- **Mode D:** the diff + updated profile (saved).

## Edge cases (extraction)

- **Corpus under ~150 words or single document.** Tentative profile; offer to proceed with caveats or ask for more.
- **Single-format corpus.** Mark platform-conditioned patterns PLATFORM; warn it needs a calibration pass for other media.
- **Multilingual writer.** Extract per language; rhythm/punctuation carry across, vocabulary mostly doesn't. Note coverage.
- **Sample contains AI-generated text.** Detection cues in `llm-isms.md`. Verify with the user before encoding any as voice — the worst possible failure of this skill.
- **Writer-in-conflict missing.** Most corpora bias neutral; if the profile will be used for adversarial writing, ask for a disagreement-heavy piece or flag the gap in Confidence notes.
- **Never hand-polish the profile to look better.** Fix it through calibration (A.5) or audit/update (C/D), so it stays a true product of the corpus.
