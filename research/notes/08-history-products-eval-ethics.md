# 08 — History, Product Landscape, Evaluation, Ethics/Legal

_Research notes for the AI Music Studio project. Compiled 2026-09-07. Verification levels per entry: **verified** = primary/official source fetched; **partial** = confirmed from search snippets / secondary sources; **unverified** = from recall only._

## Overview

This cluster supplies the *context* for the studio rather than its core algorithms: (A) seventy years of algorithmic composition and interactive music systems, from Hiller & Isaacson's rule-and-Markov ILLIAC experiments (1957) through Xenakis's drawn-sound UPIC (1977), Cope's recombinant EMI (1980s–2000s), Rowe's still-useful 1993 taxonomy of interactive systems, real-time accompaniment and improvisation partners (Dannenberg, Vercoe, Lewis, Biles, Pachet, Assayag), the first neural sequence models (Eck & Schmidhuber 2002, Boulanger-Lewandowski 2012, folk-rnn 2016), and the parallel *commercial* lineage of auto-accompaniment (Band-in-a-Box 1990, Korg i3 1993) and notation/sequencing software; (B) the 2024–2026 product landscape, which has bifurcated into audio-level text-to-song platforms (Suno, Udio, Google Lyria/Flow Music, ElevenLabs, Stable Audio, Mureka) now being pulled into label-licensed "walled gardens", versus symbolic/score-level assistants embedded in existing tools (Hookpad Aria, Composer's Assistant, MIDI-GPT, Scaler 3, Logic Session Players, LLM→DAW bridges like AbletonMCP), with the notation incumbents (Dorico, Sibelius, MuseScore) conspicuously *not* shipping generative AI and Finale discontinued (Aug 2024); (C) evaluation methodology, where distribution metrics (FAD→KAD, FMD for symbolic) are being shown to correlate weakly with human preference, large human-preference benchmarks and MOS challenges are emerging (2025–2026), and co-creativity evaluation (CSI, Karimi et al., Kantosalo) plus creativity theory (Boden, Ritchie, Colton, Jordanous) offer the vocabulary for evaluating a *human-centred* tool rather than a generator; and (D) the legal/ethical landscape as of September 2026: the major-label suits against Suno/Udio (June 2024) have partly resolved into licensing deals (UMG–Udio Oct 2025; WMG–Udio and WMG–Suno Nov 2025) while UMG and Sony still litigate Suno with 61k+ asserted recordings; German courts (GEMA v. OpenAI, Nov 2025; GEMA v. Suno, **31 July 2026**) have held that memorisation inside a model is an infringing reproduction not covered by the TDM exception; the U.S. human-authorship rule stands (Thaler cert denied Mar 2026; USCO Part 2, Jan 2025); the EU AI Act's GPAI transparency duties apply since Aug 2025; and streaming platforms report AI now exceeding 50% of daily uploads (Deezer, July 2026) with tagging, demotion and fraud prosecutions following.

## Key takeaways for the studio

1. **Rowe's 1993 taxonomy is directly reusable** for the studio's design space: *score-driven vs performance-driven* input, *transformative / generative / sequenced* response, and *instrument vs player* paradigm. The founder's "compile" loop is largely a *score-driven, transformative* system in the *instrument* paradigm, with optional *player*-paradigm agents (e.g., a Session-Player-like bassist). Use this vocabulary in the taxonomy.
2. **The auto-accompaniment lineage (Band-in-a-Box → Korg i3/Pa, Yamaha PSR → Logic Session Players 2024) is the closest commercial ancestor of "compile from a lead sheet".** All of them take *chords + style + key + tempo* and render parts; none let you annotate with audio/sketch/hum, and none round-trip to editable notation cleanly. That gap is the studio's opening.
3. **Almost every symbolic assistant that composers actually adopted is an in-context infiller with user-selected regions and editable results** (Hookpad Aria, Composer's Assistant, MIDI-GPT, Magenta Studio). The market has validated "select a region → ask → accept/edit" as the interaction primitive; text-to-full-song is validated only for non-musicians.
4. **Notation incumbents have left generative AI on the table.** Dorico 6 (Apr 2025), Sibelius (Feb 2026 release), MuseScore Studio 4.6/4.7 ship no generative features; Finale is dead (Aug 2024). A notation-native AI studio has no direct competitor in 2026.
5. **Evaluation: do not rely on FAD.** Use KAD (audio) / FMD (symbolic) for distributional sanity checks only; the 2025 human-preference benchmarks show weak metric–human correlation. For the *studio*, the right instruments are the **Creativity Support Index**, Karimi et al.'s co-creativity framework (who/what/when/how), ownership/agency questionnaires, and expert-vs-novice listening tests with paired-similar stimuli (Echoes of Humanity method).
6. **Human-authored, symbolic-first material is the safest legal footing in 2026.** German courts treat model memorisation of works as reproduction; U.S. copyright requires human authorship for protection of outputs (Thaler; USCO Part 2), and human-controlled, human-edited symbolic material *is* protectable. A studio whose outputs are human-authored notation, compiled from the user's own material, sits on the right side of both lines.
7. **Training-data provenance matters for an open-source studio.** Use PDMX (CC-BY, 250k public-domain MusicXML), Aria-MIDI (1M+ transcribed piano MIDI), Stable Audio Open (CC-licensed audio) and similar; document a public training-content summary (EU AI Act template); consider Fairly Trained-style certification. Avoid Lakh/MuseScore-scraped copyrighted material for any released weights.
8. **Label "walled gardens" (no downloads, fingerprinting) are the industry's chosen model for audio generation**; Suno's own download caps (Sept 2026) show how constraining that is for professional workflows. A local, symbolic, human-owned pipeline is the counter-offer.
9. **Disclosure is becoming mandatory infrastructure**: DDEX AI-credit metadata (Spotify, Sept 2025), Deezer tagging, SynthID watermarks (Google), EU transparency duties. The studio should emit provenance/credit metadata ("compiled by X from human-authored material") by design.
10. **Surveys consistently show musicians want assistive, not substitutive, AI** (APRA AMCOS 2024: 54% think AI can assist the creative process, 82% fear for income, 95–97% demand consent/disclosure). This is exactly the studio's positioning.

---

# A. Historical roots

### IlliacSuite — Illiac Suite (String Quartet No. 4) and *Experimental Music: Composition with an Electronic Computer*
- **Who/where/when:** Lejaren Hiller & Leonard Isaacson, University of Illinois Urbana-Champaign; work composed 1956–57 on ILLIAC I; book McGraw-Hill 1959.
- **Links:** https://en.wikipedia.org/wiki/Illiac_Suite
- **What it is:** Generally credited as the first score composed by a computer. Four "experiments": (1) generation of cantus firmi, (2) four-voice writing under strict counterpoint rules (generate-and-test), (3) rhythm, dynamics and playing instructions, (4) Markov-chain (stochastic) generation. Output was symbolic (notes for string quartet) and then human-engraved and performed.
- **Evidence:** Historical; no user study. Established the *rule-based generate-and-test* and *Markov* paradigms.
- **Why it matters for the studio:** The two paradigms of experiment 2 (constraint rules) and experiment 4 (probabilistic style) are exactly the two modes a "compiler" needs: hard constraints from the composer's annotations plus soft stylistic priors.
- **Tags:** [history] [symbolic-generation] [notation]
- **Verification:** verified
- **BibKey:** hiller1959experimental

### UPIC — Unité Polyagogique Informatique du CEMAMu (Xenakis)
- **Who/where/when:** Iannis Xenakis, CEMAMu, Paris; completed 1977; first work *Mycènes Alpha* (1978). Stochastic-music theory in *Formalized Music* (1971, rev. 1992).
- **Links:** https://en.wikipedia.org/wiki/UPIC
- **What it is:** A digitising tablet + computer on which the composer *draws* waveforms, envelopes and "arcs" (x = time, y = pitch) that are rendered directly to sound; drawings can be stretched, transposed, inverted, algorithmically transformed. Successors: IanniX (open-source), UPISketch (2018, macOS/iOS).
- **Evidence:** Historical; adopted by Estrada, Risset, Mâche among others.
- **Why it matters for the studio:** The earliest realisation of *sketch as score*: drawing is the primary input and is directly executable. Directly relevant to the "scribble/sketch on the notation" annotation channel.
- **Tags:** [history] [sketch] [multimodal-input] [representation]
- **Verification:** verified
- **BibKey:** xenakis1992formalized

### KoenigProject — Project 1 (1964) and Project 2 (1966)
- **Who/where/when:** Gottfried Michael Koenig, Institute of Sonology, Utrecht; 1964 and 1966.
- **Links:** (no stable primary URL fetched)
- **What it is:** Serial/aleatoric composition programs: Project 1 produces a structured table of parameters (pitch, duration, register, dynamics, entry delays) from selection principles the composer sets; Project 2 exposes far more composer-specified constraints and a "score" of parameter-selection strategies. Output is a symbolic parameter list the composer then transcribes into notation.
- **Evidence:** Historical.
- **Why it matters for the studio:** Early example of the composer *programming the generator's constraints* rather than the notes — the "composition as program" metaphor the founder uses.
- **Tags:** [history] [symbolic-generation] [music-as-code]
- **Verification:** unverified (recall; dates widely cited)
- **BibKey:** koenig1970project

### EMI — Experiments in Musical Intelligence ("Emmy") and Emily Howell
- **Who/where/when:** David Cope, UC Santa Cruz; started 1981; ICMC paper 1987; books *Computers and Musical Style* (1991), *Experiments in Musical Intelligence* (1996), *Virtual Music* (MIT Press 2001, ed. Cope with Hofstadter et al.); database deleted 2005; Emily Howell album 2009.
- **Links:** https://en.wikipedia.org/wiki/Experiments_in_Musical_Intelligence
- **What it is:** Recombinant style modelling in ~20,000 lines of Lisp: segment a corpus of one composer, pattern-match "signatures", classify segments (SPEAC: statement/preparation/extension/antecedent/consequent), and recombine under grammar constraints into new works in that style (Bach chorales, Mozart, Chopin, opera). Emily Howell added interactive feedback so a *personal* style emerged.
- **Evidence:** Hofstadter's touring "Chopin vs EMI" tests — audiences (incl. at University of Oregon, 1997, with Steve Larson) guessed at roughly chance. *Virtual Music* (2001) collects the Cope–Hofstadter debate on whether recombinant pastiche is creativity; Hofstadter found the results disturbing precisely because they succeeded.
- **Why it matters for the studio:** The canonical warning about *style pastiche* and authorship; also the origin of the "creativity vs perception of creativity" argument later formalised by Colton. Cope's deletion of the database anticipates today's memorisation/originality debates.
- **Tags:** [history] [symbolic-generation] [style-transfer] [ethics-legal] [evaluation]
- **Verification:** verified (Wikipedia + recall for Virtual Music details)
- **BibKey:** cope2001virtual

### RoweIMS — *Interactive Music Systems: Machine Listening and Composing*
- **Who/where/when:** Robert Rowe, NYU; MIT Press, 1993 (now free online).
- **Links:** https://wp.nyu.edu/robert_rowe/text/interactive-music-systems-1993/chapter-1-interactive-music-systems/
- **What it is:** Defines interactive music systems as sensing→processing→response, and classifies them on three dimensions: (1) **score-driven** (match input against a stored score/fragments; uses beat/meter) vs **performance-driven** (no stored score; uses perceptual measures like density, regularity); (2) response method **transformative** (vary existing input material), **generative** (rules produce complete output from elementary seeds), **sequenced** (play back prerecorded fragments); (3) **instrument paradigm** (extends a human performer's gesture → solo-like) vs **player paradigm** (an artificial musician with its own personality → duet-like). Also introduces the *Cypher* system.
- **Evidence:** Conceptual; became the standard vocabulary in NIME/ICMC.
- **Why it matters for the studio:** Provides a ready-made axis set for the project's taxonomy. The founder's loop is score-driven + transformative, instrument paradigm, with the AI as "compiler"; accompaniment agents would be player-paradigm.
- **Tags:** [history] [co-creation-framework] [real-time] [accompaniment]
- **Verification:** verified
- **BibKey:** rowe1993interactive

### Voyager — George Lewis's *Voyager*
- **Who/where/when:** George E. Lewis (trombonist/composer), begun 1987 (Forth on Atari/Mac); "Too Many Notes: Computers, Complexity and Culture in *Voyager*", *Leonardo Music Journal* 10, 2000.
- **Links:** https://doi.org/10.1162/096112100570585
- **What it is:** A "virtual improvising orchestra": listens (pitch-to-MIDI) to a human improviser and generates multiple independent voices with their own behaviours; may respond, ignore, or initiate. Explicitly *not* an instrument the human controls — a player-paradigm partner rooted in Afrological improvisation aesthetics.
- **Evidence:** Decades of performances/recordings (Voyager, 1993 CD); conceptual essay.
- **Why it matters for the studio:** The antithesis of "compile": an AI with its own agency. Useful as the far pole of the control axis and as a source of ideas for "player" agents that the composer can invite in but not fully script.
- **Tags:** [history] [real-time] [mixed-initiative] [co-creation-framework]
- **Verification:** partial
- **BibKey:** lewis2000toomanynotes

### Accompaniment1984 — Real-time computer accompaniment (Dannenberg) and the Synthetic Performer (Vercoe)
- **Who/where/when:** Roger B. Dannenberg, CMU, "An On-Line Algorithm for Real-Time Accompaniment", ICMC 1984; Barry Vercoe, MIT Media Lab/IRCAM, "The Synthetic Performer in the Context of Live Performance", ICMC 1984 (with Puckette 1985 follow-up).
- **Links:** https://www.cs.cmu.edu/~rbd/bib-accomp.html
- **What it is:** Score following: dynamic-programming alignment of a live monophonic performance to a stored score, driving synchronised accompaniment (Dannenberg); Vercoe's system tracked a flautist via pitch + fingering sensors and learned tempo tendencies across rehearsals. Later: polyphonic following (1985), stochastic vocal tracking (Grubb & Dannenberg 1997), *Music Score Alignment and Computer Accompaniment* (CACM 2006, with Raphael), Human-Computer Music Performance (2011–14).
- **Evidence:** Engineering demonstrations; CACM 2006 is the standard review.
- **Why it matters for the studio:** Score-driven interaction is the studio's native mode; score following is the technology that would let the composer *hum or play* against the compiled score and have the AI stay aligned.
- **Tags:** [history] [accompaniment] [real-time] [transcription]
- **Verification:** verified (Dannenberg bibliography) / partial (Vercoe)
- **BibKey:** dannenberg1984online

### GenJam — Genetic Jammer
- **Who/where/when:** John A. "Al" Biles, Rochester Institute of Technology; "GenJam: A Genetic Algorithm for Generating Jazz Solos", ICMC 1994; later interactive versions (1998–2000s).
- **Links:** https://igm.rit.edu/~jabics/GenJam.html
- **What it is:** Genetic algorithm evolves populations of measure- and phrase-level jazz licks over a chord progression; the human "mentor" gives real-time good/bad feedback as fitness (interactive GA); later versions trade fours with the human and use autonomous fitness.
- **Evidence:** Long-running performance practice ("Virtual Quintet"); famous for exposing the *fitness bottleneck* of human-in-the-loop evaluation.
- **Why it matters for the studio:** Early formalisation of *annotation as fitness*: the human's thumbs-up/down on generated material steers the system — the primitive form of the studio's annotate→regenerate loop.
- **Tags:** [history] [accompaniment] [mixed-initiative] [annotation]
- **Verification:** partial
- **BibKey:** biles1994genjam

### Continuator — The Continuator (Pachet) and Flow Machines
- **Who/where/when:** François Pachet, Sony CSL Paris; "The Continuator: Musical Interaction with Style", *Journal of New Music Research* 32(3), 2003 (ICMC 2002 earlier). Flow Machines (ERC project 2012–17): *Daddy's Car* (2016), SKYGGE *Hello World* album (2018).
- **Links:** https://www.francoispachet.fr/continuator/ ; https://doi.org/10.1076/jnmr.32.3.333.16861
- **What it is:** Learns a variable-order Markov model (prefix trees) of a player's MIDI phrases *in real time* and continues each phrase in that style when the player stops; can be biased by external constraints. Flow Machines generalised this to *Markov constraints* (style + hard constraints such as meter, harmony, positional) and lead-sheet generation (FlowComposer), producing the first commercially released "AI-assisted" pop songs.
- **Evidence:** Addessi & Pachet studies with children (reflexive interaction increased engagement); Flow Machines outputs were human-arranged/produced.
- **Why it matters for the studio:** *Markov constraints* are the pre-deep-learning version of "generate in my style subject to my annotations"; FlowComposer's lead-sheet-first workflow is a direct ancestor of the symbolic-first studio.
- **Tags:** [history] [real-time] [symbolic-generation] [controllability] [accompaniment]
- **Verification:** partial (site fetched; JNMR citation from recall)
- **BibKey:** pachet2003continuator

### OMax — OMax / Somax2 (IRCAM)
- **Who/where/when:** Gérard Assayag, Georges Bloch, Marc Chemillier, Shlomo Dubnov et al., IRCAM; OMax from 2004–06 (Factor Oracle); Somax (Bonnasse-Gahot 2014) → Somax2 (Borg, Assayag, 2020s, Max/MSP).
- **Links:** https://forum.ircam.fr/projects/detail/somax-2/ ; https://forum.ircam.fr/projects/detail/omax/
- **What it is:** "Stylistic reinjection": learns a Factor Oracle over the live audio/MIDI stream and improvises by navigating and recombining the performer's own material; Somax2 adds reactive listening (harmonic/melodic influence from what the human plays now) and multi-agent co-improvisation.
- **Evidence:** Extensive concert practice (Bernard Lubat, Steve Lehman etc.); design papers at ICMC/NIME/CMJ.
- **Why it matters for the studio:** Shows how an AI can work exclusively from *the composer's own material* (no external corpus) — an ethically clean approach to style; also a model for "recombine my sketches".
- **Tags:** [history] [real-time] [mixed-initiative] [accompaniment]
- **Verification:** partial
- **BibKey:** assayag2006omax

### EckLSTM — Finding temporal structure in music: blues improvisation with LSTM
- **Who/where/when:** Douglas Eck & Jürgen Schmidhuber, IDSIA; IEEE Workshop on Neural Networks for Signal Processing 2002 (and IDSIA tech report IDSIA-07-02).
- **Links:** https://people.idsia.ch/~juergen/blues/
- **What it is:** First LSTM music generation: learns 12-bar blues chord progressions and melodies (piano-roll, quantised) and generates coherent long-range structure where earlier RNNs drifted.
- **Evidence:** Qualitative; demonstrated LSTM keeps global form.
- **Why it matters for the studio:** Origin of neural symbolic generation; the *structure* problem it addressed remains the central problem for "compiling" full forms.
- **Tags:** [history] [symbolic-generation] [structure]
- **Verification:** partial
- **BibKey:** eck2002blues

### RNNRBM — Modeling temporal dependencies in high-dimensional sequences: polyphonic music
- **Who/where/when:** Nicolas Boulanger-Lewandowski, Yoshua Bengio, Pascal Vincent, Université de Montréal; ICML 2012.
- **Links:** https://icml.cc/2012/papers/590.pdf
- **What it is:** RNN-RBM for polyphonic piano-roll prediction; introduced the four benchmark datasets (JSB Chorales, MuseData, Nottingham, Piano-midi.de) used for a decade.
- **Evidence:** Log-likelihood benchmarks on those datasets; also improved polyphonic transcription.
- **Why it matters for the studio:** Anchors the modern symbolic-generation benchmark lineage; the datasets are small, clean and licence-friendly (JSB chorales) — still useful for unit-testing a harmony engine.
- **Tags:** [history] [symbolic-generation] [dataset]
- **Verification:** partial
- **BibKey:** boulangerlewandowski2012modeling

### folkRNN — Music transcription modelling and composition using deep learning (folk-rnn)
- **Who/where/when:** Bob L. Sturm, João Felipe Santos, Oded Ben-Tal, Iryna Korshunova; QMUL/Kingston; Conference on Computer Simulation of Musical Creativity (CSMC) 2016; arXiv 1604.08723.
- **Links:** https://arxiv.org/abs/1604.08723 ; https://github.com/IraKorshunova/folk-rnn ; https://folkrnn.org
- **What it is:** Character/token LSTM over ~23,000 ABC-notation folk transcriptions; generates new tunes in ABC. Evaluated at population level (statistics vs corpus), individual level (idiomatic conventions), and by *using* outputs for composition (Ben-Tal). Web interface let musicians steer by key/meter/seed.
- **Evidence:** Musicians adopted tunes into sessions; a series of follow-ups (Sturm & Ben-Tal 2017, "Machine folk" concerts) and the "Let's Have Another Gan Ainm" album.
- **Why it matters for the studio:** Demonstrates text-based *notation as the model's native representation* (ABC) and evaluation *by composers using the output* — both aligned with the studio.
- **Tags:** [history] [symbolic-generation] [notation] [evaluation] [representation]
- **Verification:** verified
- **BibKey:** sturm2016folkrnn

### BandInABox — Band-in-a-Box and the arranger-keyboard lineage
- **Who/where/when:** PG Music (Peter Gannon), Victoria BC; first release 1990 (PC, Atari ST); Soloist 1997; RealDrums 2006; RealTracks + Audio Chord Wizard 2007; annual releases continue (BiaB 2026). Arranger keyboards: Korg i3 (1993, first Korg "interactive" workstation), Yamaha PSR series (1980s→), Korg Pa series (Pa80 2000 → Pa5X 2022).
- **Links:** https://en.wikipedia.org/wiki/Band-in-a-Box ; https://www.pgmusic.com
- **What it is:** Type chords into a bar grid, pick key/tempo/style → the program generates a full band arrangement (originally MIDI styles; since 2007 "RealTracks" = recorded human phrases spliced to fit chords). Melodist/Soloist generate melodies/solos; Audio Chord Wizard transcribes chords from audio. Arranger keyboards do the same in hardware in real time from left-hand chords, with style/variation/fill/intro/ending buttons.
- **Evidence:** 35 years of continuous commercial existence; huge hobbyist base.
- **Why it matters for the studio:** This *is* the "compile a lead sheet" paradigm in its commercial form (the founder grew up on a Korg i3). Its limits define the opportunity: no multimodal annotation, coarse style vocabularies, weak editability of generated parts, MIDI/audio not notation-first.
- **Tags:** [history] [product] [accompaniment] [symbolic-generation]
- **Verification:** verified (BiaB) / partial (keyboards)
- **BibKey:** pgmusic1990bandinabox

### NotationSequencerHistory — Notation and MIDI-sequencer software lineage (brief)
- **Who/where/when:** Finale (Coda/MakeMusic, 1988; **discontinued 26 Aug 2024**, support ended 26 Aug 2025); Encore (Passport Designs, 1990); Sibelius (Finn brothers, Acorn 1993 → Windows/Mac 1998; Avid since 2006); Dorico (Steinberg, 2016); MuseScore (2002, Muse Group). Sequencers: Cakewalk (Twelve Tone Systems, 1987 DOS), Cubase (Steinberg, Atari ST 1989), Logic (C-Lab Notator 1988 → Emagic Logic → Apple 2002).
- **Links:** https://www.makemusic.com/press-room/press-releases-2024/makemusic-sunsets-finale/ ; https://blog.dorico.com/2024/08/finale-sunset/
- **What it is:** Two separate tool families — engraving-first (notation) and time-line-first (sequencer/DAW) — that never fully merged; MusicXML (2004, Recordare/W3C Music Notation CG) is the interchange bridge. MakeMusic's stated reason for killing Finale: "millions of lines of code" made meaningful improvement "exponentially harder"; it partnered with Steinberg to sell a $149 Dorico crossgrade.
- **Evidence:** Historical.
- **Why it matters for the studio:** The studio's "notation that compiles to audio" must sit across these two families; the Finale exit shows the incumbents' legacy stacks are a liability and users are mobile.
- **Tags:** [history] [notation] [product]
- **Verification:** verified (Finale) / partial (others)
- **BibKey:** makemusic2024finale

### BachInABox — "Bach in a Box" and *Bach by Design*
- **Who/where/when:** R. A. McIntyre, "Bach in a Box: The Evolution of Four Part Baroque Harmony Using the Genetic Algorithm", IEEE Conf. on Evolutionary Computation 1994; David Cope, *Bach by Design* (Centaur CD, 1994) — first commercial recording of EMI output.
- **Links:** https://doi.org/10.1109/ICEC.1994.350040
- **What it is:** GA harmonises a given melody into four-part Baroque style using a rule-based fitness function (McIntyre). Cope's CD was the public debut of computer-composed Bach-style pieces.
- **Evidence:** Small-scale; historically cited as an early GA harmonisation.
- **Why it matters for the studio:** Harmonise-my-melody is a core "compile" task; early rule-fitness approaches are still a useful baseline/constraint layer.
- **Tags:** [history] [symbolic-generation] [theory-analysis]
- **Verification:** unverified (recall)
- **BibKey:** mcintyre1994bachinabox

---

# B. Product landscape 2024–2026

_Classification key used below: **A** = audio-level generation; **S** = symbolic/score-level; **I** = iterative editing supported (regions, stems, infills, re-generation of parts); **1** = essentially one-shot generation._

### Suno — Suno (v4.5/v5 → licensed models), Suno Studio 1.0 (Sept 2025) and 2.0 (Aug 2026), download caps (Sept 2026)
- **Who/where/when:** Suno Inc., Cambridge MA (Mikey Shulman CEO). Suno Studio announced 24 Sept 2025; acquired WavTool 30 June 2025 and Songkick (from WMG) Nov 2025; Studio 2.0 launched 13 Aug 2026.
- **Links:** https://suno.com/blog/studio-2 ; https://suno.com/blog/suno-acquires-wavtool ; https://www.musicbusinessworldwide.com/suno-limits-subscribers-downloads-per-month/
- **What it is:** [A][I-partial] Text/lyrics → full song with vocals (≤ ~8 min). Studio = a browser "generative audio workstation": multitrack timeline, stem separation, per-section regeneration/extension, audio effects, automation; Studio 2.0 (Premier tier) adds **MIDI import/recording/editing with a wavetable synth**, a chat-bar AI assistant, and unlimited 32-bit/48 kHz stem export. Announced 10 Aug 2026, effective 3 Sept 2026: **downloads capped** — Free 7 lifetime (personal use), Pro 20/month, Premier 60/month (extra purchasable) — as part of the WMG deal; "all prior models will be retired" when the new licensed models launch.
- **Evidence:** Pricing: Pro ~$8–10/mo, Premier ~$24–30/mo. Audited by litigation: UMG/Sony discovery says Suno trained on "millions" of their recordings (May 2026 filing).
- **Why it matters for the studio:** The dominant text-to-song incumbent is itself moving toward a DAW with MIDI — i.e., toward *editability* — validating the founder's critique of one-shot generation. But it remains audio-first and legally encumbered; its new download caps make it a poor "compile" target for professionals.
- **Tags:** [product] [audio-generation] [text-conditioning] [editing] [ethics-legal]
- **Verification:** verified
- **BibKey:** suno2026studio2

### Udio — Udio and the UMG/WMG licensed "walled garden"
- **Who/where/when:** Uncharted Labs (Andrew Sanchez, David Ding et al., ex-DeepMind), New York; launched Apr 2024; settled with UMG 29 Oct 2025 and WMG 19 Nov 2025.
- **Links:** https://www.musicbusinessworldwide.com/universal-music-settles-udio-lawsuit-strikes-deal-for-licensed-ai-music-platform/ ; https://www.prnewswire.com/news-releases/universal-music-group-and-udio-announce-udios-first-strategic-agreements-for-new-licensed-ai-music-creation-platform-302599129.html
- **What it is:** [A][I-partial] Text → 32-s segments extendable into songs; inpainting of sections; stems. Post-settlement: existing product continues "with enhanced controls" (downloads disabled Oct 2025 after a 48-hour grace window), and a **new subscription platform launches in 2026** where creations stay inside the platform — no downloads, fingerprinting/filtering, customisation/streaming/sharing only; licensed catalogues with artist opt-in.
- **Evidence:** Reddit/user backlash over lost downloads (Billboard, Nov 2025); antitrust commentary on the walled-garden model.
- **Why it matters for the studio:** Shows the endpoint of label-licensed audio generation: outputs the user cannot own or take elsewhere. A composer-centred studio must guarantee the opposite (portable notation/MIDI/stems).
- **Tags:** [product] [audio-generation] [ethics-legal]
- **Verification:** verified
- **BibKey:** udio2025umg

### Lyria — Google DeepMind Lyria family, Music AI Sandbox, MusicFX, Lyria RealTime, Lyria 3/3 Pro/3.5, and Google Flow Music (ex-Producer.ai / Riffusion)
- **Who/where/when:** Google DeepMind + Google Labs + YouTube. MusicFX (AI Test Kitchen, 2023–24); Music AI Sandbox expanded with Lyria 2 (Apr 2025); Lyria RealTime API (20 May 2025); Lyria 3 in Gemini app (Feb 2026); **Google acquired Producer.ai (formerly Riffusion) 25 Feb 2026** and relaunched it as **Google Flow Music** (Lyria 3 Pro); Believe/TuneCore partnership 6 May 2026; Lyria 3.5 current.
- **Links:** https://deepmind.google/models/lyria/ ; https://deepmind.google/blog/music-ai-sandbox-now-with-new-features-and-broader-access/ ; https://www.musicbusinessworldwide.com/believe-partners-with-google-to-offer-ai-music-creation-tool-flow-music-to-its-artists/
- **What it is:** [A][I] Text (and image) → music with vocals/lyrics up to ~3 min with explicit section structure (intro/verse/chorus/bridge); Music AI Sandbox offers *Create / Extend / Edit* (inpainting) on clips for pro users; Lyria RealTime streams continuous audio steerable by prompt weights (also open-weights sibling **Magenta RealTime**, see below). All outputs SynthID-watermarked. Training: "materials YouTube and Google have a right to use under our terms of service, partner agreements and applicable law"; Google disclaims ownership of Flow Music outputs.
- **Evidence:** Ranked among top systems in 2025 human-preference benchmarks (Grötschla et al.); no independent user studies of the Sandbox published.
- **Why it matters for the studio:** Most complete *audio-level* editing loop among big-tech offerings (extend/inpaint/real-time steer) and the only one with a public open-weights real-time model — a candidate rendering/"audio compile" back-end, subject to licence review.
- **Tags:** [product] [audio-generation] [editing] [real-time] [text-conditioning] [image]
- **Verification:** verified
- **BibKey:** google2026lyria

### ElevenMusic — Eleven Music (ElevenLabs)
- **Who/where/when:** ElevenLabs; launched 5 Aug 2025 with licences from Merlin Network and Kobalt; later consumer "ElevenMusic" remix/streaming service (2026).
- **Links:** https://techcrunch.com/2025/08/05/elevenlabs-launches-an-ai-music-generator-which-it-claims-is-cleared-for-commercial-use/
- **What it is:** [A][I-partial] Text/lyrics → full songs with vocals in many languages, claimed *cleared for commercial use* on the basis of licensed training/rights deals with revenue-sharing to rights-holders; section-level editing of lyrics/structure.
- **Evidence:** First major text-to-music launch built on licences rather than post-hoc settlement.
- **Why it matters for the studio:** Demonstrates that a "licensed by construction" audio model is commercially viable — relevant if the studio ever bundles an audio renderer.
- **Tags:** [product] [audio-generation] [ethics-legal]
- **Verification:** verified
- **BibKey:** elevenlabs2025music

### StableAudio — Stable Audio 2.5 (enterprise) and Stable Audio Open (open weights)
- **Who/where/when:** Stability AI; Stable Audio Open 1.0 paper 31 July 2024 (Evans, Parker, Carr, Zukowski, Taylor, Pons; ICASSP 2025); Stable Audio 2.5 launched 10 Sept 2025; WMG–Stability partnership 19 Nov 2025 (UMG–Stability Oct 2024).
- **Links:** https://arxiv.org/abs/2407.14358 ; https://huggingface.co/stabilityai/stable-audio-open-1.0 ; https://stability.ai/news-updates/stability-ai-introduces-stable-audio-25-the-first-audio-model-built-for-enterprise-sound-production-at-scale
- **What it is:** [A][I] Open: 1.2B-param latent diffusion text-to-audio, 44.1 kHz stereo ≤47 s, trained only on CC-licensed Freesound + Free Music Archive audio; weights under Stability AI Community License (free < $1M revenue). 2.5: ≤3-min multi-part tracks in <2 s on GPU, **audio inpainting / audio-to-audio**, "trained on a fully licensed dataset", aimed at brands (WPP).
- **Evidence:** Paper reports FAD/KL/CLAP; FD-OpenL3 competitive with closed models; 2024 Stable Audio 2.0 paper had a listening test.
- **Why it matters for the studio:** The reference open, licence-clean audio model — the natural default for local sound-design/rendering experiments in an open-source studio.
- **Tags:** [product] [audio-generation] [text-conditioning] [ethics-legal] [dataset]
- **Verification:** verified
- **BibKey:** evans2024stableaudioopen

### Mureka — Mureka (Kunlun Tech / Skywork AI), Mureka O1 "music reasoning" model
- **Who/where/when:** Kunlun Tech (Beijing); Mureka O1 launched 26 Mar 2025 (claimed first chain-of-thought "MusiCoT" music model), Mureka V7 later 2025; API and fine-tuning on user songs.
- **Links:** https://www.mureka.ai ; https://www.prnewswire.com/news-releases/kunlun-tech-launches-the-worlds-first-music-reasoning-large-model-mureka-o1-leading-the-global-ai-music-revolution-302411665.html
- **What it is:** [A][I-partial] Lyrics-first text-to-song with vocals; "reasoning" over structure before generation; reference-audio style conditioning; song editing (section regeneration), stem export; developer API.
- **Evidence:** Vendor benchmarks only.
- **Why it matters for the studio:** Example of *planning-then-generating* (structure first) in a commercial model — the audio analogue of the founder's compile step; also one of the few platforms offering *fine-tune on your own catalogue*.
- **Tags:** [product] [audio-generation] [structure] [text-conditioning]
- **Verification:** partial
- **BibKey:** kunlun2025mureka

### LogicPro11 — Logic Pro 11 Session Players, Stem Splitter, ChromaGlow, Chord Track (Apple)
- **Who/where/when:** Apple; announced 7 May 2024, released 13 May 2024 (Logic Pro for Mac 11 / iPad 2); 11.1 (Nov 2024) and 11.2 (2025) updates added instruments/features.
- **Links:** https://www.apple.com/newsroom/2024/05/logic-pro-takes-music-making-to-the-next-level-with-new-ai-features/
- **What it is:** [S][I] **Session Players** = Drummer (2013) + new **Bass Player** (8 players; complexity/intensity; slides, mutes, dead notes, pickup hits) + **Keyboard Player** (4 styles, block chords → extended voicings) that *follow the Chord Track* and can be edited as MIDI regions ("trained in collaboration with" session musicians). **Stem Splitter** (4 stems, on-device Apple silicon); **ChromaGlow** saturation. $199.99 / free update.
- **Evidence:** No public evaluation; widely reviewed as the first mainstream DAW with generative *symbolic* accompaniment beyond drums.
- **Why it matters for the studio:** The best current example of "chords + style → editable MIDI parts" inside a DAW — the arranger-keyboard idea reborn. Its parameters (complexity, intensity, style) are a reasonable minimum control vocabulary for the studio's "compile" step; its lack of notation view, multimodal input or arrangement-level reasoning is the gap.
- **Tags:** [product] [accompaniment] [symbolic-generation] [editing] [DAW-plugin]
- **Verification:** verified
- **BibKey:** apple2024logicpro11

### Live12 — Ableton Live 12 "Similar Sounds", MIDI Generators/Transformations
- **Who/where/when:** Ableton, Berlin; Live 12 released 5 Mar 2024; 12.1/12.2/12.3 (2024–25).
- **Links:** https://www.ableton.com/en/live/what-is-new-in-12/
- **What it is:** [S][I] No generative AI for music; **Sound Similarity Search** uses ML audio embeddings to find similar samples/presets in the library; new rule-based **MIDI Generators** (Rhythm, Seed, Shape, Stacks) and **Transformations** (Arpeggiate, Connect, Ornament, Quantize, Recombine, Strum…) are non-neural, fully editable devices. Max-for-Live hosts third-party ML devices (Magenta Studio, Neutone).
- **Evidence:** —
- **Why it matters for the studio:** Ableton's stance — deterministic, transparent generators + ML only for *retrieval* — is a deliberate design position that many producers trust; a good foil for the studio's "AI as compiler" and a reminder that transparency is a feature.
- **Tags:** [product] [symbolic-generation] [DAW-plugin]
- **Verification:** partial
- **BibKey:** ableton2024live12

### HookpadAria — Hookpad + Aria (Hooktheory)
- **Who/where/when:** Hooktheory (Dave Carlton, Chris Anderson, Ryan Miyakawa) with Chris Donahue's group (CMU); Aria announced 30 Dec 2024 (beta), GA 2025.
- **Links:** https://www.hooktheory.com/hookpad/aria ; https://www.hooktheory.com/blog/generative-ai-songwriting/
- **What it is:** [S][I] Inside Hookpad's Roman-numeral/lead-sheet editor the user *selects a region* and asks Aria to write chords, melody, or both (chords-for-melody / melody-for-chords / infill). Powered by the **Anticipatory Music Transformer** (Thickstun, Hall, Donahue, Liang 2023) fine-tuned on Hooktheory's own **TheoryTab** database (>50,000 public user analyses). Suggestions are ordinary editable Hookpad notation. $14.99/mo add-on; 10 free infills/day.
- **Evidence:** No published user study; vendor logs only "fingerprints" of requests/accepted suggestions.
- **Why it matters for the studio:** The closest shipping analogue of the founder's loop (symbolic, region-based, editable, harmony-aware) and proof that an academic infilling model can be productised on a small, consented, functional-harmony dataset. Cross-ref cluster on infilling (Anticipatory Music Transformer).
- **Tags:** [product] [symbolic-generation] [infilling] [notation] [editing] [theory-analysis]
- **Verification:** verified
- **BibKey:** hooktheory2024aria

### Scaler3 — Scaler 3 (Scaler Music / Plugin Boutique)
- **Who/where/when:** Scaler Music (Davide Carbone) / Plugin Boutique; announced NAMM Jan 2025, released Mar 2025.
- **Links:** https://www.scalerplugin.com ; https://help.pluginboutique.com/hc/en-us/articles/35864679857684-What-s-new-in-Scaler-3
- **What it is:** [S][I] Chord/scale detection from MIDI or audio, chord-set suggestions by genre/artist "style", an **Arrange page** (multi-track timeline for chords, bass, melody, phrases), built-in sounds, performances/phrases per chord; rule/curated-content based rather than neural. Exports MIDI to the host.
- **Evidence:** —
- **Why it matters for the studio:** Market-leading "harmony assistant" plugin; its arrange page shows demand for lead-sheet-to-arrangement inside DAWs, but with no notation and canned phrases.
- **Tags:** [product] [symbolic-generation] [theory-analysis] [DAW-plugin]
- **Verification:** partial
- **BibKey:** scaler2025v3

### OrbCaptain — Orb Producer Suite 3 (Hexachords) and Captain Chords Epic (Mixed In Key)
- **Who/where/when:** Hexachords (Orb Composer 2018 → Orb Producer Suite 3.0 ~2021–22); Mixed In Key (Captain Plugins 2017 → Captain Chords Epic 2022–23).
- **Links:** https://www.hexachords.com ; https://mixedinkey.com/captain-plugins/
- **What it is:** [S][I] Four MIDI-generating plugins (Chords, Melody, Bass, Arpeggio) that share a chord progression and generate/re-roll parts per block ("AI" = constraint/probabilistic engines); Captain Chords: chord progression builder with style presets, melody/bass companions, drag-out MIDI.
- **Evidence:** —
- **Why it matters for the studio:** Shows the practical "one shared chord track drives many part generators" architecture — a small-scale compile loop — and the UI convention of *re-roll a block*.
- **Tags:** [product] [symbolic-generation] [DAW-plugin] [accompaniment]
- **Verification:** partial
- **BibKey:** hexachords2022orb

### Dorico6 — Dorico 6 (Steinberg)
- **Who/where/when:** Steinberg (Daniel Spreadbury et al.), released 30 Apr 2025; $99 update, Finale/Sibelius crossgrade.
- **Links:** https://blog.dorico.com/2025/04/dorico-6-released/
- **What it is:** [S] Notation: new **Proofreading panel** (flags meter/marking/instrument-change problems), cutaway scores, chord-symbol customisation, engraving rulers/grid, condensing, Fill view. **No generative/ML features.** Existing "Generate notes from chord symbols"/"Generate chord symbols from selection" are rule-based.
- **Evidence:** —
- **Why it matters for the studio:** Now the professional engraving reference (post-Finale); a natural export target (MusicXML/Dorico) and evidence that the notation market has *no* AI composition assistant.
- **Tags:** [product] [notation]
- **Verification:** verified
- **BibKey:** steinberg2025dorico6

### MuseScore46 — MuseScore Studio 4.6 / 4.7 + Muse Hub (Muse Group)
- **Who/where/when:** Muse Group (Martin Keary product lead); 4.5 (Mar 2025), 4.6 (30 Sept 2025), 4.7 (2026); open-source (GPLv3).
- **Links:** https://musescore.org/en/4.6 ; https://github.com/musescore/MuseScore
- **What it is:** [S] Free notation editor with Muse Sounds orchestral playback via Muse Hub; 4.6 added percussion panel, guitar techniques, fretboard auto-fill from chord symbols, MusicXML improvements; planned **Cantai** AI choir integration (delayed). No generative composition features. Also hosts musescore.com score-sharing (source of PDMX public-domain subset).
- **Evidence:** —
- **Why it matters for the studio:** The obvious open-source engraving/playback substrate (or fork target) for a notation-first studio; also the community whose scores feed licence-clean datasets.
- **Tags:** [product] [notation] [toolkit]
- **Verification:** verified
- **BibKey:** musegroup2025musescore46

### Sibelius2026 — Sibelius (Avid) 2025–2026 releases
- **Who/where/when:** Avid; monthly/quarterly releases (2025.12, 2026.02).
- **Links:** https://www.avid.com/resource-center/sibelius-february-2026-release
- **What it is:** [S] Feb 2026: dark/light themes, engraving rules, ManuScript scripting extensions, crash fixes; **no AI features**. A rumoured "Sibelius AI" could not be confirmed in any Avid release note through Feb 2026.
- **Evidence:** —
- **Why it matters for the studio:** Confirms takeaway 4.
- **Tags:** [product] [notation]
- **Verification:** verified (absence)
- **BibKey:** avid2026sibelius

### MoisesStudio — Moises AI Studio (Moises / Music.AI)
- **Who/where/when:** Moises Systems (Geraldo Ramos), Salt Lake City/Brazil; AI Studio launched 20 Aug 2025.
- **Links:** https://moises.ai/newsroom/product-announcements/launch-ai-studio/
- **What it is:** [A][I] Generates **context-aware instrumental stems** that adapt to the user's existing audio (harmony adherence + style from audio reference/text/presets) inside a simplified DAW; bundled stem separation, beat/chord detection, voice conversion, auto-mix/master. Explicitly does **not** generate full songs, lyrics or vocals; company stresses licensed/annotated training data for separation.
- **Evidence:** —
- **Why it matters for the studio:** A commercial "add a part to *my* track" system — the audio-domain counterpart of the studio's compile-one-part step — and a positioning (no full songs) that matches the founder's philosophy.
- **Tags:** [product] [audio-generation] [accompaniment] [editing] [transcription]
- **Verification:** verified
- **BibKey:** moises2025aistudio

### SpliceCreate — Splice "Create" (Stacks)
- **Who/where/when:** Splice; Create launched 2023, expanded 2024–25.
- **Links:** https://splice.com/sounds/create
- **What it is:** [A][I] Not generative: assembles a *stack* of key/BPM-compatible human-made samples from Splice's licensed library from a seed sound, swappable per layer, exportable to the DAW. (Splice also offers AI-powered search and, 2025, "Splice Skills"/plugins.)
- **Evidence:** —
- **Why it matters for the studio:** Retrieval-and-assembly of *licensed human material* as an alternative to generation — a legally clean "compile" strategy for audio texture.
- **Tags:** [product] [audio-generation] [toolkit]
- **Verification:** partial (page fetched but content JS-rendered)
- **BibKey:** splice2024create

### AbletonMCP — Ableton MCP (LLM → Ableton Live bridge) and the LLM-agent-in-DAW wave
- **Who/where/when:** Siddharth Ahuja (ahujasid), open-source, Mar 2025; many forks (jpoindexter 200+ tools; LofiFren; itsuzef); parallel projects for Logic/REAPER/Bitwig/FL via MCP or OSC.
- **Links:** https://github.com/ahujasid/ableton-mcp
- **What it is:** [S][I] MIT-licensed MCP server + Ableton Remote Script over a socket; Claude/other LLMs create tracks, MIDI clips and notes, load instruments/effects, set tempo/playback, and build arrangements in Arrangement View from natural-language instructions. ~3k GitHub stars. Limitations noted by author: complex arrangements must be chunked; default devices only.
- **Evidence:** Community demos; no formal study.
- **Why it matters for the studio:** Proof of demand for *conversational control of a DAW* and a reusable pattern (tool-calling agent → structured music edits). Cross-ref LLM-agent cluster.
- **Tags:** [product] [LLM-agent] [DAW-plugin] [symbolic-generation] [toolkit]
- **Verification:** verified
- **BibKey:** ahuja2025abletonmcp

### ComposersAssistant2 — Composer's Assistant 2 (REAPER)
- **Who/where/when:** Martin E. Malandro, Sam Houston State University; CA1 ISMIR 2023 (arXiv 2301.12525), CA2 ISMIR 2024 (arXiv 2407.14700).
- **Links:** https://arxiv.org/abs/2407.14700 ; https://github.com/m-malandro/composers-assistant-REAPER
- **What it is:** [S][I] T5-like transformer for **multi-track MIDI infilling at the track–measure level** inside REAPER: the user deletes/selects bars on any tracks and the model fills them, with controls for rhythmic conditioning (2 types), horizontal/vertical onset density, pitch range/steps, "rhythmic interest". Code, weights and REAPER scripts released (CC BY 4.0).
- **Evidence:** Listening studies (CA1 and CA2) found no significant quality difference between infilled and original human passages.
- **Why it matters for the studio:** The cleanest open-source instantiation of "edit → compile the hole" in a real DAW with fine-grained controls; directly reusable. Cross-ref infilling cluster.
- **Tags:** [symbolic-generation] [infilling] [DAW-plugin] [controllability] [editing]
- **Verification:** verified
- **BibKey:** malandro2024composersassistant2

### MIDIGPT — MIDI-GPT (Metacreation Lab) with REAPER/Ableton (Calliope) front-ends
- **Who/where/when:** Philippe Pasquier, Jeff Ens, Renaud Bougueng Tchemeube et al., Metacreation Lab, Simon Fraser University; MMM (2020) → MIDI-GPT paper (AAAI 2025); Calliope interface (ICCC 2022); midigpt-REAPER plugin (2025).
- **Links:** https://www.metacreation.net/projects/midi-gpt ; https://github.com/Metacreation-Lab/MIDI-GPT ; https://github.com/Metacreation-Lab/midigpt-REAPER
- **What it is:** [S][I] GPT-2-style model over General MIDI (up to 128 instruments, 10+ tracks) supporting continuation, **bar-level multi-track infilling**, and attribute control (instrument, style, note density, polyphony, duration; velocity/micro-timing tokens). Trained on GigaMIDI; released under Open RAIL-M (non-commercial). Deployed in DAWs, synths (Teenage Engineering collab) and game tools.
- **Evidence:** Paper evaluates originality, stylistic similarity and control effectiveness (density/duration controls effective, polyphony weaker).
- **Why it matters for the studio:** Alternative open infilling backbone with explicit attribute sliders; its RAIL licence and GigaMIDI provenance illustrate the licensing trade-offs the studio must weigh.
- **Tags:** [symbolic-generation] [infilling] [controllability] [DAW-plugin]
- **Verification:** verified (project page) / partial (venue)
- **BibKey:** pasquier2025midigpt

### MagentaStudio — Magenta Studio 2.0 (Ableton) and Magenta RealTime / "Live Music Models"
- **Who/where/when:** Google Magenta (Adam Roberts et al.); Magenta Studio 1.0 (2019) → 2.0 (Max-for-Live devices, 2023); Magenta RealTime open weights (June 2025) with paper "Live Music Models" (arXiv 2508.04651, Aug 2025).
- **Links:** https://magenta.tensorflow.org/studio-announce-2 ; https://arxiv.org/abs/2508.04651 ; https://github.com/magenta/magenta-realtime
- **What it is:** [S]+[A][I] Studio: five MIDI devices (Continue, Generate, Interpolate, Groove, Drumify) operating on selected clips with temperature/length/variation knobs. Magenta RealTime: ~800M-param open-weights model generating continuous audio in 2-s chunks steerable in real time by weighted text/audio style prompts; Lyria RealTime is the larger API sibling.
- **Evidence:** Paper: beats other open-weights models on automatic quality metrics at lower compute.
- **Why it matters for the studio:** Magenta Studio remains the reference for *clip-level symbolic tools inside a DAW*; Magenta RT is the only open, real-time steerable audio model (live "audio compile").
- **Tags:** [symbolic-generation] [audio-generation] [real-time] [DAW-plugin] [toolkit]
- **Verification:** verified (arXiv) / partial (authors, size)
- **BibKey:** magenta2025livemusicmodels

### WavTool — WavTool (browser DAW with GPT-4 "Conductor") → acquired by Suno
- **Who/where/when:** WavTool (2023, San Francisco); acquired by Suno 30 June 2025.
- **Links:** https://suno.com/blog/suno-acquires-wavtool
- **What it is:** [S]+[A][I] Browser DAW with VST support, sample-accurate editing, stem separation, AI-generated MIDI, and a chat assistant ("Conductor", GPT-4) that edits the project from natural language. Became the basis of Suno Studio.
- **Evidence:** —
- **Why it matters for the studio:** Early "LLM inside the DAW" product; its acquisition shows the text-to-song leaders buying *editability*.
- **Tags:** [product] [LLM-agent] [DAW-plugin]
- **Verification:** verified
- **BibKey:** suno2025wavtool

### SynthV2 — Synthesizer V Studio 2 Pro (Dreamtonics) and the AI-singer category (ACE Studio, Vocaloid 6, Kits.ai)
- **Who/where/when:** Dreamtonics (Kanru Hua), SV Studio 2 Pro announced Dec 2024, released 2025; ACE Studio (Timedomain, 2022→2025 v1.9+); Yamaha Vocaloid 6 (Oct 2022, VOCALO CHANGER); Kits.ai (2023→, licensed artist voices).
- **Links:** https://dreamtonics.com/synthesizerv/ ; https://acestudio.ai ; https://www.vocaloid.com ; https://www.kits.ai
- **What it is:** [S→A][I] Note-level piano-roll + lyrics → sung vocals with per-note pitch/timbre/breath editing, style/vocal-mode parameters, AI retakes; ACE Studio adds audio-to-MIDI+lyrics import and expressive "AI Pitch"; Vocaloid 6 adds voice-to-voice conversion; Kits.ai sells licensed, revenue-shared artist voice models.
- **Evidence:** —
- **Why it matters for the studio:** These are *symbolic-first* vocal renderers — a compiled score's vocal line can be rendered without any text-to-song model, keeping authorship with the composer. Also models a consent-based voice-licensing business (Kits.ai).
- **Tags:** [product] [expression-performance] [symbolic-generation] [notation] [ethics-legal]
- **Verification:** partial
- **BibKey:** dreamtonics2025synthv2

### NeutoneMorpho — Neutone Morpho / Neutone FX
- **Who/where/when:** Neutone Inc. (Tokyo/London, ex-Qosmo); Neutone FX (2022) hosts community RAVE-style models; Morpho (2024) real-time tone morphing.
- **Links:** https://neutone.ai ; https://neutone.jp/morpho
- **What it is:** [A][I] VST3/AU plugin running neural audio models in real time: transforms incoming audio's timbre into a trained model's (instruments, voices, textures) with dry/wet, latency compensation; SDK for artists to train/publish models on their own recordings.
- **Evidence:** STARTS Prize nomination; used in electronic/experimental practice.
- **Why it matters for the studio:** "Insert example audio" as a *timbre* annotation is realisable with models trained on the composer's own material — an ethical audio-level counterpart to the symbolic core.
- **Tags:** [product] [audio-generation] [style-transfer] [real-time] [DAW-plugin]
- **Verification:** partial
- **BibKey:** neutone2024morpho

### ProductTable — Other tools (summary table)

| Tool | Maker / status (Sept 2026) | Level | Iterative? | Notes | Verif. |
|---|---|---|---|---|---|
| AIVA | AIVA Technologies (LU), since 2016; subscription; SACEM-registered "composer" | S+A | I (edit generated MIDI, style models) | Trained on classical/PD scores + licensed; MIDI export | partial |
| Boomy | Boomy Corp; 2019→; distribution to DSPs; implicated in the Michael Smith fraud (tracks credited to CEO) | A | 1 (style rerolls) | Focus on non-musicians | partial |
| Soundraw | Soundraw Inc. (JP); royalty-free | A | I (section-level mood/length edits) | In-house composed training data claim | partial |
| Beatoven.ai | India; royalty-free background music; "licensed/consented" data claim | A | I (mood/section) | Video-length aware | partial |
| Loudly | Berlin; text→music, playlists, licensing | A | partial | Own licensed catalogue claim | partial |
| Soundful | San Diego; template-based; "human-created samples" | A | partial | Loops→tracks | partial |
| Tuney | London; adaptive/video music, "trained on licensed music" | A | I (length/edits) | B2B | partial |
| LANDR | Montreal; AI mastering (2014→), Stems, Composer, sample search | A | I | Mastering; plugins | partial |
| iZotope (Native Instruments) | Ozone/Neutron/Nectar "assistants" (ML-assisted mix/master since 2016) | A | I | Not generative | partial |
| FL Studio 2024/2025 | Image-Line; stem separation (2024), Gopher AI mastering | A | — | No gen-AI composition | partial |
| Bitwig Studio 5.x | Bitwig; The Grid; no ML features | — | — | Community MCP bridges exist | partial |
| StaffPad | David William Hearn; handwriting→notation (2015, MS Surface/iPad) | S | I | Pen input as primary; no AI composition | partial |
| ScoreCloud | DoReMIR (SE); audio/MIDI→notation transcription | S | I | Sing/play → score | partial |
| Flat.io / Noteflight | Browser notation editors (Tutteo; Hal Leonard) | S | I | Flat has a Chrome/Google Classroom base; no gen-AI | partial |
| Soundslice | Adrian Holovaty; sheet music + synced audio/video; AI scanning of sheet music (2024–25) | S | I | Also transcribes tab; no generation | partial |
| Jambot | Independent (2024); in-DAW/browser AI jam partner | A | real-time | Status unclear | unverified |
| Session (AI drummer) | Various products named "Session"; not uniquely identifiable | — | — | Could not verify a specific product | unverified |
| Kits.ai | Licensed artist voice models, royalty-sharing | A | I | Voice conversion | partial |
| Vocaloid 6 / ACE Studio | Yamaha / Timedomain AI singers | S→A | I | See SynthV2 entry | partial |
| Riffusion (orig.) | Forsgren & Martiros, Dec 2022 open-source spectrogram diffusion; relaunched 2025 (FUZZ) → Producer.ai → Google Flow Music (Feb 2026) | A | I | See Lyria entry | verified |
| Band-in-a-Box 2026 | PG Music; annual; RealTracks | S+A | I | See history entry | verified |

---

# C. Evaluation methodology

### FAD — Fréchet Audio Distance
- **Who/where/when:** Kevin Kilgour, Mauricio Zuluaga, Dominik Roblek, Matthew Sharifi; Google; Interspeech 2019 (arXiv 1812.08466, Dec 2018).
- **Links:** https://arxiv.org/abs/1812.08466 ; https://github.com/google-research/google-research/tree/master/frechet_audio_distance
- **What it is:** Fréchet distance between Gaussians fit to VGGish embeddings of reference vs evaluated audio sets; originally proposed for music *enhancement*, then adopted as the default metric for generative music/audio.
- **Evidence:** Correlated with human ratings of enhancement artefacts in the original paper only.
- **Why it matters for the studio:** Ubiquitous but flawed baseline; know its assumptions before using it for rendered output.
- **Tags:** [evaluation] [audio-generation]
- **Verification:** partial
- **BibKey:** kilgour2019fad

### FADadapt — Adapting Fréchet Audio Distance for Generative Music Evaluation (fadtk)
- **Who/where/when:** Azalea Gui, Hannes Gamper, Sebastian Braun, Dimitra Emmanouilidou; Microsoft Research; ICASSP 2024.
- **Links:** https://arxiv.org/abs/2311.01616 ; https://github.com/microsoft/fadtk
- **What it is:** Shows FAD's sample-size bias, poor embedding choice (VGGish) and weak reference sets; proposes extrapolating to infinite sample size, using **CLAP-LAION-music** embeddings and music reference sets, and **per-song FAD** for outlier detection.
- **Evidence:** Correlated with human listening data and MusicCaps quality annotations across several generative systems.
- **Why it matters for the studio:** If FAD is used at all, use fadtk's recipe.
- **Tags:** [evaluation] [audio-generation] [toolkit]
- **Verification:** verified
- **BibKey:** gui2024fad

### KAD — KAD: No More FAD! Kernel Audio Distance
- **Who/where/when:** Yoonjin Chung, Pilsun Eu, Junwon Lee, Keunwoo Choi, Juhan Nam, Ben Sangbae Chon; Gaudio Lab / KAIST; arXiv Feb 2025 (ICASSP-track).
- **Links:** https://arxiv.org/abs/2502.15602 ; https://github.com/YoonjinXD/kadtk
- **What it is:** Replaces the Gaussian/Fréchet assumption with an MMD kernel distance: distribution-free, unbiased, converges with small sample sizes, GPU-scalable.
- **Evidence:** Reports stronger alignment with human perceptual judgments than FAD.
- **Why it matters for the studio:** Preferred distributional metric for any audio renderer evaluation in 2026.
- **Tags:** [evaluation] [audio-generation] [toolkit]
- **Verification:** verified
- **BibKey:** chung2025kad

### FMD — Fréchet Music Distance (symbolic)
- **Who/where/when:** Jan Retkowski, Jakub Stępniak, Mateusz Modrzejewski; Warsaw University of Technology; arXiv Dec 2024 (rev. Jan 2025), COLING 2025.
- **Links:** https://arxiv.org/abs/2412.07948 ; https://github.com/jryban/frechet-music-distance
- **What it is:** Fréchet distance over embeddings of *symbolic* music (CLaMP 2 / MusicGen-encoder–style) between reference and generated MIDI/ABC sets; validated to separate model quality levels across datasets.
- **Evidence:** Sensitivity experiments across models/datasets; released code.
- **Why it matters for the studio:** The first standard distributional metric for **symbolic** output — the studio's native domain.
- **Tags:** [evaluation] [symbolic-generation] [toolkit]
- **Verification:** verified
- **BibKey:** retkowski2024fmd

### YangLerch — On the evaluation of generative models in music
- **Who/where/when:** Li-Chia Yang & Alexander Lerch, Georgia Tech; *Neural Computing and Applications* 32, 4773–4784 (online 2018, print 2020).
- **Links:** https://doi.org/10.1007/s00521-018-3849-7 ; https://github.com/RichardYang40148/mgeval
- **What it is:** Proposes objective, interpretable symbolic features (pitch count/class histogram/transition matrix, note length histogram/transitions, IOI etc.) and compares *distributions* of generated vs training sets via KL/overlap (absolute + relative measures) — the "mgeval" toolkit.
- **Evidence:** Demonstrated on MIDI generation systems; widely used as a first-pass check.
- **Why it matters for the studio:** Cheap, transparent symbolic diagnostics that composers can read (e.g., "your compiled bass has an unusual IOI distribution vs your own sketches").
- **Tags:** [evaluation] [symbolic-generation] [toolkit]
- **Verification:** partial
- **BibKey:** yang2020evaluation

### CLAPscore — CLAP score, MusicCaps and Song Describer for text-to-music evaluation
- **Who/where/when:** CLAP: Yusong Wu et al. (LAION-CLAP, ICASSP 2023) and Elizalde et al. (Microsoft CLAP, 2023). MusicCaps: Agostinelli et al. (MusicLM, 2023) — 5.5k 10-s AudioSet clips with expert captions. Song Describer Dataset: Ilaria Manco, Benno Weck et al. (NeurIPS 2023 ML4Audio workshop) — 1.1k crowd captions on 706 CC-licensed full tracks.
- **Links:** https://arxiv.org/abs/2211.06687 ; https://www.kaggle.com/datasets/googleai/musiccaps ; https://arxiv.org/abs/2311.10057
- **What it is:** CLAP score = cosine similarity between text-prompt and audio embeddings (prompt adherence); MusicCaps/SDD provide caption–audio pairs as references. SDD was created partly because MusicCaps is YouTube-derived (licence/availability issues).
- **Evidence:** Used across MusicGen/AudioLDM/Stable Audio papers; 2025 studies show CLAP score correlates only moderately with human preference.
- **Why it matters for the studio:** Text is one of the studio's annotation modalities; CLAP-style alignment scores can be a *soft* check that a rendered passage matches a textual annotation, not a quality metric.
- **Tags:** [evaluation] [text-conditioning] [dataset]
- **Verification:** partial
- **BibKey:** wu2023clap

### MuChoMusic — MuChoMusic: Evaluating Music Understanding in Multimodal Audio-Language Models
- **Who/where/when:** Benno Weck, Ilaria Manco, Emmanouil Benetos, Elio Quinton, George Fazekas, Dmitry Bogdanov; UPF/QMUL/UMG; ISMIR 2024.
- **Links:** https://arxiv.org/abs/2408.01337 ; https://github.com/mulab-mir/muchomusic
- **What it is:** 1,187 human-validated multiple-choice questions on 644 tracks testing knowledge/reasoning about music (theory, structure, culture, function) in audio-LLMs.
- **Evidence:** Five open audio-LLMs show over-reliance on the language modality (answer without really listening).
- **Why it matters for the studio:** If the studio uses an audio-LLM to "listen to" hummed/inserted audio annotations, MuChoMusic is the benchmark that tells you how much it actually hears.
- **Tags:** [evaluation] [multimodal-input] [dataset]
- **Verification:** verified
- **BibKey:** weck2024muchomusic

### MusicEval — MusicEval: A Generative Music Dataset with Expert Ratings for Automatic Text-to-Music Evaluation
- **Who/where/when:** Cheng Liu, Hui Wang, Jinghua Zhao, Shiwan Zhao, Hui Bu, Xin Xu, Jiaming Zhou, Haoqin Sun, Yong Qin; Nankai University / AISHELL; ICASSP 2025 (arXiv Jan 2025).
- **Links:** https://arxiv.org/abs/2501.10811 ; https://www.aishelltech.com/AISHELL_7A
- **What it is:** 2,748 clips from 31 text-to-music systems over 384 prompts rated by 14 music professionals (13,740 ratings) on overall musical impression and text alignment; a CLAP-based MOS predictor baseline. Basis of AudioMOS Challenge 2025 Track 1.
- **Evidence:** Dataset + baseline released.
- **Why it matters for the studio:** Expert-rated reference data for training/validating any automatic "does the render match the annotation" judge.
- **Tags:** [evaluation] [dataset] [text-conditioning]
- **Verification:** verified
- **BibKey:** liu2025musiceval

### AudioMOS — AudioMOS Challenge 2025 and ICASSP 2026 Automatic Song Aesthetics Evaluation (ASAE) Challenge
- **Who/where/when:** AudioMOS: Wen-Chin Huang, Hui Wang, Cheng Liu, Yi-Chiao Wu, Andros Tjandra, Wei-Ning Hsu, Erica Cooper, Yong Qin, Tomoki Toda (Nagoya/Nankai/Meta/NII), arXiv Sept 2025 (ASRU 2025). ASAE: ICASSP 2026 grand challenge (arXiv 2601.07237, Jan 2026).
- **Links:** https://arxiv.org/abs/2509.01336 ; https://arxiv.org/abs/2601.07237
- **What it is:** Shared tasks for *predicting* human quality ratings of generated audio: AudioMOS Track 1 = text-to-music overall quality + text alignment (MusicEval), Track 2 = Meta **Audiobox Aesthetics** four axes (production quality, complexity, enjoyment, usefulness) across TTS/TTA/TTM; ASAE = overall musicality plus five aesthetic dimensions of full AI songs. 24 teams (AudioMOS); baselines beaten.
- **Evidence:** Community benchmarks; establishes MOS-prediction as a research line.
- **Why it matters for the studio:** Off-the-shelf aesthetic predictors (Audiobox Aesthetics, winning ASAE systems) can rank candidate renders before the composer hears them — a cheap pre-filter in a compile loop.
- **Tags:** [evaluation] [audio-generation]
- **Verification:** verified
- **BibKey:** huang2025audiomos

### HumanPrefBench — Benchmarking Music Generation Models and Metrics via Human Preference Studies
- **Who/where/when:** Florian Grötschla, Ahmet Solak, Luca A. Lanzendörfer, Roger Wattenhofer; ETH Zürich; ICASSP 2025 (arXiv June 2025).
- **Links:** https://arxiv.org/abs/2506.19085 ; https://doi.org/10.1109/ICASSP49660.2025.10887745
- **What it is:** 6,000 songs from 12 SOTA generators; 15,000 pairwise comparisons by 2,500 raters; ranks models and computes correlation of FAD/KAD/CLAP and other metrics with human preference; data released.
- **Evidence:** First human-preference ranking of current models; documents metric–human gaps.
- **Why it matters for the studio:** Methodological template (pairwise, large-N, open data) and a caution against metric-driven claims.
- **Tags:** [evaluation] [audio-generation] [dataset]
- **Verification:** verified
- **BibKey:** grotschla2025benchmarking

### AestheticsVsPref — From Aesthetics to Human Preferences: Comparative Perspectives of Evaluating Text-to-Music Systems
- **Who/where/when:** Huan Zhang, Jinhua Liang, Huy Phan, Wenwu Wang, Emmanouil Benetos; QMUL/Surrey; arXiv 30 Apr 2025.
- **Links:** https://arxiv.org/abs/2504.21815
- **What it is:** Compares perceptual aesthetic scores and distributional metrics (Mauve Audio Divergence, KAD) against human preferences over five leading TTM systems; finds automatic metrics inconsistent with human judgment; releases a multi-model benchmark set.
- **Evidence:** Human study across five systems.
- **Why it matters for the studio:** Independent confirmation that human-centred evaluation must be primary.
- **Tags:** [evaluation] [audio-generation]
- **Verification:** verified
- **BibKey:** zhang2025aesthetics

### EvalSurvey — A Survey on Evaluation Metrics for Music Generation
- **Who/where/when:** Faria Binte Kader & Santu Karmaker; University of Central Florida; arXiv Aug 2025.
- **Links:** https://arxiv.org/abs/2509.00051
- **What it is:** Taxonomy of objective (symbolic and audio) and subjective metrics; identifies poor metric–perception correlation, cross-cultural bias and lack of standardisation; proposes directions for a comprehensive framework.
- **Evidence:** Survey.
- **Why it matters for the studio:** One-stop map for the literature review's evaluation section.
- **Tags:** [evaluation]
- **Verification:** verified
- **BibKey:** kader2025survey

### Boden — Boden's P-/H-creativity and exploratory/combinational/transformational creativity
- **Who/where/when:** Margaret A. Boden, University of Sussex; *The Creative Mind: Myths and Mechanisms* (1990; 2nd ed. Routledge 2004).
- **Links:** https://doi.org/10.4324/9780203508527
- **What it is:** Psychological (P-) vs historical (H-) creativity; three kinds of creativity — combinational, exploratory (within a conceptual space), transformational (changing the space). Standard vocabulary in computational creativity.
- **Evidence:** Theoretical.
- **Why it matters for the studio:** Lets the project state precisely what the AI is expected to do: mostly *exploratory* generation inside the composer-defined space, with the human providing transformational moves.
- **Tags:** [evaluation] [co-creation-framework] [creativity-support]
- **Verification:** partial
- **BibKey:** boden2004creativemind

### Ritchie — Some empirical criteria for attributing creativity to a computer program
- **Who/where/when:** Graeme Ritchie, University of Aberdeen; *Minds and Machines* 17(1), 67–99, 2007 (earlier 2001 workshop version).
- **Links:** https://doi.org/10.1007/s11023-007-9066-2
- **What it is:** Eighteen formal criteria over an "inspiring set" and output set using ratings of *typicality* and *quality*: novelty relative to the inspiring set, proportion of good/typical outputs, etc.
- **Evidence:** Applied to several CC systems (e.g., by Pereira et al.).
- **Why it matters for the studio:** Gives a principled way to measure whether compiled output is *both* stylistically typical of the composer's material and of high quality without merely copying it.
- **Tags:** [evaluation] [co-creation-framework]
- **Verification:** partial
- **BibKey:** ritchie2007criteria

### ColtonTripod — Creativity versus the perception of creativity in computational systems (the "creative tripod")
- **Who/where/when:** Simon Colton, Imperial College London; AAAI Spring Symposium on Creative Intelligent Systems, 2008.
- **Links:** https://www.aaai.org/Papers/Symposia/Spring/2008/SS-08-03/SS08-03-003.pdf
- **What it is:** A system is perceived as creative if it exhibits **skill, appreciation and imagination** (the tripod); emphasises framing/perception and later (Colton & Wiggins 2012; Colton, Charnley & Pease's FACE/IDEA) the need for systems to explain themselves.
- **Evidence:** Conceptual; applied to The Painting Fool.
- **Why it matters for the studio:** "Appreciation" = the AI's ability to evaluate its own output against the composer's annotations — the missing leg in most generators and a design goal for the compiler.
- **Tags:** [evaluation] [co-creation-framework]
- **Verification:** partial
- **BibKey:** colton2008tripod

### SPECS — A Standardised Procedure for Evaluating Creative Systems (SPECS)
- **Who/where/when:** Anna Jordanous, University of Kent; *Cognitive Computation* 4(3), 246–279, 2012.
- **Links:** https://doi.org/10.1007/s12559-012-9156-1
- **What it is:** Three-step methodology: (1) define creativity for the domain using 14 empirically derived components (e.g., originality, value, intention & emotional involvement, domain competence, social interaction, spontaneity, variety…), (2) choose standards, (3) test against them; case study on musical improvisation systems.
- **Evidence:** Applied to GenJam-like improvisers and others; meta-evaluation paper (ICCC 2014).
- **Why it matters for the studio:** A reusable checklist for defining what "creative support" means for *this* studio before running studies.
- **Tags:** [evaluation] [co-creation-framework]
- **Verification:** partial
- **BibKey:** jordanous2012specs

### CSI — Quantifying the Creativity Support of Digital Tools through the Creativity Support Index
- **Who/where/when:** Erin Cherry & Celine Latulipe, UNC Charlotte; *ACM TOCHI* 21(4), 2014 (earlier CHI EA 2009 "The creativity support index", Carroll & Latulipe).
- **Links:** https://doi.org/10.1145/2617588
- **What it is:** Psychometric questionnaire with six factors — **Exploration, Expressiveness, Immersion, Enjoyment, Results Worth Effort, Collaboration** — each rated on two agreement items, plus paired-factor comparisons that weight factors by importance for the task, yielding a 0–100 score.
- **Evidence:** Validated across multiple tool studies; now the default instrument in music co-creation papers (e.g., Cococo, Louie et al. 2020; AI Song Contest follow-ups).
- **Why it matters for the studio:** The primary quantitative instrument for iterating on the studio's UI; report per-factor scores, and pair with ownership/agency items.
- **Tags:** [evaluation] [creativity-support] [HCI-study]
- **Verification:** partial (DOI known; page 403)
- **BibKey:** cherry2014csi

### KarimiCoCreative — Evaluating Creativity in Computational Co-Creative Systems
- **Who/where/when:** Pegah Karimi, Kazjon Grace, Mary Lou Maher, Nicholas Davis; UNC Charlotte / U. Sydney; ICCC 2018 (arXiv 1807.09886).
- **Links:** https://arxiv.org/abs/1807.09886
- **What it is:** Framework of four questions for co-creative evaluation — **who** evaluates (human/AI/both), **what** is evaluated (product, process, interaction/collaboration), **when** (during/after/continuous), **how** (metrics, qualitative, user studies); surveys existing systems and finds most evaluate only user experience.
- **Evidence:** Survey/framework across visual art, humour, games, robotics.
- **Why it matters for the studio:** Structures the evaluation plan: the studio should evaluate the *interaction* (annotation→compile turn-taking) and the *process*, not just final pieces.
- **Tags:** [evaluation] [co-creation-framework] [mixed-initiative]
- **Verification:** verified
- **BibKey:** karimi2018evaluating

### KantosaloModes — Modes for creative human–computer collaboration: alternating and task-divided co-creativity
- **Who/where/when:** Anna Kantosalo & Hannu Toivonen, University of Helsinki; ICCC 2016; extended in Kantosalo's 2019 PhD and "Human–computer co-creativity: designing, evaluating and modelling" work.
- **Links:** https://computationalcreativity.net/iccc2016/wp-content/uploads/2016/01/Modes-for-Creative-Human-Computer-Collaboration.pdf
- **What it is:** Distinguishes **alternating** co-creativity (turn-taking on the same artefact) from **task-divided** co-creativity (agents own different sub-tasks); evaluated with the Poetry Machine in classrooms.
- **Evidence:** School studies (children writing poetry) with qualitative + questionnaire data.
- **Why it matters for the studio:** The founder's loop is *alternating* at the artefact level (compose↔compile) but *task-divided* at the role level (human = ideas/annotations, AI = realisation). Naming this helps the taxonomy.
- **Tags:** [co-creation-framework] [mixed-initiative] [evaluation]
- **Verification:** partial
- **BibKey:** kantosalo2016modes

### CMUCreativity — CMU study: AI-assisted vs unassisted melody composition (Oros, Telang, Randall)
- **Who/where/when:** Jose Oros, Rahul Telang (Heinz College) & Richard Randall (School of Music), Carnegie Mellon; CMU News 30 Jan 2026; poster MIT CODE Nov 2025; dissertation defence May 2026 (working paper).
- **Links:** https://www.cmu.edu/news/stories/archives/2026/january/as-ai-generated-music-advances-humans-still-lead-in-creativity-cmu-research-finds
- **What it is:** Randomised experiment: 140 musically trained participants composed 15-s piano melodies, half with access to Udio-generated "inspiration", half without; independent raters judged creativity, enjoyment, musicality.
- **Evidence:** AI-assisted composers were **slower, wrote fewer notes and received lower creativity ratings**; human-only melodies outperformed the AI inspirations themselves. Authors note AI "lowers the bar" for low-knowledge users.
- **Why it matters for the studio:** Direct evidence that one-shot audio inspiration can *hurt* trained composers — supporting the studio's premise that AI should realise the composer's ideas rather than supply them. (Cross-ref agent 02.)
- **Tags:** [evaluation] [HCI-study] [creativity-support]
- **Verification:** verified (press release; paper not yet published)
- **BibKey:** oros2026cmu

### EchoesHumanity — Echoes of Humanity: Exploring the Perceived Humanness of AI Music
- **Who/where/when:** Flavio Figueiredo, Giovanni Martinelli, Henrique Sousa, Pedro Rodrigues, Frederico Pedrosa, Lucas N. Ferreira; UFMG (Brazil); NeurIPS 2025 Creative AI track (arXiv 2509.25601).
- **Links:** https://arxiv.org/abs/2509.25601
- **What it is:** Blind, Turing-like pairwise test with a randomised crossover design on *real-world* Suno outputs vs human songs, controlling pairwise similarity; free-text justifications analysed.
- **Evidence:** Listeners' ability to spot the AI track **causally increases when pairs are similar**; cues cited are mostly vocal/technical.
- **Why it matters for the studio:** Methodological template for "can listeners tell compiled from hand-arranged" tests; pair-matching matters.
- **Tags:** [evaluation] [HCI-study]
- **Verification:** verified
- **BibKey:** figueiredo2025echoes

### DeezerIpsos — Deezer/Ipsos survey: 97% cannot tell AI from human music
- **Who/where/when:** Deezer & Ipsos Digital; 9,000 adults in 8 countries, fielded 6–10 Oct 2025, published 12 Nov 2025.
- **Links:** https://newsroom-deezer.com/2025/11/deezer-ipsos-survey-ai-music/
- **What it is:** Blind listening + attitudes: 97% failed to distinguish fully-AI tracks; 71% surprised; 52% uncomfortable; 80% want labelling; 70% see a threat to musicians' livelihoods; 65% oppose training on copyrighted material.
- **Evidence:** Large-N cross-national survey (industry-commissioned).
- **Why it matters for the studio:** Public appetite for disclosure/labelling and for human authorship — supports provenance metadata as a studio feature.
- **Tags:** [evaluation] [ethics-legal] [HCI-study]
- **Verification:** verified
- **BibKey:** deezer2025ipsos

### MiRA — Towards Assessing Data Replication in Music Generation with Music Similarity Metrics on Raw Audio (MiRA)
- **Who/where/when:** Roser Batlle-Roca, Wei-Hsiang Liao, Xavier Serra, Yuki Mitsufuji, Emilia Gómez; UPF Barcelona / Sony AI; ISMIR 2024 (arXiv 2407.14364).
- **Links:** https://arxiv.org/abs/2407.14364 ; https://github.com/roserbatlleroca/mira
- **What it is:** Model-independent tool using several audio similarity metrics (CLAP, DEfNet/Discogs-EffNet, CoverID, etc.) to detect *exact* replication of training data in generated audio; validated with controlled synthetic replication across genres.
- **Evidence:** Detects exact replication at proportions above ~10%; released for transparency audits.
- **Why it matters for the studio:** Any renderer the studio ships should be audited for memorisation; MiRA is the open baseline.
- **Tags:** [evaluation] [ethics-legal] [audio-generation] [toolkit]
- **Verification:** verified
- **BibKey:** batlleroca2024mira

### SunoUdioAnalysis — Data-Driven Analysis of Text-Conditioned AI-Generated Music: A Case Study with Suno and Udio
- **Who/where/when:** Luca Casini, Laura Cros Vila, David Dalmazzo, Anna-Kaisa Kaila, Bob L. T. Sturm; KTH Stockholm (MUSAiC); arXiv Sept 2025.
- **Links:** https://arxiv.org/abs/2509.11824
- **What it is:** Large-scale analysis of user prompts, metatags and generated lyrics from Suno and Udio (May–Oct 2024) using text embeddings/clustering; identifies lyrical themes, language use and "peculiar" steering strategies via metatags.
- **Evidence:** Corpus analysis with interactive plots.
- **Why it matters for the studio:** Empirical picture of how people actually try to *control* text-to-song systems — the pain points a symbolic, annotation-based interface should solve.
- **Tags:** [evaluation] [text-conditioning] [HCI-study]
- **Verification:** verified
- **BibKey:** casini2025sunoudio

### TrainingWatermark — Watermarking Training Data of Music Generation Models
- **Who/where/when:** Pascal Epple, Igor Shilov, Bozhidar Stevanoski, Yves-Alexandre de Montjoye; Imperial College London; arXiv Dec 2024 (rev. 2025).
- **Links:** https://arxiv.org/abs/2412.08549
- **What it is:** Tests whether audio watermarks in training data survive into a music generator's outputs (MusicGen fine-tuning), as a membership/provenance mechanism for rights-holders.
- **Evidence:** Watermarks partially detectable in outputs depending on strength/proportion.
- **Why it matters for the studio:** Provenance tooling relevant to dataset governance for an open model.
- **Tags:** [ethics-legal] [evaluation] [audio-generation]
- **Verification:** partial
- **BibKey:** epple2024watermarking

---

# D. Ethics, law and policy (status as of 7 Sept 2026)

### LabelsVSuno — UMG Recordings et al. v. Suno (D. Mass. 1:24-cv-11611) and UMG et al. v. Uncharted Labs/Udio (S.D.N.Y. 1:24-cv-04777)
- **Who/where/when:** Filed 24 June 2024 by UMG, Sony Music and Warner (coordinated by RIAA). Sept 2025: plaintiffs sought to add **stream-ripping / DMCA §1201(a)** claims (YouTube circumvention); judge allowed the amendment (2025–26). **26 May 2026:** UMG & Sony moved to file a second amended complaint asserting **61,026** recordings after discovery showed training on "millions" of their recordings; dispositive-motion deadline Jan 2027 (scheduling order Mar 2026). Warner exited both cases via settlements (Nov 2025); Udio case resolved with UMG (Oct 2025) and WMG; **Sony and UMG v. Suno remains active** and is the bellwether for fair use in music-AI training.
- **Links:** https://www.musicbusinessworldwide.com/umg-and-sony-seek-to-add-61000-copyrighted-works-to-suno-lawsuit-after-discovery-reveals-suno-trained-on-millions-of-their-recordings/ ; https://www.musicbusinessworldwide.com/files/2026/05/UMG_Sony_Suno.pdf
- **What it is:** Direct infringement (unlicensed copying for training), plus §1201 anti-circumvention; Suno/Udio plead fair use and (initially) refused to disclose training data. Statutory damages up to $150k/work sought.
- **Evidence:** Complaints include side-by-side prompt outputs replicating recordings (e.g., producer-tag reproductions).
- **Why it matters for the studio:** Defines the legal risk of audio models trained on commercial recordings; underscores why the studio should not depend on such models and should keep provenance of everything it trains on.
- **Tags:** [ethics-legal] [audio-generation]
- **Verification:** verified
- **BibKey:** umg2024vsuno

### UMGUdio — UMG–Udio settlement and licensed platform (29 Oct 2025)
- **Who/where/when:** Universal Music Group & Udio; announced 29 Oct 2025; first partner agreements (publishers etc.) Nov 2025.
- **Links:** https://www.musicbusinessworldwide.com/universal-music-settles-udio-lawsuit-strikes-deal-for-licensed-ai-music-platform/
- **What it is:** Compensatory settlement (undisclosed) + recorded-music and publishing licences; a **2026 subscription platform** in a "walled garden" (no downloads, fingerprinting/filtering), artist/songwriter opt-in and revenue; Udio's current product continues with tightened controls (downloads disabled).
- **Evidence:** First settlement in the RIAA cases; strong user backlash; antitrust commentary.
- **Why it matters for the studio:** Sets the template — licensing in exchange for containment — that the rest of the industry (WMG–Suno) followed.
- **Tags:** [ethics-legal] [product]
- **Verification:** verified
- **BibKey:** umg2025udio

### WMGDeals — Warner Music Group settlements: Udio (19 Nov 2025), Stability AI partnership (19 Nov 2025), Suno (25 Nov 2025)
- **Who/where/when:** WMG (Robert Kyncl) with Udio, Stability AI and Suno, Nov 2025.
- **Links:** https://www.musicbusinessworldwide.com/warner-music-group-settles-with-suno-strikes-first-of-its-kind-deal-with-ai-song-generator/ ; https://musically.com/2025/11/19/wmg-becomes-second-major-label-to-sign-a-deal-with-stability-ai/
- **What it is:** WMG–Suno: Suno to launch **licensed models in 2026 and deprecate current ones**; artist **opt-in** for name/image/voice/compositions; **free tier cannot download** (play/share only), paid tiers get monthly caps with paid top-ups; Suno buys Songkick. WMG–Udio: licensed platform (mirrors UMG deal). WMG–Stability: co-develop "responsible" pro tools trained on licensed data.
- **Evidence:** Suno implemented the caps on 3 Sept 2026 (see Suno entry).
- **Why it matters for the studio:** Confirms the direction: licensed audio generation = constrained ownership. The studio's differentiator is user-owned symbolic output.
- **Tags:** [ethics-legal] [product]
- **Verification:** verified
- **BibKey:** wmg2025suno

### GEMAvOpenAI — GEMA v. OpenAI (LG München I, 42 O 14139/24, 11 Nov 2025)
- **Who/where/when:** Munich Regional Court I, 42nd Civil Chamber; GEMA (German collecting society) v. OpenAI over nine German song lyrics; judgment 11 Nov 2025 (appeal pending).
- **Links:** https://www.loc.gov/item/global-legal-monitor/2026-01-13/germany-court-prohibits-memorization-and-reproduction-of-copyrighted-song-lyrics-in-ai-models/
- **What it is:** Held that **memorisation of lyrics in model weights is a reproduction** (§16 UrhG) not covered by the text-and-data-mining exception (§44b UrhG, Art. 4 DSM Directive), and that outputting them is a further infringement attributable to OpenAI, not the prompting user; damages and injunction; OpenAI must license.
- **Evidence:** First European merits ruling on GenAI training/memorisation.
- **Why it matters for the studio:** Any model the studio trains/ships must avoid verbatim memorisation of protected works (lyrics *and* scores); public-domain/CC symbolic corpora avoid the issue.
- **Tags:** [ethics-legal]
- **Verification:** verified (LOC summary + law-firm notes)
- **BibKey:** lgmunich2025gemaopenai

### GEMAvSuno — GEMA v. Suno (LG München I, 42 O 763/25, **31 July 2026**)
- **Who/where/when:** Same chamber (presiding judge Elke Schwager); GEMA sued Jan 2025 over outputs resembling "Daddy Cool", "Rasputin", "Forever Young", "Big in Japan", "Atemlos", "Mambo No. 5"; oral hearing Jan 2026; judgment 31 July 2026; Suno says it will explore appeal. (**Note:** the ruling is July 2026, not January 2026 as sometimes reported; January was the hearing.)
- **Links:** https://www.juve-patent.com/cases/munich-regional-court-stops-suno-using-gema-protected-music/ ; https://variety.com/2026/digital/news/suno-loses-ai-lawsuit-gema-1236825010/
- **What it is:** Court found the works were "effectively stored" in Suno's models (memorisation → reproduction), that stream-ripping from YouTube circumvented technical protection, that §44b TDM does not apply where works are retained in reproducible form, and that Suno (not basic-prompt users) is liable for infringing outputs generated in Germany. Remedies: cease-and-desist, disclosure of revenues, damages TBD; not yet enforceable.
- **Evidence:** First European judgment against a music generator on the merits.
- **Why it matters for the studio:** Extends the OpenAI logic from lyrics to *music*; makes memorisation audits (MiRA) and clean data non-negotiable for any EU-distributed model.
- **Tags:** [ethics-legal] [audio-generation]
- **Verification:** verified
- **BibKey:** lgmunich2026gemasuno

### USCOReports — U.S. Copyright Office, *Copyright and Artificial Intelligence* Parts 1–3; Perlmutter dismissal
- **Who/where/when:** USCO (Register Shira Perlmutter). Part 1 *Digital Replicas* (31 July 2024); **Part 2 *Copyrightability* (29 Jan 2025)**; **Part 3 *Generative AI Training* pre-publication (9 May 2025)**; Perlmutter removed by the White House 10 May 2025 (litigation over the removal followed); final Part 3 not confirmed published as of Sept 2026.
- **Links:** https://www.copyright.gov/ai/ ; https://www.copyright.gov/ai/Copyright-and-Artificial-Intelligence-Part-3-Generative-AI-Training-Report-Pre-Publication-Version.pdf
- **What it is:** Part 2: prompts alone do not confer authorship; **human-authored expressive inputs, creative selection/arrangement, and modifications of AI output are protectable** to the extent of the human contribution; case-by-case. Part 3: training on copyrighted works is prima facie reproduction; fair use depends on transformativeness and market effects — likely fair for research/non-substitutive uses, **unlikely where outputs compete with the training works** or data was obtained illegally; endorses voluntary licensing markets.
- **Evidence:** Policy reports (not binding law) but heavily cited by courts and litigants.
- **Why it matters for the studio:** Part 2 is the strongest argument for the studio's design: notation written, edited and arranged by the composer, with AI as a tool, yields a *copyrightable* work; text-to-song outputs generally do not.
- **Tags:** [ethics-legal]
- **Verification:** partial (dates from multiple secondary sources)
- **BibKey:** usco2025part2

### Thaler — Thaler v. Perlmutter (D.C. Cir. 2025; cert. denied 2 Mar 2026)
- **Who/where/when:** Stephen Thaler (Creativity Machine, "A Recent Entrance to Paradise"); D.D.C. 2023 (Howell J.); D.C. Circuit affirmed 18 Mar 2025 (Millett J.); cert. petition No. 25-449 filed 9 Oct 2025; **certiorari denied 2 Mar 2026**.
- **Links:** https://www.scotusblog.com/cases/thaler-v-perlmutter/
- **What it is:** The Copyright Act requires a **human author**; a work autonomously generated by an AI with no human authorship is unregistrable. Question presented: whether AI outputs "without a direct, traditional authorial contribution by a natural person can be copyrighted." Left undecided: how much human contribution suffices.
- **Evidence:** Final for now in the U.S.
- **Why it matters for the studio:** Cements the value of keeping the human as author of record; the studio's provenance logs (who wrote/edited what) may become evidence of authorship.
- **Tags:** [ethics-legal]
- **Verification:** verified
- **BibKey:** thaler2025perlmutter

### EUAIAct — EU AI Act GPAI obligations (from 2 Aug 2025), GPAI Code of Practice (10 July 2025) and training-content summary template (24 July 2025)
- **Who/where/when:** European Parliament & Council, Regulation (EU) 2024/1689 (in force 1 Aug 2024); European Commission / AI Office guidelines and template, July 2025; obligations for general-purpose AI providers apply from 2 Aug 2025 (enforcement powers from Aug 2026; legacy models by Aug 2027).
- **Links:** https://digital-strategy.ec.europa.eu/en/policies/contents-code-gpai ; https://www.mayerbrown.com/en/insights/publications/2025/08/eu-ai-act-news-rules-on-general-purpose-ai-start-applying-guidelines-and-template-for-summary-of-training-data-finalized
- **What it is:** GPAI providers must keep technical documentation, adopt a **copyright policy** (respect machine-readable opt-outs under Art. 4(3) DSM), and publish a **"sufficiently detailed summary" of training content** using the Commission's template; the voluntary Code of Practice has a copyright chapter (lawful access, honour robots.txt/opt-outs, mitigate infringing outputs). Open-source models get some exemptions but **not** from the copyright policy and training summary duties.
- **Evidence:** Regulation + guidance; first enforcement from Aug 2026.
- **Why it matters for the studio:** If the studio releases model weights in the EU, it must publish a training-content summary and honour opt-outs — trivial if it trains only on PD/CC/consented data.
- **Tags:** [ethics-legal]
- **Verification:** partial
- **BibKey:** eu2024aiact

### ELVISAct — Tennessee ELVIS Act (Ensuring Likeness Voice and Image Security), signed 21 Mar 2024, effective 1 July 2024
- **Who/where/when:** Tennessee General Assembly / Gov. Bill Lee; first U.S. state law updating right of publicity to cover **voice** (incl. simulations) against unauthorised AI clones; followed by similar bills in other states and federal NO FAKES Act proposals (2024–25).
- **Links:** https://www.tn.gov/governor/news/2024/3/21/photos--gov--lee-signs-elvis-act-into-law.html
- **What it is:** Civil liability for unauthorised use of an individual's voice/likeness and for distributing tools whose primary purpose is producing such replicas.
- **Evidence:** Legislation.
- **Why it matters for the studio:** Any voice-rendering feature must use consented/licensed voice models (Kits.ai-style) or synthetic voices.
- **Tags:** [ethics-legal] [expression-performance]
- **Verification:** partial
- **BibKey:** tennessee2024elvis

### FairlyTrained — Fairly Trained certification and Ed Newton-Rex's resignation from Stability AI
- **Who/where/when:** Ed Newton-Rex resigned as VP Audio at Stability AI 15 Nov 2023 over the company's fair-use stance on training; launched non-profit **Fairly Trained** 17 Jan 2024 (Licensed Model certification; standards tightened 2025).
- **Links:** https://www.fairlytrained.org ; https://ed.newtonrex.com/blog/launching-fairly-trained
- **What it is:** Certifies generative models trained only on licensed, public-domain, or consented data (e.g., Beatoven, Soundful, Tuney, Kits.ai, LANDR, Endel, Lemonaide among early certified companies; Stable Audio Open's data would qualify).
- **Evidence:** Certification list; industry recognition.
- **Why it matters for the studio:** A concrete external standard the studio could meet for any released model.
- **Tags:** [ethics-legal]
- **Verification:** partial
- **BibKey:** newtonrex2024fairlytrained

### StatementAITraining — "Statement on AI training" (22 Oct 2024)
- **Who/where/when:** Organised by Ed Newton-Rex; launched with ~10,500 signatories (Björn Ulvaeus, Thom Yorke, Radiohead, The Cure, Kate Bush, Julianne Moore, Kazuo Ishiguro…), later >50,000.
- **Links:** https://ed.newtonrex.com/statement-on-ai-training
- **What it is:** One sentence: "The unlicensed use of creative works for training generative AI is a major, unjust threat to the livelihoods of the people behind those works, and must not be permitted."
- **Evidence:** Signatory count; used in UK Data (Use and Access) Bill lobbying (2025) alongside the silent album *Is This What We Want?* (Feb 2025).
- **Why it matters for the studio:** Signals where much of the creative community stands; a consent-based studio can credibly align with it.
- **Tags:** [ethics-legal]
- **Verification:** partial
- **BibKey:** newtonrex2024statement

### Spawning — Spawning / "Have I Been Trained?" (Holly Herndon & Mat Dryhurst)
- **Who/where/when:** Spawning AI (Herndon, Dryhurst, Jordan Meyer), founded 2022; *Have I Been Trained?* search over LAION-5B (Sept 2022); *Do Not Train* registry / ai.txt (2023); Source.Plus PD/CC dataset platform (2024); Herndon & Dryhurst's *Holly+* vocal deepfake (2021) and *The Call* (2024, Serpentine) as consent-based training artworks.
- **Links:** https://spawning.ai ; https://haveibeentrained.com
- **What it is:** Opt-out infrastructure (registries honoured by Stability, Hugging Face) and an artistic practice of *consensual* dataset creation.
- **Evidence:** >1.5 billion opt-outs reported by 2024 (unverified figure).
- **Why it matters for the studio:** Model for consent-first data governance and for artists training on their *own* voices/material — matching the studio's ethos.
- **Tags:** [ethics-legal]
- **Verification:** partial
- **BibKey:** spawning2022haveibeentrained

### DeezerStats — Deezer AI-content statistics 2025–2026
- **Who/where/when:** Deezer newsroom: Jan 2025 ~10% of daily deliveries fully AI (~10k/day); Apr 2025 18% (20k/day); Sept 2025 28% (30k/day); **12 Nov 2025 34% (50k/day)**; **Apr 2026 44% (75k/day)**; **21 July 2026: >50% at peak in June 2026 (~90k/day)**; 13.4M AI tracks tagged in 2025.
- **Links:** https://newsroom-deezer.com/2026/07/ai-music-exceeds-50-percent-daily-uploads-deezer/ ; https://newsroom-deezer.com/2026/04/ai-generated-tracks-represent-44-of-new-uploaded-music/
- **What it is:** Deezer's proprietary detector (claimed 99.8% accuracy, <1 false positive per 10k) tags fully-AI albums, **labels them to listeners (since June 2026)**, excludes them from algorithmic/editorial recommendation, and removes fraudulent/idle AI tracks. AI tracks draw only 1–3% of streams; **~85% of their streams are fraudulent**.
- **Evidence:** Platform telemetry (self-reported).
- **Why it matters for the studio:** Quantifies the flood the studio positions against, and shows that *disclosure + demotion* is now normal — human-authored provenance is an asset.
- **Tags:** [ethics-legal] [product]
- **Verification:** verified
- **BibKey:** deezer2026aistats

### SpotifyPolicy — Spotify AI policies (25 Sept 2025)
- **Who/where/when:** Spotify (Sam Duboff, Charlie Hellman), 25 Sept 2025.
- **Links:** https://www.musicbusinessworldwide.com/spotify-has-deleted-75m-spammy-tracks-as-it-unveils-new-ai-music-policies/
- **What it is:** (1) **Impersonation policy** — unauthorised AI voice clones removable; (2) **spam filter** against mass uploads, duplicates, SEO tricks, <30-s bait tracks (75M "spammy" tracks removed in the prior 12 months); (3) support for the **DDEX AI-disclosure metadata standard** so labels/distributors credit AI's role in vocals, instrumentation or production. Endorsed by UMG and WMG.
- **Evidence:** Policy statement.
- **Why it matters for the studio:** DDEX AI credits are a concrete metadata target for the studio's export ("human-composed; AI-assisted arrangement/rendering").
- **Tags:** [ethics-legal] [product]
- **Verification:** verified
- **BibKey:** spotify2025aipolicy

### SmithFraud — United States v. Michael Smith (S.D.N.Y.): AI-generated streaming fraud
- **Who/where/when:** Indicted 4 Sept 2024 (wire fraud, money laundering; ~$10M alleged, 2017–2024); **pleaded guilty 19 Mar 2026** to conspiracy to commit wire fraud ($8.09M); sentencing set 29 July 2026 (outcome not verified).
- **Links:** https://www.aimusicpreneur.com/ai-music-news/michael-smith-ai-streaming-fraud-guilty-plea-2026/
- **What it is:** Hundreds of thousands of AI-generated tracks (many sourced at up to 10k songs/month; hundreds credited to Boomy's CEO as co-writer) streamed by ~1,040 bot accounts (~661k fake streams/day) across Spotify, Apple, Amazon, YouTube; detected by the Mechanical Licensing Collective in 2023, not by the DSPs.
- **Evidence:** First U.S. criminal case of AI-music streaming fraud.
- **Why it matters for the studio:** Illustrates the misuse mode of one-shot mass generation; a composer-centric studio has no comparable attack surface.
- **Tags:** [ethics-legal]
- **Verification:** verified
- **BibKey:** usdoj2024smith

### GEMASACEM — GEMA/SACEM × Goldmedia study *AI and Music* (30 Jan 2024)
- **Who/where/when:** Goldmedia GmbH for GEMA and SACEM; published Jan 2024; survey of ~15,000 members.
- **Links:** https://www.gema.de/en/news/ai-study ; https://www.goldmedia.com/fileadmin/goldmedia/Studie/2023/GEMA-SACEM_AI-and-Music/AI_and_Music_GEMA_SACEM_Goldmedia.pdf
- **What it is:** Forecasts the generative-AI music market at ~$3bn by 2028 and **27% of creators' revenues at risk by 2028**; 35% of members already use AI; 71% see risks > opportunities; 95% want disclosure of training data; GEMA later proposed a two-pillar licensing model for AI (Sept 2024).
- **Evidence:** Member survey + market model.
- **Why it matters for the studio:** Establishes the economic framing collecting societies use; the studio's positioning (assist human members) is compatible with GEMA's stance.
- **Tags:** [ethics-legal]
- **Verification:** partial
- **BibKey:** goldmedia2024gemasacem

### CISACStudy — CISAC/PMP Strategy global economic study (4 Dec 2024)
- **Who/where/when:** CISAC with PMP Strategy; Dec 2024.
- **Links:** https://www.cisac.org/services/reports-and-research/cisacpmp-strategy-ai-study
- **What it is:** Gen-AI music+audiovisual outputs market to reach ~€64bn by 2028 (music ~€16bn/yr); music creators risk losing **24% of revenues by 2028** (cumulative ~€10bn) via substitution and unlicensed training; calls for licensing and transparency.
- **Evidence:** Economic modelling.
- **Why it matters for the studio:** Same as above; global scope.
- **Tags:** [ethics-legal]
- **Verification:** partial
- **BibKey:** cisac2024pmp

### APRAAMCOS — APRA AMCOS *AI and Music* report (19 Aug 2024)
- **Who/where/when:** APRA AMCOS (Australia/NZ) with Goldmedia; survey of 4,200+ members, May–June 2024.
- **Links:** https://www.apraamcos.com.au/about-us/news-and-events/ai-in-music-report
- **What it is:** 38% already use AI; **54% agree AI can assist the creative process**; 82% fear for their livelihood; 65% risks > opportunities; 83% worry about discoverability; 97% want policy action and training-data disclosure; 95% demand permission before use; 23% of revenue at risk by 2028 (AUD 519M cumulative); 89% of Aboriginal & Torres Strait Islander creators fear cultural appropriation. (Ivors Academy/UK Musicians' Union surveys 2024–25 report similar ~⅔ concern levels — partial.)
- **Evidence:** Largest member survey of its kind.
- **Why it matters for the studio:** Quantifies the demand for *assistive* AI with consent — the studio's target segment.
- **Tags:** [ethics-legal] [HCI-study]
- **Verification:** verified
- **BibKey:** apraamcos2024ai

### PDMX — PDMX: A Large-Scale Public Domain MusicXML Dataset for Symbolic Music Processing
- **Who/where/when:** Phillip Long, Zachary Novack, Taylor Berg-Kirkpatrick, Julian McAuley; UC San Diego; ICASSP 2025 (arXiv Sept 2024).
- **Links:** https://arxiv.org/abs/2409.10831 ; https://github.com/pnlong/PDMX
- **What it is:** >250,000 public-domain MusicXML scores scraped from MuseScore.com with ratings/tags metadata; released CC BY 4.0; shows user ratings filter quality for multitrack generation training.
- **Evidence:** Generation experiments on rating-filtered subsets.
- **Why it matters for the studio:** The largest copyright-clean **notation** corpus — the default training/eval set for a symbolic-first studio (cross-ref datasets cluster).
- **Tags:** [dataset] [notation] [ethics-legal] [symbolic-generation]
- **Verification:** verified
- **BibKey:** long2024pdmx

### AriaMIDI — Aria-MIDI: A Dataset of Piano MIDI Files for Symbolic Music Modeling
- **Who/where/when:** Louis Bradshaw & Simon Colton; Queen Mary University of London; ICLR 2025 (arXiv 2504.15071).
- **Links:** https://arxiv.org/abs/2504.15071 ; https://github.com/loubbrad/aria-midi
- **What it is:** >1M MIDI files (~100k hours) transcribed from crawled piano recordings via LM-scored metadata crawling, audio classification/segmentation and a piano transcription model; released with metadata tags (licence: research; underlying recordings not PD — provenance caveat).
- **Evidence:** Statistical analyses; used to pretrain Aria models.
- **Why it matters for the studio:** Huge symbolic performance corpus for expressive rendering, but transcribed-from-audio provenance is legally greyer than PDMX — document the trade-off.
- **Tags:** [dataset] [symbolic-generation] [expression-performance] [ethics-legal]
- **Verification:** partial
- **BibKey:** bradshaw2025ariamidi

### ConcordAnthropic — Concord Music Group et al. v. Anthropic (lyrics)
- **Who/where/when:** Filed Oct 2023 (M.D. Tenn., transferred to N.D. Cal.); Jan 2025 stipulation on output guardrails; ongoing 2026 (partial). Related: *Bartz v. Anthropic* (books) June 2025 fair-use ruling and $1.5bn settlement Sept 2025 — training on lawfully acquired books held fair use, pirated copies not.
- **Links:** https://www.courtlistener.com/?q=Concord+Music+Group+v.+Anthropic
- **What it is:** Music publishers allege Claude reproduced lyrics; case tests output-side infringement and guardrails for LLMs, complementing the German GEMA rulings.
- **Evidence:** Pending.
- **Why it matters for the studio:** Lyrics handling in any LLM component should include guardrails against reproducing protected lyrics.
- **Tags:** [ethics-legal] [LLM-agent]
- **Verification:** partial/unverified (2026 status)
- **BibKey:** concord2023anthropic

### EthicalFooting — Why a symbolic-first, human-authored studio has a different ethical footing (synthesis note)
- **Who/where/when:** Synthesis of the above (this document).
- **Links:** —
- **What it is:** (1) **Authorship/copyrightability:** outputs are notation the composer wrote, selected, arranged and edited → protectable under USCO Part 2 / Thaler line; text-to-song outputs largely are not. (2) **Training data:** symbolic corpora with clean provenance exist (PDMX, JSB, Nottingham, TheoryTab-style consented analyses, the composer's own works), whereas SOTA audio models are trained on commercial recordings now judged infringing in Germany. (3) **Memorisation:** symbolic models trained on PD data cannot reproduce protected recordings; style learned from *the user's own* sketches (OMax/Continuator lineage) sidesteps the pastiche problem. (4) **Voice/likeness:** render vocals via consented singing synthesis (SynthV/ACE/Kits) or none — ELVIS Act compliant. (5) **Disclosure:** emit DDEX AI credits / provenance logs by default. (6) **Market substitution:** the studio increases human output rather than substituting for it, aligning with GEMA/CISAC/APRA member preferences (54% want assistive AI). Residual risks: style imitation of living composers, use of transcribed-from-audio corpora (Aria-MIDI), and any bundled audio renderer's training data.
- **Evidence:** See cited entries.
- **Why it matters for the studio:** This is the ethics section of the manifesto/literature review.
- **Tags:** [ethics-legal] [notation] [symbolic-generation]
- **Verification:** synthesis
- **BibKey:** (none)
