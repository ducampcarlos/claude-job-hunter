---
name: interview
description: Prepare for an interview using a job folder under jobs/. Researches the company from public sources and builds likely questions with answers drawn only from the candidate's real profile.
---

# /interview

Input: the path of a folder in `jobs/` (or the company name).

Follow `CLAUDE.md`.

1. Read `job.md`, `analysis.md` and the profile files in that folder and in `profile/`.
2. Research the company from public sources (site, blog, public repos, recent news). Note only what you can cite; say "not found" otherwise.
3. Write `jobs/<folder>/interview-prep.md` with:
   - **Company snapshot:** what they do, size/stage if public, recent news, 3 facts worth mentioning.
   - **Likely questions** (technical, behavioural, role-specific), each with a suggested answer built from a real story in `achievements.md`, in STAR form (situation, task, action, result).
   - **Gaps to prepare for:** each `GAP` from the analysis with an honest way to address it ("I haven't used X in production; I have done Y, which is similar because...").
   - **Questions to ask them** (5, specific to the company).
   - **Logistics checklist.**
4. Never put invented achievements in the suggested answers.
