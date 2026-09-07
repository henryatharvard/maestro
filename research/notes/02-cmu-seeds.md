# 02 — CMU music-AI cluster + founder seed items (Amuse, Jan-2026 CMU study, ExpressEdit, REAL)

## Overview

Carnegie Mellon hosts two generations of music-AI research that map almost exactly onto the studio's thesis. The older generation is Roger Dannenberg (Emeritus, CS/Art/Music): real-time computer accompaniment (ICMC 1984), the Nyquist composition language, co-founding Audacity, the "Human-Computer Music Performance" (HCMP) programme, and — with PhD student Shuqi Dai (2020–2024) — a sustained argument that deep music generation lacks *hierarchical structure and repetition*, answered with structure-aware, user-editable melody generation ("MusicFrameworks", imitation-based personalised generation). The newer generation is Chris Donahue's Generative Creativity Lab (G-CLef, gclef-cmu.org; Donahue holds the *Dannenberg* Assistant Professorship and is part-time at Google DeepMind/Magenta). G-CLef's line runs Piano Genie (2019) → Sheet Sage lead-sheet transcription (2022) → Anticipatory Music Transformer infilling (2023) → the deployed **Hookpad Aria** copilot (2024) → **Amuse** multimodal-inspiration songwriting (CHI 2025 Best Paper) → a **design space of live music agents** (CHI 2026) → **Decomposer** (2026), which literally *decompiles MIDI into editable Strudel programs* — the closest existing realisation of the founder's "composition as program / compile" metaphor. The lab also owns the evaluation stack (Music Arena, MAD metric) and audio-control work (Music ControlNet, with Watanabe and Adobe). Two of the founder's named seeds turned out *not* to be CMU music work: **ExpressEdit** is a KAIST (Juho Kim's KIXLAB) IUI 2024 video-editing system that is nonetheless the best available template for natural-language + sketch annotation-driven editing; **REAL** is a small 2026 GitHub project (two-person student team, Claude-Code skills) for human-director-centred *video* assembly whose four-step pipeline ends in a `/real-compile` step — a vocabulary twin of the studio's loop, but not a research system and not about music. The Jan-2026 CMU news item ("humans still lead in creativity") is a Heinz College (Oros/Telang) + School of Music (Randall) randomised experiment with Udio, presented only as a CODE@MIT 2025 poster; no paper is public yet.

## Key takeaways for the studio

- **Hookpad Aria is the closest deployed precedent for the studio's core loop**: a lead-sheet editor (melody + chords, symbolic) with an AI that does continuation, *infilling of arbitrary spans*, and harmony↔melody — non-sequential composition. Its acceptance data (74k of 318k suggestions accepted by 3k users in ~9 months) is the best public evidence that musicians want *span-level* suggestions inside a notation editor rather than whole songs.
- **Amuse shows how to turn multimodal annotations (image / text / audio) into symbolic material without paired data**: multimodal LLM → keywords (a transparent, user-editable intermediate) → N chord candidates → *rejection sampling against a small music prior* trained on Hooktheory (accept if u < P(x)/(M·Q(x))). This "LLM proposes, music model filters" pattern is directly reusable for any annotation → notation step. Study evidence (N=10 within-subjects, Wilcoxon) shows large gains in inspiration support, controllability, exploration, expressiveness, with *no* difference in time or judged output quality.
- **Decomposer (2026) is the literal "music as compiled program" result**: MIDI → Strudel code that re-renders faithfully and exposes repeats/voices/harmony as editable structure; trained with SFT + RL on execution-based faithfulness and readability rewards. Adopt its decompile↔compile framing, its readability rubric, and Strudel (or a similar live-coding DSL) as one candidate intermediate representation.
- **Anticipatory Music Transformer is the right generative primitive for "compile a part given fixed material"**: asynchronous conditioning on control events lets the human pin notes/parts and have the model fill the rest; it also runs in-browser (MIDInfinite, 51 notes/s on M3).
- **Dai & Dannenberg supply the structural-representation argument**: their ISMIR 2022 analysis shows Music Transformer-style outputs differ strikingly from human pop in repetition/structure; MusicFrameworks makes section/phrase structure, chords and "basic melody" *explicit user-editable inputs* — an editable structural skeleton is exactly the kind of annotation layer the studio wants.
- **ExpressEdit is the template for multimodal annotation-driven editing**: user writes NL + sketches on a frame; GPT-4 decomposes the request into *temporal / spatial / operation / parameter* references; per-modality resolvers (transcript similarity, CLIP+SAM) locate targets; the system returns *editable suggestions with an "examine" breakdown* of how it interpreted each reference. Replace frame→bar/staff, timeline→score timeline, CLIP→symbolic/audio similarity and you have a music annotation compiler. 46% of suggestions accepted, 58% of final edits were modified suggestions — iteration, not one-shot.
- **REAL's one transferable lesson**: "a coherent error reads as an editorial fact" — pipelines must validate loudly and *badge estimated vs measured* quantities; the "word is the identity, the timestamp is derived" anchoring idea maps to anchoring annotations to musical events (bar/beat/note) with timestamps derived at compile time.
- **Evaluation infrastructure exists to borrow**: Music Arena (live pairwise TTM preference with open data), MAD (embedding-based divergence correlating 0.84 with human rankings vs FAD 0.49), SynTheory (probes whether models encode theory concepts), and Dannenberg/Dai structure metrics.
- **Sketch-based *music* editing exists but is thin**: Draw and Listen! (TISMIR 2022, Rochester) inpaints a melody from drawn pitch-contour and note-density curves; no system yet combines NL + sketch + audio-example annotation on notation the way ExpressEdit does for video — this is white space.
- **Structure/alignment plumbing**: Just Label the Repeats (ISMIR 2024) shows that *one targeted human annotation* (clicking repeat signs) lifts audio↔score alignment from 33% to 82% — a strong argument for cheap, well-placed human annotation over full automation.

---

### G-CLef — Generative Creativity Lab (G-CLef) @ CMU
- **Who/where/when:** Chris Donahue (PI, Dannenberg Assistant Professor, CMU CSD; part-time Research Scientist, Google DeepMind Magenta). PhD students: Wayne Chi, Irmak Bukey, Yewon Kim, Nathan Pruyne (CSD), Alexander Wang (HCII). MS: Satvik Dixit (ECE), Lynn Ye (Music & Technology). Alumni: Shih-Lun Wu (now MIT PhD), Xun Zhou, Yichen Huang. Founded 2023 when Donahue joined CMU after a Stanford postdoc (Percy Liang) and UCSD PhD (Puckette, McAuley).
- **Links:** https://gclef-cmu.org/ ; https://gclef-cmu.org/research ; https://gclef-cmu.org/team ; https://chrisdonahue.com/publication/
- **What it is:** Lab mission "empower and enrich human creativity and productivity with generative AI", centred on music with side-lines in code LLM evaluation (Copilot Arena, ICML 2025) and agents. Publications 2023–2026 (lab page): SingSong (arXiv 2023); Anticipatory Music Transformer (TMLR 2024); Music ControlNet (TASLP 2024); ReaLchords (ICML 2024); V2Meow (AAAI 2024); Foundation Models for Music survey (arXiv 2024); Towards Music-Aware Virtual Assistants (UIST 2024); Do Music Generation Models Encode Music Theory? (ISMIR 2024); Just Label the Repeats (ISMIR 2024); Hookpad Aria (ISMIR LBD 2024); MIDInfinite/local deployment (ISMIR LBD 2024); Amuse (CHI 2025, Best Paper); Copilot Arena (ICML 2025); Aligning Text-to-Music Evaluation with Human Preferences (ISMIR 2025); Music Arena (NeurIPS 2025 Creative AI track); Live Music Models / Magenta RealTime (arXiv 2025); RISE (ISMIR 2025); Unified Cross-modal Translation (TASLP 2025, with Sogang); A Design Space for Live Music Agents (CHI 2026); MultiVerse (UIST 2026); Decomposer (preprint 2026). Jan 2026 news: two ICASSP 2026 papers (FoleyBench, music captioning), EDIT-Bench (ICLR 2026 oral), Schmidt HAVI grant for a multimodal music-AI project co-led with Annie Hsieh.
- **Evidence:** —
- **Why it matters for the studio:** The single most aligned academic group: symbolic-first, deployed-with-real-musicians (Hookpad Aria), multimodal inspiration (Amuse), and now programs-as-representation (Decomposer). Natural collaboration / hiring pool; their public PDFs are all at gclef-cmu.org/static/pdfs/.
- **Tags:** [co-creation-framework] [symbolic-generation] [evaluation] [HCI-study] [history]
- **Verification:** verified (fetched lab pages and chrisdonahue.com)
- **BibKey:** gclef2026lab

