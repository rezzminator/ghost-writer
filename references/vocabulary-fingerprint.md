# Vocabulary Fingerprint

A reference used during Mode A (extract) to capture the writer's lexical choices — the specific words they reach for when they have alternatives. This is the layer that classical stylometry (the Federalist Papers method, function-word attribution) leans on most, because it's hard to fake and deeply identifying.

Read this file alongside `extraction-checklist.md` and `cognitive-moves.md`. The mechanical layer captures *how* sentences are shaped; the cognitive layer captures *what moves* the writer makes on an idea; this layer captures *which specific words* gets reached for.

## Compute it; don't estimate it

**The countable parts of this layer must be produced by `scripts/index_corpus.py`, not by eyeballing the corpus.** Estimating word frequencies by reading is lossy and unreliable — a human (or a model skimming) will swear a writer "uses 'leverage' constantly" when the real count is 3 in 50,000 words. The indexer counts every word and gives you exact figures: the top 200 content words, the full function-word table, the synonym-binaries tally across all inflections, ranked hedges and intensifiers, and candidate pet-phrase n-grams.

Run it first (Mode A Step 2):

```bash
python3 scripts/index_corpus.py <corpus> --top 200 --json out.json
```

Then transcribe its output into Sections 6.1–6.6 verbatim. Reserve human judgment for what the indexer can't compute: which top-content words are *voice* vs *topic* (6.1), casualism markers in context (6.7), profanity in context (6.8), sentence-final shape (6.9), topic-shift habits (6.10), question shape (6.11). The index gives you the skeleton; you add the reading.

**Capture at least the top 200 content words** for a substantive corpus — not a hand-picked 15. The long tail matters: word #150 ("merely", "till") is often more identifying than word #5, because the common words are shared by everyone and the mid-frequency words are where individual voice lives.

## What this layer is

Vocabulary fingerprint is the set of word-level choices the writer makes, observable across the corpus as **consistent picks among alternatives**. The diagnostic question is not "does the writer use the word X" — almost any writer uses any common word at least once. The diagnostic question is: when the writer had a choice between near-synonyms, which did they pick *consistently*?

A vocabulary rule qualifies for the profile only if:

- The word or category appears in the corpus with measurable frequency (or measurable absence).
- Where a near-synonym was available, the writer's pick is consistent across at least two distinct pieces.
- The rule has a quoted instance — or, for frequency rules, a count.

## What this layer is NOT

- **Single-occurrence words.** "Said 'kerfuffle' once" is not a vocabulary rule.
- **Topic vocabulary.** Words specific to the subject of a piece, not the writer. If the corpus is about hiking, "elevation" appearing 12 times is topic, not voice.
- **Generic word-frequency virtues.** "Has a wide vocabulary." Only meaningful with numbers (type-token ratio) and only useful if distinctively high or low for the register.

The line between vocabulary fingerprint and topic vocabulary is the cross-piece test: if a word recurs across pieces on different topics, it's vocabulary. If it recurs only in pieces on one subject, it's topic.

## Categories to scan for

When reading the corpus, scan along each dimension independently. Capture: the rule, frequency or count, quoted instances, and classification (VOICE / PLATFORM / BORDERLINE — most vocabulary is VOICE).

### 1. Distinctive lexicon (keyness, NOT raw frequency)

**Raw word frequency is the wrong tool for vocabulary fingerprint, and this is the most important thing to get right.** The most-frequent words in *every* English writer are the same generic words — "one, like, get, work, good, people, things, way." Ranking by raw count surfaces those and tells you nothing about the individual. (If your top word is "one", you used the wrong ranking.)

What you want is **keyness**: how much *more* the writer uses a word than baseline English. The indexer computes this — its "Distinctive vocabulary (keyness-ranked)" section is what feeds this profile section, *not* the raw-frequency list. Keyness surfaces "merely", "till", "schlep", "founders" — the words that are actually this writer — instead of "good" and "way".

Then comes the judgment step the script **cannot** do: split the keyness list into **voice** (travels across the writer's pieces regardless of subject — "merely", "till", "tend", "simply") vs **topic** (bound to what this corpus happens to be about — "startup", "lisp", "founders", "vcs"). Both score high keyness; only the *voice* words become generation rules. Topic words are explicitly excluded so generated text doesn't drift to the writer's usual subjects. Also drop residual names and boilerplate the filter missed (a domain, a co-founder's name). **This voice-vs-topic call requires a reader — it's the clearest example of why the indexer and human judgment are partners, not substitutes.**

