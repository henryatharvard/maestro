#!/usr/bin/env python3
"""Assign every notes entry a primary taxonomy node (auto-coded from tags/title/cluster
with a manual override table), and emit taxonomy-map.md + taxonomy-map.csv + node counts."""
import re, glob, csv, json, collections

alias = json.load(open('bib_aliases.json'))

NODES = collections.OrderedDict([
 ('F1','Algorithmic composition lineage'),('F2','Interactive systems & accompaniment lineage'),
 ('F3','Commercial auto-accompaniment & notation lineage'),('F4','Theories of co-creativity & creativity support'),
 ('F5','Human-centered music-AI programmes & design spaces'),
 ('S1.1','Compose: performance capture & transcription'),('S1.2','Compose: voice / humming'),
 ('S1.3','Compose: sketch / pen'),('S1.4','Compose: image / video / text inspiration'),('S1.5','Compose: example audio & personal style'),
 ('S2.1','Annotate: encodings, standards & tools'),('S2.2','Annotate: machine-proposed annotations (analysis)'),
 ('S2.3','Annotate: control vocabularies'),('S2.4','Annotate: multimodal annotation as instruction'),('S2.5','Annotate: economics of human labelling'),
 ('S3.1','Compile: symbolic representations & tokenizers'),('S3.2','Compile: infilling & constrained regeneration'),
 ('S3.3','Compile: attribute/text/rule-conditioned symbolic generation'),('S3.4','Compile: structure-aware & hierarchical pipelines'),
 ('S3.5','Compile: harmonization, accompaniment & arrangement'),('S3.6','Compile: music LLMs & music-as-code'),
 ('S3.7','Compile: expressive performance rendering'),('S3.8','Compile: audio rendering & symbolic-conditioned audio'),
 ('S3.9','Compile: text-to-music & full-song audio generation'),('S3.10','Compile: music-understanding models as critics'),
 ('S4.1','Edit: editing paradigms'),('S4.2','Edit: symbolic editing, variation & proofreading'),('S4.3','Edit: audio editing & inpainting'),
 ('S4.4','Edit: AI→human feedback & explanation'),('S4.5','Edit: history, versioning & alternatives'),
 ('S5.1','Play: score following & accompaniment'),('S5.2','Play: improvisation partners'),('S5.3','Play: RL-tuned & live neural models'),('S5.4','Play: design spaces, practice & games'),
 ('E1','Evidence: controlled studies of co-creative systems'),('E2','Evidence: field studies & practitioner perspectives'),
 ('E3','Evidence: deployed systems with usage data'),('E4','Evaluation: metrics for generated music'),
 ('E5','Evaluation: creativity & co-creativity frameworks'),('E6','Evaluation: music-theory competence benchmarks'),
 ('B1','Substrate: notation engines & editors'),('B2','Substrate: symbolic toolkits'),('B3','Substrate: runtime & integration'),
 ('B4','Substrate: datasets & corpora'),('B5','Substrate: education & pedagogy'),
 ('C1','Context: product landscape'),('C2','Context: law & policy'),('C3','Context: ethics, provenance & disclosure'),('C4','Context: economics & attitudes'),
 ('X','Unassigned / meta'),
])

