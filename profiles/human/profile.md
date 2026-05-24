# Style Profile: human (built-in default)

Source corpus: no specific writer. This is the **negative profile** — it defines human writing by the absence of LLM-tells rather than the presence of any one person's fingerprint.

Profile created: built-in. Last audit: —.

## What this profile is

Most profiles in this skill answer the question *"how does this specific person write?"* by pinning down density-based rules from a corpus.

This one answers a different question: *"how do humans write, in general, when nothing AI-shaped is leaking through?"* The answer is mostly: with variety. The reason LLM prose is identifiable isn't that it uses bad words — it's that it uses *the same words and shapes too consistently*. Human prose is bursty, uneven, sometimes weird, and never settles into the LLM-default rhythm of balanced paragraphs and confident transitions.

So this profile is dominated by what to *avoid* (Section 1) and what *not* to be consistent about (Sections 3 and 5). The positive rules are deliberately thin — there's no fingerprint to reproduce, just a clearing where one could exist.

Use this profile when:

- The user asks to "humanize" text — the input is AI-sounding prose, and they want it rewritten to read human.
- The user wants generic-but-human writing and hasn't profiled a specific person yet.
- A specific person's profile is too thin to use confidently — fall back to `human` and ask for more samples.

Don't use this profile when the user has a specific person in mind. Use their profile instead.

## 1. Banned words & phrases (full LLM-ism catalog)

This is the longest section because it's the most important. Position matters: ban-list rules encountered early in the profile have the strongest influence on generation. Every item below maps to a pattern in `references/llm-isms.md` — read that file for cues, examples, and fixes.

### Banned content moves (catalog patterns 1–6)

- **No significance inflation.** Don't open with "marking a pivotal moment in…" or "a transformative milestone in…" State the fact.
- **No notability name-dropping.** Don't list prestige outlets (NYT, BBC, FT…) without specifics. Cite one source with a year, or drop it.
- **No superficial -ing analyses.** Chains like "symbolizing… reflecting… showcasing… underscoring…" are banned. Replace with a concrete claim.
- **No promotional language.** "Nestled in the breathtaking…", "a vibrant hub of…", "captivating", "compelling".
- **No vague attributions.** "Experts believe", "industry observers", "some say". Name a specific source.
- **No formulaic challenges trope.** "Despite challenges… continues to thrive."

### Banned vocabulary (catalog pattern 7 — the long list)

These words are statistically overrepresented in LLM-generated prose. Most have a plainer alternative.

- *actually, additionally, moreover, furthermore, however* (overused as transitions)
- *testament, landscape, showcasing, leverage, robust, seamless, holistic, comprehensive, intricate*
- *vital, crucial, significant, profound, pivotal, transformative, groundbreaking, cutting-edge, state-of-the-art, ever-evolving*
- *navigate, delve, unlock, foster, bolster, underscore, illuminate, illustrate, exemplify*
- *amplify, champion, craft (as "craft a solution"), elevate, embark, empower, harness, pioneer, resonate, spearhead, supercharge, transcend, unleash, unveil, utilize* (just say "use")
- *meticulous, multifaceted, nuanced, paramount, remarkable, revolutionary, unparalleled, vibrant, impactful, actionable, bespoke, captivating, insightful*

If you reach for one of these, stop and pick a plainer word. "Use" not "utilize". "Help" not "empower". "Is" not "serves as". "Show" not "showcase".

### Banned constructions (catalog patterns 8–13)

- **No copula avoidance.** "Serves as a / functions as a / stands as a / acts as a / features / boasts" → use *is* and *has*.
- **No negative parallelisms / tailing negations.** "It's not just X, it's Y." "…, no guessing required." State the point directly.
- **No rule-of-three lists.** Three parallel items with matching shape and length ("innovation, inspiration, and insights") is the most reliable LLM tell. Use the natural number of items — usually two or four. If three is genuinely right, break the parallelism (different lengths, different forms).
- **No synonym cycling.** *The protagonist… the main character… the central figure… the hero…* Pick one term and repeat it. Repetition is fine; cycling reads as a thesaurus exercise.
- **No false ranges.** "Topics range from the Big Bang to dark matter." "From beginners to experts." List the items directly.
- **No subjectless passive fragments.** "No configuration needed." "Tests run automatically." Name the actor when it helps clarity.

### Banned style patterns (catalog patterns 14–23)

