# Assessment

Skills are shown by doing, so every sprint ends with a "prove it" deliverable. Exams are optional gates on top of that.

## Proficiency levels

| Level | Name | Meaning |
| --- | --- | --- |
| 0 | Not started | Never done it |
| 1 | Guided | Can do it by following instructions |
| 2 | Independent | Can do it without notes and fix common problems |
| 3 | Can teach | Can explain why, handle unusual cases and coach someone else |

Aim for level 2 on every sprint before you move on, and level 3 on the areas your role depends on.

## Sprint check (peer review)

A teammate or study partner reviews your deliverable with these questions. All must be yes to mark the sprint done. Studying alone? Find a study partner in the [Discussions](https://github.com/ceemaeve/skills-site/discussions), or run the self-check below.

1. Does it work when someone else follows the steps?
2. Is every setting justified, not just copied?
3. Is there evidence (screenshots, logs, command output)?
4. Did you break it on purpose and fix it at least once?
5. Is anything sensitive (passwords, keys) kept out of the repo?

## No study partner? Run the check yourself

A self-check is weaker than a second pair of eyes. It still catches most gaps, and it keeps you moving until you find a partner.

1. Wait a day after you finish the deliverable.
2. Rebuild it from your own written steps, on a fresh VM or a snapshot from before the sprint. Where you get stuck, your steps are incomplete. Fix them.
3. Answer the five sprint-check questions in writing, one line each, with the evidence (screenshot, log or command output) next to each answer.
4. Optional: give Claude the deliverable and the five questions and ask what a reviewer would flag. Check anything it says against the official documentation before you act on it, because Claude can be wrong.
5. Mark the sprint done when all five answers are yes. Post the deliverable in [Discussions](https://github.com/ceemaeve/skills-site/discussions) if you want a second reviewer.

## Exam readiness checklist

Before booking a certification exam:

- Every sprint mapped to that exam is at level 2 or higher.
- You scored well on official or reputable practice assessments twice, taken at least a few days apart. Microsoft Learn offers free practice assessments for its exams. A common working target is 80% or better, but treat that as a rule of thumb, not an official figure.
- You reviewed every domain where you scored lowest and redid the related lab.
- You know the exam format and passing score (see CERT-NOTES.md and the official page).

Don't book the exam until all four are true. Then book it and keep the review week.

## Capstone rubric (S13)

Score each 0 to 3. Passing is 2 or higher on every line.

| Area | What a 2 looks like |
| --- | --- |
| Design | Diagram and document match what was built |
| Identity and access | Least privilege, documented delegation, no shared admin accounts |
| Network and services | Documented addressing, DNS and DHCP working across both sites |
| Security | Baseline applied, findings from a scan fixed, evidence kept |
| Monitoring and recovery | Alerts firing, one restore tested end to end |
| Automation | At least half of the build repeatable from code in Git |
| Communication | A teammate can run the runbook cold. Walkthrough is clear and on time |

## Skills-only track evidence

If someone is not sitting exams, the peer-reviewed deliverables and the capstone are their record. Keep them in your repo under `deliverables/<name>/<sprint>/`.