Capture the top ~40–60 voice words from the keyness list. Keep the raw-frequency top-200 only as a reference for the quantitative/function-word layer; don't mistake it for the fingerprint.

Skip stopwords (the, a, of, and, one, etc.) — those are the function-word layer below.

### 2. Function-word frequency

The top function words from the indexer (articles, prepositions, common conjunctions, common pronouns, modal verbs, "be" forms). This is the layer hardest to fake during generation and most diagnostic during authorship attribution.

The signal isn't the absolute frequencies (every English text leans on "the", "of", "to") — it's the *relative* frequencies. Does this writer use "I" three times more than "you"? Does "but" outrank "however" by 8:1? Does "we" appear at all? These ratios are the fingerprint.

For thinner corpora, just capture standout function-word patterns — don't force a full frequency table.

### 3. Verb preferences

The writer's top 20 verbs by frequency, with the diagnostic question: where common alternatives existed, which did they pick?

The most identifying axis is plain vs. elevated:

- **Plain verbs:** use, make, do, get, have, go, take, give, show, find, put, ask, tell, say, see, know, think, try
- **Elevated alternatives:** utilize, create/produce/craft, execute/perform, obtain/acquire, possess, depart/proceed, accept/receive, contribute/deliver, demonstrate/illustrate, locate/identify, position/situate, inquire, inform/notify, articulate, observe/perceive, comprehend/recognize, contemplate/consider, attempt

A writer who consistently picks "use" over "utilize" and "show" over "demonstrate" has a markedly different fingerprint from one who reaches for the elevated form. This is one of the highest-signal vocabulary dimensions.

### 4. Hedge vocabulary

Not just hedge *rate* (already in the quantitative layer), but which hedges specifically. Each writer reaches for a different subset:

- "I think" / "I guess" / "I'd say" / "I'd argue"
- "Maybe" / "probably" / "likely" / "possibly"
- "Sort of" / "kind of" / "kinda" / "sorta"
- "Honestly" / "frankly" / "to be fair"
- "Could be that" / "might be" / "it's possible"
- No hedges (commits directly)

A writer who hedges with "I think" but never "kind of" has a different fingerprint from one who hedges with "kind of" but never "I think." Catalog the writer's top 5 hedges with counts.

### 5. Intensifier vocabulary

Same logic for intensifiers:

- "Really" / "very" / "super" / "extremely" / "absolutely"
- "Pretty" / "fairly" / "somewhat" / "rather"
- "Totally" / "completely" / "entirely"
- "Kinda" / "a bit" / "a little"
- No intensifiers (uses precise words instead)

Top 5 intensifiers with counts. A writer who reaches for "super" reads completely different from one who reaches for "rather", even with identical mechanical patterns.

### 6. Synonym binaries

The most identifying section in this whole layer. When the corpus shows the writer had a choice between two common alternatives, list the binaries with their consistent pick:

| Pair | Writer picks | Evidence |
|---|---|---|
| use / utilize | use | "use the existing config" |
| help / assist | help | "this helps debug" |
| weird / strange | weird | "kinda weird that…" |
| but / however | but (sentence-initial) | "But the test fails" |
| big / large / sizable | big | "a big change" |
| guess / assume | guess | "I'd guess so" |
| OK / okay | OK | "OK so let's…" |
| etc. | | |

Look for these especially in transitional and intensifier positions, where the writer had real alternatives. Aim for 8–15 binaries in a substantive profile. They compound — applying the binaries during generation is one of the fastest ways to make output sound like the writer.

### 7. Casualism / internet markers

For writers with corpora that include chat, Slack, Twitter/X, Reddit, Discord:

- "Lol" / "lmao" / "haha" / "ahah" — and at what frequency
- "Fr" / "ngl" / "tbh" / "imo" / "imho" / "iirc"
- "Rn" / "ig" / "idk" / "idc"
- Lowercase sentence starts as a register marker
- Letter-stretching for emphasis: "niiiice", "soooo"
- Emoji frequency by category (faces, hands, objects)

Capture with density (per 1000w, or per message in chat formats) and the writer's specific subset.

### 8. Profanity

