# Build checks: each case copies src/ to a scratch dir, applies one mutation, runs build.py with SRC_DIR
# pointing at the copy, and checks the exit code and message.
#   python3 tests/test_build_checks.py
import json, os, shutil, subprocess, sys, tempfile
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')

def run(mutate, raw=None, tpl=None):
    tmp = tempfile.mkdtemp()
    try:
        src = os.path.join(tmp, 'src')
        shutil.copytree(os.path.join(ROOT, 'src'), src)
        # An old site/ with one marker file: a failed build must leave it exactly as it was.
        os.makedirs(os.path.join(tmp, 'site'))
        open(os.path.join(tmp, 'site', 'keep.txt'), 'w').close()
        if tpl:
            tpl(src)
        files = {}
        for name in ('data', 'resources'):
            files[name] = json.load(open(os.path.join(src, name + '.json'), encoding='utf-8'))
        mutate(files['data'], files['resources'])
        for name, obj in files.items():
            json.dump(obj, open(os.path.join(src, name + '.json'), 'w', encoding='utf-8'), ensure_ascii=False)
        if raw:
            with open(os.path.join(src, 'data.json'), 'a', encoding='utf-8') as f:
                f.write(raw)
        p = subprocess.run([sys.executable, os.path.join(ROOT, 'src', 'build.py')], env=dict(os.environ, SRC_DIR=src),
                           capture_output=True, text=True)
        site = os.path.join(tmp, 'site')
        listing = sorted(os.listdir(site)) if os.path.isdir(site) else None
        pages = {f: open(os.path.join(site, f), encoding='utf-8').read() for f in ('index.html', 'resources.html', 'calendar.html')
                 if listing and f in listing}
        return p.returncode, p.stdout + p.stderr, listing, pages
    finally:
        shutil.rmtree(tmp)

def gate(d, gid):
    return next(g for g in d['gates'] if g['id'] == gid)

def m_track_item(d, r):
    next(t for t in d['tracks'] if t['id'] == 'C')['items'].append('S99')
def m_cost(d, r):
    del gate(d, 'g802')['cost']
def m_res(d, r):
    gate(d, 'gsec')['res'] = 'nope'
def m_res_list(d, r):
    gate(d, 'glinux')['res'] = ['linux-plus', 'nope']
def m_tool(d, r):
    r['tools'][0]['sprints'].append('S99')
def m_chooser_track(d, r):
    d['chooser'] = [{'label': 'x', 'track': 'Z'}]
def m_chooser_empty(d, r):
    d['chooser'] = []
def m_no_chooser(d, r):
    del d['chooser']
def m_no_notice(d, r):
    del d['notice']
def m_entry_no_track(d, r):
    del d['chooser'][0]['track']
def m_no_res(d, r):
    del gate(d, 'gsec')['res']
def m_no_sprints(d, r):
    del r['tools'][0]['sprints']
def m_item_obj(d, r):
    next(t for t in d['tracks'] if t['id'] == 'C')['items'].append({'x': 1})
def m_no_anchor(d, r):
    del r['tools'][0]['anchor']
def m_http(d, r):
    d['kitUrl'] = 'http://example.com'

def m_json_syntax(d, r):
    pass
def m_cost_text(d, r):
    gate(d, 'g802')['cost'] = '$300'
def m_sprint_weeks(d, r):
    d['sprints'][0]['weeks'] = '3'
def m_no_exam(d, r):
    del r['comptia'][0]['exam']
def m_dup_anchor(d, r):
    r['tools'][0]['anchor'] = r['comptia'][0]['anchor']
def m_chooser_str(d, r):
    d['chooser'] = 'x'
def m_sprint_no_id(d, r):
    del d['sprints'][0]['id']
def m_gate_no_id(d, r):
    del d['gates'][0]['id']
def m_track_no_id(d, r):
    del d['tracks'][0]['id']
def m_dup_id(d, r):
    d['gates'][0]['id'] = d['sprints'][0]['id']
def m_sprint_bad_id(d, r):
    d['sprints'][0]['id'] = 'Z1'
def m_res_nested(d, r):
    gate(d, 'glinux')['res'] = [['linux-plus']]
def m_tool_nested(d, r):
    r['tools'][0]['sprints'].append(['S1'])
def m_ftp(d, r):
    d['kitUrl'] = 'ftp://example.com'
def m_js(d, r):
    r['tools'][0]['links'][0][1] = 'javascript:alert(1)'
def m_kit_heading(d, r):
    d['sprints'][0]['name'] += ' renamed'