- **Em-dashes: max ~3 per 1000 words, and never the literal `--`.** The em-dash is the single most identifiable formatting tell of LLM text because LLMs use it as a universal clarification tool. Replace with colons for explanation, parentheses for asides, periods for new thoughts. The double-hyphen `--` is a rendering tell on top of the density problem — never produce it under any profile. If a profiled writer genuinely uses em-dashes, render the real character `—` at their documented (low) rate; the default here is to avoid them.
- **No boldface for key terms.** Don't bold concepts in every paragraph. Bold sparingly or not at all.
- **No inline-header lists.** "**Performance:** Performance improved by 40%" — convert to prose or use a real header.
- **Headings in sentence case, not Title Case.** "Strategic negotiations and partnerships", not "Strategic Negotiations And Partnerships".
- **No emojis as section markers.** "🚀 Launch phase. 💡 Key insight." Remove.
- **Match the source's quote style.** Don't auto-insert curly quotes if the writer uses straight quotes.
- **No stacked compound modifiers.** "Cross-functional, data-driven, client-facing, mission-critical, end-to-end." Drop the hyphens or rephrase.
- **No persuasive authority tropes.** "At its core, what matters is…" "The truth is, …" "Make no mistake — …" State the point.
- **No signposting announcements.** "Let's dive in", "Here's what you need to know", "Buckle up". Start with the content.
- **No fragmented headers.** A header followed by a one-sentence stub that repeats the header word.

### Banned communication patterns (catalog patterns 24–26)

- **No chatbot artifacts.** "I hope this helps!" "Let me know if you'd like me to expand on any section!" Cut entirely.
- **No cutoff disclaimers.** "While specific details are limited based on available information…" "Based on data available up to my training cutoff…" Find sources or remove.
- **No sycophancy.** "Great question!" "You're absolutely right!" "What a thoughtful framing." Respond to the substance.

### Banned filler and hedging (catalog patterns 27–29)

- **No filler phrases.** "In order to" → "to". "Due to the fact that" → "because". "At this point in time" → "now". "It is important to note that" → cut.
- **No excessive hedging.** "Could potentially possibly…" "It might perhaps be the case that…" Pick one hedge or commit.
- **No generic conclusions.** "The future looks bright." "Exciting times lie ahead." "Only time will tell." End on a specific claim, a plan, a fact — or just stop.

## 2. Anti-performative rules

This profile has no fingerprint to mimic, so there's nothing to crank up by accident — but there's a related failure mode worth guarding against: *manufacturing* fingerprint where none exists. When humanizing AI text or generating fresh, the temptation is to dial in quirks ("let me add some !" or "let me throw in a sentence fragment.") to make it feel personal. Don't.

- One distinctive habit is fine. Three start to feel performative.
- Don't add casualisms ("lol", "fr", "tbh", emoji) unless the writing task demands them.
- Don't add hedges or "I think" framings just to sound less authoritative — humans are often direct.
- Don't add stutters, parentheticals, or asides to manufacture texture. Texture comes from variability of length and rhythm, not from sprinkled quirks.

## 3. Cognitive moves & frames (LLM defaults banned; commit to thinking)

The mechanical ban list (Section 1) handles the surface tells. But default-LLM reasoning has its own fingerprint at the layer above the words — the *moves* it reaches for when handling an idea. This profile bans those too, because a draft can pass every mechanical check and still read AI because the thinking underneath is committee-shaped.

See `references/cognitive-moves.md` for the methodology. The `human` profile inverts that file's logic: instead of capturing one writer's moves, it bans the default-LLM moves and points at the human-natural alternatives.

### Banned LLM cognitive defaults

- **No both-sides-ism.** "While X has its merits, Y also has its strengths." Don't perform balance. If you have a view, commit to it. If you don't, say what's still uncertain — but don't fake a survey.
- **No 5-angle topic survey.** Listing "five considerations" or "four perspectives" on a question without committing to one is the LLM signature of avoiding a position. Pick the angle that matters and go.
- **No reflexive synthesis.** Default-LLM ends sections with "ultimately, the answer depends on context." Often it doesn't depend; the writer just hasn't decided.
- **No round-the-houses framing.** "Before answering X, let's first consider Y, which leads us to Z." Start near the answer.
- **No "it depends" without follow-through.** If it depends, *say what it depends on*. "It depends" alone is a non-answer.
- **No false consensus framing.** "Most experts agree…", "It is widely accepted that…". If you can name the experts, name them. If you can't, drop the framing.
- **No neutral-framing of contested claims.** Saying "some argue X, others argue Y" about a question with a defensible answer is a way of avoiding the answer. Humans take positions.

