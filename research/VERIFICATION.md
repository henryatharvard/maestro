# Independent verification pass — literature-review.md

Scope: 34 assigned claim clusters, ~70 primary-source lookups (arXiv abstract/HTML pages, ISMIR
proceedings archive, ACM DL, court and agency pages, official project/product pages, PyPI, GitHub).
Line numbers refer to `/home/claude/research/literature-review.md` as of 2026-09-07.

**Headline: 6 of the 8 highest-priority thesis anchors verified exactly. 16 corrections required,
of which 4 are substantive (two numbers wrong, one thesis-bearing overstatement, one legal
sub-fact wrong) and 3 are citations that could not be verified at all.**

---

## Corrections required

### C1. HumTrans "next-best method" figure is simply the wrong row *(substantive)*

**As written (§4.2, line 176):**
> "@gupta2024dynhumtrans corrected HumTrans's onset and offset labels and paired a CNN frame
> classifier with dynamic-programming decoding to reach an octave-invariant note-plus-onset F1 of
> **0.673 against 0.564 for the next-best method**"

**What the source says.** Table 1 of *Dynamic HumTrans*, Note+Onsets column (octave-invariant):
proposed **0.673**; MIR-ST500 **0.604**; VOCANO **0.564**; JDC-STP 0.490; basic_pitch 0.434;
SheetSage 0.170. The next-best method is MIR-ST500 at 0.604. 0.564 is *third*.

URL: https://arxiv.org/html/2410.05455v1

**Replacement text:**
> "...to reach an octave-invariant note-plus-onset F1 of 0.673 against 0.604 for the next-best
> method (MIR-ST500) — a real but modest gain that still leaves roughly one note in three wrong..."

Note the follow-on clause "a large gain" should also soften: 0.673 vs 0.604 is ~11% relative.

---

### C2. The "single digits vs 0.67" juxtaposition compares two different label sets *(substantive)*

**As written (§4.6, line 206):**
> "Purpose-built humming transcription reaches ~0.67 note F1 and **off-the-shelf models single
> digits** [@liu2023humtrans; @gupta2024dynhumtrans]"

**As written (§13.1 G8, line 729):**
> "**Off-the-shelf transcribers reach single-digit note F1** on a clean humming corpus and a
> purpose-built model reaches roughly 0.67 [@liu2023humtrans; @gupta2024dynhumtrans]."

**What the sources say.** Both halves are individually sourced but they are not comparable, and
placing them side by side implies a ~10x model-quality gap that does not exist.

- HumTrans's own baselines, scored against HumTrans's **original** onset/offset labels
  (mir_eval `precision_recall_f1_overlap`, octave-invariant): JDC-STP 6.741% val / 5.667% test;
  MIR-ST500 6.341% / 5.755%; VOCANO 3.194% / 3.352%; Sheet Sage 2.702% / 3.005%.
  https://arxiv.org/html/2309.09623v2
- Gupta et al. found those labels defective, corrected onsets/offsets heuristically, and retained
  only the 52.2% of training and 57% of test samples whose note counts matched. On that
  **corrected** subset the *same* off-the-shelf models score 0.434–0.604 note+onset F1 and
  0.726–0.813 notes-only F1. https://arxiv.org/html/2410.05455v1

The single-digit numbers are therefore largely an artefact of bad ground truth, not of model
incapability. §4.2 (line 176) states this correctly; the two summary sentences drop the caveat.

**Replacement text for line 206:**
> "Purpose-built humming transcription reaches ~0.67 octave-invariant note-plus-onset F1 on
> relabelled data, and off-the-shelf models 0.43–0.60 on the same data — single-digit F1 scores
> reported against HumTrans's original labels reflect defective onset annotation rather than model
> incapability [@liu2023humtrans; @gupta2024dynhumtrans]"

**Replacement text for line 729 (G8):**
> "On a clean humming corpus with corrected onset labels, off-the-shelf transcribers reach
> 0.43–0.60 note-plus-onset F1 and a purpose-built CNN-plus-dynamic-programming model roughly 0.67
> [@liu2023humtrans; @gupta2024dynhumtrans]."

The *argument* — that interactive correction is mandatory — survives either way; roughly one note
in three is still wrong at the state of the art. Only the size of the claimed gap is wrong.

---

### C3. Roman-numeral accuracy is understated by 10–15 points *(substantive)*

