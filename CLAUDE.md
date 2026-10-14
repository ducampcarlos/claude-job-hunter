# Job hunter: rules for Claude

This repo is a personal job-application workspace. These rules apply to every task here.

## Non-negotiable

1. **Never invent experience.** Use only what is in `profile/master-cv.md` and `profile/achievements.md`. You may reorder, shorten, reword and emphasise; you may not add a skill, employer, title, date, metric or tool that is not there. If the job asks for something the candidate lacks, say so in `analysis.md` as a *gap*.
2. **Never send anything.** No submitting forms, no sending email, no messaging recruiters. Prepare drafts (files, Gmail drafts) and stop for the human to review and send.
3. **Never automate logged-in job platforms** (LinkedIn, Indeed, etc.): their terms forbid it and it can get the account banned. Reading a public job posting by URL is fine.
4. **Privacy.** `profile/*.md` (without `.example`), `jobs/` and `tracker.csv` are gitignored. Never copy their contents into committed files, issues or commit messages.
5. **Honest match.** If the fit is poor, say so and recommend skipping rather than polishing a weak application.

## Layout

- `profile/`: source of truth about the candidate (copy the `*.example.md` files to start).
- `jobs/<YYYY-MM-DD>_<company>_<role>/`: one folder per application (`job.md`, `analysis.md`, `cv.md`, `cover-letter.md`).
- `tracker.csv`: managed with `python scripts/tracker.py`.
- Skills: `/apply <url or pasted posting>`, `/interview <company folder>`, `/followup`.
