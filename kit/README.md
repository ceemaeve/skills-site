# Skill Training Completed: study kit

A skills-first study path from IT basics through Windows Server, Azure, AWS, Linux, Cisco networking, cloud, security and AI security, with Claude as a study partner you check and Microsoft Copilot from basics to administration. It is built around a VMware Workstation home lab. Certifications are optional gates along the way, not the structure. Written for a small team, and usable on your own.

Site and calendar: https://skills.thisevelife.space, part of [thisevelife.space](https://thisevelife.space)

This folder is the download kit. The website offers it as a ZIP and builds its sprint pages from `SPRINTS.md`.

## What's here

| File | What it's for |
| --- | --- |
| [SKILL-MAP.md](SKILL-MAP.md) | Which skill areas each certification tests. This is where the overlap is |
| [SPRINTS.md](SPRINTS.md) | The 24 sprints (3 Claude, 3 Copilot, 1 Foundations, 14 core, 1 Cisco networking, 1 AWS, 1 AI security), with labs, deliverables and exam gates |
| [TRACKS.md](TRACKS.md) | Paths for different roles, including skills-only |
| [LAB-ENVIRONMENT.md](LAB-ENVIRONMENT.md) | VM layout, networks, snapshots, Azure and AWS sandbox rules, Claude and Copilot rules |
| [ASSESSMENT.md](ASSESSMENT.md) | Proficiency levels, peer review and exam readiness |
| [PROGRESS-TEMPLATE.md](PROGRESS-TEMPLATE.md) | Copy this to track your own progress |
| [CERT-NOTES.md](CERT-NOTES.md) | Exam facts as checked on 2026-10-13 (SecAI+ on 2026-10-21) |

## Certifications covered

CompTIA Network+ (Foundations), Cisco CCNA (Networking), AWS Certified Solutions Architect – Associate (AWS), Microsoft AZ-802, AZ-104 and AB-900, GitHub Copilot GH-300, CompTIA Cloud+, Security+, SecAI+ and Linux+, and LPIC-1, 2 and 3. Exam versions change, so re-check the official pages before booking.

## How to use it

1. Pick a track in TRACKS.md.
2. Build the lab in LAB-ENVIRONMENT.md (sprint S0). Track F starts smaller, with the Foundations lab in F2.
3. Work through the sprints in order. Finish each "prove it" deliverable and get a peer review. No study partner yet? Find one in [Discussions](https://github.com/ceemaeve/skills-site/discussions), or run the self-check in ASSESSMENT.md.
4. Track your own progress in a copy of PROGRESS-TEMPLATE.md.
5. Book an exam only when you meet the readiness checklist in ASSESSMENT.md.

## Using it with your own Claude

Download the ZIP from https://skills.thisevelife.space and add them to a Claude Project as knowledge, or put them in a folder you work from with Claude. Ask Claude to coach you through one sprint at a time, check your "prove it" deliverables against the sprint, and re-verify exam facts against the official pages before you book.

## Rules

- Never commit passwords, keys, tokens or personal data. Use throwaway credentials in the lab.
- Keep deliverables in `deliverables/<name>/<sprint>/`. Before S0 that is a plain folder on your computer with screenshots and notes. You need Git only once S0 teaches it.
- Fix errors or outdated facts in these files with a normal commit and say what you changed.