# manual overrides by (canonical) bibkey -> node
MANUAL = {
 'huang2016chordripple':'S3.5','huang2017coconet':'S3.2','huang2018musictransformer':'S3.4','ippolito2018infilling':'S3.2',
 'roberts2018musicvae':'S3.3','donahue2019pianogenie':'S5.3','huang2019bachdoodle':'E3','roberts2019magentastudio':'B3',
 'roberts2018magentajs':'B2','louie2020cococo':'E1','huang2020aisongcontest':'E2','engel2020ddsp':'S3.8','magenta2020tonetransfer':'S1.2',
 'young2021compositionalsteering':'S2.3','wu2022mididdsp':'S3.7','louie2022expressive':'E1','magenta2022ddspvst':'S3.8',
 'wu2024realchords':'S5.3','scarlatos2025realjam':'S5.3','blanchard2025jambot':'S5.2','lyria2025livemusic':'S3.8','wu2026gapt':'S5.3',
 'wu2026streaming':'S5.3','kim2026designspace':'F5','brade2026agentsinconcert':'S5.4','novack2026lmdm':'S5.3','wu2026stemphonic':'S3.5',
 'wang2026latentft':'S4.3','huang2025creativityinteraction':'F5','mit2026mtcshowcase':'F5','cuthbert2010music21':'B2','cuthbert2023ocw21m383':'B5',
 'egozy21m385':'B5','egozy2018concertcue':'S2.1','egozy2005harmonix':'S5.4','farbood2004hyperscore':'S1.3','machover1992hyperinstruments':'F2',
 'vercoe1984syntheticperformer':'F2','gclef2026lab':'F5','kim2025amuse':'S1.4','donahue2024hookpadaria':'E3','thickstun2024anticipatory':'S3.2',
 'kim2026decomposer':'S3.6','wu2024musiccontrolnet':'S3.8','donahue2023singsong':'S1.2','donahue2022sheetsage':'S1.1','wang2026multiverse':'E1',
 'kim2025musicarena':'E4','huang2025aligning':'E4','bukey2024justlabel':'S2.5','wei2024musictheory':'E6','zhou2024midinfinite':'B3',
 'jung2025unified':'S1.1','wang2024musicaware':'S5.4','wang2025rise':'S5.4','ma2024foundation':'F4','oros2026cmu':'E1',
 'dannenberg1984online':'F2','dannenberg2014hcmp':'S5.1','dannenberg1997nyquist':'S3.6','dai2021controllable':'S3.4','dai2022missing':'S2.2',
 'dai2023personalised':'S3.4','dai2024interconnections':'S2.2','tilekbay2024expressedit':'S2.4','thisgoober2026real':'S2.4','benetatos2022drawlisten':'S1.3',
 'wu2024muskitsespnet':'B2','castellon2021codified':'S3.10','cmu2025musictech':'F5',
 'huang2020popmusictransformer':'S3.1','hsiao2021compoundword':'S3.1','zeng2021musicbert':'S3.1','sturm2016folkrnn':'F1','fradet2021miditok':'B2',
 'bradshaw2025aria':'S3.1','bradshaw2025ariamidi':'B4','le2025nlpsurvey':'F4','ji2023survey':'F4','hadjeres2017deepbach':'S3.2','pati2019inpaintnet':'S3.2',
 'chen2020sketchnet':'S1.3','ens2020mmm':'S3.2','chang2021xlnet':'S3.2','guo2022musiac':'S3.2','malandro2024composersassistant2':'S3.2','malandro2023composersassistant':'S3.2','pasquier2025midigpt':'S3.2',
 'zhouzheng2025midirwkv':'S3.2','min2023polyffusion':'S3.2','lv2023getmusic':'S3.2','zhang2025groove':'S4.2','yu2022museformer':'S3.4','vonrutte2023figaro':'S2.3',
 'lu2023musecoco':'S3.3','wu2023musemorphose':'S4.2','tan2020fadernets':'S3.3','dong2023mmt':'S3.1','chen2024sympac':'S3.4','bhandari2025text2midi':'S3.3',
 'xu2025metascore':'B4','wu2025midillm':'S3.6','huang2024scg':'S3.3','petteno2025lcdiff':'S3.3','lin2026diffsymbo':'S3.3','yuan2024chatmusician':'S3.6',
 'qu2024mupt':'S3.6','wang2025notagen':'S3.6','wu2024melodyt5':'S3.6','jiang2025functionalignment':'S3.5','kumar2026howfar':'E6','li2024ziqieval':'E6',
 'wang2024wholesong':'S3.4','tan2022melodyinfilling':'S2.3','zhao2021accomontage':'S3.5','zhao2023qa':'S3.5','zhao2024structured':'S3.5',
 'kaliakatsospapakostas2025harmonization':'S3.5','jeong2019virtuosonet':'S3.7','borovik2023scoreperformer':'S3.7','zhang2024dexter':'S3.7',
 'dhariwal2020jukebox':'S3.9','agostinelli2023musiclm':'S3.9','huang2023noise2music':'S3.9','copet2023musicgen':'S3.9','liu2023audioldm':'S3.9','liu2024audioldm2':'S3.9',
 'evans2024longform':'S3.9','evans2024stableaudioopen':'S3.9','li2023jen1':'S3.9','melechovsky2024mustango':'S3.8','prajwal2024musicflow':'S3.9','forsgren2022riffusion':'S3.9',
 'suno2026':'C1','udio2025':'C1','google2025lyria2':'C1','google2025lyriarealtime':'C1','adobe2024musicgenaicontrol':'S4.3','elevenlabs2025music':'C1','mureka2025':'C1',
 'novack2025arc':'S4.3','splice2025landr':'C1','ziv2024magnet':'S3.9','rouard2024musicgenstyle':'S1.5','tal2024jasco':'S3.8','lelan2024melodyflow':'S4.3',
 'rouard2025musicgenstem':'S3.9','gong2025acestep':'S3.9','gong2026acestep15':'S3.9','yuan2025yue':'S3.9','ning2025diffrhythm':'S3.9','liu2025songgen':'S3.9','heartmula2026':'S3.9',
 'lin2023cocomulla':'S3.8','novack2024ditto':'S3.8','zhang2024musicmagus':'S4.3','manor2024zeta':'S4.3','wang2023audit':'S4.3','han2023instructme':'S4.3',
 'zhang2025instructmusicgen':'S4.3','tsai2025musecontrollite':'S3.8','hou2024melodycontrolnet':'S3.8','yang2025songeditor':'S4.3','parker2024stemgen':'S3.9',
 'mariani2024msdm':'S3.9','nistal2024diffariff':'S3.9','chu2025text2fx':'S4.3','floresgarcia2025sketch2sound':'S1.2','zhu2024musichifi':'S3.8',
 'ronchini2025ttmuserstudy':'E2','li2024mert':'S3.10','zhu2025muq':'S3.10','wu2023clap':'S3.10','liu2023mullama':'S3.10','gardner2024llark':'S3.10',
 'deng2024musilingo':'S3.10','tang2024salmonn':'S3.10','chu2024qwen2audio':'S3.10','zhao2024openmu':'S3.10','weck2024muchomusic':'E6','manco2023songdescriber':'E4',
 'shneiderman2007cst':'F4','shneiderman2020hcai':'F4','cherry2014csi':'E5','lubart2005partners':'F4','deterding2017mici':'F4','kantosalo2016modes':'F4',
 'karimi2018evaluating':'E5','davis2016drawingapprentice':'F4','guzdial2019friend':'F4','rezwana2023cofi':'F4','rezwana2022perceptions':'F4',
 'jordanous2012standardised':'E5','wan2024secondmind':'F4','fiebrink2018mlcreativetool':'F4','papadopoulos2016flowcomposer':'S3.2','dinculescu2019midime':'S1.5',
 'frid2020example':'E1','micchi2021ikeepcounting':'E2','suh2021socialglue':'E2','zhang2021cosmic':'S3.6','tchemeube2022calliope':'B3','tchemeube2023mmmc':'E1',
 'metacreation2023mmm4live':'B3','shepardson2022notochord':'S5.2','zhang2023loopcopilot':'E1','yu2023musicagent':'S3.6','deng2024composerx':'S3.6',
 'ramoneda2024refinpaint':'S4.4','googledeepmind2025sandbox':'C1','krol2025ownership':'E1','sturm2019machinefolk':'E2','sturm2019openquestions':'C2',
 'deruty2022sonycsl':'E2','newman2023perceptions':'E2','morris2024haisp':'E2','ford2024reflection':'E2','fu2025novice':'E2','herndon2021hollyplus':'C3',
 'yang2020evaluation':'E4','bryankinns2021xai':'S4.4','scurto2021coexplorer':'S5.3','terry2002sideviews':'S4.5',
 'ghias1995qbh':'S1.2','frank2020humtosearch':'S1.2','hawthorne2018onsets':'S1.1','gardner2022mt3':'S1.1','bittner2022basicpitch':'S1.1','liu2023humtrans':'S1.2',
 'gupta2024dynhumtrans':'S1.2','cartwright2015vocalsketch':'S1.2','vochlea2021dubler':'S1.2','doremir2014scorecloud':'S1.2','elkins2025dawzy':'S2.4',
 'xenakis1977upic':'S1.3','xenakis1992formalized':'F1','coughlan2006interaction':'S1.3','garcia2012paper':'S1.3','hearn2015staffpad':'S1.3','cavez2024challenges':'S1.3',
 'cavez2025euterpen':'S1.3','fu2026tactus':'S2.1','namgyal2022mididraw':'S1.3','liang2024drawlody':'S1.3','riosvila2024smt':'S1.1','zhang2022vis2mus':'S1.4',
 'chowdhury2024melfusion':'S1.4','rinaldi2024art2mus':'S1.4','su2024v2meow':'S1.4','kang2024video2music':'S1.4','tian2025vidmuse':'S1.4','liu2024mumullama':'S1.4','li2024muvi':'S1.4',
 'cannam2010sonicvisualiser':'S2.1','giraud2018dezrann':'S2.1','pugin2014verovio':'B1','goebl2023meifriend':'S2.1','w3c2021musicxml40':'S3.1','walshaw2011abc':'S3.1',
 'huron1995humdrum':'S3.1','cheppudira2010vexflow':'B1','newzik2026readers':'S2.1','gotham2019wheninrome':'B4','neuwirth2018abc':'B4',
 'shneiderman1983direct':'S4.1','masson2024directgpt':'S4.1','brooks2023instructpix2pix':'S4.1','igarashi1999teddy':'S4.1','cypher1993wwid':'S4.1','omar2019hazel':'S3.6',
 'foscarin2019diff':'S4.5','flat2026history':'S4.5','grossman2010chronicle':'S4.5','suh2024luminate':'S4.5','nienhuys2003lilypond':'S3.6','wang2015chuck':'S3.6',
 'mclean2014tidal':'S3.6','assayag1999openmusic':'S3.6','nierhaus2009algorithmic':'F1','xu2026libretto':'S3.6',
 'osmd2026':'B1','vexflow2024':'B1','alphatab2026':'B1','abcjs2026':'B1','lilypond2026':'B1','musescore2026studio':'B1','makemusic2024finale':'F3','soundslice2026':'B1',
 'flat2026':'B1','w3c2026webmidi':'B3','spessasynth2026':'B3','liao2024symusic':'B2','dong2020muspy':'B2','cancinochacon2022partitura':'B2','raffel2014prettymidi':'B2',
 'clap2022':'B3','korg1993i3':'F3','pgmusic2026biab':'S3.5','pgmusic1990bandinabox':'F3','clavia2023nordstage4':'B3',
 'raffel2016lakh':'B4','hawthorne2019maestro':'B4','kong2020giantmidi':'B4','zhang2022atepp':'B4','long2024pdmx':'B4','kantarelis2024chordonomicon':'B4','ens2021metamidi':'B4',
 'lev2024lamidi':'B4','wang2020pop909':'B4','gotham2022openscore':'B4','hentschel2021mozart':'B4','melechovsky2024midicaps':'B4','manilow2019slakh':'B4','xmader2021musescore':'C3',
 'napoleslopez2021augmentednet':'S2.2','karystinaios2023chordgnn':'S2.2','sailor2024rnbert':'S2.2','chen2021attend':'S2.2','nihahn2024schenker':'S2.2','finkensiep2018skipgrams':'S2.2',
 'nieto2016msaf':'S2.2','kim2023allinone':'S2.2','bock2016madmom':'S2.2','huang2005palestrinapal':'S2.2','egozy2016harmonix':'S5.4','miller2009schizophonic':'S5.4',
 'harmonix2020fuser':'S5.4','horn2022tunepad':'B5','freeman2019earsketch':'B5','aaron2016sonicpi':'B5','yousician2026':'B5','oros2026helpthathurts':'E2',
 'hiller1959experimental':'F1','koenig1970project':'F1','cope2001virtual':'F1','rowe1993interactive':'F2','lewis2000toomanynotes':'F2','biles1994genjam':'F2',
 'pachet2003continuator':'F2','assayag2006omax':'F2','eck2002blues':'F1','boulangerlewandowski2012modeling':'F1','mcintyre1994bachinabox':'F1',
 'kunlun2025mureka':'C1','apple2024logicpro11':'C1','ableton2024live12':'C1','scaler2025v3':'C1','hexachords2022orb':'C1','steinberg2025dorico6':'B1',
 'musegroup2025musescore46':'B1','avid2026sibelius':'B1','moises2025aistudio':'C1','splice2024create':'C1','ahuja2025abletonmcp':'B3','suno2025wavtool':'C1',
 'dreamtonics2025synthv2':'C1','neutone2024morpho':'S1.5','kilgour2019fad':'E4','gui2024fad':'E4','chung2025kad':'E4','retkowski2024fmd':'E4','liu2025musiceval':'E4',
 'huang2025audiomos':'E4','grotschla2025benchmarking':'E4','zhang2025aesthetics':'E4','kader2025survey':'E4','boden2004creativemind':'E5','ritchie2007criteria':'E5',
 'colton2008tripod':'E5','figueiredo2025echoes':'E4','deezer2025ipsos':'C4','batlleroca2024mira':'C3','casini2025sunoudio':'E3','epple2024watermarking':'C3',
 'umg2024vsuno':'C2','umg2025udio':'C2','wmg2025suno':'C2','lgmunich2025gemaopenai':'C2','lgmunich2026gemasuno':'C2','usco2025part2':'C2','thaler2025perlmutter':'C2',
 'eu2024aiact':'C2','tennessee2024elvis':'C2','newtonrex2024fairlytrained':'C3','newtonrex2024statement':'C3','spawning2022haveibeentrained':'C3','deezer2026aistats':'C3',
 'spotify2025aipolicy':'C3','usdoj2024smith':'C3','goldmedia2024gemasacem':'C4','cisac2024pmp':'C4','apraamcos2024ai':'C4','concord2023anthropic':'C2',
}

