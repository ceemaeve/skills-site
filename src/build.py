# Builds the Skill Training Completed site from data.json, resources.json and the study kit's SPRINTS.md.
#   python3 src/build.py   (from the repo root, or from src/)
# Needs the kit (ceemaeve/skill-training-completed) checked out at ../kit (the deploy does this),
# next to this repo as ../../skill-training-completed, or at $KIT_DIR.
# Writes index.html, calendar.html, resources.html, 404.html, sprints/, fonts/, og.png, robots.txt,
# sitemap.xml and the icon files into ../site/
import json, html, os, re, shutil, sys
SCRIPT = os.path.dirname(os.path.abspath(__file__))
# $SRC_DIR (tests) reads the src files from there and writes to <SRC_DIR>/../site, never the repo's own site/.
HERE = os.environ.get('SRC_DIR') or SCRIPT
OUT = os.path.join(HERE, '..', 'site')
def load_json(name):
    try:
        return json.load(open(os.path.join(HERE, name), encoding='utf-8'))
    except json.JSONDecodeError as ex:
        print('%s: line %d column %d: %s' % (name, ex.lineno, ex.colno, ex.msg))
        sys.exit(1)
data = load_json('data.json')
res = load_json('resources.json')

def validate(data, res):
    # Returns error strings as "<file>: <where>: <problem>".
    errs = []
    sprints = {s['id'] for s in data['sprints']}
    gates = {g['id'] for g in data['gates']}
    tracks = {t['id'] for t in data['tracks']}
    anchors = set()
    for k in ('microsoft', 'foundation', 'comptia', 'lpi', 'cisco', 'tools'):
        for n, x in enumerate(res.get(k, [])):
            if isinstance(x.get('anchor'), str):
                if x['anchor'] in anchors:
                    errs.append('resources.json: duplicate anchor "%s"' % x['anchor'])
                anchors.add(x['anchor'])
            else:
                errs.append('resources.json: %s %s: missing anchor' % (k, n))
            if k != 'tools' and not (isinstance(x.get('exam'), str) and x['exam']):
                errs.append('resources.json: %s %s: missing exam' % (k, n))
    for s in data['sprints']:
        if not isinstance(s.get('weeks'), int) or isinstance(s.get('weeks'), bool):
            errs.append('data.json: sprint %s: weeks must be a number' % s['id'])
    for t in data['tracks']:
        for i in t['items']:
            if not isinstance(i, str):
                errs.append('data.json: track %s: invalid item %r' % (t['id'], i))
            elif i not in sprints | gates:
                errs.append('data.json: track %s: unknown item "%s"' % (t['id'], i))
    for g in data['gates']:
        if 'cost' not in g:
            errs.append('data.json: gate %s: no cost' % g['id'])
        elif not isinstance(g['cost'], (int, float)) or isinstance(g['cost'], bool):
            errs.append('data.json: gate %s: cost must be a number' % g['id'])
        if not isinstance(g.get('weeks'), int) or isinstance(g.get('weeks'), bool):
            errs.append('data.json: gate %s: weeks must be a number' % g['id'])
        r = g.get('res')
        if r is None:
            errs.append('data.json: gate %s: missing res' % g['id'])
        elif not isinstance(r, (str, list)):
            errs.append('data.json: gate %s: invalid res %r' % (g['id'], r))
        else:
            for a in [r] if isinstance(r, str) else r:
                if a not in anchors:
                    errs.append('data.json: gate %s: no Resources card "%s"' % (g['id'], a))
    for t in res['tools']:
        where = 'tool %s' % t.get('anchor', '?')
        if not isinstance(t.get('sprints'), list):
            errs.append('resources.json: %s: missing sprints' % where)
            continue
        for i in t['sprints']:
            if i not in sprints:
                errs.append('resources.json: %s: unknown sprint "%s"' % (where, i))
    ch = data.get('chooser')
    if ch is None:
        errs.append('data.json: chooser: missing')
    elif not isinstance(ch, list):
        errs.append('data.json: chooser: must be a list')
    elif not ch:
        errs.append('data.json: chooser: empty')
    else:
        for n, c in enumerate(ch):
            ok = True
            for f in ('track', 'label'):
                if not isinstance(c, dict) or not isinstance(c.get(f), str) or not c[f]:
                    errs.append('data.json: chooser[%d]: missing %s' % (n, f))
                    ok = False
            if ok and c['track'] not in tracks:
                errs.append('data.json: chooser: unknown track "%s"' % c['track'])
    nt = data.get('notice')
    if nt is None:
        errs.append('data.json: notice: missing')
    elif not isinstance(nt, str) or not nt:
        errs.append('data.json: notice: invalid')
    def walk(x, file, where):
        if isinstance(x, str):
            if x.startswith('http://'):
                errs.append('%s: %s: not https: %s' % (file, where, x))
        elif isinstance(x, dict):
            for k, v in x.items():
                walk(v, file, '%s.%s' % (where, k) if where else k)
        elif isinstance(x, list):
            for n, v in enumerate(x):
                walk(v, file, '%s[%d]' % (where, n))
    walk(data, 'data.json', '')
    walk(res, 'resources.json', '')
    return errs

