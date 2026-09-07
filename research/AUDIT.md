---
title: "Internal-consistency and quality audit — literature-review.md"
subtitle: "Document audit against notes/, taxonomy.md, references.bib (no external sources consulted)"
date: "2026-09-07"
---

# Summary

Audited: `literature-review.md` (43,383 words, sections 1–13) against `notes/01–08` (464 entries, 394 distinct BibKeys), `taxonomy.md`, `taxonomy-map.{md,csv}`, `references.bib` (399 records) and `bib_aliases.json`.

| Check | Findings | Verdict |
|---|---|---|
| 1. Claim-to-source traceability (35 claims sampled, §§2–13) | **12** problems (23 OK, 8 DRIFT, 4 UNSUPPORTED) | Sound in the numbers, weak in the superlatives |
| 2. Hedging discipline | **11 breaches** (+ 8 named risk areas that pass) | Mostly disciplined; law/economics/history are the leaks |
| 3. Contradictions between sections | **9 findings** | Two are substantive, seven are cosmetic |
| 4. Redundancy | **12 cases** (cap reached; ~4,000–4,500 words recoverable) | Systematic: S1.4/S2.4 duplicate S3.3/S4.1 |
| 5. Taxonomy fidelity | **4 findings**, none in the review itself | Review is fully conformant; the map has 3 defects |
| 6. Citation hygiene | **7 findings**; 0 missing keys, 0 alias keys | Excellent; 3 uncited bib records to resolve |
| 7. Prose quality | **15 flags** | No bullets, no first person; sentence length is the problem |
| **Total** | **70 numbered items — 67 distinct** (3 cross-listed: the §2.3 primacy claim, the ELVIS date and the Goldmedia date each appear under two checks) | |

## The five highest-priority fixes