Frequency, specific words used, and contexts where it appears (only in chat? in long-form too? only when frustrated? as intensifier vs. as content?). Profanity is hard to ignore as fingerprint — a writer who never swears is texturally different from one who casually drops "shit" mid-sentence, and the imitation will read wrong if you get this wrong in either direction.

### 9. Sentence-final vocabulary

What words tend to land at the end of a sentence? Three common shapes:

- **Hedge-end:** "…probably." / "…I think." / "…or so."
- **Concrete-end:** "…the database." / "…Tuesday." / "…$40."
- **Intensifier-end:** "…really." / "…fast." / "…a lot."

Some writers consistently end on a specific shape across sentences. This is observable and identifying.

### 10. Topic-shift vocabulary

How does the writer signal a topic change between paragraphs? Catalog the specific transitions used:

- "Anyway,"
- "OK so,"
- "Right,"
- "Now,"
- "But here's the thing —"
- "Moving on,"
- "On a related note,"
- No transition word, just a new paragraph

A writer's typical topic-shift word is one of their most identifying small-scale tics.

### 11. Question vocabulary

When the writer asks a question, what shape does it take?

- "What if X?"
- "Is X actually Y?"
- "Why does X happen?"
- "Could X be Z?"
- "I wonder if X."
- Direct statement-as-question: "X is Y?"

If the corpus has multiple questions, the question shape is often very consistent within a writer.

### 12. Banned-by-omission (vocabulary subset)

A focused subset of Section 1 of the profile: words the writer demonstrably avoids at the lexical level. Especially:

- Plain-word alternatives the writer always picks (from Synonym binaries, surfaced here as the *avoided* word).
- LLM-tell vocabulary the corpus shows zero or near-zero usage of (cross-reference `llm-isms.md`).
- Register-violations: words the writer never crosses register lines on (e.g., never uses "kinda" in formal contexts).

## Extraction prompts

When reading the corpus, ask these questions explicitly:

1. What are the 20 most-frequent content words across the corpus? Of those, which are tied to topic and which travel across pieces?
2. Of the writer's verbs in the corpus, what fraction is "plain" (use, make, do, have, get, take) vs. "elevated" (utilize, craft, execute, possess, obtain)? Note the ratio.
3. List every hedge that appears 3+ times. What's the writer's top hedge by frequency?
4. List every intensifier that appears 3+ times. What's the writer's top intensifier?
5. Pick 5 synonym pairs that show up in the corpus (use/utilize, help/assist, big/large, weird/strange, but/however). Which side did the writer pick? Consistent?
6. Are there casualism markers in the corpus? If yes, which ones, and at what density?
7. Is there profanity? If yes, at what rate and in which contexts?
8. How does the writer end sentences? Sample 20 sentence endings from across the corpus and look for a shape.
9. Look at every paragraph transition in the corpus. Is there a recurring topic-shift word?
10. Look at every question in the corpus. Is there a recurring question shape?
11. What's the writer's contraction rate? (Already in quantitative layer, but verify against vocabulary observations.)
12. Find a word a default writer would use that this writer demonstrably never uses. (Vocabulary-level banned-by-omission.)

## Profile section format

This is the expanded Section 5 of the profile template. It replaces the stub Vocabulary & word choice section. Apply when the corpus is substantive enough (≥5000 words and ≥10 pieces). For thinner corpora, use the abridged version below.

