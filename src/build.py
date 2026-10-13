# Builds the Skill Training Completed site from data.json and resources.json.
#   python3 src/build.py   (from the repo root, or from src/)
# Writes index.html, calendar.html, resources.html, 404.html, fonts/, og.png, robots.txt, sitemap.xml and the icon files into ../site/
import json, html, os, shutil
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'site')
os.makedirs(OUT, exist_ok=True)
data = json.load(open(os.path.join(HERE, 'data.json'), encoding='utf-8'))
e = html.escape
byid = {s['id']: s for s in data['sprints']}
byid.update({g['id']: g for g in data['gates']})

def weeks(track):
    return sum(byid[i]['weeks'] for i in track['items'])

cards = ''
for t in data['tracks']:
    cards += ('<div class="card"><span class="k">Track %s</span><h3>%s</h3><p>%s</p>'
              '<div class="meta"><b>%d weeks</b> &middot; for: %s</div>'
              '<a class="go" href="calendar.html?track=%s">Plan this track</a></div>\n'
              % (e(t['id']), e(t['name']), e(t['blurb']), weeks(t), e(t['fit']), e(t['id'])))
rows = ''
for s in data['sprints']:
    rows += ('<div class="sprint"><span class="id">%s</span><span class="nm">%s</span><span class="wk">%d weeks</span>'
             '<span class="oc">%s</span></div>\n' % (e(s['id']), e(s['name']), s['weeks'], e(s['outcome'])))
chips = ''.join('<li><b>%s</b><span>%s</span></li>' % (e(c['name']), e(c['what'])) for c in data['certs'])
css = open(os.path.join(HERE, 'shared.css'), encoding='utf-8').read()

def fill(s):
    return (s.replace('__SHARED_CSS__', css).replace('__KIT_URL__', e(data['kitUrl'])).replace('__HOME_URL__', e(data['homeUrl']))
             .replace('__TRACK_CARDS__', cards).replace('__SPRINT_ROWS__', rows).replace('__CERT_CHIPS__', chips))

# Resources page, from resources.json
res = json.load(open(os.path.join(HERE, 'resources.json'), encoding='utf-8'))

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

ms_learn = ms_udemy = ''
for x in res['microsoft']:
    ms_learn += ('<div class="card"><span class="k">%s</span><h3>%s</h3>%s<h4>Official pages</h4>%s<h4>Learning paths</h4>%s</div>\n'
                 % (e(x['exam']), e(x['name']), tip(x.get('note')), linklist(x['links']), linklist(x['paths'])))
    ms_udemy += ('<div class="card"><span class="k">%s</span><h3>%s</h3>%s%s</div>\n'
                 % (e(x['exam']), e(x['name']), tip(x.get('udemyNote')), udemy(x['udemy'])))

def exam_card(x):
    out = '<div class="card"><span class="k">%s</span><h3>%s</h3>%s' % (e(x['code']), e(x['title']), tip(x.get('note')))
    out += '<h4>Official pages</h4>%s' % linklist(x['official'])
    if x.get('free'):
        out += '<h4>Free study material</h4>%s' % linklist(x['free'])
    out += '<h4>Sybex study guide</h4>'
    if x.get('book'):
        t, by, url = x['book']
        out += ('<div class="book"><ul class="links"><li><span>%s<span class="by">%s &middot; on Amazon</span></span></li></ul></div>'
                % (ext(url, t), e(by)))
    out += tip(x.get('bookNote'))
    out += '<h4>Udemy</h4>%s%s</div>\n' % (tip(x.get('udemyNote')), udemy(x['udemy']))
    return out

comptia = ''.join(exam_card(x) for x in res['comptia'])
foundation = ''.join(exam_card(x) for x in res['foundation'])
lpi = ''.join(exam_card(x) for x in res['lpi'])
cisco = ''.join(exam_card(x) for x in res['cisco'])

idx = fill(open(os.path.join(HERE, 'index.src.html'), encoding='utf-8').read())
resp = (fill(open(os.path.join(HERE, 'resources.src.html'), encoding='utf-8').read()).replace('__MS_LEARN__', ms_learn)
        .replace('__MS_UDEMY__', ms_udemy).replace('__COMPTIA__', comptia).replace('__FOUNDATION__', foundation).replace('__LPI__', lpi).replace('__CISCO__', cisco).replace('__CHECKED__', e(res['checked'])))
open(os.path.join(OUT, 'resources.html'), 'w', encoding='utf-8').write(resp)
cal = fill(open(os.path.join(HERE, 'calendar.src.html'), encoding='utf-8').read()).replace('__DATA__', json.dumps(data, ensure_ascii=False).replace('</', '<\\/'))
open(os.path.join(OUT, 'index.html'), 'w', encoding='utf-8').write(idx)
open(os.path.join(OUT, 'calendar.html'), 'w', encoding='utf-8').write(cal)
open(os.path.join(OUT, '404.html'), 'w', encoding='utf-8').write(fill(open(os.path.join(HERE, '404.src.html'), encoding='utf-8').read()))
for f in ('favicon.png', 'favicon.ico', 'apple-touch-icon.png', 'og.png', 'robots.txt', 'sitemap.xml'):
    shutil.copy(os.path.join(HERE, f), os.path.join(OUT, f))
shutil.copytree(os.path.join(HERE, 'fonts', 'web'), os.path.join(OUT, 'fonts'), dirs_exist_ok=True)

# Check: no template placeholder may survive into a page.
import re
for page in ('index.html', 'calendar.html', 'resources.html', '404.html'):
    left = re.findall(r'__[A-Z_]+__', open(os.path.join(OUT, page), encoding='utf-8').read())
    assert not left, '%s still has %s' % (page, sorted(set(left)))
print('ok', len(idx), len(cal))
