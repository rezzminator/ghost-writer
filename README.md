# Ghostwriter

**Version:** 1.3.0 · **License:** MIT · **Repo:** [github.com/mreza0100/ghost-writer](https://github.com/mreza0100/ghost-writer)

A Claude Code skill that captures how someone writes — across four layers: the mechanical fingerprint (sentence rhythm, punctuation density, formatting quirks), the cognitive moves (how they frame problems, what they refuse, where they concretize, how they shape conclusions), the rhetorical structure (the essay-scale shape: opening pattern, full argument arc, scale-shifts, example-texture mix, reference horizon, self-reference patterns, term-coining, aphorism placement), and the vocabulary fingerprint (the specific words they reach for when alternatives exist) — from a corpus of their writing, and generates new text that reproduces all four layers.

This is not persona imitation. It doesn't try to capture worldview, opinions, or vibe. It reads observable, measurable, quotable patterns at four levels and reproduces them at the documented densities. The result is auditable: every rule in a profile has at least one quoted example from the source corpus, classified by type and rated by confidence.

## Why this exists

LLMs have a default voice. You've read it: balanced paragraphs, confident verbs, "moreover," neat tricolons, tidy transitions. When you ask an LLM to "write in someone's style," it usually produces its own default prose wearing a costume — a few surface-level quirks layered on top of the same underlying rhythm, the same default vocabulary, the same default reasoning shape, and the same default essay arc.

Ghostwriter takes a different approach. It builds a structured profile from a corpus of real writing across four layers:

- **Mechanical fingerprint** — density-based rules (not just presence/absence), patterns classified as VOICE / PLATFORM / BORDERLINE, a banned-words list of LLM-isms the writer demonstrably avoids.
- **Cognitive moves** — the repeatable operations the writer performs on an idea _before_ assembling words: framing moves, reasoning moves, concretization tendencies, reflexive rejections, conclusion shape, audience assumptions, argument shape.
- **Rhetorical structure** — the essay-scale shape between cognitive moves and the mechanical/vocabulary layers: opening shape, full argument arc, scale-shifts, example-texture mix, reference horizon, self-reference patterns, term-coining propensity, meta-commentary, negation-as-thesis, definition-by-compression, aphorism placement, footnote habit. This is the layer that captures *what shape the piece takes as it unfolds* — and the most-often-missed layer in style imitation.
- **Vocabulary fingerprint** — the specific lexical choices: verb preferences, hedge vocabulary, intensifiers, synonym binaries, casualism markers, sentence-final and topic-shift vocabulary. This is the layer classical stylometry (the Federalist Papers method) leans on most.

Generated text is then checked against a 29-pattern LLM-ism catalog (surface), the writer's cognitive moves (thinking), the writer's rhetorical structure (shape), and the writer's vocabulary fingerprint (words) before delivery.

## How it works

### Five modes

| Mode                | Input                              | Output                                 |
| ------------------- | ---------------------------------- | -------------------------------------- |
| **A — Extract**     | Corpus of writing samples          | Structured style profile (all four layers) |
| **A.5 — Calibrate** | Profile + user feedback on samples | Refined profile                        |
| **B — Generate**    | Profile + writing prompt           | New text in that style + audit note    |
| **C — Audit**       | Profile + recent writing           | Drift report (4 buckets)               |
| **D — Update**      | Profile + audit/feedback           | Revised profile + changelog            |

Modes chain naturally: A then A.5 for first-time profiling. C then D for maintenance. A then B for one-shot "write like this" requests.

### The profile lifecycle

Profiles are living documents, not one-shot artifacts. They compound with iteration:

1. **Extract** from a corpus (10+ documents, 2+ formats recommended)
2. **Calibrate** with tagged feedback (WRONG, OVERSTATED, UNDERSTATED, MISSING, NEEDS_NUANCE, LLM_ISM, NOT_ME)
3. **Generate** using the profile
4. **Audit** against new writing every 6-8 weeks
5. **Update** to close drift gaps

### What a profile captures

The profile is organized into four layers, with each rule evidence-grounded by quoted examples from the corpus.

**Mechanical layer:**

- **Banned words and phrases** — patterns the writer demonstrably avoids, placed first because position affects generation
- **Anti-performative rules** — guards against exaggerating one-time patterns into theatrical signature moves
- **Quantitative layer** — sentence length, burstiness, punctuation rates per 1000 words, contraction rate, hedge-word rate
- **Sentence structure and rhythm** — paragraph shape, clause-joining patterns, opener variety
- **Quirks** — idiosyncrasies with density figures
- **Negative rules** — patterns that are strikingly absent
- **Format-specific modes** — same voice, different registers (blog vs email vs Slack)

**Cognitive-moves layer:**

- **Framing moves** — reframe, reject, steelman, concretize, zoom-out, reduce
- **Reasoning moves** — test by counterexample, comparison, inversion, incentives, falsification, mechanism, constraint-finding
- **Concretization tendencies** — what the writer pairs abstract claims with
- **Reflexive rejections** — what the writer refuses to accept (appeals to authority, round numbers, "everyone agrees", etc.)
- **Shape of conclusion** — action item, open question, compression, hedge, cut-off
- **Audience assumptions** — what's left unsaid because it's assumed
- **Argument shape** — the structural move-set of how a piece is built

**Rhetorical-structure layer:**

- **Opening shape** — paradox, anecdote, question, scene-setting, direct thesis, negation, etc., with density
- **Full argument arc** — the macro shape of the piece end-to-end
- **Scale-shifts** — rate of concrete↔abstract movement and dominant direction
- **Example-texture mix** — ratios of personal anecdote / historical figure / named company / dated anchor / hypothetical / data / domain-transfer
- **Reference horizon** — temporal span and domain span of citations
- **Self-reference pattern** — when "I" appears and what it's doing (confident assertion / anecdote / uncertainty / procedural)
- **Term-coining propensity** — coined terms per 10,000 words, with structural slot
- **Meta-commentary on the writing itself** — when the writer steps outside the argument
- **Negation-as-thesis frequency** — opening or thesis sentences leading with negation-of-conventional
- **Definition-by-compression** — surprising "X is Y" substitutions used as central tools
- **Aphorism placement** — where compressed principles land in the piece
- **Footnote habit** — density, function, tonal contrast (long-form only)

**Vocabulary-fingerprint layer:**

- **Top content lexicon** — the words that travel across pieces (voice), not the ones tied to single pieces (topic)
- **Function-word patterns** — standout pronoun and connector ratios (classical stylometry's strongest signal)
- **Verb preferences** — plain-to-elevated ratio; identifying picks ("use" not "utilize")
- **Hedge vocabulary** — which specific hedges the writer reaches for ("I think" vs "perhaps")
- **Intensifier vocabulary** — "really / very / super" vs "quite / considerably"
- **Synonym binaries** — the diagnostic table: when alternatives exist, which side did the writer pick consistently
- **Casualism / internet markers** — "lol", emoji, lowercase starts, letter-stretching, with density
- **Profanity** — frequency, words, contexts
- **Sentence-final vocabulary** — what shape sentences land on (hedge / concrete / intensifier)
- **Topic-shift vocabulary** — how paragraph transitions get signaled
- **Question vocabulary** — how questions are phrased
- **Banned-by-omission (lexical)** — words the writer demonstrably avoids
- **Pet phrases** — multi-word recurring units with counts

Every rule at all four layers is tagged: VOICE (travels with the writer) / PLATFORM (convention of the medium) / BORDERLINE (ambiguous). Cognitive-move rules, rhetorical-structure rules, and vocabulary-binary rules additionally require at least two quoted instances from the corpus — single occurrences are not patterns.

### What a profile does NOT capture

- Opinions, beliefs, values
- Subject matter or topics
- Subjective vibe descriptors ("warm," "snarky," "earnest," "contrarian")
- Coarse cognitive archetypes ("thinks like an engineer")
- Generic good-writing or good-thinking virtues (unless distinctively present in the corpus)
- Platform conventions confused as personal voice

The line between an in-scope cognitive move and an out-of-scope vibe descriptor is the evidence rule: a move is something you can quote two distinct instances of. A vibe descriptor is something you'd have to argue the writer demonstrates.

## Built-in profile: `human`

The repo ships with one default profile at `profiles/human/profile.md`. It's the **negative profile** — instead of capturing one writer's fingerprint, it bans the full 29-pattern LLM-ism catalog at the mechanical layer, the default-LLM reasoning moves (both-sides-ism, 5-angle topic surveys, reflexive synthesis, "it depends" without follow-through, false consensus framing) at the cognitive layer, the default-LLM rhetorical patterns (five-point listicles, "In conclusion," closers, manufactured paradox openers, sub-headers every 200 words, footnote cosplay) at the rhetorical layer, and the default-LLM vocabulary (perhaps / potentially / quite / utilize / leverage) at the vocabulary layer.

Use `human` directly when:

- You want to "humanize" some AI-sounding text — no specific writer, just remove the tells.
- You want generic-but-human writing and haven't profiled anyone yet.
- A specific person's profile is too thin to use confidently — fall back to `human`.

If you don't name a profile, `human` is the default.

### `human` is a base layer every profile inherits

This is the key thing to understand: `human` is not just one profile you pick instead of a person profile. It's the **floor that every generation stands on**. Every output is `human` (strip the LLM tells) + the person's fingerprint (add their patterns) on top. Generating as Paul Graham still removes AI tells — the PG fingerprint is layered onto humanized prose, never bolted onto default-Claude prose.

The LLM-ism scan therefore runs for **every** profile, every time. A person profile changes which patterns are permitted and at what density; it never turns the scan off. A documented rate (e.g., PG's em-dash at ~1.0/1000w) is a *ceiling*, not a license — and pure rendering tells like the literal `--` double-hyphen stay banned for every profile regardless. If a writer genuinely uses em-dashes, they're rendered as `—` at the documented low rate.

## Installation

### As a Claude Code skill

Copy the skill files into your project's Claude Code skills directory:

```bash
# From your project root
mkdir -p .claude/skills/gwriter/{functions,references,scripts,profiles}

cp SKILL.md .claude/skills/gwriter/SKILL.md
cp functions/*.md .claude/skills/gwriter/functions/
cp references/*.md .claude/skills/gwriter/references/
cp scripts/*.py .claude/skills/gwriter/scripts/
mkdir -p .claude/skills/gwriter/profiles/human
cp profiles/human/profile.md .claude/skills/gwriter/profiles/human/
```

Then use it in Claude Code by asking naturally ("build a voice profile from these essays", "write this in my voice", "humanize this text") — the skill triggers on the description and routes to the right workflow.

### Architecture: router + functions

`SKILL.md` is a thin **router** (~70 lines) that loads on every trigger. It carries the cross-cutting principles and dispatches to one of two workflow files based on the task:

- **`functions/generate-profile.md`** — extract / calibrate / audit / update a profile (Modes A / A.5 / C / D). Long and detailed, but only loads when you're building a profile (a once-per-writer task).
- **`functions/write.md`** — generate text in a profiled voice, or humanize AI text (Mode B). Loads when you're writing.
- **`functions/review.md`** — fresh-eyes check of a draft against its profile (PASS or specific corrections). The writer loops on it until the draft passes.

This progressive-disclosure split keeps the always-loaded cost low while letting the workflows be as detailed as they need to be.

### As a standalone reference

The files work as a methodology guide even without Claude Code. `SKILL.md` routes; `functions/` holds the workflows and the review gate; `references/` holds the per-layer methodology; `scripts/` holds the indexer and verifier; `USE.md` is a human-facing quick-start.

## Key design decisions

**Four layers, all evidence-grounded.** Mechanics alone produce texturally correct prose that argues like a stranger. Cognitive moves alone produce the right thinking in default-Claude prose. Rhetorical structure alone produces the right shape filled with the wrong sentences. Vocabulary alone produces the right words assembled by someone with a different mind. The profile captures all four, with the same quote-it-or-it-isn't-real discipline.

**Density, not presence.** "Em-dashes ~7.6/1000w" is a rule. "Uses em-dashes" is not. Presence-only rules produce caricature — every quirk gets cranked to maximum.

**Banned words go first; macro shape comes before words.** Position in the profile matters. Constraints encountered early have stronger influence on generation. The never-say list sits at the top. Cognitive moves come next because they shape what gets assembled. Rhetorical structure comes after, because the piece's macro shape gets planned before any sentence is written. Then quantitative numbers and vocabulary fingerprint feed the drafting itself.

**Three-pass self-review.** Pass 1 scans for LLM-isms (the 29-pattern catalog). Pass 2 scans for performative exaggeration. Pass 3 reads the draft along three sub-checks: the _thinking_ (did the writer's cognitive moves apply), the _shape_ (did the opening, arc, example-mix, term-coining match the writer's), and the _words_ (did the synonym binaries get respected; did the writer's hedges and intensifiers show up rather than Claude defaults). These are different failure modes — a single pass catches one and misses the others. On top of the writer's own three passes, an independent `review` agent re-checks the finished draft against the profile — fresh eyes catch leaks the author is blind to, and the writer loops on its corrections until it passes.

**VOICE vs PLATFORM classification.** Without this, a profile built from Slack messages will produce Slack-style text in every format. The classification prevents platform conventions from being encoded as personal voice.

**Compute, don't estimate — on both ends.** Two scripts make the countable parts deterministic. At extraction, `scripts/index_corpus.py` produces word frequencies, the top-200 lexicon, function-word ratios, synonym binaries, punctuation rates, and burstiness — instead of eyeballing the corpus (estimation is lossy and confidently wrong: "this writer uses 'leverage' constantly" when the real count is 3 in 50k words). At generation, `scripts/check_output.py` verifies the draft mechanically — the literal `--`, AI vocabulary, chatbot closers, burstiness floor, em-dash-over-ceiling, synonym-binary inversions — so the self-review doesn't depend on the model noticing its own leaks. The indexer separating the em-dash character `—` from the literal `--` is what caught the most common leak in the first place. Human judgment is reserved for what genuinely needs reading: cognitive moves, rhetorical structure, tone, and which high-frequency words are voice vs. topic.

**Corpus is the source of truth.** Every rule must have a quoted example. If you can't find a quote that demonstrates the rule, the rule isn't there. Under-claiming beats over-claiming.

## Files

```
SKILL.md                             — Router (~70 lines): cross-cutting principles + dispatch to a function
functions/generate-profile.md        — Workflow: extract / calibrate / audit / update a profile (Modes A/A.5/C/D) + the profile template
functions/write.md                   — Workflow: generate text in a voice / humanize AI text (Mode B)
functions/review.md                  — Gate: independent fresh-eyes review of a draft against its profile (PASS / corrections loop)
USE.md                               — Human-facing quick-start guide
scripts/index_corpus.py              — Corpus indexer (extraction): exact word frequencies, keyness-ranked distinctive lexicon, function-word table, synonym binaries, spelling variants, punctuation rates, burstiness (stdlib only)
scripts/check_output.py              — Output verifier (generation): checks a draft for `--`, AI vocabulary, chatbot closers, low burstiness, em-dash-over-ceiling, synonym-binary inversions; exit-codes on hard fails (stdlib only)
references/extraction-checklist.md   — Corpus vetting rules and 8-dimension mechanical extraction grid
references/llm-isms.md               — 29-pattern catalog of LLM-tells with detection cues
references/cognitive-moves.md        — Cognitive-moves layer extraction (7 categories + 8 prompts)
references/rhetorical-structure.md   — Rhetorical-structure layer extraction (12 categories + 12 prompts)
references/vocabulary-fingerprint.md — Vocabulary-fingerprint layer extraction (12 categories + 12 prompts)
profiles/human/profile.md            — Built-in default profile (negative profile / humanizer)
profiles/                            — Where extracted profiles are stored (user profiles gitignored)
```

## The LLM-ism catalog

The `references/llm-isms.md` file catalogs 29 patterns commonly found in LLM-generated text, grouped by surface area:

- **Content patterns** — significance inflation, promotional language, vague attributions
- **Language patterns** — AI vocabulary ("moreover," "leverage," "robust"), copula avoidance, rule of three
- **Style patterns** — em-dash overuse, boldface overuse, signposting announcements
- **Communication patterns** — chatbot closers, sycophantic tone
- **Filler and hedging** — filler phrases, excessive hedging, generic conclusions

This catalog is used during extraction (to verify corpus authenticity), calibration (to identify LLM-ism tags), and generation (Pass 1 of the pre-delivery self-check).

## The cognitive-moves catalog

The `references/cognitive-moves.md` file captures the layer upstream of words — the moves the writer performs on an idea before assembling sentences. Seven categories with extraction prompts:

- **Framing moves** — what the writer does to a problem before arguing about it
- **Reasoning moves** — their reflex when a claim shows up
- **Concretization tendencies** — what they pair abstract claims with (example, number, scenario, or nothing)
- **Reflexive rejections** — what they refuse to accept (the most distinctive cognitive fingerprints are often negative)
- **Shape of conclusion** — how they end a piece
- **Audience assumptions** — what they leave unsaid because it's assumed
- **Argument shape** — the structural shape of how an argument is built

The discipline is the same as the mechanical layer: each rule requires two quoted instances. If you'd have to argue a move is present, it isn't a rule.

## The rhetorical-structure catalog

The `references/rhetorical-structure.md` file captures the essay-arc layer — the shape the piece takes as it unfolds. This is the most-often-missed layer in style imitation; writers like Paul Graham are recognizable largely at this macro scale. Twelve categories with twelve extraction prompts:

- **Opening shape** — paradox, anecdote, question, scene-setting, direct thesis, historical, negation, quoted, numerical, definition
- **Full argument arc** — the macro shape of the piece (problem→reframe→mechanism→examples→advice, or anecdote→generalization, or definition→consequences, etc.)
- **Scale-shifts** — rate and direction of concrete↔abstract movement
- **Example-texture mix** — ratios of personal anecdote / historical / named-company / dated-anchor / hypothetical / data / domain-transfer
- **Reference horizon** — temporal span and domain span of citations within and across pieces
- **Self-reference pattern** — what "I" is doing across instances (confident assertion / anecdote / uncertainty / procedural / opinion)
- **Term-coining propensity** — coined terms per 10,000 words, and the structural slot they occupy
- **Meta-commentary on the writing itself** — when the writer steps outside the argument
- **Negation-as-thesis frequency** — thesis sentences leading with negation-of-conventional rather than positive-claim
- **Definition-by-compression** — surprising "X is Y" substitutions used as central tools
- **Aphorism placement** — opening, midway, closing, or mixed
- **Footnote habit** — density, function, tonal contrast to main text (long-form writers only)

The two highest-leverage sections are **4.1 (opening shape)** and **4.2 (argument arc)** — most writers have one dominant opening shape and one dominant arc, and catching them captures a huge amount of macro-scale fingerprint in two moves.

## The vocabulary-fingerprint catalog

The `references/vocabulary-fingerprint.md` file captures the lexical layer — the specific words the writer reaches for when alternatives exist. This is where classical stylometry's identifying signal lives (the Federalist Papers attribution method works on this layer). Twelve categories with twelve extraction prompts:

- **Top content lexicon** — words that travel across pieces (voice), not those tied to single pieces (topic)
- **Function-word patterns** — pronoun and connector ratios — classical stylometry's strongest signal
- **Verb preferences** — plain vs. elevated; the writer's top 20 verbs
- **Hedge vocabulary** — which specific hedges, not just hedge rate
- **Intensifier vocabulary** — specific intensifiers, not generic "uses intensifiers"
- **Synonym binaries** — the diagnostic table: when alternatives exist, the writer's pick (use/utilize, but/however, weird/strange, etc.)
- **Casualism / internet markers** — "lol", emoji, lowercase, letter-stretching, with density
- **Profanity** — frequency, words, contexts
- **Sentence-final vocabulary** — what shape sentences land on
- **Topic-shift vocabulary** — how paragraph transitions get signaled
- **Question vocabulary** — how questions are phrased
- **Banned-by-omission (lexical)** — words the writer demonstrably avoids

The single highest-leverage section is the synonym-binaries table. Applying those binaries during generation is the fastest way to make output sound like the writer.

## Credits

- Extraction methodology adapted from [Sam Dumont's voice-skill work](https://www.linkedin.com/in/samdumont/)
- LLM-ism catalog adapted from [blader/humanizer](https://github.com/blader/humanizer) (MIT) and [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)
- Vocabulary-fingerprint methodology draws on classical stylometry (function-word frequency, type-token ratio, lexical attribution)
- Audit framework (4-bucket drift report) from McFarland's voice plugin methodology
- Four-layer framing (mechanics + cognitive moves + rhetorical structure + vocabulary) — own synthesis, bridging Dumont's pure-mechanics approach and McFarland's pure-persona approach. The rhetorical-structure layer was added after profiling Paul Graham and noticing that mechanics + vocabulary + cognitive moves captured the sentences but missed the macro shape that makes a PG essay a PG essay.

## Updating

Compare the `version` field in your installed `SKILL.md` frontmatter against the repo's latest:

```bash
cd /path/to/ghost-writer-repo && git pull

# Core skill + router targets (functions/ are required by the router)
cp SKILL.md /your/project/.claude/skills/ghostwriter/SKILL.md
cp functions/*.md /your/project/.claude/skills/ghostwriter/functions/

# Scripts (indexer + verifier)
cp scripts/*.py /your/project/.claude/skills/ghostwriter/scripts/

# References (check for new files)
cp references/*.md /your/project/.claude/skills/ghostwriter/references/

# Profiles (human/profile.md gets updated; your custom profiles are untouched)
mkdir -p /your/project/.claude/skills/ghostwriter/profiles/human
cp profiles/human/profile.md /your/project/.claude/skills/ghostwriter/profiles/human/
```

## License

MIT
