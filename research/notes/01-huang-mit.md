# Cluster 01 — Cheng-Zhi Anna Huang, the MIT / Google Magenta lineage of human-centered music AI, and the wider MIT music-technology lineage

*Research date: 2026-09-07. Verification levels per entry. WebSearch budget ran out mid-task, so late items were verified by direct fetch of known URLs (arXiv HTML, PMLR, Zenodo, MIT pages) rather than search.*

## Overview

This cluster traces one continuous intellectual line: Barry Vercoe's MIT Experimental Music Studio (Csound, the 1984 "Synthetic Performer" that listened and played along) → Tod Machover's Opera of the Future group (Hyperinstruments; Hyperscore, a sketch-based composition tool for novices, 2002–present) → Anna Huang, who did her MIT Media Lab master's in Machover's orbit (2008), spent eight years on Google Brain / DeepMind's Magenta team (Coconet, Music Transformer, Bach Doodle, Cococo, AI Song Contest, Expressive Communication, MIDI-DDSP, ReaLchords) and in Fall 2024 returned to MIT as the Robert N. Noyce Career Development Associate Professor jointly in EECS and Music & Theater Arts, directing the **Human-AI Resonance (HAI-Res)** lab at CSAIL. Huang's Magenta-era work is the single most important body of *empirical* HCI evidence that steering interfaces (voice lanes, semantic sliders, example sliders, alternatives, chunk-wise infilling) change composers' sense of control, ownership and self-efficacy, and that model expressiveness and interface steerability are *complementary* rather than substitutes. Her MIT-era work (2024–2026) pivots hard toward **real-time jamming agents** trained with reinforcement learning (ReaLchords → ReaLJam → GAPT → streaming audio accompaniment; jam_bot with Jordan Rudess; the CHI 2026 "Design Space for Live Music Agents"), plus new latent-editing (LatentFT) and multi-stem (Stemphonic) generation. The Magenta team itself continued the "AI as tool for musicians, never a replacement" line with Magenta RealTime (2025) and Magenta RealTime 2 (June 2026, DAW-integrated, MIDI-controllable, ~200 ms). Alongside, MIT's other music-technology faculty supply the studio's *symbolic infrastructure* (Michael Cuthbert's music21 — the de-facto Python toolkit for notation parsing, Roman-numeral analysis, corpus search and MusicXML/MIDI/LilyPond export, taught in 21M.383) and its *interaction pedagogy* (Eran Egozy's 21M.385 Interactive Music Systems, ConcertCue, and the Harmonix game lineage). MIT formally launched a Music Technology and Computation graduate program (SM/MASc) in Fall 2024, with Egozy as director and Huang as core faculty.

## Key takeaways for the studio

1. **Nonlinear, rewrite-style generation is the Huang paradigm, not left-to-right.** Coconet's abstract literally says composers "write music in a nonlinear fashion, scribbling motifs here and there, often revisiting choices," and models this with blocked-Gibbs infilling. This is the closest ML analogue to the founder's compose → annotate → edit → *compile* loop: the AI fills the masked parts the human leaves open.
2. **Steering tools measurably shift ownership to the human.** Cococo (CHI 2020, N=21) shows Voice Lanes, Semantic Sliders, Example-Based Sliders and Multiple Alternatives raise controllability (5.9 vs 3.5/7), ownership (5.2 vs 3.8) and sense of collaboration; the paper argues generative power "may need to be partitioned into smaller, semantically meaningful tools." Design the "compile" step as a set of such partitioned, semantic controls rather than one big button.
3. **Better models and better interfaces are complementary.** Expressive Communication (IUI 2022; 26 composers, 1,020 listener comparisons) found steering interfaces gave the *bigger* gains in ownership/control/efficacy, while the more expressive model (Music Transformer vs PerformanceRNN) gave better listener-judged musicality. Invest in both; do not assume a stronger model removes the need for controls.
4. **Practitioners decompose songs into modules and curate.** The AI Song Contest study (13 teams, 61 people) found teams ran multiple small models aligned to "musical building blocks," generated massively and curated post hoc, and asked for systems that are "decomposable, steerable, interpretable, and adaptive." The studio's compile step should be modular per layer (melody, harmony, bass, drums, structure) and expose ranking/curation.
5. **Real-time accompaniment is now RL-shaped and open.** ReaLchords (ICML 2024) → ReaLJam (CHI EA 2025) → GAPT (ICLR 2026) show how to make a chord-accompaniment agent that anticipates, adapts within 2–3 beats to a key change, and avoids reward-hacking collapse; PyTorch code is public (realchords-pytorch). A "jam mode" in the studio can build on this.
6. **Anticipation must be visualized.** ReaLJam's "waterfall" of committed (opaque) vs. tentative (translucent) chords, and jam_bot's preview screen + kill-switch, are concrete UI patterns for showing an agent's plan so the human retains agency.
7. **Sketch-to-music has a 25-year MIT pedigree.** Hyperscore (Farbood/Machover, 2002; web relaunch 2022) lets novices draw colored contour lines that map to motives and a harmony line; it is the direct ancestor of "scribble to compose" and proves the concept with children in Toy Symphony. Study its motive-window/sketch-window split.
8. **music21 is the symbolic backbone to adopt, not rebuild.** v10.5.0 (June 2026), BSD-3, Python ≥3.12: parses MusicXML/MIDI/ABC/Humdrum, does key and Roman-numeral analysis, ships a corpus (all 371 Bach chorales via `corpus.chorales.Iterator`, Palestrina, Beethoven quartets, Essen, O'Neill's), exports MusicXML/MIDI/LilyPond. Cuthbert's OCW course shows how to teach corpus-driven theory with it.
9. **Live models are moving into the DAW at consumer latency.** Magenta RealTime 2 (2026: 40 ms frames, ~200 ms control latency, MIDI note control, Apple Silicon) and Live Music Diffusion Models (~30 ms, JUCE, gaming laptop) mean audio rendering/jamming layers can run locally in a plugin.
10. **Evaluate co-creation with both composer self-report and listener judgments** (Expressive Communication framework), and expect musicians to resist "collaborator" framing while embracing "tool that supports ideation" framing (Krol et al., CHI 2025 — cross-cluster).

---

## Entries

### Chordripple — Chordripple: Recommending Chords to Help Novice Composers Go Beyond the Ordinary
- **Who/where/when:** Cheng-Zhi Anna Huang, David Duvenaud, Krzysztof Z. Gajos; Harvard University; ACM IUI, 2016
- **Links:** https://doi.org/10.1145/2856767.2856792 ; listed on https://czhuang.github.io/
- **What it is:** A chord-recommendation tool for novice composers. As the user writes a chord progression, Chordripple suggests replacement or next chords, ranked by a learned chord embedding (a word2vec-style "chord2vec" trained on a pop/rock corpus) so that suggestions are both plausible and "beyond the ordinary." The human keeps authorship: the system only proposes, and proposals are ranked by adventurousness.
- **Evidence:** User study with novice composers comparing recommendation conditions; Huang's page lists it as an IUI 2016 full paper (details of N and metrics not re-verified).
- **Why it matters for the studio:** Earliest Huang work on *recommendation as steering* in a symbolic (chord) representation — a lightweight "suggest, don't dictate" pattern for the harmony layer of the studio.
- **Tags:** [symbolic-generation] [controllability] [creativity-support] [HCI-study] [representation]
- **Verification:** partial (title/venue/year verified from Huang's homepage; system details from recall)
- **BibKey:** huang2016chordripple

### Coconet — Counterpoint by Convolution
- **Who/where/when:** Cheng-Zhi Anna Huang, Tim Cooijmans, Adam Roberts, Aaron Courville, Douglas Eck; Google Brain / Université de Montréal; ISMIR 2017 (arXiv 1903.07227)
- **Links:** https://arxiv.org/abs/1903.07227 ; code in Magenta: https://github.com/magenta/magenta/tree/main/magenta/models/coconet
- **What it is:** A convolutional model over a piano-roll of four voices (JSB chorales) trained as an orderless NADE to *complete partial scores*: any subset of notes can be masked and re-sampled. Generation uses blocked Gibbs sampling as "an analogue to rewriting." Input: a partial score with arbitrary masks; output: completed four-voice counterpoint. The human controls *which* cells are fixed vs. regenerated, in any order.
- **Evidence:** Gibbs sampling beat ancestral sampling on both log-likelihood and human evaluation; abstract states this is because some conditional distributions are poorly modelled. The abstract's framing: "human composers write music in a nonlinear fashion, scribbling motifs here and there, often revisiting choices previously made."
- **Why it matters for the studio:** The canonical *infilling-as-editing* model: the composer authors some material, leaves holes, and the model "compiles" the rest; then the composer re-masks and re-runs. Directly underlies the Bach Doodle and Cococo.
- **Tags:** [symbolic-generation] [infilling] [editing] [notation] [controllability]
- **Verification:** verified (arXiv abstract fetched; authors/venue from Huang's homepage)
- **BibKey:** huang2017coconet

### MusicTransformer — Music Transformer: Generating Music with Long-Term Structure
- **Who/where/when:** Cheng-Zhi Anna Huang, Ashish Vaswani, Jakob Uszkoreit, Noam Shazeer, Ian Simon, Curtis Hawthorne, Andrew M. Dai, Matthew D. Hoffman, Monica Dinculescu, Douglas Eck; Google Brain; ICLR 2019 (arXiv 1809.04281, Sept 2018)
- **Links:** https://arxiv.org/abs/1809.04281 ; https://openreview.net/forum?id=rJe4ShAcF7 ; https://magenta.withgoogle.com/music-transformer
- **What it is:** Transformer with relative self-attention whose memory cost is reduced from quadratic to linear in sequence length, enabling minute-long performance-MIDI generation with repeated motifs and ABA-like structure. Demonstrated three modes: unconditioned generation, *continuation of a given motif*, and seq2seq *melody → accompaniment*. Trained on JSB Chorales and Piano-e-Competition (MAESTRO precursor).
- **Evidence:** State-of-the-art NLL on Piano-e-Competition; listening studies preferred it over PerformanceRNN and vanilla Transformer. Huang's homepage claims it is the most-cited music-generation paper at ICLR.
- **Why it matters for the studio:** The workhorse symbolic model of the lineage; the melody→accompaniment seq2seq mode is a literal "compile a lead sheet into a piano part" primitive, and motif-continuation supports iterative development of human-authored ideas.
- **Tags:** [symbolic-generation] [structure] [accompaniment] [expression-performance]
- **Verification:** verified (arXiv abstract fetched)
- **BibKey:** huang2018musictransformer

### InfillingPiano — Infilling Piano Performances
- **Who/where/when:** Daphne Ippolito, Anna Huang, Curtis Hawthorne, Douglas Eck; Google Brain; NeurIPS 2018 Workshop on Machine Learning for Creativity and Design
- **Links:** listed on https://czhuang.github.io/ ; workshop: https://neurips2018creativity.github.io/
- **What it is:** Extends Music Transformer-style performance modelling to *fill in a missing middle section* of an expressive piano performance given the surrounding context, i.e. infilling in the performance-MIDI (event-token) domain rather than the piano-roll domain of Coconet. A companion workshop paper ("Transformer-NADE for Piano Performances", same venue) explores orderless training for the same goal.
- **Evidence:** Workshop paper; qualitative examples.
- **Why it matters for the studio:** Shows that the "leave a hole, let the AI compile it" operation extends to expressive timing/velocity data, not just notes — relevant when the studio edits *performances* rather than scores.
- **Tags:** [symbolic-generation] [infilling] [editing] [expression-performance]
- **Verification:** partial (title/venue from Huang's homepage; content from recall)
- **BibKey:** ippolito2018infilling

### MusicVAE — A Hierarchical Latent Vector Model for Learning Long-Term Structure in Music
- **Who/where/when:** Adam Roberts, Jesse Engel, Colin Raffel, Curtis Hawthorne, Douglas Eck; Google Brain (Magenta); ICML 2018 (arXiv 1803.05428)
- **Links:** https://arxiv.org/abs/1803.05428 ; https://github.com/magenta/magenta/tree/main/magenta/models/music_vae ; https://magenta.withgoogle.com/music-vae
- **What it is:** A recurrent VAE with a hierarchical "conductor" decoder that emits embeddings per bar, then decodes each bar, avoiding posterior collapse and enabling 16-bar melodies, drum patterns and trios. The human controls generation via the latent space: sampling, *interpolation between two clips*, and attribute vectors. Backs Magenta Studio's Generate/Interpolate and the AI Song Contest teams' workflows.
- **Evidence:** "Dramatically better sampling, interpolation, and reconstruction performance than a flat baseline"; listening tests on interpolations.
- **Why it matters for the studio:** Latent-space interpolation is a concrete *edit primitive* ("morph my A-section groove toward my B-section groove"); MusicVAE is the reference open implementation.
- **Tags:** [symbolic-generation] [representation] [editing] [controllability] [structure]
- **Verification:** verified (arXiv abstract fetched)
- **BibKey:** roberts2018musicvae

### PianoGenie — Piano Genie
- **Who/where/when:** Chris Donahue, Ian Simon, Sander Dieleman; Google Brain (Magenta) / UCSD / DeepMind; ACM IUI 2019 (arXiv 1810.05246)
- **Links:** https://arxiv.org/abs/1810.05246 ; https://magenta.withgoogle.com/pianogenie ; https://github.com/magenta/magenta/tree/main/magenta/models/piano_genie
- **What it is:** An "intelligent controller": eight buttons are decoded in real time into plausible 88-key piano music by an RNN autoencoder with a discrete bottleneck; musically meaningful constraints on the encoder make button contour map to pitch contour. Input: button presses with timing; output: piano notes. The human controls rhythm, phrasing, and rough melodic contour; the model fills in exact pitches.
- **Evidence:** IUI paper with qualitative/user evaluation; widely demoed.
- **Why it matters for the studio:** A gesture-level "sketch → notes" mapping: the user supplies contour and rhythm (very close to humming/scribbling a line), the model compiles pitches. A template for low-fidelity human input steering high-fidelity output.
- **Tags:** [real-time] [controllability] [sketch] [symbolic-generation] [creativity-support]
- **Verification:** verified (arXiv abstract fetched)
- **BibKey:** donahue2019pianogenie

### BachDoodle — The Bach Doodle: Approachable Music Composition with Machine Learning at Scale
- **Who/where/when:** Cheng-Zhi Anna Huang, Curtis Hawthorne, Adam Roberts, Monica Dinculescu, James Wexler, Leon Hong, Jacob Howcroft; Google Brain / Google Doodles; ISMIR 2019 (arXiv 1907.06637)
- **Links:** https://arxiv.org/abs/1907.06637 ; dataset: https://magenta.withgoogle.com/datasets/bach-doodle ; interactive: https://www.google.com/doodles/celebrating-johann-sebastian-bach
- **What it is:** Google's first AI-powered Doodle (March 2019). Users enter a two-bar melody on a simplified sheet-music grid; Coconet (re-implemented in TensorFlow.js, quantized to ~400 KB, 40 s → 2 s) harmonizes it into four voices in Bach style, running in-browser or on Cloud TPU depending on a speed calibration. Users could rate results and opt in to a public dataset.
- **Evidence:** >55 million harmonization queries in three days, 350 cumulative years of engagement. The released Bach Doodle Dataset contains 21.6 million harmonizations from 8.5 million sessions (melody, harmonization, rating, country, session duration, playback count), CC BY 4.0.
- **Why it matters for the studio:** Proof at planetary scale that *human-authored melody → AI-compiled harmonization* on a notation surface is approachable for total novices; the dataset is a unique record of how people rate AI harmonizations of their own material.
- **Tags:** [symbolic-generation] [notation] [infilling] [dataset] [education] [product] [HCI-study]
- **Verification:** verified (arXiv abstract and dataset page fetched)
- **BibKey:** huang2019bachdoodle

### MagentaStudio — Magenta Studio: Augmenting Creativity with Deep Learning in Ableton Live
- **Who/where/when:** Adam Roberts, Jesse Engel, Yotam Mann, Jon Gillick, Claire Kayacik, Signe Nørly, Monica Dinculescu, Carey Radebaugh, Curtis Hawthorne, Douglas Eck; Google Brain (Magenta); MUME workshop 2019; v2.0 as Ableton Live 10.1+ Max-for-Live device
- **Links:** https://magenta.withgoogle.com/studio ; https://github.com/tensorflow/magenta-studio
- **What it is:** Five DAW-plugin tools wrapping Magenta models: Continue (RNN continues a melody/drum clip up to 32 bars), Generate (MusicVAE 4-bar phrases), Interpolate (MusicVAE, up to 16 clips between two), Groove (GrooVAE humanizes drum timing/velocity, trained on ~15 h of drummer recordings), Drumify (GrooVAE turns any rhythm into a drum groove). Inputs/outputs are MIDI clips in Live; controls are temperature, variation count and clip selection.
- **Evidence:** Product deployment; workshop paper describes design goals (the standalone versions are no longer maintained).
- **Why it matters for the studio:** The reference example of generative tools packaged as *small, composable DAW operations* on user clips rather than a text-to-song box; the exact "operate on my material" granularity the founder wants.
- **Tags:** [DAW-plugin] [product] [symbolic-generation] [editing] [toolkit]
- **Verification:** verified (official page fetched); workshop-paper citation partial
- **BibKey:** roberts2019magentastudio

### MagentaJS — Magenta.js: A JavaScript Library for Music Generation (and the Magenta ecosystem)
- **Who/where/when:** Adam Roberts, Curtis Hawthorne, Ian Simon et al.; Google Brain (Magenta); ISMIR 2018 late-breaking/demo; library 2018–present
- **Links:** https://github.com/magenta/magenta-js ; https://magenta.withgoogle.com/
- **What it is:** TensorFlow.js ports of Magenta models (MusicVAE, MusicRNN, Coconet, Piano Genie, DDSP, etc.) with a NoteSequence protobuf as the shared symbolic representation, enabling browser-native co-creation demos (Bach Doodle, Cococo, Tone Transfer). Apache-2.0.
- **Evidence:** Demo paper; dozens of public web demos built on it.
- **Why it matters for the studio:** If the studio has a web front end, magenta-js and the NoteSequence schema are ready-made pieces for symbolic in-browser inference and interchange.
- **Tags:** [toolkit] [representation] [symbolic-generation]
- **Verification:** partial (repo known; demo-paper venue from recall)
- **BibKey:** roberts2018magentajs

### Cococo — Novice-AI Music Co-Creation via AI-Steering Tools for Deep Generative Models
- **Who/where/when:** Ryan Louie, Andy Coenen, Cheng-Zhi Anna Huang, Michael Terry, Carrie J. Cai; Northwestern University / Google Research; ACM CHI 2020
- **Links:** https://doi.org/10.1145/3313831.3376739 ; PDF: https://youralien.github.io/files/cococo_chi2020_copy.pdf ; demo video: https://www.youtube.com/watch?v=jmlc-0pHcOw
- **What it is:** A web notation/piano-roll editor on top of Coconet with four "AI-steering tools": **Voice Lanes** (restrict generation to chosen voices and time spans), **Example-Based Sliders** (similarity to a reference passage), **Semantic Sliders** (conventional↔surprising via temperature; happy↔sad via major/minor triad bias), and **Multiple Alternatives** (audition several fills). All implemented as "soft priors" on Coconet's sampling distribution, no retraining. Input: partial four-voice score + slider settings; output: infilled score the user keeps editing.
- **Evidence:** Needfinding study found the baseline AI "overwhelm[s] users with the amount of musical content" and frustrates with non-determinism. Summative within-subjects study, N=21 novices, 15-min tasks: Cococo beat the conventional infilling interface on controllability (5.9 vs 3.5), comprehensibility (5.3 vs 3.2), sense of collaboration (5.9 vs 4.0), self-efficacy (5.9 vs 3.7), ownership (5.2 vs 3.8), creative expression (5.5 vs 3.8), all p<0.01. Users built pieces "bit-by-bit" voice-by-voice and used "generate, audition, edit" loops; one described the system as "an art assistant, who is extremely proficient, but has a clear understanding of who is in control." Authors: generative capabilities "may need to be partitioned into smaller, semantically meaningful tools to promote effective co-creation."
- **Why it matters for the studio:** The best-documented blueprint for the studio's edit/annotate/compile UI: annotations (lanes, sliders, examples) become constraints on a compile step; the study quantifies their effect on ownership.
- **Tags:** [HCI-study] [co-creation-framework] [controllability] [infilling] [editing] [notation] [creativity-support] [mixed-initiative]
- **Verification:** verified (author PDF fetched)
- **BibKey:** louie2020cococo

### AISongContest — AI Song Contest: Human-AI Co-Creation in Songwriting
- **Who/where/when:** Cheng-Zhi Anna Huang, Hendrik Vincent Koops, Ed Newton-Rex, Monica Dinculescu, Carrie J. Cai; Google Brain / RTL Netherlands / ByteDance; ISMIR 2020 (arXiv 2010.05388)
- **Links:** https://arxiv.org/abs/2010.05388 ; https://www.aisongcontest.com/
- **What it is:** Survey-based thematic analysis of how 13 teams (61 people, 2–15 per team, median 4) built songs with AI for the 2020 VPRO AI Song Contest. Not a system: a field study of real co-creation workflows across lyrics, melody, harmony, bass, drums, vocal/instrument synthesis and structure.
- **Evidence:** Teams used a median of 4 model types (GPT-2, CharRNN, MusicVAE, Coconet, DrumRNN, WaveNet, GANs…); "rarely attempted end-to-end generation"; generated massively and curated post hoc (one team 450 melodies; another 10,000 lyric lines); steered by priming inputs, fine-tuning on curated data, latent interpolation; manually authored structure because small models lack "holistic context." One team described "jamming with another musician… priming the AI with chord progressions, hearing AI output, riffing on that output." Conclusion: need interfaces that are "more decomposable, steerable, interpretable, and adaptive."
- **Why it matters for the studio:** Independent evidence that expert practitioners *already* work in the founder's modular, iterative way and want the AI to fit into it; the four adjectives are a ready-made requirements list.
- **Tags:** [HCI-study] [co-creation-framework] [controllability] [structure] [evaluation]
- **Verification:** verified (arXiv PDF fetched)
- **BibKey:** huang2020aisongcontest

### DDSP — DDSP: Differentiable Digital Signal Processing
- **Who/where/when:** Jesse Engel, Lamtharn (Hanoi) Hantrakul, Chenjie Gu, Adam Roberts; Google Brain (Magenta); ICLR 2020 (arXiv 2001.04643)
- **Links:** https://arxiv.org/abs/2001.04643 ; https://github.com/magenta/ddsp ; https://magenta.withgoogle.com/ddsp
- **What it is:** A library of differentiable synthesizer/effects modules (harmonic additive synth, filtered noise, reverb) so neural nets output *interpretable synthesis parameters* (f0, loudness, harmonic distribution) instead of raw waveforms. Enables independent control of pitch and loudness, extrapolation to unseen pitches, dereverberation, and timbre transfer between instruments with small models.
- **Evidence:** High-fidelity monophonic resynthesis without autoregressive or adversarial models; ablations in the paper.
- **Why it matters for the studio:** The interpretable-parameter approach is how a rendering layer can stay *editable* after generation (nudge vibrato, change loudness curve) rather than being a fixed audio blob — consistent with the "compile, then edit again" loop.
- **Tags:** [audio-generation] [controllability] [style-transfer] [toolkit] [expression-performance]
- **Verification:** verified (arXiv abstract fetched)
- **BibKey:** engel2020ddsp

### ToneTransfer — Tone Transfer (DDSP in the browser)
- **Who/where/when:** Magenta + Google AIUX teams; Google Research; released 1 Oct 2020
- **Links:** https://magenta.withgoogle.com/tone-transfer ; https://sites.research.google/tonetransfer
- **What it is:** Web app: record or upload humming/singing/any instrument; SPICE extracts pitch, a DDSP model (TF.js) re-renders it as flute, saxophone, violin, trumpet, etc. The human controls the input performance (pitch contour, dynamics, timing) and picks the target instrument; UX research explicitly targeted non-Western instruments as inputs.
- **Evidence:** Product; user research described on the blog; year-long Magenta/AIUX collaboration.
- **Why it matters for the studio:** Concrete precedent for **humming as input** to a musical rendering step; the whole pipeline (sing → pitch → timbre) is exactly the founder's "hum an idea, get an instrument line."
- **Tags:** [humming] [multimodal-input] [audio-generation] [style-transfer] [product]
- **Verification:** verified (official page fetched)
- **BibKey:** magenta2020tonetransfer

### CompositionalSteering — Compositional Steering of Music Transformers
- **Who/where/when:** Halley Young, Vincent Dumoulin, Pablo Samuel Castro, Jesse Engel, Cheng-Zhi Anna Huang; Google Brain / UPenn; HAI-GEN Workshop at ACM IUI 2021
- **Links:** listed on https://czhuang.github.io/ ; workshop: https://hai-gen.github.io/2021/
- **What it is:** Steers a pretrained Music Transformer at sampling time by *composing* several lightweight attribute controls (e.g., pitch-range, density, key) into one product-of-experts-style distribution, so users can combine constraints without retraining the base model.
- **Evidence:** Workshop paper; quantitative attribute-adherence results (details not re-verified).
- **Why it matters for the studio:** A route to letting many simultaneous annotations ("keep this in the low register, denser here, stay in D minor") jointly constrain a compile step on a frozen model.
- **Tags:** [controllability] [symbolic-generation] [annotation]
- **Verification:** partial (title/venue verified via homepage; method from recall)
- **BibKey:** young2021compositionalsteering

### MIDIDDSP — MIDI-DDSP: Detailed Control of Musical Performance via Hierarchical Modeling
- **Who/where/when:** Yusong Wu, Ethan Manilow, Yi Deng, Rigel Swavely, Kyle Kastner, Tim Cooijmans, Aaron Courville, Cheng-Zhi Anna Huang, Jesse Engel; Mila/Université de Montréal, Northwestern, Google Brain; ICLR 2022 oral (arXiv 2112.09312); Outstanding Paper at NeurIPS 2021 CtrlGen workshop
- **Links:** https://arxiv.org/abs/2112.09312 ; https://github.com/magenta/midi-ddsp
- **What it is:** Three-level hierarchy **notes → performance → synthesis**: from MIDI it predicts per-note expression (vibrato, dynamics, articulation, brightness…), then DDSP synthesis parameters, then audio (URMP monophonic instruments). Users can intervene at any level — write notes, tweak an expression curve, or edit synthesis parameters — or let learned priors fill in.
- **Evidence:** Reconstructs high-fidelity audio, predicts performance attributes, allows independent manipulation of expression, and renders new note sequences realistically (listening tests in paper).
- **Why it matters for the studio:** The clearest published instance of a *compiler with intermediate representations*: score → expressive performance → sound, every stage human-editable. Maps one-to-one onto the founder's "compile" metaphor.
- **Tags:** [expression-performance] [audio-generation] [controllability] [editing] [representation] [notation]
- **Verification:** verified (arXiv abstract fetched)
- **BibKey:** wu2022mididdsp

### ExpressiveCommunication — Expressive Communication: A Common Framework for Evaluating Developments in Generative Models and Steering Interfaces
- **Who/where/when:** Ryan Louie, Jesse Engel, Cheng-Zhi Anna Huang; Northwestern University / Google Research; ACM IUI 2022 (arXiv 2111.14951)
- **Links:** https://arxiv.org/abs/2111.14951 ; https://doi.org/10.1145/3490099.3511159
- **What it is:** An evaluation framework and 2×2 study: two models (PerformanceRNN vs Music Transformer) × two interfaces ("Radio" — curate random full phrases — vs "Steering" — chunk-by-chunk composition with semantic filtering). Composers write music to express a given image/word; listeners judge whether it communicates the intended feeling and how musical it is.
- **Evidence:** 26 composers made 100+ pieces; 20 listeners gave 1,020 head-to-head comparisons. Steering interface: ownership 4.8 vs 2.42, control 5.0 vs 2.58 (p<1e-6); its pieces better evoked target feelings and sounded more musical. Music Transformer: preferred for feeling (p<0.001) and musicality (p<1e-5). Steering mattered most when the target emotion (e.g., fear) fought the model's bias. Conclusion: "more expressive models and more steerable interfaces are important and complementary."
- **Why it matters for the studio:** Gives the studio an evaluation protocol (composer self-report + blind listener judgments of communicative intent) and evidence to justify investing in editing/steering UI even as models improve.
- **Tags:** [evaluation] [HCI-study] [co-creation-framework] [controllability] [creativity-support]
- **Verification:** verified (arXiv PDF fetched)
- **BibKey:** louie2022expressivecommunication

### DDSPVST — DDSP-VST (neural synth/effect plugin + web trainer)
- **Who/where/when:** Magenta team (Jesse Engel et al.); Google; 2022
- **Links:** https://magenta.withgoogle.com/ddsp-vst ; https://github.com/magenta/ddsp-vst
- **What it is:** macOS/Windows VST/AU plugins: a MIDI-playable neural synthesizer and an audio effect that re-timbres any input while preserving pitch and dynamics; a free Colab web trainer builds a personal model from "as little as a couple minutes of audio."
- **Evidence:** Product release; no formal study.
- **Why it matters for the studio:** Shows the founder's "insert example audio" annotation can literally become a *trained timbre* in minutes and live inside the DAW.
- **Tags:** [DAW-plugin] [audio-generation] [style-transfer] [product] [multimodal-input]
- **Verification:** verified (official page fetched; release year from recall)
- **BibKey:** magenta2022ddspvst

### ReaLchords — Adaptive Accompaniment with ReaLchords
- **Who/where/when:** Yusong Wu, Tim Cooijmans, Kyle Kastner, Adam Roberts, Ian Simon, Alexander Scarlatos, Chris Donahue, Cassie Tarakajian, Shayegan Omidshafiei, Aaron Courville, Pablo Samuel Castro, Natasha Jaques, Cheng-Zhi Anna Huang; Google DeepMind / Mila; ICML 2024, PMLR 235:53328–53345 (arXiv 2506.14723)
- **Links:** https://proceedings.mlr.press/v235/wu24c.html ; https://arxiv.org/abs/2506.14723 ; audio: https://storage.googleapis.com/realchords/index.html ; PyTorch reimplementation: https://github.com/lukewys/realchords-pytorch
- **What it is:** An *online* (causal, no future access) chord-accompaniment model for a live melody. Frame-based at 16th-note resolution (≤256 frames), 5,041-chord vocabulary, 8-layer decoder (512-d). Pretrained by MLE on ~38k Hooktheory melody–chord pairs, then RL-finetuned with (a) self-supervised reward models (contrastive InfoNCE and discriminative, multi-scale) scoring harmonic *and temporal* coherence and (b) a KL term distilling from an offline encoder-decoder teacher that *can* see the future melody — "forcing anticipation."
- **Evidence:** Note-in-chord ratio 54.3% (ReaLchords-M) vs 37.0% for online MLE; recovers from a tritone transposition at beat 17 within 2–3 beats (MLE never does); listening test with 10 musicians, 192 pairwise comparisons: significantly preferred over MLE and distillation-only baselines; self-supervised rewards correlated with human judgments.
- **Why it matters for the studio:** The state-of-the-art recipe for a responsive harmonic partner that follows the *human's* line rather than the reverse; symbolic (chord-symbol) output plugs straight into a lead-sheet workflow.
- **Tags:** [real-time] [accompaniment] [symbolic-generation] [mixed-initiative] [evaluation]
- **Verification:** verified (PMLR page + arXiv HTML fetched)
- **BibKey:** wu2024realchords

### ReaLJam — ReaLJam: Real-Time Human-AI Music Jamming with Reinforcement Learning-Tuned Transformers
- **Who/where/when:** Alexander Scarlatos, Yusong Wu, Ian Simon, Adam Roberts, Tim Cooijmans, Natasha Jaques, Cassie Tarakajian, Cheng-Zhi Anna Huang; UMass Amherst / Mila / Google DeepMind / UW; CHI 2025 Extended Abstracts (arXiv 2502.21267)
- **Links:** https://arxiv.org/abs/2502.21267 ; https://doi.org/10.1145/3706599.3720227
- **What it is:** Web interface + client-server protocol wrapping ReaLchords for live jamming: user plays melody on a MIDI keyboard or computer keys; agent outputs chords. Key idea is **anticipation**: the agent continually predicts how the performance will unfold and shows upcoming chords in a "waterfall" descending toward the piano — committed chords opaque, revisable predictions semi-transparent. Round-trip latency typically <100 ms at 150 BPM. Three model variants (MLE, RL-S, RL-M) and many user-adjustable settings.
- **Evidence:** N=6 experienced musicians, 60-min sessions (baseline + 8 modified settings + free choice). Enjoyment 4.3/5, adaptation 2.7/5; RL-trained models beat the pretrained one on all measures; users valued "surprise" that still matched expectation, wanted genre control and structure awareness; preferences for settings varied strongly by individual and did not always match objective ratings.
- **Why it matters for the studio:** Concrete UI for *showing an agent's plan before it commits* — the visual language the studio needs whenever the AI proposes material in real time; plus evidence that customization per musician is essential.
- **Tags:** [real-time] [accompaniment] [HCI-study] [mixed-initiative] [controllability]
- **Verification:** verified (arXiv PDF fetched)
- **BibKey:** scarlatos2025realjam

### JamBot — The jam_bot, a Real-Time System for Collaborative Free Improvisation with Music Language Models
- **Who/where/when:** Lancelot Blanchard, Perry Naseck, Stephen Brade, Kimaya Lecamwasam, Jordan Rudess, Cheng-Zhi Anna Huang, Joseph A. Paradiso; MIT Media Lab (Responsive Environments) + HAI-Res; ISMIR 2025 (Daejeon); DOI 10.5281/zenodo.17706584
- **Links:** https://zenodo.org/records/17706584 ; https://ismir2025program.ismir.net/poster_321.html ; project: https://arts.mit.edu/jordan-rudess-mit/
- **What it is:** A stage system that improvises with Dream Theater keyboardist Jordan Rudess (CAST Visiting Artist). Built on Music Transformer, fine-tuned on Rudess's own recorded basslines, chords and melodies; the model is prompted into distinct *roles* (lead, accompaniment, call-and-response) via modified context/conditioning; a low-latency multi-threaded scheduler "listens, and prompts and schedules model generations seamlessly." A preview screen shows upcoming decisions; restart and kill-switch preserve performer agency; a kinetic petal sculpture (Naseck) externalizes the AI's state. Premiered 21 Sept 2024 (work-in-progress) and later in a sold-out concert.
- **Evidence:** Year-long co-design with a virtuoso; critical acclaim; no controlled study.
- **Why it matters for the studio:** Demonstrates *personalized* symbolic models (fine-tuned on one artist's material) with explicit role assignment — a model for the studio letting a composer "compile" in their own voice — and again the pattern of previewing AI intent.
- **Tags:** [real-time] [accompaniment] [mixed-initiative] [expression-performance] [symbolic-generation]
- **Verification:** verified (Zenodo + ISMIR program + Arts at MIT pages fetched)
- **BibKey:** blanchard2025jambot

### LiveMusicModels — Live Music Models (Magenta RealTime & Lyria RealTime)
- **Who/where/when:** Lyria Team, Google DeepMind (Adam Roberts, Chris Donahue, Kehang Han, Antoine Caillon, Brian McWilliams, Cassie Tarakajian, Ian Simon, Ilaria Manco, Jesse Engel, Noah Constant et al.; Huang listed among contributors); arXiv 2508.04651, Aug 2025
- **Links:** https://arxiv.org/abs/2508.04651 ; https://github.com/magenta/magenta-realtime ; https://huggingface.co/google/magenta-realtime
- **What it is:** Defines "live music models": generate a continuous audio stream in real time with synchronized user control. Magenta RealTime (open weights; 770M "Large", 220M base) generates 2-second chunks with a 10-second context, steerable by text and/or audio prompts blended by weight; Lyria RealTime is the API model with extra controls (tempo, density, brightness, instrumentation).
- **Evidence:** Outperforms other open-weights music models on automatic quality metrics despite fewer parameters; RTF 1.8× on an H100.
- **Why it matters for the studio:** The first open, steerable *streaming* audio model — a candidate rendering/jam engine; its 2-s chunk latency is the baseline that MRT2 later crushed.
- **Tags:** [audio-generation] [real-time] [text-conditioning] [controllability] [toolkit]
- **Verification:** verified (arXiv abstract + HTML fetched)
- **BibKey:** roberts2025livemusicmodels

### MagentaRT2 — Magenta RealTime 2
- **Who/where/when:** Magenta / Lyria team, Google DeepMind; released 4 June 2026
- **Links:** https://magenta.withgoogle.com/magenta-realtime-2 ; https://github.com/magenta/magenta-realtime ; https://huggingface.co/google/magenta-realtime-2
- **What it is:** Open-weights live music model moving from 2-second chunks to frame-level autoregression (40 ms frames), control latency ~200 ms (vs ~3 s), running in real time on Apple Silicon (230M "small" on any M-series; 2.4B "base" on Pro/Max chips) with a Python library, C++ inference engine and direct DAW integration. Controls: text prompts, audio clips for style, and **MIDI input for note and timing control** plus drums on/off. Uses MusicCoCa style embeddings and the SpectroStream codec. Code Apache-2.0.
- **Evidence:** Blog claims ~15× lower latency than v1; no published study yet.
- **Why it matters for the studio:** A locally runnable, MIDI-steerable audio layer that can render or jam on top of the studio's symbolic material inside a plugin. The blog restates the lineage's creed: "For a decade, the Magenta team has championed a vision of AI as a tool for musicians, never a replacement."
- **Tags:** [audio-generation] [real-time] [DAW-plugin] [controllability] [product]
- **Verification:** verified (official blog + GitHub fetched)
- **BibKey:** magenta2026realtime2

### GAPT — Generative Adversarial Post-Training Mitigates Reward Hacking in Live Human-AI Music Interaction
- **Who/where/when:** Yusong Wu, Stephen Brade, Aleksandra Teng Ma, Tia-Jane Fowler, Enning Yang, Berker Banar, Aaron Courville, Natasha Jaques, Cheng-Zhi Anna Huang; Mila / MIT / Georgia Tech / UW / McGill; ICLR 2026 (arXiv 2511.17879)
- **Links:** https://arxiv.org/abs/2511.17879 ; code: https://github.com/lukewys/realchords-pytorch ; audio: https://realchords-GAPT.github.io
- **What it is:** Addresses "reward hacking" in RL post-training of ReaLchords-style melody→chord agents, where coherence rewards drive collapse to "repetitive, trivial, and low-coverage chord choices." Adds a co-evolving discriminator that separates policy trajectories from real data; the policy maximizes discriminator output alongside coherence rewards, with a two-phase (warm-up then confidence-gated) update schedule.
- **Evidence:** Simulation with fixed melodies and learned melody agents (Pareto frontier of harmony ~85% note-in-chord vs Vendi-score diversity); in-person study with **12 expert musicians**, three anonymized systems × three tasks; GAPT rated highest on adaptation quality, adaptation speed and perceived control/agency, significantly beating ReaLchords on speed and agency (p<0.05).
- **Why it matters for the studio:** Shows *diversity* must be an explicit training target for a co-creative agent or it becomes boring; also the first open PyTorch stack for the whole ReaLchords family.
- **Tags:** [real-time] [accompaniment] [HCI-study] [evaluation] [symbolic-generation]
- **Verification:** verified (arXiv HTML fetched)
- **BibKey:** wu2026gapt

### StreamAccomp — Streaming Generation for Music Accompaniment
- **Who/where/when:** Yusong Wu, Mason Wang, Heidi Lei, Stephen Brade, Lancelot Blanchard, Shih-Lun Wu, Aaron Courville, Cheng-Zhi Anna Huang; Mila / MIT; ISMIR 2026 (arXiv 2510.22105, Oct 2025)
- **Links:** https://arxiv.org/abs/2510.22105 ; https://github.com/lukewys/stream-music-gen ; https://lukewys.github.io/stream-music-gen
- **What it is:** Real-time *audio-to-audio* accompaniment: a 16-layer decoder-only Transformer over DAC RVQ tokens (50 Hz, 4 codebooks) listens to an incoming stem and emits an accompanying stem, across 18 GM instrument families (Slakh2100). Formalizes two design knobs: **future visibility** t_f (latency offset, −4 to +4 s) and **output chunk size** k, trained across the grid with a delay pattern.
- **Evidence:** COCOLA coherence, Beat-F1 and FAD on 1,024 Slakh clips plus blind pairwise listening; larger t_f improves coherence but demands faster inference; "naive maximum-likelihood streaming training is insufficient for coherent accompaniment where future context is not available."
- **Why it matters for the studio:** Quantifies the latency/coherence trade-off the studio will face in any live audio layer, and is open code.
- **Tags:** [audio-generation] [real-time] [accompaniment] [evaluation]
- **Verification:** verified (arXiv HTML fetched)
- **BibKey:** wu2026streaming

### LiveAgentsDesignSpace — A Design Space for Live Music Agents
- **Who/where/when:** Yewon Kim, Stephen Brade, Alexander Wang, David Zhou, Haven Kim, Bill Wang, Sung-Ju Lee, Hugo F. Flores García, Cheng-Zhi Anna Huang, Chris Donahue; CMU / MIT / UIUC / UCSD / KAIST / Northwestern; ACM CHI 2026 (arXiv 2602.05064)
- **Links:** https://arxiv.org/abs/2602.05064 ; interactive visualizer: https://live-music-agents.github.io
- **What it is:** Systematic review of 184 live-music-agent systems (153 papers from HCI/AI/computer-music venues + 31 videos; 731 papers screened; 89.8% inter-annotator agreement) yielding a design space of 31 dimensions / 165 codes in four aspects: Usage Context (user role, agent role, topology…), Interaction (I/O modality, planning, temporal structure, control mode/scope, system initiative, agency framing tool/partner/hybrid), Technology (model class, learning, adaptation, latency emphasis, integration), Ecosystem (authorship, economic, cultural).
- **Evidence:** Only ~5% of systems discuss ecosystem/policy; trend from reactive accompanists to proactive partners; control vs novelty and coherence vs diversity trade-offs.
- **Why it matters for the studio:** A ready taxonomy vocabulary for the *real-time* half of the studio, and a living artifact to position the design against.
- **Tags:** [co-creation-framework] [real-time] [evaluation] [mixed-initiative]
- **Verification:** verified (arXiv HTML fetched)
- **BibKey:** kim2026designspace

### AgentsInConcert — Agents in Concert: A Case-Study of Bringing AI to the Stage in Practice
- **Who/where/when:** Stephen Brade, Teng Ma, Lancelot Blanchard, Kimaya Lecamwasam, Carlos Mariano Salcedo, Suwan Kim, Perry Naseck, Andrew Li, Matthew R. Michalek, Sebastian Franjou, Cheng-Zhi Anna Huang; MIT (HAI-Res + Media Lab); ACM IUI 2026, DOI 10.1145/3742413.3789104
- **Links:** https://doi.org/10.1145/3742413.3789104
- **What it is:** Case study of deploying multiple AI music agents in a real concert (the jam_bot / Jordan Rudess + MIT Chamber Chorus program at the Media Lab), documenting the practical engineering, rehearsal and performer-agency lessons of bringing generative agents on stage.
- **Evidence:** Reflective case study (details behind ACM paywall; not fetched).
- **Why it matters for the studio:** Field lessons on robustness, previews/kill-switches and rehearsal workflows for any "performance mode" of the studio.
- **Tags:** [real-time] [HCI-study] [mixed-initiative]
- **Verification:** partial (title/authors/venue from dblp + ACM DOI; content inferred from related jam_bot coverage)
- **BibKey:** brade2026agentsinconcert

### LMDM — Live Music Diffusion Models: Efficient Fine-Tuning and Post-Training of Interactive Diffusion Music Generators
- **Who/where/when:** Zachary Novack*, Stephen Brade*, Haven Kim, Hugo Flores García, Nithya Shikarpur, Chinmay Talegaonkar, Suwan Kim, Valerie K. Chen, Julian McAuley, Taylor Berg-Kirkpatrick, Cheng-Zhi Anna Huang; UCSD / MIT / Adobe; arXiv 2605.22717, May 2026
- **Links:** https://arxiv.org/abs/2605.22717 ; audio: https://stephenbrade.github.io/lmdm-public/
- **What it is:** Repurposes an open audio diffusion model (Stable Audio Open Small, 340M) into a streaming, block-wise generator with KV-caching (encoder-decoder or block-causal variants) and an "ARC-Forcing" adversarial post-training that curbs error accumulation without RL or reward models. Modes: text-conditioned streaming, **sketch-based synthesis** (time-aligned top-k CQT loudness controls extracted from a musician's live audio), and stem-conditioned jamming with adjustable future visibility (−2..+2 s). Deployed via ONNX + C++/JUCE as a "generative delay" effect on a consumer gaming laptop.
- **Evidence:** ~30 ms latency after post-training (8 steps), TTFF 0.03 s; FD/KL/CLAP competitive with Stable Audio Open and MusicGen-Large at far lower latency; N=3 musicians (sax, guitar, cello) described it as a "musical partner rather than simple effect"; limits: EDM bias from MTG-Jamendo, quality below frontier models.
- **Why it matters for the studio:** Open recipe for a local, low-latency audio partner that accepts *sketch-like control signals*; the "generative delay" is a fresh instrument metaphor for the studio's audio layer.
- **Tags:** [audio-generation] [real-time] [sketch] [controllability] [DAW-plugin] [text-conditioning]
- **Verification:** verified (arXiv HTML fetched)
- **BibKey:** novack2026lmdm

### Stemphonic — Stemphonic: All-at-once Flexible Multi-stem Music Generation
- **Who/where/when:** Shih-Lun Wu, Ge Zhu, Juan-Pablo Cáceres, Cheng-Zhi Anna Huang, Nicholas J. Bryan; Adobe Research (internship); arXiv 2602.09891, Feb 2026
- **Links:** https://arxiv.org/abs/2602.09891 ; demo: https://stemphonic-demo.vercel.app
- **What it is:** Diffusion/flow model that generates a *variable set of synchronized stems in one pass* (vs. fixed-stem parallel or slow one-stem-at-a-time). Tricks: stem grouping in batches, shared initial noise within a group, conditioning on existing sub-mixes, and per-stem binary **activity patterns** (when each instrument plays). Conditioning: global + per-stem text, tempo, existing audio.
- **Evidence:** FAD_stem/FAD_mix, CLAP, activity-F1 on MoisesDB and MUSDB; 25–50% faster than iterative baseline, better mix quality with a 2-pass scheme.
- **Why it matters for the studio:** Arrangement-as-compile: given the composer's existing stems and an "activity score," it fills in the remaining parts — aligned with the founder's arranger-workstation instincts.
- **Tags:** [audio-generation] [accompaniment] [controllability] [text-conditioning] [structure]
- **Verification:** verified (arXiv HTML fetched)
- **BibKey:** wu2026stemphonic

### LatentFT — Latent Fourier Transform
- **Who/where/when:** Mason L. Wang, Cheng-Zhi Anna Huang; MIT CSAIL (HAI-Res); arXiv 2604.17986, Apr 2026
- **Links:** https://arxiv.org/abs/2604.17986
- **What it is:** Diffusion autoencoder whose latent sequence is transformed with a DFT into a "latent spectrum" separating musical information by *timescale*; training masks latent frequencies at random so the decoder learns to reconstruct from partial spectra. At inference, users apply custom masks to keep/blend patterns at chosen latent frequencies — an "equalizer for musical patterns" enabling variations, blends of two pieces, and isolation of characteristics.
- **Evidence:** Qualitative and reconstruction experiments (details not extracted).
- **Why it matters for the studio:** A non-text, timescale-aware *edit* control ("keep the phrase-level shape, vary the surface") that could sit behind a scribble/annotation gesture.
- **Tags:** [editing] [representation] [controllability] [audio-generation]
- **Verification:** verified (arXiv HTML fetched)
- **BibKey:** wang2026latentft

### HuangPhilosophy — Anna Huang's articulated philosophy of human-AI co-creation (talks, bios, course)
- **Who/where/when:** Cheng-Zhi Anna Huang; MIT (2024–2026): GenAI Summit 2025 (UCSD) talk "Creativity through Interaction"; MIT Spectrum Spring 2025; MIT News June 2026; course 21M.369 (Fall 2024) → 21M.386 "Algorithms and Interactions for Human-AI Music Making"
- **Links:** https://genaisummit2025.ucsd.edu/schedule/anna-huang ; https://betterworld.mit.edu/spectrum/issues/spring-2025/music-and-technology-intertwined ; https://news.mit.edu/2026/inaugural-mit-music-technology-research-showcase-celebrates-work-students-0629 ; https://musictech.mit.edu/21m369fa24/ ; https://czhuang.github.io/
- **What it is:** Verbatim statements of position. GenAI Summit abstract: "How can we elicit creativity not through imitation but through interaction? … Coconet … supports a nonlinear compositional process through an iterative block-Gibbs like generative procedure, while MIDI-DDSP supports intuitive user control in performance synthesis through hierarchical modeling. … I'm interested in designing visualizations and interactions that can help musicians understand and steer system behavior, and algorithms that can learn from their feedback in more organic ways. I aim to build systems that musicians can shape, negotiate, and jam with in their creative practice." Spectrum: "I'm interested in thinking about creativity not through imitation, but as a collaborative process where creative ideas emerge through human-AI interaction"; "We also teach machines to listen, so that they can jam with other musicians and respond to what they're playing." MIT News 2026: "We work with these musicians, we go into the studio, and every week we try something. The technology grows with the creative process." Homepage: neural networks "as a lens onto music, and a mirror onto our own understanding of music"; goal of designing "interactive systems and visualizations" so artists can "understand and steer" AI. Course 21M.369/386 surveys generative modeling, learning from human feedback, RL/social RL, and "abstractions that empower human-AI collaboration."
- **Evidence:** Primary pages fetched.
- **Why it matters for the studio:** These are quotable anchors for the studio's manifesto: interaction over imitation, steer + understand, nonlinear composition, co-design in the studio week by week.
- **Tags:** [co-creation-framework] [creativity-support] [history]
- **Verification:** verified
- **BibKey:** huang2025creativityinteraction

### MITMTC — MIT Music Technology and Computation Graduate Program & HAI-Res lab
- **Who/where/when:** MIT Music & Theater Arts (SHASS) + School of Engineering + Schwarzman College of Computing; director Eran Egozy; faculty Anna Huang, Mark Rau, Paris Smaragdis, Grisha Coleman, Ian Hattwick; launched Fall 2024 (SM for MIT undergrads from Fall 2025; open admission from Fall 2026; MASc also offered); first showcase 13 May 2026, Linde Music Building
- **Links:** https://musictech.mit.edu/ ; https://musictech.mit.edu/mtcgp/ ; https://news.mit.edu/2026/inaugural-mit-music-technology-research-showcase-celebrates-work-students-0629 ; https://risingstars-eecs.mit.edu/speakers/anna-huang
- **What it is:** New graduate program (SM/MASc; EECS PhD track via affiliated faculty) with dedicated labs in the Edward and Joyce Linde Music Building. Huang's **Human-AI Resonance (HAI-Res)** group at CSAIL "co-design[s] with musicians new algorithms and interactions for Human-AI partnerships." Showcase projects: Rachel Loh, "Visualizing the Internal State of Music Models for Live Human-AI Improvisation"; Nithya Shikarpur, live Hindustani voice + generative models + loops; Brade/Kim/Chen, "Whale, Cello (there?)" (cello vs real-time diffusion model trained on whale song); Zhixing Chen, generative music from dance circles; Claire Southard, EEG decoding of imagined music; Salcedo, neural cellular automata visuals. 10 students admitted for 2026–27 from 100+ applicants.
- **Evidence:** Institutional reporting; first cohort of five.
- **Why it matters for the studio:** The nearest academic community to the studio's thesis (Boston/Cambridge), a pipeline of open real-time co-creation prototypes, and a venue for co-design partnerships and evaluation.
- **Tags:** [education] [co-creation-framework] [real-time] [history]
- **Verification:** verified
- **BibKey:** mit2026mtcshowcase

### music21 — music21: A Toolkit for Computer-Aided Musicology (Cuthbert)
- **Who/where/when:** Michael Scott Asato Cuthbert (with Christopher Ariza for the founding paper); MIT; ISMIR 2010 paper; toolkit 2008–present, v10.5.0 released 17 June 2026
- **Links:** https://github.com/cuthbertLab/music21 ; docs: https://www.music21.org/music21docs/ ; corpus list: https://www.music21.org/music21docs/about/referenceCorpus.html ; module: https://www.music21.org/music21docs/moduleReference/moduleCorpusChorales.html
- **What it is:** Python toolkit "for computer-aided musical analysis and computational musicology." Parses MusicXML, MIDI, ABC, Humdrum **kern, MEI, Noteworthy, Capella etc. into a hierarchical `Stream` object model (Score → Part → Measure → Note/Chord/etc.) and writes MusicXML, MIDI, LilyPond (PNG/PDF), braille, and text; opens scores in MuseScore/Finale. Analysis: key finding (Krumhansl-Schmuckler et al.), `roman.romanNumeralFromChord`/`RomanNumeral`, chord identification, intervals, voice-leading, meter/beat-strength, feature extraction (jSymbolic/native), search/similarity, serial matrices, plotting. Bundled corpus (BSD code; scores public domain or by permission): all Bach chorales (371 Riemenschneider, addressable via `corpus.chorales.Iterator` by Riemenschneider/BWV/Kalmus/Budapest/Bärenreiter numbering or title), Bach cantatas/organ works, Palestrina (200+ mass movements), Monteverdi madrigals (books 3–5), Beethoven/Haydn/Mozart quartets, Essen folksong (ABC), O'Neill's 1,800+ Irish tunes, Aird's Airs, Josquin, Schubert, Schumann, Joplin, Webern, trecento music, theory exercises. License BSD-3-clause; Python ≥3.12; ~2.5k GitHub stars.
- **Evidence:** Two decades of use in computational musicology and ML pipelines (e.g., JSB Chorales datasets used by Coconet/Music Transformer derive from music21's chorale corpus); Tymoczko's 2013 MTO review.
- **Why it matters for the studio:** The symbolic layer's parser/analyzer/exporter: read the composer's MusicXML, annotate with Roman numerals and keys, search corpora for exemplars, emit MusicXML/MIDI/LilyPond after the AI compiles. Its corpus is also training/evaluation data.
- **Tags:** [toolkit] [notation] [representation] [theory-analysis] [corpus] [music-as-code]
- **Verification:** verified (GitHub README, docs pages fetched); ISMIR 2010 citation partial
- **BibKey:** cuthbert2010music21

### OCW21M383 — MIT OCW 21M.383 Computational Music Theory and Analysis (Spring 2023) and "Video 12b: Chorales as a Corpus"
- **Who/where/when:** Michael Scott Asato Cuthbert; MIT OpenCourseWare; Spring 2023; CC BY-NC-SA
- **Links:** https://ocw.mit.edu/courses/21m-383-computational-music-theory-and-analysis-spring-2023/ ; https://ocw.mit.edu/courses/21m-383-computational-music-theory-and-analysis-spring-2023/pages/about-the-course-and-music21/ ; https://learn.mit.edu/search?resource=18680&resource_title=video-12b-chorales-as-a-corpus
- **What it is:** "Presents major approaches to computational music theory and musicology in the symbolic (score-based) domain… algorithms for music theory, encoding, corpus studies, musical search and similarity, feature extraction and machine learning, music generation, and computational music perception." Every problem set is Python + music21 in notebooks ("as you proceed through this class, you'll be unlocking features of music21"). Lecture arc: how computers "hear" music → pitch/duration/score representation → Streams as hierarchies → MusicXML (incl. interview with Michael Good) → **corpus studies and statistics on the Bach chorales** (Videos 12b "Chorales as a Corpus", 12c plotting, 12d ties; Classes 13–15 corpus statistics, encoding corpora, voice leading) → equivalence classes/OPTIC → music cognition guest sessions → scales, chords and Roman numerals (Video 22b: "Working and Composing with Scales, Chords, and Roman Numerals"; 22c algorithmic improvisation, George Lewis) → three classes of algorithmic composition → feature extraction/ML/AI → OMR and visualization. Video 12b demonstrates treating the 371 chorales as a queryable dataset (iterate, filter by number/title, analyze keys/harmony across the set) — the same corpus that trains Coconet.
- **Evidence:** Full syllabus/video list fetched; the individual Video 12b page could not be fetched (redirect loop), so its exact contents are inferred from title and course context.
- **Why it matters for the studio:** A tested pedagogy for teaching composers to treat notation as data and to write analysis "programs" — the mindset behind "composition as a program to be compiled"; also a source of exercises for a studio tutorial.
- **Tags:** [education] [theory-analysis] [corpus] [notation] [music-as-code] [toolkit]
- **Verification:** verified (course pages fetched); Video 12b content partial
- **BibKey:** cuthbert2023ocw21m383

### Egozy21M385 — 21M.385 / 6.4550 Interactive Music Systems (Eran Egozy, MIT)
- **Who/where/when:** Eran Egozy, Professor of the Practice in Music Technology, MIT MTA (cross-listed EECS 6.4550); taught Fall and Spring, ongoing
- **Links:** https://catalog.mit.edu/subjects/21m/ ; https://musictech.mit.edu/courses/ ; https://mta.mit.edu/person/eran-egozy
- **What it is:** Catalog: "Explores audio synthesis, musical structure, human computer interaction (HCI), and visual presentation for the creation of interactive musical experiences." Students build real-time Python (Kivy) apps: synthesis, sequencing, MIDI/gesture input, note-highway and rhythm-game-style interfaces, culminating in team final projects and a public demo concert. Egozy also teaches 21M.387/6.3020 Fundamentals of Music Processing. Students call it "their favorite class at MIT so far… because it employs both sides of their personalities" (Egozy, Spectrum 2025).
- **Evidence:** Course description verified; specifics of labs from recall of past syllabi.
- **Why it matters for the studio:** Pedagogical and design source for game-like, low-latency, visually clear musical interaction — the "playable" side of a composition tool.
- **Tags:** [education] [real-time] [game] [creativity-support]
- **Verification:** partial (catalog/course list verified; lab details from recall)
- **BibKey:** egozy21m385

### ConcertCue — ConcertCue: live program-note streaming for classical concerts
- **Who/where/when:** Eran Egozy (with student Nathan Gutierrez '17 and collaborators); MIT Music Technology Lab; 2017–present; Knight Foundation grant $50k (July 2018)
- **Links:** https://musictech.mit.edu/concertcue/ ; https://www.concertcue.com/
- **What it is:** Mobile web app that streams time-synchronized program notes (text, images, media) to audience phones during a live performance, cued to specific musical events. Deployed at MIT ensembles, Boston Symphony Orchestra (Tanglewood and "Casual Fridays," 2017–2020), Boston Baroque, New World Symphony, Radius Ensemble, Michigan Tech.
- **Evidence:** Deployments and grant; a conference paper exists (I recall a NIME 2018 paper by Egozy and Eun Young Lee) but could not be verified this session.
- **Why it matters for the studio:** A model for *time-aligned annotation* of a score/performance for a human reader — the same data structure the studio needs for annotations that steer AI, but pointed at audiences.
- **Tags:** [annotation] [real-time] [product] [education]
- **Verification:** verified (project page); paper unverified
- **BibKey:** egozy2018concertcue

### Harmonix — Guitar Hero / Rock Band (Harmonix Music Systems) as music-making interfaces
- **Who/where/when:** Eran Egozy and Alex Rigopulos (co-founders, MIT Media Lab alumni, Machover's group); Harmonix, founded 1995; Guitar Hero 2005, Rock Band 2007
- **Links:** https://mta.mit.edu/person/eran-egozy ; https://www.harmonixmusic.com/
- **What it is:** Rhythm games that let non-musicians *perform* music via simplified controllers and a scrolling "note highway," with tight audio-visual feedback and scoring. Harmonix grew out of Media Lab work on making musical expression accessible (Egozy and Rigopulos both did master's research under Machover). >35 million units sold; Egozy in Time 100.
- **Evidence:** Commercial history (MIT bio). Egozy's specific public statements about games as music-making interfaces were not retrievable this session (unverified).
- **Why it matters for the studio:** The note-highway/anticipation visual and the "make anyone feel like a musician" goal are direct ancestors of ReaLJam's waterfall and Piano Genie — useful for the studio's performance/jam UI.
- **Tags:** [game] [history] [creativity-support] [real-time]
- **Verification:** partial (bio verified; quotes unverified)
- **BibKey:** egozy2005harmonix

### Hyperscore — Hyperscore: a graphical sketchpad for novice composers
- **Who/where/when:** Morwaread (Mary) Farbood, Egon Pasztor, Kevin Jennings; Tod Machover's Opera of the Future group, MIT Media Lab; IEEE Computer Graphics & Applications 24(1), 2004 (system from 2001–2002; ICMC 2007 follow-up "Composing with Hyperscore"); commercialized by Harmony Line Inc. 2004–2017; rebuilt by Peter Torpey (2021), web version 2022 (v5.0) under nonprofit New Harmony Line
- **Links:** https://doi.org/10.1109/MCG.2004.1255809 ; https://en.wikipedia.org/wiki/Hyperscore ; https://www.hyperscore.com/ (TLS misconfigured at fetch time)
- **What it is:** Users first create short **motives** (melodic/rhythmic fragments) in "motive windows," each assigned a color; then in a **sketch window** they *draw* colored lines whose contour and vertical position control pitch/transposition of that motive over time, layering many lines into a texture. A separate **harmony line** is drawn to shape harmonic tension; the system auto-harmonizes so the texture stays consonant/dissonant as drawn. Output is General-MIDI playback and an exportable score. Used by children in Machover's *Toy Symphony* (2002–03) to compose orchestral pieces, in schools and hospitals, and in the City Symphonies.
- **Evidence:** Deployed with thousands of children; qualitative reports (NYT 2002, Scientific American Frontiers); no controlled studies retrieved.
- **Why it matters for the studio:** *The* precedent for "scribble to compose": a freehand line becomes a compile instruction over human-authored motives, with a separate drawn control for harmony. Its motive/sketch/harmony-line decomposition is a strong candidate for the studio's sketch layer.
- **Tags:** [sketch] [symbolic-generation] [notation] [creativity-support] [education] [history] [controllability]
- **Verification:** partial (Wikipedia + Machover bio fetched; IEEE article citation from recall)
- **BibKey:** farbood2004hyperscore

### Hyperinstruments — Hyperinstruments / Opera of the Future (Tod Machover)
- **Who/where/when:** Tod Machover, MIT Media Lab (Professor of Music and Media; group founded at the Lab's start, hyperinstruments from 1986); "Hyperinstruments: A Progress Report 1987–1991" (MIT Media Lab, 1992); Brain Opera 1996; Toy Symphony 2002–03; City Symphonies 2012–
- **Links:** https://www.media.mit.edu/groups/opera-of-the-future/overview/ ; https://en.wikipedia.org/wiki/Tod_Machover
- **What it is:** Sensor-augmented instruments that let performer gesture shape sound beyond the acoustic instrument (Hypercello for Yo-Yo Ma, *Begin Again Again…* 1991; Hyperviolin), then "hyperinstruments for non-professionals" (Brain Opera) and composition tools for children (Hyperscore). Machover's stated goal: "making every human being into a musician." Huang (SM 2008) and Egozy (SM 1995) both came through the Media Lab in this orbit; Kimaya Lecamwasam (jam_bot co-author) is a current Opera of the Future PhD student collaborating with HAI-Res.
- **Evidence:** Decades of premieres; no controlled studies.
- **Why it matters for the studio:** Establishes the MIT stance that technology should *expand* human expression (hyper-), not substitute for it — the institutional ancestor of Huang's "interaction, not imitation."
- **Tags:** [history] [expression-performance] [creativity-support] [real-time]
- **Verification:** partial (Wikipedia fetched; report citation from recall)
- **BibKey:** machover1992hyperinstruments

### Vercoe — Barry Vercoe: Csound and the Synthetic Performer
- **Who/where/when:** Barry Vercoe; MIT Experimental Music Studio (est. 1973 after PDP-11 acquisition; he joined MIT 1971) → founding member of MIT Media Lab (1985); MUSIC 11 (1973), Csound (1985–86; LGPL); "The Synthetic Performer in the Context of Live Performance," ICMC 1984 (demonstrated at IRCAM 1984)
- **Links:** https://csound.com/ ; https://en.wikipedia.org/wiki/Barry_Vercoe
- **What it is:** Csound is a text-based sound-compiler language (orchestra + score files) still in wide use — the literal ancestor of "music as code that gets compiled." The Synthetic Performer was an early real-time score-following accompanist that listened to a live flautist and adjusted tempo/expression — the first "AI accompanist" in this lineage. Students include Miller Puckette (Max/Pd) and Paris Smaragdis (now MIT MTC faculty).
- **Evidence:** Historical; Csound in continuous development for ~40 years.
- **Why it matters for the studio:** Grounds the founder's "compile" metaphor historically (Csound's *orc/sco* compile model) and shows the real-time-accompaniment thread (Vercoe 1984 → ReaLchords 2024) is 40 years old at MIT.
- **Tags:** [history] [music-as-code] [accompaniment] [real-time] [toolkit]
- **Verification:** partial (Wikipedia fetched; ICMC citation and Csound license from recall)
- **BibKey:** vercoe1984syntheticperformer

---

## Cross-cluster pointers (found while working; not full entries here)

- **Krol, Llano Rodriguez, Loor Paredes — "Exploring the Needs of Practising Musicians in Co-Creative AI Through Co-Design," CHI 2025 (arXiv 2502.09055).** Monash/Sussex; 13 musicians, two co-design workshops + 2-week ecological deployment of a MusicBERT masked-variation tool. Findings: musicians reject "collaborator" framing ("you actually need empathy, to collaborate"), insist on ownership of the creative process, want DAW integration and music-theory (not MIDI) terminology, and value "moments instead of the whole." → HCI/co-creation-studies cluster. Verified.
- **Bradshaw, Spangher, Biderman, Colton — "The Ghost in the Keys: A Disklavier Demo for Human-AI Musical Co-Creativity" (Aria-Duet), NeurIPS 2025 Creative AI (arXiv 2511.01663).** Turn-taking duet with the Aria model on a Disklavier; explicitly motivated by rejecting "text-prompting, an asynchronous workflow." → real-time / symbolic LLM cluster. Verified.
- **Hawthorne et al., "Enabling Factorized Piano Music Modeling and Generation with the MAESTRO Dataset" (Wave2Midi2Wave), ICLR 2019** — Huang coauthor; transcription + dataset. → transcription/dataset cluster.
- **Sturm, Uitdenbogerd, Huang, Koops — TISMIR special collection "AI and Musical Creativity" editorial (2021).** → ethics/evaluation cluster.
- **Wu et al., FLAM: Frame-Wise Language-Audio Modeling, ICML 2025** (Huang coauthor; Adobe) — frame-level audio-text grounding, useful for audio annotation search. → audio representation cluster.
- **Chris Donahue (CMU)** — coauthor on ReaLchords, Live Music Models, Design Space; his Anticipatory Music Transformer (Thickstun et al. 2023) and Hookpad Aria belong to the controllable symbolic cluster.
- **MusicBERT / masked variation** (Krol et al.) and **Coconet** both implement "mask-and-refill" editing — unify under an [infilling] taxonomy node.
