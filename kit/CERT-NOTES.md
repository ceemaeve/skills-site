# Certification notes

Last checked: 2026-10-13 (SecAI+ added 2026-10-21). The study order lives in [SPRINTS.md](SPRINTS.md); this file holds exam facts and sources. Exam versions and retirement dates change, so re-check the official pages before booking any exam.

## Assumptions (change these and the dates move)

- About 8 hours per week: roughly 3 hours reading or video, 4 hours hands-on lab, 1 hour practice questions.
- Lab host: A host with 32GB RAM (about 16GB with every VM on), an SSD with about 500GB free, and VMware Workstation. Nested Hyper-V is out of scope for this lab. See [LAB-ENVIRONMENT.md](LAB-ENVIRONMENT.md).
- Hours per cert are rough planning numbers, not Microsoft, CompTIA or LPI figures.

## The certifications

| Cert | Exam(s) | Format | Notes |
| --- | --- | --- | --- |
| CompTIA A+ (Foundations) | 220-1201 (Core 1), 220-1202 (Core 2) | 90 min, max 90 questions each; pass 675 (Core 1), 700 (Core 2) | V15, launched Mar 2025, estimated 2028 retirement. Both exams needed, in any order. Added 2026-10-13 |
| Cisco CCNA (Networking) | 200-301 | 120 min, $300 | v1.1 until Feb 2, 2027; v2.0 from Feb 3, 2027 (same code). No prerequisites. Valid 3 years. Added 2026-10-13 |
| AWS Certified Solutions Architect – Associate (AWS) | SAA-C03 | 130 min, 65 questions (50 scored), pass 720, $150 | No new version announced (checked 2026-10-13). AWS recommends a year of hands-on AWS design work; no prerequisite. Valid 3 years. Added 2026-10-13 |
| Microsoft 365 Certified: Copilot and Agent Administration Fundamentals (Copilot) | AB-900 | $99 | Skills list updated October 14, 2026. Free practice assessment on Microsoft Learn. Added 2026-10-13 |
| GitHub Copilot (Copilot) | GH-300 | $99, pass 700 | Valid 2 years. Free practice assessment on Microsoft Learn. Skills list current as of August 7, 2026. Added 2026-10-13 |
| CompTIA Network+ (Foundations) | N10-009 | 90 min, max 90 questions, pass 720 | V9, launched Jun 20, 2024, estimated 2027 retirement. Added 2026-10-13 |
| Microsoft AZ-802, Administering Windows Server | AZ-802 | Pass mark 700 | AD DS 20-25%, storage 15-20%, monitor/troubleshoot 15-20%, hybrid mgmt, VMs, networking, security 10-15% each |
| Microsoft AZ-104, Azure Administrator | AZ-104 | Pass mark 700 | Identity/governance 20-25%, compute 20-25%, storage 15-20%, networking 15-20%, monitor/backup 10-15% |
| CompTIA Cloud+ | CV0-004 | 90 min, max 90 questions, pass 750 | Released Sep 2024. CompTIA lists an estimated 2027 retirement, so do it earlier |
| CompTIA Security+ | SY0-701 (V7) until June 11, 2027; SY0-801 (V8) from Nov 17, 2026 | 90 min, max 90 questions, pass 750 | V8 adds an AI threats objective and AI in security automation, and shifts weight from program management (20% to 14%) to general concepts (12% to 16%) |
| CompTIA SecAI+ (AI security) | CY0-001 (V1) | 60 min, max 60 questions (multiple-choice and performance-based), pass 600 on a scale of 100 to 900 | Launched Feb 17, 2026; CompTIA lists an estimated retirement 3 years later. CompTIA's first expansion exam: it adds to Security+, CySA+ or PenTest+. Recommended: 3 to 4 years in IT and 2+ years of hands-on security. Exam price $298 (CompTIA store, checked 2026-10-21). Renewal terms aren't on CompTIA's pages either; a training provider lists a 3-year cycle through CompTIA CE, so confirm before you rely on it. Added 2026-10-21 |
| CompTIA Linux+ | XK0-006 | 90 min, max 90 questions, pass 720 | Released Jul 2025. Estimated 2028 retirement |
| LPIC-1 | 101-500, 102-500 | 90 min, 60 questions each | No prerequisite. Valid 5 years |
| LPIC-2 | 201-450, 202-450 | 90 min, 60 questions each | Requires an active LPIC-1 |
| LPIC-3 | 300, 303, 305 or 306 | One specialty of four | Pick one specialty. Requires an active LPIC-2; confirm on lpi.org |

