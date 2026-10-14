---
name: followup
description: Find applications that are due for a follow-up and draft short, polite follow-up messages. Drafts only; never sends.
---

# /followup

Follow `CLAUDE.md`.

1. Run `python scripts/tracker.py due` to list applications whose follow-up date has passed.
2. For each one, read its folder in `jobs/` and write `followup.md` with a 3-4 sentence message: reference the role and the date applied, add one new relevant fact if there is one, ask about next steps, and offer to answer questions.
3. If a Gmail connector is available, create a **draft** (never send) addressed to the recruiter contact if one is known; otherwise leave the text in `followup.md`.
4. After the human sends it, they run `python scripts/tracker.py update <id> --followup-in 7` to push the date.