def rule_node(cl, title, tags):
    t = title.lower(); g = set(tags)
    if 'ethics-legal' in g and cl == '08': return 'C3'
    if 'product' in g and 'notation' in g: return 'B1'
    if 'product' in g: return 'C1'
    if 'dataset' in g or 'corpus' in g: return 'B4'
    if 'education' in g: return 'B5'
    if 'evaluation' in g and 'HCI-study' in g: return 'E1'
    if 'HCI-study' in g: return 'E2'
    if 'evaluation' in g: return 'E4'
    if 'history' in g: return 'F1'
    if 'co-creation-framework' in g: return 'F4'
    if 'humming' in g: return 'S1.2'
    if 'sketch' in g: return 'S1.3'
    if 'image' in g or 'video' in g: return 'S1.4'
    if 'transcription' in g: return 'S1.1'
    if 'annotation' in g: return 'S2.1'
    if 'theory-analysis' in g: return 'S2.2'
    if 'real-time' in g: return 'S5.3'
    if 'infilling' in g and 'audio-generation' not in g: return 'S3.2'
    if 'music-as-code' in g or 'LLM-agent' in g: return 'S3.6'
    if 'expression-performance' in g: return 'S3.7'
    if 'editing' in g and 'audio-generation' in g: return 'S4.3'
    if 'editing' in g: return 'S4.2'
    if 'accompaniment' in g and 'audio-generation' not in g: return 'S3.5'
    if 'structure' in g: return 'S3.4'
    if 'audio-generation' in g and ('symbolic-generation' in g or 'controllability' in g): return 'S3.8'
    if 'audio-generation' in g: return 'S3.9'
    if 'representation' in g or 'toolkit' in g: return 'B2' if 'toolkit' in g else 'S3.1'
    if 'text-conditioning' in g or 'controllability' in g: return 'S3.3'
    if 'symbolic-generation' in g: return 'S3.3'
    return 'X'