**As written (§1.4/§5.2, line 65):**
> "with **Roman-numeral accuracy around 45–50% on full labels** and above 80% on key
> [@napoleslopez2021augmentednet; @sailor2024rnbert]"

**As written (§4.6, line 206):**
> "Roman-numeral labelling **sits near 46%** (S2.2)"

**What the sources say.**
- AugmentedNet (ISMIR 2021), Table 4, best method (RNalt): full Roman-numeral label **51.5%**,
  key **82.9%** on the full test set; per-corpus full-label 47.9%–62.4%.
  https://archives.ismir.net/ismir2021/paper/000050.pdf
- RNBert (ISMIR 2024), Table 4, trained on the complete dataset: full Roman numeral **0.624**,
  key **0.823**. Its reproduction of AugmentedNet gives 0.464 RN / 0.829 key.
  https://malcolmsailor.com/assets/RNBERT_ISMIR_Camera_Ready.pdf

The review's 45–50% band tracks only the *weakest* number in the pair (RNBert's reproduction of
AugmentedNet at 46.4%) and omits the state of the art entirely.

**Replacement text for line 65:**
> "with full-label Roman-numeral accuracy of about 51% for AugmentedNet and 62% for RNBert, and
> key accuracy of 82–83% [@napoleslopez2021augmentednet; @sailor2024rnbert]"

**Replacement text for line 206:**
> "Roman-numeral labelling sits at 51–62% on full labels (S2.2)"

The "correct, don't trust" conclusion is unaffected and arguably better supported by real numbers.

---

### C4. Expressive Communication's finding is stated more strongly than the paper supports *(substantive, thesis-bearing)*

**As written (§3.2, line 142):**
> "Expressive Communication crossed two models with two interfaces (26 composers, 1,020 listener
> comparisons) and found that **steering interfaces moved composer control, ownership and
> self-efficacy more than a stronger model did**, while the stronger model improved listener-judged
> musicality: the two are complementary [@louie2022expressive]."

**And the propagated form (§13, line 753):**
> "The controlled studies found **steering to matter more than model strength**
> [@louie2020cococo; @louie2022expressive]."

**What the source says.** The paper's own headline statement is symmetric, not ranked:
> "both better steering interfaces and more expressive models make a difference in composer's
> feelings of empowerment (i.e., control, ownership, efficacy) and their effectiveness in creating
> music that evokes the intended feelings and that sounds more musical to outside listeners."

URL: https://arxiv.org/html/2111.14951v1 (venue confirmed: IUI '22, DOI 10.1145/3490099.3511159)

The counts (26 composers; 1,020 comparisons = 20 listeners × 51 pairs) are exactly right. The
*complementarity* claim is right. The *ranking* — interface > model on empowerment — is the
review's inference and is not what the paper reports. This matters because line 753 uses it as one
of the review's five load-bearing conclusions, and it is the single claim a reviewer of this
document is most likely to check.

**Replacement text for line 142:**
> "Expressive Communication crossed two models with two interfaces (26 composers, 1,020 listener
> comparisons) and found that better steering interfaces and more expressive models each
> independently improved composer control, ownership and self-efficacy as well as listener-judged
> musicality — the two are complementary rather than substitutes [@louie2022expressive]."

**Replacement text for line 753:**
> "The controlled studies found that steering interfaces move composer control, ownership and
> self-efficacy even when the model is held fixed, and that interface and model gains are
> complementary [@louie2020cococo; @louie2022expressive]."

---

### C5. GEMA v. Suno: the January date was a *cancelled* hearing, not a hearing *(legal detail)*

**As written (§12.2):**
> "On 31 July 2026 the same chamber decided GEMA v. Suno — the judgment is July 2026, **the January
> date sometimes reported being the oral hearing** — over outputs resembling well-known catalogue
> songs..."

**What the source says.** LG München I press release **1/2026 of 20 January 2026** (42 O 763/25):
the oral hearing scheduled for **26 January 2026** was *postponed* after the defendant filed a
recusal motion (rejected, but the appeal period was still running) and **rescheduled to Monday
9 March 2026**. So no January hearing took place. Judgment: press release **16/2026 of
31 July 2026**, case **42 O 763/25**.

URLs:
- https://www.justiz.bayern.de/gerichte-und-behoerden/landgericht/muenchen-1/presse/2026/1.php
- https://www.justiz.bayern.de/gerichte-und-behoerden/landgericht/muenchen-1/presse/2026/16.php

