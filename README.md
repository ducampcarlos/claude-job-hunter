# claude-job-hunter

[![CI](https://github.com/ducampcarlos/claude-job-hunter/actions/workflows/ci.yml/badge.svg)](https://github.com/ducampcarlos/claude-job-hunter/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-yellow.svg)](LICENSE)

**A [Claude Code](https://claude.com/claude-code) workspace that prepares job applications for you, and leaves the sending to you.**

Give it a job posting. It saves the posting, scores your fit honestly, adapts your CV and writes a short cover letter **using only facts from your own profile**, then logs the application. You review everything and press send yourself.

## Why it works this way

* **It never invents experience.** Your tailored CV is a reordering and rewording of a master CV you wrote. Gaps against the posting are shown as gaps, not hidden.
* **It never sends or submits anything.** No auto-apply, no bots on LinkedIn or other platforms (their terms forbid it and it can get your account banned). Mass applications also convert worse than a few personalised ones.
* **Your data stays on your machine.** Your profile, the `jobs/` folder and the tracker are gitignored; only `*.example` templates are committed.

## Quickstart

```bash
git clone https://github.com/ducampcarlos/claude-job-hunter.git && cd claude-job-hunter

# 1. Create your private profile from the templates
for f in profile/*.example.md; do cp "$f" "${f%.example.md}.md"; done
# edit profile/master-cv.md, achievements.md, preferences.md

# 2. Open Claude Code in this folder and run:
#    /apply https://example.com/jobs/backend-engineer
```

## Commands (Claude Code skills)

| Command | What it does |
| --- | --- |
| `/apply <url or text>` | Saves the posting, analyses requirements vs. your profile (with a fit score and gaps), writes `cv.md` and `cover-letter.md`, logs it in the tracker. Recommends **skip** when the fit is poor. |
| `/interview <job folder>` | Researches the company from public sources and prepares likely questions with STAR answers drawn from your achievements bank, plus how to address each gap. |
| `/followup` | Finds applications past their follow-up date and drafts short messages (Gmail **drafts**, never sent). |

The rules Claude follows live in [`CLAUDE.md`](CLAUDE.md) and the skills in [`.claude/skills/`](.claude/skills/).

## Layout

```
profile/                      your source of truth (gitignored; *.example.md are the templates)
jobs/2026-10-14_acme_backend/ one folder per application (gitignored)
  job.md  analysis.md  cv.md  cover-letter.md  interview-prep.md  followup.md
tracker.csv                   managed by scripts/tracker.py (gitignored)
scripts/tracker.py            dependency-free tracker CLI
```

## The tracker

```bash
python scripts/tracker.py add --company Acme --role "Backend dev" --link https://... --fit 78
python scripts/tracker.py update 1 --status applied     # sets a follow-up date 7 days out
python scripts/tracker.py list --status applied
python scripts/tracker.py due                           # applications that need a follow-up
```

Statuses: `saved`, `applied`, `interviewing`, `offer`, `rejected`, `withdrawn`.

## Tips

* The better your `achievements.md` (real stories with real numbers), the better the letters. Generic input gives generic output.
* Keep one summary variant per kind of role in your master CV (for example web, infrastructure, games) and let Claude pick.
* Read every letter before sending. You are the one signing it.

## Development

```bash
pip install pytest ruff
ruff check . && pytest
```

## License

MIT, see [LICENSE](LICENSE). Copyright (c) 2026 Carlos Ducamp.