rows = []
for f in sorted(glob.glob('notes/*.md')):
    cl = f.split('/')[-1][:2]
    txt = open(f, encoding='utf-8').read()
    for p in re.split(r'\n(?=### )', txt)[1:]:
        title = p.split('\n')[0][4:].strip()
        tags = re.findall(r'\[([A-Za-z\-]+)\]', (re.search(r'\*\*Tags:\*\*\s*(.*)', p) or [None, ''])[1] if re.search(r'\*\*Tags:\*\*\s*(.*)', p) else '')
        keym = re.search(r'\*\*BibKey:\*\*\s*([^\n]+)', p)
        keys = re.findall(r'[a-z][a-z0-9]+', keym.group(1).split('(')[0]) if keym else []
        key = keys[0] if keys else ''
        key = alias.get(key, key)
        ver = (re.search(r'\*\*Verification:\*\*\s*(\w+)', p) or [None, ''])[1] if re.search(r'\*\*Verification:\*\*\s*(\w+)', p) else ''
        who = re.search(r'\*\*Who/where/when:\*\*\s*(.*)', p)
        yrs = re.findall(r'(19[5-9]\d|20[0-2]\d)', who.group(1)) if who else []
        year = yrs[-1] if yrs else ''
        if 'ProductTable' in title:   # summary table, not an entry
            continue
        v = ver.split()[0].lower() if ver else ''
        ver = v if v in ('verified','partial','unverified') else 'partial'
        if key in MANUAL:
            node, how = MANUAL[key], 'manual'
        else:
            node, how = rule_node(cl, title, tags), 'auto'
        rows.append(dict(cluster=cl, title=title, year=year, bibkey=key, node=node, how=how, verification=ver, tags=' '.join(tags)))

