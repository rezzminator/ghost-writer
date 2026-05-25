# Function: Write with a profile (generate / humanize)

Loaded by `SKILL.md` when the task is **producing text** — writing something new in a profiled voice, or humanizing AI-sounding text. For *building or maintaining* a profile, see `functions/generate-profile.md`.

(Note: this is the skill's execution workflow. The repo-root `USE.md` is a separate human-facing quick-start guide — different audience.)

Mode B covers two operations on the same machinery:

- **Generate** — input is a writing prompt; produce new text in the profile's style.
- **Humanize** — input is existing AI-sounding text; rewrite it through the profile (typically `human`) to strip LLM-tells.

The only difference is whether you start from a prompt or from an existing draft to revise.

---

## Write in a fresh agent, then gate on an independent review

The caller never drafts inline — accumulated context dilutes the profile. The flow is orchestrated by the caller, one agent-spawn deep:

1. **Spawn the writer.** A general-purpose agent, briefed to **read in full first** — this file, the chosen `profiles/<name>/profile.md` and its `index.json`, `profiles/human/profile.md`, and the `references/*.md` it needs — then run the steps below and return the draft plus the Rules-applied note.
2. **Spawn a fresh reviewer.** A general-purpose agent given `functions/review.md` and the draft. It returns `PASS` or `NEEDS CORRECTION` plus specific remarks. Fresh eyes are the point — the writer is blind to its own profile drift.
3. **Fix and re-review.** On `NEEDS CORRECTION`, hand the remarks back to the writer (continue the *same* writer so it keeps the profile loaded) to revise, then re-run the reviewer on the new draft.
4. **Stop at PASS, or after three review rounds.** If it still fails at the cap, deliver the best draft and surface the outstanding remarks — never loop forever, never hide a failure.

The caller relays the final draft; it does not write or review itself. If you are the writer agent, start at *Choosing a profile*. If you are the reviewer, follow `functions/review.md`.

---

## The one rule that governs everything here: every profile inherits `human`

`human` is not an alternative you pick instead of a person profile. It's the **floor every generation stands on**. Every output is `human` (strip the LLM tells) + the person's fingerprint (add their patterns) on top. Generating as Paul Graham still removes AI tells; the PG fingerprint is layered onto humanized prose, never onto default-Claude prose.

When the two layers seem to conflict:

- **The `human` ban list is the default for anything the person profile doesn't document.** Silence in a person profile means "inherit the human ban", not "anything goes".
- **A person profile overrides a `human` ban only with documented evidence, and only at the documented density.** A writer's documented semicolon rate at ~4/1000w means a 500-word piece gets *one or two*, not a sprinkle — a documented rate is a ceiling, not a license.
- **Rendering tells are never overridable:** the em-dash `—` and the literal `--`, emoji section markers, "I hope this helps" closers, "great question" sycophancy. Banned for every profile, full stop. Em-dashes are banned outright for every profile — recast with commas, periods, or parentheses; never produce `—` or `--`, even if the writer uses them.

So Pass 1 of the self-review runs for **every** profile, every time. A person profile changes what's permitted and at what density; it never turns the scan off.

---

## Choosing a profile

1. If the user names a profile, use it.
2. If the user provides a corpus and asks for new text in one go, do `functions/generate-profile.md` Mode A first (quick), then come back.
3. If neither, default to `profiles/human/profile.md` and note which profile was used in the Rules-applied note. Don't ask for routine requests — defaulting to `human` is right and trivial to override.

---

## Steps

1. **Read the profile top-down.** Order matters.
   - Banned words + anti-performative rules first (Sections 1–2) — they shape every following choice.
   - **Cognitive moves (Section 3)** next — they shape *how the writer approaches this topic*.
   - **Rhetorical structure (Section 4)** — plan the macro shape *before* drafting: opening shape, argument arc, example-texture mix, whether to coin a term, where the aphorism lands.
   - Then quantitative (5) and vocabulary (6) — especially 6.6 synonym binaries and 6.6b spelling variants and 6.4 hedges. Internalize the writer's specific verb/hedge/spelling picks before drafting, because Claude's defaults otherwise win every micro-choice.
   - Then sentence structure (7) and the rest for the drafting itself.
2. **If humanizing,** read the input once for content, once for which LLM-isms it carries (cross-ref `references/llm-isms.md`). Plan the rewrite at the paragraph level — wholesale restructuring beats find-and-replace.
3. **Apply the cognitive moves to the topic before drafting words.** The most-skipped step. Ask: how would this writer frame this question? What would they refuse? Where would they concretize? What shape would the argument take? What would the conclusion be? Do those operations mentally, *then* draft.
4. **Check the priority hierarchy** (below) — context conventions can override the profile.
5. **Draft (or rewrite).** Reproduce profile rules at documented densities. Match densities; don't crank. For `human` especially, vary sentence length aggressively — burstiness σ ≥ 7 is the single most important target.
6. **Run the three-pass self-review** before delivering.
7. **Append the Rules-applied note**, then return the draft for the review gate above.

**On a revision pass** (the caller returns with review remarks): address each remark specifically, re-run the affected self-review pass, update the Rules-applied note, and return the revised draft — don't re-draft from scratch.

---

## Priority hierarchy (when style and context conflict)

Personal style does not always win.

1. **Hard contextual norms** — legal briefs, academic abstracts, regulatory filings, medical notes, formal letters. Form conventions override; apply style at the margins (vocabulary, paragraph shape).
2. **Audience norms** — when the audience won't tolerate the writer's quirks (rambling exec summary for a phone-reading CEO). Compress; keep voice cues; downscale density.
3. **Personal style** — default for blog posts, emails, social, casual writing.
4. **Platform conventions** — apply on top of style, only for the platform being written to. Don't import another platform's conventions.

When the trade-off kicks in, say so in the Rules-applied note.

---

## Three-pass self-review (do this before delivering)

Three failure modes; a single pass catches one and misses the others.

**Pass 1 — LLM-ism scan (runs for EVERY profile).** Applies the `human` base layer; never skipped. **Run it mechanically first** if you have file access:

```bash
python3 scripts/check_output.py draft.txt --profile-stats profiles/<name>/index.json
```

It exit-codes 1 on hard fails (`—`, `--`, chatbot closers, sycophancy — the em-dash and double-hyphen are now hard fails, not warnings) and warns on AI vocabulary, banned transitions, negation-parallelism, low burstiness, and synonym-binary inversions. Fix every FAIL and review every WARN against the profile. Then do the human read for what the script can't judge (subtle phrasing, tone). No file access? Skim against `references/llm-isms.md` — cues: em-dashes, "moreover/furthermore/actually", neat tricolons, balanced paragraph lengths, "it's not just X, it's Y", "navigate the complexities", "in today's fast-paced world", chatbot closers, sycophancy.

For each catalog match, in order: (1) Is it a rendering tell never allowed (`—`, `--`, emoji markers, closers, sycophancy)? Delete regardless of profile. (2) Does the person profile document this pattern with a density? If not, the `human` ban applies — revise. (3) If documented, is the draft within the ceiling? Allowed-at-1.0/1000w is not the same as allowed; cut to rate. The most common failure: the model reads a low documented rate as "allowed" and sprinkles well above it.

**Pass 2 — Performative scan.** Every place the draft has a "signature move" applied loudly: check Section 2. Is the move actually high-density in the corpus, or did you crank a one-time tic into a catchphrase? Smell test: would the writer's friend roll their eyes?

**Pass 3 — Moves, structure, and vocabulary** (three lenses, one read):

- *Moves.* Read for the *thinking*, ignoring words. Did the writer's cognitive moves (Section 3) apply, or did default-Claude reasoning sneak in — 5-angle survey, both-sides balance, "while X has merits, Y also has strengths", unrequested synthesis, generic uplift? If the mechanics are right but the thinking reads like a committee, fix the thinking.
- *Structure.* Look at the macro shape. Did the opening match the writer's dominant shape (4.1)? The arc (4.2)? Example-texture ratios (4.4)? If the writer coins terms (4.7), is one present? Right sentences in the wrong arc reads more wrong than the reverse.
- *Vocabulary.* Scan the words. Verbs match the plain-vs-elevated profile (6.3)? Hedges/intensifiers from the writer's lists (6.4–6.5), not Claude defaults ("perhaps", "potentially", "quite")? Synonym binaries respected (6.6)? Spelling variants right (6.6b — no stray "whilst"/"towards"/"-ise")? The single most common vocabulary failure: reaching for the elevated synonym when the writer always picks plain.

Skipped, this pass produces "mechanically right but conceptually a stranger" / "thinking right but in the wrong shape" / "thinking and shape right but worded by someone else."

---

## Common failure modes

- **Topic drift.** Corpus about hiking, prompt about taxes — don't import hiking metaphors. Style ≠ subject.
- **Caricature.** Match densities, not just presence.
- **Default-Claude leak.** Well-balanced varied prose with tidy transitions is *your* default, not theirs. Find the messier/weirder spots in the corpus and lean in.
- **Persona invention.** Don't invent personality, opinions, or biographical hooks the corpus didn't show.
- **Length mismatch.** Infer length from the task, not from corpus length.
- **Platform contamination.** Don't import LinkedIn line breaks into an email or Slack lowercase into a memo.

---

## "Rules applied" note format

End the response with:

```markdown
---
**Profile used:** `<profile name>` (e.g., `human` default, or `<person>`)
**Operation:** generate | humanize

**Rules applied (top hits):**
- <Rule>: <how reproduced, with target density if relevant>
- ...

**Self-review:**
- LLM-ism pass: <patterns found and removed, OR "none flagged">
- Performative pass: <quirks dialed back, OR "no cranking detected">
- Moves / structure / vocabulary: <how each shaped the draft, OR "using human defaults">

**Trade-offs:** <if priority hierarchy kicked in, briefly. Otherwise omit.>
```

Keep it short — audit trail, not essay. The profile-name line matters even when defaulting to `human`, so the user can swap if they meant a specific person.

## Edge cases (generation)

- **No profile named** → default to `human`; say so.
- **Profile passed in but parts conflict with a fresh sample** → flag the conflict; ask which to honor. Don't silently override.
- **"Write more like this" mid-draft** → treat the existing fragment as a tiny corpus; quick mental extract; continue.
- **Thin/low-confidence profile** → keep the high-confidence rules, fall back to `human` for the rest, and say which.