errors = validate(data, res)
if errors:
    print('\n'.join(errors))
    sys.exit(1)
os.makedirs(os.path.join(OUT, 'sprints'), exist_ok=True)
e = html.escape
byid = {s['id']: s for s in data['sprints']}
byid.update({g['id']: g for g in data['gates']})
SITE = 'https://skills.ceema.dev/'

# --- The kit's SPRINTS.md: one section per sprint
kit_dirs = [os.environ.get('KIT_DIR', ''), os.path.join(SCRIPT, '..', 'kit'), os.path.join(SCRIPT, '..', '..', 'skill-training-completed')]
kit_md = next((os.path.join(d, 'SPRINTS.md') for d in kit_dirs if d and os.path.exists(os.path.join(d, 'SPRINTS.md'))), None)
if not kit_md:
    raise SystemExit('Study kit not found. Clone ceemaeve/skill-training-completed next to this repo, or set KIT_DIR.')
sections = {}
for part in re.split(r'\n(?=## )', open(kit_md, encoding='utf-8').read()):
    m = re.match(r'## ([FSN]\d+)\. ', part)
    if m:
        sections[m.group(1)] = part.split('\n---')[0]

def inline(text):
    text = e(text, quote=False)
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
    text = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text)
    # Kit file names (ASSESSMENT.md, LAB-ENVIRONMENT.md) link to the file on GitHub.
    return re.sub(r'\b([A-Z][A-Z-]+\.md)\b', lambda m: '<a href="%s/blob/main/%s">%s</a>' % (data['kitUrl'], m.group(1), m.group(1)), text)

def md_to_html(md):
    # The kit's sprint sections use paragraphs, **bold**, `code` and numbered lists only.
    out, items = [], []
    def flush():
        if items:
            out.append('<ol>%s</ol>' % ''.join('<li>%s</li>' % inline(i) for i in items))
            items.clear()
    for line in md.split('\n')[1:]:
        line = line.rstrip()
        m = re.match(r'\d+\. (.*)', line)
        if m:
            items.append(m.group(1))
            continue
        flush()
        if not line:
            continue
        if line.startswith('**Gate:'):
            out.append('<p class="gate">%s</p>' % inline(line))
        elif re.fullmatch(r'\*\*[^*]+\*\*', line):
            out.append('<h2>%s</h2>' % e(line.strip('*')))
        else:
            out.append('<p>%s</p>' % inline(line))
    flush()
    return '\n'.join(out)

def kit_anchor(s):
    head = '%s. %s (%d weeks)' % (s['id'], s['name'], s['weeks'])
    return data['kitUrl'] + '/blob/main/SPRINTS.md#' + re.sub(r'[^a-z0-9 -]', '', head.lower()).replace(' ', '-')

for s in data['sprints']:
    head = '## %s. %s (%d weeks)' % (s['id'], s['name'], s['weeks'])
    assert s['id'] in sections and sections[s['id']].startswith(head), 'kit SPRINTS.md has no heading "%s"' % head
    s['doc'] = 'sprints/%s.html' % s['id'].lower()

def weeks(track):
    return sum(byid[i]['weeks'] for i in track['items'])

def exam_cost(track):
    return sum(byid[i].get('cost', 0) for i in track['items'] if track['gates'])

cards = ''
for t in data['tracks']:
    start = t['id'] == 'F'
    cost = exam_cost(t)
    cards += ('<div class="card%s" id="track-%s"><span class="k">Track %s%s</span><h3>%s</h3><p>%s</p>'
              '<div class="meta"><b>%d weeks</b>%s &middot; for: %s</div>'
              '<a class="go" href="calendar.html?track=%s">Plan this track</a></div>\n'
              % (' start' if start else '', e(t['id'].lower()), e(t['id']), ' &middot; start here if new to IT' if start else '',
                 e(t['name']), e(t['blurb']), weeks(t), ' &middot; exams about $%s' % format(cost, ',') if cost else '', e(t['fit']), e(t['id'])))
GROUPS = [('F', 'Foundations', 'F1 to F3, for people new to IT (Tracks F and E)'),
          ('S', 'Core sprints', 'S0 to S13, the shared lab and most of the exams'),
          ('N', 'Networking', 'N1, the Cisco sprint for Track G')]