1. **§2.3 contradicts §6.2 and §13.1 on the earliest generative feature on a notation surface.** §2.3: "The first learned member on a notation surface is Hookpad Aria (2024)." §6.2/§13.1 (G3) both credit "DeepBach's 2017 MuseScore plugin," as do the notes. Fix: rewrite §2.3 as "the first learned member on a *commercial* notation surface" and cross-reference S3.2, or delete the primacy claim.
2. **Four unsupported primacy claims that no note makes** (§6.5 Music Transformer "the first neural 'compile a lead sheet into a piano part'"; §7.1 Udio "the first mainstream tool to offer audio inpainting"; §7.2 Magenta RealTime 2 "the first open audio model whose training explicitly pairs audio with transcribed symbolic data"; §10.4 FMD "the first standard distributional metric over *symbolic* music"). Fix: scope each to the corpus ("the earliest instance in this corpus") or cut. These are the only claims in the sample with no note backing at all.
3. **"The largest gap" is awarded to three different things.** §8.2: symbolic editing (S4.2) is "the largest single gap the review identifies." §10.1: MMM-C's control deficit is "the largest single gap in this literature." §1.4/§13.1: the annotation layer (S2.4) is "the studio's genuine white space"/"the central gap." Fix: reserve "largest gap" for S2.4 (the thesis of §13), and demote the other two to "the largest *measured* control deficit" and "the thinnest editing node."
4. **Law and economics figures are stated at higher precision than their `partial` notes support** — Goldmedia given a fabricated day ("published 30 January 2024" vs the note's "Jan 2024") with four unhedged percentages; the ELVIS Act given an effective date ("1 July 2024") that appears nowhere in the notes; the EU AI Act given four exact dates from a `partial` note; Lakh's 176,581 files and MAESTRO's 1,276 performances stated flat from `partial`/recalled notes. Fix: add "reported"/"per the project page" hedges and strip the invented day precision, matching the discipline §10.1 and §11.5 already show.
5. **Cut ~4,000 words of duplicated coverage** — the four worst: §4.4's text-to-symbolic paragraph reproduces §6.3 (MuseCoco/Text2midi/MIDI-LLM/MetaScore, same figures); §3.2's Design Space passage reproduces §9.4 verbatim in substance; the Hookpad Aria telemetry (318k/3k/74k/23%) appears in full four times (§1.4, §2.3, §6.2, §10.3); RefinPaint's study is reported three times (§6.2, §8.2, §10.1) — and §8.2 even says it is "treated at length under S3.2" before repeating it.

---

# 1. Claim-to-source traceability

35 claims sampled across §§2–13, weighted toward numbers, dates, N values, licences, model sizes and superlatives. Verdicts: **OK 23 · DRIFT 8 · UNSUPPORTED 4**.

## 1a. DRIFT (8)

1. **DRIFT — `literature-review.md` §2.3 (L97), primacy of Hookpad Aria.**
   Review: "The first learned member on a notation surface is Hookpad Aria (2024)."
   Notes: `notes/03-symbolic-models.md` (DeepBach) — "implemented as a MuseScore plugin where the composer selects a region and asks for re-harmonisation," ICML 2017, verification `verified`. The review's own §6.2 and §13.1 G3 both name DeepBach's 2017 MuseScore plugin as a notation-surface deployment.
   Fix: change to "the first learned member on a *commercial* notation surface" and add "(DeepBach's 2017 MuseScore plugin preceded it in research; see S3.2)".

2. **DRIFT — §10.4 (L559), Fréchet Music Distance primacy.**
   Review: "Fréchet Music Distance [@retkowski2024fmd] is the first standard distributional metric over *symbolic* music."
   Notes: `notes/08` — "Fréchet distance over embeddings of *symbolic* music … validated to separate model quality levels across datasets." No primacy or standardisation claim.
   Fix: "the first widely reported distributional metric over *symbolic* music in this corpus."

3. **DRIFT — §3.2 (L148), RefinPaint's affiliation.**
   Review: "Sony CSL Tokyo's RefinPaint extends the stance to critique."
   Notes: `notes/05-hci-cocreation.md` — "Pedro Ramoneda, Martín Rocamora, Taketo Akama; Universitat Pompeu Fabra, Sony CSL Tokyo." Two of three authors are UPF; only Akama is Sony CSL.
   Fix: "RefinPaint, a UPF–Sony CSL Tokyo collaboration, extends the stance to critique."

4. **DRIFT — §9.4 (L509), the Harmonix mission quote.**
   Review: "Harmonix, founded in 1995 by Egozy and Rigopulos out of Machover's Media Lab group, *whose stated aim was* 'making every human being into a musician' …"
   Notes: `notes/01-huang-mit.md` attributes that quote to **Machover** ("Machover's stated goal: 'making every human being into a musician'"), and the Harmonix entry records verification as `partial (bio verified; quotes unverified)` with "Egozy's specific public statements … were not retrievable this session."
   Fix: "out of Machover's Media Lab group, whose director's stated goal was 'making every human being into a musician'".

5. **DRIFT — §12.4 (L695), Goldmedia publication date.**
   Review: "published 30 January 2024 on a survey of roughly 15,000 members."
   Notes: `notes/08` — "published Jan 2024; survey of ~15,000 members," verification `partial`.
   Fix: "published in January 2024"; drop the day.

6. **DRIFT — §11.5 (L653) and §10.2 (L549), what `oros2026helpthathurts` is.**
   Review §11.5: "the first empirical studies of generative AI in *composition teaching* … include an experiment reporting that AI ideation can reduce the originality of *student* compositions."
   Notes: `notes/07` describes "Help That Hurts: The Creativity Cost of Generative AI Ideation in Music Composition" (Oros, Randall, Telang — the same CMU authors as `oros2026cmu`) as "an experiment suggesting AI ideation can *reduce* creative output quality/originality in composition tasks"; the *education* papers bundled in the same note are Liu & Liao (flute learning) and Park & Choo. Nothing in the notes makes it a teaching study or its participants students.
   Fix: in §11.5 say "an experiment on AI ideation in composition tasks (not in a classroom setting)" and keep the education framing for the Liu & Liao / Park & Choo material; reconcile with §10.2, which correctly calls it "the related SSRN working paper."

7. **DRIFT — §5.2 (L226) and §6.4 (L292), the corpus behind Dai and Dannenberg's structure results.**
   Review: "extracted section/phrase repetition structure from 909 transcriptions with 93% phrase-boundary accuracy" under the heading "For symbolic pop."
   Notes: `notes/02` — "909 **Chinese pop** MIDI transcriptions."
   Fix: add "Chinese pop" once (the genre restriction is load-bearing for a generalisation about "human pop").

8. **DRIFT — §11.4 (L645), strength of the Composer's Assistant licence result.**
   Review: "Composer's Assistant, trained only on permissively licensed MIDI, **proves** a competitive infilling model can be built inside these constraints."
   Notes: `notes/03` — "Trained only on permissively-licensed MIDI"; evidence is a listening study finding parity with human excerpts. The review's own §13.1 G12 states it correctly: "shows the constraint is workable."
   Fix: replace "proves" with "shows"; align with G12.

## 1b. UNSUPPORTED (4)

9. **UNSUPPORTED — §6.5 (L298).** "Music Transformer's melody-to-accompaniment mode was the first neural 'compile a lead sheet into a piano part'." Both Music Transformer notes (`notes/01`, `notes/03`) describe the seq2seq melody→accompaniment mode but make no primacy claim, and no note surveys earlier neural harmonisers for comparison. Fix: "Music Transformer demonstrated a seq2seq melody→accompaniment mode — the earliest instance in this corpus of …".

10. **UNSUPPORTED — §7.1 (L342).** "Udio, launched in April 2024, … was the first mainstream tool to offer *audio inpainting* of a user-selected region." `notes/04` and `notes/08` both record Udio's inpainting (premium feature) with no primacy claim. Fix: delete "the first mainstream tool to offer" or scope to "the earliest mainstream inpainting feature recorded in this corpus."

11. **UNSUPPORTED — §7.2 (L362).** Magenta RealTime 2 "was trained on about 71k hours of mostly instrumental stock music paired with MT3-inferred MIDI labels, **the first open audio model whose training explicitly pairs audio with transcribed symbolic data**." `notes/04` records "trained on ~71k h mostly-instrumental stock music with **MT3-inferred MIDI labels**" and nothing about being first. Fix: cut the clause, or "the only open audio model in this corpus whose training pairs audio with transcribed symbolic data."

12. **UNSUPPORTED — §12.2 (L683).** "Tennessee's ELVIS Act, **effective 1 July 2024**, was the first United States state law extending the right of publicity to voice including simulations." `notes/08` supports the "first U.S. state law" characterisation and the liability scope but records **no** effective date, and the entry's verification is `partial`. Fix: drop the date or mark it as reported.

## 1c. OK (23)

Verified faithful against the cited notes, including hedge preservation where present:

13. §2.1 Bach Doodle — ">55 million harmonisation queries in three days," "21.6 million" rated pairs, "8.5 million sessions," CC BY 4.0 (§6.2, §10.3, §11.4 identical). Matches `notes/01`, `notes/05`, `notes/07`. **OK**
14. §2.3/§6.5 Band-in-a-Box — ">4,400 hours" of RealTracks, "202 new sets," AI-Notes transcriber, 1990 origin, RealTracks since 2007. Matches `notes/07`, `notes/08` (Soloist 1997 / RealDrums 2006 / ACW 2007 all present in `notes/08`). **OK**
15. §2.3 Korg i3 — "48 styles each with four variations, two fills and two intros/endings," 16-track sequencer, "about $2,500," hedged "credited with inspiring." Matches `notes/07`. **OK**
16. §2.1 Koenig — "Project 1 (1964) and Project 2 (1966), **as commonly dated**" preserves the note's `unverified (recall; dates widely cited)`. **OK (exemplary)**
17. §2.1 McIntyre / *Bach by Design* — carries the explicit hedge "recorded in the notes from recollection rather than a fetched source," matching `unverified (recall)`. **OK (exemplary)**
18. §3.1 Morai Maker — ">100 participants (91 in the controlled study)," role split. Matches `notes/05`. **OK**
19. §3.2/§9.4 Design Space for Live Music Agents — 731 screened, 184 coded (153 papers + 31 videos), 89.8% agreement, 31 dimensions, 165 codes, ~5% ecosystem. Matches `notes/01`, `notes/02`. **OK**
20. §4.1 Aria-MIDI — "1,186,253 files (~100,629 hours) transcribed from YouTube, again non-commercial." Matches `notes/07` exactly; CC-BY-NC-SA in §6.8/§13.1 matches. **OK**
21. §4.1 Sheet Music Transformer — CER −91.8%, LER −89.1%, GrandStaff 53,882, Quartets 38,051, oemer MIT, Audiveris AGPL-3.0. Matches `notes/06`. **OK**
22. §4.1 unified cross-modal translation — ">1,300-hour YouTube Score Video," SER 24.58% → 13.67%, first score-image-conditioned audio generation (this primacy claim *is* in the note). Matches `notes/02`. **OK**
23. §4.2 Ghias et al. — 183-song MIDI database, 10–12 pitch transitions discriminating 90%. Matches `notes/06`. **OK**
24. §4.2 HumTrans — 56.22 h, 1,000 segments hummed twice, ten music-trained students, 6.8% validation / 5.7% test note F1. Matches `notes/06`. **OK**
25. §4.6/§13.1 Dynamic HumTrans — "~0.67 note F1" against the note's 0.673 octave-invariant note+onset F1. **OK**
26. §4.2 VocalSketch — 4,429 imitations, 248 contributors, 0.80 / 0.45 / 0.42–0.54. Matches `notes/06`. **OK**
27. §4.4/§10.1 Amuse — every figure checks out against `notes/02`, including the ones easy to garble: 6.20 vs 4.60 (p<.01), 5.80 vs 4.40, 17.4 vs 17.6 min, 45 listeners / 900 pairwise judgements, p=.009 vs raw GPT-4o, 58% keyword relevance, M=7.64, 25,000 GPT-4o progressions, 50-hour Hooktheory prior. **OK (the most accurately reported study in the review)**
28. §5.1 Dezrann — 35,000+ annotations, 1,500+ pieces, ten corpora, GPLv3+ code / ODbL data, `.dez` JSON, measure-and-beat anchoring. Matches `notes/06`. **OK**
29. §5.2 AugmentedNet — 82.9% key, 67.0% scale degree, 46.4% full Roman numeral, adoption in Sibelius. Matches `notes/07`. **OK**
30. §5.5/§13.1 Just Label the Repeats — measure-level alignment 33% → 82% via a clickable repeat-labelling UI. Matches `notes/02`. **OK**
31. §5.4/§8.1 ExpressEdit — 176 requests from ten editors, 78/97 sketched, temporal recall 0.68 / spatial mIoU 0.56 / operation F1 0.82, 45.98% accepted, 58.09% modified, SUS 75.7, Examine 6.1/7, sketches in 26%. Matches `notes/02`. Correctly *not* attributed to CMU (the note flags "Not CMU"). **OK**
32. §5.4/§6.6 Not that Groove — 89% TPR / 94% TNR expert-test agreement, best of eight models 68%. Matches `notes/03`. **OK**
33. §6.2 DeepBach — "roughly 1,270 participants," pseudo-Gibbs, MuseScore plugin. Matches `notes/03` ("~1,270"). **OK**
34. §6.2/§6.8 Anticipatory Music Transformer — 128M–780M checkpoints, Apache 2.0, Lakh training, twenty-second accompaniments rated comparably to human music. Matches `notes/03`. **OK**
35. §6.6 Decomposer — 21,174 pairs, 688 public Strudel programs, compile 0.99 vs 0.75–0.82, onset F1 0.60 vs 0.27–0.28, 0.58 vs 0.21–0.23 multi-instrument, readability 0.61–0.74 vs 0.09/0.29–0.36, "There was no user study." Matches `notes/02` down to the ablation caveats. **OK (exemplary)**

Also spot-checked and clean: §6.7 PianoFlow (2,968 h, 26 listeners, 708 ratings, 67.1% win, 54% over human recordings); §6.5 AccoMontage2 (72 participants, p<0.05, musicality p=0.053); §7.2 Music ControlNet (49% / 35× / 11×, no code); §7.3 Ronchini et al. (17 producers, seven countries, 94% ideation); §9.3 ReaLchords (5,041-chord vocabulary, ~38k pairs, 37.0%→54.3%, ten musicians / 192 comparisons); §9.3 GAPT (~85% note-in-chord, 12 experts, p<0.05); §9.3 MIDInfinite (51 notes/s, 72.9% / 86.3%); §10.1 MMM-C (18 composers, SUS 73.8–75.7, control 5.2/10 vs desire 9.5/10); §10.1 ReaLJam (N=6, 4.3/5, 2.7/5, five of six); §10.4 Deezer/Ipsos (9,000 adults, eight countries, 97%, 80%, 65%); §10.4 Grötschla et al. (15,000 comparisons, 2,500 raters, 6,000 songs, twelve generators); §10.6 ABC-Eval (1,086 items, ten sub-tasks, seven models, >90% syntax); §11.1 Verovio (C++20, dual LGPL-3.0/GPL-3.0, v6.2.0 May 2026, timemap); §11.4 PDMX / OpenScore / GiantMIDI / ATEPP / MetaMIDI / LA-MIDI (all counts, hours and licences correct); §12.3 Spotify (25 September 2025, 75 million tracks, DDEX); §12.3 Michael Smith ($8.09M, ~1,040 bot accounts, guilty plea 19 March 2026, MLC detection); §12.3 Deezer telemetry (~10% Jan 2025 → >50% peak June 2026, ~90,000/day); §1.4 *Thaler* (certiorari denied March 2026).

---

# 2. Hedging discipline

`grep` of `notes/*.md` finds **82 `partial` and 5 `unverified`** entries (85 distinct BibKeys; 76 keys have *no* verified note anywhere). An automated pass for precise figures cited from those keys with no hedging device within the sentence returned 8 raw hits; manual review of the areas the brief named adds 3 more. Eleven breaches follow; the eight named risk areas that **pass** are listed after them, because the review's discipline is generally good and the exceptions are concentrated in law, economics and pre-2016 history.

1. **§11.4 (L635) — Lakh MIDI.** "Lakh MIDI, 176,581 files (CC-BY *on the collection*)." `notes/07` verification: `partial (recalled; widely documented)`. Fix: "roughly 176,600 files, reportedly CC-BY on the collection."
2. **§4.1 (L172) and §11.4 (L636) — MAESTRO.** "roughly 200 hours of Disklavier performances with audio under CC-BY-NC-SA"; table: "MAESTRO, ~200 h / 1,276 performances." The hours are hedged; the performance count and the licence are not, and `notes/07` is `partial (recalled)`. Fix: hedge the licence ("reportedly CC-BY-NC-SA") or mark the row `(partial)` as the table already does for DCML and MidiCaps.
3. **§12.2 (L683) — EU AI Act.** Four exact dates and the "sufficiently detailed summary" template attributed to `@eu2024aiact`, whose note is `partial`. Fix: "obligations … have applied since August 2025, with enforcement powers from August 2026 (dates per secondary sources)."
4. **§12.2 (L683) — ELVIS Act.** See finding 12 above; the effective date is both unhedged and absent from the note.
5. **§12.4 (L695) — Goldmedia.** ~$3bn by 2028, 27%, 71%, 95% all flat from a `partial` note, plus the invented day. Fix: "reports … projected" + "in January 2024."
6. **§12.4 (L695) — CISAC/PMP.** "creators risking 24 per cent of revenues" flat from a `partial` note (the €64bn figure is hedged with "roughly"). Fix: "a modelled 24 per cent."
7. **§3.2 (L152) and §9.4 (L509) — Harmonix unit sales.** "selling more than 35 million units," twice, from a note verified `partial`. Fix: "reportedly selling more than 35 million units," and state it once (see redundancy finding 8).
8. **§2.2 (L85) vs §9.1 (L489) — Vercoe's Synthetic Performer.** §9.1 correctly writes "**reportedly** tracked a flautist through pitch and fingering sensors"; §2.2 states the same claim flat. The note is `partial`/recall. Fix: mirror §9.1's hedge in §2.2, or drop the detail there and cross-reference S5.1.
9. **§2.1 (L81) — Eck and Schmidhuber.** "learned 12-bar blues progressions and melodies and kept global form where earlier recurrent networks drifted" stated flat; `notes/08` is `partial`. Fix: "is generally credited with keeping global form where earlier recurrent networks drifted."
10. **§2.1 (L81) — RNN-RBM benchmark provenance.** "introduced the JSB Chorales, MuseData, Nottingham and Piano-midi.de benchmarks that anchored evaluation for a decade" — a strong historiographic claim from a `partial` note. Fix: "popularised" + "reportedly."
11. **§2.2 (L89) / §9.2 (L493) — GenJam and OMax capabilities.** Both entries are `partial`; the review states mechanism and historical significance flat ("is remembered for exposing the *fitness bottleneck*", "practise 'stylistic reinjection'"). §9.2 does hedge the Continuator ("with reported studies"); apply the same treatment to GenJam and OMax.

**Named risk areas that pass (no action needed):**
- **CMU Oros/Telang/Randall** — §10.1 is a model of the practice: it states the finding, then "These claims need care: as of September 2026 the work exists only as a conference poster … no public paper, no effect sizes, no rater counts, and no disambiguation of 'slower'," and marks the SSRN companion as "verified only through its Crossref record." §10.7 and §10.8 both keep the hedge.
- **Education-AI papers** — §10.2 and §11.5 both say "verified only through Crossref metadata and of mixed venue quality … treat them as signals worth replicating, not results." (The separate framing error is finding 6, not a hedging failure.)
- **DAW protocols** — §11.3: "Only one protocol was verified directly: CLAP … VST3, Audio Units, ReaScript, Ableton Link's tempo synchronisation … are recorded as recalled rather than re-verified."
- **Nord Stage** — §11.3: "the Nord Stage family **reportedly** transmits on a global MIDI channel … though this entry is unverified recall."
- **Practice apps** — §11.5: "efficacy studies are few and the entry is partial."
- **Spawning's opt-out figure** — the note carries ">1.5 billion opt-outs reported by 2024 (**unverified figure**)"; §12.3 describes the infrastructure and **omits the number entirely**. Correct call.
- **Newton-Rex signature counts** — §12.3: "roughly 10,500 signatories and later exceeded 50,000; **both entries are partial**."
- **Dataset licences generally** — §11.4 marks DCML, MidiCaps, POP909/Slakh/MusicNet/MedleyDB/MUSDB18 as partial in-line ("all partially verified"), and §11.4's tier table is the right instrument for this.

---

# 3. Contradictions between sections

1. **Earliest notation-surface generative feature — §2.3 vs §6.2 and §13.1.** See check 1, finding 1. *Substantive.* Fix as described there.
2. **Which gap is "the largest" — §8.2 vs §10.1 vs §1.4/§13.1.** §8.2 (L441): "this is the largest single gap the review identifies" (symbolic editing, S4.2). §10.1 (L533): "the largest single gap in this literature" (MMM-C's control desire). §1.4 (L65): the annotation layer is "the studio's genuine white space … the most defensible research contribution available here"; §13.1 G1: "This is the central gap." *Substantive* — three superlatives for three different referents undercuts §13's argument. Fix: keep S2.4 as "the central gap"; rewrite §8.2 as "the largest gap on the *editing* side" and §10.1 as "the largest measured control deficit in this literature."
3. **Hedging of GPT-4 on MusicTheoryBench — §6.6 vs §10.6.** §6.6 (L310) states it flat: "on its own MusicTheoryBench all LLMs including GPT-4 were near chance on *reasoning*." §10.6 (L575) hedges the identical claim: "GPT-4's accuracy on the reasoning split is reported near random (**a figure recalled rather than re-verified**)." Fix: import the §10.6 parenthetical into §6.6, or cross-reference E6 and drop the figure from §6.6.
4. **ACE-Step latency — §7.1 prose vs Table 7.1 (§7.2).** §7.1 (L348): ACE-Step 1.0 "generated up to 4 min of music with vocals in about 20 s on an A100"; only 1.5's "8-step turbo variant renders a full song in under 2 s on an A100." Table 7.1 row (L381) collapses both versions into one line with "<2 s / song on A100." Fix: split the row, or qualify the cell "1.5 turbo: <2 s; 1.0: ~20 s."
5. **Hookpad Aria's timeline and the derived "nine months" — §2.3, §6.2, §10.3, §12.1.** §2.3 dates it "(2024)"; §6.2 "From its March 2024 beta"; §10.3 "From its March 2024 release … roughly 23% acceptance over **about nine months**"; §12.1 gives no date. The notes themselves disagree (`notes/02`: beta March 2024, launch August 2024; `notes/07`: "Aria launched Dec 2024"; `notes/05`: "2023–"), and the "about nine months" window is a derivation that appears in no note and is inconsistent with the Feb 2025 arXiv reporting date. Fix: adopt one canonical framing ("beta March 2024, launch August 2024") in §6.2 and cross-reference it elsewhere; delete "over about nine months" or replace with "over the reporting period to early 2025."
6. **Amuse's listening result reads as a null in §10.1 and a win in §4.4.** §4.4 (L190): the chords "matched the LSTM prior on coherence, exceeded raw GPT-4o (p = .009) and were most preferred for keyword relevance (58%)." §10.1 (L531): "found Amuse's progressions **on a par with** an LSTM harmonic prior for coherence," followed by "multimodal inspiration changes the *experience* of composing measurably and the *artefact* not at all." Dropping the 58% relevance win makes the §10.1 conclusion stronger than the data. Fix: add the relevance result to §10.1 before the conclusion sentence.
7. **SingSong's preference margin — §4.2 vs §7.1.** §4.2: "listeners significantly preferred it to a retrieval baseline"; §7.1: "in roughly 66% of pairwise comparisons." The notes disagree on whether the percentage is confirmed (`notes/02`: "exact percentage not confirmed here"; `notes/04`: "~66%"). Fix: state the figure once, in §7.1, with "reported at roughly 66%."
8. **Suno Studio announcement date.** §12.1: "announced 24 September 2025"; §7.1: "in September 2025 it launched Suno Studio." The notes give 24 September (`notes/08`) and 25 September (`notes/04`). Not a contradiction inside the review, but the sourcing is unresolved. Fix: pick 24 September and note the discrepancy, or write "late September 2025."
9. **§9.5's participant tally mixes study types.** "the evidence base is small (N = 6, 12, 3 and 10 musicians across the four studies with human participants)" — ReaLchords' ten musicians were a *listening* panel (192 pairwise comparisons), not interactive participants, per `notes/01`. Fix: "N = 6, 12 and 3 interactive participants, plus a ten-musician listening panel for ReaLchords."

Explicitly checked and **consistent** across sections: Music ControlNet (§5.3, §7.1, §7.2, §13.1 — 49% / 35× / 11×, partial-in-time controls, no code released); Anticipatory Music Transformer (§1.4, §3.2, §5.3, §6.2, §6.8, §9.3, §12.1, §13.2); MIDI-DDSP (§6.7, §6.8, §7.2 prose and table, §7.4, §13.1 — monophonic URMP, Apache-2.0, three-level hierarchy everywhere); Composer's Assistant (§1.4, §5.3, §6.2, §8.2, §11.3, §11.4, §12.1, §13.1 — REAPER, CC BY 4.0, ten controls, permissive training data, listener parity); Magenta RealTime / Live Music Models (§7.2, §7.4, §9.3, §9.4, §9.5, §13.1 — v1 2-s chunks / ~190k h / 2025 and v2 40-ms frames / ~200 ms / 230M+2.4B / ~71k h / 2026 kept distinct throughout); Suno's feature timeline (§1.1, §7.1, §7.2 table, §7.4, §11.1, §12.1, §12.2, §12.5 — v3 Feb 2024 through v5.5 March 2026, Studio Sept 2025, Studio 2.0 MIDI August 2026, WMG settlement 25 Nov 2025 effective 3 Sept 2026); ExpressEdit (§5.4, §8.1, §8.4, §13.1); RefinPaint (§3.1, §3.2, §5.x, §6.2, §8.2, §8.4, §10.1, §10.8, §13.1 — same figures, same "where before how" characterisation); Aria-MIDI (§4.1, §6.8, §11.4, §12.3, §13.1 — 1.19M files, ~100,629 h, CC-BY-NC-SA everywhere); PDMX (§1.4, §11.4, §12.3, §13.1 — >250k, CC-BY, public-domain-only, though §1.4 and §13.1 pair it with OpenScore's CC0 in a way that could be misread as PDMX being CC0); music21 (§3.2, §5.1, §5.2, §6.6, §11.2, §11.4, §11.5, §11.6, §13.3 — BSD-3, v10.5.0 June 2026, 371 chorales, no MEI export).

---

# 4. Redundancy (12 worst cases)

Each case is two or more subsections covering the same work at comparable length with the same figures, where one should become a cross-reference. Estimated recoverable length in brackets.

1. **§4.4 (S1.4) vs §6.3 (S3.3) — text-to-symbolic generation.** [~250 words] §4.4's third paragraph and §6.3's second paragraph both give MuseCoco (twelve attributes, 1.2B decoder, ~20% control accuracy), Text2midi (272M, 168K MidiCaps, 65.8/54.6, 35.6/14.6), MIDI-LLM (55k tokens, FAD 0.173 vs 0.818, 58 musicians, ~4,000 generations) and MetaScore (963K scores, 22 participants). **Cut §4.4's paragraph** to two sentences on why text is the weakest S1 channel plus "see S3.3"; S3.3 is the taxonomically correct home.
2. **§3.2 (F5) vs §9.4 (S5.4) — Design Space for Live Music Agents.** [~180 words] Both enumerate 731 screened / 184 systems / 153 papers + 31 videos / 89.8% agreement / 31 dimensions / 165 codes / four aspects with their sub-lists / ~5% ecosystem / living database. §9.5 repeats the 5% a third time. **Cut §3.2's to one sentence** ("the first systematic map of real-time human–AI music collaboration, treated in detail under S5.4") and keep §9.4.
3. **§1.4, §2.3, §6.2, §10.3 (+ §6.8, §12.1, §13.1) — Hookpad Aria's telemetry.** [~150 words] The 318,000 / 3,000 / 74,000 / ~23% quadruple is stated in full four times and referenced three more. **Keep §10.3** (E3 is the node for deployed usage data) and reduce §1.4, §2.3 and §6.2 to the acceptance rate plus "(see E3)" — §6.2 already carries a "(see E3)" pointer and repeats the figures anyway.
4. **§6.2 (S3.2) vs §8.2 (S4.2) vs §10.1 (E1) — RefinPaint.** [~150 words] All three give "15 annotators / 50%, 30%, 10% fragment sizes / four amateur composers." §8.2 opens "Three further works reach the same primitive from the compile side and are **treated at length under S3.2**" and then treats them at length again. **Keep §6.2's mechanism and §10.1's study**; cut §8.2's RefinPaint sentence to its cross-reference.
5. **§5.4 (S2.4) vs §8.1 (S4.1) — ExpressEdit and DirectGPT.** [~300 words] §5.4 gives ExpressEdit's full pipeline and all study numbers plus DirectGPT's 50%/50%/72%; §8.1 gives DirectGPT's 50%/50%/72% and ExpressEdit's 45.98%/58.09%/0.68/0.56/0.82/26% again. **Keep §5.4** (S2.4 is the review's declared white space and the natural home) and reduce §8.1 to the *transferable contract* it states so well ("select a region … receive inspectable, editable suggestions"), citing S2.4 for the evidence.
6. **§7.1 (S3.9) vs §8.3 (S4.3) — the "industry converged" material.** [~200 words] Adobe Project Music GenAI Control (same parenthetical list, same "never shipped"), Stable Audio 2.5 (3-min under 2 s, 75 ms on an H100) and Instruct-MusicGen (~8% extra parameters, 5,000 steps, Slakh/MoisesDB) all appear twice. **Keep §8.3** (editing is the operative claim) and reduce §7.1's mentions to one clause each.
7. **§7.2 (S3.8) vs §8.3 (S4.3) — MuseControlLite.** [~120 words] Both give "85M-parameter decoupled cross-attention adapters," RoPE, "melody accuracy 56.6% to 61.1%," "6.75× fewer trainable parameters," inpainting/outpainting, and both call it the best/most practical open starting point. **Keep §7.2**; §8.3 keeps only the inpainting capability.
8. **§3.2 (F5) vs §9.4 (S5.4) vs §11.5 (B5) — Egozy, 21M.385 and Harmonix.** [~200 words] The 21M.385 curriculum (Python/Kivy, synthesis, sequencing, gesture, note highway, public demo concert) is described three times; Guitar Hero/Rock Band with "more than 35 million units" twice. **Keep §11.5** for the course (B5 is the pedagogy node) and §9.4 for the games (S5.4); cut §3.2 to one sentence on the MIT programme.
9. **§5.2 (S2.2) vs §6.4 (S3.4) — Dai and Dannenberg's structure statistics.** [~110 words] 93% phrase-boundary accuracy, 50–90% repeated-phrase coverage, 94% vs 47% cadence rates appear in both, once as percentages and once spelled out. **Keep §5.2** (analysis models) and let §6.4 cite the conclusion only ("deep generators differ strikingly from human pop; see S2.2").
10. **§5.4 (S2.4) vs §6.4 (S3.4) — Libretto.** [~110 words] Both give the text grammar with onset slots, the 29-axis structural fingerprint, and 12% → 39% → 94%. **Keep §6.4** (structure is Libretto's contribution) and let §5.4 keep only the "musician-readable feedback" observation, which is what S2.4 needs.
11. **§5.4 (S2.4) vs §6.6 (S3.6) — Not that Groove.** [~100 words] Both give the drumroll notation, the three instruction types, 89% TPR / 94% TNR and 68%. **Keep §6.6** (LLM editing) and reduce §5.4 to the unit-test lesson.
12. **§6.2 (S3.2) vs §9.3 (S5.3) — MIDInfinite; and §4.5 (S1.5) vs §6.2 (S3.2) — MIDI-RWKV.** [~120 words] MIDInfinite's 51 notes/s and 72.9%/86.3% appear in both §6.2 and §9.3; MIDI-RWKV's state tuning, edge deployment and CC BY 4.0 licence are described twice in near-identical terms. **Keep §9.3** for MIDInfinite (real-time is the point) and **§6.2** for MIDI-RWKV; cross-reference the other.

Two further cases were below the cut but worth noting: §6.6 vs §10.1 (ComposerX's 32.2%/55.4% twice) and §6.2 vs §8.2 (FlowComposer's web lead-sheet editor and eight-bar regeneration finding described twice at similar length).

---

# 5. Taxonomy fidelity

**The review itself is fully conformant.** All 68 `###` subsection headings in §§2–13 either carry a node code or are one of the 19 legitimate non-node headings (§1.1–1.4, the eleven "Implications for the studio" closers required by `WRITER_BRIEF.md`, §10.7, §13.1–13.3). Every node code used — 49 distinct — exists in `taxonomy.md`, and **all 49 taxonomy nodes (F1–F5, S1.1–S1.5, S2.1–S2.5, S3.1–S3.10, S4.1–S4.5, S5.1–S5.4, E1–E6, B1–B5, C1–C4) have a review subsection.** Node-count claims inside the review are all correct against `taxonomy-map.csv`: S4.3=11 vs S4.2=2 (§8.1), S4.4=2 (§8.1, G5), S2.4=4 (G1), S4.5=5 (G6), S3.9=23 (§13 intro).

**Part D ↔ §13.1 is a clean 1:1 mapping.** All twelve Part D gaps appear as G1–G12 in the same order and with the same node attributions, and §13.1 introduces no gap absent from Part D. G5 and G8 add prior art beyond Part D's list (Cococo and ExpressEdit; ScoreCloud and Dubler) — an enrichment, not a divergence.

Four findings, all in the companion files rather than the review:

1. **`taxonomy-map.csv` line for Composer's Assistant is coded to the wrong node.** Row: `03,ComposersAssistant — …,2024,malandro2023composersassistant,**F4**,auto,verified,…`. Composer's Assistant is an infilling system; `taxonomy.md` lists it under **S3.2** (and S2.3, S4.2, C1), and the review treats it there. Fix: recode to S3.2. This is one of the three `auto` rows, and the only one whose node is wrong.
2. **`taxonomy-map.csv` contains a row with node `X`.** Row: `08,ProductTable — Other tools (summary table),,,X,auto,,`. A summary table is not an entry; it inflates the 464 count. Fix: drop the row (and adjust the "464 entries" figure in `taxonomy.md` §1 and §6 to 463), or assign it C1.
3. **`taxonomy-map.csv` `verification` column has four junk values** — `Flat`, `Nierhaus`, `synthesis`, and one empty — where the schema allows `verified|partial|unverified`. These are field-shift artifacts from commas in the source notes. Fix: repair the four rows in `build_map.py`'s output.
4. **`taxonomy.md` §6's "thinnest nodes" list is incomplete.** It names S2.3 (3), S2.4 (4), S2.5 (1), S4.2 (2), S4.4 (2) and S5.1 (1) but omits S1.5 (3) and S5.2 (3), which are equally thin. Not an error in the review (which nowhere claims the list is exhaustive), but the taxonomy's own diagnostic should be complete. Also cosmetic: **§7's subsections run S3.9 → S3.8 → S3.10**, deliberately (the "paradigm to invert" is introduced first) but out of taxonomy order; a half-sentence in §7's framing paragraph should say so, since the review elsewhere claims to "follow Part A's order."

---

# 6. Citation hygiene

**Missing keys: zero.** Extracting every `@key` from `literature-review.md` yields 396 distinct real keys and 1,342 citation instances; all 396 resolve against `references.bib`. (Two apparent misses, `nierhaus2009algorithmic.` at §2.1 L77 and `rezwana2023cofi.` at §8 L415, are narrative citations followed by a sentence-final period — regex artifacts, not errors.)

**Alias keys: zero.** None of the 21 aliases in `bib_aliases.json` (`hooktheory2023aria`, `hooktheory2024aria`, `magenta2025livemusicmodels`, `oros2025generativeai`, `thickstun2023anticipatory`, `wu2026midillm`, …) appears in the review. Every one was correctly resolved to its canonical key. This is the cleanest result in the audit.

1. **Duplicate bib record for VexFlow; the older one is uncited.** `cheppudira2010vexflow` ("VexFlow: A JavaScript library for rendering music notation") and `vexflow2024` ("… notation and guitar tablature") are the same project. §11.1 cites `@vexflow2024`. **Recommendation: drop `cheppudira2010vexflow` from `references.bib`** (or, if the 2010 original is wanted as the historical reference, cite both together in §11.1's VexFlow clause).
2. **`cmu2025musictech` is uncited and has a natural home.** The note is CMU institutional context (Music & Technology programme, Randall, Stiles, Dannenberg's Spring 2025 project list including AMADS and Accomplice), verification `partial`. §3.2 (F5) characterises CMU's music groups and §2.2 covers the Dannenberg line without it. **Recommendation: cite it in §3.2** where the review says the G-CLef lab "is the closest academic analogue of the studio's loop," to support the surrounding claim about which CMU groups do music — or drop it as institutional background that carries no reviewable claim.
3. **`splice2025landr` is uncited while LANDR is named in prose.** §12.3 lists Fairly Trained's "early certifications including Beatoven, Soundful, Kits.ai and LANDR" under `@newtonrex2024fairlytrained` only, and §12.1 discusses Splice Create under `@splice2024create`. **Recommendation: cite `splice2025landr`** alongside `@splice2024create` in §12.1 (it covers the mastering half of the same product family), which also fixes finding 4 below.
4. **Works named in prose with no citation attached.** (a) §12.3: Beatoven, Soundful, Kits.ai and LANDR are named as certified models with only the certifier cited. (b) §6.6 (L308): **Csound, SuperCollider, Faust, Gibber, TidalCycles' mini-notation, Strudel, MPS** and **Tanimoto's liveness levels** are all named in a passage whose only citations are `@wang2015chuck`, `@mclean2014tidal`, `@aaron2016sonicpi` and `@omar2019hazel` — defensible because those bib records are composite `@misc` entries whose `note` fields list the companion systems, but a reader cannot tell which citation covers which system. (c) §11.1 (L607): **Encore (1990)**, **Cakewalk (1987)** and **Noteflight** are named without citations (§2.3 flags the sequencer dates as "partially verified"; §11.1 does not). Fix: add "(covered in the same record)" style signposting in §6.6, or split the composite `@misc` entries.
5. **`@wang2020pop909` is used to cite Wikifonia.** §11.4's tier table: "Wikifonia (site closed 2013) [@wang2020pop909]". The bib record is POP909; the *note* is a composite entry covering JSB Chorales, Nottingham, POP909 and Wikifonia, so the citation traces to a source — but the bibliography will render "POP909" against a claim about Wikifonia. Fix: add a `wikifonia` `@misc` record, or write "Wikifonia (site closed 2013; recorded in the POP909-cluster note)".
6. **Two bib records for one work, both cited: Composer's Assistant.** §6.2 cites `@malandro2023composersassistant` for version 1's 25-participant test; everywhere else uses `@malandro2024composersassistant2`. Both exist in `references.bib` and both are legitimate (ISMIR 2023 and ISMIR 2024 papers), and the note declares both BibKeys — but `taxonomy.md` lists only `malandro2024composersassistant2` as representative, and `taxonomy-map.csv` codes the 2023 key to the wrong node (check 5, finding 1). Fix: keep both citations but add the v1/v2 distinction to `taxonomy.md`'s S3.2 representative list.
7. **`@vercoe1984syntheticperformer` carries Csound.** §2.2 (L85): "Vercoe's Csound (1985–86) compiles an orchestra file and a score file into sound [@vercoe1984syntheticperformer]." The bib record's `note` field does cover Csound ("Csound (1985--86, LGPL): https://csound.com/"), so this resolves — but a reader sees a 1984 conference paper cited for a 1985–86 language. Fix: either split out a `vercoe1986csound` record or say "Vercoe, whose Csound (1985–86) …".

---

# 7. Prose quality (flagged, not fixed)

**Two structural requirements are fully met** and deserve recording: sections 2–13 contain **zero bullet or numbered lists** (all prose plus four legitimate tables — the §7.2 capability matrix, the §11.4 licence tiers, and two smaller comparisons), and there are **zero first-person slips**. An automated scan for `we|our|I|us|my` returns only false positives: "ILLIAC I", "I/O", "Landgericht München I", "Have I Been Trained?", "one's own", and quoted composer-voice phrases in scare quotes ("in my style, subject to my annotations", "everything I wrote is a constraint", "transform what I wrote"). Marketing tone is likewise absent — product claims are consistently attributed ("advertises", "self-reported", "claimed parity with Suno is self-reported").

The problem is sentence length. **116 sentences exceed 60 words.** The thirteen worst:

1. **§12.3 (L691), 112 words** — "The studio's ethical position is therefore implementable rather than aspirational: outputs are symbolic and human-authored, so authorship rests with the composer…". Four independent clauses and five citations; split at "The studio's ethical position is therefore implementable."
2. **§3.2 (L144), 110 words** — "Its line runs from Piano Genie … through the Anticipatory Music Transformer … to the deployed Hookpad Aria … to Amuse …". A four-station itinerary in one breath; split after Hookpad Aria.
3. **§9.3 (L503), 110 words** — Live Music Diffusion Models: architecture, post-training, three capabilities, deployment, latency, participant reactions and a limitation in one sentence. Split at "It offers text-conditioned streaming".
4. **§13.1 (L715), 110 words** — G1's six-part enumeration of "constituent parts … never assembled." The strongest paragraph in §13 and the hardest to read; convert to three sentences (encodings / interaction precedents / control vocabulary).
5. **§9.4 (L507), 107 words** — Design Space: 184 systems, 31 dimensions, 165 codes and four aspects with all sub-lists. Split after "165 codes across four aspects".
6. **§7.1 (L348), 106 words** — ACE-Step 1.5: planner, RL, turbo timings, memory range, four backends, API and VST3. Split after "conditions a DiT decoder".
7. **§8.6 (L477), 106 words** — the synthetic-triple corpus proposal. Split after "inverting known musical transformations".
8. **§12.1 (L671), 105 words** — Hookpad Aria + Composer's Assistant 2 + MIDI-GPT + Scaler 3/Orb/Captain Chords in one sentence.
9. **§5.1 (L216), 105 words** — MEI plus Verovio plus element ids plus timemap plus mei-friend.
10. **§11.2 (L617), 97 words** — MidiTok's ten tokenisations plus BPE/Unigram plus the MMM mapping, then partitura in the same sentence.
11. **§9.3 (L501), 93 words** — Streaming Accompaniment: architecture, latency, future-visibility ablation and conclusion.
12. **§11.1 (L607), 93 words** — OSMD, VexFlow, alphaTab, abcjs and their versions and licences in one sentence.
13. **§1.2 (L45), 92 words** — the cluster-seeding sentence; an em-dash list of eight items inside a sentence that also states the expansion method.

Two claims stated more strongly than the evidence supports (beyond the four UNSUPPORTED primacy claims in check 1):

14. **§11.4 (L639)** — "The Lakh caveat is **the most widely ignored fact in the symbolic literature**." A bibliometric claim the review has not measured; the note says only that Lakh is "the most-used multitrack symbolic training set 2016–2024" with an uneven-quality, grey-zone caveat. Fix: "a caveat the symbolic literature routinely omits."
15. **§8.4 (L461)** — "This subsumes RefinPaint's where-to-modify as a diagnostic, ReaLJam's committed/tentative split as a preview, ExpressEdit's Examine as reference resolution, and Cococo's debugging as an intended workflow." "Subsumes" asserts that an unbuilt design supersedes four evaluated systems. Fix: "would combine … in one surface", matching the more careful "The route through is visible even though no one has taken it" two paragraphs earlier.
