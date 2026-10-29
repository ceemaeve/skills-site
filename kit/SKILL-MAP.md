# Skill map

The curriculum is organized by skill, not by certification. Each skill area is taught once, and the certs that test it are listed here. That's where the overlap comes from.

**Key:** ● primary topic for that exam, ◐ partly covered, ○ light mention, blank = not covered.

This is a judgment call based on the official outlines and study guides read on 2026-09-29 (AZ-802, AZ-104, Cloud+ CV0-004, Linux+ XK0-006, LPIC-1/2/3 topic lists). The Security+ column follows the V8 (SY0-801) objectives, checked on 2026-10-13. The SecAI+ marks follow the CY0-001 objectives, read on 2026-10-21; they are the same kind of judgment call.

| Skill area | Sprint | AZ-802 | AZ-104 | Cloud+ | Sec+ | Linux+ | LPIC-1 | LPIC-2 | LPIC-3 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Networking and name resolution | S1 | ● | ● | ◐ | ◐ | ◐ | ◐ | ● | ○ |
| Identity, directory services and access | S2 | ● | ● | ◐ | ◐ | ◐ | ◐ | ○ | ◐ (Mixed Env.) |
| Hybrid identity and governance | S3 | ◐ | ● | ◐ | ○ | | | | |
| Compute and virtualization | S4 | ◐ | ● | ◐ | | ◐ | ○ | ○ | ● (305) |
| Storage and file services | S5 | ● | ● | ◐ | | ◐ | ◐ | ● | ◐ (306) |
| Security and hardening | S6 | ◐ | ○ | ● | ● | ◐ | ◐ | ◐ | ◐ (303) |
| Monitoring, backup, troubleshooting | S7 | ● | ◐ | ◐ | ◐ | ● | ○ | ◐ | ◐ |
| Automation and infrastructure as code | S8 | ○ | ◐ | ◐ | ◐ | ● | ◐ | ○ | ○ |
| Cloud architecture and operations | S9 | ○ | ◐ | ● | ◐ | ○ | | | |
| Linux services and advanced admin | S10 | | | | | ◐ | ◐ | ● | ◐ |
| Security operations, governance, risk | S11 | | | ○ | ● | | | | ○ |
| Containers, virtualization, HA | S12 | | | ◐ | ○ | ◐ | | | ● (305/306) |

**Foundations sprint (Tracks F and E)**

| Skill area | Sprint | Network+ |
| --- | --- | --- |
| Networking fundamentals | F2 | ● |

Network+ also overlaps the core path: S1 (networking and name resolution) and S6 (security and hardening) go deeper on the same topics.

**Networking (Track G)**

| Skill area | Sprint | CCNA |
| --- | --- | --- |
| Networking fundamentals | F2 | ◐ |
| Networking and name resolution | S1 | ◐ |
| Cisco routing and switching | N1 | ● |

**AWS (Track H)**

| Skill area | Sprint | AWS SAA |
| --- | --- | --- |
| Networking and name resolution | S1 | ◐ |
| Cloud architecture and operations | S9 | ◐ |
| AWS core services | A1 | ● |

**Copilot (P1 in Tracks A, B, D, E and J; P2 and P3 for Tracks B and J)**

| Skill area | Sprint | AB-900 | GH-300 |
| --- | --- | --- | --- |
| Copilot basics | P1 | ○ | ○ |
| Identity and directory services | S2 | ◐ | |
| Hybrid identity and governance | S3 | ◐ | |
| Security and hardening | S6 | ◐ | |
| Automation and infrastructure as code | S8 | | ◐ |
| Copilot and agent administration | P2 | ● | |
| GitHub Copilot for scripts | P3 | | ● |

**AI security (Track K)**

| Skill area | Sprint | Sec+ | SecAI+ |
| --- | --- | --- | --- |
| Networking and name resolution | S1 | ◐ | ○ |
| Identity, directory services and access | S2 | ◐ | ◐ |
| Security and hardening | S6 | ● | ◐ |
| Monitoring, backup, troubleshooting | S7 | ◐ | ◐ |
| Security operations, governance, risk | S11 | ● | ◐ |
| AI security | X1 | ○ | ● |

**Claude (C1 in every track; C2 and C3 for Track I)**

The Claude sprints don't map to an exam. They support every other sprint: C1 makes Claude a study partner you check, C2 helps with the scripts in S8 and S10, and C3 turns a lab chore into a Skill.

## How to read it

- A skill area with several filled or half-filled marks is where one sprint pays off across multiple exams. Networking, identity, storage and security are the biggest.
- LPIC-3 has four specialties. You take only one, so the LPIC-3 column shows the specialty that fits each area. Pick yours by S12.
- Linux content is not one block. Each sprint from S1 to S8 has a short "Linux lane" so the Linux skills build up alongside the Windows and Azure ones. S10 and S12 then go deeper.

## Suggested emphasis by exam (from published domain weights)

- **AB-900:** Microsoft 365 core features and objects 30–35%, data protection and governance for Microsoft 365 and Copilot 35–40%, Copilot and agent administration 25–30%.
- **GH-300:** use GitHub Copilot responsibly 15–20%, GitHub Copilot features 25–30%, data and architecture 10–15%, prompt engineering and context crafting 10–15%, developer productivity 10–15%, privacy, content exclusions and safeguards 10–15%.
- **AWS Solutions Architect – Associate SAA-C03:** secure architectures 30%, resilient architectures 26%, high-performing architectures 24%, cost-optimized architectures 20%.
- **CCNA 200-301 v2.0:** infrastructure and connectivity 25%, switching and network access 25%, IP routing 20%, network services and security 20%, AI and network operations 10%.
- **Network+ N10-009:** troubleshooting 24%, concepts 23%, implementation 20%, operations 19%, security 14%.

- **AZ-802:** AD DS 20-25%, storage 15-20%, monitor/troubleshoot 15-20%, hybrid management, VMs, networking, security 10-15% each.
- **AZ-104:** identity/governance 20-25%, compute 20-25%, storage 15-20%, networking 15-20%, monitor/backup 10-15%.
- **Cloud+ CV0-004:** architecture 23%, deployment 19%, security 19%, operations 17%, troubleshooting 12%, DevOps fundamentals 10%.
- **Security+ SY0-801 (V8):** security operations 27%, threats, vulnerabilities and attacks 24%, security architecture 19%, general security concepts 16%, program management and oversight 14%.
- **SecAI+ CY0-001:** securing AI systems 40%, AI-assisted security 24%, AI governance, risk and compliance 19%, basic AI concepts related to cybersecurity 17%.
- **Linux+ XK0-006:** system management 23%, troubleshooting 22%, services and user management 20%, security 18%, automation 17%.