rows = ''
for letter, title, sub in GROUPS:
    rows += '<h3 class="grp">%s <small>%s</small></h3>\n' % (e(title), e(sub))
    for s in data['sprints']:
        if s['id'][0] != letter:
            continue
        rows += ('<details class="sprint"><summary><span class="id">%s</span><span class="nm">%s</span><span class="wk">%d weeks</span></summary>'
                 '<p class="oc">%s</p><a class="doc" href="%s">Labs and deliverable</a></details>\n'
                 % (e(s['id']), e(s['name']), s['weeks'], e(s['outcome']), e(s['doc'])))
chips = ''.join('<li><b>%s</b><span>%s</span></li>' % (e(c['name']), e(c['what'])) for c in data['certs'])
css = open(os.path.join(HERE, 'shared.css'), encoding='utf-8').read()

def fill(s):
    return (s.replace('__SHARED_CSS__', css).replace('__KIT_URL__', e(data['kitUrl'])).replace('__ZIP_URL__', e(data['zipUrl']))
             .replace('__STUDY_URL__', e(data['studyUrl'])).replace('__HOME_URL__', e(data['homeUrl']))
             .replace('__TRACK_CARDS__', cards).replace('__SPRINT_ROWS__', rows).replace('__CERT_CHIPS__', chips))

# --- Resources data (the sprint pages list each sprint's lab tools)
def tools_for(sid):
    return [t for t in res['tools'] if sid in t['sprints']]

# --- Sprint pages
sprint_tpl = fill(open(os.path.join(HERE, 'sprint.src.html'), encoding='utf-8').read())
group_name = {g[0]: g[1] for g in GROUPS}
order = [s for letter, _, _ in GROUPS for s in data['sprints'] if s['id'][0] == letter]
for n, s in enumerate(order):
    tracks = ', '.join(t['id'] for t in data['tracks'] if s['id'] in t['items'])
    pager = ''
    if n:
        p = order[n - 1]
        pager += '<a class="prev" href="%s.html"><small>Previous</small>%s. %s</a>' % (p['id'].lower(), e(p['id']), e(p['name']))
    if n + 1 < len(order):
        p = order[n + 1]
        pager += '<a class="next" href="%s.html"><small>Next</small>%s. %s</a>' % (p['id'].lower(), e(p['id']), e(p['name']))
    page = (sprint_tpl.replace('__S_ID__', e(s['id'])).replace('__S_NAME__', e(s['name'])).replace('__S_OUTCOME__', e(s['outcome']))
            .replace('__S_SLUG__', s['id'].lower()).replace('__S_GROUP__', e(group_name[s['id'][0]])).replace('__S_WEEKS__', str(s['weeks']))
            .replace('__S_TOOLS__', ''.join('<li><a href="/resources.html#%s">%s</a></li>' % (e(t['anchor']), e(t['name'])) for t in tools_for(s['id'])) or '<li>Nothing beyond the lab from S0.</li>')
            .replace('__S_TRACKS__', e(tracks)).replace('__S_KIT__', e(kit_anchor(s))).replace('__S_PAGER__', pager)
            .replace('__S_BODY__', md_to_html(sections[s['id']])))
    open(os.path.join(OUT, 'sprints', '%s.html' % s['id'].lower()), 'w', encoding='utf-8').write(page)

# --- Resources page, from resources.json

def ext(url, text):
    return '<a href="%s" target="_blank" rel="noopener">%s</a>' % (e(url), e(text))

def linklist(pairs):
    return '<ul class="links">%s</ul>' % ''.join('<li>%s</li>' % ext(u, t) for t, u in pairs)

def udemy(courses):
    out = ''
    for c in courses:
        if 'rating' in c:
            r = '<span class="r">%.1f &#9733; &middot; %s ratings</span>' % (c['rating'], format(c['ratings'], ','))
        else:
            r = '<span class="r none">No ratings yet</span>'
        kind = ' &middot; %s' % e(c['note']) if c.get('note') and 'rating' in c else ''
        out += '<li><span>%s<span class="by">%s%s</span>%s</span></li>' % (ext(c['url'], c['title']), e(c['by']), kind, r)
    return '<ul class="links ol">%s</ul>' % out

def tip(text):
    return '<p class="tip">%s</p>' % e(text) if text else ''

def cost(x):
    return '<p class="cost"><b>Exam cost:</b> %s</p>' % e(x['cost']) if x.get('cost') else ''

def book(x):
    out = '<h4>Study guide</h4>'
    if x.get('book'):
        t, by, url, publisher, store = x['book']
        out += ('<div class="book"><ul class="links"><li><span>%s<span class="by">%s &middot; %s &middot; on %s</span></span></li></ul></div>'
                % (ext(url, t), e(by), e(publisher), e(store)))
    return out + tip(x.get('bookNote'))