```markdown
## 5. Vocabulary fingerprint

### 5.1 Top content lexicon
- Top content words (excluding stopwords, 30 items for substantive corpora, 15 for thinner):
  "<word>" (Nx), "<word>" (Nx), …
- Words that travel across pieces (voice, not topic): "<word>", "<word>"
- Words tied to single pieces (topic, excluded from rules): "<word>"

### 5.2 Function-word patterns
- Standout function-word patterns: "<observation, e.g., 'but' outranks 'however' 12:1>"
- Pronoun preferences: I/we/you ratios if distinctive
- (For substantive corpora) Top 15 function words with counts.

### 5.3 Verb preferences
- Top 20 verbs by frequency.
- Plain-to-elevated ratio: <e.g., "85% plain (use, make, do); rarely elevated (1 'utilize' in 8000 words)">
- Identifying verb picks: "<verb>" over "<alternative>" — Nx in corpus.

### 5.4 Hedge vocabulary
- Top hedges with counts: "I think" (Nx), "probably" (Nx), "kind of" (Nx)
- Hedges the writer demonstrably avoids: "<hedge>"

### 5.5 Intensifier vocabulary
- Top intensifiers with counts: "<word>" (Nx), "<word>" (Nx)
- Intensifiers avoided: "<word>"

### 5.6 Synonym binaries (the diagnostic table)
- use / utilize → uses "use" (12x vs 0x)
- help / assist → uses "help" (8x vs 0x)
- but (sentence-initial) / however → uses "but" (15x vs 1x)
- weird / strange → uses "weird" (4x vs 1x)
- guess / assume → uses "guess" (3x vs 0x)
- [add 8–15 binaries observed in the corpus]

### 5.7 Casualism / internet markers
- (If present) "<marker>" (per 1000w or per message)
- (If absent — register is consistently formal) Note: no casualism markers observed.

### 5.8 Profanity
- Rate: <e.g., "1 per 1000w in casual contexts, 0 in long-form">
- Specific words: "<word>", "<word>"
- (Or: no profanity in corpus.)

### 5.9 Sentence-final vocabulary
- Dominant shape: <hedge-end / concrete-end / intensifier-end / mixed>
- Examples from corpus:
  - "<sentence end 1>"
  - "<sentence end 2>"

### 5.10 Topic-shift vocabulary
- Most-used topic-shift word: "<word>" (Nx)
- Other shifts observed: "<word>", "<word>"
- (Or: no consistent topic-shift word — paragraph break alone.)

### 5.11 Question vocabulary
- Dominant shape: "<shape, e.g., 'What if X?' or direct statement-as-question>"
- Examples:
  - "<question 1>"
  - "<question 2>"

### 5.12 Banned-by-omission (lexical)
- Words the writer demonstrably avoids: "<word>", "<word>"
- Cross-reference with Section 1 of profile for the master never-say list.

### Pet phrases (multi-word recurring units)
- "<phrase>" (Nx)
- "<phrase>" (Nx)
```

For thin corpora (<5000 words OR <10 pieces), use an abridged version with sections 5.3 (verb preferences), 5.4 (hedges), 5.6 (synonym binaries), 5.7 (casualisms), 5.10 (topic-shift), and pet phrases. Skip the top-N lexicon and function-word frequency tables — they'll be noisy with thin data.

## How this gets used in Mode B

During generation, the vocabulary fingerprint sits below the cognitive moves in the read order: cognitive moves shape *what* gets said; vocabulary shapes *which words* get reached for to say it.

1. Read banned words first (Section 1).
2. Read anti-performative (Section 2).
3. Read cognitive moves (Section 3) — internalize the writer's typical operations on the topic.
4. Read vocabulary fingerprint (Section 5) — internalize the verb/hedge/intensifier choices, the synonym binaries, the casualism markers.
5. Draft. As you write each sentence, when you reach for a verb, check the binaries — is the plainer alternative the writer's pick? When you reach for a hedge, check Section 5.4 — is this the writer's actual hedge or one they don't use?
6. Self-review includes a vocabulary check (folded into Pass 3, alongside cognitive moves): did the draft apply the synonym binaries? Use the writer's hedges, not generic ones? Match casualism density?

## Common failure modes

- **Lexicon padding.** Forcing every top-content word from the corpus into the draft, regardless of whether it fits the new task. Frequency in the corpus tells you what's available to the writer, not what's required in every output.
- **Synonym binary inversion.** Picking the elevated form when the writer always picks plain. Single most common vocabulary failure during generation — Claude's defaults skew elevated, the writer's voice usually doesn't.
- **Hedge homogenization.** Reaching for "perhaps" / "potentially" / "arguably" (Claude defaults) when the writer reaches for "maybe" / "I think" / "probably" / "kinda". Different hedges have different temperatures.
- **Topic contamination.** Including words tied to specific corpus pieces ("the migration", "the bug we found") in a draft on a different topic. Vocabulary rules must cross-piece test.
- **Casualism crank.** Adding "lol" or emoji or letter-stretching at higher density than the corpus shows. The casualism markers in this layer are *match the density*, not *use because the writer occasionally does*.
- **Profanity miscalibration.** Either adding profanity that wasn't in the corpus (manufacturing edge), or scrubbing profanity that was characteristic (sanitizing).
