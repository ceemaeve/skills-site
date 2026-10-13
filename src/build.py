# Builds the Skill Training Completed site from data.json and resources.json.
#   python3 src/build.py   (from the repo root, or from src/)
# Writes index.html, calendar.html, resources.html, 404.html, og.png, robots.txt, sitemap.xml and the icon files into ../site/
import json, html, os, shutil
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'site')
os.makedirs(OUT, exist_ok=True)
data = json.load(open(os.path.join(HERE, 'data.json')))
e = html.escape
byid = {s['id']: s for s in data['sprints']}
byid.update({g['id']: g for g in data['gates']})

def weeks(track):
    return sum(byid[i]['weeks'] for i in track['items'])

cards = ''
for t in data['tracks']:
    cards += ('<div class="card"><span class="k">Track %s</span><h3>%s</h3><p>%s</p>'
              '<div class="meta"><b>%d weeks</b> at 8 hours a week &middot; for: %s</div>'
              '<a class="go" href="calendar.html?track=%s">Plan this track</a></div>\n'
              % (e(t['id']), e(t['name']), e(t['blurb']), weeks(t), e(t['fit']), e(t['id'])))
rows = ''
for s in data['sprints']:
    rows += ('<div class="sprint"><span class="id">%s</span><span class="nm">%s</span><span class="wk">%d weeks</span>'
             '<span class="oc">%s</span></div>\n' % (e(s['id']), e(s['name']), s['weeks'], e(s['outcome'])))
chips = ''.join('<span class="chip">%s</span>' % e(c) for c in data['certs'])
css = open(os.path.join(HERE, 'shared.css')).read()

def fill(s):
    return (s.replace('__SHARED_CSS__', css).replace('__KIT_URL__', e(data['kitUrl'])).replace('__HOME_URL__', e(data['homeUrl']))
             .replace('__TRACK_CARDS__', cards).replace('__SPRINT_ROWS__', rows).replace('__CERT_CHIPS__', chips))

# Resources page, from resources.json
res = json.load(open(os.path.join(HERE, 'resources.json')))

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

ms_learn = ms_udemy = comptia = ''
for x in res['microsoft']:
    tip = '<p class="tip">%s</p>' % e(x['note']) if x.get('note') else ''
    ms_learn += ('<div class="card"><span class="k">%s</span><h3>%s</h3>%s<h4>Official pages</h4>%s<h4>Learning paths</h4>%s</div>\n'
                 % (e(x['exam']), e(x['name']), tip, linklist(x['links']), linklist(x['paths'])))
    tip = '<p class="tip">%s</p>' % e(x['udemyNote']) if x.get('udemyNote') else ''
    ms_udemy += ('<div class="card"><span class="k">%s</span><h3>%s</h3>%s%s</div>\n'
                 % (e(x['exam']), e(x['name']), tip, udemy(x['udemy'])))
for x in res['comptia']:
    tip = '<p class="tip">%s</p>' % e(x['note']) if x.get('note') else ''
    t, by, url = x['book']
    comptia += ('<div class="card"><span class="k">%s</span><h3>CompTIA %s</h3>%s'
                '<h4>Official exam page</h4>%s'
                '<h4>Sybex study guide</h4><div class="book"><ul class="links"><li><span>%s<span class="by">%s &middot; on Amazon</span></span></li></ul></div>'
                '<h4>Udemy</h4>%s</div>\n'
                % (e(x['code']), e(x['exam']), tip, linklist([['CompTIA %s (%s)' % (x['exam'], x['code']), x['page']]]),
                   ext(url, t), e(by), udemy(x['udemy'])))

idx = fill(open(os.path.join(HERE, 'index.src.html')).read())
resp = (fill(open(os.path.join(HERE, 'resources.src.html')).read()).replace('__MS_LEARN__', ms_learn)
        .replace('__MS_UDEMY__', ms_udemy).replace('__COMPTIA__', comptia).replace('__CHECKED__', e(res['checked'])))
open(os.path.join(OUT, 'resources.html'), 'w').write(resp)
cal = fill(open(os.path.join(HERE, 'calendar.src.html')).read()).replace('__DATA__', json.dumps(data, ensure_ascii=False).replace('</', '<\\/'))
open(os.path.join(OUT, 'index.html'), 'w').write(idx)
open(os.path.join(OUT, 'calendar.html'), 'w').write(cal)
open(os.path.join(OUT, '404.html'), 'w').write(fill(open(os.path.join(HERE, '404.src.html')).read()))
for f in ('favicon.png', 'favicon.ico', 'apple-touch-icon.png', 'og.png', 'robots.txt', 'sitemap.xml'):
    shutil.copy(os.path.join(HERE, f), os.path.join(OUT, f))
print('ok', len(idx), len(cal))
