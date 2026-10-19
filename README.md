# skills-site

Source for the Skill Training Completed website at **https://skills.thisevelife.space** (skilltrainingcompleted.dev and www redirect there). Public repo. Pushing to `main` builds the site and deploys it to TEL-SVS-01.

Moved here from the private `tel-sites` repo (`src/site-skills/`, last commit there 3fa4dfc) on 2026-10-09. The first build was checked byte-for-byte against the live site.

## Layout

| Path | What it is |
|---|---|
| `src/data.json` | Sprints, gates, tracks, certs and the links the pages use (`kitUrl`, `homeUrl`) |
| `src/resources.json` | Study links on the Resources page (Microsoft Learn, CompTIA, Cisco, LPI, Sybex, Udemy) and the date they were checked |
| `src/*.src.html`, `src/shared.css` | Page templates |
| `src/build.py` | Writes the site into `site/` (index, calendar, resources, 404, one page per sprint in `sprints/`, fonts, og.png, robots.txt, sitemap.xml, icons) |
| `src/sprint.src.html` | Template for the sprint pages; their text comes from the kit's SPRINTS.md |
| `src/make_og.py` | Remakes `src/og.png` (needs Pillow and the fonts it names; run by hand, not in the deploy) |
| `tests/test_build_checks.py` | Proves each build check stops bad data: breaks a scratch copy of `src/` once per check and expects the right message |
| `site/` | Build output. Not committed; the deploy builds it fresh |
| `.github/workflows/deploy.yml` | Builds, then syncs `site/` to `/var/www/skills` |

## Change the site

1. Edit `src/data.json` or a template. Never edit `site/` by hand.
2. Check it: clone the kit next to this repo (`git clone https://github.com/ceemaeve/skill-training-completed ../skill-training-completed`), run `python3 src/build.py` (prints `ok` and the page count), then open `site/index.html`.
3. Run `python3 tests/test_build_checks.py` before you push. Every line must say PASS.
4. Commit and push to `main`. The Deploy workflow does the rest (Actions tab shows it).

Who owns which files, and the checklists for routine changes, are in the ceema.dev project doc `claude/SKILLS-SITE-HANDOFF.md`.

## Rules

1. **Two repos.** The public repo https://github.com/ceemaeve/skill-training-completed is the download kit (the training .md files people give to their own Claude). The sprint pages are built from its SPRINTS.md: the deploy checks out the kit, and a daily run picks up kit edits. Everything else on the site comes from this repo. The server never reads either repo. Each sprint in `src/data.json` must have a heading `## <id>. <name> (<weeks> weeks)` in the kit, or the build fails.
2. **Own folder.** The deploy owns `/var/www/skills` only and deletes anything the build no longer makes. Its `DEPLOY_PATH` secret must be exactly `/var/www/skills`; the workflow refuses anything else.
3. **Caddy lives with the server.** The site's Caddy file is written by `deploy/setup-server.sh` in ceemaeve/ceema-dev (`/etc/caddy/sites/skills.caddy`). Change it there.

## Deploy secrets

Settings > Secrets and variables > Actions: `DEPLOY_HOST`, `DEPLOY_USER`, `DEPLOY_PATH` (`/var/www/skills`), `DEPLOY_SSH_KEY`, `DEPLOY_KNOWN_HOSTS`. The server's `setup-server.sh base` stage prints all five.
