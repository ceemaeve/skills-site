# Builds the Skill Training Completed site from data.json.
#   python3 src/build.py   (from the repo root, or from src/)
# Writes index.html, calendar.html, 404.html, og.png, robots.txt, sitemap.xml and the icon files into ../site/
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

idx = fill(open(os.path.join(HERE, 'index.src.html')).read())
cal = fill(open(os.path.join(HERE, 'calendar.src.html')).read()).replace('__DATA__', json.dumps(data, ensure_ascii=False).replace('</', '<\\/'))
open(os.path.join(OUT, 'index.html'), 'w').write(idx)
open(os.path.join(OUT, 'calendar.html'), 'w').write(cal)
open(os.path.join(OUT, '404.html'), 'w').write(fill(open(os.path.join(HERE, '404.src.html')).read()))
for f in ('favicon.png', 'favicon.ico', 'apple-touch-icon.png', 'og.png', 'robots.txt', 'sitemap.xml'):
    shutil.copy(os.path.join(HERE, f), os.path.join(OUT, f))
print('ok', len(idx), len(cal))