**Replacement text:**
> "On 31 July 2026 the same chamber decided GEMA v. Suno (42 O 763/25); the oral hearing originally
> set for 26 January 2026 was postponed over a recusal motion and heard on 9 March 2026, which is
> why January dates are sometimes reported for this case..."

Everything else in that sentence is confirmed by the court's press release: memorisation as a §16
UrhG reproduction, §44b inapplicable, stream-ripping circumventing YouTube's rolling cipher, and
Suno rather than the prompting user liable.

---

### C6. The Finale quotation is not verbatim

**As written (§2.3, line 95):**
> "MakeMusic discontinued Finale on 26 August 2024, stating that **"millions of lines of code" made
> improvement "exponentially harder,"** and offered a $149 Dorico crossgrade"

**What the source says (press release, 26 August 2024):**
> "Today's massive codebase—millions of lines accumulated over decades—has exponentially increased
> the challenge of delivering customer value."

The phrase "exponentially harder" appears nowhere and should not sit inside quotation marks.
The crossgrade is $149 for **Dorico Pro** (list $579), for owners of any Finale version or Finale
PrintMusic.

URL: https://www.makemusic.com/press-room/press-releases-2024/makemusic-sunsets-finale/

**Replacement text:**
> "MakeMusic discontinued Finale on 26 August 2024, stating that its "massive codebase — millions of
> lines accumulated over decades — has exponentially increased the challenge of delivering customer
> value," and offered Finale owners a $149 crossgrade to Dorico Pro (list $579)"

(Date and $149 figure are both confirmed; only the quotation needs fixing. §11.1 line 611 restates
the same facts without the quotation and needs no change.)

---

### C7. music21's Python requirement is 3.11, not 3.12

**As written (§11.2, line 615):**
> "v10.5.0 (June 2026) is BSD-3-Clause **on Python 3.12 or later**"

**What the source says.** music21 **10.5.0**, released **17 June 2026**; classifier "OSI Approved ::
BSD License", BSD 3-clause; **Requires: Python >=3.11**.

URL: https://pypi.org/project/music21/

**Replacement text:**
> "v10.5.0 (17 June 2026) is BSD-3-Clause on Python 3.11 or later"

---

### C8. "Human-AI Resonance group" / "HAI-Res lab" is not an attested name

**As written (§3.2, line 142):**
> "Since 2024 her **Human-AI Resonance group** at MIT has turned toward RL-tuned jamming agents"

**As written (§9.4, line 507):**
> "Both sit within MIT's Music Technology and Computation programme and **Huang's HAI-Res lab**,
> whose stated method is weekly co-design with musicians"

**What the sources say.** No lab or group name appears on either of Huang's official MIT pages or
in MIT News's June 2026 feature on her students' work. Her listed identity is: **Robert N. Noyce
Career Development Professor**; **Associate Professor**, shared appointment between **EECS** and
**Music and Theater Arts**. "In Search of Human-AI Resonance" is the title of an MIT Alumni
Association talk, not a lab name. "HAI-Res" returns no institutional page at all.

URLs:
- https://www.eecs.mit.edu/people/cheng-zhi-anna-huang/
- https://mta.mit.edu/person/anna-huang
- https://news.mit.edu/2026/inaugural-mit-music-technology-research-showcase-celebrates-work-students-0629

**Replacement text for line 142:**
> "Since arriving at MIT in Fall 2024 — where she is Robert N. Noyce Career Development Professor
> with a shared appointment in EECS and Music and Theater Arts — her group has turned toward
> RL-tuned jamming agents"

**Replacement text for line 507:**
> "Both sit within MIT's Music Technology and Computation programme and Huang's research group,
> whose stated method is weekly co-design with musicians"

Do not print "HAI-Res" as a lab name unless a primary MIT page can be produced for it.

---

### C9. MIT MTC: the ten-student figure is the 2026–27 intake, not the first cohort

**As written (§3.2, line 142):**
> "It sits inside MIT's Music Technology and Computation programme, launched Fall 2024 with Egozy as
> director, which **held its first showcase in May 2026 and admitted ten students from more than a
> hundred applicants**"