### Encouraged human-natural moves

These are positive moves to reach for when generating. None are required (this is a general profile, not a fingerprint), but applying any of them moves the draft away from the LLM default.

- **Commit to a position when one is defensible.** Even if hedged, a real claim beats a balanced survey.
- **Concretize.** When the topic permits a specific example, use one. Name a product, a year, a number, a scenario. Abstract claims paired with concrete cases read human; abstract claims surveyed at the abstract level read AI.
- **Ask "compared to what?" reflexively.** When the topic involves a comparison, anchor it. "Faster" → "faster than X."
- **Refuse appeals to authority.** Don't write "experts say." Write the substance, or cite a specific person with a specific claim.
- **End with a specific thing.** Either a concrete action ("so: do X"), a real open question ("what I don't know is whether…"), or a one-sentence compression of the point. Avoid generic uplift ("the future is bright"), generic deferral ("only time will tell"), and generic synthesis ("ultimately, it's about balance").
- **Skip throat-clearing.** Don't recap the question before answering. Don't explain that you're about to explain. Start on the substance.

### Audience assumption default

Assume the reader is competent. Don't over-explain basics. Don't define terms a target reader knows. The LLM-default is to assume zero context and over-scaffold; humans assume context and let the reader catch up if needed.

## 4. Rhetorical structure (LLM defaults banned; let shape match content)

Default-LLM prose has recognizable macro shapes — survey-the-five-perspectives, balanced-X-then-Y, "in conclusion," fake counterintuitive opener, sub-headers every 200 words. This profile bans those. Without a specific writer's arc to imitate, the rule is *don't manufacture shape; let the content decide it*.

See `references/rhetorical-structure.md` for the methodology. The `human` profile inverts it the same way Section 1 and Section 3 do: ban the defaults, point at the natural alternatives.

### Banned LLM rhetorical patterns

- **No five-point listicle structure** unless the piece actually has five discrete points that need separating. Default-LLM defaults to numbered lists with parallel sub-headers; humans use them only when the content calls for them.
- **No "In conclusion," / "To summarize," closer.** End on the substance.
- **No manufactured paradox opener.** "X is not what you think" / "The secret to X is the opposite of what everyone says" are LLM-default attention grabs. Open with a paradox only if the paradox is real and earned.
- **No fake personal anecdote.** "Imagine you're at a coffee shop and…" Don't invent a scenario you don't have. If concretization helps, use a real-world named example.
- **No over-scaffolding with sub-headers.** Sub-headers every 200 words is a default-LLM pattern. Use sub-headers when the piece has genuinely distinct sections; otherwise let paragraphs do the work.
- **No domain-transfer name-dropping.** "Like a Stradivarius…" / "As in evolutionary biology…" only when the comparison genuinely earns its keep. LLM-default reaches for prestige analogies as decoration.
- **No coined-term cosplay.** Don't invent a name for a concept ("call this X") unless the name compresses a real insight. Coined-term-padding ("I'll call this 'flow blocking'") reads AI when there's no actual concept underneath.
- **No footnote cosplay.** Don't add footnotes that add nothing — citations to vague "research" or asides that could be in the main text. Footnotes are for genuine digressions, jokes, or specific citations.
- **No meta-commentary on the writing itself** unless it's the writer's actual habit. "This is the kind of thing essays are for" sounds knowing in PG; sounds cosplay in default LLM.

### Encouraged human-natural patterns

When generating without a specific writer's profile, let these defaults guide the macro shape:

- **Let the opening match the content.** If the piece argues a position, open with the position or its strongest motivating case. If it explains a mechanism, open with the question. If it tells a story, start in the story. Don't force a shape the content doesn't need.
- **Let the argument arc match the topic.** A how-to has steps. An analysis has claim → evidence → counterargument → resolution. An essay can wander. Pick the arc the content calls for, then commit to it.
- **Concretize with real examples.** Named companies, real years, actual numbers, specific people. Avoid generic "imagine a startup" or "consider a typical user" unless the abstraction is the point.
- **Match reference horizon to scope.** A piece about Q3 sales doesn't need to roam to Renaissance Florence. A piece about institutions might. Don't force breadth.
- **Use "I" when warranted, not as performance.** If the writing task has a first-person voice, use "I" naturally. Don't manufacture personal anecdote where none exists.
- **End where the argument ends.** Don't add a "looking ahead" paragraph that adds no information. Specific action, real open question, or compressed restatement — or just stop.
- **Aphorisms are earned, not added.** A compressed principle is welcome when it emerges from the argument. Don't drop one in to feel pithy.

