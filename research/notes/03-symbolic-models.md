# 03 — Symbolic music models: representations, generation, infilling, editing and control

## Overview

Symbolic music generation (MIDI / score / lead-sheet / ABC / piano-roll) is the technical core of a symbolic-first studio because its outputs are directly readable and editable by a composer. Since 2016 the field has moved through four representational families — MIDI-like performance events (Music Transformer), metrically structured event tokens (REMI, Compound Word, Octuple, MMM's per-track bars), text-native score notation (ABC, used by folk-rnn and now by every "music LLM": ChatMusician, MuPT, NotaGen, MelodyT5), and image-like piano rolls used by diffusion models (Polyffusion, whole-song cascaded diffusion, GETMusic's GETScore) — and through three task framings: continuation from scratch, attribute/text-conditioned generation (FIGARO, MuseCoco, Text2midi, MIDI-LLM), and **infilling/inpainting of an existing piece** (Coconet, MMM, Composer's Assistant, Anticipatory Music Transformer, MIDI-GPT, MIDI-RWKV, Polyffusion). A converging control vocabulary has emerged — per-track instrument, note density (horizontal/vertical), polyphony, pitch range, duration range, chords, section labels, style/genre — applied at track and bar granularity. In parallel, Gus Xia's Music X Lab has built a "lead sheet → piano arrangement → orchestration" pipeline (AccoMontage, Q&A, structured arrangement, whole-song hierarchical generation) that is the closest existing analogue to the founder's "compile" metaphor, and expressive-performance rendering (VirtuosoNet, ScorePerformer/PianoFlow, DExter, MIDI-DDSP, RenderBox) has matured into a separable score→performance→audio stage. 2025–2026 state of the art is dominated by (a) scaled ABC LLMs with RL fine-tuning (NotaGen), (b) large transcribed datasets (Aria-MIDI, 1M piano files; MetaScore, 963K MuseScore files; GigaMIDI), (c) small deployable infilling models with rich controls (MIDI-GPT shipped in Cubase, MIDI-RWKV), and (d) LLM adaptation for text-to-MIDI (MIDI-LLM, ISMIR 2026). Benchmarks (ZIQI-Eval, ABC-Eval, MusicTheoryBench) show general-purpose LLMs still reason poorly about symbolic music, and direct MusicXML/MEI generation remains almost unexplored.

## Key takeaways for the studio

- **Infilling is the primitive that implements "edit → compile".** Mask-and-regenerate at (track × bar) granularity exists in mature form: MMM/MIDI-GPT (bar- and track-level, 128 GM instruments), Composer's Assistant 1/2 (REAPER, arbitrary track-measures, ~10 fine-grained controls), MIDI-RWKV (long context, personalisable, runs on edge), Anticipatory Music Transformer (fix any subset of notes as "controls" and fill the rest), Polyffusion/GETMusic (arbitrary piano-roll masks). Design the studio's data model so any region can be marked "regenerate" while everything else is a hard constraint.
- **Control vocabulary is converging and should be the studio's annotation schema.** Instrument, horizontal/vertical note-onset density, polyphony, pitch range/mean pitch, duration range, chord per beat, section/form label, tempo, style/genre (FIGARO, MusIAC, Composer's Assistant 2, MIDI-GPT, SymPAC prompt bars, MuseCoco's 12 attributes). These are exactly the things a composer would "annotate" on a score.
- **Representation choice depends on the layer.** Event tokens (REMI/CP/Octuple/MMM; all in MidiTok) for MIDI-performance data; ABC text for score-level content and LLM compatibility (ChatMusician, MuPT's synchronized multi-track SMT-ABC, NotaGen, MelodyT5); piano-roll for diffusion inpainting. **No verified system generates MusicXML/MEI directly** — MetaScore (MuseScore-sourced) converts to REMI+/MMT — so a MusicXML↔ABC/token bridge is a required engineering component and an open research gap.
- **Hierarchical "compile" pipelines already exist and should be studied as architecture templates:** whole-song cascaded diffusion (form → phrase/key → reduced lead sheet → lead sheet → accompaniment, each level human-editable), MusicFrameworks (section/phrase → basic melody → rhythm → melody), and Music X Lab's lead sheet → piano texture → orchestral function pipeline (AccoMontage → Q&A → Structured Arrangement, NeurIPS 2024).
- **The lead sheet is the natural human-authored "source code".** Harmonization with hard chord constraints (B* search), accompaniment from lead sheets (AccoMontage 1/2), lead-sheet generation with LLMs (MIDI-LLM in-the-wild study, 58 musicians), and prompt-bar conditioning (SymPAC) all treat melody+chords as the interface.
- **Training-free guidance lets new constraints be added without retraining** (Stochastic Control Guidance for non-differentiable rules, ICML 2024; LC-Diff plug-in latent constraints, ISMIR 2025). This is the right mechanism for annotation-driven steering where the set of annotations will grow over time.
- **LLMs are strong at ABC generation when specialised, weak at symbolic reasoning in general.** NotaGen/MuPT/ChatMusician outperform GPT-4 on composition tasks, but ZIQI-Eval (16 LLMs, all "poor"), ABC-Eval (near-random on sequence-level tasks) and MusicTheoryBench show that zero-shot natural-language *editing* of scores is only reliable in narrow domains (drum grooves, "Not that Groove"). Plan for specialised models plus an LLM orchestrator, not an LLM alone.
- **Expressive rendering is a separable, controllable stage** (VirtuosoNet, ScorePerformer, PianoFlow, DExter, MIDI-DDSP, RenderBox). "Compile to audio" can be score → expressive MIDI (with dynamics/tempo/articulation and even emotion/text controls) → synthesis, keeping every stage editable.
- **DAW integration exists; notation-editor integration barely does.** Composer's Assistant (REAPER), MIDI-GPT (Cubase, Ableton, OP-Z, Calliope), MusIAC (Colab) vs. DeepBach's 2017 MuseScore plugin as nearly the only notation-editor example — a clear opportunity for a symbolic-first studio.
- **Data and licensing:** Aria-MIDI (1M+ piano files, CC-BY-NC-SA 4.0), GigaMIDI, MetaScore (963K scores), MelodyHub (261K melodies), Lakh MIDI, POP909, ASAP; Composer's Assistant deliberately trained only on permissively-licensed MIDI. Licensing of training data will constrain what an open-source studio can ship.

---

## A. Representations, tokenizers, datasets, surveys

### MusicTransformer — Music Transformer: Generating Music with Long-Term Structure
- **Who/where/when:** Cheng-Zhi Anna Huang, Ashish Vaswani, Jakob Uszkoreit, et al. (Google Brain / Magenta); ICLR 2019 (arXiv Sep 2018)
- **Links:** https://arxiv.org/abs/1809.04281 ; code: https://github.com/magenta/magenta (Magenta); project: https://magenta.tensorflow.org/music-transformer
- **What it is:** Decoder-only Transformer over MIDI-like performance events (NOTE_ON/NOTE_OFF, TIME_SHIFT, VELOCITY) with a memory-efficient *relative* self-attention (linear rather than quadratic memory), enabling ~minute-long piano continuations with repeated motifs. Inputs: a primer (or a melody for the accompaniment variant); output: a continuation. Human control is limited to priming and melody-conditioning; no infilling.
- **Evidence:** State of the art on Piano-e-Competition NLL; also JSB Chorales; generates pieces ~4× longer than Oore et al. (2018).
- **Why it matters for the studio:** The anchor for all event-token symbolic models and for the "structure via attention" line; its representation (performance MIDI, no bars) is the baseline REMI reacted against.
- **Tags:** [symbolic-generation] [representation] [structure]
- **Verification:** verified (arXiv abstract fetched)
- **BibKey:** huang2018musictransformer

### REMI / PopMusicTransformer — Pop Music Transformer: Beat-based Modeling and Generation of Expressive Pop Piano Compositions
- **Who/where/when:** Yu-Siang Huang, Yi-Hsuan Yang (Taiwan AI Labs / Academia Sinica); ACM Multimedia 2020
- **Links:** https://arxiv.org/abs/2002.00212 ; code: https://github.com/YatingMusic/remi
- **What it is:** Introduces REMI ("revamped MIDI-derived events"): Bar, Position (16/bar), Tempo, Chord (60 types), Note-On, Note Velocity (32), Note Duration tokens — imposing a metrical grid so the Transformer-XL "knows" where beats and bars are. Trained on transcribed pop piano; generates from scratch or continues a prompt. Chord and tempo tokens are explicit and can be seeded, but there is no infilling.
- **Evidence:** Objective beat/downbeat salience metrics and a listening study show better rhythmic and harmonic coherence than MIDI-like tokens.
- **Why it matters for the studio:** REMI (and REMI+) is the de-facto default MIDI tokenization (MidiTok, FIGARO, Text2midi); bar/position/chord tokens are exactly the anchors a bar-level annotation system needs.
- **Tags:** [representation] [symbolic-generation]
- **Verification:** verified (arXiv PDF fetched)
- **BibKey:** huang2020popmusictransformer

### CPWord — Compound Word Transformer: Learning to Compose Full-Song Music over Dynamic Directed Hypergraphs
- **Who/where/when:** Wen-Yi Hsiao, Jen-Yu Liu, Yin-Cheng Yeh, Yi-Hsuan Yang (Taiwan AI Labs / Academia Sinica); AAAI 2021
- **Links:** https://arxiv.org/abs/2101.02402 ; code: https://github.com/YatingMusic/compound-word-transformer
- **What it is:** Groups co-occurring tokens into a "compound word" per time step, split into a *note* family (pitch, duration, velocity) and a *metric* family (position/bar, tempo, chord), each predicted by its own head with type-specific embedding sizes. Cuts sequence length several-fold so full pop-piano songs (~10k REMI tokens) fit in a linear Transformer.
- **Evidence:** 5–10× faster training convergence than REMI with comparable quality; enables full-song generation.
- **Why it matters for the studio:** Shows that a structured, typed token (rather than a flat stream) is both faster and more musically legible — a good target format for a studio's internal representation and for MidiTok's CPWord implementation.
- **Tags:** [representation] [symbolic-generation]
- **Verification:** verified (arXiv PDF fetched)
- **BibKey:** hsiao2021compoundword

### Octuple/MusicBERT + MidiBERT-Piano — MusicBERT: Symbolic Music Understanding with Large-Scale Pre-Training; BERT-like Pre-training for Symbolic Piano Music Classification Tasks
- **Who/where/when:** Mingliang Zeng, Xu Tan, Rui Wang, et al. (Microsoft Research Asia); ACL 2021 Findings. MidiBERT-Piano: Yi-Hui Chou, I-Chun Chen, Chin-Jui Chang, Joann Ching, Yi-Hsuan Yang (Academia Sinica); arXiv 2021, Journal of Creative Music Systems 2024
- **Links:** https://arxiv.org/abs/2106.05630 ; https://github.com/microsoft/muzic ; https://arxiv.org/abs/2107.05223 ; https://github.com/wazenmai/MIDI-BERT
- **What it is:** MusicBERT introduces *OctupleMIDI*, an 8-field token per note (bar, position, instrument, pitch, duration, velocity, time signature, tempo) and bar-level masking, pre-trained on >1M MIDI songs; downstream melody completion, accompaniment suggestion, genre and style classification. MidiBERT-Piano compares REMI vs Compound-Word inputs for BERT pre-training on piano MIDI, with note-level (melody extraction, velocity) and sequence-level (composer, emotion) tasks. Both are *understanding* models, not generators.
- **Evidence:** MusicBERT beats non-pretrained baselines on all four tasks; MidiBERT beats RNN baselines on four classification tasks.
- **Why it matters for the studio:** Understanding models are needed for the "annotate" step (auto-labelling melody/track roles, style, emotion) and Octuple is the compact multi-track note representation used by many later systems.
- **Tags:** [representation] [theory-analysis] [dataset]
- **Verification:** verified (arXiv abstracts fetched)
- **BibKey:** zeng2021musicbert (and chou2021midibert)

### folk-rnn — Music transcription modelling and composition using deep learning
- **Who/where/when:** Bob L. Sturm, João Felipe Santos, Oded Ben-Tal, Iryna Korshunova (QMUL / KTH); Conference on Computer Simulation of Musical Creativity 2016 (arXiv Apr 2016)
- **Links:** https://arxiv.org/abs/1604.08723 ; code/data: https://github.com/IraKorshunova/folk-rnn ; web: https://folkrnn.org
- **What it is:** Character-level LSTM trained on ~23,000 Irish/Celtic session tunes in ABC notation; generates complete tunes as text that renders directly to notation. Human control is via seeding (key, meter, opening notes) and temperature; no infilling. Evaluated at population level, individual-tune level, and for usefulness in composers' practice.
- **Evidence:** Statistical comparison to corpus; musicological analysis; used in multiple composer collaborations and a public web app.
- **Why it matters for the studio:** Established ABC-as-text as a viable symbolic representation for neural models — the lineage that leads to ChatMusician/MuPT/NotaGen — and showed early on that composers use such models as idea generators, not song machines.
- **Tags:** [symbolic-generation] [representation] [notation] [creativity-support] [history]
- **Verification:** verified (arXiv abstract fetched)
- **BibKey:** sturm2016folkrnn

### MidiTok — MidiTok: A Python package for MIDI file tokenization
- **Who/where/when:** Nathan Fradet, Jean-Pierre Briot, Fabien Chhel, Amal El Fallah Seghrouchni, Nicolas Gutowski (Sorbonne / Aubay); ISMIR 2021 Late-Breaking Demo; extended arXiv 2023 (2310.17202); v3.0.6 (July 2025)
- **Links:** https://github.com/Natooz/MidiTok ; docs: https://miditok.readthedocs.io ; https://archives.ismir.net/ismir2021/latebreaking/000005.pdf ; https://arxiv.org/abs/2310.17202
- **What it is:** MIT-licensed library implementing REMI, REMI+, MIDI-Like, TSD, Structured, CPWord, Octuple, MuMIDI, MMM and PerTok tokenizers behind one API, with BPE/Unigram/WordPiece sub-word training (via HF tokenizers), data augmentation, PyTorch Dataset/Collator utilities and Hugging Face Hub integration.
- **Evidence:** Widely adopted (Text2midi, MIDI-GPT team author is a maintainer); the 2023 paper shows BPE speeds up and improves symbolic models.
- **Why it matters for the studio:** The obvious tokenization backbone for any open-source symbolic studio; supports round-tripping MIDI↔tokens, which editing requires.
- **Tags:** [toolkit] [representation]
- **Verification:** verified (GitHub README fetched)
- **BibKey:** fradet2021miditok

### Aria-MIDI + Aria — Aria-MIDI: A Dataset of Piano MIDI Files for Symbolic Music Modeling; Scaling Self-Supervised Representation Learning for Symbolic Piano Performance
- **Who/where/when:** Louis Bradshaw, Simon Colton (QMUL); ICLR 2025. Aria model: Louis Bradshaw, Honglu Fan, Alexander Spangher, Stella Biderman, Simon Colton (QMUL / EleutherAI / USC / Geneva); ISMIR 2025
- **Links:** https://arxiv.org/abs/2504.15071 ; https://github.com/loubbrad/aria-midi ; https://arxiv.org/abs/2506.23869 ; https://github.com/EleutherAI/aria
- **What it is:** Aria-MIDI: 1.19M MIDI files (~801K after dedup, ~100,000 hours) transcribed from internet solo-piano recordings via an LLM-driven crawler, a piano/non-piano audio classifier and the Aria-AMT transcriber, with LLM-extracted metadata (composer 99.3% accuracy); CC-BY-NC-SA 4.0. Aria: a 650M-parameter decoder trained on it with an *absolute-onset* tokenization (onsets relative to 5-s segments instead of cumulative time-shifts), fine-tuned for continuation, contrastive embeddings (SimCLR) and classification. Human control: prompt continuation only (plus a Disklavier turn-taking duet demo, "Aria-Duet", arXiv 2511.01663).
- **Evidence:** Trained listeners preferred Aria continuations over Anticipatory Music Transformer and MusicGen (p<0.001), on par with Suno v3.5; SOTA composer/genre classification from embeddings.
- **Why it matters for the studio:** The largest open piano dataset and the strongest open piano continuation model; the tokenization insight (absolute onsets) is relevant to any studio representation; licence is non-commercial.
- **Tags:** [dataset] [symbolic-generation] [representation] [transcription] [expression-performance]
- **Verification:** verified (arXiv PDFs fetched)
- **BibKey:** bradshaw2025ariamidi (and bradshaw2025aria)

### LeSurvey — Natural Language Processing Methods for Symbolic Music Generation and Information Retrieval: a Survey
- **Who/where/when:** Dinh-Viet-Toan Le, Louis Bigo, Mikaela Keller, Dorien Herremans (Univ. Lille / CNRS / SUTD); ACM Computing Surveys 2025 (arXiv Feb 2024)
- **Links:** https://arxiv.org/abs/2402.17467 ; https://dl.acm.org/doi/10.1145/3714457
- **What it is:** Systematic survey organised along two axes — *representations* (time-slice vs event-based tokenization; elementary vs composite tokens) and *models* (RNNs, Transformers, pre-trained BERT/GPT variants) — covering both generation and MIR. Discusses data-scale disparity (billions of text tokens vs millions of music tokens), polyphony/simultaneity, and the epistemological limits of the music-as-language analogy. Note: the brief's title "A Survey on Deep Learning for Symbolic Music Generation and Information Retrieval" refers to this paper.
- **Evidence:** Survey (no experiments); advocates lighter models, explainability, standard benchmarks.
- **Why it matters for the studio:** The best single map of tokenization choices and their trade-offs — the reference to consult when designing the studio's internal symbolic format.
- **Tags:** [representation] [symbolic-generation] [evaluation]
- **Verification:** verified (arXiv PDF fetched)
- **BibKey:** le2025nlpsurvey

### JiSurvey — A Survey on Deep Learning for Symbolic Music Generation: Representations, Algorithms, Evaluations, and Challenges
- **Who/where/when:** Shulei Ji, Xinyu Yang, Jing Luo (Xi'an Jiaotong University); ACM Computing Surveys 2023 (updates the 2020 arXiv survey "A Comprehensive Survey on Deep Music Generation", arXiv 2011.06801)
- **Links:** https://dl.acm.org/doi/10.1145/3597493 ; https://arxiv.org/abs/2011.06801 (2020 version)
- **What it is:** Taxonomy of symbolic generation by representation (piano-roll, event, text, graph), by algorithm (VAE, GAN, Transformer, diffusion, RL) and by task (melody, polyphony, accompaniment, arrangement, style transfer), with a section on evaluation metrics and open challenges (structure, controllability, interaction).
- **Evidence:** Survey; catalogues metrics and datasets.
- **Why it matters for the studio:** Complementary to Le et al.; its task taxonomy (melody→harmony→arrangement→performance) is a useful scaffold for the studio's literature review.
- **Tags:** [symbolic-generation] [evaluation] [representation]
- **Verification:** partial (ACM DL blocked; located via search; 2020 arXiv version known)
- **BibKey:** ji2023survey

---

## B. Infilling / inpainting / editing an existing piece

### DeepBach — DeepBach: a Steerable Model for Bach Chorales Generation
- **Who/where/when:** Gaëtan Hadjeres, François Pachet, Frank Nielsen (Sony CSL Paris / LIP6 / École Polytechnique); ICML 2017
- **Links:** https://arxiv.org/abs/1612.01010 ; code: https://github.com/Ghadjeres/DeepBach
- **What it is:** Four-voice chorale model (bidirectional LSTMs per voice) sampled by pseudo-Gibbs resampling of individual notes, so a user can *fix* any notes, rhythms or cadences/fermatas and regenerate the rest — implemented as a MuseScore plugin where the composer selects a region and asks for re-harmonisation. Inputs: a partial or complete chorale plus constraints; outputs: a complete chorale.
- **Evidence:** Discrimination test with ~1,270 participants: DeepBach outputs were judged "Bach" nearly as often as real chorales; experts fooled at high rates.
- **Why it matters for the studio:** The original *steerable, notation-editor-integrated* symbolic model — the earliest concrete instance of "edit in the score, regenerate the rest".
- **Tags:** [symbolic-generation] [infilling] [editing] [notation] [controllability] [history]
- **Verification:** verified (arXiv abstract fetched)
- **BibKey:** hadjeres2017deepbach

### Coconet — Counterpoint by Convolution
- **Who/where/when:** Cheng-Zhi Anna Huang, Tim Cooijmans, Adam Roberts, Aaron Courville, Douglas Eck (Google Brain / MILA); ISMIR 2017
- **Links:** https://arxiv.org/abs/1903.07227 ; code: https://github.com/magenta/magenta/tree/main/magenta/models/coconet
- **What it is:** Convolutional orderless-NADE over a 4-voice piano-roll; trained to predict arbitrary masked notes, and sampled with blocked Gibbs "rewriting", so any subset of the score can be held fixed and the remainder inpainted (harmonise a melody, fill a voice, fix a bar). Later deployed as the Bach Doodle (2019), harmonising user-drawn melodies for millions of users.
- **Evidence:** Human evaluation and NLL show Gibbs rewriting far outperforms ancestral sampling, even with imperfect conditionals.
- **Why it matters for the studio:** Canonical "inpainting anywhere" formulation; the iterative rewrite loop mirrors compose→edit→compile.
- **Tags:** [infilling] [editing] [symbolic-generation] [accompaniment]
- **Verification:** verified (arXiv abstract fetched; authors from knowledge)
- **BibKey:** huang2017coconet

### InpaintNet — Learning to Traverse Latent Spaces for Musical Score Inpainting
- **Who/where/when:** Ashis Pati, Alexander Lerch, Gaëtan Hadjeres (Georgia Tech / Sony CSL); ISMIR 2019
- **Links:** https://arxiv.org/abs/1907.01164 ; code: https://github.com/ashispati/InpaintNet
- **What it is:** VAE-RNN that, given the measures before and after a gap in a monophonic melody, generates a path through the VAE latent space to produce the missing measures — explicitly framed as a tool for interactive composition (fill a hole, keep both sides).
- **Evidence:** Objective metrics and listening test vs. baselines; latent-space traversal was viable and coherent.
- **Why it matters for the studio:** Early monophonic melody infilling with past/future context; motivates latent-space editing as a complement to token infilling.
- **Tags:** [infilling] [editing] [symbolic-generation]
- **Verification:** verified (arXiv abstract fetched; authors from knowledge)
- **BibKey:** pati2019inpaintnet

### SketchNet — Music SketchNet: Controllable Music Generation via Factorized Representations of Pitch and Rhythm
- **Who/where/when:** Ke Chen, Cheng-i Wang, Taylor Berg-Kirkpatrick, Shlomo Dubnov (UC San Diego); ISMIR 2020
- **Links:** https://arxiv.org/abs/2008.01291 ; code: https://github.com/RetroCirce/Music-SketchNet
- **What it is:** Fills missing measures of a monophonic piece while letting the user *sketch* partial pitch contours and/or rhythm patterns for those measures; a factorised VAE (SketchVAE) separates pitch and rhythm so either can be specified independently, and SketchInpainter/SketchConnector combine context and sketch.
- **Evidence:** On Irish folk tunes, beats baselines on objective metrics and in a listening study; sketch constraints are respected.
- **Why it matters for the studio:** Direct precedent for "scribble a contour/rhythm on the score and let the AI complete it" — sketch-conditioned infilling.
- **Tags:** [sketch] [infilling] [controllability] [symbolic-generation]
- **Verification:** verified (arXiv abstract fetched)
- **BibKey:** chen2020sketchnet

### MMM — MMM: Exploring Conditional Multi-Track Music Generation with the Transformer
- **Who/where/when:** Jeff Ens, Philippe Pasquier (Metacreation Lab, Simon Fraser University); arXiv 2020
- **Links:** https://arxiv.org/abs/2008.06048 ; demo/code: https://github.com/jeffreyjohnens/MMM ; https://jeffreyjohnens.github.io/MMM/
- **What it is:** GPT-2-style model over a *MultiTrack* representation in which each track's bars are serialised as their own time-ordered sequence and tracks are concatenated (so a whole track or single bar can be masked and regenerated — the *BarFill* variant). Users control which tracks/bars to (re)generate, instrument per track and note-density level; an interactive interface targets iterative composition.
- **Evidence:** Qualitative/interactive demonstration; became the basis of MIDI-GPT.
- **Why it matters for the studio:** The origin of bar×track infilling with attribute controls, the operation a symbolic studio most needs; representation is in MidiTok.
- **Tags:** [infilling] [editing] [controllability] [symbolic-generation] [representation]
- **Verification:** verified (arXiv abstract fetched)
- **BibKey:** ens2020mmm

### XLNetInfill — Variable-Length Music Score Infilling via XLNet and Musically Specialized Positional Encoding
- **Who/where/when:** Chin-Jui Chang, Chun-Yi Lee, Yi-Hsuan Yang (NTHU / Academia Sinica); ISMIR 2021
- **Links:** https://arxiv.org/abs/2108.05064 ; code: https://github.com/reichang182/variable-length-piano-infilling
- **What it is:** Adapts XLNet's permutation LM to fill a gap of *variable* length (up to 128 notes) in polyphonic piano scores given past and future context, with a relative-bar positional encoding and look-ahead onset prediction so the fill lands on the right beat.
- **Evidence:** Objective metrics and human evaluation outperform prior infilling baselines; handles variable gap lengths that fixed-length models cannot.
- **Why it matters for the studio:** Shows how to infill when the composer deletes an arbitrary span and the number of notes is unknown — a common editing case.
- **Tags:** [infilling] [editing] [symbolic-generation]
- **Verification:** verified (arXiv abstract fetched)
- **BibKey:** chang2021xlnet

### MusIAC — MusIAC: An extensible generative framework for Music Infilling Applications with multi-level Control
- **Who/where/when:** Rui Guo, Ivor Simpson, Chris Kiefer, Thor Magnusson, Dorien Herremans (University of Sussex / SUTD); EvoMUSART 2022 (arXiv Feb 2022)
- **Links:** https://arxiv.org/abs/2202.05528 ; code: https://github.com/ruiguo-bio/musiac
- **What it is:** Transformer infilling of multi-track MIDI with *track-level* control tokens (note density, polyphony rate, occupation rate) and *bar-level* tokens (tensile strain and cloud diameter — tonal-tension measures from the spiral array), plus key/tempo/time-signature/instrument. A Colab interface lets a musician upload MIDI, choose what to infill and set controls, then download MIDI/WAV. A 2025 IEEE Access follow-up, "An Exploration of Controllability in Symbolic Music Infilling" (Herremans group), extends this analysis.
- **Evidence:** Control tokens improve perceived artistic coherence vs. density-only control.
- **Why it matters for the studio:** Introduces *tension* as an annotatable bar-level control — a high-level, composer-meaningful handle beyond density.
- **Tags:** [infilling] [controllability] [editing] [symbolic-generation]
- **Verification:** verified (arXiv PDF fetched)
- **BibKey:** guo2022musiac

### AMT — Anticipatory Music Transformer
- **Who/where/when:** John Thickstun, David Hall, Chris Donahue, Percy Liang (Stanford); TMLR 2024 (arXiv Jun 2023)
- **Links:** https://arxiv.org/abs/2306.08620 ; code: https://github.com/jthickstun/anticipation ; models on Hugging Face (stanford-crfm/music-*)
- **What it is:** "Anticipation": control events (e.g., a fixed melody, or any subset of notes the user wants kept) are interleaved into the event stream slightly *before* the moment they occur, so an ordinary autoregressive model learns to condition on them asynchronously. This yields infilling and accompaniment (fill all notes not marked as controls) from a single model trained on Lakh MIDI; 128M–780M-parameter checkpoints released under Apache 2.0.
- **Evidence:** Comparable log-likelihood to plain autoregressive baselines; human raters found 20-s accompaniments comparable in musicality to human-composed music.
- **Why it matters for the studio:** Elegant general mechanism for "everything I wrote is a hard constraint; fill the rest", and a strong open baseline (used by Aria as comparator).
- **Tags:** [infilling] [accompaniment] [controllability] [symbolic-generation]
- **Verification:** verified (arXiv abstract fetched)
- **BibKey:** thickstun2023anticipatory

### ComposersAssistant — Composer's Assistant: An Interactive Transformer for Multi-Track MIDI Infilling; Composer's Assistant 2: Interactive Multi-Track MIDI Infilling with Fine-Grained User Control
- **Who/where/when:** Martin E. Malandro (Sam Houston State University); ISMIR 2023 and ISMIR 2024
- **Links:** https://arxiv.org/abs/2301.12525 ; https://arxiv.org/abs/2407.14700 ; code/plugin: https://github.com/m-malandro/composers-assistant-REAPER
- **What it is:** T5-style encoder–decoder (d=384, 10+10 layers) that fills arbitrary deleted *track-measures* in a multi-track MIDI project, wired into REAPER via scripts: the composer creates empty MIDI items on named tracks to indicate what to generate. v1 controls: per-track mono/poly tokens and implicit chord/rhythm conditioning via temporary guide tracks. v2 adds two rhythmic-conditioning modes, horizontal and vertical note-onset density, several pitch controls (range etc.) and a "rhythmic interest" control. Trained only on permissively-licensed MIDI.
- **Evidence:** v1 listening test N=25 (rankings); v2 shows large objective gains and a listening study finding AI-completed excerpts rated comparably to fully human ones.
- **Why it matters for the studio:** The most complete existing example of DAW-embedded, composer-driven multi-track infilling with fine-grained controls — essentially a prototype of the studio's "compile the missing parts" step.
- **Tags:** [infilling] [editing] [controllability] [DAW-plugin] [co-creation-framework] [symbolic-generation]
- **Verification:** verified (arXiv PDFs fetched)
- **BibKey:** malandro2023composersassistant (and malandro2024composersassistant2)

### MIDI-GPT — MIDI-GPT: A Controllable Generative Model for Computer-Assisted Multitrack Music Composition
- **Who/where/when:** Philippe Pasquier, Jeff Ens, Nathan Fradet, Paul Triana, Davide Rizzotti (SFU Metacreation Lab), Jean-Baptiste Rolland, Maryam Safi (Steinberg); arXiv Jan 2025 (reported as AAAI 2025 — venue not confirmed from a primary source)
- **Links:** https://arxiv.org/abs/2501.17011 ; code: https://github.com/Metacreation-Lab/MIDI-GPT ; Calliope web app: https://metacreation.net/calliope/
- **What it is:** ~20M-parameter Transformer (6 layers, 2048-token context) successor to MMM: bars are sequenced *within* tracks, then tracks concatenated, enabling infilling at bar and track level for all 128 GM instruments. Conditioning: instrument, 10 instrument-relative note-density levels, polyphony range, note-duration range (5 bins), and style (MusicMap ontology). Trained on GigaMIDI. Integrated in Steinberg Cubase, an Ableton Live plugin, Teenage Engineering OP-Z, Elias game-audio middleware and the Calliope web app.
- **Evidence:** Low training-data duplication that decreases with length; stylistic consistency; controls enforced (duration best).
- **Why it matters for the studio:** Proves that a small, controllable bar×track infilling model can ship inside commercial DAWs — the reference architecture for a studio's local "compile" engine.
- **Tags:** [infilling] [editing] [controllability] [DAW-plugin] [product] [symbolic-generation]
- **Verification:** verified (arXiv PDF fetched)
- **BibKey:** pasquier2025midigpt

### MIDI-RWKV — Adaptable Symbolic Music Infilling with MIDI-RWKV (a.k.a. Personalizable Long-Context Symbolic Music Infilling with MIDI-RWKV)
- **Who/where/when:** Christian Zhou-Zheng, Philippe Pasquier (SFU Metacreation Lab); arXiv Jun 2025 (v2)
- **Links:** https://arxiv.org/abs/2506.13001 ; code/weights: https://github.com/christianazinn/MIDI-RWKV
- **What it is:** Compact foundation model on the linear-time RWKV-7 architecture for multi-track, long-context, controllable infilling that can run on edge devices; introduces *state tuning* (fine-tuning only the initial recurrent state) for style personalisation from a handful of a composer's own files. Explicitly framed around iterative refinement of existing work rather than from-scratch generation.
- **Evidence:** 31-page evaluation (17 tables) against prior infilling models; open code and weights (CC-BY 4.0).
- **Why it matters for the studio:** Addresses two studio requirements at once — local/offline inference and personalisation to the composer's own style with very little data.
- **Tags:** [infilling] [editing] [style-transfer] [controllability] [symbolic-generation]
- **Verification:** verified (arXiv abstract fetched)
- **BibKey:** zhouzheng2025midirwkv

### Polyffusion — Polyffusion: A Diffusion Model for Polyphonic Score Generation with Internal and External Controls
- **Who/where/when:** Lejun Min, Junyan Jiang, Gus Xia, Jingwei Zhao (NYU Shanghai / MBZUAI / NUS); ISMIR 2023
- **Links:** https://arxiv.org/abs/2307.10304 ; code: https://github.com/aik2mlj/polyffusion
- **What it is:** Image-diffusion over 8-bar piano-roll segments (POP909). *Internal control* = inpainting masks (keep melody, fill accompaniment; fill arbitrary regions; iterate for long form); *external control* = cross-attention on chord or texture embeddings from pre-trained encoders. One model covers melody→accompaniment, accompaniment→melody, arbitrary segment inpainting and chord/texture-conditioned arrangement.
- **Evidence:** 36-participant listening study on creativity/naturalness/musicality; significantly beats Transformer and sampling baselines on most metrics; 0 invalid notes in 160 samples.
- **Why it matters for the studio:** Cleanly separates "what to keep" (mask) from "what to steer" (condition), which maps onto annotation types; piano-roll masks correspond to region selection in a score editor.
- **Tags:** [infilling] [controllability] [accompaniment] [symbolic-generation] [representation]
- **Verification:** verified (arXiv PDF fetched)
- **BibKey:** min2023polyffusion

### GETMusic — GETMusic: Generating Any Music Tracks with a Unified Representation and Diffusion Framework
- **Who/where/when:** Ang Lv, Xu Tan, Peiling Lu, et al. (Renmin University / Microsoft Research Asia); arXiv 2023
- **Links:** https://arxiv.org/abs/2305.10841 ; code: https://github.com/microsoft/muzic/tree/main/getmusic
- **What it is:** *GETScore* stacks tracks vertically and time horizontally, two rows (pitch, duration) per track; *GETDiff* is a discrete diffusion model trained to denoise masked target tracks given intact source tracks, so any of the 665 source→target combinations over six tracks (bass, drums, guitar, piano, strings, melody) — and zero-shot infilling of arbitrary masked cells — work from one model.
- **Evidence:** Beats PopMAG and Museformer on chord accuracy and distribution metrics; 10 music-trained raters, κ>0.6.
- **Why it matters for the studio:** "Give me a bass line for these tracks / fill bars 9–12 of the guitar" as a single masked-denoising operation on a track×time grid — a natural fit for a multi-track score editor.
- **Tags:** [infilling] [accompaniment] [symbolic-generation] [representation]
- **Verification:** verified (arXiv PDF fetched; author list from knowledge)
- **BibKey:** lv2023getmusic

### NotThatGroove — Not that Groove: Zero-Shot Symbolic Music Editing (v2: Zero-Shot Symbolic Music Editing as a Reasoning Task for Large Language Models)
- **Who/where/when:** Li Zhang (Drexel University); arXiv May 2025 (v2 May 2026)
- **Links:** https://arxiv.org/abs/2505.08203
- **What it is:** Studies whether general LLMs can *edit* an existing drum groove from natural-language instructions (specific "add a cymbal on beat 1", descriptive "reduce hi-hat activity", stylistic "make it funkier") with no training, using a compact text "drumroll" notation (one line per instrument, one character per 16th). Evaluation via expert-authored unit tests rather than ground-truth edits.
- **Evidence:** Unit tests agree with professional musicians (89% TPR / 94% TNR); best of 8 LLMs (gpt-4.1-mini) passes 68% of tests; reasoning models help.
- **Why it matters for the studio:** The clearest existing study of NL-instruction *editing* of symbolic music; shows it is feasible in a narrow domain and that test-based evaluation is the right tool for edit verification.
- **Tags:** [editing] [LLM-agent] [text-conditioning] [evaluation] [symbolic-generation]
- **Verification:** verified (arXiv PDF/HTML fetched)
- **BibKey:** zhang2025groove

---

## C. Controllable and text/attribute-conditioned generation

### Museformer — Museformer: Transformer with Fine- and Coarse-Grained Attention for Music Generation
- **Who/where/when:** Botao Yu, Peiling Lu, Rui Wang, et al. (Nanjing University / Microsoft Research Asia / Peking University); NeurIPS 2022
- **Links:** https://arxiv.org/abs/2210.10349 ; code: https://github.com/microsoft/muzic/tree/main/museformer
- **What it is:** Sparse attention where each bar attends finely to "structure-related" previous bars (1, 2, 4, 8, 12, 16, 24, 32 bars back — chosen from bar-similarity statistics) and coarsely to summaries of the others; models >3× longer sequences than full attention for full-song multi-track generation from scratch (Lakh MIDI). No infilling or user controls.
- **Evidence:** Better perplexity at all lengths; repetition-similarity curves closer to human music; higher human ratings for short- and long-term structure.
- **Why it matters for the studio:** Encodes a musical prior (repetition at phrase-multiples) into architecture — informs how a studio's models should see form.
- **Tags:** [structure] [symbolic-generation]
- **Verification:** verified (arXiv PDF fetched)
- **BibKey:** yu2022museformer

### FIGARO — FIGARO: Generating Symbolic Music with Fine-Grained Artistic Control
- **Who/where/when:** Dimitri von Rütte, Luca Biggio, Yannic Kilcher, Thomas Hofmann (ETH Zürich); ICLR 2023 (arXiv Jan 2022)
- **Links:** https://arxiv.org/abs/2201.10936 ; code: https://github.com/dvruette/figaro
- **What it is:** "Description-to-sequence": a per-bar description made of *expert* features (instruments present, chords, time signature, note density, mean pitch, mean velocity, mean duration) plus *learned* VQ-VAE codes conditions a seq2seq Transformer that emits REMI+ (multi-track REMI) tokens. A composer can write or edit the bar-by-bar description (change chords, add an instrument, raise density) and regenerate; also enables style transfer by swapping learned codes.
- **Evidence:** SOTA controllable generation on Lakh MIDI; generalises to out-of-distribution descriptions.
- **Why it matters for the studio:** Bar-level description = a formal annotation language; FIGARO is the closest to "annotate bars with chords/density/instrumentation, then compile".
- **Tags:** [controllability] [symbolic-generation] [style-transfer] [annotation] [representation]
- **Verification:** verified (arXiv abstract fetched)
- **BibKey:** vonrutte2023figaro

### MuseCoco — MuseCoco: Generating Symbolic Music from Text
- **Who/where/when:** Peiling Lu, Xin Xu, Chenfei Kang, et al. (Microsoft Research Asia); arXiv Jun 2023
- **Links:** https://arxiv.org/abs/2306.00110 ; code: https://github.com/microsoft/muzic/tree/main/musecoco
- **What it is:** Two-stage text→symbolic: (1) text-to-attribute understanding (a BERT-style classifier over ~12 attributes such as instrument, rhythm/danceability, bar count, time signature, key, tempo, pitch range, emotion, genre, time) and (2) attribute-to-music generation (1.2B-parameter decoder). Because the interface is attributes, users can bypass text and set attributes directly; outputs are editable MIDI. From-scratch only.
- **Evidence:** ~20% higher objective control accuracy than baselines; higher musicality/controllability ratings; large model beats GPT-4 (ABC) in their study.
- **Why it matters for the studio:** Demonstrates that text should be *compiled to an explicit attribute layer* the composer can inspect and override — an argument against opaque text-to-song.
- **Tags:** [text-conditioning] [controllability] [symbolic-generation]
- **Verification:** verified (arXiv abstract fetched)
- **BibKey:** lu2023musecoco

### MuseMorphose — MuseMorphose: Full-Song and Fine-Grained Piano Music Style Transfer with One Transformer VAE
- **Who/where/when:** Shih-Lun Wu, Yi-Hsuan Yang (Academia Sinica / Taiwan AI Labs); IEEE/ACM TASLP 2023 (arXiv May 2021)
- **Links:** https://arxiv.org/abs/2105.04090 ; code: https://github.com/YatingMusic/MuseMorphose
- **What it is:** Transformer VAE where each bar of an existing pop-piano piece is encoded to a latent and decoded conditioned on user-set *bar-level* attributes (rhythmic intensity, polyphony, 8 levels each), so the piece's content is preserved while its texture is rewritten bar by bar — attribute-conditioned *editing* of a whole song.
- **Evidence:** Beats RNN (MusicVAE-style) baselines on fidelity, attribute-control accuracy and diversity across full songs.
- **Why it matters for the studio:** A model of "keep the piece, turn a knob per bar" — annotation-as-fader on an existing composition.
- **Tags:** [style-transfer] [editing] [controllability] [symbolic-generation]
- **Verification:** verified (arXiv abstract fetched)
- **BibKey:** wu2023musemorphose

### FaderNets — Music FaderNets: Controllable Music Generation Based on High-Level Features via Low-Level Feature Modelling
- **Who/where/when:** Hao Hao Tan, Dorien Herremans (SUTD); ISMIR 2020
- **Links:** https://arxiv.org/abs/2007.15474 ; code: https://github.com/gudgud96/music-fader-nets
- **What it is:** Disentangled "faders" for low-level attributes (rhythm density, note density) in a VAE, with a Gaussian-mixture latent that captures the high-level attribute *arousal* semi-supervised from 1% labels; sliding a fader rewrites an existing piano phrase along that dimension.
- **Evidence:** Learns arousal with minimal labels; enables arousal style transfer on VGMIDI.
- **Why it matters for the studio:** Shows how emotion-level annotations ("more intense here") can be grounded in low-level controllable features.
- **Tags:** [controllability] [style-transfer] [editing] [symbolic-generation]
- **Verification:** verified (arXiv abstract fetched)
- **BibKey:** tan2020fadernets

### MMT — Multitrack Music Transformer
- **Who/where/when:** Hao-Wen Dong, Ke Chen, Shlomo Dubnov, Julian McAuley, Taylor Berg-Kirkpatrick (UC San Diego); ICASSP 2023
- **Links:** https://arxiv.org/abs/2207.06983 ; code: https://github.com/salu133445/mmt ; demo: https://salu133445.github.io/mmt/
- **What it is:** Each note is one 6-tuple event (type, beat, position, pitch, duration, instrument) with multi-head output, giving 2.6–3.5× more music per token than MMM/REMI+ and fast inference; 64 instruments; trained on the Symbolic Orchestral Database (5,743 pieces). Modes: unconditioned, *instrument-informed* (user lists instruments) and n-beat continuation; no infilling. Includes attention analysis (consonant intervals, aligned beats).
- **Evidence:** Competitive quality with large speed/memory gains; suitable for real-time creative tools.
- **Why it matters for the studio:** Efficient multi-track/orchestral representation; instrument-specification is a basic orchestration control.
- **Tags:** [symbolic-generation] [representation] [controllability] [real-time]
- **Verification:** verified (arXiv PDF fetched)
- **BibKey:** dong2023mmt

### SymPAC — SymPAC: Scalable Symbolic Music Generation with Prompts and Constraints
- **Who/where/when:** Haonan Chen, Jordan B. L. Smith, Bochen Li, et al. (ByteDance / QMUL / CUHK); ISMIR 2024
- **Links:** https://arxiv.org/abs/2409.03055
- **What it is:** Trains a multi-track symbolic model solely on ~1M in-house *audio* tracks auto-transcribed with MIR models (beat, chords, sections, multi-track transcription). Control is via *prompt bars* — a leading block holding genre, section labels, tempo, chords and track list that the user can fully or partially specify — and via finite-state-machine *constrained decoding* that guarantees generated tokens obey the grammar and the user's constraints.
- **Evidence:** 12 MIR researchers/producers rated it significantly above FIGARO and MMT on coherence, richness, arrangement, structure and overall.
- **Why it matters for the studio:** Hard constraints at decode time (rather than soft conditioning) are what a composer expects when they write "Cmaj7 here"; prompt bars are a compact section-level annotation.
- **Tags:** [controllability] [symbolic-generation] [structure] [transcription]
- **Verification:** verified (arXiv PDF fetched)
- **BibKey:** chen2024sympac

### Text2midi — Text2midi: Generating Symbolic Music from Captions
- **Who/where/when:** Keshav Bhandari, Abhinaba Roy, Kyra Wang, Geeta Puri, Simon Colton, Dorien Herremans (QMUL / SUTD); AAAI 2025
- **Links:** https://arxiv.org/abs/2412.16526 ; code/demo: https://github.com/AMAAI-Lab/Text2midi
- **What it is:** Frozen FLAN-T5 text encoder + 18-layer autoregressive decoder (272M params, 159M trainable) emitting REMI+ tokens (MidiTok); pre-trained on SymphonyNet with pseudo-captions, fine-tuned on MidiCaps (168K MIDI–caption pairs). Control via musical terms in the caption (tempo, key, chords, mood, genre); from-scratch only.
- **Evidence:** Beats MuseCoco on tempo (65.8% vs 54.6%) and key accuracy (35.6% vs 14.6%) and CLAP score; 11 listeners rated it above MuseCoco but below ground truth; struggles with instrumentation specificity; 2,048-token context.
- **Why it matters for the studio:** Open, reproducible text→MIDI baseline; its weaknesses (instrumentation, length) illustrate why text alone is an insufficient control surface.
- **Tags:** [text-conditioning] [symbolic-generation] [dataset]
- **Verification:** verified (arXiv PDF fetched)
- **BibKey:** bhandari2025text2midi

### MetaScore — Generating Symbolic Music from Natural Language Prompts using an LLM-Enhanced Dataset
- **Who/where/when:** Weihan Xu, Julian McAuley, Shlomo Dubnov, Taylor Berg-Kirkpatrick, Hao-Wen Dong (Duke / UC San Diego / U. Michigan); ISMIR 2025 (arXiv Oct 2024)
- **Links:** https://arxiv.org/abs/2410.02084 ; https://ismir2025program.ismir.net/poster_32.html
- **What it is:** MetaScore: 963K MuseScore-sourced scores with metadata (genre via classifier, composer, complexity, instruments), plus LLM (BLOOM) generated captions. Two generators: MST-Tags (categorical control) and MST-Text (free-text), both built on REMI+/MMT-style representations — i.e., scores are converted to MIDI tokens rather than generated as MusicXML.
- **Evidence:** 22-participant study: MST-Text comparable to Text2midi on overall quality and better than a BART baseline on coherence, arrangement and adherence.
- **Why it matters for the studio:** Largest *score*-origin (not performance) dataset; tag-conditioning offers a controllable alternative to captions; confirms the absence of native MusicXML generation.
- **Tags:** [dataset] [text-conditioning] [notation] [symbolic-generation]
- **Verification:** verified (arXiv PDF fetched)
- **BibKey:** xu2025metascore

### MIDI-LLM — MIDI-LLM: Adapting Large Language Models for Text-to-MIDI Music Generation
- **Who/where/when:** Shih-Lun Wu, Dave Carlton, Ryan Miyakawa, Yoon Kim, Chris Donahue, Cheng-Zhi Anna Huang (MIT / CMU / industry); ISMIR 2026 (arXiv Nov 2025)
- **Links:** https://arxiv.org/abs/2511.03942 ; https://openreview.net/pdf?id=GVW9YixIAI
- **What it is:** Expands Llama-3.2-1B's vocabulary with MIDI tokens and trains in two stages — continued unimodal pre-training on music-adjacent text and standalone MIDI, then supervised fine-tuning on text–MIDI pairs — preserving the LLM's text abilities and vLLM-compatible inference.
- **Evidence:** Outperforms Text2midi on controllability and quality; in-the-wild study with 58 musicians and ~4,000 generations showed higher acceptance for lead-sheet generation.
- **Why it matters for the studio:** Strongest recent evidence that a general LLM can be turned into a symbolic co-writer for *lead sheets* while retaining language for dialogue — a plausible backbone for an annotation-understanding "compiler front end".
- **Tags:** [text-conditioning] [LLM-agent] [symbolic-generation] [HCI-study]
- **Verification:** verified (arXiv abstract fetched)
- **BibKey:** wu2026midillm

### SCG — Symbolic Music Generation with Non-Differentiable Rule Guided Diffusion
- **Who/where/when:** Yujia Huang, Adishree Ghatare, Yuanzhe Liu, et al. (Caltech / RPI / NVIDIA / Dalhousie–Vector); ICML 2024
- **Links:** https://arxiv.org/abs/2402.14285 ; code: https://github.com/yjhuangcd/rule-guided-music
- **What it is:** Stochastic Control Guidance steers a pre-trained latent diffusion model (piano-roll) toward *non-differentiable* rules — pitch-class histogram, horizontal/vertical note density, chord progression — by forward-evaluating the rule on candidate samples at each step, training-free. Supports *editing*: modify an existing piece within a chosen time window, either as a variant or to satisfy new rules.
- **Evidence:** Improves both rule adherence and quality over baselines (including classifier guidance) on symbolic piano data.
- **Why it matters for the studio:** New annotation types can be added as plain functions without retraining; window-based editing of an existing piece fits the loop exactly.
- **Tags:** [controllability] [editing] [symbolic-generation]
- **Verification:** verified (arXiv PDF fetched)
- **BibKey:** huang2024scg

### LC-Diff — Conditional Diffusion as Latent Constraints for Controllable Symbolic Music Generation
- **Who/where/when:** Matteo Pettenò, Alessandro Ilic Mezza, Alberto Bernardini (Politecnico di Milano); ISMIR 2025 (arXiv Nov 2025)
- **Links:** https://arxiv.org/abs/2511.07156 ; https://ismir2025program.ismir.net/poster_133.html
- **What it is:** Keeps a frozen unconditional VAE and trains small conditional diffusion priors on its latent space as plug-and-play constraints, giving fader-like control over note density, pitch range, melodic contour and rhythmic complexity (Toussaint) for monophonic melodies (10M sequences from 176K MIDI files).
- **Evidence:** Pearson correlation >0.8 between requested and realised attributes for all attributes, beating attribute-regularised VAEs and cVAEs; better Fréchet Music Distance.
- **Why it matters for the studio:** Another retrofit-control mechanism: new controls without touching the base model.
- **Tags:** [controllability] [symbolic-generation]
- **Verification:** verified (arXiv PDF fetched)
- **BibKey:** petteno2025lcdiff

### Diff-Symbo — Diff-Symbo: Text-Controlled Long-Duration Symbolic Music Generation Using Autoregressive Latent Diffusion Model
- **Who/where/when:** Zhiwei Lin, Jun Chen, Boshi Tang, et al. (Tsinghua / industry); arXiv Aug 2026
- **Links:** https://arxiv.org/abs/2608.05222
- **What it is:** Autoregressive latent diffusion for text-conditioned multi-track symbolic music aimed at long durations and consistency; addresses paired-data scarcity with 19,345 LLM-generated text templates.
- **Evidence:** Reports gains in controllability and quality over GPT-4, MuseCoco and MMT baselines.
- **Why it matters for the studio:** Indicative of the mid-2026 frontier for text→symbolic; still from-scratch generation, no editing.
- **Tags:** [text-conditioning] [symbolic-generation]
- **Verification:** verified (arXiv abstract fetched; very recent, not peer-reviewed)
- **BibKey:** lin2026diffsymbo

---

## D. Music LLMs on text notation (ABC) and their evaluation

### ChatMusician — ChatMusician: Understanding and Generating Music Intrinsically with LLM
- **Who/where/when:** Ruibin Yuan, Hanfeng Lin, Yi Wang, et al. (M-A-P / HKUST / QMUL and others); arXiv Feb 2024 (published in Findings of ACL 2024 — venue from knowledge, not re-fetched)
- **Links:** https://arxiv.org/abs/2402.16153 ; code/models: https://github.com/hf-lin/ChatMusician ; https://shanghaicannon.github.io/ChatMusician/
- **What it is:** LLaMA-2-7B continually pre-trained and fine-tuned on MusicPile (4B tokens) treating ABC notation as a second language. Supports conditioned generation from chords, motifs, musical form, style and text, plus music-theory Q&A; releases MusicTheoryBench (college-level theory + reasoning).
- **Evidence:** Beats GPT-4 on their composition tasks in human evaluation; MMLU slightly improved; on MusicTheoryBench, all LLMs including GPT-4 are near chance on *reasoning*.
- **Why it matters for the studio:** First open LLM that composes in notation and talks about it; its benchmark exposes the reasoning gap a studio must design around.
- **Tags:** [symbolic-generation] [LLM-agent] [text-conditioning] [notation] [evaluation]
- **Verification:** verified (arXiv abstract fetched)
- **BibKey:** yuan2024chatmusician

### MuPT — MuPT: A Generative Symbolic Music Pretrained Transformer
- **Who/where/when:** Xingwei Qu, Yuelin Bai, Yinghao Ma, et al. (M-A-P / Waterloo / HKUST / Manchester); arXiv Apr 2024 (widely reported as accepted at ICLR 2025 — venue not confirmed from a primary source)
- **Links:** https://arxiv.org/abs/2404.06393 ; https://map-mupt.github.io/ ; models on Hugging Face (m-a-p/MuPT-*)
- **What it is:** Family of 190M–4.23B-parameter decoders trained on 33.6B tokens of ABC with 8,192-token context. Introduces *SMT-ABC* (Synchronized Multi-Track ABC), interleaving bars of the same index across tracks with `<|>` delimiters so multi-part alignment survives; proposes a Symbolic Music Scaling law under data repetition. Generation is from-scratch/continuation.
- **Evidence:** ABC outperformed MIDI tokens for LLMs in their study; scaling law fits with repeated epochs.
- **Why it matters for the studio:** SMT-ABC is the most practical text encoding of multi-track *scores* (bar-aligned) — a candidate interchange format between the studio's notation view and LLMs.
- **Tags:** [symbolic-generation] [representation] [notation] [LLM-agent]
- **Verification:** verified (arXiv PDF fetched)
- **BibKey:** qu2024mupt

### NotaGen — NotaGen: Advancing Musicality in Symbolic Music Generation with Large Language Model Training Paradigms
- **Who/where/when:** Yashan Wang, Shangda Wu, Jianhuai Hu, et al. (Central Conservatory of Music, Beijing, and others); arXiv Feb 2025 (v5 2025)
- **Links:** https://arxiv.org/abs/2502.18008 ; code/weights: https://github.com/ElectricAlexis/NotaGen ; demo: https://electricalexis.github.io/notagen-demo/
- **What it is:** LLM-style pipeline for classical *scores* in ABC: pre-train on 1.6M pieces, fine-tune on ~9K high-quality classical works, then reinforce with *CLaMP-DPO* (preference optimisation using the CLaMP 2 music–text model as an automatic judge, no human labels). Conditioning is a "period–composer–instrumentation" prompt; generation from scratch.
- **Evidence:** Subjective A/B tests favour NotaGen over baselines (and human-composed pieces in some comparisons); CLaMP-DPO improves controllability and quality.
- **Why it matters for the studio:** The current strongest open *score*-level generator and a template for RL-from-model-feedback that could be redirected at composer-specified rewards (annotations).
- **Tags:** [symbolic-generation] [notation] [controllability] [LLM-agent]
- **Verification:** verified (arXiv abstract fetched)
- **BibKey:** wang2025notagen

### MelodyT5 — MelodyT5: A Unified Score-to-Score Transformer for Symbolic Music Processing
- **Who/where/when:** Shangda Wu, Yashan Wang, Xiaobing Li, Feng Yu, Maosong Sun (Central Conservatory of Music / Tsinghua); ISMIR 2024
- **Links:** https://arxiv.org/abs/2407.02277 ; code: https://github.com/sanderwood/melodyt5 ; https://huggingface.co/sander-wood/melodyt5
- **What it is:** Encoder–decoder over ABC that unifies seven melody-centric score-to-score tasks (e.g., melody generation, harmonisation, melodisation, segmentation, variation) in one model, pre-trained on MelodyHub (261K melodies, >1M task instances).
- **Evidence:** Multi-task transfer improves low-data tasks vs single-task models.
- **Why it matters for the studio:** A single "score in → score out" model for lead-sheet operations (add chords to a melody, write a melody over chords, segment phrases) — the kind of operator a compile step chains.
- **Tags:** [symbolic-generation] [accompaniment] [notation] [structure]
- **Verification:** verified (arXiv abstract fetched; authors from GitHub/knowledge)
- **BibKey:** wu2024melodyt5

### FunctionAlignment — Versatile Symbolic Music-for-Music Modeling via Function Alignment
- **Who/where/when:** Junyan Jiang, Daniel Chin, Liwei Lin, Xuanjie Liu, Gus Xia (NYU Shanghai / MBZUAI Music X Lab); ISMIR 2025
- **Links:** https://arxiv.org/abs/2506.15548
- **What it is:** Two pretrained symbolic LMs (a RoFormer trained from scratch on 357K Los Angeles MIDI files, 16th-note grid) — one reading a *reference* sequence, one writing a *target* — joined by a lightweight adapter, so understanding (chord recognition, metrical analysis) and generation (chord-conditioned melody, melody-conditioned chords, drums↔song) are the same "music-for-music" operation, parameter-efficiently.
- **Evidence:** Strong results across five tasks incl. few-shot chord recognition and metre transcription on RWC-Pop (93 songs); code and weights released.
- **Why it matters for the studio:** A general recipe for "given this part, produce/analyse that part" with small adapters — exactly the pluggable operator set a compile pipeline needs.
- **Tags:** [symbolic-generation] [accompaniment] [theory-analysis] [controllability]
- **Verification:** verified (arXiv PDF fetched)
- **BibKey:** jiang2025functionalignment

### HowFarLLMs — How Far Can Pretrained LLMs Go in Symbolic Music? Controlled Comparisons of Supervised and Preference-based Adaptation
- **Who/where/when:** Deepak Kumar, Emmanouil Karystinaios, Gerhard Widmer, Markus Schedl (JKU Linz); NLP4MusA 2026 (arXiv Jan 2026)
- **Links:** https://arxiv.org/abs/2601.22764
- **What it is:** Controlled comparison of off-the-shelf instruction-tuned LLMs vs. domain-adapted variants (SFT vs. preference optimisation/DPO) vs. a music-specialised baseline on ABC generation and understanding across several corpora, analysing the domain-adaptation vs. prior-preservation trade-off and how metrics disagree.
- **Evidence:** Multiple corpora and metrics; shows adaptation choices materially change outcomes and that standard metrics behave idiosyncratically for music.
- **Why it matters for the studio:** Practical guidance for turning a general LLM into the studio's notation-literate assistant.
- **Tags:** [LLM-agent] [evaluation] [symbolic-generation] [notation]
- **Verification:** verified (arXiv abstract fetched)
- **BibKey:** kumar2026howfar

### SymbolicLLMBenchmarks — ZIQI-Eval; ABC-Eval; (WildScore)
- **Who/where/when:** ZIQI-Eval: Jiajia Li, Lu Yang, Mingni Tang, et al. (Wuhan University / SJTU / Shenyang Conservatory), arXiv Jun 2024 (reported as ACL 2024 Findings — venue not confirmed from a primary source). ABC-Eval: Jiahao Zhao, Yunjia Li, Wei Li, Kazuyoshi Yoshii (Kyoto University / Fudan), arXiv Sep 2025. WildScore: Gagan Mundada, Yash Vishe, Amit Namburi, et al. (UC San Diego), arXiv Sep 2025.
- **Links:** https://arxiv.org/abs/2406.15885 ; https://github.com/zcli-charlie/ZIQI-Eval ; https://arxiv.org/abs/2509.23350 ; https://arxiv.org/abs/2509.04744
- **What it is:** ZIQI-Eval: >14,000 questions across 10 categories / 56 sub-categories of music knowledge (theory, history, instruments, symbolic tasks) for text LLMs. ABC-Eval: 1,086 items over 10 sub-tasks on ABC scores from syntax to segment- and sequence-level understanding and instruction following. WildScore: in-the-wild multimodal reasoning over *score images* with real user questions (belongs primarily to the multimodal cluster). Also MusicTheoryBench (ChatMusician).
- **Evidence:** ZIQI-Eval: all 16 LLMs "poor". ABC-Eval: 7 LLMs incl. GPT-5/Gemini/DeepSeek score >90% on syntax but near random on sequence-level tasks (e.g., emotion). WildScore: mixed strengths and clear gaps.
- **Why it matters for the studio:** Quantifies where an LLM orchestrator can and cannot be trusted with notation; motivates specialised models plus verification (unit tests, constraints).
- **Tags:** [evaluation] [LLM-agent] [notation] [theory-analysis]
- **Verification:** verified (arXiv abstracts/PDFs fetched)
- **BibKey:** li2024ziqieval (and zhao2025abceval, mundada2025wildscore)

---

## E. Structure-aware generation, harmonization, arrangement ("compile" pipelines)

### WholeSong — Whole-Song Hierarchical Generation of Symbolic Music Using Cascaded Diffusion Models
- **Who/where/when:** Ziyu Wang, Lejun Min, Gus Xia (NYU Shanghai / MBZUAI Music X Lab); ICLR 2024
- **Links:** https://arxiv.org/abs/2405.09901 ; code: https://github.com/ZZWaang/whole-song-gen ; OpenReview: https://openreview.net/forum?id=sn7CYWyavh
- **What it is:** Four cascaded piano-roll diffusion models generate a full pop song top-down: (1) form/phrase structure and key, (2) reduced lead sheet (harmonic skeleton), (3) lead sheet (melody + chords), (4) accompaniment — each conditioned on the levels above. Every level is an interpretable, editable symbolic object, and external pre-trained encoders can steer chord progression, rhythm patterns and accompaniment texture.
- **Evidence:** Human study shows higher ratings for full-song structure than flat baselines; controllability demonstrated at each level.
- **Why it matters for the studio:** The most literal existing "compiler": human-editable intermediate representations at every stage of a form→lead-sheet→arrangement pipeline.
- **Tags:** [structure] [symbolic-generation] [controllability] [accompaniment] [co-creation-framework]
- **Verification:** verified (arXiv abstract fetched)
- **BibKey:** wang2024wholesong

### MusicFrameworks — Controllable Deep Melody Generation via Hierarchical Music Structure Representation; What is missing in deep music generation? A study of repetition and structure in popular music
- **Who/where/when:** Shuqi Dai, Zeyu Jin, Celso Gomes, Roger B. Dannenberg (CMU / Adobe); ISMIR 2021. Follow-up: Shuqi Dai, Huiran Yu, Roger B. Dannenberg (CMU); ISMIR 2022
- **Links:** https://arxiv.org/abs/2109.00663 ; https://arxiv.org/abs/2209.00182 ; https://shuqid.net/
- **What it is:** MusicFrameworks decomposes melody composition into section/phrase structure → "basic melody" (one note per beat) → rhythm → realised melody, with Transformers/LSTMs per stage; a user can edit chords, the basic melody and the rhythm structure and regenerate downstream. The 2022 study analyses Chinese and American pop corpora to show multi-level repetition and structure that current generators miss.
- **Evidence:** Listeners preferred generated melodies over POP909 human melodies ~50% of the time; corpus analysis quantifies non-random repetition.
- **Why it matters for the studio:** Concrete hierarchy of *editable intermediate representations* for melody, and evidence that structure must be explicit — supports an annotation layer for form/phrases.
- **Tags:** [structure] [controllability] [symbolic-generation] [editing]
- **Verification:** verified (arXiv abstracts fetched)
- **BibKey:** dai2021musicframeworks (and dai2022missing)

### StructuralMelodyInfilling — Melody Infilling with User-Provided Structural Context
- **Who/where/when:** Chih-Pin Tan, Alvin W. Y. Su, Yi-Hsuan Yang (NCKU / Academia Sinica); ISMIR 2022
- **Links:** https://arxiv.org/abs/2210.02829 ; code: https://github.com/tanchihpin0517/structure-aware_infilling
- **What it is:** Transformer that fills a missing melody segment given past/future context *and* user-provided structural information (e.g., which earlier phrase the gap should echo), via an attention-selecting module, so the fill respects form rather than only local smoothness.
- **Evidence:** Objective and subjective results show structure-conditioned fills beat structure-agnostic baselines on pop melodies.
- **Why it matters for the studio:** Infilling that takes *form annotations* ("this is the return of A") as input — precisely the annotate→compile pattern.
- **Tags:** [infilling] [structure] [annotation] [symbolic-generation]
- **Verification:** verified (arXiv abstract fetched; authors from knowledge)
- **BibKey:** tan2022melodyinfilling

### AccoMontage — AccoMontage: Accompaniment Arrangement via Phrase Selection and Style Transfer; AccoMontage2: A Complete Harmonization and Accompaniment Arrangement System
- **Who/where/when:** Jingwei Zhao, Gus Xia (Music X Lab, NYU Shanghai); ISMIR 2021. AccoMontage2: Li Yi, Haochen Hu, Jingwei Zhao, Gus Xia; ISMIR 2022
- **Links:** https://arxiv.org/abs/2108.11213 ; https://github.com/zhaojw1998/AccoMontage ; https://arxiv.org/abs/2209.00353 ; https://github.com/billyblu2000/AccoMontage2
- **What it is:** Lead sheet (melody + chords) → full-length piano accompaniment by (1) retrieving accompaniment *phrases* from a database with dynamic programming over phrase fitness and transition smoothness, then (2) re-harmonising them to the target chords via a chord–texture disentangled VAE (style transfer). AccoMontage2 adds a melody-harmonisation module (structured chord progressions via three loss terms) and a GUI where users pick chord style (Pop/R&B/Dark) and texture density/rhythmic complexity.
- **Evidence:** 72 participants: significantly better coherence and structure than learning-only baselines (p<0.05), musicality marginal (p=0.053).
- **Why it matters for the studio:** "Retrieve human-made material and adapt it to my chords" is a compositionally transparent form of compile — and the phrase database could be the composer's own past work.
- **Tags:** [accompaniment] [style-transfer] [structure] [symbolic-generation] [controllability]
- **Verification:** verified (arXiv PDFs/abstracts fetched)
- **BibKey:** zhao2021accomontage (and yi2022accomontage2)

### QandA — Q&A: Query-Based Representation Learning for Multi-Track Symbolic Music re-Arrangement
- **Who/where/when:** Jingwei Zhao, Gus Xia, Ye Wang (NUS / NYU Shanghai / MBZUAI); IJCAI 2023 (AI, the Arts and Creativity track)
- **Links:** https://arxiv.org/abs/2306.01635 ; code: https://github.com/zhaojw1998/Query-and-reArrange
- **What it is:** Self-supervised content/style disentanglement for multi-track music: content is learned from the mixture, style (function) from individual tracks, and a query-based decoder re-renders the piece for a new set of tracks. Covers re-instrumentation, piano-cover generation, orchestration (piano → band) and voice separation with the user choosing the target instrumentation.
- **Evidence:** Better multi-track structure and quality than baselines in objective and subjective tests.
- **Why it matters for the studio:** "Arrange this piano sketch for this ensemble" as one operation with chosen tracks — a key compile step for an arranger-workstation heritage.
- **Tags:** [accompaniment] [style-transfer] [symbolic-generation] [controllability]
- **Verification:** verified (arXiv abstract fetched)
- **BibKey:** zhao2023qa

### StructuredArrangement — Structured Multi-Track Accompaniment Arrangement via Style Prior Modelling
- **Who/where/when:** Jingwei Zhao, Gus Xia, Ziyu Wang, Ye Wang (NUS / MBZUAI / NYU Shanghai); NeurIPS 2024 (arXiv Oct 2023)
- **Links:** https://arxiv.org/abs/2310.16334 ; code/demo: https://github.com/zhaojw1998/Structured-Arrangement-Code ; https://proceedings.neurips.cc/paper_files/paper/2024/hash/b95cb2d3f647dae571203bab285077e7-Abstract-Conference.html
- **What it is:** Two-stage "compile" from lead sheet to full band: (1) piano arrangement via texture-style retrieval (AccoMontage lineage), (2) orchestration by infusing per-track *function* styles, modelled as vector-quantised style codes whose long-term flow is generated by a multi-stream Transformer prior — giving whole-song coherence, genre choice and hierarchical control over the arrangement.
- **Evidence:** Higher coherence, structure and quality than baselines with lower compute; whole-song outputs.
- **Why it matters for the studio:** Closest existing system to the founder's arranger-workstation vision (lead sheet in, structured multi-track arrangement out) with editable intermediate piano stage.
- **Tags:** [accompaniment] [structure] [symbolic-generation] [controllability] [style-transfer]
- **Verification:** verified (arXiv abstract fetched; venue via NeurIPS proceedings page)
- **BibKey:** zhao2024structured

### BstarHarmonization — Incorporating Structure and Chord Constraints in Symbolic Transformer-based Melodic Harmonization
- **Who/where/when:** Maximos Kaliakatsos-Papakostas, Konstantinos Soiledis, Konstantinos-Theodoros Tsamis, et al. (Hellenic Mediterranean University / Athena RC / Aristotle University of Thessaloniki); arXiv Dec 2025
- **Links:** https://arxiv.org/abs/2512.07627 ; https://zenodo.org/records/16948248
- **What it is:** Melody harmonisation (Hooktheory, 17,476 lead sheets) with BART and GPT-2 models that accept structure tokens and *user-specified chord constraints* at given bar/beat positions; proposes B* (beam + A* + backtracking) decoding to guarantee the constrained chords appear where requested.
- **Evidence:** Soft constraints satisfied only 50–63% of the time; B* reaches 90–98% at ~400–1,900 model calls; chord-symbol tokens beat pitch-class tokens under constraints.
- **Why it matters for the studio:** Directly addresses "I want this chord here" as a hard constraint in a lead-sheet workflow — an editing-style harmonisation primitive.
- **Tags:** [accompaniment] [controllability] [editing] [symbolic-generation] [notation]
- **Verification:** verified (arXiv PDF/HTML fetched)
- **BibKey:** kaliakatsospapakostas2025harmonization

---

## F. Expressive performance rendering (score → performance → audio)

### VirtuosoNet — VirtuosoNet: A Hierarchical RNN-based System for Modeling Expressive Piano Performance
- **Who/where/when:** Dasaem Jeong, Taegyun Kwon, Yoojin Kim, Juhan Nam (KAIST / SNU); ISMIR 2019
- **Links:** https://archives.ismir.net/ismir2019/paper/000112.pdf ; code: https://github.com/jdasam/virtuosoNet
- **What it is:** MusicXML score (with dynamics/articulation/tempo markings) → expressive performance MIDI (tempo, velocity, onset deviation, articulation, pedal) via a hierarchical attention score encoder, CVAE performance encoder (style latent) and measure→note two-level decoder. Trained on 226 pieces / 1,052 Yamaha e-Competition performances aligned to scores.
- **Evidence:** Five piano students rated three pieces on seven criteria; significant gains over prior systems, near human quality for lyrical melodies.
- **Why it matters for the studio:** Establishes MusicXML→expressive MIDI as a learnable, style-controllable rendering stage and uses score annotations (markings) as inputs.
- **Tags:** [expression-performance] [notation] [controllability]
- **Verification:** verified (ISMIR PDF fetched)
- **BibKey:** jeong2019virtuosonet

### MIDI-DDSP — MIDI-DDSP: Detailed Control of Musical Performance via Hierarchical Modeling
- **Who/where/when:** Yusong Wu, Ethan Manilow, Yi Deng, et al. (Mila / Google Magenta); ICLR 2022
- **Links:** https://arxiv.org/abs/2112.09312 ; code: https://github.com/magenta/midi-ddsp
- **What it is:** Three-level hierarchy for monophonic instruments: notes → expression parameters (volume, vibrato, brightness, attack…) → DDSP synthesis parameters → audio. Users can intervene at any level (edit a note, drag an expression curve, or let priors fill in), giving controllable, realistic rendering of MIDI scores.
- **Evidence:** Listening tests rate synthesis realism close to real recordings on URMP; expression controls verified.
- **Why it matters for the studio:** A model of "compile to audio with every stage editable"; the expression layer is an annotation surface (crescendo, vibrato) between notation and sound.
- **Tags:** [expression-performance] [audio-generation] [controllability] [editing]
- **Verification:** verified (arXiv abstract fetched)
- **BibKey:** wu2022mididdsp

### ScorePerformer / PianoFlow — ScorePerformer: Expressive Piano Performance Rendering with Fine-Grained Control; SyMuPe: Affective and Controllable Symbolic Music Performance
- **Who/where/when:** Ilya Borovik, Vladimir Viro (Peachnote); ISMIR 2023. SyMuPe/PianoFlow: Ilya Borovik, Dmitrii Gavrilev, Vladimir Viro; ACM Multimedia 2025
- **Links:** https://archives.ismir.net/ismir2023/paper/000069.pdf ; https://github.com/ilya16/ScorePerformer ; https://arxiv.org/abs/2511.03425
- **What it is:** ScorePerformer: SPMuple tokens (8 score + 4 performance fields), an MMD-VAE Transformer with hierarchical style embeddings at global/bar/beat/onset level, and *direction-marking classifiers* that map words like crescendo, staccato, ritardando to latent deltas — so a user can steer rendering with score-like directions at any granularity (ASAP: 212 pieces, 937 performances). PianoFlow (SyMuPe): conditional flow matching on 2,968 h of aligned score–performance MIDI (PERiScoPe) with emotion and free-text (Flan-T5) controls; 355 notes/s inference.
- **Evidence:** ScorePerformer: correlation/MAE on tempo, onset deviation, duration, velocity. PianoFlow: 67.1% pairwise win rate (708 ratings, 26 listeners), preferred over human recordings in 54% of comparisons.
- **Why it matters for the studio:** Expression control via *notated directions and text* at bar/beat/note granularity is exactly annotation-driven rendering; real-time-capable.
- **Tags:** [expression-performance] [controllability] [annotation] [text-conditioning] [real-time]
- **Verification:** verified (ISMIR PDF and arXiv abstract fetched)
- **BibKey:** borovik2023scoreperformer (and borovik2025symupe)

### DExter / RenderBox — DExter: Learning and Controlling Performance Expression with Diffusion Models; RenderBox: Expressive Performance Rendering with Text Control
- **Who/where/when:** Huan Zhang, Shreyan Chowdhury, Carlos Cancino-Chacón, Jinhua Liang, Simon Dixon, Gerhard Widmer (QMUL / JKU Linz); Applied Sciences 2024 (arXiv Jun 2024). RenderBox: Huan Zhang, Akira Maezawa, Simon Dixon (QMUL / Yamaha); arXiv Feb 2025
- **Links:** https://arxiv.org/abs/2406.14850 ; https://www.mdpi.com/2076-3417/14/15/6543 ; https://arxiv.org/abs/2502.07711
- **What it is:** DExter: diffusion over performance-parameter sequences conditioned on the score and on perceptual *mid-level features*, enabling interpretation generation, steering and style transfer between performers. RenderBox: a diffusion Transformer that renders score+text ("play it tenderly, slightly rushed") directly to multi-instrument *audio* with curriculum learning from synthesis to expressive performance.
- **Evidence:** DExter matches prior renderers on quantitative metrics and listening tests while capturing time-varying expressive correlations. RenderBox: strong FAD/CLAP, tempo/pitch accuracy and human ratings of naturalness and prompt adherence.
- **Why it matters for the studio:** Text- and feature-steered expression are the "annotate the performance" layer; RenderBox also points to audio-cluster work (score→audio without a MIDI intermediary).
- **Tags:** [expression-performance] [controllability] [text-conditioning] [audio-generation]
- **Verification:** verified (arXiv abstracts fetched)
- **BibKey:** zhang2024dexter (and zhang2025renderbox)

---

## Cross-cluster pointers
- HCI/co-creation cluster: Bach Doodle (Coconet deployment), Composer's Assistant listening/usage studies, MIDI-LLM in-the-wild study (58 musicians), Aria-Duet Disklavier demo, Calliope web app (MIDI-GPT), DeepBach MuseScore plugin.
- Multimodal/annotation cluster: Music SketchNet (sketch-conditioned infilling), WildScore and NOTA (score-image understanding by MLLMs), RenderBox text-controlled rendering, "Not that Groove" NL editing.
- Audio cluster: MIDI-DDSP and RenderBox (symbolic→audio), SymPAC and Aria-MIDI (audio→symbolic transcription pipelines feeding symbolic models), MusicGen/Suno used as comparators by Aria.
- Datasets cluster: Aria-MIDI, GigaMIDI, MetaScore, MidiCaps, MelodyHub, Lakh MIDI, POP909, ASAP, Hooktheory, SOD.
- Evaluation cluster: ZIQI-Eval, ABC-Eval, MusicTheoryBench, Fréchet Music Distance (LC-Diff), unit-test evaluation of edits (Not that Groove), CLaMP-based automatic judging (NotaGen).
