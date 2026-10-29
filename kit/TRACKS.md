# Team tracks

The sprints are the same for everyone. What changes is which parts a person does and whether they sit exams.

Every track starts with C1, Claude basics (2 weeks, see SPRINTS.md). Tracks B, C, F, G and H then take P1, Copilot basics (2 weeks). The weeks below include them.

## Track A: Claude

For anyone who wants to use Claude well in IT work, on its own or next to another track.

- Do C1, S0, C2 and C3 (see SPRINTS.md). S0 teaches the command line and Git that C2 needs.
- No exam. Claude Academy courses give completion certificates; the "prove it" deliverables are your record.
- C2 needs a paid Claude plan or an Anthropic Console account. C1 and C3 work on the free plan.
- About 8 weeks at 8 hours per week.
- On another track already? Add C2 and C3 after S0 (4 weeks).

## Track B: Foundations (Claude, Copilot, Network+)

For people new to IT, or moving into IT from another kind of work.

- Do C1, P1 and F2 (see SPRINTS.md). C1 comes first because Claude is your study partner for everything after it.
- You do not need Git in this track. Keep each deliverable in a folder with screenshots and a short notes file. S0 teaches Git.
- Sit Network+ after F2.
- About 10 weeks at 8 hours per week.
- Then pick D, E, G, H or J, or carry on with S0.

## Track C: Copilot (AB-900, GH-300)

For IT people asked to roll out or support Microsoft 365 Copilot, and for anyone who scripts with GitHub Copilot.

- Do C1, P1, S0, S1, S2, S3, S6, P2 and P3 (see SPRINTS.md). S1 to S3 and S6 give P2 the identity and security groundwork it needs.
- Sit AB-900 after P2 and GH-300 after P3.
- P2 needs a one-month Microsoft 365 Business free trial (card required; cancel before it ends). P3 works on GitHub Copilot Free.
- About 26 weeks at 8 hours per week.
- On Track H already? It includes P2 and AB-900; add P3 and GH-300 (3 weeks) for GitHub Copilot.

## Track D: Networking (CCNA)

For network administration, network operations center (NOC) and network support roles.

- Do F2, S0, S1 and N1 (see SPRINTS.md). S0 builds the lab that S1 needs.
- Sit CCNA after N1. Network+ after F2 is optional.
- About 17 weeks at 8 hours per week.
- New to IT? Do Track B first, then go straight to S0.

## Track E: AWS (Solutions Architect – Associate)

For cloud jobs on AWS.

- Do S0, S1, S9 and A1 (see SPRINTS.md). S0 builds the lab that S1 needs.
- In S9, skip lab 3 (it needs the file server from S5) and lab 5 (Azure cost alerts; A1 lab 1 does the AWS version). In lab 2, use AWS as the second cloud.
- Sit AWS Solutions Architect – Associate after A1.
- About 16 weeks at 8 hours per week.
- New to IT? Do Track B first, then go straight to S0.

## Track F: Skills only (no exams)

For people who want the capability without the certificate.

- Do every sprint's labs and its "prove it" deliverable.
- Skip the exam gates and their review weeks. That saves about 10 weeks.
- New to IT? Do the F2 labs first, still without the exam.
- Skip S9 (cloud architecture) and S11 (security operations) if they don't apply to the role, and jump to S13 with a smaller capstone.
- About 48 weeks at 8 hours per week (42 if you skip S9 and S11).
- Assessment is by peer review of the deliverables using the rubric in ASSESSMENT.md.

## Track G: Security-focused

- Do S0 through S2, S6, S7, S9, S11 and the capstone with a security emphasis. S9 adds cloud security context.
- Sit Cloud+ after S9 and Security+ after S11.
- About 30 weeks at 8 hours per week (26 if you skip S9 and Cloud+).

## Track H: Microsoft (AZ-802, AZ-104)

- Do S0 through S8, including the Linux lanes at reduced depth (one lab per sprint is enough).
- Sit AZ-802 after S7 and AZ-104 after S8.
- Then P2 (Copilot and agent administration) and AB-900. Microsoft 365 admins are the people who roll Copilot out.
- About 37 weeks at 8 hours per week.

## Track I: AI security (Security+, SecAI+)

For security staff who now have to secure AI systems or use AI in their security work.

- Do C1, S0, S1, S2, S6, S7, S11 and X1 (see SPRINTS.md). S1, S2, S6, S7 and S11 give X1 the networking, identity, hardening, logging and risk groundwork it assumes.
- Sit Security+ after S11 and SecAI+ after X1. SecAI+ adds to Security+, CySA+ or PenTest+ and is not meant as a first security exam.
- Security+ V8 (SY0-801) replaces V7 on November 17, 2026. Study V8 unless you will sit the exam before that date.
- X1 runs a small open AI model on the lab host with Ollama. Everything else works on free plans.
- About 26 weeks at 8 hours per week.
- On Track G already? It has the groundwork and Security+. Add X1 and SecAI+ (5 weeks).

## Track J: Linux (Linux+, LPIC-1, LPIC-2, LPIC-3)

- Do S0, S1, S2, S5, S6, S7 and S8 with the Linux lane as the main lab and the Windows lab as reference.
- Then S10, S12 and the capstone (S13).
- Sit Linux+ and LPIC-1 after S10, LPIC-2 after S12, LPIC-3 after the capstone.
- About 40 weeks at 8 hours per week.

## Choosing

| If your role is mostly... | Start with track |
| --- | --- |
| New to IT, or help desk and desktop support | B, then D, E, G, H or J |
| Network administration or a NOC | D (Track B first if new to IT) |
| Windows and Microsoft 365 administration | H |
| Linux server administration | J |
| Cloud engineering on Azure | H, then S9 and Cloud+ |
| Cloud engineering on AWS | E |
| Security or compliance | G |
| Securing AI systems, or using AI in security work | I (or G, then add X1) |
| Not interested in exams | F, with the other track's sprints as a guide |
| Using Claude well in IT work | A, on its own or next to another track |
| Rolling out or supporting Copilot | C (H if you also want the Windows Server and Azure exams) |

## Working as a team

- Pair up on the fault lab (S7) and the tabletop (S11): one breaks, one fixes.
- Review each other's "prove it" deliverables before anyone moves on.
- Keep deliverables in your team repo under `deliverables/<name>/<sprint>/`.
- Hold a 20-minute demo at the end of each sprint, one person presenting.
