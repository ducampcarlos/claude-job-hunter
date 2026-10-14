---
name: apply
description: Prepare a tailored job application from a posting URL or pasted text. Saves the posting, scores the fit honestly, adapts the CV and writes a cover letter from the candidate's real profile, then logs it in the tracker. Never sends anything.
---

# /apply

Input: a job posting URL or the pasted posting text.

Follow `CLAUDE.md`. In particular: never invent experience and never send anything.

## Steps

1. **Read the profile.** Load `profile/master-cv.md`, `profile/achievements.md` and `profile/preferences.md`. If a file is missing, tell the human to copy the matching `*.example.md` and fill it in, then stop.
2. **Get the posting.** For a URL, fetch the public page. For pasted text, use it as is. If the page needs a login, ask for the pasted text instead. Create `jobs/<YYYY-MM-DD>_<company>_<role>/` and save the posting as `job.md` (postings disappear).
3. **Analyse** into `analysis.md`:
   - Role, seniority, stack, location/remote policy, salary if stated.
   - Requirements split into **must-have** and **nice-to-have**.
   - **Match table:** each must-have → evidence from the profile (quote the line) or `GAP`.
   - **Fit score** 0-100 with a two-line justification, plus red flags (vague scope, unpaid test, unrealistic stack list, conflicts with `preferences.md`).
   - **Recommendation:** `apply`, `apply with caveats` or `skip`. If `skip`, stop here and log it in the tracker as `saved` with the reason.
4. **Tailor the CV** into `cv.md`: one page, most relevant experience first, keywords from the posting *only where they are true*, achievements with their real metrics. Keep the same facts as the master CV.
5. **Cover letter** into `cover-letter.md`: under 200 words, specific to this company, no clichés ("passionate", "team player"), one concrete story from the achievements file that maps to their top requirement. Mirror the language of the posting (Spanish or English).
6. **Self-check** before finishing: for every claim in `cv.md` and `cover-letter.md`, confirm it appears in the profile. Remove anything that does not.
7. **Log it:**
   `python scripts/tracker.py add --company "<c>" --role "<r>" --link "<url>" --fit <score> --status saved`
8. **Report** in a few lines: fit score, the gaps, files created, and what the human must do next (review, export `cv.md` to PDF, apply manually). Do not apply on their behalf.

## Output quality bar

- Facts match the master CV exactly.
- No more than one page of CV.
- Gaps are shown, not hidden.