Note: some older study plans mention LPIC 1-4. LPI has no LPIC-4. LPIC-3 has four specialties: Mixed Environments (300), Security (303), Virtualization and Containerization (305), High Availability and Storage Clusters (306). 303 and 305 fit best with the rest of this plan.

## Security+ V7 or V8

V8 (SY0-801) replaces V7 on November 17, 2026, and V7 (SY0-701) retires on June 11, 2027. Study V8 unless you will sit the exam before that date.

## Overlap map

- **AZ-802 and AZ-104:** Entra ID, Azure Files, Azure VMs, storage, monitoring, backup.
- **AZ-104 and Cloud+:** cloud concepts, networking, storage, deployment, security.
- **Cloud+ and Security+:** cloud security, IAM, logging and monitoring.
- **Security+ and SecAI+:** access control, encryption, logging and monitoring, risk and governance. SecAI+ adds the AI-specific threats and controls.
- **Linux+ and LPIC-1:** shell, packages, filesystems, users, services, networking, scripting.
- **LPIC-2 and LPIC-3:** services, networking and security depth on Linux.

## Lab plan

The VM layout, networks and snapshot rules are in [LAB-ENVIRONMENT.md](LAB-ENVIRONMENT.md). Run only what the current sprint needs and suspend the rest.

## Weekly rhythm

- **Week 1 of each topic:** read the official skills outline, then video or course for the topic.
- **Middle weeks:** hands-on lab tied to each skills-measured bullet. Write down every step you did.
- **Last 2 weeks before an exam:** practice exams, review weak domains, book the exam.
- **Rule:** a topic isn't done until you can do it in the lab without notes.

## Sources

- [CompTIA A+](https://www.comptia.org/en-us/certifications/a/)
- [CompTIA Network+](https://www.comptia.org/en-us/certifications/network/)
- [Cisco CCNA](https://www.cisco.com/site/us/en/learn/training-certifications/certifications/enterprise/ccna/index.html) and [CCNA v2.0 exam topics](https://learningnetwork.cisco.com/s/ccna-v2-exam-topics)
- [AB-900 certification](https://learn.microsoft.com/en-us/credentials/certifications/copilot-and-agent-administration-fundamentals/) and [study guide](https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/ab-900)
- [GH-300 certification](https://learn.microsoft.com/en-us/credentials/certifications/github-copilot/) and [study guide](https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/gh-300)
- [AWS Certified Solutions Architect – Associate](https://aws.amazon.com/certification/certified-solutions-architect-associate/) and [SAA-C03 exam guide](https://docs.aws.amazon.com/aws-certification/latest/solutions-architect-associate-03/solutions-architect-associate-03.html)
- [AZ-802 study guide](https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/az-802)
- [AZ-104 study guide](https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/az-104)
- [CompTIA Security+](https://www.comptia.org/en-us/certifications/security/)
- [CompTIA SecAI+](https://www.comptia.org/en-us/certifications/secai/) and [CY0-001 exam objectives](https://lecbyo.files.cmp.optimizely.com/download/4ac9eb6a529711f0b35e3e002873e549)
- [CompTIA Linux+](https://www.comptia.org/en-us/certifications/linux/)
- [CompTIA Cloud+](https://www.comptia.org/en-us/certifications/cloud/)
- [LPIC-1](https://www.lpi.org/our-certifications/lpic-1-overview/), [LPIC-2](https://www.lpi.org/our-certifications/lpic-2-overview/), [LPIC-3](https://www.lpi.org/our-certifications/lpic-3-overview/)
