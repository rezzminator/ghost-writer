# LLM-ism Catalog (29 patterns)

A reference list of patterns commonly found in LLM-generated text. Use this catalog in three places:

- **Mode A (Extract):** if the sample shows several of these patterns clustered, ask the user whether the sample is fully theirs before encoding any of them as voice. Encoding LLM-isms as personal style is the single worst failure mode for this skill.
- **Mode A.5 (Calibrate):** the `LLM_ISM` tag means "this calibration sample contains a pattern from this catalog." Use this list to translate the user's tags into specific things to remove.
- **Mode B (Generate):** before delivering generated text, scan it against this list. Each match is a candidate for revision unless the source sample demonstrably uses the pattern at a known density (in which case match the density, don't crank).

Source: adapted from [blader/humanizer](https://github.com/blader/humanizer) (MIT) and [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing).

The patterns are grouped by surface area. Each one has a short cue ("looks like…") so you can scan-detect during a self-review pass.

## Content patterns

1. **Significance inflation.** "Marking a pivotal moment in…", "a transformative milestone in the evolution of…". Cue: importance language attached to ordinary facts. Fix: state the fact plainly.
2. **Notability name-dropping.** "Cited in NYT, BBC, FT, and The Hindu." Cue: a list of prestige outlets without specifics. Fix: cite one source with a year or quote, or drop it.
3. **Superficial -ing analyses.** "Symbolizing… reflecting… showcasing… underscoring…" Cue: chained -ing verbs that gesture at meaning without delivering it. Fix: replace with a concrete claim or remove.
4. **Promotional language.** "Nestled in the breathtaking region…", "a vibrant hub of…". Cue: travel-brochure adjectives. Fix: neutral description.
5. **Vague attributions.** "Experts believe…", "Industry observers have noted…", "Some say…". Cue: collective unnamed authorities. Fix: name a specific source or drop the claim.
6. **Formulaic challenges trope.** "Despite challenges… continues to thrive." Cue: the obstacle-then-overcoming arc applied generically. Fix: name the specific challenges and what specifically happened.

## Language patterns

7. **AI vocabulary.** Words that recur in default-LLM prose far more than in human prose: _actually, additionally, moreover, furthermore, testament, landscape, showcasing, leverage, robust, seamless, holistic, comprehensive, intricate, vital, crucial, significant, profound, pivotal, transformative, groundbreaking, cutting-edge, state-of-the-art, ever-evolving, navigate, delve, unlock, foster, bolster, underscore, illuminate, illustrate, exemplify_. Cue: any of these in a position where a plainer word would do. Fix: substitute the plainer word, or restructure.
8. **Copula avoidance.** "Serves as a… functions as a… stands as a… acts as a… features… boasts…" Cue: dressed-up substitutes for _is_ and _has_. Fix: use _is_ and _has_.
9. **Negative parallelisms / tailing negations.** "It's not just X, it's Y." "…, no guessing required." Cue: setting up a denial only to reverse it. Fix: state the point directly.
10. **Rule of three.** "Innovation, inspiration, and insights." "Faster, better, stronger." Cue: three parallel items with similar shape and length, especially with alliteration or rhythm. Fix: use the natural number of items the content actually requires (often two or four).
11. **Synonym cycling.** Across one passage: _the protagonist… the main character… the central figure… the hero…_ Cue: a single referent named four different ways to avoid repetition. Fix: pick one term and repeat it. Repetition is fine.
12. **False ranges.** "Topics range from the Big Bang to dark matter." "From beginners to experts." Cue: framing a list as a spectrum to suggest comprehensiveness. Fix: list the topics directly without the range scaffolding.
13. **Passive voice / subjectless fragments.** "No configuration needed." "Tests run automatically." Cue: actor erased. Fix: name the actor when it helps clarity. Passive is fine when the actor is obvious or irrelevant.

## Style patterns

14. **Em-dash overuse.** "Institutions — not the people — yet this continues — and so on." Cue: more than ~3 em-dashes per 1000 words, or multiple per paragraph. Fix: prefer commas, periods, or colons. Note: many human writers use em-dashes; match the density of the source sample, not the LLM default — and remember a documented rate is a *ceiling*. A profile that lists em-dash at 1.0/1000w means a 500-word piece should usually have **zero**. **The literal `--` double-hyphen is a rendering tell on top of the density problem and is NEVER acceptable for any profile.** If a writer genuinely uses em-dashes, render the real character `—` at the documented rate; never `--`. This is the single most reported leak — the em-dash slips back in even when the profile says the writer barely uses them.
15. **Boldface overuse.** Bolding key terms in every paragraph. Cue: bold used as a substitute for clear writing. Fix: bold sparingly or not at all.
16. **Inline-header lists.** "**Performance:** Performance improved by 40%. **Reliability:** Reliability is up." Cue: every bullet starts with a bolded term followed by a colon. Fix: convert to flowing prose, or use a real header.
17. **Title Case Headings.** "Strategic Negotiations And Partnerships." Cue: every word capitalized in headings of body prose. Fix: sentence case is more common in human writing — "Strategic negotiations and partnerships."
18. **Emojis.** "🚀 Launch phase. 💡 Key insight." Cue: emoji as section markers or bullet decorations. Fix: remove unless the source sample uses them at a known rate.
19. **Curly quotes vs straight quotes.** Cue: curly (typographic) quotes inserted automatically. Fix: match what the sample actually uses; many casual writers use straight quotes consistently.
20. **Hyphenated compound modifiers.** "Cross-functional, data-driven, client-facing, mission-critical, end-to-end." Cue: stacked corporate-speak compounds. Fix: drop hyphens on common pairs or rephrase.
21. **Persuasive authority tropes.** "At its core, what matters is…" "The truth is, …" "Make no mistake — …" Cue: rhetorical scaffolding that announces a forthcoming truth. Fix: state the point directly.
22. **Signposting announcements.** "Let's dive in." "Here's what you need to know." "Buckle up." Cue: the writer narrating that they're about to write. Fix: start with the content.
23. **Fragmented headers.** A header followed by one short sentence repeating the header word. ("## Performance" → "Speed matters.") Cue: header + tiny stub. Fix: let the header carry the meaning, or remove the header.

## Communication patterns (chat residue)

24. **Chatbot artifacts.** "I hope this helps!" "Let me know if you'd like me to expand on any section." Cue: assistant-to-user closers in non-chat output. Fix: remove entirely.
25. **Cutoff / source disclaimers.** "While specific details are limited based on available information…" "Based on data available up to my training cutoff…" Cue: the model hedging about its own knowledge inside a piece of writing. Fix: find sources or remove.
26. **Sycophantic tone.** "Great question!" "You're absolutely right!" "What a thoughtful framing." Cue: praise of the prompt. Fix: respond directly.

## Filler and hedging

27. **Filler phrases.** "In order to" → "to". "Due to the fact that" → "because". "At this point in time" → "now". "It is important to note that" → drop entirely. Cue: multi-word phrases that compress to a single common word. Fix: compress.
28. **Excessive hedging.** "Could potentially possibly…" "It might perhaps be the case that…" "May arguably suggest…" Cue: stacked hedges where one would do. Fix: pick one hedge or commit to the claim.
29. **Generic conclusions.** "The future looks bright." "Exciting times lie ahead." "Only time will tell." Cue: closer that adds no information. Fix: end with a specific claim, plan, or fact — or just stop.

## How to use this catalog during generation

Before delivering generated text, run a self-check:

1. Skim for any of the 29 patterns by their cues.
2. For each match, check the source sample: does the writer demonstrably use this pattern at a measurable density?
3. If yes → match the density, don't exceed it.
4. If no → revise. The pattern is yours leaking through, not theirs.

Most LLM-isms can survive in tiny doses without being noticeable. The damage comes from clustering: three or four patterns from this catalog in the same paragraph is the texture readers identify as "AI-written."