# write csv
with open('taxonomy-map.csv', 'w', newline='', encoding='utf-8') as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)

counts = collections.Counter(r['node'] for r in rows)
hows = collections.Counter(r['how'] for r in rows)
lines = ['---', 'title: "Taxonomy map: all 463 entries assigned to a primary node"', 'date: "2026-09-07"', '---', '',
         f'Assignments: {hows["manual"]} hand-coded by canonical BibKey, {hows["auto"]} auto-coded from tags/titles (provisional; review when citing). '
         'Node codes follow `taxonomy.md`. Entries appearing in several clusters appear once per cluster (the notes differ).', '',
         '## Counts per node', '', '| Node | Name | Entries |', '|---|---|---|']
for n, name in NODES.items():
    if counts.get(n): lines.append(f'| {n} | {name} | {counts[n]} |')
lines += ['', '## Entries by node', '']
for n, name in NODES.items():
    sel = [r for r in rows if r['node'] == n]
    if not sel: continue
    lines.append(f'### {n}. {name}'); lines.append('')
    lines.append('| Cluster | Work | Year | BibKey | Coded | Verified |'); lines.append('|---|---|---|---|---|---|')
    for r in sorted(sel, key=lambda r: (r['year'], r['title'])):
        t = r['title'].replace('|', '/')
        lines.append(f"| {r['cluster']} | {t[:120]} | {r['year']} | `{r['bibkey']}` | {r['how']} | {r['verification']} |")
    lines.append('')
open('taxonomy-map.md', 'w', encoding='utf-8').write('\n'.join(lines))
print(hows); print(sorted(counts.items(), key=lambda x: -x[1])[:60])
print('unassigned:', [r['title'][:60] for r in rows if r['node']=='X'])
