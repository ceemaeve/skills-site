# Lab environment

Host: A host with 32GB RAM (about 16GB with every VM on), an SSD with about 500GB free, and VMware Workstation. Nested Hyper-V is out of scope, so any lab that needs a hypervisor inside a VM is done as reading and light configuration only.

## Networks

| VMware network | Type | Subnet | Purpose |
| --- | --- | --- | --- |
| VMnet10 | Host-only | 10.10.10.0/24 | "Corp" site |
| VMnet11 | Host-only | 10.10.20.0/24 | "Branch" site |
| VMnet8 | NAT | (VMware default) | Internet access, used only by RTR1 |

Turn off the VMware DHCP service on VMnet10 and VMnet11. DHCP is something you build in S1.

## Virtual machines

| VM | OS | RAM | Network | Address | Role |
| --- | --- | --- | --- | --- | --- |
| RTR1 | Debian | 1GB | VMnet10, VMnet11, VMnet8 | .1 on each lab network | Router, NAT, firewall practice |
| DC1 | Windows Server | 2GB | VMnet10 | 10.10.10.10 | Domain controller, corp site |
| DC2 | Windows Server | 2GB | VMnet11 | 10.10.20.10 | Domain controller, branch site |
| SRV1 | Windows Server | 3GB | VMnet10 | 10.10.10.20 | File, DNS, DHCP, Windows Admin Center |
| CL1 | Windows 11 | 4GB | VMnet10 | DHCP | Client |
| LNX1 | Debian or Ubuntu | 2GB | VMnet10 | 10.10.10.30 | Linux service host |
| LNX2 | Rocky or AlmaLinux | 2GB | VMnet10 | 10.10.10.31 | RHEL-family practice |

All VMs on at once is about 16GB, which leaves headroom on a 32GB host. In practice, run only what the current sprint needs and suspend the rest.

Use evaluation editions of Windows Server and Windows 11 from the Microsoft Evaluation Center. Check their current time limits, and use snapshots so an expired evaluation is a rebuild, not a disaster.

## Foundations lab (Track F)

Track F needs less than the full lab:

- Cisco Packet Tracer and Wireshark, both free.
- Your home router, read-only: look, screenshot, change nothing you can't put back.

## Cisco lab (Track G)

- Cisco Packet Tracer, free with a Cisco Networking Academy account. It covers most N1 labs.
- Cisco Modeling Labs Free, up to five nodes with real IOS images, for RESTCONF and anything Packet Tracer can't do. It runs as a VM on the lab host. Check Cisco's CML Free install guide for the memory it needs, and suspend the Windows VMs while it runs.

## AI security lab (Track K)

- One small open AI model run with Ollama on the lab host, for X1. Small models need no GPU but answer slowly. Check Ollama's current system requirements and the memory each model needs, and suspend the Windows VMs while it runs.
- LNX1 for the gateway script and the logs, and your S11 log setup for the detection rules.
- A few made-up documents for the model to answer questions about. Never real company or personal data.

## Naming

- Domain name for the lab: use a name that is not your real production domain, for example `corp.test`. `.test` is reserved for testing and will never resolve on the internet.
- For S3 (hybrid identity) add a UPN suffix on a domain you own, because Entra sync needs a routable, verified domain.
- VM names are as in the table. Keep them short and lowercase in scripts.

## Snapshots

Take a snapshot at each of these points and name it clearly:

1. `clean-install` after the OS is installed and updated.
2. `pre-<sprint>` before each sprint's first lab.
3. `post-<sprint>` when the "prove it" deliverable is done.

Delete old snapshots regularly. A long snapshot chain slows the disk and eats space.

## Azure sandbox rules

1. Use a free account. Set a budget alert before creating anything.
2. Put every lab in its own resource group named `rg-<sprint>-<name>`.
3. Tag everything with `owner` and `sprint`.
4. Delete the resource group when the lab is finished. Don't leave VMs running overnight.
5. Never put real credentials, personal data or production settings in the lab.
6. Do not link the lab tenant to your employer's or any production tenant.

## AWS sandbox rules (Track H)

1. Use a new AWS account of your own. Check the current Free Tier terms when you sign up, because they change.
2. Put MFA on the root user, then sign in with an IAM Identity Center user instead.
3. Set a budget alert before creating anything.
4. Tag everything with `owner` and `sprint`.
5. Delete what you build when the lab is finished. NAT gateways, load balancers and RDS bill by the hour.
6. Never put real credentials, personal data or production settings in the lab, and do not link the account to your employer's AWS organization.

## Claude rules (C1 to C3)

1. Use your own Claude account. Never sign in with an employer's account for lab work.
2. Never paste a password, key, token, or real company or personal data into a chat or a CLAUDE.md. Use placeholders.
3. Run Claude Code only inside your lab repo, on the lab host or a lab VM, and take a snapshot before it runs anything new.
4. Read every change and command before you approve it. You own what it does.
5. Check answers against the official docs before they go in a deliverable, and say where Claude helped.

## Copilot rules (P1 to P3)

1. Use your own Microsoft and GitHub accounts. Never use an employer's tenant or organization for lab work.
2. For P2, create a new tenant with a Microsoft 365 Business free trial. It needs a card and becomes a paid subscription unless you cancel, so put the end date in your calendar and cancel before it.
3. Use test users and made-up sample files only. Never real names, ID numbers or company data.
4. Don't link a payment method for pay-as-you-go agents. Reading how billing works is enough.
5. Never paste a password, key or token into a prompt, and keep secrets out of the scripts repo.

## AI security rules (X1)

1. Attack only the application you built in your own lab. Never run prompt injection, jailbreaks or any other test against a system you don't own or don't have written permission to test.
2. Use made-up data only: fake names, fake ID numbers, fake keys.
3. Keep API keys and secrets out of prompts, logs and scripts.
4. Treat every model answer as untrusted input, including answers about itself.
5. Check what an AI assistant tells you about a log against the log, and say where it helped.

## Backups of the lab itself

- Copy your VM folders or export the key VMs (DC1, SRV1, LNX1) to an external drive after major milestones.
- Keep scripts and documents in your own Git repo. Never commit passwords, keys or tokens.

## Ground rules for the team

- Each person builds their own lab. Sharing one lab hides the mistakes that teach the most.
- Use throwaway passwords in the lab and never reuse them anywhere else.
- Write down every fix you make. Those notes become the runbooks.