## 5. Quantitative layer (human-typical density ranges)

These aren't targets to hit exactly. They're the rough envelope of human prose. Generated text that falls inside this envelope reads human; text that falls outside (especially on burstiness) reads AI.

| Metric | Human-typical range | LLM-default (avoid) |
|---|---|---|
| Avg sentence length | 12–22 words | 18–22 words (centered) |
| **Burstiness (σ of sentence length)** | **7–14 words** | **3–6 words** |
| Avg paragraph length | 1–8 sentences (highly variable) | 3–5 (uniform) |
| Type-token ratio (first 500w) | 0.45–0.65 | 0.60–0.75 (over-varied) |
| Em-dashes / 1000w | 0–3 | 5–15 |
| Semicolons / 1000w | 0–4 | 0–2 (LLMs underuse) |
| Contraction rate | 60–90% (casual); 20–50% (formal) | 30–60% (regardless of register) |
| Hedge-word rate / 1000w | 0–8 (varies wildly) | 4–10 (uniform) |
| Exclamation rate / 1000w | 0–5 (casual); ~0 (formal) | 0–2 (regardless) |
| Rule-of-three lists per 1000w | 0–1 | 3–8 |

**The single most important number here is burstiness.** Aim for σ ≥ 7. Mix one short sentence (5–8 words) into every 4–6 long ones (20+ words). If every sentence in a paragraph lands within ±5 words of the average, the paragraph reads AI even if every other rule is satisfied. This is the variation-is-the-rule principle, and it's the hardest one to fake by accident.

## 6. Vocabulary fingerprint (defaults, not a specific writer's picks)

Because `human` is the negative profile, this section can't list a specific writer's lexical choices — there's no corpus. What it can do is structure the same dimensions as a person profile (see `references/vocabulary-fingerprint.md`) and bake in the human-default-vs-LLM-default contrast. When a specific writer is profiled, swap their actual picks in for these defaults.

### 6.1 Top content lexicon

N/A for the negative profile. Use the lexicon the topic calls for. The only rule: **repeat words rather than cycling synonyms**. If "protagonist" is the clearest word, use it four times in a paragraph. Don't reach for "central figure", "main character", "hero" — synonym cycling is a top-3 LLM tell (catalog pattern 11).

### 6.2 Function-word patterns

N/A specifically, but a general rule: don't manufacture distinctive pronoun ratios. If the writing task naturally uses "I", use "I". If it's third-person, stay third-person. The LLM-default tic is sliding into "we" framings ("we can see that…") even when no first-person was warranted; avoid.

### 6.3 Verb preferences

**Default: plain over elevated.** Reach for the plain verb first.

- *Use* (not utilize)
- *Make* (not create / produce / craft — unless the meaning genuinely requires the elevated form)
- *Do* (not execute / perform / carry out)
- *Have* (not possess / contain — same caveat)
- *Get* (not obtain / acquire — in casual register)
- *Go* (not proceed / depart)
- *Take* (not accept / receive — when the meaning matches)
- *Give* (not contribute / deliver / provide — except when the meaning requires)
- *Show* (not demonstrate / illustrate — for casual register)
- *Find* (not locate / identify / discover — when the meaning matches)
- *Say* (not state / articulate / express)
- *Help* (not assist / facilitate / support)
- *Try* (not attempt / endeavor)
- *Know* (not be aware of / be cognizant of)
- *Ask* (not inquire / request)
- *Think* (not consider / contemplate / believe)
- *Look at* (not examine / observe / scrutinize)

Use the elevated form only when the meaning genuinely requires it ("perform" in surgery context, not "do"; "demonstrate" when a proof is involved, not "show"). The LLM-default is to reach for elevated forms regardless of fit; the human-default is the opposite.

### 6.4 Hedge vocabulary

**Prefer:** *maybe, probably, I think, I'd say, sort of, kind of, kinda, honestly, to be fair, I guess, my guess is, might, could*

**Avoid (LLM-default hedges):** *perhaps, potentially, arguably, conceivably, ostensibly, putatively, presumably*

If the writing context is formal, use *might, may, could,* or commit (no hedge) — but still avoid the LLM-default hedge family above.

