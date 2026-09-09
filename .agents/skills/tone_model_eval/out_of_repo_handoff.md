Required checklist for acting on a positive recommendation from this eval (the
spec's Behavior #4/#5). None of these steps live in this repo — no file in
`warpdotdev/docs` selects which model powers a `draft_*`/copy-pass skill run;
that's controlled at the Warp platform level.

1. **Enumerate schedules that run docs drafting.**
   ```bash
   oz schedule list
   ```
   Filter the result to schedules whose prompt or skill references
   `warpdotdev/docs` drafting (`draft_docs`, `draft_feature_doc`,
   `draft_quickstart`, or any other copy-pass skill).

2. **Record each schedule's current model.**
   ```bash
   oz schedule get <SCHEDULE_ID>
   ```
   Run this once per schedule found in step 1 and note its `model_id`.

3. **Find the Agent Profile for ad hoc/event-triggered runs.** A drafting run
   that isn't `oz schedule`-triggered (a Slack- or Linear-triggered request, for
   example) uses an Agent Profile's base model instead. In the Warp app, go to
   **Settings** > **Agents** > **Profiles** and identify which profile owns docs
   drafting requests, then note its base model.

4. **Apply the eval's recommended model.**
   - For a schedule found in step 1:
     ```bash
     oz schedule update <SCHEDULE_ID> --model <MODEL_ID>
     ```
   - For an Agent Profile found in step 3: update its base model in
     **Settings** > **Agents** > **Profiles** in the Warp app.

5. **Name who is authorized to run these commands.** Whoever owns/administers
   Pod-Docs' scheduled agents runs steps 1-4. Confirm the current owner before
   running the commands — this configuration isn't version-controlled in this
   repo, so the eval report can't pin a name that stays accurate over time.

6. **Verify the change took effect.** Re-run this eval's fixture set
   (`score_outputs.py score` + `report`) through the newly-configured model, or,
   at minimum, check the next 2-3 real agent-authored docs PRs'
   `style_lint.py --changed` and `review-docs-pr` output for the violation
   categories this eval flagged (`tone-buzzword`, `tone-meta-opener`) to confirm
   production output matches what the eval predicted.

A "no meaningful difference found" outcome (see the eval report's
recommendation section) skips this checklist entirely — there's nothing to
hand off.
