#!/usr/bin/env python3
"""Merge per-cluster .bib fragments into one references.bib.

- Same key in several files  -> keep the longest (most complete) entry.
- Different keys, same work  -> detect via normalized title / DOI / arXiv id,
  keep the first-seen key as canonical, record aliases in bib_aliases.json.
Writes: references.bib, bib_aliases.json, bib_report.txt
"""
import re, glob, json, sys, collections

def parse_bib(text):
    entries = []
    i = 0
    n = len(text)
    while True:
        m = re.search(r'@(\w+)\s*\{\s*([^,\s]+)\s*,', text[i:])
        if not m:
            break
        start = i + m.start()
        etype, key = m.group(1), m.group(2)
        # brace matching
        depth = 0
        j = i + m.end() - 1  # position of '{' after @type
        j = text.index('{', start)
        k = j
        while k < n:
            c = text[k]
            if c == '{':
                depth += 1
            elif c == '}':
                depth -= 1
                if depth == 0:
                    break
            k += 1
        body = text[start:k+1]
        entries.append((etype.lower(), key, body))
        i = k + 1
    return entries

def field(body, name):
    m = re.search(r'\b' + name + r'\s*=\s*(\{(?:[^{}]|\{[^{}]*\})*\}|"[^"]*"|[^,\n]+)', body, re.I)
    if not m:
        return ''
    v = m.group(1).strip()
    v = v.strip('{}"').strip()
    return v

def norm_title(t):
    t = re.sub(r'\{|\}', '', t.lower())
    t = re.sub(r'[^a-z0-9 ]+', ' ', t)
    t = re.sub(r'\s+', ' ', t).strip()
    return t[:70]

files = sorted(glob.glob('bib/*.bib'))
by_key = collections.OrderedDict()
origin = {}
for f in files:
    for etype, key, body in parse_bib(open(f, encoding='utf-8').read()):
        if key in by_key:
            if len(body) > len(by_key[key][1]):
                by_key[key] = (etype, body)
                origin[key] = f
        else:
            by_key[key] = (etype, body)
            origin[key] = f

# duplicate-work detection -> union-find groups
parent = {k: k for k in by_key}
def find(k):
    while parent[k] != k:
        parent[k] = parent[parent[k]]
        k = parent[k]
    return k
def union(a, b):
    ra, rb = find(a), find(b)
    if ra != rb:
        parent[rb] = ra

seen_title = {}
seen_doi = {}
seen_arxiv = {}
NEVER_MERGE = {('apraamcos2024ai', 'goldmedia2024gemasacem')}
for key, (etype, body) in by_key.items():
    t = norm_title(field(body, 'title'))
    doi = field(body, 'doi').lower().replace('https://doi.org/', '')
    arx = field(body, 'eprint').lower()
    if not arx:
        m = re.search(r'arxiv\.org/abs/(\d{4}\.\d{4,5})', body)
        arx = m.group(1) if m else ''
    hit = None
    if doi and doi in seen_doi:
        hit = seen_doi[doi]
    elif arx and arx in seen_arxiv:
        hit = seen_arxiv[arx]
    elif t and len(t) > 25 and t in seen_title:
        hit = seen_title[t]
    if hit and hit != key and (key, hit) not in NEVER_MERGE and (hit, key) not in NEVER_MERGE:
        union(hit, key)
    if doi: seen_doi.setdefault(doi, key)
    if arx: seen_arxiv.setdefault(arx, key)
    if t: seen_title.setdefault(t, key)

# manual aliases (hand-checked same-work pairs with different titles/keys)
MANUAL = {
    'thickstun2023anticipatory': 'thickstun2024anticipatory',
    'louie2022expr': 'louie2022expressive',
    'donahue2022melody': 'donahue2022sheetsage',
    'wu2026midillm': 'wu2025midillm',
    'hooktheory2023aria': 'donahue2024hookpadaria',
    'hooktheory2024aria': 'donahue2024hookpadaria',
    'roberts2025livemusicmodels': 'lyria2025livemusic',
    'magenta2025livemusicmodels': 'lyria2025livemusic',
    'kim2026livemusicagents': 'kim2026designspace',
    'dai2021musicframeworks': 'dai2021controllable',
    'dai2022repetition': 'dai2022missing',
    'gotham2023wheninrome': 'gotham2019wheninrome',
    'blanchard2025jambot': 'blanchard2025jam',
    'huang2025audiomos': 'huang2025audiomos',
    'oros2025generativeai': 'oros2026cmu',
    'malandro2024composersassis': 'malandro2024composersassistant2',
    'tchemeube2022calliope': 'tchemeube2022calliope',
    'evans2024stableaudioopen': 'evans2024stableaudioopen',
    'egozy2016ims': 'egozy21m385',
    'suno2026studio2': 'suno2026',
    'udio2025umg': 'udio2025',
    'google2026lyria': 'google2025lyria2',
    'magenta2026realtime2': 'lyria2025livemusic',
    'kantosalo2016modes': 'kantosalo2016modes',
    'ronchini2025ttm': 'ronchini2025ttmuserstudy',
    'umg2024vsuno': 'umg2024vsuno',
}
for a, c in MANUAL.items():
    if a != c and a in by_key and c in by_key:
        union(c, a)

# groups -> canonical (prefer a MANUAL target present in the group, else first-seen key)
groups = collections.defaultdict(list)
for k in by_key:
    groups[find(k)].append(k)
canon = {}
manual_targets = set(MANUAL.values())
for root, members in groups.items():
    if len(members) < 2:
        continue
    pref = [m for m in members if m in manual_targets]
    canonical = pref[0] if pref else members[0]
    # keep the longest body under the canonical key
    best = max(members, key=lambda m: len(by_key[m][1]))
    if best != canonical:
        etype, body = by_key[best]
        body = re.sub(r'^(@\w+\s*\{)\s*[^,\s]+\s*,', r'\g<1>' + canonical + ',', body, count=1)
        by_key[canonical] = (etype, body)
    for m in members:
        if m != canonical:
            canon[m] = canonical

out = []
kept = 0
for key, (etype, body) in by_key.items():
    if key in canon:
        continue
    out.append(body.rstrip() + '\n')
    kept += 1

header = ('%% references.bib — merged from research/bib/*.bib on 2026-09-07\n'
          '%% %d entries kept, %d alias keys folded (see bib_aliases.json)\n\n' % (kept, len(canon)))
open('references.bib', 'w', encoding='utf-8').write(header + '\n'.join(out))
json.dump(canon, open('bib_aliases.json', 'w'), indent=1, sort_keys=True)

with open('bib_report.txt', 'w') as r:
    r.write(f'files: {len(files)}\nraw entries: {sum(1 for _ in by_key) + 0}\nunique keys: {len(by_key)}\nkept: {kept}\naliases: {len(canon)}\n\n')
    for a, c in sorted(canon.items()):
        r.write(f'{a:45s} -> {c}\n')
print(open('bib_report.txt').read())