Pick *one* hedge per uncertain claim. Stacked hedges ("could potentially perhaps be the case that…") are catalog pattern 28 — banned.

### 6.5 Intensifier vocabulary

**Prefer:** *really, very, super, totally, a lot, pretty (= moderately), too, a bit, a little*

**Avoid (LLM-default intensifiers):** *quite, exceedingly, exceptionally, considerably, immensely, profoundly, tremendously, remarkably, extraordinarily*

Best move: replace intensifier + adjective with a more precise word. "Really fast" → "fast". "Very wrong" → "wrong". The LLM-default is intensifier-padding; humans cut the intensifier when the adjective carries the meaning.

### 6.6 Synonym binaries (human-defaults)

The diagnostic table for the negative profile — when there's a plain/elevated binary, default to plain.

| Pair | Human default | Note |
|---|---|---|
| use / utilize | **use** | "Utilize" is one of the top LLM tells. Almost never pick it. |
| help / assist | **help** | "Assist" reads corporate. |
| make / create / produce / craft | **make** | "Craft" is heavily AI-flagged. |
| show / demonstrate | **show** | "Demonstrate" only when proof/argument requires it. |
| find / discover / identify | **find** | "Discover" only when the discovery is the point. |
| but (sentence-initial) / however | **but** | "However" is acceptable mid-sentence; avoid as sentence opener. |
| also / additionally / furthermore | **also** | "Furthermore" and "additionally" are LLM-default transitions. |
| about / regarding / concerning | **about** | |
| because / due to the fact that / owing to | **because** | "Due to the fact that" is catalog pattern 27 — banned. |
| to / in order to | **to** | "In order to" is catalog pattern 27 — banned. |
| now / at this point in time | **now** | |
| weird / strange / unusual | **weird** | (in casual register; "unusual" is fine in formal) |
| big / large / sizable / substantial | **big** | (in casual register) |
| guess / assume / presume | **guess** | "Assume" is fine when precise; avoid "presume". |
| OK / okay | **OK** | (consistency matters; pick one and stick) |
| anyway / regardless / nevertheless | **anyway** | (in casual register) |

These are *defaults to pick* when the corresponding person-profile doesn't have a different documented pick. When you're using a person's profile, override with their observed pick from their Section 5.6.

### 6.7 Casualism / internet markers

**Register-dependent — match the writing context, don't add by default.** If the task is a casual blog post or a chat message, casualisms are fine at low density. If the task is anything formal, zero casualisms.

The LLM-default failure mode here is *adding* casualisms ("lol", emoji, "fr") to *manufacture* human-ness. Don't. Real humans use casualisms naturally in casual contexts; layering them onto formal contexts reads as caricature.

### 6.8 Profanity

**Default: none.** Don't add profanity that wasn't requested. If the task specifies profanity (an explicit content rewrite, a profile that documents it), apply at the documented rate; otherwise, zero.

### 6.9 Sentence-final vocabulary

**No fixed shape — vary.** A common LLM-default sentence ending is the generic uplift ("…the future is bright.", "…exciting times ahead.", "…only time will tell."). Avoid. End on a concrete noun, a specific number, a hedge that earns its place, or a one-word punchline.

### 6.10 Topic-shift vocabulary

**Default: no transition word; just start the new paragraph.** Or use a plain "But" / "So" / "OK so" / "Anyway" / "Now" if the topic shift is sharp enough to need signposting.

**Banned:** "Moreover", "furthermore", "additionally", "in addition", "subsequently", "consequently", "in conclusion" — these are LLM-default paragraph transitions and are catalog pattern 23 / 27.

### 6.11 Question vocabulary

**Default: direct.** "Why does this happen?" "What if X?" "Is that right?"

**Avoid:** "One might wonder if…", "It begs the question whether…", "We may ask ourselves…" — LLM-default question framings, all catalog pattern 21 (persuasive authority tropes).

### 6.12 Banned-by-omission (lexical)

Cross-reference Section 1 of this profile. The lexical-level highlights:

- *Utilize, leverage, robust, holistic, seamless, comprehensive, intricate, paramount, vital, crucial, transformative, pivotal, groundbreaking, cutting-edge, ever-evolving, navigate (metaphorical), delve, foster, unlock, harness, underscore, illuminate, showcase, craft.* The full list is in Section 1; this is a vocabulary-section reminder.

### Pet phrases (multi-word recurring units)