**What the source says (MIT News, 29 June 2026).** Inaugural Music Technology Research Showcase:
**13 May 2026**. First cohort: **five** master's students, all former MIT undergraduates. For
**2026–27**: over 100 applicants, **ten** admitted. Egozy is "MTC Director and professor of the
practice of music" — the review's "Egozy as director" is correct. Program launched Fall 2024
(announced 27 September 2024; first class enrolled Fall 2025).

URL: https://news.mit.edu/2026/inaugural-mit-music-technology-research-showcase-celebrates-work-students-0629

**Replacement text:**
> "...launched Fall 2024 with Egozy as director, which held its first showcase on 13 May 2026 with a
> founding cohort of five and admitted ten students from more than a hundred applicants for 2026–27"

---

### C10. Magenta RealTime 2: Max/PD/SuperCollider bindings unverified

**As written (§9.3, line 503):**
> "Magenta RealTime 2 (June 2026) cut control latency about 15-fold to roughly 200 ms with 40-ms
> frames and causal sliding-window attention, runs in real time on Apple Silicon (230M and 2.4B
> models) with a C++ engine, DAW integration **and Max/PD/SuperCollider bindings**"

**What the source says.** Release **4 June 2026**. Control latency ~3 s → **~200 ms** (the 15-fold
claim is right). Models **230M** and **2.4B**. "An inference engine written in C++, enabling
efficient streaming audio generation on a MacBook GPU via MLX", a suite of example applications,
and DAW drop-in. Text/Audio/MIDI control confirmed; open weights on Hugging Face confirmed.
**No mention of Max, Pure Data or SuperCollider bindings.**

URL: https://magenta.withgoogle.com/magenta-realtime-2

**Replacement text:** delete "and Max/PD/SuperCollider bindings", or replace with "and a suite of
example applications built on that engine". Also set the date precisely to 4 June 2026.

---

### C11. MMM-C SUS range is 71.4–75.7, not 73.8–75.7

**As written (§3.2, line 150):** "it scored SUS 73.8–75.7"

**What the source says.** SUS by task: **73.75** (T1), **75.71** (T2), **71.43** (T3). Ease of
control **5.23/10**; desire for more control **9.54/10**; **18** expert composers (8 hobbyist,
10 professional) — all three of the review's other figures confirmed.

URL: https://arxiv.org/html/2504.14071v1

**Replacement text:** "it scored SUS 71.4–75.7 across three tasks"

---

### C12. Google/Producer.ai: acquisition and rebrand are separate events, months apart

**As written (§12.1, line 669):**
> "...and **the February 2026 acquisition of Producer.ai — formerly Riffusion — relaunched as Google
> Flow Music**"

**What the source says.** The acquisition was announced **24 February 2026**, bringing ProducerAI
(formerly Riffusion) and its team into Google Labs and Google DeepMind. The rebrand to **Google
Flow Music** was reported separately in **April 2026** (9to5Google, 20 April 2026 — already in the
bib note for `forsgren2022riffusion`).

URL: https://www.musicbusinessworldwide.com/google-acquires-ai-music-platform-and-suno-challenger-producerai/

**Replacement text:**
> "...and the acquisition of Producer.ai — formerly Riffusion — announced on 24 February 2026 and
> rebranded as Google Flow Music that April"

---

### C13. Deezer's fraud figure is "up to 85%" and refers to 2025

**As written (§12.3):**
> "while they draw only 1 to 3 per cent of streams, **approximately 85 per cent of those streams are
> fraudulent**"

**What the source says (Deezer newsroom, 21 July 2026).** "90,000 AI-generated tracks per day now
represent over 50% of all new music uploads on Deezer at peak level in June, 2026"; fully-AI music
accounts for 1–3% of listening; **up to 85%** of streams generated by fully-AI tracks were
identified as fraudulent **in 2025** and demonetised.

URL: https://newsroom-deezer.com/2026/07/ai-music-exceeds-50-percent-daily-uploads-deezer/

**Replacement text:**
> "while they draw only 1 to 3 per cent of streams, up to 85 per cent of those streams were
> identified as fraudulent in 2025 and demonetised"

(The >50%/June 2026/~90,000-a-day figures in the same sentence are confirmed exactly, as is the
whole descending series in the bib note.)

---

### C14. Verovio's current release is 6.2.1

**As written (§11.1, line 611):** "a C++20 library (dual LGPL-3.0/GPL-3.0, **v6.2.0 May 2026**)"

**What the source says.** v6.2.0 released 20 May 2026; **v6.2.1 released 22 May 2026** is the
current release. Dual LGPL-3.0/GPL-3.0 confirmed.