### Amuse — Amuse: Human-AI Collaborative Songwriting with Multimodal Inspirations
- **Who/where/when:** Yewon Kim (KAIST → now CMU PhD), Sung-Ju Lee (KAIST), Chris Donahue (CMU). ACM CHI 2025 (Yokohama), **Best Paper Award** (top ~1%; confirmed on the G-CLef page and Kim's site). arXiv Dec 2024.
- **Links:** https://arxiv.org/abs/2412.18940 ; https://doi.org/10.1145/3706598.3713818 ; project: https://yewon-kim.com/amuse/ ; code: https://github.com/elianakim/Amuse ; video: https://youtu.be/FbFD3B2OCo8
- **What it is:** A songwriting assistant that turns image, text, or audio "inspirations" into **chord progressions** inside Hookpad (deployed as a Chrome extension alongside Hooktheory's Aria copilot). Pipeline: (1) multimodal LLM (GPT-4o-2024-05-13, T=1.0) extracts *music keywords* from the inspiration — the user can inspect, add or delete keywords (transparent intermediate layer); (2) the LLM is prompted to generate N *diverse* 4-bar progressions (varying root/quality/extensions, diatonic vs chromatic patterns, cadences; Self-BLEU 0.30 vs 0.61 for naive repeated querying); (3) **rejection sampling against a unimodal chord prior**: two LSTMs estimate P(x) (trained on the 50-hour Hooktheory melody/chord dataset from Sheet Sage) and Q(x) (trained on 25,000 GPT-4o-generated progressions); a candidate is accepted iff u < P(x)/(M·Q(x)) with M=7.64 (95th percentile). This sidesteps the absence of paired multimodal↔chord data. Audio inspirations are handled by a separate "Chord Transcriber" (chords extracted from the audio) vs the "Chord Generator" for image/text. Accepted chords paste into the Hookpad editor for playback/editing; users then continue with Aria for melody. Released code covers the chord-generation method (training P/Q, rejection sampling, interactive keyword→chords CLI), not the extension UI; no license file at repo root.
- **Evidence:** Formative interviews N=8 hobbyist songwriters (inspiration from audio 7, narrative 3, visual 2). **User study N=10** (8 hobbyists, 2 professionals; active Hookpad/Aria users), within-subjects Baseline (Aria only) vs Assist (Amuse+Aria), 8-bar chorus in 25 min, Wilcoxon signed-rank: inspiration support 6.20 vs 4.60 (p<.01), task alignment 6.10 vs 4.30 (p=.016), output quality (self-rated) 6.40 vs 5.30 (p=.023); CSI facets controllability 5.80 vs 4.40, collaboration 5.80 vs 3.90, exploration 6.10 vs 4.40, expressiveness 6.00 vs 4.20 (all p<.05); *no* difference in completion time (17.4 vs 17.6 min) or in externally judged composition quality. Usage patterns: kick-start with inspiration (6), ad-hoc inspiration flow (3), lyrics-centred (1). **Listening study N=45** (900 pairwise judgments): Amuse ≈ LSTM prior on coherence, both ≫ raw GPT-4o (p=.009 / 2e-5); Amuse most preferred for keyword relevance (58%, p=.006 vs LSTM). JSD to Hooktheory bigram distribution: prior 0.30, Amuse 0.46, GPT-4o 0.57.
- **Why it matters for the studio:** It is the reference design for *multimodal annotation → symbolic material*: keywords as a human-legible, editable contract between the annotation and the generator; LLM breadth disciplined by a small domain prior; output landing in an editable notation surface. Also a warning: participants expected the *downstream* model (Aria) to know the inspiration context — the studio's annotations must propagate through the whole compile chain, not just one stage.
- **Tags:** [multimodal-input] [image] [text-conditioning] [symbolic-generation] [HCI-study] [co-creation-framework] [creativity-support] [notation] [controllability] [annotation]
- **Verification:** verified (arXiv HTML full text, project page, GitHub README, lab page)
- **BibKey:** kim2025amuse

### HookpadAria — Hookpad Aria: A Copilot for Songwriters
- **Who/where/when:** Chris Donahue, Shih-Lun Wu, Yewon Kim, Dave Carlton, Ryan Miyakawa, John Thickstun; CMU + Hooktheory + Cornell. ISMIR 2024 Late-Breaking Demo (arXiv 2502.08122, Feb 2025). Product beta March 2024, official launch August 2024.
- **Links:** https://arxiv.org/abs/2502.08122 ; product: https://hooktheory.com/hookpad/aria
- **What it is:** Generative copilot integrated into Hookpad, a web lead-sheet editor (melody + harmony, symbolic). Capabilities designed for *non-sequential* workflows: (1) left-to-right continuation, (2) **infilling missing spans in the middle of existing material**, (3) harmony from melody and melody from harmony. Built on the Anticipatory Music Transformer approach (per Donahue's site) trained on Hooktheory's crowd-annotated corpus. Framed explicitly as a "scalable data flywheel for music co-creation".
- **Evidence:** Since March 2024 release: 318k suggestions generated for 3k users, of which 74k accepted into songs (~23% acceptance).
- **Why it matters for the studio:** The nearest existing product to "compose → annotate → compile a part → edit" in a notation editor, with real acceptance telemetry. Its limitation (no multimodal context; Amuse had to be bolted on) marks where the studio should go further.
- **Tags:** [product] [symbolic-generation] [infilling] [notation] [co-creation-framework] [DAW-plugin]
- **Verification:** verified (arXiv abstract; chrisdonahue.com news)
- **BibKey:** donahue2024hookpadaria

### AMT — Anticipatory Music Transformer
- **Who/where/when:** John Thickstun, David Hall, Chris Donahue, Percy Liang; Stanford CRFM. arXiv June 2023; TMLR 2024.
- **Links:** https://arxiv.org/abs/2306.08620 ; code: https://github.com/jthickstun/anticipation ; blog: https://crfm.stanford.edu/2023/06/16/anticipatory-music-transformer.html ; co-composition blog: https://crfm.stanford.edu/2024/08/06/co-composition.html
- **What it is:** "Anticipation": a controllable generative model of an event process conditioned *asynchronously* on a correlated control process, implemented by interleaving control tokens shortly before the events they constrain. For symbolic music the controls are a subset of the notes themselves, so the same model does prompted continuation, **span infilling**, and **accompaniment given a fixed part**. Trained on Lakh MIDI (released checkpoints in several sizes, ~128M–780M per repo — unverified here).
- **Evidence:** Matches autoregressive models on prompted generation; human evaluators rated anticipatory accompaniments similar in musicality to human-composed music over 20-s clips.
- **Why it matters for the studio:** The generative primitive for "compile": the human pins arbitrary notes/parts (the controls), the model fills the remainder; controls can be sparse or dense and live anywhere in time, which is exactly what score-level annotations produce. Underlies Hookpad Aria and MIDInfinite.
- **Tags:** [symbolic-generation] [infilling] [controllability] [accompaniment] [representation]
- **Verification:** verified (arXiv abstract)
- **BibKey:** thickstun2024anticipatory

### Decomposer — Decomposer: Learning to Decompile Symbolic Music to Programs
- **Who/where/when:** Yewon Kim, Apurva Gandhi, David Chung, Graham Neubig, Chris Donahue; CMU. Preprint, July 2026 (arXiv 2607.01849).
- **Links:** https://arxiv.org/abs/2607.01849 ; project: https://yewon-kim.com/decomposer ; code: https://github.com/elianakim/Decomposer ; demo: https://huggingface.co/spaces/haiyewon/decomposer-demo
- **What it is:** Post-training framework that converts MIDI into **executable Strudel programs** (a live-coding music DSL) that re-render the input while exposing repeated patterns, voices, harmony and timing as *editable code*. Base model Qwen3-8B. Stage 1: SFT on **STRUDEL-SYNTH**, 21,174 (Strudel, MIDI) pairs distilled from a frontier LLM (Claude Opus 4.6) and rendered — ~30× the 688 public Strudel programs. Stage 2: RL with execution-based rewards computed from the input MIDI and program alone (so unpaired MIDI can be used): a *faithfulness* reward (render program → compare to input) and a *readability* reward (penalise note-by-note transcription). Users edit the program and re-render.
- **Evidence:** Compile rate 0.99 vs 0.75–0.82 for frontier LLMs; onset F1 on Lakh 0.60 vs 0.27–0.28 (GPT-5.5, Claude Opus 4.6, Gemini 3.5 Flash); multi-instrument onset F1 0.58 vs 0.21–0.23; readability rubric 0.61 (LMD) / 0.74 (Strudel-Synth) vs 0.09 for a heuristic converter and 0.29–0.36 for frontier LLMs; generalises to GigaMIDI, Nottingham, NES-MDB. Ablations show an explicit faithfulness↔readability trade-off and that RL without SFT plateaus. No user study.
- **Why it matters for the studio:** This *is* the "composition as program, compiled by AI" idea, run in the decompile direction: it gives the studio a candidate intermediate representation (structured program) in which human edits are semantic (change a loop, a transposition, a voice) and the compile step is deterministic rendering. Pair with a forward model (program + annotations → new program) to close the loop.
- **Tags:** [music-as-code] [representation] [symbolic-generation] [editing] [structure] [LLM-agent]
- **Verification:** verified (arXiv HTML full text; project page)
- **BibKey:** kim2026decomposer

### MusicControlNet — Music ControlNet: Multiple Time-varying Controls for Music Generation
- **Who/where/when:** Shih-Lun Wu (CMU LTI MS), Chris Donahue (CMU), Shinji Watanabe (CMU LTI), Nicholas J. Bryan (Adobe Research). arXiv Nov 2023; IEEE/ACM TASLP 2024. Basis of Adobe's "Project Music GenAI Control" (Feb 2024). Described in the CMU SCS magazine piece "Expanding Music Generation with Adobe" (Marylee Williams).
- **Links:** https://arxiv.org/abs/2311.07069 ; https://musiccontrolnet.github.io/web/ ; https://magazine.cs.cmu.edu/expanding-music-generation ; Adobe blog: https://blog.adobe.com/en/publish/2024/02/28/adobe-research-audio-creation-editing
- **What it is:** Diffusion model over spectrograms with ControlNet-style adapters giving **time-varying controls** — melody, dynamics, and rhythm curves — alongside text; controls are extracted from training audio and may be *partially specified in time* (e.g., a melody for bars 1–4 only, free elsewhere). The user can supply controls by playing, composing, or literally drawing curves.
- **Evidence:** 49% more faithful to input melodies than MusicGen's melody conditioning with 35× fewer parameters and 11× less training data; two extra control types beyond text+melody.
- **Why it matters for the studio:** The audio-rendering side of the loop: symbolic/drawn annotations (melody line, dynamics envelope, rhythm) steer audio generation, and *partial* specification is exactly the compile-a-region interaction. CMU–Adobe collaboration shows the industry path.
- **Tags:** [audio-generation] [controllability] [sketch] [text-conditioning] [editing] [multimodal-input]
- **Verification:** verified (arXiv page, magazine article, lab page)
- **BibKey:** wu2024musiccontrolnet

### SingSong — SingSong: Generating Musical Accompaniments from Singing
- **Who/where/when:** Chris Donahue, Antoine Caillon, Adam Roberts, Ethan Manilow, Philippe Esling, Andrea Agostinelli, et al. (11 authors); Google Research / Magenta. arXiv Jan 2023 (preprint).
- **Links:** https://arxiv.org/abs/2301.12662 ; examples: https://g.co/magenta/singsong
- **What it is:** Sung vocals in → full instrumental accompaniment out (audio-to-audio). Source separation applied to a large music corpus yields aligned (vocal, instrumental) pairs; AudioLM is adapted for conditional audio-to-audio generation.
- **Evidence:** Listeners significantly preferred SingSong instrumentals over a strong retrieval baseline in pairwise tests (exact percentage not confirmed here).
- **Why it matters for the studio:** Canonical "hum/sing it, get a backing" — the humming/singing annotation modality in the founder's loop, at the audio level.
- **Tags:** [humming] [audio-generation] [accompaniment] [multimodal-input]
- **Verification:** verified (arXiv page; lab page)
- **BibKey:** donahue2023singsong

### SheetSage — Melody Transcription via Generative Pre-training
- **Who/where/when:** Chris Donahue, John Thickstun, Percy Liang; Stanford. ISMIR 2022.
- **Links:** https://arxiv.org/abs/2212.01884 ; code+dataset: https://github.com/chrisdonahue/sheetsage ; examples: https://chrisdonahue.com/sheetsage
- **What it is:** Melody transcription from arbitrary polyphonic recordings using Jukebox representations (from the "JukeMIR" line — Castellon, Donahue, Liang, ISMIR 2021 best-paper runner-up) rather than spectrograms; introduces a **50-hour Hooktheory melody/harmony dataset** from crowd annotations. Integrated with beat, key, and chord estimation into **Sheet Sage**, which outputs human-readable lead sheets from audio.
- **Evidence:** +20% over spectrogram features; +77% relative to prior baselines.
- **Why it matters for the studio:** The "insert example audio → get notation" step, and the dataset that later powers Amuse's prior and Aria's training. Audio→lead-sheet is the entry point for annotating with reference recordings.
- **Tags:** [transcription] [notation] [dataset] [representation] [toolkit]
- **Verification:** verified (arXiv page)
- **BibKey:** donahue2022melody

### PianoGenie — Piano Genie
- **Who/where/when:** Chris Donahue, Ian Simon, Sander Dieleman; Google Magenta/DeepMind. ACM IUI 2019.
- **Links:** https://arxiv.org/abs/1810.05246 ; code: https://github.com/tensorflow/magenta/tree/master/magenta/models/piano_genie ; demo: https://chrisdonahue.com/piano-genie
- **What it is:** Eight-button controller decoded in real time into plausible piano music via an RNN autoencoder with a discrete bottleneck and musically meaningful constraints on the encoder (e.g., contour monotonicity). Non-musicians improvise; used live by The Flaming Lips.
- **Evidence:** Qualitative/user demo; no controlled N reported in abstract.
- **Why it matters for the studio:** Early exemplar of "human gesture is the identity, notes are derived" — low-dimensional human intent expanded by a model, the same shape as sketch/hum → notation.
- **Tags:** [real-time] [expression-performance] [symbolic-generation] [creativity-support] [history]
- **Verification:** verified (arXiv page)
- **BibKey:** donahue2019pianogenie

### LiveMusicAgents — A Design Space for Live Music Agents
- **Who/where/when:** Yewon Kim, Stephen Brade, Alexander Wang, David Zhou, Haven Kim, Bill Wang, Sung-Ju Lee, Hugo Flores García, Cheng-Zhi Anna Huang, Chris Donahue; CMU + KAIST + Google DeepMind. ACM CHI 2026 (arXiv Feb 2026).
- **Links:** https://arxiv.org/abs/2602.05064 ; https://doi.org/10.1145/3772318.3791291 ; https://live-music-agents.github.io
- **What it is:** Survey/design space of **184 systems** (academic literature and videos) for real-time human–AI music collaboration, organised along dimensions of usage context, interaction, technology and ecosystem; released as a public annotated database ("living artifact"). Aims to bridge HCI, AI and computer-music communities.
- **Evidence:** 184 systems coded; framework, no user study.
- **Why it matters for the studio:** Ready-made taxonomy of interaction dimensions to reuse in the studio's own taxonomy (esp. the real-time/accompaniment corner); the database is a citation source.
- **Tags:** [co-creation-framework] [real-time] [accompaniment] [evaluation]
- **Verification:** verified (arXiv abstract; HCII CHI-2026 list)
- **BibKey:** kim2026livemusicagents

### MultiVerse — MultiVerse: A Creator-Centered Approach to Steering Context-Adaptive Lyrics
- **Who/where/when:** Alexander Wang, Chris Donahue, David Lindlbauer; CMU HCII/CSD. ACM UIST 2026 (arXiv Aug 2026).
- **Links:** https://arxiv.org/abs/2608.19350 ; https://doi.org/10.1145/3830398.3830530 ; https://ayw0.github.io/multiverse/
- **What it is:** "C3" creator-centred adaptive-media authoring: songwriters explicitly author *controls* (intent, lyric structure such as rhyme/rhythm placement, locked phrases, audience context) that govern how an LLM adapts lyrics per listener; rule-based validators enforce the controls.
- **Evidence:** N=10 songwriters, MultiVerse vs a prompting workflow; creators preferred explicit constraint authoring, acknowledging flexibility/iteration-speed trade-offs; interviews on authorship and new compositional strategies.
- **Why it matters for the studio:** Same philosophy as the studio — the *creator authors constraints*, the model fills — applied to lyrics; the validator-enforced-controls pattern is a good compile-time check design.
- **Tags:** [co-creation-framework] [controllability] [HCI-study] [text-conditioning]
- **Verification:** verified (arXiv abstract; project page)
- **BibKey:** wang2026multiverse

### MusicArena — Music Arena: Live Evaluation for Text-to-Music
- **Who/where/when:** Yonghyun Kim, Wayne Chi, Anastasios N. Angelopoulos, Wei-Lin Chiang, Koichi Saito, Shinji Watanabe, Yuki Mitsufuji, Chris Donahue; CMU + Sony AI + LMArena. arXiv July 2025; NeurIPS 2025 Creative AI track. Platform launched July 2025.
- **Links:** https://arxiv.org/abs/2507.20900 ; https://music-arena.org ; data: https://huggingface.co/music-arena
- **What it is:** Open platform for live pairwise human-preference evaluation of text-to-music models: users type prompts, hear two outputs, vote; LLM-based routing handles heterogeneous model signatures; collects listening behaviour and free-text feedback; rolling open data releases with privacy guarantees; leaderboard.
- **Evidence:** Platform + protocol paper; blog (Sept 2025) reports first findings.
- **Why it matters for the studio:** Evaluation infrastructure and an open preference dataset; the studio could run its symbolic/arrangement outputs through an Arena-style protocol.
- **Tags:** [evaluation] [audio-generation] [dataset]
- **Verification:** verified (arXiv abstract; lab page)
- **BibKey:** kim2025musicarena

### MAD — Aligning Text-to-Music Evaluation with Human Preferences
- **Who/where/when:** Yichen Huang, Zachary Novack, Koichi Saito, Jiatong Shi, Shinji Watanabe, Yuki Mitsufuji, John Thickstun, Chris Donahue; CMU + UCSD + Sony + Cornell. ISMIR 2025 (arXiv Mar 2025).
- **Links:** https://arxiv.org/abs/2503.16669
- **What it is:** Shows Fréchet Audio Distance is inconsistent and weakly correlated with human judgement; proposes **MAUVE Audio Divergence (MAD)** on self-supervised audio embeddings and releases the **MusicPrefs** human-preference dataset.
- **Evidence:** MAD average rank correlation 0.84 vs FAD 0.49 on synthetic tests; 0.62 vs 0.14 correlation with MusicPrefs.
- **Why it matters for the studio:** A defensible automatic metric for rendered audio during iteration.
- **Tags:** [evaluation] [audio-generation] [dataset]
- **Verification:** verified (arXiv abstract)
- **BibKey:** huang2025aligning

### JLTR — Just Label the Repeats for In-The-Wild Audio-to-Score Alignment
- **Who/where/when:** Irmak Bukey, Michael Feffer, Chris Donahue; CMU. ISMIR 2024.
- **Links:** https://arxiv.org/abs/2411.07428 ; code: https://github.com/irmakbky/jltr-alignment
- **What it is:** Offline alignment of real performance audio to *scanned sheet music*: improved score features (measure detection) and audio features (raw onset probabilities from a transcription model), plus a **clickable UI where the human labels repeat signs and jumps** instead of relying on automatic detection.
- **Evidence:** Measure-level alignment accuracy 33% → 82% (150% relative) over prior methods.
- **Why it matters for the studio:** Concrete evidence that a tiny, well-chosen human annotation beats automation; also the plumbing for aligning reference recordings to the score the composer is editing.
- **Tags:** [annotation] [notation] [transcription] [structure] [HCI-study]
- **Verification:** verified (arXiv page)
- **BibKey:** bukey2024justlabel

### SynTheory — Do Music Generation Models Encode Music Theory?
- **Who/where/when:** Megan Wei, Michael Freeman, Chris Donahue, Chen Sun; Brown + CMU. ISMIR 2024.
- **Links:** https://arxiv.org/abs/2410.00872 ; https://brown-palm.github.io/music-theory ; code: https://github.com/brown-palm/syntheory
- **What it is:** SynTheory, a synthetic MIDI+audio dataset isolating tempo, time signature, notes, intervals, scales, chords and progressions; probes Jukebox and MusicGen representations layer-by-layer for these concepts.
- **Evidence:** Theory concepts are linearly detectable; detectability varies by model size and layer.
- **Why it matters for the studio:** A method to check whether a chosen backbone "understands" the symbolic concepts the composer annotates with.
- **Tags:** [theory-analysis] [evaluation] [dataset] [representation]
- **Verification:** verified (arXiv page)
- **BibKey:** wei2024musictheory

### ReaLchords — Adaptive Accompaniment with ReaLchords
- **Who/where/when:** Yusong Wu, Tim Cooijmans, Kyle Kastner, Adam Roberts, Ian Simon, et al. incl. Chris Donahue, Cheng-Zhi Anna Huang; Google DeepMind + Mila. ICML 2024.
- **Links:** https://proceedings.mlr.press/v235/wu24c.html ; https://storage.googleapis.com/realchords/index.html
- **What it is:** Online model that improvises **chord accompaniment to a live user melody**: MLE-pretrained online model fine-tuned with RL using a harmonic/temporal-coherence reward plus distillation from an offline teacher that sees the future melody. Successor ReaLJam (2025) adds a jamming UI.
- **Evidence:** Quantitative metrics and listening tests show adaptation to unfamiliar inputs.
- **Why it matters for the studio:** Real-time harmonic co-creation in the symbolic domain; the offline-teacher-to-online-student trick is relevant to any latency-bound compile step.
- **Tags:** [real-time] [accompaniment] [symbolic-generation] [mixed-initiative]
- **Verification:** verified (PMLR page)
- **BibKey:** wu2024realchords

### MagentaRT — Live Music Models (Magenta RealTime / Lyria RealTime; Magenta RealTime 2)
- **Who/where/when:** Lyria Team, Google DeepMind (Caillon, McWilliams, Tarakajian, Simon, Manco, Engel, … Donahue, Han, Roberts; 30+ authors). arXiv Aug 2025 (2508.04651); Magenta RealTime open weights June 2025; Magenta RealTime 2 (MRT2) released later with 230M and 2.4B parameter models.
- **Links:** https://arxiv.org/abs/2508.04651 ; code: https://github.com/magenta/magenta-realtime (Apache-2.0) ; weights: https://huggingface.co/google/magenta-realtime-2 ; https://magenta.withgoogle.com/mrt2
- **What it is:** "Live music models" generate a continuous 48 kHz stereo stream in chunks, each steered by prior audio and a style embedding (MusicCoCa text/audio embedding; SpectroStream codec; Depthformer). MRT2 adds real-time streaming on Apple Silicon, an AUv3 DAW plugin, standalone app, and "Jam" note/chord control (hold a chord, the ensemble follows the harmony), plus Max/PD/SuperCollider bindings. Lyria RealTime is the hosted variant (≤2 s control latency).
- **Evidence:** Open-weights release; engineering benchmarks (real-time on M1 Air for 230M).
- **Why it matters for the studio:** The current open, DAW-pluggable real-time audio backbone with harmonic (note) steering — a candidate renderer for "compile this section and let me steer it live".
- **Tags:** [audio-generation] [real-time] [DAW-plugin] [controllability] [product]
- **Verification:** verified (GitHub README/docs; arXiv abstract; magenta page) — MRT1 800M size from recall (unverified)
- **BibKey:** lyria2025livemusic

### MIDInfinite — Local Deployment of Large-Scale Music AI Models on Commodity Hardware
- **Who/where/when:** Xun Zhou, Charlie Ruan, Zihe Zhao, Tianqi Chen, Chris Donahue; CMU. ISMIR 2024 LBD.
- **Links:** https://arxiv.org/abs/2411.09625 ; demo: https://rickzx.github.io/inf-music
- **What it is:** Ports the Anticipatory Music Transformer to the browser via MLC (WebGPU); infinite MIDI stream demo.
- **Evidence:** 51 notes/s on an M3 MacBook Pro; faster than playback 72.9% of the time, 86.3% with 2-s buffering.
- **Why it matters for the studio:** Proof that a symbolic infilling model can run client-side — relevant to an open-source studio's deployment story.
- **Tags:** [toolkit] [symbolic-generation] [real-time]
- **Verification:** verified (arXiv page)
- **BibKey:** zhou2024midinfinite

### UnifiedScoreTranslation — Unified Cross-modal Translation of Score Images, Symbolic Music, and Performance Audio
- **Who/where/when:** Jongmin Jung, Dongmin Kim, Sihun Lee, Seola Cho, Hyungjoon So, Irmak Bukey, Chris Donahue, Dasaem Jeong; Sogang University + CMU. arXiv May 2025; IEEE/ACM TASLP (Dec 2025 per Donahue's news).
- **Links:** https://arxiv.org/abs/2505.12863
- **What it is:** One encoder–decoder Transformer with unified tokenisation of score images, MusicXML, MIDI and audio, trained multitask on the new **YouTube Score Video (YTSV)** dataset (>1,300 h of aligned score-image/audio, ~10× prior datasets).
- **Evidence:** OMR symbol error rate 24.58% → 13.67% (SOTA); first score-image-conditioned audio generation.
- **Why it matters for the studio:** Cross-modal bridge among the studio's core representations (scanned/handwritten score ↔ symbolic ↔ audio) — including a path from a *photographed sketch of notation* to symbolic.
- **Tags:** [representation] [transcription] [notation] [audio-generation] [dataset] [multimodal-input]
- **Verification:** verified (arXiv HTML)
- **BibKey:** jung2025unified

### MusicAwareVA — Towards Music-Aware Virtual Assistants
- **Who/where/when:** Alexander Wang, David Lindlbauer, Chris Donahue; CMU HCII/CSD. ACM UIST 2024.
- **Links:** https://doi.org/10.1145/3654777.3676416 ; https://ayw0.github.io/publications/2024-MVA/
- **What it is:** Spoken notifications are re-sung in harmony with the currently playing music (lyrics replaced by the alert), instead of muting playback.
- **Evidence:** User study: musical assistant fit music better, less intrusive, more delightful than standard (N not captured).
- **Why it matters for the studio:** Peripheral; shows the HCII–G-CLef pairing and a "generate-to-fit-existing-music" constraint problem.
- **Tags:** [HCI-study] [audio-generation] [accompaniment]
- **Verification:** verified (project page)
- **BibKey:** wang2024musicaware

### RISE — RISE: Adaptive Music Playback for Realtime Intensity Synchronization with Exercise
- **Who/where/when:** Alexander Wang (Michigan/CMU), Chris Donahue (CMU), Dhruv Jain (Michigan). ISMIR 2025 (Daejeon).
- **Links:** https://gclef-cmu.org/static/pdfs/2025rise.pdf
- **What it is:** Estimates intense song segments (structure analysis + drum-stem loudness), finds cutpoints via recurrence matrices, and a state machine loops/skips segments in real time to align music energy with workout intervals.
- **Evidence:** 6 raters on 514 clips: transition naturalness 4.3/5 vs 4.5/5 unmodified (n.s.); N=12 users, 11/12 preferred adaptive.
- **Why it matters for the studio:** Structure-aware *rearrangement* of existing audio by cut-points — a form of non-destructive audio editing on musical structure.
- **Tags:** [structure] [editing] [real-time] [HCI-study]
- **Verification:** verified (PDF)
- **BibKey:** wang2025rise

### FM4Music — Foundation Models for Music: A Survey
- **Who/where/when:** Yinghao Ma, Anders Øland, Anton Ragni, et al. (40+ authors incl. Chris Donahue, Roger Dannenberg, Shuqi Dai, Shih-Lun Wu); QMUL-led. arXiv 2024.
- **Links:** https://github.com/nicolaus625/FM4Music ; PDF: https://gclef-cmu.org/static/pdfs/2024mafoundation.pdf
- **What it is:** Broad survey of music foundation models (representations, pretraining, adaptation, evaluation, ethics), with both CMU generations as co-authors.
- **Evidence:** —
- **Why it matters for the studio:** Background reading; taxonomy source for the audio/representation side.
- **Tags:** [representation] [evaluation] [ethics-legal]
- **Verification:** partial (lab page listing; arXiv id from recall)
- **BibKey:** ma2024foundation

### CMU-Udio-2026 — "Generative AI and Musical Creativity" (CMU news, Jan 30 2026: "As AI-Generated Music Advances, Humans Still Lead in Creativity")
- **Who/where/when:** Jose Oros (PhD student, Information Systems, Heinz College), Rahul Telang (Trustees Professor of IS, Heinz), Richard Randall (Assoc. Prof. of Music Theory, School of Music). Poster #18, Conference on Digital Experimentation (CODE@MIT), Nov 14–15 2025. CMU news story by Stacey Federoff, Jan 30 2026 (Heinz repost Feb 2026; phys.org Feb 2026). **No paper, preprint or SSRN working paper is public as of Sept 2026**; Oros was to defend in May 2026. *Not* a Donahue/G-CLef study.
- **Links:** https://www.cmu.edu/news/stories/archives/2026/january/as-ai-generated-music-advances-humans-still-lead-in-creativity-cmu-research-finds ; https://www.heinz.cmu.edu/media/2026/February/as-ai-generated-music-advances-humans-still-lead-in-creativity-cmu-research-finds ; https://ide.mit.edu/events/2025-conference-on-digital-experimentation-mit-codemit/
- **What it is:** Randomised experiment: **140 musically trained participants** each composed a **15-second melody on a small piano keyboard**; a randomly selected treatment group could use **Udio** (text-prompt music generator) to generate tunes "for inspiration", the control group composed unaided. All melodies were then rated by a **separate group of listeners on creativity, enjoyment and musicality**.
- **Evidence:** Reported claims (verbatim from the article): AI-assisted melodies "were slower, used fewer notes and were judged by listeners as less creative." The article does not disambiguate "slower" (tempo vs. composition time), does not report effect sizes, rater N, or which of enjoyment/musicality differed significantly. Quotes: Oros — "We're trying to understand how these tools shape music and if they can support creative ideation when composing songs"; "A lot of studies on the effect of AI focus on productivity, but creativity and novelty are central outcomes." Randall — "Humans create music out of their own personal experiences and inspirations, and that resonates." Telang raised training-corpus/copyright concerns.
- **Why it matters for the studio:** Direct empirical support for the founder's rejection of text-to-full-song as *the* creative paradigm: Udio-as-inspiration in a composition task made output less creative by listener judgement. It is also a caution: the AI condition was a *prompt-to-audio* tool bolted beside a keyboard, not an integrated symbolic co-creator — the studio should be evaluated with the same design (randomised, blind raters) to show the difference. Treat numbers as preliminary until the paper appears.
- **Tags:** [HCI-study] [evaluation] [creativity-support] [ethics-legal]
- **Verification:** verified (CMU + Heinz articles, CODE@MIT programme fetched); underlying paper unverified/unpublished
- **BibKey:** oros2025generativeai

### Dannenberg1984 — An On-Line Algorithm for Real-Time Accompaniment
- **Who/where/when:** Roger B. Dannenberg; CMU. Proc. International Computer Music Conference 1984 (Paris), pp. 193–198.
- **Links:** https://www.cs.cmu.edu/~rbd/bib.html (bibliography); PDF via https://www.cs.cmu.edu/~rbd/papers/
- **What it is:** First practical score-following/computer-accompaniment system: dynamic-programming match of a live monophonic performance against a stored score, with tempo estimation driving accompaniment playback in real time (contemporaneous with Vercoe's Synthetic Performer).
- **Evidence:** Demonstrated live with trumpet; foundational, widely cited.
- **Why it matters for the studio:** Origin of "the human leads, the machine follows the score" — the historical anchor for accompaniment/real-time modes and for treating the score as the shared contract.
- **Tags:** [history] [accompaniment] [real-time] [notation]
- **Verification:** verified (author bibliography)
- **BibKey:** dannenberg1984online

### HCMP — Human-Computer Music Performance (HCMP) programme
- **Who/where/when:** Roger B. Dannenberg with Nicolas E. Gold, Dawen Liang, Guangyu Xia (and others); CMU. "Human-Computer Music Performance: From Synchronized Accompaniment to Musical Partner" (SMC 2013); "Methods and Prospects for Human-Computer Music Performance of Popular Music" and "Active Scores: Representation and Synchronization in HCMP of Popular Music" (Computer Music Journal 38(2), 2014); "HCMP: A Brief History and Future Prospects" (JASA 2014).
- **Links:** https://www.cs.cmu.edu/~rbd/bib.html ; https://www.cs.cmu.edu/~music/cmp/
- **What it is:** Framework for computers as *performing partners* in popular music (bands, not soloist + accompaniment): beat/section-level synchronisation, "active scores" (machine-readable, structure-aware scores that can be re-sequenced live, with repeats/cues), and roles for human cueing. Later offshoots: Xia's improvised duet interaction (NIME 2017), Accomplice (current keyboard accompaniment project), Arco (ICMC 2025), O2 networking (CMJ 2022).
- **Evidence:** System papers and performances; no large N studies.
- **Why it matters for the studio:** "Active scores" are an early structured-score representation designed for both humans and machines to edit and follow — a direct ancestor of an annotated, compilable score.
- **Tags:** [history] [accompaniment] [real-time] [structure] [notation] [representation]
- **Verification:** verified (author bibliography)
- **BibKey:** dannenberg2014hcmp

### Nyquist-Audacity — Nyquist (composition/synthesis language) and Audacity (editor)
- **Who/where/when:** Roger B. Dannenberg, "Machine Tongues XIX: Nyquist, a Language for Composition and Sound Synthesis", Computer Music Journal 21(3), 1997 (also "The Nyquist Composition Environment", ICMC 2008). Dominic Mazzoni & Roger B. Dannenberg, "A Fast Data Structure for Disk-Based Audio Editing", Computer Music Journal 26(2), 2002 — the Audacity architecture paper; Audacity was begun at CMU in 1999–2000 by Mazzoni and Dannenberg.
- **Links:** https://www.cs.cmu.edu/~music/nyquist ; https://www.audacityteam.org/ ; https://www.cs.cmu.edu/~rbd/bib.html
- **What it is:** Nyquist: a Lisp/SAL-based language in which *scores are programs* (behaviours, transformations, temporal combinators like `sim`/`seq`) — music-as-code lineage. Audacity: the dominant open-source audio editor (Nyquist is its plug-in scripting language).
- **Evidence:** Decades of use; Audacity is among the most downloaded open-source audio tools.
- **Why it matters for the studio:** Both are CMU precedents for the founder's two pillars — music as compilable program (Nyquist) and open-source editing infrastructure (Audacity); also shows that a scripting language embedded in an editor is a viable extension surface.
- **Tags:** [music-as-code] [toolkit] [history] [editing] [product]
- **Verification:** verified (author bibliography)
- **BibKey:** dannenberg1997nyquist

### MusicFrameworks — Controllable Deep Melody Generation via Hierarchical Music Structure Representation
- **Who/where/when:** Shuqi Dai, Zeyu Jin, Celso Gomes, Roger B. Dannenberg; CMU + Adobe. ISMIR 2021.
- **Links:** https://arxiv.org/abs/2109.00663
- **What it is:** "MusicFrameworks": a hierarchical representation with **section- and phrase-level structure**, a *basic melody* (skeleton), rhythm structure and chords; two Transformer networks generate rhythm and basic melody, then a third generates the final melody autoregressively conditioned on them. Users can **alter chords, basic melody, and rhythm structure** to customise or vary a piece — long-form generation with explicit, editable structure.
- **Evidence:** Listening test against POP909 human melodies: generated melodies rated as good as or better than human-composed ~half the time.
- **Why it matters for the studio:** A concrete, editable structural skeleton (section/phrase/basic melody/rhythm/chords) — exactly the intermediate "annotation layer" a composer edits before the AI compiles the surface.
- **Tags:** [symbolic-generation] [structure] [controllability] [representation] [editing]
- **Verification:** verified (arXiv page)
- **BibKey:** dai2021controllable

### WhatIsMissing — What Is Missing in Deep Music Generation? A Study of Repetition and Structure in Popular Music
- **Who/where/when:** Shuqi Dai, Huiran Yu, Roger B. Dannenberg; CMU. ISMIR 2022.
- **Links:** https://arxiv.org/abs/2209.00182 ; PDF: https://www.cs.cmu.edu/~rbd/papers/repetition-ismir2022.pdf
- **What it is:** Analysis of two pop datasets (Chinese and American) establishing four principles: hierarchical structure levels; song-specific repetition with limited vocabulary; interaction between structure and rhythm/melody/harmony; non-random repetition trends measurable via cross-entropy. Music from recent deep generators is analysed with the same tools and "often reveals striking differences from a structural perspective."
- **Evidence:** Corpus statistics; comparison of generated vs human music on repetition/structure metrics.
- **Why it matters for the studio:** Supplies the structural metrics and the argument that structure must be an explicit, human-controllable layer rather than an emergent hope.
- **Tags:** [theory-analysis] [structure] [evaluation] [corpus]
- **Verification:** verified (arXiv page)
- **BibKey:** dai2022missing

### PersonalisedImitation — Personalised Popular Music Generation Using Imitation and Structure
- **Who/where/when:** Shuqi Dai, Xichu Ma, Ye Wang, Roger B. Dannenberg; CMU + NUS. Journal of New Music Research 51(1), 2022 (published 2023). arXiv 2021.
- **Links:** https://doi.org/10.1080/09298215.2023.2166848
- **What it is:** Statistical-ML system that *imitates* a chosen reference song's structure, melody, chord progression and bass style to generate a new personalised song — structure analysis first, then generation constrained to the analysed template; explicitly designed so a user can pick what to imitate.
- **Evidence:** Subjective evaluation (details not fetched; publisher page blocked).
- **Why it matters for the studio:** "Insert example audio/score as annotation → imitate its structure" is one of the founder's core interactions; this is a symbolic-domain precedent.
- **Tags:** [symbolic-generation] [structure] [style-transfer] [controllability]
- **Verification:** partial (bibliography + search snippets; publisher page 403)
- **BibKey:** dai2023personalised

### StructureInterconnections — The Interconnections of Music Structure, Harmony, Melody, Rhythm, and Predictivity
- **Who/where/when:** Shuqi Dai, Huan Zhang, Roger B. Dannenberg; CMU. Music & Science vol. 7, 2024 (extends "Automatic Analysis and Influence of Hierarchical Structure on Melody, Rhythm and Harmony in Popular Music", CSMC-MuMe 2020). Dai's PhD (CMU CS, advisor Dannenberg, completed 2024) centres on this structure work plus singing (SingStyle111, ISMIR 2023; ExpressiveSinger, ACM MM 2024).
- **Links:** https://doi.org/10.1177/20592043241234758 ; https://www.shuqid.net/
- **What it is:** Algorithms extracting two-level (section/phrase) repetition structure from 909 Chinese pop MIDI transcriptions, then quantifying how structural position conditions harmony, pitch distributions, rhythm and predictability.
- **Evidence:** 93% phrase-boundary accuracy; repeated phrases cover 50–90% of most songs; V–I at section ends 94% vs 47% elsewhere; entropy lower at boundaries; 2–3 sections per song with 1–6 phrases each.
- **Why it matters for the studio:** Ready-made structure analyser and priors for a "structure view" of a composition, and for compile-time sanity checks (e.g., cadence placement).
- **Tags:** [theory-analysis] [structure] [corpus] [representation]
- **Verification:** verified (journal page)
- **BibKey:** dai2024interconnections

### ExpressEdit — ExpressEdit: Video Editing with Natural Language and Sketching
- **Who/where/when:** Bekzat Tilekbay, Saelyne Yang, Michal Lewkowicz (Yale), Alex Suryapranata, Juho Kim; KAIST KIXLAB (+ Yale). ACM IUI 2024 (also HAI-GEN 2024 workshop). **Not CMU.**
- **Links:** https://arxiv.org/abs/2403.17693 ; https://doi.org/10.1145/3640543.3645164 ; https://expressedit.kixlab.org/ ; code: https://github.com/fesiib/video-editing-pipeline ; demo video: https://youtu.be/t16Se9rNLLQ
- **What it is:** Editing informational videos by **describing an edit in natural language and sketching on a video frame** (rectangles/free-form marks marking regions) — the timeline is used for positional references and for adjusting results. Pipeline: GPT-4 **parses the command into four reference types — temporal ("whenever he discusses tips"), spatial ("top-left", or the sketch), edit operation, and parameters**; temporal references are resolved positionally (timecodes), against the transcript, or against dense visual captions (BLIP-2/InternVideo) via SentenceTransformer similarity (top-10 segments); spatial references are resolved by Segment-Anything instance crops matched to the text/sketch in CLIP space; operation/parameter references handle explicit, relative and abstract directives. Output is a set of **edit suggestions** (7 operations: text, image, shape, cut, zoom, crop, blur) the user can accept, reject, or manually adjust (span on timeline, position/size on canvas, parameters), with an **"Examine" panel** showing how each reference was interpreted.
- **Evidence:** Formative study N=10 editors, 176 multimodal edit requests (all had NL; 78/97 visual ones were sketches on frames). Pipeline accuracy on 50 ground-truth commands: temporal recall 0.68, spatial mIoU 0.56, operation F1 0.82. User study N=10 novices, 40-min task: 5.2 multimodal commands, 9.3 requests incl. iterations, 16.6 final edits; **45.98% of suggestions accepted; 58.09% of final edits were modified suggestions**; time split ~31% ideating/describing, 33% examining, 35% manual editing; SUS 75.7; creativity support 5.7/7; Examine feature rated 6.1/7. Sketches appeared in 26% of commands and simplified spatial specification; vague commands failed; users wanted animation/transitions/audio ops and multi-frame sketching.
- **Why it matters for the studio:** The best worked template for **multimodal annotation-driven editing**: a *reference-type grammar* (when / where / what / how) that a music version can copy almost verbatim (temporal → bars/beats/sections or "the second time the chorus comes", spatial → staff/voice/register, operation → reharmonise/thin/transpose/add counter-line, parameters → "brighter", "like the reference clip"); resolvers per modality (score search, audio-similarity for example clips, sketch → contour/region); and — crucially — *inspectable, editable suggestions* rather than silent rewrites. No music-specific ExpressEdit exists yet; the closest music analogues are Draw and Listen! (sketch→melody inpainting, below) and Amuse (multimodal→chords, no sketch, no spatial targeting).
- **Tags:** [annotation] [sketch] [multimodal-input] [editing] [LLM-agent] [HCI-study] [video] [mixed-initiative]
- **Verification:** verified (arXiv HTML full text; project page)
- **BibKey:** tilekbay2024expressedit

### REAL — REAL Pipeline (GitHub: This-Goober/REAL)
- **Who/where/when:** GitHub user "This-Goober" (self-described two-person student team; the account's other repos are music-related — "ré.ai", a personal site of a young violinist, and "TUNE", a violin-intonation pitch-analysis "skill"). Public repo, MIT licence, 0 stars; batch-1 field sessions dated 2026-08. **No acronym expansion is given anywhere in the repo; no paper exists.**
- **Links:** https://github.com/This-Goober/REAL ; demo video: https://www.youtube.com/watch?v=Oz6rBUQU4j8 ; live storyboard demo: https://this-goober.github.io/REAL/skills/batch-1/outputs/STORYBOARD-segment.html
- **What it is:** An AI-assisted **video** (not music) editing pipeline implemented as four **Claude skills** (Claude apps / Claude Code) whose stance is "an AI agent acting as a production crew for a human director … the human makes every creative call; the agent does the bookkeeping and refuses to guess." Steps: `/real-brainstorm` (idea/script → NOTEBOOK.md + SHOTLIST.md), `/real-create-catalogue` (footage folder → approved renames + `asset-catalog.json`, with dHash near-duplicate detection that *asks the creator* in the uncertain band), `/real-storyboarding` (→ interactive review page + `reel.json`, the single authoritative edit; every timing badged `estimated` or `measured`), `/real-compile` (`reel.json` → validated `.fcpxml` for Final Cut Pro; "zero editorial decisions"). Core idea: **word anchors** — "the word is the identity, the timestamp is derived": placements are pinned to spoken words and timestamps are re-derived at compile time from a measured clock (ffmpeg `silencedetect` on the narration; forced alignment planned). Requires macOS + Final Cut Pro, Python 3.10+, ffmpeg; rendering is deliberately out of scope (output is an editable timeline). Status: batch 1 field-tested on real reels; batch 2 rebuilt, 21/21 synthetic regression checks; a "capability journal" with one entry (word-anchor snapping).
- **Evidence:** Self-reported measurements only: estimated clock 7% long overall but 28% long on one beat; cue offsets of −1.7 s / −1.05 s under estimation; 22 placements silently dropped by a batch-1 translator; cloud connectors ~350k tokens/MB. Key stated finding: "A random error looks like noise. A coherent error reads as an editorial fact."
- **Why it matters for the studio:** Not a research contribution and not about music, but a vocabulary and architecture twin of the founder's loop (brainstorm → catalogue → storyboard → **compile**, human as director, agent as crew) built on the same agentic tooling the studio might use. Transferable design rules: one owner per decision; one authoritative machine-readable artefact (`reel.json` ↔ an annotated score file); anchors on semantic events (word ↔ beat/bar/note) with derived timing; loud refusal on anything not representable; badge estimated vs measured. If the founder listed it as *music* related, that is a misattribution — only the owner's sibling repos (TUNE) are musical.
- **Tags:** [LLM-agent] [video] [editing] [toolkit] [co-creation-framework] [product]
- **Verification:** verified (README, journal, gap report fetched raw; GitHub profile)
- **BibKey:** thisgoober2026real

### DrawAndListen — Draw and Listen! A Sketch-Based System for Music Inpainting
- **Who/where/when:** Christodoulos Benetatos, Zhiyao Duan; University of Rochester (AIR Lab). TISMIR 5(1):141–155, 2022. **Not CMU** — included as the music-specific sketch-editing analogue to ExpressEdit.
- **Links:** https://doi.org/10.5334/tismir.128 ; https://labsites.rochester.edu/air/projects/DrawAndListen.html
- **What it is:** Fill missing measures of a monophonic melody from **hand-drawn curves**: a pitch-contour curve and a note-density (rhythm) curve, plus pitch/rhythm offset sliders; a multi-encoder/decoder VAE disentangles relative pitch, relative rhythm and surrounding context.
- **Evidence:** Objective + subjective evaluation on the Irish folk dataset (24,065 tunes); beats rule-based and genetic baselines on musicality and fidelity to the sketch; users without notation knowledge found it intuitive.
- **Why it matters for the studio:** Demonstrates "scribble on the notation → infill" in the symbolic domain — the sketch modality of the founder's loop — but only for monophonic melody and without NL or audio annotations; combining it with ExpressEdit's grammar is open territory. (Related but unverified: "MIDI-Draw: Sketching to Control Melody Generation", 2023.)
- **Tags:** [sketch] [infilling] [symbolic-generation] [HCI-study] [annotation]
- **Verification:** verified (journal page)
- **BibKey:** benetatos2022drawlisten

### MuskitsESPnet — Muskits-ESPnet: A Comprehensive Toolkit for Singing Voice Synthesis in New Paradigm
- **Who/where/when:** Yuning Wu, Jiatong Shi, et al., Shinji Watanabe, Qin Jin; CMU WAVLab + Renmin University. ACM Multimedia 2024 (open-source software track); successor to Muskits (Interspeech 2022).
- **Links:** https://arxiv.org/abs/2409.07226 ; https://doi.org/10.1145/3664647.3685000 ; code: https://github.com/espnet/espnet
- **What it is:** ESPnet-based singing-voice-synthesis toolkit: score/lyrics → singing, with continuous (SSL) and discrete (codec) pretrained-audio paradigms, multiple score input formats, **automatic music-score correction**, and perception-based auto-evaluation. Watanabe's group otherwise touches music mainly through co-authorship (Music ControlNet, Music Arena, MAD) and the Sony collaboration. Note: **MuQ** (self-supervised music representation with Mel-RVQ, TASLP 2025) is Tencent AI Lab / SJTU, *not* CMU.
- **Evidence:** Toolkit paper; recipes/benchmarks rather than user studies.
- **Why it matters for the studio:** The open-source path from a symbolic vocal line + lyrics to a rendered vocal — the "render this part" compile step for voice.
- **Tags:** [toolkit] [audio-generation] [notation] [transcription]
- **Verification:** partial (arXiv abstract fetched; author list from recall/search snippet)
- **BibKey:** wu2024muskitsespnet

### JukeMIR — Codified Audio Language Modeling Learns Useful Representations for Music Information Retrieval
- **Who/where/when:** Rodrigo Castellon, Chris Donahue, Percy Liang; Stanford. ISMIR 2021 (Best Paper runner-up).
- **Links:** https://arxiv.org/abs/2107.05677 ; code: https://github.com/p-lambda/jukemir
- **What it is:** Shows OpenAI Jukebox's intermediate representations transfer to MIR tasks (tagging, genre, key, emotion), beating spectrogram and prior pretrained features — the "Jukebox-era" result that seeded Sheet Sage and SynTheory.
- **Evidence:** State-of-the-art or competitive on four MIR benchmarks with linear probes.
- **Why it matters for the studio:** Justifies using large generative-audio backbones as analysis features when the composer inserts example audio.
- **Tags:** [representation] [transcription] [evaluation]
- **Verification:** partial (publication list; abstract not fetched)
- **BibKey:** castellon2021codified

### CMU-Other — Other CMU music/creativity pointers (brief)
- **Who/where/when:** CMU School of Music "Music & Technology" programme (BS/MS; faculty incl. Richard Randall, Jesse Stiles; historical thesis projects incl. Zeyu Jin's "Formal Semantics for Music Notation Control Flow" → Live Score Display); HCII (Lindlbauer, Forlizzi/Holstein) — music-specific work found only via Alexander Wang's papers with Donahue; Bhiksha Raj's group — no music-generation or music-editing system located in this pass (co-author with Dannenberg on "Artificial Creative Intelligence: Breaking the Imitation Barrier", ICCC 2020); Dannenberg's current project list (Spring 2025): O2, AMADS symbolic-music-analysis library, Arco, Accomplice (keyboard accompaniment), Soundcool web port, "Computer Music Archeology", "Music Patterns and Music Models".
- **Links:** https://www.cmu.edu/cfa/music/programs/music-technology/ ; https://www.cs.cmu.edu/~rbd/projects-spring2025.html
- **What it is:** Institutional context; AMADS (analysis algorithms for key, contour, chord labelling) and Accomplice are the live Dannenberg-side codebases.
- **Evidence:** —
- **Why it matters for the studio:** Identifies which CMU groups actually do music (G-CLef, Dannenberg/Dai lineage, WAVLab for singing) and which the founder can skip.
- **Tags:** [history] [toolkit] [theory-analysis]
- **Verification:** partial (pages fetched; Raj/HCII negative result from limited search)
- **BibKey:** cmu2025musictech