**None.** The human profile has no fingerprint, so no pet phrases. The temptation when humanizing is to manufacture catchphrases ("Look,", "Here's the thing,", "Real talk,") to make it feel personal. Don't — caught by Section 2 (anti-performative rules).

## 7. Sentence structure & rhythm

- **Vary sentence length within every paragraph.** This is the single biggest tell. LLMs default to uniformity; humans don't.
- **Fragments are allowed.** "Worth it." "Not great." "Maybe." Use sparingly; one or two per ~10 sentences is plenty.
- **Mix clause-joining moves.** Don't lean on em-dashes (banned anyway). Use commas, periods, semicolons (if the register permits), and conjunctions.
- **One short sentence near the end of a paragraph often works.** It lands the point. LLMs rarely do this.
- **Don't pad with transitional sentences.** "With that said,", "That being said,", "On the other hand," — usually droppable.

## 8. Quirks & idiosyncrasies (intentionally minimal)

There are none in this profile, by design. If you find yourself wanting to add a quirk to make the output feel less neutral, resist. The right move is to pull from the corpus of an actual person — switch profiles.

## 9. Negative rules (the strict list)

Everything in Section 1 is also a negative rule. The 29 patterns from `references/llm-isms.md` are banned by default in this profile. Run a self-check against the full catalog before delivering any text.

Additional negatives:

- **No throat-clearing openers.** Don't start a piece with "Let me start by saying", "I'll begin with", "Before I get into it". Start with the content.
- **No uniform paragraph lengths.** If three paragraphs in a row are within ±20% of the same word count, the piece reads AI. Vary the shape.
- **No "delve" or its synonyms** ("dive into", "explore in depth", "unpack"). Just do the thing.

## 10. Default mode

**Informational** — direct, factual, no narrative arc by default. The user can override per task ("write this as a story", "write this for a blog post with a hook"), but in the absence of direction, default to informational and short.

## 11. Format-specific modes (general guidance)

Because this profile isn't tied to a specific writer, the format guidance is generic. The user should override if they have specific format conventions in mind.

- **Long-form / blog:** narrative arc allowed when the user asks for it; 1–6 sentence paragraphs; vary opener sentence length per paragraph.
- **Email:** brief greeting only if external; one-line context; one paragraph of substance; clear ask or close. No "I hope this finds you well".
- **Slack / chat:** short messages; lowercase sentence starts allowed; no closing; full thoughts in 1–2 sentences max.
- **Documentation / technical:** instruction-oriented; numbered steps when steps are sequential; code in code blocks; no "as a developer, you'll appreciate".

## 12. Voice in action (humanize example)

The clearest demonstration of this profile is a before/after pair. The "before" is dense LLM-default prose; the "after" is the same content rewritten through this profile.

**Before (AI-default):**
> AI-assisted coding serves as a transformative tool in modern software development, marking a pivotal moment in how engineers approach their craft. In today's rapidly evolving technological landscape, these groundbreaking tools — nestled at the intersection of research and practice — are reshaping workflows, fostering collaboration, and empowering developers to deliver more impactful results. It's not just autocomplete; it's a paradigm shift. While challenges remain, the future looks bright.

**After (this profile applied):**
> AI coding assistants speed up the boring parts. They're good at boilerplate — config files, the glue code you don't want to write — and decent at sketching a test. You still have to read the test. The risk is how confident the suggestions look. I've taken code that passed lint and discovered later it missed the point, because I stopped paying attention. The only real backstop is tests. Without them, you're judging vibes.

Differences worth noting: no banned vocabulary, em-dash density dropped from ~5/100w to ~0.3/100w (one in the new version, in a place that earns it), no rule-of-three lists, no "it's not just X, it's Y", no generic conclusion. Sentence length varies (5 / 19 / 6 / 25 / 11 / 9 / 14). Burstiness σ ≈ 7 in the after, ≈ 4 in the before. The before reads AI; the after reads written.

## 13. Confidence notes

This is a baseline, not a fingerprint. It will produce text that reads human but doesn't read like any specific human. That's the design — when the user wants a specific person, they should profile that person and use *their* profile.

If output from this profile feels too neutral or generic for the task, the right fix is more context (audience, register, format) rather than adding manufactured quirks. The skill of using this profile well is in trusting variability and avoiding LLM-isms, not in adding flavor.

## Changelog

- Built-in. Created as part of the ghostwriter skill default set, adapted from the methodology of [blader/humanizer](https://github.com/blader/humanizer) (MIT).
