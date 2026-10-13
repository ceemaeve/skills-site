# Build checks: each case copies src/ to a scratch dir, applies one mutation, runs build.py with SRC_DIR
# pointing at the copy, and checks the exit code and message.
#   python3 tests/test_build_checks.py
import json, os, shutil, subprocess, sys, tempfile
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')

def run(mutate):
    tmp = tempfile.mkdtemp()
    try:
        src = os.path.join(tmp, 'src')
        shutil.copytree(os.path.join(ROOT, 'src'), src)
        files = {}
        for name in ('data', 'resources'):
            files[name] = json.load(open(os.path.join(src, name + '.json'), encoding='utf-8'))
        mutate(files['data'], files['resources'])
        for name, obj in files.items():
            json.dump(obj, open(os.path.join(src, name + '.json'), 'w', encoding='utf-8'), ensure_ascii=False)
        p = subprocess.run([sys.executable, os.path.join(ROOT, 'src', 'build.py')], env=dict(os.environ, SRC_DIR=src),
                           capture_output=True, text=True)
        return p.returncode, p.stdout + p.stderr
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
def m_http(d, r):
    d['kitUrl'] = 'http://example.com'

CASES = [
    ('unknown_track_item', m_track_item, 1, 'data.json: track C: unknown item "S99"'),
    ('gate_missing_cost', m_cost, 1, 'gate g802: no cost'),
    ('bad_res', m_res, 1, 'gate gsec: no Resources card "nope"'),
    ('bad_res_in_list', m_res_list, 1, 'gate glinux: no Resources card "nope"'),
    ('tool_unknown_sprint', m_tool, 1, 'tool tool-vmware: unknown sprint "S99"'),
    ('chooser_unknown_track', m_chooser_track, 1, 'chooser: unknown track "Z"'),
    ('empty_chooser', m_chooser_empty, 1, 'chooser: empty'),
    ('http_link', m_http, 1, 'not https'),
    ('clean_build', lambda d, r: None, 0, 'ok'),
]

failed = 0
for name, mutate, code, text in CASES:
    got, out = run(mutate)
    good = got == code and text in out
    failed += not good
    print('%s %s' % ('PASS' if good else 'FAIL', name))
    if not good:
        print('  expected exit %d containing %r, got exit %d:\n  %s' % (code, text, got, out.strip().replace('\n', '\n  ')[-400:]))
sys.exit(1 if failed else 0)
