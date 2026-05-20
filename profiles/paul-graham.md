# Style Profile: Paul Graham (multi-format)

Source corpus: **~1.31M words across 3 written formats.**
- **PRIMARY — essays:** ~570,700 words, 231 essays from paulgraham.com (~2001–2024). The core voice. Canonical index: `profiles/paul-graham.index.json`.
- **SECONDARY — HN comments:** ~339,000 words, ~9,980 comments by `pg` on Hacker News (2006–2024), cleaned of `Source:`/timestamp/URL boilerplate. The comment register. Index: `profiles/paul-graham.hn.index.json` (raw) + cleaned re-index.
- **SECONDARY — tweets:** ~560 words, 15 verified public tweets (2020–2025). Short-form. **Tiny — directional only.** Index: `profiles/paul-graham.x.index.json` (raw).
- **CROSS-CHECK ONLY (not in voice stats):** interviews + talks (transcribed speech, contaminated by interviewer edits and page chrome); *On Lisp* / *ANSI Common Lisp* (PG's writing but technical-reference register — characterized as a distinct mode in §11, stats not folded in).
- **SKIPPED:** technical/arc (code), context/, mail/ (near-empty).

Profile created: 2026-05-20. Last audit: —.

**The headline of this profile is VOICE vs PLATFORM with teeth.** The old profile was single-format (essays only) and had to *guess* which patterns travel. With essays + HN comments + tweets, the call is now evidenced: a pattern present in essays AND HN (AND tweets where the sample allows) is **cross-format VOICE**; a pattern only in essays is **essay-PLATFORM**. Tags below:

- **[VOICE · XF]** — confirmed across formats. Travels. Use everywhere.
- **[VOICE · essay]** — clearly personal but only the essay corpus evidences it at scale (cognitive moves, coining). Likely travels; evidence is essay-bound.
- **[PLATFORM · essay]** — a convention of the published essay. Do NOT port to short-form.
- **[PLATFORM · HN]** — a convention of the comment register. Do NOT port to essays.

---

## 1. Banned words & phrases (never-say list)

First because earlier constraints bind generation hardest. Confirmed by counts across **both** the 570.7k-word essay corpus and the 339k-word HN corpus, not assumed.

- **Banned words (0 / near-0 in BOTH corpora, all LLM-tells):** "delve" (0/0), "utilize" (0/1), "seamless", "navigate"/"navigating" (figurative), "robust" (literal only), "leverage" as a verb (noun-only in corpus), "foster", "bolster", "underscore", "showcase", "holistic", "comprehensive", "intricate", "vibrant", "testament", "tapestry", "realm", "landscape" (figurative). The writer reaches for the plain word every time, in every format.
- **Elevated synonyms the writer never picks (see §6.6 — confirmed cross-format):** "obtain" (essays 3, HN 2), "commence" (1/0), "purchase" (rare/rare), "regarding"/"concerning" (1/1), "due to" as a connector (0/0 — always "because"), "however" present but swamped by "but" (essays 51:1, HN 65:1), "moreover"/"furthermore"/"additionally" (essays 11, HN 2 against "also" 633/427). Inheriting the human ban here is correct.
- **Banned constructions:** rule-of-three parallel lists; "It's not just X, it's Y" tailing-negation reversals; "in today's fast-paced world" / significance-inflation openers; chatbot closers ("I hope this helps", "let me know if…"); "great question" sycophancy; emoji section markers; Title Case Headings; bold-term-colon inline lists.
- **Rendering tell, never allowed:** the literal `--` double-hyphen. Render the real em-dash `—` only — and even that is **essay-rate** (§5); on HN/tweets PG essentially doesn't dash at all (see §1 note + §5).

Source: explicit absences computed by the indexer over both corpora + LLM-ism patterns from `llm-isms.md` confirmed absent.

**Note — words that LOOK like LLM-isms but are genuine PG voice (do NOT ban), now cross-format-confirmed:** "actually" (essays 297, HN 550 — even denser on HN, where it opens corrections), "merely" (essays 240), "simply" (essays 200, HN 163), "incidentally" (essays 33, HN 135 — an aside-marker, denser on HN), "in fact"/"fact" (435/346). Allowed at corpus density.

**Note — em-dash is essay-PLATFORM, not voice.** `—` runs ~0.99/1000w in essays but **~0/1000w in cleaned HN comments and 0 in the tweets.** Don't reach for it in short-form even though the essays have it.

## 2. Anti-performative rules

The failure mode for PG is cranking his quotable tics into caricature. Guards:

- He coins terms (§4.7) at a *measured* rate — roughly one per essay, sometimes none, and **almost never in comments or tweets.** Don't manufacture a coinage in every paragraph. A piece with zero coined terms is on-distribution.
- He opens essays with a flat declarative thesis far more than with paradox (§4.1). Don't open every piece with "The way to X is not to Y." It's one move among several.
- He starts sentences with "But", "And", "So" often, in every format (§5) — but they're load-bearing, not decorative. Use them where the logic actually turns.
- Footnotes and the "Thanks to… for reading drafts" footer are **essay-format only** (§4.12, §11). Never attach them to short-form.
- Match the *format's* density, not the global one. Em-dashes ~1/1000w in essays → a 600-word essay gets **zero or one**; a comment or tweet gets **zero**. Contractions and hedging are *higher* on HN than in essays — match the target register, don't average.

## 3. Cognitive moves & frames

The repeatable operations PG performs on an idea before assembling words. Each rule has quoted instances and a move-type. These are **[VOICE · essay]** by default (the essays evidence them at scale); where the HN corpus independently confirms the same move I upgrade to **[VOICE · XF]** and give the comment-register instance — this is new in the multi-format profile.

### Framing moves
- **[VOICE · essay | high] Reframes the asked question into a better one before answering.** Type: reframe. Instances:
  - schlep.md: "Instead of asking 'what problem should I solve?' ask 'what problem do I wish someone else would solve for me?'"
  - getideas.md: opens by refusing the asked question — "why do people think it's hard to come up with ideas for startups?"
- **[VOICE · essay | high] Collapses a two-option framing by showing the options are the same thing / inverting one.** Type: reduce/invert. Instances:
  - inequality.md: "There are two ways to do it: give money to the poor, or take it away from the rich. But they amount to the same thing…"
  - love.md: takes "Do what you love" and immediately complicates it — "But it's not enough just to tell people that."

### Reasoning moves
- **[VOICE · XF | high] Argues from a single named case, never from authority or aggregate.** Type: counterexample / named-case. Instances:
  - schlep.md: "The most striking example I know of schlep blindness is Stripe, or rather Stripe's idea."
  - HN: "If Bill Gates subscribes, he alone adds about $33k to the average net worth of their 1.7 million print subscribers." (concedes a point, then grounds it in one named case + a number)
  - **Confirmed absence cross-format:** "experts say" / "studies show" / "it's widely accepted" appear ~0 times in 910k words. He reasons from mechanism and instance.
- **[VOICE · XF | high] States the mechanism (the "by [doing X]" / "because [causal chain]" move) rather than just asserting the effect.** Type: mechanism. Instances:
  - makersschedule.md: "A single meeting can blow a whole afternoon, by breaking it into two pieces each too small to do anything hard in."
  - HN: "They liked us simply because we were the leader in our market." / "it's specifically because they work like interrupts."
- **[VOICE · XF | medium] Tests a claim by tracking the actual incentive / who-benefits.** Type: incentives. Instances:
  - HN: "when people are interviewed by reporters they often say that something they want to happen is already happening." (explains a claim by the speaker's incentive, not its truth)
  - submarine.md / essays on PR generally: the move recurs as "the question is who's paying for this."

### Concretization tendencies
- **[VOICE · XF | high] Pairs almost every abstract claim, within a sentence or two, with a named concrete instance** — a company, person, dated moment, or number. Density: pervasive in essays; on HN it's a named startup/founder or a specific number. Instances:
  - schlep.md: "Your unconscious won't even let you see ideas that involve painful schleps" → Stripe; Olympic athletes.
  - HN: "I'm not sure because I can't remember which startups only had one founder when we funded them, but I know there are 2/36 in the current batch and there were 3/26 in the previous one." (refuses to assert, then gives exact ratios)

### Reflexive rejections (things PG demonstrably refuses)
- **[VOICE · XF | high] Refuses to assert past his evidence; flags the limit instead of overclaiming.** Two+ cases where he had the option and didn't:
  - schlep.md: "Maybe that's possible, but I haven't seen it."
  - HN: "I'm not sure because I can't remember…"; "I don't think I've ever heard of such growth." (the comment register's version of the same epistemic caution — "I don't think" is his single most common reply opener)
- **[VOICE · XF | high] Refuses appeals to authority / consensus** (cross-format absence, above).

### Shape of disagreement *(NEW — the essay corpus under-evidenced this; HN fills it)*
- **[VOICE · XF/HN | high] Disagrees by directly negating, then immediately supplying the counter-mechanism — not by hedging around it.** Type: direct-counter. Instances:
  - HN: "No, it's not a black mark. There's no particular reason not to apply now, if you're ready."
  - HN: "I don't think that would be good. You want to encourage people to participate in a site like this."
- **[VOICE · XF/HN | high] Softens a correction with "I wouldn't (quite) say…", then states what he'd say instead.** Instances:
  - HN: "I wouldn't quite say we look for people who don't need us. Roughly speaking, we look for people who are like we were when we started Viaweb."
  - HN: "I wouldn't say they are consciously planting them. But when people are interviewed by reporters they often say…"
- **[VOICE · XF/HN | high] Concedes cleanly ("You're right." / "Good point.") then qualifies — never grudging, never doubling down.** Instances:
  - HN: "You're right. That's why I was careful to qualify it with 'all other things being equal.'"
  - HN: "You're right, but this doesn't necessarily prove it. It would depend where weighting happened."

### Shape of conclusion *(essay-scale — comments rarely "conclude")*
- **[VOICE · essay | high] Ends an essay on a compressed line — a derived imperative, a forward-looking aphorism, or an open question — never generic uplift.** Closing sentences:
  - good.md: "Don't just not be evil. Be good."
  - schlep.md: "It's too late now to be Stripe, but there's plenty still broken in the world, if you know how to see it."
  - want.md (open-question variant): "How do you reconcile being a machine made of matter with the feeling that you're free to choose what you do?"

### Audience assumptions
- **[VOICE · XF | medium] Assumes a maker/founder reader and shared startup-and-programming canon; drops "throwing an exception", "VCs", "ramen profitable" without full definition** (but usually defines the terms he himself coins). On HN this is sharper — he answers as a peer to other builders, no scaffolding. Evidence: makersschedule.md "having a meeting is like throwing an exception"; HN replies that assume the reader knows what a batch/demo day/C-corp is.

### Argument shape
- **[VOICE · essay | high] problem → reframe/name → mechanism → named examples → derived advice.** Type: stair-step/empirical hybrid. (Essay-scale; comments compress it to claim → mechanism → one example.) Instances:
  - schlep.md: ideas-go-unexploited (problem) → "a phenomenon I call schlep blindness" (name) → unconscious avoidance (mechanism) → Stripe (example) → "ask what problem do I wish someone else would solve for me" (advice).
  - makersschedule.md: programmers hate meetings (problem) → "the manager's schedule and the maker's schedule" (distinction) → meetings break the maker's day (mechanism) → office hours, his 3am schedule (examples) → "all we ask… is that they understand the cost" (advice).

## 4. Rhetorical structure & essay arc

All of §4 is **[PLATFORM · essay]** — these are essay-scale shapes that do NOT appear in comments or tweets (which have their own shapes; see §11). VOICE-grade *within* essays.

### 4.1 Opening shape *(essay)*
- **Dominant: direct thesis / flat declarative claim** — ~10 of 20 sampled openings, often "One of the most [important/common/surprising] things…".
- **Runner-up: question** — ~4 of 20. **Third: personal anecdote** — ~4 of 20. Occasional **epigraph quote** above the body.
- The thesis is frequently *counterintuitive*, but the literal paradox-opener ("The way to X is not to Y") is a minority, not the default.
- Instances: makersschedule.md "One reason programmers dislike meetings so much is that they're on a different type of schedule"; cities.md "Great cities attract ambitious people."; wealth.md "If you wanted to get rich, how would you do it?"; nerds.md "When we were in junior high school, my friend Rich and I made a map of the school lunch tables according to popularity."
- **Contrast (the multi-format point):** HN comments open with **"Yes,"/"No,"/"I don't think"/"Actually,"** not with a thesis (§11). The essay-opening repertoire is essay-PLATFORM.

### 4.2 Argument arc *(essay)*
- **Dominant: problem → reframe/name the distinction → mechanism → named examples → derived advice.**
- Alternates: anecdote → generalization → return (nerds.md, copy.md); question → exploration → tentative answer (wealth.md, want.md).
- Instances: schlep.md (traced in §3); good.md (motto anecdote → what "make something people want" really means → cases → "Don't just not be evil. Be good.").

### 4.3 Scale-shifts *(essay)*
- Rate per 1000w: **moderate-high** (~4–6; sampled, not machine-counted).
- Dominant direction: **balanced, cycling concrete→abstract→concrete.** Rarely stays at one altitude for long.
- Samples: makersschedule.md one broken afternoon (concrete) → "ambitious projects are by definition close to the limits of your capacity" (abstract) → office-hours program (concrete). HN comments, by contrast, mostly **stay at one scale** — the immediate concrete question.

### 4.4 Example-texture mix *(essay; ~40 examples sampled)*
- Named company / product ~25% (Stripe, YC, Apple, Microsoft, Google); Personal anecdote ~25%; Historical figure/event ~15% (Leonardo, Newton, Copernicus, Galileo); Domain transfer ~15% (meeting ↔ exception; programming ↔ painting); Hypothetical ~10%; Dated anchor ~7%; Numerical ~3%.
- Dominant: **named-company + personal-anecdote + domain-transfer.** The *breadth* is the fingerprint. On HN the mix collapses to **named-company + personal-YC-anecdote + number** (no Renaissance, no painting analogies) — see §11.

### 4.5 Reference horizon
- Essay: **"last week" to antiquity** in a single piece; **3–5 distinct domains** (programming, startups, economics, art, history, biology, physics). **[PLATFORM · essay]** — the wide horizon is an essay habit.
- HN: **narrow** — the thread's topic, recent YC batches, named startups. The roaming horizon does NOT appear in comments.

### 4.6 Self-reference pattern
- **[VOICE · XF, distribution shifts by format] "I" frequency:** essays 4,850 (≈8.5/1000w), "you" 9,613, "we" 2,332 — reader-addressed, **"you" ~2× "I"**. On HN the ratio **flips**: "I" 5,250 > "you" 3,931 — comments are first-person ("I think…", "I don't think…", "We made a conscious choice…"). The pronoun ratio is itself a format tell.
- Essay "I" distribution: confident assertion ~45%, anecdote ~30%, admitted uncertainty ~15%, procedural ~5%, opinion ~5%.
- HN "I" distribution skews to **uncertainty + assertion in reply** ("I don't think" 195, "I'm not sure" 75, "I don't know" 122 as trigrams).

### 4.7 Term-coining propensity *(essay)*
- **[PLATFORM · essay | high]** Coined terms per 10,000 words: **~0.5–1** in essays (high for an essayist; most writers ≈0); **~0 in comments/tweets** (which *reference* already-coined terms but don't mint new ones).
- Catalog (large — part of why he's recognizable): "schlep blindness", "maker's schedule"/"manager's schedule", "ramen profitable", "default alive"/"default dead", "the Blub paradox", "do things that don't scale", "make something people want", "frighteningly ambitious", "relentlessly resourceful", "the bus ticket theory of genius", "founder mode", "Web 2.0". Several became industry-standard — coining that *sticks* is the signature.
- Typical slot: **mid-paragraph near the opening, with an explicit naming move** — "a phenomenon I call schlep blindness"; "two types of schedule, which I'll call the manager's schedule and the maker's schedule." Often becomes the title.
- Generation note: coin only when an essay earns it, at ~1/essay. The move is "describe the mechanism, then give it a short memorable name" — usually adjective+noun ("schlep blindness", "founder mode") or a possessive ("maker's schedule"). Plain words doing new work; never manufactured jargon. **Don't coin in short-form.**

### 4.8 Meta-commentary on the writing itself
- **[VOICE · essay | low]** ~0.5/10kw in essays. Examples: makersschedule.md "perhaps there's a third option: to write something explaining the two types of schedule." Near-absent on HN.

### 4.9 Negation-as-thesis frequency *(essay)*
- ~188 sentences match "[Capitalized opener] … is not …"; negation-of-conventional is a **frequent thesis move**, the opener in a minority of pieces. Examples: "The way to find golden ages is not to go looking for them."; love.md "But it's not enough just to tell people that."

### 4.10 Definition-by-compression
- **[VOICE · XF | moderate]** "X is just/merely Y" surprising substitutions recur in essays ("Prestige is just fossilized inspiration."; "Plans are just another word for ideas on the shelf."; "A company is defined by the schleps it will undertake."). On HN the same move appears compressed ("Making fewer mistakes isn't the only solution. You can also make them cost less."). VOICE; the lexical engine ("just"/"merely"/"simply") travels.

### 4.11 Aphorism placement *(essay)*
- Dominant slot: **closing** (the compressed line is usually the last sentence), with frequent **mid-piece** landings as the payoff of a setup. good.md closing "Don't just not be evil. Be good."; schlep.md closing "there's plenty still broken in the world, if you know how to see it." On HN aphorisms land **first** (the comment leads with the point).

### 4.12 Footnote habit *(long-form only — PLATFORM · essay)*
- Density/1000w: **moderate-high in long essays** (greatwork, gap, wealth, superlinear carry many numbered notes; short essays few/none).
- Function: **digression / elaboration / counter-claim / occasional citation** — not just references.
- Tonal contrast: **same register to slightly drier**; multi-sentence asides in the same conversational voice.
- **Plus the acknowledgment footer:** ~159 of 231 essays end with "Thanks to [names] for reading drafts of this." A strong essay-format marker — but format-bound; **never on short-form.**

## 5. Quantitative layer (computed; transcribed verbatim)

Three columns where the data exists. **Essays = canonical** (`paul-graham.index.json`). HN = cleaned re-index (boilerplate stripped). Tweets = 15-tweet sample, **directional only**.

| Metric | Essays (PRIMARY) | HN comments | Tweets (n=15) |
|---|---|---|---|
| Words | 570,704 | ~339,070 (cleaned) | ~560 |
| Avg sentence length | **16.65w** | 14.94w (terser) | 14.46w |
| Burstiness (σ) | **10.07** (min 1, max 377) | 35.09 *(inflated by pasted list-outliers; typical comment short)* | 9.49 |
| Avg paragraph length | **3.23 sentences** | 2.04 | 2.15 |
| Type-token ratio (first 500w) | 0.46 | 0.534 | — (too small) |
| Em-dash `—` /1000w | **0.99** (raw 565) | **~0.01** (raw 5) | 0 |
| Literal `--` /1000w | 0.78 (raw 446 — export artifact; render `—`) | 0.47 | 0 |
| Semicolon /1000w | 1.59 | 1.68 | 0 |
| Colon /1000w | **4.88** | **5.06** | (4 raw) |
| Ellipsis /1000w | 0.06 | **0.60** (trailing-off) | 0 |
| Exclamation /1000w | 0.17 | 0.28 | 0 |
| Question /1000w | **3.48** | **4.22** | (2 raw) |
| Contraction /1000w | **28.23** | **34.28** (more casual) | 31.91 |
| Hedge /1000w | **4.19** | **5.88** (more hedging) | 5.32 |

- **Top sentence-initial connectors — essays:** "the" (2765), **"but" (2112)**, "and" (1604), "if" (1582), "i" (1383), "in" (1046), "it" (1007), **"so" (1003)**, "you" (920), "it's" (802).
- **Top sentence-initial connectors — HN:** **"i" (2225)**, "the" (1594), **"but" (833)**, "if" (801), "it" (762), "it's" (736), "we" (673), "this" (508), "you" (466), "and" (450), "so" (443).
- **Cross-format reads:** colon ~4.9–5.1/1000w in BOTH (VOICE). "But/And/So" sentence-openers in both (VOICE). Em-dash is **essay-only** (~0 on HN/tweets). HN is terser, more contracted, more hedged, more questioning, and uses **ellipses** where essays don't. The "so high" burstiness on HN is an artifact of a few pasted lists (e.g. a 5,090-"word" spam-domain dump) with no sentence punctuation — the median comment is 1–2 short sentences.

## 6. Vocabulary fingerprint

### 6.1 Distinctive lexicon (KEYNESS-ranked, not raw frequency)

Ranked by keyness (how much more PG uses a word than baseline English), split by hand into voice / topic / boilerplate. **Cross-format mark:** ⊕ = the word also scores distinctive in the HN keyness list (independent confirmation it's voice, not essay-topic).

- **Voice words — Tier 1 (clearest markers, travel across topics):** "merely" (28× keyness) · "till" (27.8×, archaic for "until") ⊕ · "tend"/"tends" (31×) · "seemed"/"seems" (32×) ⊕ · "whatever" (28×) · "simply" (23×) ⊕ · "already" (38.8×) ⊕ · "interesting" (28×) ⊕ · "since" (33.9×) ⊕ · "either" (25.5×) ⊕ · "trying" (38.5×) ⊕ · "thinking" (27.3×) ⊕ · "whether" (35.2×) ⊕ · "else" (32.7×) ⊕ · "later" (27.7×) ⊕ · "sometimes" (26.2×) · "worth" (25.8×) · "possible" (23.4×) · "powerful" (26×) · "valuable" (21.1×).
- **Voice words — Tier 2 (also distinctively PG, several HN-confirmed):** "actually" (raw 297 essays / 550 HN ⊕) · "exactly" ⊕ · "certainly" ⊕ · "meant" ⊕ · "real" · "smart" (29×) · "rich" (35×) · "obvious"/"obviously" (he treats the obvious as suspect — "it's far from obvious") · "care" (as in "few people care about…") · "imagine" · "matter" (as verb, "doesn't matter") · "incidentally" (aside-marker, denser on HN) · "pretty" (as in "pretty much" — higher on HN) ⊕ · "maybe" ⊕ · "kind of"/"sort of".
- **Topic words (high keyness but subject-bound — EXCLUDED from generation):** "startup"/"startups", "founders", "investors", "companies", "software", "lisp", "vcs", "hackers", "programming", "languages", "wealth", "essay", "web", "design", "yc"/"combinator", "valley"/"silicon", "spam", "users", "funding", "google", "microsoft". Do NOT drift generated text toward these subjects.
- **HN-platform words (drop — they're the medium, not PG):** "news", "comments"/"comment", "hn", "ycombinator", "site", "page", "post", "article", "karma", "batch", "demo", "apply"/"application", "reddit".
- **Dropped boilerplate/names:** "paulgraham", "jessica", "url"/"http"/"www" (URL-header noise).

### 6.2 Function-word patterns *(cross-format)*
- **"but" outranks "however" massively in both** — essays **51:1** (4829 vs 94), HN **65:1** (2748 vs 41). [VOICE · XF]
- Pronoun preference is **format-conditional** (§4.6): essays **you (9613) > I (4850) > we (2332)**; HN **I (5250) > you (3931)**. The flip is itself a tell — essays address "you", comments speak as "I".
- High "if" in both (essays 1582 sentence-initial; HN 801) — PG reasons in conditionals constantly. [VOICE · XF]

### 6.3 Verb preferences *(cross-format)*
- Top verbs (essays): have (4140), do (2648), get (1892), work (1856), make (1413), want (1380), think (1240), know (951), need (751), say (692), take (594), use (578), see (523), find (502), go (434), try (429), look (399), tell (398), give (327), keep (264). HN top verbs track the same set (have, do, ask, get, think, make, know, want, work, say…).
- Plain-to-elevated ratio: **~99% plain in both.** Essays: "use" 1184 vs "utilize" 0; "get" 2731 vs "obtain" 3; "make" 2634 vs "create/craft" 396; "show" 219 vs "demonstrate" 4. HN identical pattern.
- Identifying picks: **"get"** as the universal verb; **"make"** over "create". [VOICE · XF]

### 6.4 Hedge vocabulary *(cross-format — same stack, denser on HN)*
- Essays: **"probably" (563)**, "kind of" (362), "I think" (259), "sort of" (180), "seems to" (153), "likely" (152), "could be" (139), "might be" (132), "maybe" (131), "it seems" (112), "perhaps" (88).
- HN: **"probably" (509)**, "I think" (236), "sort of" (205), "kind of" (197), "seems to" (150), "maybe" (147), "likely" (122), "could be" (115).
- **"probably" is the signature hedge in BOTH** [VOICE · XF]. Prefer "maybe" over "perhaps" (essays 131 vs 88; HN 147 vs 44). Avoid Claude-default "potentially"/"arguably" (near-0 in both). Plus the HN-register reply-hedges **"I don't think" / "I'm not sure" / "I don't know"** (§3, §11).

### 6.5 Intensifier vocabulary *(cross-format)*
- Essays: **"so" (2920)**, "much" (1215), "too" (735), "very" (621), "really" (549), "rather" (251), "almost" (251), "especially" (204), "pretty" (160), "quite" (154).
- HN: **"so" (1624)**, "much" (764), "very" (461), "too" (392), "really" (370), **"pretty" (288 — higher rank than essays)**, "rather" (191), "almost" (136), "quite" (122).
- **"very" outranks "quite" ~4:1 in both** [VOICE · XF]. "pretty" ("pretty much", "pretty bad") is more prominent on HN — a casual-register lift. Avoid "extremely"/"incredibly"/"absolutely".

### 6.6 Synonym binaries (the diagnostic table — crystalline-plain in BOTH corpora)
Format: plain → ESSAYS (plain vs elevated) · HN (plain vs elevated). All resolve to plain. [VOICE · XF]
- use / utilize → **use** · essays 1184/0 · HN 850/0
- get / obtain → **get** · essays 2731/3 · HN 1468/2
- because / due to → **because** · essays 2146/0 · HN 1253/0
- about / regarding / concerning → **about** · essays 2556/1 · HN 1986/1
- start / commence → **start** · essays 1500/1 · HN 683/0
- but / however → **but** · essays 4829/94 · HN 2748/41
- also / additionally / furthermore / moreover → **also** · essays 633/11 · HN 430/2
- make / create / produce / craft → **make** · essays 2634/396 · HN 1647/200
- show / demonstrate → **show** · essays 219/4 · HN 213/5
- help / assist → **help** · essays 311/0 · HN 213/1
- find / discover → **find** · essays 704/224 · HN 422/68
- big / large → **big** · essays 1003/295 · HN 548/175
- probably / perhaps → **probably** · essays 738/171 · HN 577/65
- very / quite → **very** · essays 621/154 · HN 461/126
- buy / purchase → **buy** · essays 323/10 · HN 209/12
- **strange / weird → REGISTER-CONDITIONAL:** essays prefer **"strange"** (73 vs 35); HN prefers **"weird"** (16 vs 29). Use "weird" in casual/comment register, "strange" in essay register. (The one binary that flips by format.)

### 6.6b Spelling / dialect / archaism variants (computed — among the most diagnostic; cross-format-locked)
American + one archaism ("till"), identical in essays and HN. [VOICE · XF]
- **till / until → till** — essays 238/52 (4.6×), HN 141/13 (~11×). The standout: "from dinner till about 3 am", "Till recently". Most modern writers default to "until"; PG doesn't, in either format.
- **among / amongst → among** — essays 122/0, HN 96/0. Never "amongst".
- **while / whilst → while** — essays 322/0, HN 220/0. Never "whilst".
- **toward / towards → toward** — essays 89/3, HN 25/7. American no-s.
- **learned / learnt → learned** — essays 141/2, HN 63/0.
- **-ize / -ise → -ize** — essays 471/0, HN 214/0.
- **-or / -our → -or** — essays 116/1, HN 93/2 ("color/behavior/favor").
- **ok / okay → ok** — essays 66/0, HN 125/0; **anyway / anyways → anyway** — essays 66/0, HN 52/0.
- Generation rule: lock all to PG's side in every format. A single "whilst", "towards", "amongst", or "-ise" breaks the fingerprint instantly.

### 6.7 Casualism / internet markers
- **Essays:** no internet casualisms; register is **conversational-essayistic** (28 contractions/1000w, "kind of"/"sort of"/"pretty much").
- **HN:** still no "lol"/"tbh"/emoji, but **looser**: ellipsis trailing-off ("I'm tuned...", 0.60/1000w), **"Yes,"/"No,"/"Actually,"/"Incidentally,"** comment-openers, occasional "Damn." / "Well, that worked." / "No, migpwr, I'm a hardass." (addresses other users by handle), higher contractions (34/1000w). Lowercase-everywhere is NOT a PG habit — he capitalizes normally even on HN.
- Don't import chat casualisms (lol/emoji/lowercase) into any format — PG doesn't use them.

### 6.8 Profanity
- Effectively none in essays; very rare and mild on HN ("Damn.", "hardass"). Don't add profanity.

### 6.9 Sentence-final vocabulary *(cross-format)*
- Dominant shape: **concrete-end / compressed-claim-end.** Sentences land on the noun or the point, not on a hedge. Essays: "…what business consists of." / "Be good." HN: "…we'll figure it out." / "Downvoting dumb stuff is a valid contribution." [VOICE · XF]

### 6.10 Topic-shift vocabulary
- **Essays:** no ornamental transition — **paragraph break alone**, or sentence-initial **"But"/"So"/"And"/"Now"** carrying the turn.
- **HN:** same, plus **"Incidentally,"** (135 in corpus) as the aside/tangent marker — denser than in essays. No "Moreover,"/"On a related note,". [VOICE · XF, amplified on HN]

### 6.11 Question vocabulary *(cross-format)*
- Essays: **"Why [does X]?"** / **"How do you [X]?"** as section pivots; **"If [X], [what/how]?"** as openers.
- HN: shorter, sharper — **"Why?"** as a one-word pivot inside a comment ("None had worked. Why? Because…"), and direct **"What happens in the 'not' case?"** / "They don't control for the college you go to?" The "claim. Why? Because…" micro-structure is a [VOICE · XF] move (appears in essays, comments, and tweets).

### 6.12 Banned-by-omission (lexical)
- Avoided in every format: "utilize", "obtain", "commence", "regarding", "due to" (connector), "demonstrate", "delve", "leverage" (verb), "moreover"/"furthermore", "however" (used but rare), "whilst"/"amongst"/"towards"/"-ise". See §1, §6.6, §6.6b.

### Pet phrases (computed n-grams)
- **Reader-advice machinery (essay-dominant VOICE):** "you have to" (essays 416 / HN 132), "you want to" (315/98), "be able to" (231/104), "have to be" (202/90), "if you want" (203). PG builds advice by telling "you" what you have to / want to / can do.
- **Reply machinery (HN-dominant):** "I don't think" (HN 195), "I don't know" (122), "I'm not sure" (75), "I think the" (72). The comment-register engine.
- **Connective units (both):** "a lot of" (essays 610 / HN 414), "one of the most" (140), "the most" (680), "it would be" (188/162), "turn out to be"/"out to be" (144/79), "most of the".
- **Topic-bound (do NOT import as voice):** "start a startup" (195), "a startup" (783).

## 7. Sentence structure & rhythm
- **[VOICE · XF | high] High burstiness — short punch sentences against long winding ones.** Essay σ 10.07; HN comments alternate one-line replies with longer reasoned ones. Punch examples: "Meetings cost them more." / "Be good." / (HN) "Well, that worked." / "No, that one was flagged to death." Don't even out the rhythm.
- **[VOICE · XF | high] Sentence-initial conjunctions** ("But", "And", "So") as connective tissue in both formats.
- **[VOICE · XF | high] Conditional reasoning** — "If X, then Y" everywhere (essays 1582 sentence-initial "if"; HN 801).
- **[VOICE · XF | medium] Colons introduce the payoff** (~4.9–5.1/1000w both): "There are two types of schedule, which I'll call…"
- Paragraph shape: **essays ~3 sentences** [PLATFORM · essay]; **HN 1–2 sentences** [PLATFORM · HN].

## 8. Quirks & idiosyncrasies
- **[VOICE · XF | high] "till" for "until"** — both formats (§6.6b).
- **[VOICE · XF | medium] "Claim. Why? Because…" micro-structure** — poses his own one-word question and answers it, in essays, comments, and tweets.
- **[VOICE · XF | medium] "Incidentally," asides** (denser on HN).
- **[VOICE · essay | high] Coins-and-names a concept mid-flow** ("a phenomenon I call…", "which I'll call…"), §4.7 — essays only.
- **[VOICE · XF | high] Compressed "X is just/merely Y" definitions** ("Prestige is just fossilized inspiration").
- **[VOICE · essay | high] "Thanks to [names] for reading drafts of this." footer** — essay-format only.
- **[VOICE · XF | medium] Domain-transfer analogies from programming** ("having a meeting is like throwing an exception") — heavy in essays, lighter on HN.
- **[VOICE · XF | medium] Parenthetical asides that qualify or joke** ("(This is also true of starting a startup generally.)").
- **[VOICE · XF/HN | medium] Addresses other users by handle and answers as a peer** ("No, migpwr, I'm a hardass.") — comment-register.

## 9. Negative rules (patterns demonstrably absent)
- 0 "utilize" / 0 "delve" / 0 "seamless" / 0 figurative "navigate" across 910k words of essays + comments.
- 0 "experts say" / "studies show" authority appeals; argues from instance and mechanism (cross-format).
- Near-0 "moreover"/"furthermore"/"additionally"; uses "also"/"but"/"and".
- Near-0 exclamation (essays 0.17, HN 0.28/1000w). No rule-of-three flourishes. No generic-uplift closers.
- No em-dashes in comments/tweets (essay-only at ~1/1000w).
- No lowercase-everywhere, no emoji, no "lol"/"tbh" in any format.

## 10. Default mode
**Depends on the requested format — match the target register, don't average across formats.**
- Default for **long-form / "write an essay/post"** → essay mode (§11.A): thesis, mechanism, named examples, compressed close, ~3-sentence paragraphs.
- Default for **a reply / comment / "respond to this"** → HN-comment mode (§11.B): terse, first-person, opens with the verdict ("Yes,"/"No,"/"I don't think").
- Default for **a one-liner / post** → tweet mode (§11.C): a single compressed claim or mini-anecdote.
- Across all three, the **voice layer is constant** (plain verbs, "but"/"so" starts, conditionals, "probably", "till", concrete-ends, all synonym binaries + spelling locks). What changes is **scaffolding, length, dash usage, and pronoun ratio.**

## 11. Format-specific modes (each grounded in its own index)

### 11.A Essay mode (PRIMARY — fully evidenced)
- Opening: direct thesis (or question / anecdote); coined term near the top.
- Arc: problem → name/reframe → mechanism → named examples (named-company + anecdote + domain-transfer) → derived advice.
- Stats: ~16.6w sentences, σ≈10, ~3.2-sentence paragraphs, colon 4.9/1000w, em-dash ~1/1000w, question 3.5/1000w, "you" > "I".
- Furniture: numbered footnotes (drier asides); "Thanks to … for reading drafts of this." footer.
- Aphorism closes the piece. Reference horizon spans centuries and 3–5 domains.

### 11.B HN-comment mode (NEW — evidenced, ~339k words)
- **Opener = the verdict, not a thesis.** "Yes," (289) / "No," (245) / "I don't think…" (195) / "Actually," (192) / "Incidentally," (79) / direct restatement of the question.
- **Terser:** ~14.9w sentences, paragraphs of 1–2 sentences; many comments are a single sentence ("Well, that worked." / "Yes, that's a great example.").
- **First-person, peer-to-peer:** "I" > "you"; answers as one builder to another; will address users by handle.
- **Disagreement shape (the move the essays under-evidenced):** "No," + direct counter + mechanism; or "I wouldn't (quite) say… , [what he'd say instead]"; concedes with "You're right." / "Good point." then qualifies.
- **More casual punctuation:** ellipsis trailing-off (0.60/1000w), higher contractions (34/1000w) and hedging (5.88/1000w), higher question rate (4.22/1000w). **No em-dashes** (~0/1000w). Colon stays at essay rate (5.06).
- **No essay furniture:** no footnotes, no drafts-footer, no coined terms, no Renaissance roaming, no multi-domain analogies. Concretizes with a named startup or an exact number/ratio.
- "weird" replaces "strange" (§6.6). "Why? Because…" micro-structure survives.

### 11.C Tweet / short-form mode (evidenced but THIN — 15 tweets, ~560 words; directional)
- A **single compressed claim or one mini-anecdote**, self-contained. Reads like an essay's thesis sentence or its closing aphorism, standing alone.
- Templates observed: **"It's a bad sign when X. [why]. Y is incidental."**; **"Don't worry, [reassurance]. [mechanism]."**; **mini-anecdote → "Why? Because…"** ("Talked to a guy who'd had several genuinely good startup ideas. None had worked. Why? Because he was neither a programmer nor had a cofounder who was.").
- Stats (tiny sample): ~14.5w sentences, high contractions (~32/1000w), **no em-dashes, no semicolons, no hashtags, no emoji.** Occasional numbered micro-list ("1. Type tweet. 2. Hit 'Tweet' button. 3. Report crypto spam reply.").
- Voice layer identical to essays (plain verbs, "but"/"so", "honestly", concrete-end). **Low confidence on rates** — flag in any tweet-mode output.

### 11.D Technical / long-form-reference mode (*On Lisp*, *ANSI Common Lisp* — cross-check only; stats NOT folded in)
- Recognizably PG (plain verbs, "but" connectors, reframe — "There is more to Lisp than this…"), but **more formal/expository**: fewer contractions, more declarative scaffolding, named-source quotes introduced with a colon ("John Foderaro has come close: Lisp is a programmable programming language."). 
- Use only if explicitly writing technical reference prose; do not let its formality bleed into essay/comment/tweet output.

### 11.E Speech (interviews, talks — cross-check only, NOT voice stats)
- Transcribed speech is contaminated by interviewer edits, spoken filler, and page chrome. Used here only to confirm the cognitive/vocabulary layers carry into speech (they do). Do not generate "spoken PG" from this profile without real transcript calibration.

## 12. Voice in action (prompt-ready examples)
- **Essay opening (~50w):** "Most people think the way to be original is to try hard to be original. But originality isn't something you reach for directly. It's a byproduct. The people who produce the most original work are usually just trying to get something to work, and notice, along the way, that no one has done it quite like this."
- **HN-comment reply (~2–3 sentences):** "No, I don't think that's the problem. The reason the signups dropped is that you moved the button below the fold. We saw exactly the same thing with a YC company last year. Move it back and measure again." *(Note: no em-dash — HN-comment mode runs ~0 em-dashes, §11.B; an em-dash here would be an essay-mode leak.)*
- **Short concession reply (~1 sentence):** "You're right, but that only holds if the users are paying. For free products the incentive runs the other way."
- **Tweet (~1–2 sentences):** "It's a bad sign when a founder talks more about their fundraising than their users. The users are what determine whether the company lives. The round is just a number."

## 13. Confidence notes
- **Now a multi-format corpus (clears the 2+ formats bar):** essays (570.7k) + HN comments (339k) + tweets (560). The VOICE-vs-PLATFORM calls in this profile are **evidenced, not guessed** — that's the upgrade over the prior single-format version.
- **Tweet sample is tiny (15 tweets / ~560w).** Tweet-mode (§11.C) rates are directional; everything there is low-confidence. Get more verified tweets before trusting densities.
- **HN burstiness (σ 35) is inflated by a few pasted lists** (e.g. a 5,090-token spam-domain dump with no sentence punctuation). The real comment rhythm is short. Treat HN σ as unreliable; the sentence-length mean (14.9w) and paragraph length (2.0) are sound.
- **HN raw index is heavily boilerplate-polluted** (`Source:` URLs, ISO timestamps, "news/ycombinator/item/id"). The numbers in §5/§6 for HN are from a **cleaned re-index** (headers, source lines, and the top-level title stripped); the raw `paul-graham.hn.index.json` is kept only for provenance.
- **Disagreement voice is now evidenced** (HN), filling the gap the prior profile flagged. Adversarial/long-form refutation is still thinner than agreement; if writing a full rebuttal essay, calibrate.
- **Export artifacts:** essay `.md` files carry a "Want to start a startup? Get funded by Y Combinator." line and URL/title headers; negligible against 570.7k words but they inflate "title"/"url" keyness (dropped). The essay `--` (446) vs `—` (565) split is an export artifact — render `—` only.
- **Speech and the Lisp books are cross-checks, not voice sources** (§11.D/E) — their stats are deliberately excluded from §5/§6.
- "actually" (essays 297 / HN 550), "merely" (240), "incidentally" (HN 135) read like LLM-isms but are genuine, cross-format-confirmed PG voice; allowed at corpus density (§1).

## Changelog
- 2026-05-20 **Created as a multi-format profile** from essays (231 docs, 570.7k words) + HN comments (~9,980 comments, 339k words cleaned) + 15 verified tweets. Per-format indexes computed by `scripts/index_corpus.py` (`paul-graham.index.json` canonical; `.hn.index.json`, `.x.index.json` for the secondary formats; HN re-indexed after boilerplate-cleaning). Headline change vs the prior single-format version: every layer re-classified VOICE-cross-format vs PLATFORM-essay with cross-format evidence; real HN-comment mode and tweet mode added (§11.B/C); disagreement-voice added from HN (§3); em-dash reclassified essay-PLATFORM; strange/weird found register-conditional. Numbers transcribed verbatim from the indexers.