def m_aws(d, r):
    # An AWS card, a gate pointing into the aws group, and an A sprint (with a stand-in kit heading).
    card = json.loads(json.dumps(r['cisco'][0]))
    card.update(anchor='aws-test', exam='AWS Test', code='TEST-01', title='Test card')
    r.setdefault('aws', []).append(card)  # added next to any real AWS cards
    gate(d, 'gccna')['res'] = 'aws-test'
def m_aws_sprint_no_kit(d, r):
    d['sprints'].append({'id': 'A99', 'name': 'AWS', 'weeks': 3, 'outcome': 'x'})  # an id the real data never uses
def m_claude_sprint_no_kit(d, r):
    d['sprints'].append({'id': 'C99', 'name': 'Claude', 'weeks': 2, 'outcome': 'x'})  # an id the real data never uses
def m_copilot(d, r):
    # A Copilot card next to any real ones, and a gate pointing at it.
    card = json.loads(json.dumps(r['cisco'][0]))
    card.update(anchor='copilot-test', exam='Copilot Test', code='TEST-02', title='Test card')
    r.setdefault('copilot', []).append(card)
    gate(d, 'gccna')['res'] = 'copilot-test'
def m_copilot_sprint_no_kit(d, r):
    d['sprints'].append({'id': 'P99', 'name': 'Copilot', 'weeks': 2, 'outcome': 'x'})  # an id the real data never uses
def t_placeholder(src):
    with open(os.path.join(src, '404.src.html'), 'a', encoding='utf-8') as f:
        f.write('__LEFT_OVER__')

# Facts from the real data, so the cases pass before and after content changes (AWS, new sprints).
REAL = json.load(open(os.path.join(ROOT, 'src', 'data.json'), encoding='utf-8'))
REAL_RES = json.load(open(os.path.join(ROOT, 'src', 'resources.json'), encoding='utf-8'))
PAGES = 'ok %d pages' % (5 + len(REAL['sprints']))  # 5 main pages plus one per sprint
HAS_AWS_CARDS = bool(REAL_RES.get('aws'))
HAS_A_SPRINTS = any(s['id'].startswith('A') for s in REAL['sprints'])
HAS_C_SPRINTS = any(s['id'].startswith('C') for s in REAL['sprints'])
HAS_P_SPRINTS = any(s['id'].startswith('P') for s in REAL['sprints'])
HAS_COPILOT_CARDS = bool(REAL_RES.get('copilot'))

CASES = [
    ('unknown_track_item', m_track_item, 1, 'data.json: track C: unknown item "S99"'),
    ('gate_missing_cost', m_cost, 1, 'gate g802: no cost'),
    ('bad_res', m_res, 1, 'gate gsec: no Resources card "nope"'),
    ('bad_res_in_list', m_res_list, 1, 'gate glinux: no Resources card "nope"'),
    ('tool_unknown_sprint', m_tool, 1, 'tool tool-vmware: unknown sprint "S99"'),
    ('chooser_unknown_track', m_chooser_track, 1, 'chooser: unknown track "Z"'),
    ('empty_chooser', m_chooser_empty, 1, 'chooser: empty'),
    ('chooser_missing', m_no_chooser, 1, 'data.json: chooser: missing'),
    ('notice_missing', m_no_notice, 1, 'data.json: notice: missing'),
    ('chooser_entry_missing_track', m_entry_no_track, 1, 'chooser[0]: missing track'),
    ('gate_missing_res', m_no_res, 1, 'gate gsec: missing res'),
    ('tool_missing_sprints', m_no_sprints, 1, 'tool tool-vmware: missing sprints'),
    ('track_item_not_string', m_item_obj, 1, 'track C: invalid item'),
    ('tool_missing_anchor', m_no_anchor, 1, 'missing anchor'),
    ('http_link', m_http, 1, 'not https'),
    ('json_syntax', m_json_syntax, 1, 'data.json: line '),
    ('gate_cost_text', m_cost_text, 1, 'data.json: gate g802: cost must be a number'),
    ('sprint_weeks_text', m_sprint_weeks, 1, 'data.json: sprint F1: weeks must be a number'),
    ('card_missing_exam', m_no_exam, 1, 'resources.json: comptia 0: missing exam'),
    ('duplicate_anchor', m_dup_anchor, 1, 'resources.json: duplicate anchor'),
    ('chooser_not_list', m_chooser_str, 1, 'data.json: chooser: must be a list'),
    ('sprint_missing_id', m_sprint_no_id, 1, 'data.json: sprints 0: missing id'),
    ('gate_missing_id', m_gate_no_id, 1, 'data.json: gates 0: missing id'),
    ('track_missing_id', m_track_no_id, 1, 'data.json: tracks 0: missing id'),
    ('duplicate_id', m_dup_id, 1, 'data.json: duplicate id "F1"'),
    ('sprint_id_letter', m_sprint_bad_id, 1, 'data.json: sprint Z1: id must be a group letter (C, P, F, S, N, A, X) and a number'),
    ('aws_sprint_reaches_kit_check', m_aws_sprint_no_kit, 1, 'data.json: sprint A99: kit SPRINTS.md has no heading "## A99. AWS (3 weeks)"'),
    ('aws_gate_res', m_aws, 0, PAGES),
    ('copilot_gate_res', m_copilot, 0, PAGES),
    ('copilot_sprint_reaches_kit_check', m_copilot_sprint_no_kit, 1, 'data.json: sprint P99: kit SPRINTS.md has no heading "## P99. Copilot (2 weeks)"'),
    ('claude_sprint_reaches_kit_check', m_claude_sprint_no_kit, 1, 'data.json: sprint C99: kit SPRINTS.md has no heading "## C99. Claude (2 weeks)"'),
    ('res_nested_list', m_res_nested, 1, 'data.json: gate glinux: invalid res'),
    ('tool_sprints_nested', m_tool_nested, 1, 'resources.json: tool tool-vmware: invalid sprint'),
    ('ftp_link', m_ftp, 1, 'data.json: kitUrl: not https: ftp://'),
    ('javascript_link', m_js, 1, 'not https: javascript:'),
    ('kit_heading', m_kit_heading, 1, 'data.json: sprint F1: kit SPRINTS.md has no heading "## F1. '),
    ('placeholder_left', lambda d, r: None, 1, '404.html still has __LEFT_OVER__'),
    ('clean_build', lambda d, r: None, 0, PAGES),
]