def tool_card(t):
    used = ', '.join('<a href="sprints/%s.html">%s</a>' % (s.lower(), e(s)) for s in t['sprints'])
    return ('<div class="card" id="%s"><span class="k">Used in %s</span><h3>%s</h3>%s%s</div>\n'
            % (e(t['anchor']), used, e(t['name']), tip(t.get('note')), linklist(t['links'])))

ms_learn = ms_udemy = ''
for x in res['microsoft']:
    ms_learn += ('<div class="card" id="%s"><span class="k">%s</span><h3>%s</h3>%s%s<h4>Official pages</h4>%s<h4>Learning paths</h4>%s%s</div>\n'
                 % (e(x['anchor']), e(x['exam']), e(x['name']), cost(x), tip(x.get('note')), linklist(x['links']), linklist(x['paths']), book(x)))
    ms_udemy += ('<div class="card"><span class="k">%s</span><h3>%s</h3>%s%s</div>\n'
                 % (e(x['exam']), e(x['name']), tip(x.get('udemyNote')), udemy(x['udemy'])))

def exam_card(x):
    out = '<div class="card" id="%s"><span class="k">%s</span><h3>%s</h3>%s%s' % (e(x['anchor']), e(x['code']), e(x['title']), cost(x), tip(x.get('note')))
    out += '<h4>Official pages</h4>%s' % linklist(x['official'])
    if x.get('free'):
        out += '<h4>Free study material</h4>%s' % linklist(x['free'])
    out += book(x)
    out += '<h4>Udemy</h4>%s%s</div>\n' % (tip(x.get('udemyNote')), udemy(x['udemy']))
    return out

comptia = ''.join(exam_card(x) for x in res['comptia'])
foundation = ''.join(exam_card(x) for x in res['foundation'])
lpi = ''.join(exam_card(x) for x in res['lpi'])
cisco = ''.join(exam_card(x) for x in res['cisco'])
tools = ''.join(tool_card(t) for t in res['tools'])

chooser = '\n        '.join('<li><a href="calendar.html?track=%s">%s<b>Track %s</b></a></li>' % (e(c['track']), e(c['label']), e(c['track'])) for c in data['chooser'])
idx = fill(open(os.path.join(HERE, 'index.src.html'), encoding='utf-8').read()).replace('__CHOOSER__', chooser).replace('__NOTICE__', e(data['notice']))
resp = (fill(open(os.path.join(HERE, 'resources.src.html'), encoding='utf-8').read()).replace('__MS_LEARN__', ms_learn)
        .replace('__MS_UDEMY__', ms_udemy).replace('__COMPTIA__', comptia).replace('__FOUNDATION__', foundation).replace('__LPI__', lpi)
        .replace('__CISCO__', cisco).replace('__TOOLS__', tools).replace('__CHECKED__', e(res['checked'])).replace('__PRICES_CHECKED__', e(res['pricesChecked'])))
# The calendar labels two-exam gates (Linux+ and LPIC-1) with the Resources card's exam name.
data['resNames'] = {x['anchor']: x['exam'] for k in ('microsoft', 'foundation', 'comptia', 'lpi', 'cisco') for x in res[k]}
cal = fill(open(os.path.join(HERE, 'calendar.src.html'), encoding='utf-8').read()).replace('__DATA__', json.dumps(data, ensure_ascii=False).replace('</', '<\\/'))
open(os.path.join(OUT, 'index.html'), 'w', encoding='utf-8').write(idx)
open(os.path.join(OUT, 'resources.html'), 'w', encoding='utf-8').write(resp)
open(os.path.join(OUT, 'calendar.html'), 'w', encoding='utf-8').write(cal)
open(os.path.join(OUT, '404.html'), 'w', encoding='utf-8').write(fill(open(os.path.join(HERE, '404.src.html'), encoding='utf-8').read()))
for f in ('favicon.png', 'favicon.ico', 'apple-touch-icon.png', 'og.png', 'robots.txt'):
    shutil.copy(os.path.join(HERE, f), os.path.join(OUT, f))
shutil.copytree(os.path.join(HERE, 'fonts', 'web'), os.path.join(OUT, 'fonts'), dirs_exist_ok=True)

urls = ['', 'calendar.html', 'resources.html'] + [s['doc'] for s in order]
open(os.path.join(OUT, 'sitemap.xml'), 'w', encoding='utf-8').write(
    '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    + ''.join('  <url><loc>%s%s</loc></url>\n' % (SITE, u) for u in urls) + '</urlset>\n')

# Check: no template placeholder may survive into a page.
pages = ['index.html', 'calendar.html', 'resources.html', '404.html'] + [s['doc'] for s in order]
for page in pages:
    left = re.findall(r'__[A-Z_]+__', open(os.path.join(OUT, page), encoding='utf-8').read())
    assert not left, '%s still has %s' % (page, sorted(set(left)))
print('ok', len(pages), 'pages')