URLs: https://github.com/rism-digital/verovio/releases · https://github.com/rism-digital/verovio

**Replacement text:** "(dual LGPL-3.0/GPL-3.0, v6.2.1 May 2026)". Same fix in the
`pugin2014verovio` bib note.

---

### C15. Cococo author order in the prose — already correct, do not "fix" it

Flagged here because the verification brief itself listed the authors as "Louie, Huang, Cai, White,
Terry". That is wrong. The paper is **Ryan Louie, Andy Coenen, Cheng Zhi Huang, Michael Terry,
Carrie J. Cai** — exactly as §10.1 line 527 and the bib have it. There is no author named White.
No change needed; resist any edit in this direction.

URL: https://youralien.github.io/files/cococo_chi2020_copy.pdf

---

### C16. Suno download caps: no primary source located — hedge or cite

**As written (§7.1, line 342):**
> "...a non-downloadable free tier and monthly download caps, **which took effect on 3 September
> 2026 (Free 7 lifetime, Pro 20/month, Premier 60/month)** [@wmg2025suno; @suno2026]"

The Warner settlement half is confirmed (see Confirmed table). The cap *numbers and date* are not:
Suno's own release notes contain no download-cap entry, and `help.suno.com` returned 404 on the
article path tried. Seven independent secondary write-ups all agree on 3 September 2026 / Free 7
lifetime / Pro 20 / Premier 60, so the figures are probably right, but `@suno2026` (the release-notes
page) does not support them.

**Replacement text:**
> "...a non-downloadable free tier and monthly download caps, reported to have taken effect on
> 3 September 2026 at 7 lifetime downloads on Free, 20 a month on Pro and 60 on Premier; the caps
> are documented in Suno's subscription help pages rather than its release notes"

and add a citation to the Suno help-centre download-limits article (or mark the figures partial in
the bib note), rather than resting them on `@suno2026`.

---

## Confirmed