failed = 0
for name, mutate, code, text in CASES:
    got, out, site, pages = run(mutate, ',' if name == 'json_syntax' else None, t_placeholder if name == 'placeholder_left' else None)
    good = got == code and text in out and 'Traceback' not in out
    # Failure: the old site/ is untouched. Success: site/ is replaced by the new build.
    if code:
        good = good and site == ['keep.txt']
    else:
        good = good and site is not None and 'keep.txt' not in site and 'index.html' in site
        rp = pages.get('resources.html', '')
        if name == 'aws_gate_res':
            # The AWS section, its card, its jump button and the meta description all appear, and the calendar knows the exam name.
            good = good and '<section id="aws">' in rp and 'id="aws-test"' in rp and 'href="#aws"' in rp and 'CCNA, AWS SAA,' in rp \
                and 'Cisco, AWS' in rp and '<!--aws' not in rp and '"aws-test": "AWS Test"' in pages.get('calendar.html', '')
        if name == 'clean_build':
            # The AWS section shows exactly when there are AWS cards; the AWS sprint group exactly when there are A sprints.
            good = good and '<!--aws' not in rp and (('<section id="aws">' in rp and 'href="#aws"' in rp and 'CCNA, AWS SAA,' in rp)
                if HAS_AWS_CARDS else ('id="aws"' not in rp and 'href="#aws"' not in rp and 'AWS SAA' not in rp))
            good = good and (('>AWS <small>' in pages.get('index.html', '')) == HAS_A_SPRINTS)
            good = good and (('>Claude <small>' in pages.get('index.html', '')) == HAS_C_SPRINTS)
            good = good and (('>Copilot <small>' in pages.get('index.html', '')) == HAS_P_SPRINTS)
            good = good and '<!--copilot' not in rp and ((('<section id="copilot">' in rp and 'href="#copilot"' in rp and 'AB-900, GH-300,' in rp)
                if HAS_COPILOT_CARDS else ('id="copilot"' not in rp and 'href="#copilot"' not in rp and 'GH-300' not in rp)))
        if name == 'copilot_gate_res':
            good = good and '<section id="copilot">' in rp and 'id="copilot-test"' in rp and 'href="#copilot"' in rp \
                and 'AB-900, GH-300, Cloud+' in rp and ', GitHub and LPI' in rp and '<!--copilot' not in rp \
                and '"copilot-test": "Copilot Test"' in pages.get('calendar.html', '')
    failed += not good
    print('%s %s' % ('PASS' if good else 'FAIL', name))
    if not good:
        print('  expected exit %d containing %r, got exit %d, site/ %s:\n  %s' % (code, text, got, site, out.strip().replace('\n', '\n  ')[-400:]))
sys.exit(1 if failed else 0)
