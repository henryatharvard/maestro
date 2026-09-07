# 06 — Multimodal input, annotation paradigms, version control, and the "music as code / compile" lineage

## Overview

This cluster covers *how a composer gets ideas into the machine and marks them up*, and *how the machine's job can be framed as compilation*. Seven sub-areas: (A) voice/humming as input — a 30-year lineage from query-by-humming (Ghias 1995) through modern neural transcription (Onsets & Frames, MT3, Basic Pitch, Sheet Sage), humming datasets (HumTrans), vocal-to-accompaniment (SingSong) and real-time voice→MIDI products (Dubler); (B) pen/sketch input — from Xenakis's UPIC (1977) and Hyperscore (2004) to the Paris-Saclay pen+touch notation work (Cavez et al., CHI 2024/2025), contour-to-melody models (SketchNet, MIDI-Draw, Drawlody), and OMR/handwriting recognition (StaffPad, Sheet Music Transformer); (C) image/video→music conditioning (Vis2Mus, MeLFusion, Amuse, V2Meow, VidMuse, MuMu-LLaMA, MuVi); (D) annotation tools and encodings — Sonic Visualiser, Dezrann, MEI/Verovio/mei-friend, MusicXML 4.0 and the still-unfinished MNX, ABC, Humdrum, web renderers, rehearsal-annotation apps, and theorist annotation standards (RomanText, DCML); (E) editing paradigms from adjacent fields — direct manipulation vs. conversation (Shneiderman, DirectGPT), instruction-based editing (InstructPix2Pix, ExpressEdit), sketch interfaces (Teddy), programming-by-demonstration, live/projectional/structured editing (Tanimoto, Hazel, MPS); (F) versioning, diffing and history for music (Foscarin's score diff, Flat.io history, Chronicle, Luminate-style variation exploration); (G) music-as-code — score compilers (LilyPond, ABC), audio languages (Csound, SuperCollider, Max/Pd, ChucK, Faust), live coding (Tidal, Strudel, Sonic Pi, Gibber), CAC environments (OpenMusic, bach, Euterpea, Alda, music21), scholarship (Nierhaus, Dannenberg, Magnusson), and the 2024–2026 wave of LLMs that write ABC/code as an intermediate representation (ChatMusician, MIDI-LLM, Libretto). The recurring interaction pattern across all of them is *coarse human gesture → system inference → visible, editable symbolic result → human correction*, which is exactly the studio's compose→annotate→compile→edit loop.

## Key takeaways for the studio

1. **Every successful "loose" input modality lands in a symbolic, editable representation.** Humming → MIDI/lead sheet (Basic Pitch, Sheet Sage, Sing2Notes), drawing → notes (Hyperscore, Drawlody, StaffPad), image → chords (Amuse). Systems that skip the symbolic layer (SingSong, V2Meow, VidMuse, MeLFusion emit audio only) are impressive but offer no correction handle; the studio should route every modality into notation/MIDI first and render audio second.
2. **Humming transcription is still hard and needs a correction UI.** Even on a clean, in-tune dataset (HumTrans), off-the-shelf vocal transcribers reached ~6–7% note F1; a purpose-built CNN+DP model reaches ~0.67 F1. Design for *interactive* disambiguation (key/scale lock, quantisation grid, "stickiness" smoothing as in Dubler, click-to-fix as in Sing2Notes Edit Mode) rather than assuming correct transcription.
3. **Pen input's value is *relaxing* the notation editor's constraints, not just handwriting recognition.** Cavez et al.'s interviews (9 professional composers) show structured notation editors block ideation; EuterPen lets composers write digital ink, pictures and audio samples *on and between staves* without the engraver enforcing syntax. This is the closest existing model for the studio's "scribble on the score as an annotation" step.
4. **Contour sketches are a natural control signal for melody generation** (SketchNet: pitch and rhythm sketched independently; MIDI-Draw / Drawlody: drawn curve → melody with visual alignment explanation). Drawlody's 4.38/5 usability vs 2.4–2.9 for chord/DAW interfaces argues for a drawn-contour annotation type.
5. **Image/video conditioning works best as *inspiration → keywords → symbolic proposal*, with the user in the middle.** Amuse (CHI 2025) turns images/audio/text into chord progressions via an LLM plus rejection sampling against a real-music chord model; users rated it significantly better on inspiration transfer and controllability. End-to-end image→audio (Art2Mus) was *not* preferred over text-only baselines. Mood-board input should propose editable material, not finished audio.
6. **There is a rich, standardised vocabulary for machine-readable score annotation already**: MEI editorial markup, Dezrann's `.dez` JSON labels anchored to musical time (measure+beat), DCML harmony labels typed as text into MuseScore, RomanText off-score analyses, Web Annotations in mei-friend. The studio's "annotation layer" should reuse one of these (musical-time anchored, staff-scoped, typed, with free-text comment) rather than inventing a format.
7. **"Annotations as prompts" is an open gap.** No fetched work treats human margin notes on a score as instructions to a generator; the nearest are Libretto (2026: LLM agent revises music in a text grammar under musician-readable structural feedback) and instruction-editing paradigms from vision (InstructPix2Pix, ExpressEdit). This is the studio's most defensible research contribution.
8. **Direct manipulation and conversation are complementary, not rivals.** DirectGPT (CHI 2024): turning selections and drags into engineered prompts made LLM editing 50% faster with 72% shorter prompts. ExpressEdit (IUI 2024): NL + sketch on frames for video edits. The studio's edit step should let the composer *select* a region on the score and *then* type/hum/draw the instruction.
9. **"Compile" has real precedents.** LilyPond compiles text to engraved PDF; ABC→abc2midi; Faust compiles DSP to C++/WASM; Hazel evaluates programs *around* typed holes (a model for compiling an incomplete score with `[fill]` regions); projectional editors (MPS) edit the AST directly with multiple notations — a model for editing one musical model through score, piano-roll and text views simultaneously.
10. **Versioning for music is thin.** Flat.io keeps per-edit history with per-contributor colouring; Foscarin et al. (2019) give a tree-edit-distance diff over scores rendered side-by-side in Verovio; mei-friend commits MEI to GitHub. Nothing offers branch/merge with musical semantics; a variation tree (Luminate-style) over compiled outputs is unexplored for music.
11. **LLM-as-code-writer is now the mainstream route to symbolic generation** (ChatMusician: ABC as "a second language"; MIDI-LLM: MIDI tokens added to Llama vocabulary; NotaGen: ABC; Libretto: custom text grammar with explicit onset slots). Choosing a textual IR that is *both* LLM-friendly and losslessly convertible to MusicXML/MEI (ABC, **kern, or a custom grammar) is a first-order architectural decision.

---

## A. Humming / singing / voice as input

### QBH-1995 — Query By Humming: Musical Information Retrieval in an Audio Database
- **Who/where/when:** Asif Ghias, Jonathan Logan, David Chamberlin, Brian C. Smith; Cornell University; ACM Multimedia '95, 1995
- **Links:** https://www.cs.cornell.edu/zeno/papers/humming/humming.html ; https://dl.acm.org/doi/10.1145/217279.215273
- **What it is:** The founding query-by-humming paper. User hums into a microphone; autocorrelation pitch tracking converts the hum into a 3-symbol contour string (U/D/S = up/down/same relative to previous note); approximate string matching (error-tolerant) against contour strings derived from a MIDI database (183 songs). Interaction: hum → ranked song list; errors handled by tolerance in the matcher, not by user correction.
- **Evidence:** 10–12 pitch transitions sufficed to discriminate 90% of the 183 songs; search < 4 s per 100 songs on a Sparc 2; pitch tracking took 20–45 s.
- **Why it matters for the studio:** Establishes the design principle that hummed input should be reduced to a *robust, coarse representation* (contour) before matching/generation, since exact pitch from voice is unreliable. Useful as a fallback for "find the motif I hummed earlier" inside a project.
- **Tags:** [humming] [transcription] [history] [multimodal-input]
- **Verification:** verified (fetched primary source)
- **BibKey:** ghias1995qbh

### HumToSearch — The Machine Learning Behind Hum to Search (Google)
- **Who/where/when:** Christian Frank (with Alex Tudor, Duc Dung Nguyen, Matej Kastelic, Mihajlo Velimirović, et al.); Google Research Zürich; Google AI Blog, 12 Nov 2020 (product launch Oct 2020)
- **Links:** https://research.google/blog/the-machine-learning-behind-hum-to-search/
- **What it is:** Production humming search in the Google app: user taps mic → "search a song" → hums/sings/whistles 10–15 s. A neural network embeds the hum spectrogram so that it lands near embeddings of the *original studio recordings* (>500k songs) — no intermediate MIDI. Training data scarcity was solved by synthesising hummed versions from recordings via SPICE pitch extraction, later a neural hum-like generator; triplet loss plus confidence-based loss. Output: ranked candidate songs; no user correction beyond re-humming.
- **Evidence:** Blog reports qualitative accuracy gains from the synthetic-hum augmentation and confidence loss; no public metrics.
- **Why it matters for the studio:** Shows that *embedding-based* matching of hums against audio is production-viable, useful for "which of my sketches/reference tracks is this?" retrieval inside a project; also a cautionary example of an opaque pipeline with no editable intermediate.
- **Tags:** [humming] [product] [multimodal-input]
- **Verification:** verified (fetched primary source)
- **BibKey:** frank2020humtosearch

### OnsetsFrames — Onsets and Frames: Dual-Objective Piano Transcription
- **Who/where/when:** Curtis Hawthorne, Erich Elsen, Jialin Song, Adam Roberts, Ian Simon, Colin Raffel, Jesse Engel, Sageev Oore, Douglas Eck; Google Brain (Magenta); ISMIR 2018 (arXiv Oct 2017)
- **Links:** https://arxiv.org/abs/1710.11153 ; https://magenta.withgoogle.com/onsets-frames
- **What it is:** CNN+BiLSTM that jointly predicts note onsets and frame-wise pitch activity; onset predictions gate frame predictions so notes cannot start without a detected attack. Also predicts velocity. Input: piano audio; output: MIDI notes with onsets/offsets/velocity. No user control; correction happens downstream in a DAW/notation editor.
- **Evidence:** >100% relative improvement in note-with-offset F1 over prior state of the art on MAPS.
- **Why it matters for the studio:** The architectural template (onset + frame heads) underlies Basic Pitch and many hum transcribers; the studio's "play or sing it in" path inherits its failure modes (offsets, repeated notes).
- **Tags:** [transcription] [audio-generation] [toolkit]
- **Verification:** verified (fetched primary source)
- **BibKey:** hawthorne2018onsets

### MT3 — MT3: Multi-Task Multitrack Music Transcription
- **Who/where/when:** Josh Gardner, Ian Simon, Ethan Manilow, Curtis Hawthorne, Jesse Engel; Google Magenta / U. Washington; ICLR 2022 (arXiv Nov 2021)
- **Links:** https://arxiv.org/abs/2111.03017 ; code: https://github.com/magenta/mt3
- **What it is:** A T5-style encoder-decoder Transformer that maps spectrogram frames to a MIDI-like token vocabulary with instrument program tokens, trained jointly on several AMT datasets (MAESTRO, Slakh, Cerberus4, GuitarSet, MusicNet, URMP). Input: mixed polyphonic audio; output: multi-instrument note events. Human control: none at inference; errors corrected after the fact in MIDI.
- **Evidence:** Unified training substantially improves low-resource instruments (e.g., guitar) while matching piano SOTA; established a multi-task AMT benchmark suite.
- **Why it matters for the studio:** The reference approach for "drop in an example recording and get a multitrack MIDI sketch" — the studio's *example-audio-as-annotation* path. Token-based output is also LLM-compatible.
- **Tags:** [transcription] [multimodal-input] [toolkit]
- **Verification:** verified (fetched primary source)
- **BibKey:** gardner2022mt3

### BasicPitch — A Lightweight Instrument-Agnostic Model for Polyphonic Note Transcription and Multipitch Estimation
- **Who/where/when:** Rachel M. Bittner, Juan José Bosch, David Rubinstein, Gabriel Meseguer-Brocal, Sebastian Ewert; Spotify Audio Intelligence Lab; ICASSP 2022
- **Links:** https://github.com/spotify/basic-pitch ; demo https://basicpitch.io ; TS port https://github.com/spotify/basic-pitch-ts
- **What it is:** Very small CNN (harmonic CQT input) predicting onsets, notes and multipitch, instrument-agnostic, outputting MIDI *with pitch bends*. Input: any audio (mp3/wav/flac…), resampled to 22.05 kHz; outputs MIDI, note CSV, raw NPZ. Python and TypeScript (runs in-browser). Apache-2.0. The user chooses thresholds (onset/frame) and minimum note length via CLI/web sliders, which is the main error-correction knob.
- **Evidence:** Paper reports competitive note F1 with far fewer parameters than Onsets-and-Frames-class models; best on single-instrument recordings.
- **Why it matters for the studio:** The pragmatic default for hum/voice→MIDI in a browser-based studio (permissive licence, JS port, pitch-bend capture preserves expressive intent of a sung line).
- **Tags:** [transcription] [humming] [toolkit] [DAW-plugin]
- **Verification:** verified (fetched primary source)
- **BibKey:** bittner2022basicpitch

### SheetSage — Melody Transcription via Generative Pre-training
- **Who/where/when:** Chris Donahue, John Thickstun, Percy Liang; Stanford; ISMIR 2022 (Sheet Sage system: ISMIR 2021 LBD)
- **Links:** https://arxiv.org/abs/2212.01884 ; https://github.com/chrisdonahue/sheetsage ; https://chrisdonahue.com/sheetsage/
- **What it is:** Uses Jukebox's pretrained audio representations as features for a melody transcriber; a new 50-hour crowd-sourced melody dataset over broad-genre music. Sheet Sage composes melody transcription with beat tracking, key and chord estimation to output a *lead sheet* (melody + chords) from arbitrary audio. Input: audio file/URL; output: LilyPond/MusicXML-style lead sheet. No interactive correction inside the tool.
- **Evidence:** 20% relative improvement from Jukebox features vs spectrograms; 77% stronger than the best prior melody-transcription baseline.
- **Why it matters for the studio:** Directly matches the studio's symbolic-first, lead-sheet-centric representation: "insert example audio → get a lead sheet you can edit." Also demonstrates the value of generative-model features for transcription.
- **Tags:** [transcription] [notation] [symbolic-generation] [multimodal-input]
- **Verification:** verified (fetched primary source)
- **BibKey:** donahue2022sheetsage

### SingSong — SingSong: Generating Musical Accompaniments from Singing
- **Who/where/when:** Chris Donahue, Antoine Caillon, Adam Roberts, Ethan Manilow, Philippe Esling, Andrea Agostinelli, Mauro Verzetti, Ian Simon, Olivier Pietquin, Neil Zeghidour, Jesse Engel; Google Research; arXiv Jan 2023
- **Links:** https://arxiv.org/abs/2301.12662 ; https://chrisdonahue.com/publication/23-01-singsong/
- **What it is:** Vocal audio → instrumental accompaniment audio. Source separation applied to a large music corpus yields (vocal, instrumental) pairs; AudioLM is adapted for conditional generation. User sings/hums; system returns a full-band backing track. No symbolic intermediate; the only control is the input vocal itself (re-sing to change).
- **Evidence:** Listener study: SingSong instrumentals significantly preferred over a retrieval baseline for the same vocals.
- **Why it matters for the studio:** The strongest demonstration that a hummed/sung line alone carries enough information to imply harmony, groove and style. For the studio this argues for a *symbolic* SingSong: sung melody → chords + arrangement in notation that the composer can then edit.
- **Tags:** [humming] [accompaniment] [audio-generation] [multimodal-input]
- **Verification:** verified (fetched primary source)
- **BibKey:** donahue2023singsong

### HumTrans — HumTrans: A Novel Open-Source Dataset for Humming Melody Transcription and Beyond
- **Who/where/when:** Shansong Liu, Xu Li, Dian Li, Ying Shan; ARC Lab, Tencent PCG; arXiv Sept/Oct 2023 (also ICASSP 2024)
- **Links:** https://arxiv.org/abs/2309.09623 ; https://github.com/shansongliu/HumTrans
- **What it is:** 56.22 h of humming: 500 compositions split into 1,000 segments, each hummed twice by 10 music-trained students via a web interface with a reference melody, so ground truth is known. Baseline evaluation of four vocal-transcription models.
- **Evidence:** Best baseline (JDC-STP) only ~6.8% note F1 (validation) / 5.7% (test) — humming is far harder than sung lyrics for existing models.
- **Why it matters for the studio:** Quantifies how bad "just transcribe the hum" is out of the box and provides the training/eval set for a studio-specific hum model; also supports the design decision to always show the transcription for confirmation.
- **Tags:** [humming] [dataset] [transcription] [evaluation]
- **Verification:** verified (fetched primary source)
- **BibKey:** liu2023humtrans

### DynHumTrans — Dynamic HumTrans: Humming Transcription Using CNNs and Dynamic Programming
- **Who/where/when:** Shubham Gupta, Isaac Neri Gomez-Sarmiento, Faez Amjed Mezdari, Mirco Ravanelli, Cem Subakan; Mila / Université Laval / Concordia; arXiv Oct 2024 (Springer LNCS chapter 2024/25)
- **Links:** https://arxiv.org/abs/2410.05455 ; https://github.com/shubham-gupta-30/humming_transcription
- **What it is:** CNN frame classifier + dynamic-programming decoding for hum → notes; the authors also *correct* HumTrans's onset/offset ground truth and release fixed annotations.
- **Evidence:** Octave-invariant note+onset F1 0.673 vs 0.564 for the next-best method; similar accuracy octave-aware.
- **Why it matters for the studio:** Current best open baseline for the hum-to-MIDI step; DP decoding with musical constraints (scale, tempo grid) is the natural place to inject the composer's annotations (key, meter) as priors.
- **Tags:** [humming] [transcription]
- **Verification:** verified (fetched primary source)
- **BibKey:** gupta2024dynhumtrans

### VocalSketch — VocalSketch: Vocally Imitating Audio Concepts
- **Who/where/when:** Mark Cartwright, Bryan Pardo; Northwestern University; CHI 2015
- **Links:** https://interactiveaudiolab.github.io/assets/papers/cartwright_pardo_chi2015.pdf ; data https://github.com/interactiveaudiolab/VocalSketchDataSet
- **What it is:** Crowd-sourced dataset of 4,429 vocal imitations (from 10,750 recordings, 248 contributors) of everyday sounds, instruments, synthesizer patches; plus a recognition study. Establishes "vocal sketching" of *timbre* (not melody) as an input modality for sound search/design.
- **Evidence:** Forced-choice identification accuracy 0.80 for everyday sounds, 0.45 instruments, 0.42 commercial synths, 0.54 single synth sounds (chance 0.1); free-response 0.23–0.27.
- **Why it matters for the studio:** Beyond melody, composers can *vocalise* a desired sound ("this pad should go 'shhwaaa'"); the numbers show that works for timbrally distinctive targets and needs disambiguation for instruments — argues for showing top-k candidate sounds to pick from.
- **Tags:** [humming] [dataset] [HCI-study] [multimodal-input]
- **Verification:** verified (fetched primary source)
- **BibKey:** cartwright2015vocalsketch

### Dubler — Vochlea Dubler 2 (and Jam Origin MIDI Guitar) — real-time voice/instrument → MIDI controllers
- **Who/where/when:** Vochlea Music (London), Dubler 2 released 2021; Jam Origin (Denmark), MIDI Guitar 2 (2016–) / MIDI Guitar 3 open beta (jam.live)
- **Links:** https://vochlea.com/products/dubler2 ; review https://www.soundonsound.com/reviews/vochlea-dubler-2 ; https://www.jamorigin.com/
- **What it is:** Dubler 2 converts singing/humming/beatboxing to MIDI in real time: pitch → notes (with a visual "note wheel" and key/scale restriction), vowels (aaa/ooo/eee) → CC, up to 12 recorded examples per beatbox sound train drum triggers. Error handling: a "Stickiness" slider smooths note transitions; scale lock; users adapt technique. £189 (software) / £249 with mic. MIDI Guitar is the analogous polyphonic guitar→MIDI plugin (standalone/VST/AU/iOS).
- **Evidence:** Sound On Sound (Nov 2021) reports low latency for triggers, slightly more for pitch; no published accuracy study.
- **Why it matters for the studio:** Shows the *interaction design* of hum-to-MIDI that works for musicians: constrain (scale lock), smooth (stickiness), visualise (note wheel), and let users train per-user sounds. Directly reusable patterns for the studio's live hum-in step.
- **Tags:** [humming] [product] [real-time] [DAW-plugin]
- **Verification:** verified (product pages + review fetched)
- **BibKey:** vochlea2021dubler

### Sing2Notes — ScoreCloud (Doremir) and Sing2Notes (Klangio): sing → notation products
- **Who/where/when:** Doremir Music Research AB (Stockholm; Sven Ahlbäck, Sven Emtell); ScoreCleaner 2011 → ScoreCloud 2014–. Klangio GmbH (Karlsruhe); Sing2Notes app 2021–.
- **Links:** https://scorecloud.com/ ; https://klang.io/sing2notes/
- **What it is:** Consumer tools that transcribe singing/playing directly to sheet music. ScoreCloud (desktop Studio + mobile Express) transcribes audio or MIDI into notation with polyphonic analysis; MusicXML/MIDI export in paid tiers. Sing2Notes: record, upload or paste a YouTube link → sheet music in seconds, exported as PDF/MIDI (quantised and unquantised)/MusicXML; an **Edit Mode** lets users fix notes in-app; free tier = first 20 s.
- **Evidence:** No published accuracy figures; Klangio claims >4M transcriptions.
- **Why it matters for the studio:** The commercial baseline for "hum → notation → fix by hand". Their UX (quantised vs unquantised export, in-app edit mode) is the minimum the studio must match.
- **Tags:** [humming] [transcription] [notation] [product]
- **Verification:** verified (product pages fetched; ScoreCloud history via Wikipedia)
- **BibKey:** doremir2014scorecloud

### DAWZY — DAWZY: A New Addition to AI-powered "Human in the Loop" Music Co-creation
- **Who/where/when:** Aaron C. Elkins, Sawyer Blankenship, Sanchit Singh, Uyiosa Philip Amadasun, Adrian Kieback, Aman Chadha; San Diego State University; arXiv Dec 2025
- **Links:** https://arxiv.org/abs/2512.03289
- **What it is:** Open-source voice-first assistant for REAPER. Natural-language requests (text, voice, or hum) are converted by an LLM into *reversible* DAW actions: three MCP tools (state query, parameter adjustment, beat generation), atomic scripts with undo. A minimal chat box replaces menu navigation; the DAW remains the workspace.
- **Evidence:** N=21 user study; MOS (1–5): enjoyment 4.48, learning 4.38, collaboration 4.29, usability 4.14, control 3.81.
- **Why it matters for the studio:** A concrete "voice-controlled DAW" reference with the right architecture for the studio's edit step — LLM emits *reversible code* against the host application's API (a compile-to-actions pattern), and control was the lowest-rated dimension, flagging the need for direct-manipulation fallbacks.
- **Tags:** [LLM-agent] [DAW-plugin] [HCI-study] [multimodal-input] [music-as-code]
- **Verification:** verified (fetched primary source)
- **BibKey:** elkins2025dawzy

---

## B. Sketch / pen / scribble as input

### UPIC — UPIC (Xenakis, CEMAMu, 1977) and IanniX (open-source graphical sequencer)
- **Who/where/when:** Iannis Xenakis with engineer Patrick Saint-Jean; CEMAMu, Paris; first prototype 1977, real-time version 1987. IanniX: IanniX Association (Thierry Coduys et al.), 2000s–present; Scordato, eContact! 19.3 (2017) "From UPIC to IanniX".
- **Links:** https://www.iannis-xenakis.org/en/dictionary-upic/ ; https://www.iannix.org/en/whatisiannix/ ; https://github.com/buzzinglight/IanniX ; https://econtact.ca/19_3/scordato_iannix.html
- **What it is:** UPIC: composer draws arcs on a CAD-style tablet (x = time, y = pitch) and also *draws* waveforms and envelopes; a wavetable synthesiser plays the page; the same drawing can act as waveform or control signal at different time scales. First all-computer piece: *Mycènes Alpha* (1978). IanniX (GPL-3) generalises this: triggers, curves and cursors in a 2D/3D scene emit OSC/MIDI to any environment; scriptable in JavaScript.
- **Evidence:** Historical; no user studies. Les Ateliers UPIC (1986) → CCMIX pedagogical use until 2007.
- **Why it matters for the studio:** The origin of "drawing is a score"; also a warning — UPIC drawings map to *sound* not to notation, so the compiler must decide what a scribble *means* (pitch contour? dynamics? density?). IanniX's separation of drawn geometry from the sound engine is a clean model for a sketch layer that emits control data.
- **Tags:** [sketch] [history] [music-as-code] [toolkit]
- **Verification:** verified (fetched primary sources; Scordato article partial)
- **BibKey:** xenakis1977upic

### Hyperscore — Hyperscore: A Graphical Sketchpad for Novice Composers
- **Who/where/when:** Morwaread M. Farbood, Egon Pasztor (MIT Media Lab, Machover's Opera of the Future), Kevin Jennings (Trinity College Dublin); IEEE Computer Graphics & Applications 24(1), Jan/Feb 2004 (DOI 10.1109/MCG.2004.1255809)
- **Links:** https://dl.acm.org/doi/abs/10.1109/MCG.2004.1255809 ; PDF https://bpb-us-e1.wpmucdn.com/wp.nyu.edu/dist/f/11865/files/2020/08/MFarbood-IEEE2004.pdf
- **What it is:** Motive windows: click droplets on a two-octave pitch/time grid to make short motives, each assigned a colour. Sketch window: draw coloured strokes; each stroke instantiates the motive of that colour, stroke length = repetitions, stroke shape = transposition contour; strokes are physically simulated curves you can grab and pull. A central **harmony line** controls tension/resolution: flat = stable, upward red = tension, spikes = modulation; the system re-harmonises motives to fit. Instrument choice changes stroke texture. Errors are corrected by re-drawing or dragging strokes; the system continuously re-renders and plays.
- **Evidence:** Toy Symphony workshops in Dublin, Glasgow, Berlin, Boston, New York (7–12 children each, five sessions); nearly all children completed a string-orchestra piece; observed visual-pattern vs aural strategies.
- **Why it matters for the studio:** The canonical *sketch → compile* system: freehand strokes plus a harmony-tension line are compiled into orchestral notation. Its harmony line is a direct ancestor of "annotate the desired tension curve and let the AI harmonise."
- **Tags:** [sketch] [symbolic-generation] [creativity-support] [education] [history]
- **Verification:** verified (fetched primary source)
- **BibKey:** farbood2004hyperscore

### CoughlanJohnson — Interaction in Creative Tasks: Ideation, Representation and Evaluation in Composition
- **Who/where/when:** Tim Coughlan, Peter Johnson; University of Bath; CHI 2006
- **Links:** https://oro.open.ac.uk/43523 (CHI 2006 proceedings version via ACM DL)
- **What it is:** Observational study of composers (individual and collaborating) analysing how ideas are represented and evaluated; proposes cycles of ideation and evaluation as atomic units of creative interaction, catalogues representation types used in composition, and prototypes a "Sonic Sketchpad" for musical idea representation.
- **Evidence:** Qualitative observations; number of composers not stated in abstract.
- **Why it matters for the studio:** Theoretical grounding for the compose→annotate→evaluate loop: representation (sketch/annotation) is the *central* activity, not a preliminary; tools should support incomplete, ambiguous representations.
- **Tags:** [HCI-study] [sketch] [creativity-support] [co-creation-framework]
- **Verification:** verified (fetched institutional repository abstract)
- **BibKey:** coughlan2006interaction

### PaperSubstrates — Interactive Paper Substrates to Support Musical Creation (and PaperComposer, InkSplorer)
- **Who/where/when:** Jérémie Garcia, Theophanis Tsandilas, Carlos Agon, Wendy E. Mackay; Inria / Université Paris-Sud / IRCAM; CHI 2012 (DOI 10.1145/2207676.2208316); PaperComposer at IHM 2014 (DOI 10.1145/2670444.2670450); InkSplorer at NIME 2011
- **Links:** https://dl.acm.org/doi/10.1145/2207676.2208316 ; https://hal.science/hal-00664334
- **What it is:** Anoto-pen "interactive paper" components that composers lay out themselves (staff, curve, keyboard, timeline substrates) and link to OpenMusic/Max; pen strokes on paper become data (e.g., drawn curves → parameters) while remaining sketchable paper. PaperComposer lets composers build their own paper interfaces. Grounded in field studies of contemporary composers' paper sketching practices.
- **Evidence:** Participatory design with professional composers (IRCAM); qualitative.
- **Why it matters for the studio:** Shows composers want *personalised* sketch substrates rather than one fixed sketch UI, and that pen curves are naturally understood as *control functions* (dynamics, density, tempo) — a template for typed annotation "lanes".
- **Tags:** [sketch] [HCI-study] [creativity-support] [music-as-code]
- **Verification:** partial (search-result metadata; full text not fetchable — ACM/HAL blocked)
- **BibKey:** garcia2012paper

### StaffPad — StaffPad (pen-based handwriting-to-notation, product)
- **Who/where/when:** David William Hearn; StaffPad Ltd; Windows/Surface 2015, iPad 2020; US$90
- **Links:** https://www.staffpad.net/ ; review https://www.scoringnotes.com/reviews/staffpad-for-ipad/
- **What it is:** Handwrite notes, rests, dynamics, articulations and slurs with a stylus on a staff; recognition runs *one measure at a time* when the pen moves to the next bar, replacing ink with engraved notation. Misrecognitions are fixed by re-writing or via a correction palette. Adds DAW-like automation lanes (expression, pan, volume), premium sample libraries, and **ScoreSync**/StaffPad Reader for pushing parts and *shared annotations* to players' iPads in rehearsal.
- **Evidence:** Review reports "generally strong" recognition with occasional misinterpretation; no published accuracy.
- **Why it matters for the studio:** The commercial proof that measure-granular, pen-first notation entry is usable by composers; its "ink → engraved, keep ink for annotations" duality and rehearsal-sync feature are directly relevant.
- **Tags:** [sketch] [notation] [product] [annotation]
- **Verification:** verified (product and review fetched)
- **BibKey:** hearn2015staffpad

### CavezCHI24 — Challenges of Music Score Writing and the Potentials of Interactive Surfaces
- **Who/where/when:** Vincent Cavez, Catherine Letondal, Emmanuel Pietriga, Caroline Appert; Université Paris-Saclay, CNRS, Inria (LISN/ILDA); CHI 2024 (DOI 10.1145/3613904.3642079)
- **Links:** https://dl.acm.org/doi/10.1145/3613904.3642079 ; https://inria.hal.science/hal-04497643
- **What it is:** Interviews with nine professional composers; analyses frictions in notation programs ("elaborate structured document editors" that enforce notation rules) through the Cognitive Dimensions of Notations framework; argues pen+touch surfaces can *temporarily break structure* to reconcile the need for engraving rigor with creative flexibility.
- **Evidence:** N=9 interviews; qualitative findings on premature commitment, viscosity, and reliance on paper alongside software.
- **Why it matters for the studio:** Empirical justification for the studio's premise that composers need a loosely-structured annotation/sketch layer *on top of* a strict symbolic model.
- **Tags:** [HCI-study] [notation] [sketch] [creativity-support]
- **Verification:** verified (abstract via Semantic Scholar API; author page)
- **BibKey:** cavez2024challenges

### EuterPen — EuterPen: Unleashing Creative Expression in Music Score Writing
- **Who/where/when:** Vincent Cavez, Catherine Letondal, Caroline Appert, Emmanuel Pietriga; Université Paris-Saclay / CNRS / Inria; CHI 2025 (DOI 10.1145/3706598.3713488)
- **Links:** https://dl.acm.org/doi/10.1145/3706598.3713488 ; PDF https://www.vincentcavez.com/euterPen.pdf
- **What it is:** A notation-program prototype that *selectively relaxes syntactic and structural constraints*: with pen and touch, composers input and move symbols with more freedom, and can "make space on, between and around staves to insert additional content such as digital ink, pictures and audio samples." Designed through prototyping phases, a participatory design workshop and interviews.
- **Evidence:** Feedback from participating professional composers described the approach as compelling and promising (qualitative).
- **Why it matters for the studio:** The closest existing realisation of the studio's "scribble on the score, paste an image or audio clip next to a passage" annotation model. Suggests annotations should live in a spatial layer *interleaved with* the score, not in a side panel.
- **Tags:** [sketch] [annotation] [notation] [multimodal-input] [HCI-study]
- **Verification:** verified (abstract via Semantic Scholar API; author page)
- **BibKey:** cavez2025euterpen

### Tactus — Opportunities to Support Musicians' Score-based Practice with Context-Specific Annotations on Tablet
- **Who/where/when:** Xintian Fu, Vincent Cavez; Université Paris-Saclay / CNRS / Inria and Stanford; CHI EA 2026 (DOI 10.1145/3772363.3798332)
- **Links:** https://dl.acm.org/doi/10.1145/3772363.3798332 ; PDF https://www.vincentcavez.com/pdf/Tactus.pdf
- **What it is:** Video analysis of 17 musicians' practice sessions plus 10 interviews; identifies *performance-oriented* (persistent: dynamics, bowings, breaths) vs *practice-oriented* (temporary: rhythm visualisations, accidentals, progress) annotations; proposes "context-specific annotations" that are dynamic — system feedback (performance analysis), feedforward (anticipating difficulty) and user-created dynamic marks — prototyped as the web app Tactus.
- **Evidence:** N=17 videos, 10 interviews, questionnaire evaluation of feature videos (Likert).
- **Why it matters for the studio:** Provides a taxonomy of annotation *lifetimes* (persistent vs ephemeral) and *authors* (human vs system) that the studio's annotation layer should encode explicitly.
- **Tags:** [annotation] [HCI-study] [notation]
- **Verification:** verified (fetched PDF)
- **BibKey:** fu2026tactus

### SketchNet — Music SketchNet: Controllable Music Generation via Factorized Representations of Pitch and Rhythm
- **Who/where/when:** Ke Chen, Cheng-i Wang, Taylor Berg-Kirkpatrick, Shlomo Dubnov; UC San Diego / Smule; ISMIR 2020
- **Links:** https://arxiv.org/abs/2008.01291 ; https://github.com/RetroCirce/Music-SketchNet
- **What it is:** "Sketch" = partial specification of a missing measure: the user supplies a pitch contour, a rhythm pattern, or both, and the model completes it. SketchVAE factorises pitch and rhythm; SketchInpainter predicts latent codes for missing bars from context; SketchConnector fuses user sketches with predictions. Monophonic folk melodies (Irish/Scottish, 4/4).
- **Evidence:** ~16k training / 2k test melodies; listening test with 106 subjects (318 responses); improved pitch/rhythm accuracy and subjective musicality over baselines.
- **Why it matters for the studio:** Formalises sketch-as-constraint infilling — exactly the "annotate this bar with a rough contour/rhythm and compile the notes" operation, with pitch and rhythm as *separately annotatable* lanes.
- **Tags:** [sketch] [infilling] [controllability] [symbolic-generation]
- **Verification:** verified (fetched primary source)
- **BibKey:** chen2020sketchnet

### MIDIDraw — MIDI-Draw: Sketching to Control Melody Generation
- **Who/where/when:** Tashi Namgyal, Raul Santos-Rodriguez, Peter Flach; University of Bristol; ISMIR 2022 Late-Breaking/Demo (arXiv May 2023)
- **Links:** https://arxiv.org/abs/2305.11605
- **What it is:** User draws a pitch contour on a canvas; a conditional VAE trained on synthetic melodies (contours parameterised by low-frequency cosine components) generates note sequences that lie on or scatter around the curve. Proof of concept; constant rhythm.
- **Evidence:** Preliminary user testing: non-musicians drew over-oscillating curves (need guidance); users wanted rhythm variation.
- **Why it matters for the studio:** Small but instructive: drawn contours need *smoothing/guidance affordances*, and rhythm must be a separate control — informs the design of a contour-annotation tool.
- **Tags:** [sketch] [controllability] [symbolic-generation]
- **Verification:** verified (fetched primary source)
- **BibKey:** namgyal2022mididraw

### Drawlody — Drawlody: Sketch-Based Melody Creation with Enhanced Usability and Interpretability
- **Who/where/when:** Qihao Liang, Ye Wang; National University of Singapore (SMC lab); IEEE Transactions on Multimedia, 2023/2024
- **Links:** https://smcnus.comp.nus.edu.sg/archive/pdf/2024/2024_Drawlody__IEEE_TMM_Finalised.pdf
- **What it is:** User draws a simplified melodic contour; a CNN-Transformer encoder-decoder maps it to a melody via a Generalised Melody Contour (GMC) representation and "FlexMIDI" (basic pitch trend + pitch "flex" around tonal centres); outputs MIDI/audio with adjustable tempo/duration and a *visual explanation* showing sketch–melody alignment.
- **Evidence:** 18 participants (6 trained); user-friendliness 4.38/5 vs 2.94 (chord-based) and 2.38 (DAW) interfaces; interpretability 4.50/5; beat rule-based and CNN baselines on musicality; still below expert compositions on richness/stability.
- **Why it matters for the studio:** Best-evidenced sketch→melody system; its alignment visualisation is a model for showing *how* the compiler interpreted an annotation so the composer can correct the right thing.
- **Tags:** [sketch] [symbolic-generation] [controllability] [HCI-study]
- **Verification:** verified (fetched primary source)
- **BibKey:** liang2024drawlody

### SMT-OMR — Sheet Music Transformer (end-to-end polyphonic OMR), with oemer and Audiveris
- **Who/where/when:** Antonio Ríos-Vila, Jorge Calvo-Zaragoza (U. Alicante), Thierry Paquet (U. Rouen); ICDAR 2024 (arXiv Feb 2024); SMT++ full-page (arXiv May 2024). oemer: BreezeWhite (MIT licence). Audiveris: Hervé Bitteur et al. (AGPL-3.0, v5.5+).
- **Links:** https://arxiv.org/abs/2402.07596 ; https://github.com/antoniorv6/SMT ; https://github.com/BreezeWhite/oemer ; https://github.com/Audiveris/audiveris
- **What it is:** SMT: image-to-sequence Transformer that transcribes *polyphonic* (pianoform, quartet) score images directly to Humdrum **kern, chosen for its simple, parseable vocabulary. oemer: UNet segmentation + SVM classifiers → MusicXML from phone photos. Audiveris: classical pipeline with an interactive **OMR editor** to correct errors before MusicXML 4.0 export.
- **Evidence:** SMT on GrandStaff (53,882 images) and new Quartets set (38,051): SMT_NexT cut Character Error Rate by 91.8% and Line Error Rate by 89.1% vs baselines.
- **Why it matters for the studio:** OMR is how a composer's *paper* or handwritten sketch (photographed) enters the symbolic model; **kern as the OMR target aligns with the LLM-friendly text IR idea; Audiveris's correction-first UI is the right workflow for imperfect recognition.
- **Tags:** [transcription] [notation] [sketch] [toolkit]
- **Verification:** verified (fetched primary sources)
- **BibKey:** riosvila2024smt

---

## C. Image / video / text → music, cross-modal conditioning

### Vis2Mus — Vis2Mus: Exploring Multimodal Representation Mapping for Controllable Music Generation
- **Who/where/when:** Runbang Zhang, Yixiao Zhang, Kai Shao, Ying Shan, Gus Xia; NYU Shanghai Music X Lab / QMUL C4DM / Tencent / MBZUAI; arXiv Nov 2022
- **Links:** https://arxiv.org/abs/2211.05543 ; https://github.com/ldzhangyx/vis2mus
- **What it is:** Uses an image as an *interface* to symbolic accompaniment: an analysis-by-synthesis approach discovers that visual→music mapping is approximately *equivariant* — brightness, contrast and style transformations on the image correspond to musical transformations. User picks a melody sketch + accompaniment image, applies style transfer, then fine-tunes brightness/contrast to steer the generated symbolic accompaniment.
- **Evidence:** User studies: participants matched transformed music to transformed images at 62.5% (brightness), 68.2% (contrast) vs 50% chance, 60.6% (style) vs 25% chance; all p<0.05.
- **Why it matters for the studio:** A rare *symbolic* image-conditioned system with an interpretable control story; demonstrates images as continuous knobs (not just semantic prompts) over arrangement texture.
- **Tags:** [image] [symbolic-generation] [controllability] [accompaniment]
- **Verification:** verified (fetched primary source)
- **BibKey:** zhang2022vis2mus

### MeLFusion — MeLFusion: Synthesizing Music from Image and Language Cues using Diffusion Models
- **Who/where/when:** Sanjoy Chowdhury, Sayan Nag, K J Joseph, Balaji Vasan Srinivasan, Dinesh Manocha; U. Maryland / U. Toronto / Adobe Research; CVPR 2024
- **Links:** https://arxiv.org/abs/2406.04673 ; https://github.com/schowdhury671/melfusion
- **What it is:** Text-to-music diffusion model augmented with a "visual synapse" that injects self-attention features from a pretrained text-to-image model into the music model's cross-attention via learnable blending parameters. Input: image + text; output: audio. New dataset MeLBench (11,250 musician-annotated ⟨image, text, music⟩ triplets) and metric IMSM.
- **Evidence:** Up to 67.98% relative FAD improvement over text-only; 75-participant subjective study on 100 samples.
- **Why it matters for the studio:** Shows images add real information beyond captions for *mood/timbre*; but output is audio only — suitable for the studio's rendering/arrangement stage rather than composition.
- **Tags:** [image] [audio-generation] [text-conditioning] [dataset]
- **Verification:** verified (fetched primary source)
- **BibKey:** chowdhury2024melfusion

### Art2Mus — Art2Mus: Bridging Visual Arts and Music through Cross-Modal Generation (and 2026 extension)
- **Who/where/when:** Ivan Rinaldi, Nicola Fanelli, Giovanna Castellano, Gennaro Vessio; University of Bari Aldo Moro; ECCV 2024 AI4VA workshop (arXiv Oct 2024). Extended version with Matteo Mendula, Florence Levé, Matteo Testi (arXiv Feb 2026, "ArtSound" dataset).
- **Links:** https://arxiv.org/abs/2410.04906 ; https://arxiv.org/abs/2602.17599
- **What it is:** Adds an ImageBind-based image encoder + projection to frozen AudioLDM 2 to generate audio from a digitised painting, trained on synthetic artwork–music pairs (10k ArtGraph artworks × FMA tracks matched by embedding similarity). 2026 version: 105,884 pairs with dual-modality captions; Visual Conditioning Extractor and Image Aligner remove the text bottleneck.
- **Evidence:** 2024: lower KL than baselines but human raters *preferred* standard AudioLDM 2 output. 2026: 15 participants; ImageBind variants slightly better on quality, CLIP variants on semantic alignment.
- **Why it matters for the studio:** An honest negative result — end-to-end image→audio without a symbolic or textual intermediate did not beat text-only generation in listener preference, supporting the studio's "image → editable proposal" stance.
- **Tags:** [image] [audio-generation] [dataset] [evaluation]
- **Verification:** verified (fetched primary sources)
- **BibKey:** rinaldi2024art2mus

### Amuse — Amuse: Human-AI Collaborative Songwriting with Multimodal Inspirations
- **Who/where/when:** Yewon Kim, Sung-Ju Lee (KAIST), Chris Donahue (CMU); CHI 2025 (DOI 10.1145/3706598.3713818)
- **Links:** https://dl.acm.org/doi/10.1145/3706598.3713818 ; PDF https://nmsl.kaist.ac.kr/pdf/CHI25_Amuse.pdf ; https://yewon-kim.com/amuse/
- **What it is:** Images, text or audio → *chord progressions*. GPT-4o extracts music keywords from the inspiration (user can edit keywords), then proposes chord progressions; a rejection sampler filters them with an LSTM chord prior trained on HookTheory (≈50 h) so outputs stay musically plausible while keyword-relevant. A chord transcriber handles audio inspirations (with transposition). Integrated with Hookpad, where users click to insert, audition with instruments, edit chords/melody or regenerate.
- **Evidence:** N=10 songwriters (8 hobbyist, 2 pro), 8-bar chorus tasks, Amuse+Aria vs Aria-only: inspiration transformation 6.20 vs 4.60 (p<0.01), controllability 5.80 vs 4.40 (p=0.036); final-quality ratings similar. 45-musician listening test: rejection-sampled chords matched LSTM coherence and beat raw GPT-4o on relevance (58%, p<0.01). Usage patterns: kickstart (6), ad hoc (3), lyrics-centred (1).
- **Why it matters for the studio:** The exemplar of multimodal *annotation → symbolic proposal* with human-editable intermediate (keywords) and a musically grounded filter — a template for the studio's mood-board/image/reference-audio annotations compiling into lead-sheet material. (Cross-ref: co-creation cluster.)
- **Tags:** [image] [multimodal-input] [symbolic-generation] [co-creation-framework] [HCI-study] [LLM-agent]
- **Verification:** verified (fetched primary source)
- **BibKey:** kim2025amuse

### V2Meow — V2Meow: Meowing to the Visual Beat via Video-to-Music Generation
- **Who/where/when:** Kun Su, Judith Yue Li, Qingqing Huang, Dima Kuzmin, Joonseok Lee, Chris Donahue, Fei Sha, Aren Jansen, Yu Wang, Mauro Verzetti, Timo Denk; Google Research / DeepMind et al.; AAAI 2024 (arXiv May 2023)
- **Links:** https://arxiv.org/abs/2305.06594 ; https://ojs.aaai.org/index.php/AAAI/article/view/28299
- **What it is:** Video frames (1 fps; I3D flow, CLIP, ViT-VQGAN features) plus optional text prompt → 10-s music audio via a three-stage autoregressive pipeline (video → semantic tokens → coarse → fine acoustic tokens, SoundStream decode). Text prompt is the only user control besides the video.
- **Evidence:** MV100K (110k music videos); ~200 raters, 3,500+ ratings; 83.8% visual-relevance preference on MV100K; FAD/KL/MuLan-cycle/beat metrics.
- **Why it matters for the studio:** State of the art for "insert a video as annotation" at the audio level; shows text can steer style while video sets pacing — but offers no symbolic output for a composer to edit.
- **Tags:** [video] [audio-generation] [text-conditioning]
- **Verification:** verified (fetched primary source)
- **BibKey:** su2024v2meow

### Video2Music — Video2Music: Suitable Music Generation from Videos using an Affective Multimodal Transformer Model
- **Who/where/when:** Jaeyong Kang, Soujanya Poria, Dorien Herremans; Singapore University of Technology and Design; Expert Systems with Applications 249 (2024) (arXiv Nov 2023)
- **Links:** https://arxiv.org/abs/2311.00968 ; https://github.com/AMAAI-Lab/Video2Music
- **What it is:** Video → *symbolic chord sequence* (then MIDI with rhythm/loudness variation). Video features: scene cuts, motion, emotion probabilities, semantics; an Affective Multimodal Transformer decodes chords with an affective-matching loss. User supplies video (file or YouTube), desired key and an optional seed chord progression. Dataset MuVi-Sync (748 videos).
- **Evidence:** 21 raters, 7-point scale: 4.2 overall vs 3.5 for a Music Transformer baseline; significant gains on harmonic/rhythmic/loudness matching (p<0.00001). Limitation: chords only, can feel repetitive.
- **Why it matters for the studio:** The main *symbolic* video-to-music system — output is a chord chart the composer can edit, with key and seed controls; a good fit for scoring-to-picture inside a notation-first studio.
- **Tags:** [video] [symbolic-generation] [controllability] [dataset]
- **Verification:** verified (fetched primary source)
- **BibKey:** kang2024video2music

### VidMuse — VidMuse: A Simple Video-to-Music Generation Framework with Long-Short-Term Modeling
- **Who/where/when:** Zeyue Tian, Zhaoyang Liu, Ruibin Yuan, Jiahao Pan, Qifeng Liu, Xu Tan, Qifeng Chen, Wei Xue, Yike Guo; HKUST / Microsoft Research Asia; CVPR 2025 (arXiv June 2024)
- **Links:** https://arxiv.org/abs/2406.04321 ; https://github.com/ZeyueT/VidMuse ; https://vidmuse.github.io/
- **What it is:** CLIP visual encoder → Long-Short-Term Visual module (segment-level and video-level features fused by cross-attention) → autoregressive music-token decoder → EnCodec 32 kHz audio. V2M dataset: ~360k video–music pairs for pretraining, 20k fine-tune, 300 benchmark. Video-only conditioning; no user controls.
- **Evidence:** FAD/FD/KL/Density/Coverage/ImageBind score; A/B study of 600 samples with 40 participants on quality, alignment, musicality.
- **Why it matters for the studio:** Scale reference for video→audio; its long/short-term split (global mood vs local cues) is the right decomposition for annotating a *cue sheet* (global style + hit points) in a symbolic system.
- **Tags:** [video] [audio-generation] [dataset]
- **Verification:** verified (fetched primary source)
- **BibKey:** tian2025vidmuse

### MuMuLLaMA — M²UGen / MuMu-LLaMA: Multi-modal Music Understanding and Generation via Large Language Models
- **Who/where/when:** Atin Sakkeer Hussain, Shansong Liu, Chenshuo Sun, Ying Shan (M²UGen, arXiv Nov 2023); Shansong Liu, Atin Sakkeer Hussain, Qilong Wu, Chenshuo Sun, Ying Shan (MuMu-LLaMA, arXiv Dec 2024); ARC Lab, Tencent PCG
- **Links:** https://arxiv.org/abs/2311.11255 ; https://arxiv.org/abs/2412.06660 ; https://github.com/shansongliu/MuMu-LLaMA
- **What it is:** LLaMA with MERT (music), ViT (image) and ViViT (video) encoders via understanding adapters; output adapters drive MusicGen/AudioLDM 2. Tasks: music QA, text→music, *prompt-based music editing* (MUEdit: speed, pitch, instrument changes), image→music and video→music. Datasets MUCaps/MUImage/MUVideo/MUEdit total 167.69 h.
- **Evidence:** Subjective preference 58.2% (text→music), 81.3% (image→music), 80.7% (video→music) over baselines.
- **Why it matters for the studio:** Demonstrates a single conversational agent accepting *any* modality plus edit instructions — the architectural shape of the studio's annotation compiler — but at the audio level; the symbolic analogue remains to be built.
- **Tags:** [multimodal-input] [image] [video] [editing] [LLM-agent] [audio-generation]
- **Verification:** verified (fetched MuMu-LLaMA PDF; author lists partly from arXiv listings)
- **BibKey:** liu2024mumullama

### MuVi — MuVi: Video-to-Music Generation with Semantic Alignment and Rhythmic Synchronization (and VidMusician)
- **Who/where/when:** Ruiqi Li, Siqi Zheng, Xize Cheng, Ziang Zhang, Shengpeng Ji, Zhou Zhao; Zhejiang University (arXiv Oct 2024, "work in progress"). VidMusician: Sifei Li, Binxin Yang, Chunji Yin, Chong Sun, Yuxin Zhang, Weiming Dong, Chen Li; CAS Institute of Automation / WeChat, Tencent (arXiv Dec 2024).
- **Links:** https://arxiv.org/abs/2410.12957 ; https://arxiv.org/abs/2412.06296
- **What it is:** MuVi: visual adaptor compresses VideoMAE V2 features to audio-rate; contrastive pre-training with *temporal-shift* and random-replacement negatives teaches beat-level synchrony; flow-matching DiT generates audio non-autoregressively; style/genre controls. VidMusician: global visual features as semantic conditions (cross-attention) and local features as rhythmic cues (in-attention) on a text-to-music backbone; DVMSet dataset.
- **Evidence:** MuVi beat-hit score 49.23% vs 25.14% for M²UGen; MOS-Q 3.81. VidMusician outperforms prior methods on DVMSet incl. AI-generated videos.
- **Why it matters for the studio:** Separates *semantic* and *rhythmic* video conditioning — the two annotation types a film composer actually marks (mood, hit points). Suggests a symbolic pipeline: detect hit points → annotate → compile.
- **Tags:** [video] [audio-generation] [controllability]
- **Verification:** verified (fetched primary sources)
- **BibKey:** li2024muvi

---

## D. Annotation tools, encodings and theorists' annotation standards

### SonicVisualiser — Sonic Visualiser: An Open Source Application for Viewing, Analysing, and Annotating Music Audio Files
- **Who/where/when:** Chris Cannam, Christian Landone, Mark Sandler; Centre for Digital Music, QMUL; ACM Multimedia 2010 (software since 2007)
- **Links:** https://www.sonicvisualiser.org/ ; paper https://www.sonicvisualiser.org/sv2010.pdf ; https://github.com/sonic-visualiser/sonic-visualiser
- **What it is:** Desktop tool (GPL) for annotating audio: layers of time instants, time-value curves, notes, regions and labels over waveform/spectrogram; annotations entered by clicking, *tapping* keys during playback, or MIDI input; Vamp plugins add automatic beat/onset/chord/key/segmentation layers that the user then corrects. Export to CSV, MIDI, RDF (Music Ontology).
- **Evidence:** Widely used in MIR/musicology; no formal study in the paper.
- **Why it matters for the studio:** The reference model for *audio-anchored* annotation layers and for "auto-annotate then hand-correct" — the pattern the studio needs for reference-audio annotations (beats, chords, form).
- **Tags:** [annotation] [toolkit] [transcription] [theory-analysis]
- **Verification:** verified (fetched primary source)
- **BibKey:** cannam2010sonicvisualiser

### Dezrann — Dezrann: a web framework to share music analysis (2018) / Interacting with Annotated and Synchronized Music Corpora on the Dezrann Web Platform (2025)
- **Who/where/when:** Mathieu Giraud, Richard Groult, Emmanuel Leguy; CRIStAL (CNRS/Univ. Lille) & MIS (UPJV); TENOR 2018. Ballester, Bacot, Bigo, Borsan, … Giraud et al. (27 authors); TISMIR 2025 (DOI 10.5334/tismir.212)
- **Links:** https://www.dezrann.net ; https://www.tenor-conference.org/proceedings/2018/14_Giraud_tenor18.pdf ; https://transactions.ismir.net/articles/10.5334/tismir.212
- **What it is:** Browser platform for *analytical annotation* of scores and audio: labels (type, onset, optional duration, tag/comment) are placed by left-to-right drag (span) or top-to-bottom gesture (instant, e.g., cadence) on a staff or in zones above/below the score; positions are in **symbolic musical time** (measure + beat, snapping to beat grid/onsets) so the same labels align to score, waveform and video. Stored as `.dez` JSON. GPLv3+ code, ODbL data. 2025: 10 corpora, 1,500+ pieces, 35,000+ annotations (harmony, structure, texture, form), collaborative editing.
- **Evidence:** Corpus scale above; used in musicology teaching and MIR ground truth.
- **Why it matters for the studio:** The best existing *format and UI* for typed, time-anchored, staff-scoped score annotations that machines can read — the studio's annotation layer could adopt `.dez`-style semantics directly and add "instruction" as a label type.
- **Tags:** [annotation] [theory-analysis] [corpus] [toolkit] [notation]
- **Verification:** verified (fetched primary sources)
- **BibKey:** giraud2018dezrann

### MEI-Verovio — MEI (Music Encoding Initiative) and Verovio
- **Who/where/when:** MEI community (Board, Technical Team; Music Encoding Conference), current MEI 5; hosted since 2026 by Akademie der Wissenschaften und Literatur Mainz and RISM Digital Center Bern. Verovio: Laurent Pugin, Rodolfo Zitellini (Swiss RISM), Perry Roland (U. Virginia); ISMIR 2014.
- **Links:** https://music-encoding.org/ ; https://www.verovio.org ; paper https://archives.ismir.net/ismir2014/paper/000221.pdf ; https://github.com/rism-digital/verovio
- **What it is:** MEI is an XML encoding for the full history of Western notation with rich *editorial* markup (readings, corrections, supplied text, genetic/revision layers) and links to facsimiles and audio; Educational Community License 2.0. Verovio engraves MEI to SVG in which every graphical element is an addressable XML element with MEI ids, enabling in-browser interactive scores (also accepts MusicXML, Humdrum, ABC, PAE); open source (LGPL).
- **Evidence:** De facto standard in digital musicology editions; Verovio powers mei-friend, Dezrann visualisation, Foscarin's diff viewer, etc.
- **Why it matters for the studio:** MEI already has vocabulary for "this passage is a variant / correction / editorial suggestion" — i.e., for encoding *AI proposals vs human text*; Verovio's id-addressable SVG is what makes click-to-annotate on a rendered score feasible.
- **Tags:** [representation] [notation] [annotation] [toolkit]
- **Verification:** verified (fetched primary sources)
- **BibKey:** pugin2014verovio

### meiFriend — mei-friend: browser-based MEI editor with GitHub integration
- **Who/where/when:** Werner Goebl, David M. Weigl et al.; mdw – University of Music and Performing Arts Vienna; 2022– (ISMIR 2023 LBD / MEC papers)
- **Links:** https://mei-friend.mdw.ac.at/ ; https://github.com/mei-friend/mei-friend
- **What it is:** "Last-mile" editor: code view of MEI side-by-side with a live Verovio rendering; imports MusicXML/Humdrum/PAE/ABC, exports MEI/SVG/MIDI; **GitHub integration** (open, fork, commit encodings — version control for scores), and **Web Annotations / RDF linked-data annotations** attached to score elements.
- **Evidence:** Tool paper; adoption in MEI community.
- **Why it matters for the studio:** Concrete precedent for (a) text ⇄ notation dual editing (a projectional-editor pattern), (b) git-based history for symbolic music, and (c) standards-based annotations anchored to notation ids.
- **Tags:** [notation] [annotation] [toolkit] [editing]
- **Verification:** partial (site fetched; authorship/paper details from recall)
- **BibKey:** goebl2023meifriend

### MusicXML-MNX — MusicXML 4.0 and MNX (W3C Music Notation Community Group)
- **Who/where/when:** W3C Music Notation Community Group (co-chairs incl. Adrian Holovaty; MusicXML editor Karim Ratib from 2026); MusicXML 4.0 Final Community Group Specification 1 June 2021; MNX in active specification-working-group meetings through Aug 2026
- **Links:** https://www.w3.org/2021/06/musicxml40/ ; https://www.w3.org/community/music-notation/ ; MNX spec at https://mnx.formats.music
- **What it is:** MusicXML: the interchange standard for notation (250+ applications), XML, W3C CG FSA licence. MNX: the successor designed as JSON (`.mnx.json` decided Mar 2026; top-level `mnx` key; IDs up to 256 ASCII chars for app interop) with explicit semantic vs. visual separation; as of the 25 Aug 2026 working-group minutes the group was still settling core encoding (e.g., per-part maximum staves/ossia handling, integer vs float numerics) — **MNX is not yet a finished, widely implemented standard in 2026**.
- **Evidence:** Standards documents and meeting minutes.
- **Why it matters for the studio:** Interchange must be MusicXML 4.0 today; MNX's JSON design and id discipline are worth tracking (and its unfinished state means a studio-internal JSON model is justified), but annotations beyond `<direction>` text are out of scope for both — hence the need for a separate annotation layer.
- **Tags:** [representation] [notation]
- **Verification:** verified (fetched W3C pages/minutes)
- **BibKey:** w3c2021musicxml40

### ABC-abcjs — ABC notation (standard 2.1) and abcjs
- **Who/where/when:** Chris Walshaw (ABC, 1991; standard v2.1 Dec 2011); abc2midi/abcm2ps (James Allwright; Jef Moine); abcjs: Paul Rosen (v6.6.3, Apr 2026)
- **Links:** https://abcnotation.com/wiki/abc:standard:v2.1 ; https://github.com/paulrosen/abcjs
- **What it is:** ABC: plain-text tune format (header fields X:, T:, M:, L:, K:; body of note letters with duration/pitch modifiers); abc2midi compiles to MIDI, abcm2ps to PostScript/SVG. abcjs renders ABC to SVG in the browser, synthesises playback, and provides a *live editor* that re-renders on every keystroke (text ⇄ score).
- **Evidence:** ABC is the dominant text IR in recent music LLMs (ChatMusician, NotaGen, GPT-4 experiments).
- **Why it matters for the studio:** A compact, LLM-friendly textual score language with an existing compile chain (text → MIDI/SVG) and live re-render — the most practical "source code" candidate for the studio's compile step, at the cost of weaker support for complex polyphony/layout than MusicXML/MEI.
- **Tags:** [representation] [music-as-code] [notation] [toolkit]
- **Verification:** verified (fetched primary sources)
- **BibKey:** walshaw2011abc

### Humdrum — Humdrum and the **kern representation
- **Who/where/when:** David Huron (1990s); Humdrum Toolkit; humlib / Verovio Humdrum Viewer (Craig Sapp)
- **Links:** https://www.humdrum.org/ ; https://www.humdrum.org/guide/ch01/ ; https://verovio.humdrum.org
- **What it is:** Tab-separated "spines" (columns per voice/data type) × rows (successive time points) in plain text; **kern encodes pitch/duration/rests/barlines; 70+ Unix-style tools composable via pipes; users add custom spines (e.g., **harm for Roman numerals, **text, **dynam) — i.e., *annotations are just parallel columns*.
- **Evidence:** Long-standing basis for corpora (KernScores, Bach chorales) and now the OMR target of Sheet Music Transformer.
- **Why it matters for the studio:** Humdrum's spine model is an elegant way to store aligned human annotations next to notes in one text file that both LLMs and tools can consume; the "annotation spine" is a ready-made design.
- **Tags:** [representation] [annotation] [toolkit] [theory-analysis]
- **Verification:** verified (fetched primary source)
- **BibKey:** huron1995humdrum

### WebRenderers — OpenSheetMusicDisplay, VexFlow, alphaTab (browser notation rendering)
- **Who/where/when:** VexFlow: Mohit Muthanna Cheppudira (2010–; MIT; v4.2.6 Aug 2024, v5 in development). OSMD: Phonicscore GmbH, Vienna (BSD-3). alphaTab: Daniel Kuschny (MPL-2.0; Guitar Pro/MusicXML/alphaTex).
- **Links:** https://github.com/0xfe/vexflow ; https://github.com/opensheetmusicdisplay/opensheetmusicdisplay ; https://www.alphatab.net
- **What it is:** VexFlow: low-level JS engraving to SVG/Canvas with the EasyScore API. OSMD: MusicXML → VexFlow renderer for browser/Node (SVG/PNG, cursor, transposition, tablature; explicitly "a renderer, not an editor"; playback in early access). alphaTab: renders tablature/notation from Guitar Pro, MusicXML and its own alphaTex text language with synth playback.
- **Evidence:** Widely deployed OSS.
- **Why it matters for the studio:** The practical component options for a web-based score surface: Verovio (MEI-native, ids) vs OSMD/VexFlow (MusicXML-native) vs abcjs (ABC-native); choice couples to the IR decision.
- **Tags:** [toolkit] [notation]
- **Verification:** verified (VexFlow, OSMD fetched; alphaTab partial)
- **BibKey:** cheppudira2010vexflow

### ReaderApps — forScore, Newzik (and nkoda, Enote): rehearsal-annotation score readers
- **Who/where/when:** forScore LLC (iPad, 2010–); Newzik SAS (Paris; iOS/web; ~450k users, 150+ institutions); nkoda (subscription library); Enote (AI-digitised interactive scores)
- **Links:** https://forscore.co/ ; https://newzik.com/en/
- **What it is:** PDF/MusicXML score readers with Apple-Pencil annotation (layers, stamps, fingerings, markers), setlists, page turning via pedals/face gestures. Newzik adds **LiveScores** (OMR turns PDFs into interactive MusicXML: navigation, transposition) and *real-time shared annotation sync* across an ensemble (conductor's marks propagate to players), plus MusicXML/MIDI export.
- **Evidence:** Product claims; Tactus (above) studied the underlying practices.
- **Why it matters for the studio:** Rehearsal marks are the most common real-world "annotation on a score"; Newzik's shared-annotation model shows annotations as first-class, syncable objects separate from the score — the same separation the studio needs between human intent and compiled notation.
- **Tags:** [annotation] [product] [notation]
- **Verification:** verified (forScore, Newzik pages fetched; nkoda/Enote partial)
- **BibKey:** newzik2026readers

### WhenInRome — When in Rome: A Meta-corpus of Functional Harmony (RomanText)
- **Who/where/when:** Mark Gotham, Gianluca Micchi, Néstor Nápoles López, Malcolm Sailor; TISMIR 2023 (DOI 10.5334/tismir.165); RomanText format from Tymoczko, Gotham, Cuthbert, Ariza (ISMIR 2019)
- **Links:** https://transactions.ismir.net/articles/10.5334/tismir.165 ; https://github.com/MarkGotham/When-in-Rome
- **What it is:** 2,000+ Roman-numeral analyses of 1,500 works (c. 1600–1900) in **RomanText (.rntxt)**: a lightweight, human-writable *off-score* text format (measure numbers, beats, keys, Roman numerals, repeats, marginal comments) parsed by music21, with bidirectional conversion to DCML on-score labels. CC BY 4.0 for new material.
- **Evidence:** Corpus scale; conversion/feature-extraction code; used to train Roman-numeral analysis models.
- **Why it matters for the studio:** A proven text syntax in which humans annotate harmony *as instructions the machine can read* ("m5 V7 m6 I") — a natural template for the studio's harmonic-annotation lane and for LLM-readable analysis.
- **Tags:** [theory-analysis] [annotation] [corpus] [representation]
- **Verification:** verified (fetched primary source)
- **BibKey:** gotham2023wheninrome

### DCML-ABC — The Annotated Beethoven Corpus (ABC) and the DCML harmony annotation standard
- **Who/where/when:** Markus Neuwirth, Daniel Harasim, Fabian C. Moss, Martin Rohrmeier; DCML, EPFL; Frontiers in Digital Humanities 5, 2018 (DOI 10.3389/fdigh.2018.00016); corpus v2.x maintained 2018–2025
- **Links:** https://github.com/DCMLab/ABC ; https://dcmlab.github.io/standards ; https://zenodo.org/records/14996911
- **What it is:** Expert harmonic analyses of all 16 Beethoven string quartets (80 movements, ~36,000 labels) entered *directly into MuseScore files as text (harmony/lyrics) attached to notes*, then extracted with the `ms3` parser into TSV tables (notes, measures, chords, labels). The DCML standard is a regular-expression-defined modified Roman-numeral syntax (key, root, inversion, extensions, suspensions, recursive applied chords like V7/V/V, phrase and cadence marks). CC BY-NC-SA 4.0.
- **Evidence:** Corpus scale; inter-annotator review process; downstream ML use.
- **Why it matters for the studio:** Demonstrates the "annotate on the score in the editor, parse to a machine-readable table" workflow the studio wants — human marks typed on the notation become structured data via a grammar. The regex-defined label grammar is directly reusable for validating harmonic instructions.
- **Tags:** [theory-analysis] [annotation] [corpus] [representation]
- **Verification:** verified (fetched repository)
- **BibKey:** neuwirth2018abc

---

## E. Editing paradigms from adjacent fields

### DirectManipulation — Direct Manipulation: A Step Beyond Programming Languages
- **Who/where/when:** Ben Shneiderman; University of Maryland; IEEE Computer 16(8), 1983
- **Links:** https://doi.org/10.1109/MC.1983.1654471
- **What it is:** Defines direct manipulation: continuous representation of the object of interest; physical actions instead of complex syntax; rapid, incremental, reversible operations with immediately visible effect. Contrasted with command languages.
- **Evidence:** Conceptual; foundational.
- **Why it matters for the studio:** The yardstick against which conversational (prompt) editing of music must be judged; the studio's notation view should remain the continuously visible object, with hum/sketch/text as *operators* on selections.
- **Tags:** [editing] [history] [HCI-study]
- **Verification:** partial (well-known; not fetched)
- **BibKey:** shneiderman1983direct

### DirectGPT — DirectGPT: A Direct Manipulation Interface to Interact with Large Language Models
- **Who/where/when:** Damien Masson, Sylvain Malacria, Géry Casiez, Daniel Vogel; University of Waterloo / Inria Lille / Université de Lille; CHI 2024 (arXiv Oct 2023)
- **Links:** https://arxiv.org/abs/2310.03691 (CHI 2024 proceedings version via ACM DL)
- **What it is:** A UI layer over ChatGPT that turns direct-manipulation actions into engineered prompts: continuous representation of generated objects; toolbar commands that reuse prompt syntax; outputs that can be dragged/selected to compose prompts; undo. Evaluated on editing text, code and vector images.
- **Evidence:** Users were 50% faster, used 50% fewer prompts and 72% shorter prompts vs. baseline ChatGPT.
- **Why it matters for the studio:** Directly informs the "edit" step: select bars/voices on the score, then hum/type/draw — the selection becomes the scope of the compiled instruction, dramatically shortening prompts.
- **Tags:** [editing] [LLM-agent] [HCI-study] [controllability]
- **Verification:** verified (fetched primary source)
- **BibKey:** masson2024directgpt

### ExpressEdit — ExpressEdit: Video Editing with Natural Language and Sketching
- **Who/where/when:** Bekzat Tilekbay, Saelyne Yang, Michal Lewkowicz (Yale), Alex Suryapranata, Juho Kim; KAIST; IUI 2024 (DOI 10.1145/3640543.3645164)
- **Links:** https://arxiv.org/abs/2403.17693 ; https://doi.org/10.1145/3640543.3645164
- **What it is:** Users describe edits in natural language *and* sketch on frames (regions, arrows); an LLM + vision pipeline resolves temporal ("when the speaker points"), spatial and operational references into concrete edit operations that users then refine. Design was grounded in 176 multimodal edit expressions collected from 10 editors.
- **Evidence:** Observational study N=10 novices: better ability to express and implement edit ideas; more edit ideas generated.
- **Why it matters for the studio:** The cleanest analogue of "scribble + words on the artefact → machine executes edit → human refines" from a neighbouring time-based medium; its formative study method (collect natural multimodal edit expressions first) is worth replicating for music.
- **Tags:** [editing] [sketch] [multimodal-input] [HCI-study] [LLM-agent]
- **Verification:** verified (fetched primary source)
- **BibKey:** tilekbay2024expressedit

### InstructPix2Pix — InstructPix2Pix: Learning to Follow Image Editing Instructions
- **Who/where/when:** Tim Brooks, Aleksander Holynski, Alexei A. Efros; UC Berkeley; CVPR 2023 (arXiv Nov 2022)
- **Links:** https://arxiv.org/abs/2211.09800 ; https://www.timothybrooks.com/instruct-pix2pix
- **What it is:** Conditional diffusion model that takes (image, edit instruction) → edited image in one forward pass. Training pairs were *synthesised* by GPT-3 (instruction + edited caption) and Stable Diffusion with prompt-to-prompt, avoiding human labelling.
- **Evidence:** Qualitative generalisation to real images and arbitrary instructions; ablations.
- **Why it matters for the studio:** The template for *instruction-conditioned editing* of an existing artefact and for bootstrapping (score, annotation, edited-score) training triples synthetically — the missing dataset for annotation-driven symbolic editing.
- **Tags:** [editing] [text-conditioning] [controllability]
- **Verification:** verified (fetched primary source)
- **BibKey:** brooks2023instructpix2pix

### Teddy — Teddy: A Sketching Interface for 3D Freeform Design
- **Who/where/when:** Takeo Igarashi, Satoshi Matsuoka, Hidehiko Tanaka; University of Tokyo; SIGGRAPH 1999
- **Links:** https://www-ui.is.s.u-tokyo.ac.jp/~takeo/teddy/teddy.htm
- **What it is:** Freeform 2D strokes are inflated into 3D models; extrusion, cutting and smoothing are also strokes. Establishes the sketch-based-interface principle: infer a plausible complete object from an ambiguous gesture, immediately show it, and let the user refine with further gestures.
- **Evidence:** Demonstrations; later user studies in the SBIM community.
- **Why it matters for the studio:** The interaction contract for sketch→music: coarse gesture, plausible inference, instant display, gestural refinement (rather than dialog boxes).
- **Tags:** [sketch] [editing] [history]
- **Verification:** verified (project page fetched)
- **BibKey:** igarashi1999teddy

### PBD — Watch What I Do: Programming by Demonstration
- **Who/where/when:** Allen Cypher (ed.), with Daniel C. Halbert, David Kurlander, Henry Lieberman, David Maulsby, Brad A. Myers, Alan Turransky; MIT Press, 1993
- **Links:** https://acypher.com/wwid/
- **What it is:** Collected systems in which "if a user knows how to perform a task on the computer, that should be sufficient to create a program to perform the task": the system generalises from demonstrated examples to a reusable procedure, with the user correcting over-/under-generalisation.
- **Evidence:** Survey volume.
- **Why it matters for the studio:** Frames *example audio/MIDI as a demonstration*: "voice the chords like this passage" is PBD — the compiler should generalise a demonstrated arrangement pattern and let the composer correct the generalisation.
- **Tags:** [editing] [history] [co-creation-framework]
- **Verification:** verified (book site fetched)
- **BibKey:** cypher1993wwid

### LiveProg — Live programming (Tanimoto 2013), Hazel typed holes (POPL 2019), and projectional editing (JetBrains MPS)
- **Who/where/when:** Steven L. Tanimoto, "A Perspective on the Evolution of Live Programming," LIVE 2013 (ICSE workshop). Cyrus Omar, Ian Voysey, Ravi Chugh, Matthew A. Hammer, "Live Functional Programming with Typed Holes," POPL 2019 (PACMPL 3). JetBrains MPS (projectional language workbench).
- **Links:** https://arxiv.org/abs/1805.00155 ; https://hazel.org ; https://www.jetbrains.com/mps/concepts/
- **What it is:** Tanimoto's liveness levels (1–6) describe how immediately a program's edits are reflected in running output. Hazel gives a dynamic semantics for *incomplete* programs: evaluation proceeds *around* typed holes, so every editor state yields feedback. MPS edits the AST directly (no parser) and projects it in multiple notations (text, tables, diagrams) simultaneously.
- **Evidence:** Formal semantics (Hazel); industrial use (MPS).
- **Why it matters for the studio:** Three pillars for a musical compile-edit loop: (1) liveness — re-render/re-play on every annotation; (2) *holes* — a score with `[to be composed]` regions should still compile and play, with the AI filling holes; (3) projectional editing — one musical model viewed as notation, piano roll, chord chart and text, all editable.
- **Tags:** [music-as-code] [editing] [representation]
- **Verification:** verified for Hazel and MPS (fetched); Tanimoto partial
- **BibKey:** omar2019hazel

---

## F. Version control, history, branching for music

### ScoreDiff — A Diff Procedure for Music Score Files
- **Who/where/when:** Francesco Foscarin, Florent Jacquemard, Raphaël Fournier-S'niehotta; CNAM / Inria Paris; 6th International Conference on Digital Libraries for Musicology (DLfM), 2019 (DOI 10.1145/3358664.3358671)
- **Links:** https://doi.org/10.1145/3358664.3358671
- **What it is:** Compares two scores at the *graphical notation* level via an intermediate tree representation per bar/voice, combining sequence edit distance (bars) with tree edit distance (beaming/tuplet hierarchies); a Verovio-based visualiser shows the two scores side by side with differences highlighted. Motivated by collaborative editing and version control; validated on OMR datasets.
- **Evidence:** Evaluation on OMR output vs ground truth; tool released.
- **Why it matters for the studio:** The only fetched research artefact for *musical diff* — necessary for showing what the compiler changed between versions and for reviewing AI edits like a code review.
- **Tags:** [notation] [editing] [toolkit] [evaluation]
- **Verification:** verified (metadata/abstract via Semantic Scholar API)
- **BibKey:** foscarin2019diff

### FlatHistory — Flat.io version history (and Splice Studio / Blend as DAW-project precedents)
- **Who/where/when:** Tutteo Ltd (Flat.io), ongoing; Splice Studio (Splice, DAW project backup/versioning, 2013 – discontinued c. 2021); Blend.io (DAW project sharing/remixing, 2013 – defunct)
- **Links:** https://help.flat.io/en/music-notation-software/history/
- **What it is:** Flat auto-syncs every edit; major versions are created every ≤50 modifications; free users can restore the 10 most recent major versions, paid users can scrub *every single change* with a video-like slider, see change locations on a score scrollbar, view per-contributor colour coding, restore, or export any state to MusicXML/MIDI. Splice Studio offered git-like commit history and collaboration for Ableton/Logic/FL project files; Blend offered project sharing and forking.
- **Evidence:** Product documentation.
- **Why it matters for the studio:** Flat shows a linear, fine-grained, attributable history for notation is deliverable; the demise of Splice Studio/Blend signals that *file-level* DAW versioning had limited pull — semantic, musically-aware diffs and branches are the unexplored space.
- **Tags:** [product] [editing] [notation]
- **Verification:** Flat verified (fetched); Splice Studio and Blend unverified (recall)
- **BibKey:** flat2026history

### Chronicle — Chronicle: Capture, Exploration, and Playback of Document Workflow Histories
- **Who/where/when:** Tovi Grossman, Justin Matejka, George Fitzmaurice; Autodesk Research; UIST 2010
- **Links:** https://www.research.autodesk.com/publications/chronicle-capture-exploration-and-playback-of-document-workflow-histories/
- **What it is:** Records the full video and event history of a graphical document; users click any region of the final document to see the workflow, tools and settings that produced it, and play it back. Later shipped as Autodesk Screencast.
- **Evidence:** User study found it useful and easy to use.
- **Why it matters for the studio:** Provenance UI for creative artefacts: clicking a passage in the compiled score should reveal *which annotations and which compile* produced it — essential for trust in AI-authored material.
- **Tags:** [editing] [HCI-study] [creativity-support]
- **Verification:** verified (project page fetched; first author from recall)
- **BibKey:** grossman2010chronicle

### Luminate — Luminate: Structured Generation and Exploration of Design Space with LLMs for Human-AI Co-Creation (and Parallel Paths)
- **Who/where/when:** Sangho Suh, Meng Chen, Bryan Min, Toby Jia-Jun Li, Haijun Xia; UC San Diego / Notre Dame; CHI 2024 (DOI 10.1145/3613904.3642400). Precedent: Michael Terry, Elizabeth Mynatt, Kumiyo Nakakoji, Yasuhiro Yamamoto, "Variation in Element and Action: Supporting Simultaneous Development of Alternative Solutions" (Parallel Paths), CHI 2004.
- **Links:** https://arxiv.org/abs/2310.12953
- **What it is:** Instead of one chat answer, the LLM first generates *dimensions* of the design space, then a structured grid/space of many responses that users browse, filter, evaluate and combine. Parallel Paths (2004) let image editors develop several alternatives side by side from a shared history.
- **Evidence:** Luminate: N=14 professional writers found it feasible and useful for exploration.
- **Why it matters for the studio:** Model for *variation trees* over compiled outputs: several arrangements of the same annotated passage explored in parallel, with dimensions (density, register, style) as axes — a music analogue is not yet published.
- **Tags:** [creativity-support] [LLM-agent] [HCI-study] [co-creation-framework]
- **Verification:** verified (Luminate fetched); Parallel Paths partial
- **BibKey:** suh2024luminate

---

## G. Music as code / compile lineage

### LilyPond — LilyPond: music engraving compiler
- **Who/where/when:** Han-Wen Nienhuys, Jan Nieuwenhuizen (1996–); GNU project; "LilyPond, a system for automated music engraving," XIV Colloquium on Musical Informatics, 2003
- **Links:** https://lilypond.org/
- **What it is:** Text source (`\relative c' { c4 d e f }`) is *compiled* into engraved PDF/SVG/MIDI; layout decisions are made programmatically following classical engraving rules; extensible in Scheme. GPL. Explicitly the "music as source code → compiler → typeset output" model; used by Sheet Sage and MuseScore export pipelines.
- **Evidence:** Decades of use; engraving quality frequently cited.
- **Why it matters for the studio:** The literal precedent for "compile"; its pain points (edit–compile latency, error messages in terms of source not score) are exactly what a live, projectional studio should fix.
- **Tags:** [music-as-code] [notation] [toolkit]
- **Verification:** verified (site fetched; 2003 paper partial)
- **BibKey:** nienhuys2003lilypond

### AudioLangs — Csound, SuperCollider, Max/Pure Data, ChucK, Faust: audio programming languages
- **Who/where/when:** Csound: Barry Vercoe, MIT, 1985/86 (LGPL; Csound 7, web IDE). SuperCollider: James McCartney 1996, GPL 2002 (v3.14.1). Max: Miller Puckette, IRCAM 1988 (Cycling '74); Pure Data: Puckette 1996 (open source). ChucK: Ge Wang & Perry Cook, Princeton/Stanford, ICMC 2003; CMJ 2015 (v1.5.5.x; WebChucK). Faust: GRAME-CNCM (Orlarey, Fober, Letz), 2002–.
- **Links:** https://csound.com/ ; https://supercollider.github.io/ ; https://puredata.info/ ; https://chuck.stanford.edu/ ; https://faust.grame.fr/
- **What it is:** Csound: orchestra (instrument definitions) + score (note events) text files rendered to audio — a pure compile model. SuperCollider: scsynth server + sclang client; on-the-fly code evaluation. Max/Pd: visual dataflow patching with real-time signal graphs. ChucK: "strongly-timed" concurrent language where time is a first-class variable and code is added/replaced while running. Faust: functional block-diagram DSL compiled to C++/C/LLVM/WASM/Rust and to plugins/apps/web.
- **Evidence:** Canonical systems; each with long publication records.
- **Why it matters for the studio:** Two compile philosophies to borrow: Csound's *orchestra/score separation* (sound design vs. musical text — analogous to arrangement/rendering vs. notation) and ChucK/SC's *live re-evaluation* (edit code while music plays). Faust proves a DSL can compile to many targets — a model for compiling one musical IR to MusicXML, MIDI and audio.
- **Tags:** [music-as-code] [toolkit] [real-time] [history]
- **Verification:** verified (all project sites fetched)
- **BibKey:** wang2015chuck

### LiveCoding — TidalCycles, Strudel, Sonic Pi, Gibber, FoxDot: live coding environments
- **Who/where/when:** TidalCycles: Alex McLean, 2009– (Haskell; "Making programming languages to dance to: live coding with Tidal," FARM 2014). Strudel: Felix Roos, Alex McLean et al., 2022– (JS port of Tidal; AGPL-3.0; codeberg.org/uzu/strudel; ICLC 2023 paper). Sonic Pi: Sam Aaron, 2012– (Ruby; v5.0; "From Sonic Pi to Overtone," FARM 2013 with Alan Blackwell). Gibber: Charlie Roberts (ICMC 2012). FoxDot: Ryan Kirkbride (Python; ICLC 2016).
- **Links:** https://tidalcycles.org/ ; https://strudel.cc ; https://codeberg.org/uzu/strudel ; https://sonic-pi.net/ ; https://gibber.cc/
- **What it is:** Pattern languages where short code expressions describe cyclic musical patterns and are *re-evaluated live* while sound continues (Tidal/Strudel mini-notation `"bd sd [hh hh]"`; Sonic Pi `live_loop` with `sync`, Ableton Link). Strudel runs entirely in the browser with inline visualisations and a tutorial REPL; Gibber annotates the running code with live values. Sonic Pi was co-designed with teachers for UK computing curricula.
- **Evidence:** Community scale (algorave); Sonic Pi education deployments; Strudel adoption via browser.
- **Why it matters for the studio:** Live coding is the most developed practice of *music as continuously recompiled code*; mini-notations show how terse a musical text IR can be, and Strudel/Gibber show in-editor visual feedback of what the code produced — a pattern for showing how annotations compiled.
- **Tags:** [music-as-code] [real-time] [education] [toolkit]
- **Verification:** verified (sites fetched; McLean 2014 metadata via S2; Roos & McLean 2023 / Aaron & Blackwell 2013 / Kirkbride 2016 partial)
- **BibKey:** mclean2014tidal

### CAC — OpenMusic, bach, PWGL: computer-aided composition environments
- **Who/where/when:** OpenMusic: Carlos Agon, Gérard Assayag, Jean Bresson, Karim Haddad; IRCAM Music Representations team, 1998– (GPLv3; OM 8.0 released 30 Mar 2026; Assayag et al., CMJ 1999). bach: Andrea Agostini & Daniele Ghisi, 2010– (GPLv3; CMJ 2015). PWGL: Mikael Laurson, Mika Kuuskankare, Vesa Norilo, Sibelius Academy (CMJ 2009).
- **Links:** https://github.com/openmusic-project/openmusic ; https://www.bachproject.net/
- **What it is:** OpenMusic: visual Lisp programming — patches of boxes compute musical structures displayed in editable common-notation, piano-roll and sound editors; the *maquette* arranges patches on a timeline. bach: brings CAC into Max in real time with `bach.roll` (proportional notation) and `bach.score` (measured notation) objects editable by mouse *or* by patching, plus cage/dada/ears libraries. PWGL: Lisp-based visual environment with the Expressive Notation Package.
- **Evidence:** Used by generations of IRCAM/Ircam-adjacent composers; extensive literature.
- **Why it matters for the studio:** These are the composers' own "compile" tools: programs generate notation that is then hand-edited — the same loop the studio proposes, with AI replacing hand-written Lisp. Their dual editing (edit the program or edit the output notation) is the central UX question for the studio: which edits round-trip?
- **Tags:** [music-as-code] [notation] [toolkit] [history]
- **Verification:** verified (OpenMusic, bach sites fetched; PWGL partial)
- **BibKey:** assayag1999openmusic

### TextMusicLangs — Euterpea / Haskell School of Music, Alda, music21
- **Who/where/when:** Euterpea/HSoM: Paul Hudak & Donya Quick, Yale; *The Haskell School of Music* (Cambridge UP, 2018); development concluded. Alda: Dave Yarwood, 2012– (EPL-2.0). music21: Michael Scott Asato Cuthbert, MIT, 2006– (BSD-3; v10.5.0 June 2026; Cuthbert & Ariza, ISMIR 2010).
- **Links:** https://www.euterpea.com/ ; https://github.com/alda-lang/alda ; https://github.com/cuthbertLab/music21
- **What it is:** Euterpea: algebraic `Music` datatype in Haskell (notes, rests, parallel/sequential composition, modifiers) rendered to MIDI. Alda: musician-friendly text (`piano: o3 g8 a b > c d e f+ g`) with a REPL and MIDI playback, designed for algorithmic composition and live coding. music21: Python object model for scores with parsers/writers for MusicXML, MEI, **kern, ABC, MIDI, RomanText and rich analysis (keys, Roman numerals, intervals); the de facto "compiler toolkit" between representations.
- **Evidence:** HSoM textbook adoption; Alda 5.9k GitHub stars; music21 ubiquitous in MIR research.
- **Why it matters for the studio:** Concrete options for the studio's internal IR and conversion layer: an algebraic datatype (Euterpea) for a principled musical AST; Alda for a readable surface syntax; music21 as the import/export/analysis backbone.
- **Tags:** [music-as-code] [representation] [toolkit] [theory-analysis]
- **Verification:** verified (sites fetched)
- **BibKey:** cuthbert2010music21

### CompositionScholarship — Algorithmic composition & music-representation scholarship
- **Who/where/when:** Gerhard Nierhaus, *Algorithmic Composition: Paradigms of Automated Music Generation*, Springer 2009 (DOI 10.1007/978-3-211-75540-2). Roger B. Dannenberg, "Music Representation Issues, Techniques, and Systems," Computer Music Journal 17(3), 1993. Thor Magnusson, *Sonic Writing: Technologies of Material, Symbolic and Signal Inscriptions*, Bloomsbury 2019; also "Algorithms as Scores: Coding Live Music," Leonardo Music Journal 21, 2011. Curtis Roads, *The Computer Music Tutorial*, MIT Press 1996 (2nd ed. 2023).
- **Links:** https://link.springer.com/book/10.1007/978-3-211-75540-2
- **What it is:** Nierhaus surveys Markov models, generative grammars, transition networks, chaos/self-similarity, genetic algorithms, cellular automata, neural networks and AI as compositional paradigms. Dannenberg lays out the representation problem — hierarchy, time, multiple simultaneous views, performance vs. score — that any musical IR must solve. Magnusson theorises notation, instruments and code as three inscription technologies and argues code is a new kind of score.
- **Evidence:** Standard references.
- **Why it matters for the studio:** Dannenberg's issues list is a checklist for the studio's internal representation; Magnusson's "code as score" supplies the conceptual bridge from *compile* metaphor to compositional practice; Nierhaus catalogues what a rule-based "compiler backend" can do without ML.
- **Tags:** [music-as-code] [representation] [history]
- **Verification:** Nierhaus verified (fetched); Dannenberg, Magnusson, Roads partial (well-known, not fetched)
- **BibKey:** nierhaus2009algorithmic

### ChatMusician — ChatMusician: Understanding and Generating Music Intrinsically with LLM
- **Who/where/when:** Ruibin Yuan, Hanfeng Lin, Yi Wang, Zeyue Tian, Shangda Wu, et al. (Multimodal Art Projection, Skywork AI, HKUST); Findings of ACL 2024 (arXiv Feb 2024)
- **Links:** https://arxiv.org/abs/2402.16153 ; https://github.com/hf-lin/ChatMusician
- **What it is:** LLaMA2-7B continually pretrained/fine-tuned on MusicPile (4B tokens) to read and write **ABC notation** with a plain text tokenizer — "music as a second language." Generates full pieces conditioned on text, chords, melodies, motifs and musical forms; also answers theory questions (MusicTheoryBench).
- **Evidence:** Surpasses GPT-4 baseline on conditioned composition (human/automatic eval); beats LLaMA2 and GPT-3.5 zero-shot on MusicTheoryBench; slightly higher MMLU than base.
- **Why it matters for the studio:** Proof that a general LLM can treat a textual score language as code — the enabling assumption for an annotation→ABC/kern compiler; also shows conditioning on *partial symbolic material* (motif, chords, form) works.
- **Tags:** [music-as-code] [symbolic-generation] [text-conditioning] [LLM-agent] [representation]
- **Verification:** verified (fetched primary source)
- **BibKey:** yuan2024chatmusician

### MIDILLM — MIDI-LLM: Adapting Large Language Models for Text-to-MIDI Music Generation
- **Who/where/when:** Shih-Lun Wu, Yoon Kim, Cheng-Zhi Anna Huang; MIT; arXiv Nov 2025
- **Links:** https://arxiv.org/abs/2511.03942
- **What it is:** Extends Llama 3.2 (1B) vocabulary with ~55k MIDI tokens (Anticipatory Music Transformer arrival-time encoding: onset, duration, instrument-pitch); two-stage training (continued pretraining on music text + MIDI, then SFT on text–MIDI pairs). Keeps the standard LLM architecture so vLLM-style acceleration applies.
- **Evidence:** FAD 0.173 vs 0.818 for text2midi baseline; 4–14× faster inference.
- **Why it matters for the studio:** Cross-ref to text-to-symbolic cluster; relevant here as the "MIDI-as-code inside an LLM" alternative to ABC — the studio must choose between notation-level (ABC/kern) and performance-level (MIDI tokens) IRs.
- **Tags:** [symbolic-generation] [text-conditioning] [music-as-code] [LLM-agent]
- **Verification:** verified (fetched primary source)
- **BibKey:** wu2025midillm

### Libretto — Libretto: Giving LLM Agents a Sense of Musical Structure
- **Who/where/when:** Yichen Xu; UC Berkeley; arXiv June 2026 (CC BY 4.0)
- **Links:** https://arxiv.org/abs/2606.22708 ; https://github.com/Xyc-arch/Libretto ; https://libretto.site/
- **What it is:** A text grammar for symbolic music with explicit onset slots, voice declarations and bar-level blocks (timing is readable without accumulating durations), plus a 29-axis "structural fingerprint" (rhythm, harmony, melody, texture, form, variation) calibrated to corpus percentiles. An LLM agent runs generate → measure → *musician-readable feedback* ("reduce harmonic instability") → revise loops; supports gap-filling, whole-piece composition, style morphing and pedagogy drills.
- **Evidence:** 314-song Lakh reference corpus; gap-filling pass rate 12% (single shot) → 39% (loop); full-piece generation 94% with retrieval + refinement; copy-risk gates.
- **Why it matters for the studio:** The closest thing to an "annotation-driven compiler": human-legible structural notes steer revision of a text-encoded score in a loop — precisely the compile→annotate→edit cycle, though the feedback is currently generated by metrics rather than by a composer's margin notes.
- **Tags:** [music-as-code] [LLM-agent] [symbolic-generation] [structure] [evaluation] [infilling]
- **Verification:** verified (fetched primary source)
- **BibKey:** xu2026libretto

---

## Gaps and cross-cluster pointers
- **Annotations-as-prompts (score margin notes → machine instructions):** not found as a distinct line of work; nearest: EuterPen (spatial multimodal annotations, no AI), Dezrann/DCML (typed machine-readable analytical labels), Libretto (LLM revises under structural feedback), Amuse (keywords as editable intermediate), ExpressEdit/DirectGPT (selection + NL/sketch → edit). This is open territory.
- Cross-refs: Amuse, Cococo, ExpressEdit → co-creation/HCI cluster; MT3/Basic Pitch/Sheet Sage → transcription/representation cluster; ChatMusician, MIDI-LLM, MuseCoco, text2midi, NotaGen → text-to-symbolic cluster; Music ControlNet (melody/dynamics/rhythm curves) → controllability cluster (curve annotations relate to B); SingSong/V2Meow/VidMuse → audio-generation cluster.