| Claim (review location) | Verdict | Source URL |
|---|---|---|
| Coconet = Huang, Cooijmans, Roberts, Courville, Eck; ISMIR 2017, Suzhou (§2.1) | Confirmed | https://archives.ismir.net/ismir2017/paper/000187.pdf |
| Coconet abstract contains "human composers write music in a nonlinear fashion, scribbling motifs here and there, often revisiting choices previously made" (§1.4, §2.1, §6.2) | Confirmed verbatim | https://arxiv.org/abs/1903.07227 |
| Cococo N=21 novices, within-subjects, 7-point scales (§10.1) | Confirmed (21 novices, 12F/9M, ages 20–52) | https://youralien.github.io/files/cococo_chi2020_copy.pdf |
| Cococo controllability 5.9 vs 3.5; ownership 5.2 vs 3.8 (§4.5, §5.3, §10.1) | Confirmed exactly | same |
| Cococo comprehensibility 5.3/3.2, self-efficacy 5.9/3.7, collaboration 5.9/4.0, creative expression 5.5/3.8; all p<0.01 (§10.1) | Confirmed (p from 0.0071 to <0.0001, BH-corrected) | same |
| Cococo authors: Louie, Coenen, Huang, Terry, Cai; CHI 2020 (§10.1) | Confirmed | same |
| Expressive Communication = Louie, Engel, Huang; IUI '22, pp. 405–417, DOI 10.1145/3490099.3511159 (bib) | Confirmed | https://dl.acm.org/doi/10.1145/3490099.3511159 |
| Expressive Communication: 26 composers, 1,020 listener comparisons (§3.2, §10.1) | Confirmed (20 listeners × 51 pairs) | https://arxiv.org/html/2111.14951v1 |
| Amuse = Kim, Lee, Donahue; CHI 2025, Yokohama (§3.2) | Confirmed | https://yewon-kim.com/amuse/ |
| Amuse **Best Paper Award** (top 1% of submissions) (§3.2) | Confirmed via author CV | https://yewon-kim.com/uploads/CV_YewonKim.pdf |
| Amuse N=10 songwriters (8 hobbyist, 2 professional), within-subjects, randomised order (§3.2, §4.4) | Confirmed | https://arxiv.org/html/2412.18940v2 |
| Amuse: no significant difference in output quality or completion time (§3.2, §4.4) | Confirmed (time: 17.39±5.45 vs 17.61±5.27 min, p=0.922; quality items p=0.429–1.00) | same |
| Amuse listening study: 45 listeners, beat GPT-4o p=.009, 58% keyword-relevance preference (§4.4) | Confirmed | same |
| Hookpad Aria: 318k suggestions, 74k accepted, 3k users, since March 2024 (§1.4, §2.2, §6.2, §10.3) | Confirmed verbatim: "since its release in March 2024, Aria has generated 318k suggestions for 3k users who have accepted 74k into their songs" | https://arxiv.org/abs/2502.08122 |
| Hookpad Aria = ISMIR 2024 late-breaking demo (bib) | Confirmed | same |
| Anticipatory Music Transformer = Thickstun, Hall, Donahue, Liang; TMLR (§5.3, §6.2, bib) | Confirmed | https://arxiv.org/abs/2306.08620 |
| AMT anticipation = interleaving controls after stopping times so any subset of events can be pinned (§5.3) | Confirmed from abstract | same |
| GEMA v. OpenAI, LG München I, 11 Nov 2025, 42 O 14139/24 (§12.2) | Confirmed | https://dejure.org/dienste/vernetzung/rechtsprechung?Gericht=LG+M%C3%BCnchen+I&Datum=2025-11-11&Aktenzeichen=42+O+14139%2F24 |
| GEMA v. Suno judgment **31 July 2026**, LG München I, 42 O 763/25 (§12.2) | Confirmed (see C5 for the January sub-fact) | https://www.justiz.bayern.de/gerichte-und-behoerden/landgericht/muenchen-1/presse/2026/16.php |
| GEMA v. Suno holdings: memorisation = §16 reproduction; §44b inapplicable; stream-ripping circumvented the rolling cipher; Suno liable, not the prompting user (§12.2) | Confirmed | same |
| Thaler v. Perlmutter, cert denied **2 March 2026**, No. 25-449 (§12.2) | Confirmed ("Petition DENIED", 2 Mar 2026) | https://www.supremecourt.gov/search.aspx?filename=/docket/docketfiles/html/public/25-449.html |
| USCO *Copyright and AI* Part 2 (Copyrightability), January 2025 (§12.2) | Confirmed | https://content.govdelivery.com/accounts/USLOCCOPYRIGHT/bulletins/3d0f30f |
| USCO Part 3 (Generative AI Training) still only a **pre-publication version** as of Sept 2026 — the review's hedge is correct (§12.2) | Confirmed | https://www.copyright.gov/ai/Copyright-and-Artificial-Intelligence-Part-3-Generative-AI-Training-Report-Pre-Publication-Version.pdf |
| UMG–Udio settlement 29 Oct 2025 (§12.2) | Confirmed | https://www.musicbusinessworldwide.com/universal-music-settles-udio-lawsuit-strikes-deal-for-licensed-ai-music-platform/ |
| WMG–Suno settlement **25 Nov 2025**; licensed models in 2026, deprecation of existing models, artist opt-in, non-downloadable free tier, paid-tier download caps (§7.1, §12.2) | Confirmed | https://www.musicbusinessworldwide.com/warner-music-group-settles-with-suno-strikes-first-of-its-kind-deal-with-ai-song-generator/ |
| WMG–Udio ~19 Nov 2025 (§12.2) | Confirmed indirectly ("last week" relative to 25 Nov) | same |
| Sony/UMG v. Suno **still live**, D. Mass. 1:24-cv-11611; Warner no longer a plaintiff (§12.2) | Confirmed (June 2026 briefing on plaintiffs' second motion to amend) | https://www.musicbusinessworldwide.com/files/2026/06/UMG-Sony-v-Suno-DEFENDANT-SUNO-INC.S-OPPOSITION-TO-PLAINTIFFS-SECOND-MOTION-FOR-LEAVE-TO-AMEND-COMPLAINT-.pdf |
| Suno Studio 2.0 with MIDI, August 2026 (§7.1) | Confirmed (13 Aug 2026: "totally overhauled Suno Studio… **MIDI:** Import, record and edit MIDI directly on the timeline") | https://suno.com/release-notes |
| Google acquired Producer.ai/Riffusion, February 2026 (§7.1, §12.1) | Confirmed 24 Feb 2026 (rebrand date needs C12) | https://www.musicbusinessworldwide.com/google-acquires-ai-music-platform-and-suno-challenger-producerai/ |
| Finale discontinued 26 Aug 2024; $149 Dorico crossgrade (§2.3, §11.1) | Confirmed ($149 → Dorico Pro, list $579); quotation needs C6 | https://www.makemusic.com/press-room/press-releases-2024/makemusic-sunsets-finale/ |
| Deezer: AI >50% of daily uploads at peak, June 2026, ~90,000/day; 1–3% of streams (§12.3) | Confirmed | https://newsroom-deezer.com/2026/07/ai-music-exceeds-50-percent-daily-uploads-deezer/ |
| Anna Huang: MIT, joint EECS + Music and Theater Arts, **Robert N. Noyce Career Development Professor**, arrived Fall 2024 (§3.2) | Confirmed | https://www.eecs.mit.edu/people/cheng-zhi-anna-huang/ · https://news.mit.edu/2024/new-mit-music-technology-computation-graduate-program-0927 |
| Chris Donahue: **Dannenberg Assistant Professor**, CMU Computer Science Dept; leads **Generative Creativity Lab (G-CLef)**; part-time Research Scientist at Google DeepMind on Magenta (§3.2, §6.6) | Confirmed | https://chrisdonahue.com/ |
| MIT Music Technology and Computation launched Fall 2024, **Egozy as MTC Director** (§3.2) | Confirmed (cohort figures need C9) | https://news.mit.edu/2026/inaugural-mit-music-technology-research-showcase-celebrates-work-students-0629 |
| music21 v10.5.0, June 2026, BSD-3-Clause (§11.2) | Confirmed (Python version needs C7) | https://pypi.org/project/music21/ |
| Verovio dual LGPL-3.0/GPL-3.0, v6.2.x May 2026 (§11.1) | Confirmed (point release needs C14) | https://github.com/rism-digital/verovio |
| "Just Label the Repeats": alignment accuracy 33% → 82%, +150% relative (§8.x) | Confirmed verbatim: "improve alignment accuracy by 150% relative to prior work (33% to 82%)" | https://arxiv.org/abs/2411.07428 |
| HumTrans: 56.22 h, 1,000 segments hummed twice by ten music-trained students (§4.2) | Confirmed | https://arxiv.org/abs/2309.09623 |
| HumTrans best off-the-shelf 6.8% val / 5.7% test note F1 (§4.2) | Confirmed (JDC-STP 6.741% / 5.667%) — but see C2 on how it is summarised | https://arxiv.org/html/2309.09623v2 |
| Decomposer = Kim, Gandhi, Chung, Neubig, Donahue; 2026 preprint, arXiv 2607.01849 (§3.2, §5.4, §6.6) | Confirmed | https://yewon-kim.com/decomposer/ · https://yewon-kim.com/uploads/CV_YewonKim.pdf |
| Decomposer: compile rate **0.99**; onset F1 **0.60** on LMD (8B) vs **0.27** GPT-5.5 / 0.28 Claude-Opus-4.6; Strudel target; **no user study** (§6.6) | Confirmed exactly | https://arxiv.org/html/2607.01849 |
| PDMX: >250k public-domain MusicXML from MuseScore, CC BY 4.0, ICASSP 2025 (§1.4, §11.4) | Confirmed | https://arxiv.org/abs/2409.10831 |
| Aria-MIDI: **1,186,253** files, **~100,629 h**, CC-BY-NC-SA 4.0, ICLR 2025 (§4.1, §11.4) | Confirmed exactly | https://github.com/loubbrad/aria-midi |
| DirectGPT: "50% faster and relied on 50% fewer and 72% shorter prompts"; CHI 2024 (§5.4, §8.6) | Confirmed verbatim | https://arxiv.org/abs/2310.03691 |
| ExpressEdit: 45.98% of suggestions accepted; 58.09% of final edits were modified suggestions; SUS 75.7; Examine 6.1/7; sketches in ~26% of commands; temporal recall 0.68 / spatial mIoU 0.56 / operation F1 0.82; IUI 2024 (§5.4) | Confirmed exactly, every figure | https://arxiv.org/html/2403.17693v1 |
| CMU Oros / Telang / Randall: **140** musically trained participants; Udio-assisted vs unassisted 15-second melodies; AI-assisted rated slower, fewer notes, less creative; **poster only** (CODE@MIT, Nov 2025), unpublished (§10.1, §10.2) | Confirmed — the review's poster-only characterisation is correct | https://www.cmu.edu/news/stories/archives/2026/january/as-ai-generated-music-advances-humans-still-lead-in-creativity-cmu-research-finds |
| MMM-C: 18 expert composers; ease of control 5.23/10; **desire for more control 9.54/10** (§3.2, §6.2) | Confirmed (SUS range needs C11) | https://arxiv.org/html/2504.14071v1 |
| APRA AMCOS, 19 Aug 2024, 4,200+ respondents: 54% AI can assist; 82% fear for livelihood; 97% want policy attention and training-data disclosure; 95% require permission; 23% of revenue at risk by 2028 (§12.4) | Confirmed, all figures | https://www.apraamcos.com.au/about-us/news-and-events/ai-in-music-report |
| Magenta RealTime 2: June 2026, ~200 ms control latency (from ~3 s, i.e. ~15×), MIDI note input, open weights, 230M + 2.4B, C++/MLX engine, DAW integration (§9.3) | Confirmed (bindings claim needs C10) | https://magenta.withgoogle.com/magenta-realtime-2 |
| ACE-Step 1.5: **MIT licence**; 2B DiT base + 4B XL (released 2 Apr 2026) + LM 0.6B/1.7B/4B; **VST3 plugin** (C++/GGML) (§7.2) | Confirmed | https://github.com/ace-step/ACE-Step-1.5 |
| REAL (github.com/This-Goober/REAL) is a **video-editing** pipeline (LLM-aided drafting, storyboarding, compile to FCPXML), MIT licence, **no music generation** (bib) | Confirmed — the notes' conclusion is right, the founder's "music seed" label was wrong | https://github.com/This-Goober/REAL |

---

## Could not verify

**1. "Help That Hurts" (SSRN working paper), cited twice — `@oros2026helpthathurts`.**
DOI `10.2139/ssrn.6481538` did not resolve (429 from doi.org on retry), and a title-plus-author
search returns **no SSRN record at all** — only CMU/Heinz College/phys.org coverage of the
CODE@MIT poster study. The review currently treats it as a *separate* result:

> §10.1: "the related SSRN working paper "Help That Hurts" [@oros2026helpthathurts] was verified
> only through its Crossref record"
> §10.6: "whose "help that hurts" finding — AI ideation reducing the quality and originality of
> student composition output — is directionally consistent with the CMU experiment"

**Risk:** if this is the write-up of the *same* Oros/Randall/Telang experiment as
`@oros2026cmu`, the review is double-counting one unpublished study as two mutually corroborating
ones — and §10.6 leans on that corroboration. Same three authors, same finding, same period, and
CMU News says Oros was still to defend in May 2026.
**Recommendation:** either produce the SSRN landing page, or collapse the two citations into one
and delete "directionally consistent with the CMU experiment" from §10.6. Do not present it as
independent support. Since this is the founder's own seed, precision here matters most.

**2. Suno download-cap numbers and the 3 September 2026 effective date.**
No primary Suno page found (release notes silent; `help.suno.com` path 404). Seven secondary
write-ups agree on the figures. See C16 for the hedged replacement text.

**3. Google Flow Music rebrand date from a first-party page.**
Confirmed only through 9to5Google (20 April 2026) and aggregators; no Google announcement page
located. Keep the April 2026 date attributed to the trade press.

**4. APRA AMCOS "89 per cent of Aboriginal and Torres Strait Islander creators fearing cultural
appropriation" (§12.4).** Not present in the report's summary page, though every other figure in
that sentence was confirmed there. Likely inside the full PDF. Either cite the PDF page or hedge.

**5. Cococo's formative study of eleven participants and the "two 15-minute pieces" protocol
(§10.1).** Not located in the fetched text of the paper. Low risk, but unverified.

**6. MMM-C venue.** The review's bib gives IJCAI-23 with DOI 10.24963/ijcai.2023/640, which is a
valid IJCAI DOI form; the arXiv HTML rendering suggested a different venue. The DOI is the better
evidence, so the bib is probably right, but a direct IJCAI proceedings check was not completed.

**7. `dl.acm.org` returned 403 throughout**, so ACM DL pages could not be used as the primary for
Cococo, Expressive Communication or Amuse. Author lists and venues for those three were instead
confirmed from the authors' own hosted PDFs and CV plus the ACM DL search-result page titles —
adequate, but note that no ACM page was directly read.
