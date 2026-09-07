import re, glob, subprocess, datetime
ORDER = ['01-introduction','02-03-foundations','04-05-compose-annotate','06-compile-symbolic',
         '07-compile-audio','08-edit','09-play','10-evidence','11-12-substrate-context','13-agenda']
parts=[]
for name in ORDER:
    parts.append(open(f'sections/{name}.md',encoding='utf-8').read().strip())
body='\n\n---\n\n'.join(parts)
front = f'''---
title: "Human-Centered AI for Composition: A Literature Review"
subtitle: "Compose → Annotate → Compile → Edit — surveying 464 works for the design of an open-source AI music studio"
author: "AI Music Studio project"
date: "7 September 2026"
abstract: |
  The dominant public paradigm in music AI is text-to-full-song generation: a prompt in, an opaque
  master out. This review surveys the space from the opposite premise — that the composer authors
  the material, annotates it in notation, ink, voice or example, and asks a machine to *compile* a
  fuller realization under those annotations, then edits and recompiles. Drawing on 464 annotated
  entries (399 unique records, 1957–2026) across historical, symbolic-generation, audio-generation,
  HCI, multimodal-annotation, infrastructure, evaluation and legal literatures, it organizes the
  field by the stages of that loop rather than by technique. Five findings structure the argument:
  infilling under hard constraints, not generation from scratch, is the primitive that implements
  the loop; interface steerability moves control and ownership at least as much as model capability
  does; every input modality that works routes through an editable symbolic representation; the
  annotation layer — treating a composer's marks as a compilable instruction set — is the field's
  genuine white space; and a symbolic-first, human-authored system sits on materially better legal
  and ethical ground than the prompt-to-audio alternative. Twelve gaps are consolidated into a
  sequenced research agenda.
bibliography: references.bib
csl-refs: true
link-citations: true
reference-section-title: "References"
---

'''
open('literature-review.md','w',encoding='utf-8').write(front+body+'\n')
print('assembled words:', len(body.split()))
