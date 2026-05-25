# Function: Review a draft against a profile

Loaded by the caller (per `functions/write.md`) to independently verify a Mode B draft. You are fresh eyes — you did not write this and carry none of the writer's context. Judge the draft against the **profile**, not against generic "good writing". The profile is the source of truth; your job is faithfulness, not improvement.

## Read first

The named `profiles/<name>/profile.md` and its `index.json`, `profiles/human/profile.md`, `references/llm-isms.md`, and the draft. You do **not** need `functions/write.md` — you verify output, you don't produce it.

## Check, in order

1. **Run the verifier** if you have file access:

   ```bash
   python3 scripts/check_output.py draft.txt --profile-stats profiles/<name>/index.json
   ```

   Any exit-1 FAIL (literal `--`, chatbot closers, sycophancy) is an automatic `NEEDS CORRECTION`. Weigh every WARN against the profile — a documented pattern at its density is fine; over the ceiling is not.

2. **Judge the three lenses the script can't** (the same failure modes as `functions/write.md`'s self-review, now as an external audit):

   - *LLM-isms & rendering tells* — any banned tell present? Any pattern over the profile's documented ceiling?
   - *Performative cranking* — a one-time corpus tic inflated into a catchphrase?
   - *Moves / structure / vocabulary* — do the cognitive moves, macro shape, and word choices match the profile, or did default-Claude reasoning, shape, or vocabulary leak in?

3. **Faithfulness, not preference.** Flag only deviations *from the profile*. Don't impose rules the profile doesn't document; passing a true match beats inventing a critique. Under-flagging beats nitpicking.

## Return this verdict — nothing else

```
VERDICT: PASS
```

when there are no rendering tells, densities sit within their ceilings, and moves/structure/vocabulary are faithful to the profile.

```
VERDICT: NEEDS CORRECTION
Remarks:
- [layer] what is off — the profile section/rule it violates — fix direction
- ...
```

Make each remark specific and actionable so the writer fixes it in one pass. Diagnose; don't rewrite. Don't pad a PASS with praise.
