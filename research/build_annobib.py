#!/usr/bin/env python3
"""Build annotated-bibliography.md: one record per unique work, organized by taxonomy node,
merging the per-cluster notes (longest 'What it is' wins; evidence/why-it-matters merged)."""
import re, glob, csv, json, collections

alias = json.load(open('bib_aliases.json'))
NODE_NAMES = {}
for line in open('taxonomy-map.md', encoding='utf-8'):
    m = re.match(r'\| ([A-Z][0-9.]*|X) \| (.+?) \| \d+ \|', line)
    if m: NODE_NAMES[m.group(1)] = m.group(2)
node_of = {}
for r in csv.DictReader(open('taxonomy-map.csv', encoding='utf-8')):
    node_of.setdefault(r['bibkey'], r['node'])

def fld(p, name):
    m = re.search(r'\*\*' + name + r':\*\*\s*(.*?)(?=\n- \*\*|\n###|\Z)', p, re.S)
    return re.sub(r'\s+', ' ', m.group(1)).strip() if m else ''

recs = collections.OrderedDict()
for f in sorted(glob.glob('notes/*.md')):
    cl = f.split('/')[-1][:2]
    for p in re.split(r'\n(?=### )', open(f, encoding='utf-8').read())[1:]:
        title = p.split('\n')[0][4:].strip()
        keym = re.search(r'\*\*BibKey:\*\*\s*([^\n]+)', p)
        ks = re.findall(r'[a-z][a-z0-9]+', keym.group(1).split('(')[0]) if keym else []
        key = alias.get(ks[0], ks[0]) if ks else 'nokey-' + cl + '-' + title[:20]
        d = dict(title=title, who=fld(p,'Who/where/when'), links=fld(p,'Links'),
                 what=fld(p,'What it is'), ev=fld(p,'Evidence'), why=fld(p,'Why it matters for the studio'),
                 tags=fld(p,'Tags'), ver=fld(p,'Verification'), clusters=[cl])
        if key in recs:
            o = recs[key]; o['clusters'].append(cl)
            for k in ('what','ev','why','who','links','tags'):
                if len(d[k]) > len(o[k]): o[k] = d[k]
            if 'verified' in d['ver'] and 'verified' not in o['ver']: o['ver'] = d['ver']
        else:
            recs[key] = d

by_node = collections.defaultdict(list)
for k, d in recs.items(): by_node[node_of.get(k, 'X')].append((k, d))

order = ['F1','F2','F3','F4','F5','S1.1','S1.2','S1.3','S1.4','S1.5','S2.1','S2.2','S2.3','S2.4','S2.5',
 'S3.1','S3.2','S3.3','S3.4','S3.5','S3.6','S3.7','S3.8','S3.9','S3.10','S4.1','S4.2','S4.3','S4.4','S4.5',
 'S5.1','S5.2','S5.3','S5.4','E1','E2','E3','E4','E5','E6','B1','B2','B3','B4','B5','C1','C2','C3','C4','X']

out = ['---', 'title: "Annotated Bibliography"',
 'subtitle: "%d unique works, organized by taxonomy node"' % len(recs),
 'date: "7 September 2026"', '---', '',
 'Records merged from the eight research clusters in `notes/`. Each entry gives provenance, what the '
 'system does, its evidence, and why it matters for a composer-centered studio. **Verification** records '
 'how the entry was checked in September 2026: *verified* = a primary source was fetched; *partial* = '
 'secondary pages or search snippets only; *unverified* = recall, not re-confirmed. Treat figures in '
 'partial and unverified entries as indicative. Cluster numbers refer to the source notes files. '
 'Citation keys match `references.bib`.', '']
for n in order:
    if not by_node.get(n): continue
    out.append('## %s. %s' % (n, NODE_NAMES.get(n, n)))
    out.append('')
    for k, d in sorted(by_node[n], key=lambda x: x[1]['who']):
        out.append('### `%s` — %s' % (k, d['title']))
        out.append('')
        if d['who']: out.append('*%s*' % d['who'])
        if d['links']: out.append('')  ; out.append('Links: %s' % d['links'])
        out.append('')
        if d['what']: out.append(d['what']); out.append('')
        if d['ev'] and d['ev'] not in ('—','-',''): out.append('**Evidence.** %s' % d['ev']); out.append('')
        if d['why']: out.append('**For the studio.** %s' % d['why']); out.append('')
        meta = []
        if d['tags']: meta.append('Tags: %s' % d['tags'])
        meta.append('Verification: %s' % (d['ver'] or 'n/a'))
        meta.append('Cluster%s %s' % ('s' if len(set(d['clusters']))>1 else '', ', '.join(sorted(set(d['clusters'])))))
        out.append('<small>%s</small>' % ' · '.join(meta)); out.append('')
open('annotated-bibliography.md','w',encoding='utf-8').write('\n'.join(out))
print('unique works:', len(recs), '| words:', len('\n'.join(out).split()))
