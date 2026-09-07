# 04 — Audio-domain music generation, controllable/editable audio, and music-understanding models

*Research notes for the "AI music studio for composers" project. Cluster 04. Compiled 2026-09-07. Verification status per entry: **verified** = primary source fetched (arXiv abstract page / GitHub README / official page); **partial** = confirmed via secondary page or search snippets only; **unverified** = recall.*

## Overview

The audio-domain music generation field went from a single seminal raw-audio system (OpenAI **Jukebox**, 2020; VQ-VAE + transformers, minutes-long but slow and lo-fi) to a 2023 explosion of text-to-music models built on neural codecs and latent diffusion (Google **MusicLM**/**Noise2Music**, Meta **MusicGen**/AudioCraft, Surrey **AudioLDM**, Stability **Stable Audio**), and then—2024–2026—to two divergent branches. Branch A is **text-to-full-song** with vocals and lyrics: commercial (Suno v3→v5.5, Udio, Google Lyria 2/3/3.5 + ProducerAI/"Flow Music", ElevenLabs Music, Mureka) and, increasingly, open-weights (YuE, DiffRhythm, SongGen, ACE-Step 1.0/1.5, HeartMuLa). This is the paradigm the founder wants to *understand and then invert*: single-shot prompt → finished mix, human relegated to prompt author and curator. Notably, by 2025–2026 even these products have been pushed by professional users toward *editing* affordances (Suno "Replace Section", "Covers", "Personas", Suno Studio with MIDI; Udio inpainting; Music AI Sandbox "Edit"; Stable Audio 2.5 and ElevenLabs "inpainting"; ACE-Step "repainting", "lyric edit", "cover", "vocal→accompaniment")—implicit evidence that the one-shot paradigm is insufficient for musicians. Branch B is **controllable and editable audio generation** from the research community, which is directly useful to the studio: time-varying and *symbolic* conditioning (Music ControlNet, Coco-Mulla, JASCO, Mustango, MuseControlLite, Melody+Text ControlNet-DiT), training-free inference-time control and inversion-based editing (DITTO/DITTO-2, MusicMagus, ZETA/ZEUS, MelodyFlow), instruction-following editors (AUDIT, InstructME, Instruct-MusicGen, SongEditor), stem/accompaniment-level co-creation (SingSong, StemGen, Multi-Source Diffusion, Diff-A-Riff, MusicGen-Stem), and real-time "live music models" steerable by text, audio and—since June 2026—MIDI (Lyria RealTime, Magenta RealTime 1/2). A third, supporting strand is **music understanding**: self-supervised encoders (MERT, MuQ), text–audio embeddings (CLAP, MuLan/MusicCoCa), and audio LLMs (MU-LLaMA, LLark, MusiLingo, SALMONN, Qwen2-Audio/2.5-Omni, Gemini 2.5, OpenMU) with benchmarks (MuChoMusic, Song Describer) that reveal how far these are from reliable musical *critique*—they still over-rely on the text modality. For rendering notation into audio under human control, the most composer-aligned lineage remains **DDSP → MIDI-DDSP** (notes → performance → synthesis hierarchy), now joined by symbolic-conditioned audio models (JASCO, Coco-Mulla) and MIDI-steerable live models (Magenta RT 2).

## Key takeaways for the studio

1. **Symbolic conditioning of audio models exists but is thin and mostly research-grade.** Only JASCO (chords + melody salience + drums), Coco-Mulla (chords + drum MIDI + pitch), Mustango (chords/beats/key/tempo in text), Music ControlNet / MuseControlLite (melody, rhythm, dynamics curves), the Melody+Text ControlNet-DiT, MIDI-DDSP (full MIDI, monophonic) and Magenta RealTime 2 (live MIDI notes) accept structured musical input. None of the commercial full-song systems accept MIDI/chords as a *generation* condition (Suno Studio added MIDI import/edit in Aug 2026 inside its DAW, but the generator itself is prompt/audio-driven). This is a major gap—and a differentiator—for a "compile notation → audio" studio.
2. **Region editing is now table stakes**: inpainting/outpainting/"repainting" is in AudioLDM (zero-shot), JEN-1, MusicFlow, DITTO, MuseControlLite, ACE-Step, Stable Audio 2.5, Udio, Suno ("Replace Section"), Music AI Sandbox, ElevenLabs. Prefer models with *native* mask/inpaint training (JEN-1, MusicFlow, MuseControlLite, ACE-Step) over post-hoc tricks for the "edit → recompile a bar range" loop.
3. **Stem-level, "listen and respond" generation is the right unit of co-creation**: SingSong (vocal → accompaniment), StemGen, Multi-Source Diffusion (source imputation), Diff-A-Riff (accompaniment to a mix), MusicGen-Stem (bass/drums/other with per-stem editing), Instruct-MusicGen (add/remove/separate stem by instruction), ACE-Step 1.5 (vocal→BGM, multi-track layering). These map naturally onto "compile one part at a time".
4. **Training-free control via inference-time optimization (DITTO, DITTO-2) and DDPM/flow inversion (ZETA/ZEUS, MelodyFlow, MusicMagus) lets any differentiable musical feature (melody, intensity curve, structure matrix) be imposed on a frozen model**—a general mechanism for turning composer *annotations* into constraints without retraining.
5. **Real-time steerable generation is here** (Lyria RealTime API ≤2 s control latency; Magenta RealTime 2 ~200 ms control latency, 40 ms frames, on a MacBook, open weights, MIDI input, trained on stock music with MT3-inferred MIDI labels). This is the first credible open building block for an "instrument-like" AI that a Nord Stage player can jam with.
6. **Open weights you can actually build on (2026)**: ACE-Step 1.5 (MIT, 2B/4B DiT + 0.6–4B LM planner, <4–24 GB VRAM, VST3 plugin, LoRA from a few songs), YuE (Apache-2.0, 7B, heavy), DiffRhythm (Apache-2.0, 8 GB VRAM, 4m45s in ~10 s), SongGen (Apache-2.0, 1.3B, 30 s), HeartMuLa (Apache-2.0, 3B), Stable Audio Open (Stability Community License, CC-trained), MusicGen/JASCO/MAGNeT (weights CC-BY-NC 4.0—non-commercial!), Magenta RT (permissive + bespoke terms), MERT (CC-BY-SA 4.0), CLAP, MuQ. Check weight licenses separately from code licenses.
7. **Legal ground shifted in late 2025**: UMG–Udio (Oct 29, 2025) and WMG–Suno (Nov 25, 2025) settlements → "licensed models" in 2026, walled-garden playback, download caps; Stable Audio 2.5 and ElevenLabs advertise "fully licensed" training; Google says Lyria is trained on music YouTube/Google "have the right to use" and watermarks with SynthID. Stable Audio Open (Freesound + FMA, CC) and Magenta RT (stock music) are the cleanest open training-data stories. An open studio should be explicit about provenance of any audio model it ships.
8. **Music-understanding LLMs are not yet reliable critics.** MuChoMusic (1,187 human-validated MCQs) shows open audio LLMs over-rely on text; LLark/MU-LLaMA/MusiLingo are captioning/QA-level; OpenMU-Bench adds lyrics/ABC-notation/tool-use tasks. For annotation and critique, pair a strong music encoder (MERT/MuQ) with task-specific heads or with a general LLM (Gemini 2.5 / Qwen2.5-Omni) and keep the human in the loop.
9. **Evaluation practice in this field is weak and mostly about fidelity/text-adherence (FAD, CLAP score, small MOS panels)**; almost no paper evaluates *composer* workflows. The one relevant user study (Ronchini et al. 2025, N=17 producers with MusicGen + Demucs) reports "creative misalignment", tempo/key/beat alignment pain, and demand for control/editability—empirical support for the studio thesis.
10. **The commercial trajectory itself validates the thesis**: Suno went prompt → Covers/Personas/Replace Section → Suno Studio DAW (Sep 2025) → MIDI import/record/edit (Aug 2026); Google went MusicLM → Music AI Sandbox with multitrack/inpaint → Lyria RealTime → ProducerAI/Flow Music "replace & extend" conversational refinement. Everyone is being pulled toward iterative, region- and stem-level, notation-aware editing—exactly the loop the studio proposes to make first-class.

---

## A. Foundations (2020–2024)

### Jukebox — Jukebox: A Generative Model for Music
- **Who/where/when:** Prafulla Dhariwal, Heewoo Jun, Christine Payne, et al. (Jong Wook Kim, Alec Radford, Ilya Sutskever); OpenAI; arXiv, 2020.
- **Links:** https://arxiv.org/abs/2005.00341 ; code https://github.com/openai/jukebox ; samples https://jukebox.openai.com
- **What it is:** First raw-audio model to generate minutes-long songs *with singing*. Multi-scale VQ-VAE compresses 44.1 kHz audio into three levels of discrete codes; autoregressive Transformers (up to 5B) model the top level and upsample. Conditioning: artist, genre, and unaligned lyrics; also "primed" continuation from an audio excerpt. No symbolic conditioning; no editing beyond continuation; extremely slow (hours per minute of audio).
- **Evidence:** Qualitative; human-perceived coherence "up to multiple minutes"; lyrics conditioning improved singing controllability. No formal listening study reported in the abstract.
- **Why it matters for the studio:** Historical anchor for text/metadata-to-song; also the encoder later reused as a feature extractor for music understanding (e.g., LLark). Shows the cost of end-to-end audio without symbolic structure.
- **Tags:** [audio-generation] [history] [text-conditioning]
- **Verification:** verified
- **BibKey:** dhariwal2020jukebox

### MusicLM — MusicLM: Generating Music From Text
- **Who/where/when:** Andrea Agostinelli, Timo I. Denk, Zalán Borsos, et al. (13 authors incl. Jesse Engel, Neil Zeghidour, Christian Frank); Google Research; arXiv, Jan 2023.
- **Links:** https://arxiv.org/abs/2301.11325 ; project https://google-research.github.io/seanet/musiclm/examples/ ; dataset MusicCaps (Kaggle)
- **What it is:** Hierarchical sequence-to-sequence generation: MuLan (joint music–text embedding) conditions a w2v-BERT semantic-token stage and a SoundStream acoustic-token stage (AudioLM lineage). Generates 24 kHz music from text, and—crucially for this project—can be conditioned on a **hummed or whistled melody** plus text (melody tokens from a dedicated embedding), transforming the user's melody into the described style. Released **MusicCaps** (5.5k expert-captioned 10-s clips), the de-facto text-to-music benchmark. Closed weights; productised as MusicFX / Dream Track.
- **Evidence:** Outperformed Mubert and Riffusion in audio quality and text adherence (FAD, KLD, MuLan cycle consistency + human listening tests).
- **Why it matters for the studio:** The first mainstream demonstration that a *hummed melody* can steer a text-to-music model—precisely the "hum or sing" annotation channel in the studio vision. MusicCaps remains the standard evaluation set.
- **Tags:** [audio-generation] [text-conditioning] [humming] [multimodal-input] [dataset] [evaluation]
- **Verification:** verified (abstract + HF paper page for authors)
- **BibKey:** agostinelli2023musiclm

### Noise2Music — Noise2Music: Text-conditioned Music Generation with Diffusion Models
- **Who/where/when:** Qingqing Huang, Daniel S. Park, Tao Wang, et al. (15 authors incl. Quoc V. Le, Wei Han); Google; arXiv, Feb 2023.
- **Links:** https://arxiv.org/abs/2302.03917 ; examples https://google-research.github.io/noise2music
- **What it is:** Cascaded diffusion: a generator produces an intermediate representation (low-fi waveform or spectrogram) from text, a cascader upsamples to 24 kHz 30-s clips. Training captions were pseudo-labelled at scale using an LLM (to generate candidate descriptions) and MuLan (to score them). Text only; no editing, no symbolic control; closed.
- **Evidence:** Captures genre, tempo, instrumentation, mood, era; competitive FAD/MuLan metrics vs MusicLM (paper).
- **Why it matters for the studio:** Establishes the LLM-pseudo-labelling recipe for building text–music datasets—reusable when building annotation corpora for a symbolic-first studio.
- **Tags:** [audio-generation] [text-conditioning] [dataset]
- **Verification:** verified
- **BibKey:** huang2023noise2music

### MusicGen — Simple and Controllable Music Generation
- **Who/where/when:** Jade Copet, Felix Kreuk, Itai Gat, et al. (Tal Remez, David Kant, Gabriel Synnaeve, Yossi Adi, Alexandre Défossez); Meta AI (FAIR); NeurIPS 2023.
- **Links:** https://arxiv.org/abs/2306.05284 ; code https://github.com/facebookresearch/audiocraft (AudioCraft)
- **What it is:** Single-stage autoregressive transformer LM over interleaved EnCodec token streams (codebook interleaving patterns replace cascades). Conditioning: text (T5) and **melody via chromagram** of a reference audio (e.g., a whistled/played melody). 300M/1.5B/3.3B, mono and stereo, 32 kHz, ~30 s. Open code (MIT) and weights (**CC-BY-NC 4.0**, non-commercial). Widely fine-tuned (Coco-Mulla, Instruct-MusicGen, MusicGen-Style, MusicGen-Stem all build on it).
- **Evidence:** Human study (overall quality, text relevance, melody similarity) and objective metrics (FAD, KL, CLAP) vs MusicLM, Riffusion, Mousai, Noise2Music; ablations on interleaving patterns.
- **Why it matters for the studio:** The most-extended open text-to-music backbone; chromagram melody conditioning is a coarse but usable "sketch → audio" channel; non-commercial weights are a constraint for a shipped product.
- **Tags:** [audio-generation] [text-conditioning] [controllability] [humming] [toolkit]
- **Verification:** verified
- **BibKey:** copet2023musicgen

### AudioLDM — AudioLDM: Text-to-Audio Generation with Latent Diffusion Models
- **Who/where/when:** Haohe Liu, Zehua Chen, Yi Yuan, et al. (Xinhao Mei, Xubo Liu, Danilo Mandic, Wenwu Wang, Mark D. Plumbley); University of Surrey / Imperial; ICML 2023.
- **Links:** https://arxiv.org/abs/2301.12503 ; code https://github.com/haoheliu/AudioLDM ; https://audioldm.github.io
- **What it is:** Latent diffusion in a VAE-compressed mel space, conditioned on CLAP embeddings (train on audio embeddings, infer from text). Enables **zero-shot text-guided manipulation—style transfer, inpainting, super-resolution**—without task-specific training. Trainable on a single GPU. Open code and weights.
- **Evidence:** SOTA TTA on AudioCaps by FD/IS/KL and subjective ratings at the time.
- **Why it matters for the studio:** Template for "inpaint a region, keep the rest" in the audio domain; also the base model for ZETA/ZEUS editing and MusicMagus.
- **Tags:** [audio-generation] [text-conditioning] [editing] [infilling]
- **Verification:** verified
- **BibKey:** liu2023audioldm

### AudioLDM 2 — AudioLDM 2: Learning Holistic Audio Generation with Self-supervised Pretraining
- **Who/where/when:** Haohe Liu, Yi Yuan, Xubo Liu, et al. (Xinhao Mei, Qiuqiang Kong, Qiao Tian, Yuping Wang, Wenwu Wang, Yuxuan Wang, Mark D. Plumbley); Surrey / ByteDance; IEEE/ACM TASLP 2024 (arXiv Aug 2023).
- **Links:** https://arxiv.org/abs/2308.05734 ; code https://github.com/haoheliu/AudioLDM2 ; https://audioldm.github.io/audioldm2
- **What it is:** Introduces a "language of audio" (LOA): AudioMAE features as an intermediate representation; a GPT-2 translates any conditioning modality (text, phonemes, audio) into LOA, then latent diffusion renders. One framework for text-to-audio, text-to-music, text-to-speech. Open weights (music-specific checkpoint). Text only for music; no explicit symbolic control.
- **Evidence:** SOTA/competitive on AudioCaps, MusicCaps, LJSpeech.
- **Why it matters for the studio:** Shows how a general intermediate representation lets one renderer serve many conditioning types—an architectural pattern relevant to a "compiler" that must accept notation, text, hums, and audio examples.
- **Tags:** [audio-generation] [text-conditioning] [representation]
- **Verification:** verified (abstract); author list from memory (partial)
- **BibKey:** liu2024audioldm2

### StableAudio2 — Long-form Music Generation with Latent Diffusion (Stable Audio 2.0)
- **Who/where/when:** Zach Evans, Julian D. Parker, CJ Carr, Zack Zukowski, Josiah Taylor, Jordi Pons; Stability AI; ISMIR 2024 (arXiv Apr 2024). Predecessor: "Fast Timing-Conditioned Latent Audio Diffusion" (Stable Audio 1.0, ICML 2024, arXiv 2402.04825).
- **Links:** https://arxiv.org/abs/2404.10301 ; code https://github.com/Stability-AI/stable-audio-tools ; product https://stableaudio.com
- **What it is:** Diffusion transformer over a highly compressed (21.5 Hz) continuous latent from a new autoencoder; **timing conditioning** (start time, total length) lets the user choose duration and position; generates full 4 m 45 s stereo 44.1 kHz tracks with intro/development/outro; **audio-to-audio style transfer** by initialising from a user's audio. Stable Audio 1.0 introduced timing conditioning and 95-s stereo. Weights of 1.0/2.0 not open (trained on licensed AudioSparx data); the open sibling is Stable Audio Open.
- **Evidence:** Better FDopenl3, KL, CLAP than baselines; listening test confirmed structural coherence over long durations.
- **Why it matters for the studio:** Timing conditioning is a simple, explicit *structural* control (where in the piece am I?) that composers understand; audio-to-audio initialisation is a re-rendering primitive.
- **Tags:** [audio-generation] [text-conditioning] [structure] [style-transfer] [controllability]
- **Verification:** verified
- **BibKey:** evans2024longform

### StableAudioOpen — Stable Audio Open
- **Who/where/when:** Zach Evans, Julian D. Parker, CJ Carr, Zack Zukowski, Josiah Taylor, Jordi Pons; Stability AI; ICASSP 2025 (arXiv Jul 2024).
- **Links:** https://arxiv.org/abs/2407.14358 ; weights https://huggingface.co/stabilityai/stable-audio-open-1.0 ; code https://github.com/Stability-AI/stable-audio-tools
- **What it is:** Open-weights text-to-audio DiT (≈1.2B) generating 44.1 kHz stereo up to 47 s, trained **only on Creative Commons audio from Freesound and the Free Music Archive** (≈486k recordings). Weights under the Stability AI Community License (free below revenue threshold). Text + timing conditioning; no symbolic input; commonly used as the base for controllable adapters (MuseControlLite, Melody+Text ControlNet-DiT, Sketch2Sound).
- **Evidence:** Competitive FDopenl3/KL/CLAP vs closed models on AudioCaps and Song Describer; quality gap on music with vocals acknowledged.
- **Why it matters for the studio:** The cleanest-provenance open music/sound model; the natural base for fine-tuning region-editing and symbolic-conditioning adapters for an open-source studio.
- **Tags:** [audio-generation] [text-conditioning] [ethics-legal] [toolkit]
- **Verification:** verified
- **BibKey:** evans2024stableaudioopen

### JEN-1 — JEN-1: Text-Guided Universal Music Generation with Omnidirectional Diffusion Models
- **Who/where/when:** Peike Li, Boyu Chen, Yao Yao, et al. (Yikai Wang, Allen Wang, Alex Wang); Futureverse; arXiv, Aug 2023 (also IEEE CAI 2024).
- **Links:** https://arxiv.org/abs/2308.04729 ; demo https://www.jenmusic.ai (product) — no code
- **What it is:** Latent diffusion in a masked-autoencoder latent with "omnidirectional" training that mixes bidirectional and autoregressive (causal) modes so one model does **text-to-music, inpainting, and continuation**. Text only; closed weights (commercial product "JEN").
- **Evidence:** Claims better FAD/CLAP than MusicGen and Noise2Music on MusicCaps with ~22.6% of MusicGen's parameters.
- **Why it matters for the studio:** Early proof that generation + region-inpainting + continuation can be one model—the three primitives of an audio "recompile" step.
- **Tags:** [audio-generation] [infilling] [editing] [text-conditioning]
- **Verification:** verified
- **BibKey:** li2023jen1

### Mustango — Mustango: Toward Controllable Text-to-Music Generation
- **Who/where/when:** Jan Melechovsky, Zixun Guo, Deepanway Ghosal, Navonil Majumder, Dorien Herremans, Soujanya Poria; SUTD (Singapore); NAACL 2024.
- **Links:** https://arxiv.org/abs/2311.08355 ; code https://github.com/AMAAI-Lab/mustango ; dataset MusicBench
- **What it is:** Latent diffusion (Tango lineage) with **MuNet**, a music-domain-knowledge-informed UNet guidance module that consumes chords, beats, key and tempo parsed from the prompt. Releases **MusicBench** (52k music–text pairs, augmented with pitch-shift/tempo/volume changes and MIR-extracted theory captions). Open weights.
- **Evidence:** Better controllability (chord/beat/key/tempo accuracy) than MusicGen and AudioLDM2; FAD/KL competitive.
- **Why it matters for the studio:** Demonstrates chord/key/tempo-aware audio generation from structured text—an interface layer between a lead sheet and an audio renderer.
- **Tags:** [audio-generation] [controllability] [text-conditioning] [dataset] [theory-analysis]
- **Verification:** verified
- **BibKey:** melechovsky2024mustango

### MusicFlow — MusicFlow: Cascaded Flow Matching for Text Guided Music Generation
- **Who/where/when:** K R Prajwal, Bowen Shi, Matthew Le, et al. (Apoorv Vyas, Andros Tjandra, Mahi Luthra, Baishan Guo, Huiyu Wang, Triantafyllos Afouras, David Kant, Wei-Ning Hsu); Meta FAIR; ICML 2024 (arXiv Oct 2024).
- **Links:** https://arxiv.org/abs/2410.20478 — no public code/weights
- **What it is:** Two flow-matching networks: text → HuBERT semantic units, then (text, semantic) → EnCodec acoustic features. Trained with masked prediction so the same model performs **continuation and infilling** zero-shot. 2–5× smaller than MusicGen with comparable quality; non-autoregressive.
- **Evidence:** Competitive FAD/CLAP on MusicCaps with 50–80% fewer parameters; infilling evaluated by masking spans.
- **Why it matters for the studio:** Masked-prediction training is the principled route to "recompile this span given surrounding context"; also shows flow matching as a fast alternative to AR decoding.
- **Tags:** [audio-generation] [infilling] [text-conditioning]
- **Verification:** verified
- **BibKey:** prajwal2024musicflow

### Riffusion → ProducerAI → Google Flow Music — Riffusion (spectrogram Stable Diffusion) and its 2025–2026 commercial afterlife
- **Who/where/when:** Seth Forsgren & Hayk Martiros (Dec 2022, hobby project); Riffusion Inc. ($4M 2023); public beta with in-house "FUZZ" model Jan 2025; rebranded **Producer.ai / ProducerAI** (Jul 2025); **acquired by Google Feb 24, 2026** (team joined Google Labs + DeepMind); relaunched on Lyria 3 and renamed **Google Flow Music** Apr 2026.
- **Links:** https://en.wikipedia.org/wiki/Riffusion ; https://www.musicbusinessworldwide.com/google-acquires-ai-music-platform-and-suno-challenger-producerai/ ; https://9to5google.com/2026/04/20/producerai-becomes-google-flow-music/ ; https://flowmusic.app
- **What it is:** Original Riffusion fine-tuned Stable Diffusion on mel-spectrogram images and inverted them to audio; used latent interpolation to loop/morph. ProducerAI pivoted to a **conversational, multi-turn refinement UX** ("creative collaborator") rather than one-shot prompts. Flow Music (Gemini + Lyria 3/3.5) offers "replace & extend" of specific sections, iterative variation, lyrics/vocals, SynthID watermarking, integration with Nano Banana (art) and Veo (video); included in Google AI plans.
- **Evidence:** No papers; product claims only.
- **Why it matters for the studio:** Case study of the market moving from single-shot prompt to conversational, section-level iteration—the studio's loop, but audio-only and without notation. Also a warning: independent open-ish players get absorbed by platforms.
- **Tags:** [audio-generation] [product] [editing] [history] [LLM-agent]
- **Verification:** verified (Wikipedia + MBW + 9to5Google)
- **BibKey:** forsgren2022riffusion

## B. Commercial full-song systems and platforms (2024–2026)

### Suno — Suno (v3 → v3.5 → v4 → v4.5 → v5 → v5.5) and Suno Studio
- **Who/where/when:** Suno Inc. (Cambridge, MA; founded 2022 by ex-Kensho engineers). Model timeline (from official release notes): v3 alpha Feb 22 2024 (2-min clips), v3.5 May 24 2024 (4-min, 2-min extensions), v4 Nov 19 2024, v4.5 May 1 2025, **v5 Sep 23 2025**, v4.5-all free tier Oct 21 2025, **v5.5 Mar 26 2026** (+ "Custom Models": train a personal v5.5). **Suno Studio** generative DAW Sep 25 2025 (Premier tier); MIDI import/record/edit Aug 13 2026; "Voices" Aug 7 2026; natural-language lyrics editing Jul 9 2026.
- **Links:** https://suno.com ; https://suno.com/release-notes ; https://www.musicbusinessworldwide.com/suno-launches-its-own-daw-after-introducing-most-powerful-model-yet/ ; WMG deal https://www.musicbusinessworldwide.com/warner-music-group-settles-with-suno-strikes-first-of-its-kind-deal-with-ai-song-generator/
- **What it is:** Text/lyrics-to-full-song with vocals. Editing affordances added over time: **Audio Input** (upload/record to extend, Jun 2024), **Stems** (vocal/instrumental split Jul 2024; later 12-stem export), **Covers** (keep melody, change style, Sep 2024), **Replace Section** (regenerate a time range, Oct 2024), **Personas** (save vocal/style identity, Oct 2024), **Remaster** (re-render with newer model, Nov 2024), **Extend**, **Add Vocals / Add Instrumental**, **Hooks** (short-form video). Suno Studio: multitrack timeline, generate stems/parts to match existing tracks, BPM/pitch/volume control, synths/effects, and (2026) MIDI. No public model details; no symbolic conditioning of the generator; not real-time. Legal: RIAA/major-label suits (Jun 2024) alleging stream-ripping; **WMG settled Nov 25 2025**—licensed models in 2026, current models deprecated, free tier non-downloadable, paid download caps, artist opt-in for name/voice; UMG/Sony suits and GEMA/Koda claims continued as of late 2025.
- **Evidence:** None public (no papers, no benchmarks). Wide anecdotal adoption; a Grammy-winning producer quoted in launch PR.
- **Why it matters for the studio:** The archetype the founder rejects—but its feature history (stems → replace-section → covers/personas → DAW → MIDI) is the strongest market evidence that users demand iterative, part-level, notation-adjacent control. Studio should offer what Suno Studio cannot: notation as the source of truth, explainable "compile", open weights and provenance.
- **Tags:** [audio-generation] [product] [editing] [text-conditioning] [ethics-legal] [DAW-plugin]
- **Verification:** verified (official release notes + MBW)
- **BibKey:** suno2026

### Udio — Udio (v1 → v1.5 → v1.5 Allegro) and the 2025 UMG/WMG walled-garden pivot
- **Who/where/when:** Uncharted Labs / Udio (NYC), founded Dec 2023 by ex-Google DeepMind researchers David Ding, Conor Durkan, Charlie Nash, Yaroslav Ganin, Andrew Sanchez; public beta Apr 10 2024; v1.5 Jul 23 2024; v1.5 Allegro Mar 18 2025; "Udio Playground" Oct 9 2025. **UMG settlement Oct 29 2025**; WMG deal Nov 2025.
- **Links:** https://www.udio.com ; https://en.wikipedia.org/wiki/Udio ; https://www.musicbusinessworldwide.com/universal-music-settles-udio-lawsuit-strikes-deal-for-licensed-ai-music-platform/
- **What it is:** Text/lyrics-to-song generating ~30-s segments that are **extended** forwards/backwards into full songs; **Remix** (re-generate with a new prompt from an existing clip), **audio Inpainting** (select a region and regenerate—premium), audio upload, stems. After the UMG deal: a **"walled garden"**—downloads disabled (48-h grace window), streaming/sharing only, fingerprinting and filtering, and a new subscription platform trained only on licensed music to launch in 2026. Closed model; no symbolic conditioning; not real-time.
- **Evidence:** None public.
- **Why it matters for the studio:** Udio pioneered mainstream *audio inpainting* in a consumer song tool, then became the first "licensed-only" platform—illustrating both the demand for region editing and the fragility of building on unlicensed corpora. A composer-centric open studio avoids both traps by rendering the composer's own material.
- **Tags:** [audio-generation] [product] [editing] [infilling] [ethics-legal]
- **Verification:** verified (Wikipedia + MBW); v2/2026 platform details partial
- **BibKey:** udio2025

### Lyria2-Sandbox — Google DeepMind Lyria / Lyria 2 / Music AI Sandbox / MusicFX DJ
- **Who/where/when:** Google DeepMind + YouTube (Music AI Incubator). Lyria announced Nov 2023 (Dream Track); **MusicFX DJ** + Sandbox multitrack/inpainting Oct 23 2024 (with Jacob Collier); **Lyria 2 + expanded Sandbox** Apr 24 2025 (US musicians); Lyria 2 on Vertex AI (I/O May 2025).
- **Links:** https://deepmind.google/blog/new-generative-ai-tools-open-the-doors-of-music-creation/ ; https://deepmind.google/blog/music-ai-sandbox-now-with-new-features-and-broader-access/ ; https://deepmind.google/models/lyria/
- **What it is:** Lyria (RL-tuned for quality/prompt adherence) powers: **Music AI Sandbox** with *Create* (text + optional lyrics placed on a timeline, key, tempo), *Extend* (continue uploaded/generated audio), *Edit* (transform mood/genre of a whole clip or a **selected region**, fill gaps, blend transitions—i.e., inpainting), multitrack views and loop generation; **MusicFX DJ** (real-time mixing of weighted text prompts with instrument toggles, brightness/chaos/density, key/tempo, 48 kHz stereo streaming). Lyria 2: 48 kHz stereo, "professional-grade". All outputs SynthID-watermarked. Closed weights; no symbolic (MIDI) input; key/tempo are the only structured controls.
- **Evidence:** Artist testimonials via YouTube Music AI Incubator; no published evaluations.
- **Why it matters for the studio:** The most "studio-like" closed system: timeline, region edit, extend, tempo/key. Its co-design with professional musicians (Collier et al.) is the closest existing analogue to a composer-in-the-loop product—but still audio-only.
- **Tags:** [audio-generation] [product] [editing] [infilling] [real-time] [controllability]
- **Verification:** verified
- **BibKey:** google2025lyria2

### LyriaRT-Lyria3 — Lyria RealTime API, Lyria 3 / 3.5, Gemini integration (2025–2026)
- **Who/where/when:** Google DeepMind / Google Labs. **Lyria RealTime** API in Gemini API / AI Studio Jun 12 2025 (announced I/O May 2025); **Lyria 3** Feb 2026 (with ProducerAI acquisition, Gemini app music); **Lyria 3.5** mid-2026 (3-minute songs, sharper vocals/lyrics; in Flow Music and Gemini).
- **Links:** https://magenta.withgoogle.com/lyria-realtime ; https://deepmind.google/models/lyria/lyria-realtime/ ; https://deepmind.google/models/lyria/
- **What it is:** Lyria RealTime is a **block-autoregressive streaming model** (48 kHz stereo) steered moment-to-moment by weighted blends of text prompts plus BPM, key, note density, brightness, instrumentation—**≤2 s from control change to audible effect**; open-sourced demo apps PromptDJ, **PromptDJ-MIDI** (physical MIDI controllers map to parameters), PromptDJ-Pad. Lyria 3/3.5: full songs with multilingual vocals, lyrics, image-to-music via Gemini, up to 3 min, SynthID; trained on music Google/YouTube "have the right to use".
- **Evidence:** No papers beyond "Live Music Models" (see Magenta RT); product claims.
- **Why it matters for the studio:** Real-time steering with MIDI *controllers* (parameters, not notes) is the closed-source ceiling for "jam with the AI"; the open counterpart (Magenta RT 2) now accepts MIDI *notes*.
- **Tags:** [audio-generation] [real-time] [product] [controllability] [multimodal-input] [image]
- **Verification:** verified (official pages); Lyria 3.5 details partial
- **BibKey:** google2025lyriarealtime

### AdobeMusicGenAIControl — Adobe Project Music GenAI Control
- **Who/where/when:** Adobe Research (Nicholas J. Bryan) with UC San Diego (Zachary Novack, Julian McAuley, Taylor Berg-Kirkpatrick) and CMU (Shih-Lun Wu, Chris Donahue, Shinji Watanabe); announced Feb 28 2024 (Hot Pod Summit); research prototype.
- **Links:** https://blog.adobe.com/en/publish/2024/02/28/adobe-research-audio-creation-editing
- **What it is:** Text-to-music followed by **fine-grained editing controls in the same workflow**: tempo, structure, repeating patterns, intensity, clip length, remix of a section, reference melody, seamless loops—"pixel-level control for music". Technically the productisation of Music ControlNet + DITTO (below). Never shipped publicly (as of 2026).
- **Evidence:** See Music ControlNet / DITTO papers.
- **Why it matters for the studio:** A major vendor framing the problem exactly as "generate, then *edit with musical parameters*", validating the loop; also shows that the research (ControlNet + inference-time optimisation) is mature enough to prototype.
- **Tags:** [audio-generation] [editing] [controllability] [product]
- **Verification:** verified
- **BibKey:** adobe2024musicgenaicontrol

### ElevenMusic — ElevenLabs Music (Eleven Music v1 Aug 2025; Music v2 2026)
- **Who/where/when:** ElevenLabs; launched Aug 2025 with licensing deals (Merlin, Kobalt — partial); Music v2 2026.
- **Links:** https://elevenlabs.io/music ; API docs https://elevenlabs.io/docs
- **What it is:** Text-to-song with vocals, **lyric editing throughout the track, section regeneration (verse/chorus/bridge) without restarting**, instrumentals, **2–6 stem export**, multilingual, mid-track genre transitions, long-form; API supports generation, **audio-reference matching, inpainting** and long-form composition. Claims training on licensed data only and "cleared for commercial use". Closed; no symbolic input; not real-time.
- **Evidence:** None public.
- **Why it matters for the studio:** Another commercial confirmation that section-level regeneration + stems + inpainting are baseline expectations; the licensed-data positioning is the new norm.
- **Tags:** [audio-generation] [product] [editing] [infilling] [ethics-legal]
- **Verification:** verified (product page); licensing partners partial
- **BibKey:** elevenlabs2025music

### Mureka — Mureka (Kunlun Tech / Skywork AI)
- **Who/where/when:** Kunlun Tech (Beijing); Mureka O1 / V6 announced Mar 2025 (O1 marketed as first "chain-of-thought" music model), later V7/V7.5 (2025) — versions partial.
- **Links:** https://www.mureka.ai
- **What it is:** Text/lyrics-to-song with Easy/Custom/Soundtrack modes, remix, reference-song style, vocals + instrumentals; API. Closed; no symbolic input.
- **Evidence:** None public; vendor claims of MOS parity with Suno.
- **Why it matters for the studio:** Shows the Chinese commercial ecosystem (alongside open YuE/ACE-Step/DiffRhythm from Chinese labs) converging on the same one-shot paradigm.
- **Tags:** [audio-generation] [product]
- **Verification:** partial (homepage confirms product; versions from recall)
- **BibKey:** mureka2025

### StableAudio25 — Stable Audio 2.5 (enterprise; inpainting; ARC post-training)
- **Who/where/when:** Stability AI; announced **Sep 10–11, 2025**. Underlying acceleration method: "Fast Text-to-Audio Generation with Adversarial Post-Training" (Zachary Novack, Zach Evans, Zack Zukowski, et al.; arXiv May 2025), which also produced **Stable Audio Open Small** (open weights).
- **Links:** https://stability.ai/news-updates/stability-ai-introduces-stable-audio-25-the-first-audio-model-built-for-enterprise-sound-production-at-scale ; ARC paper https://arxiv.org/abs/2505.08175
- **What it is:** 3-minute tracks in <2 s on GPU; multi-part structure (intro/development/outro); **inpainting** (upload audio, pick a region/start point, generate continuation/fill) and audio-to-audio; **ARC** = adversarial relativistic-contrastive post-training (first non-distillation acceleration for diffusion/flow), ~12 s of 44.1 kHz stereo in ~75 ms on H100 and ~7 s on a phone for the Open Small variant; "ping-pong" sampling. 2.5 trained on a "fully licensed dataset" (AudioSparx); available via API, fal, Replicate, ComfyUI, on-prem enterprise (WPP partnership). 2.5 weights closed; Open Small weights open.
- **Evidence:** ARC paper: latency/quality/CLAP trade-offs vs distillation baselines.
- **Why it matters for the studio:** Sub-second generation makes *interactive* recompilation feasible; inpainting-as-API is the primitive for "regenerate bars 17–24".
- **Tags:** [audio-generation] [editing] [infilling] [product] [real-time]
- **Verification:** verified (official announcement + arXiv)
- **BibKey:** novack2025arc

### SpliceLANDR — Splice and LANDR AI features (context only)
- **Who/where/when:** Splice (sample marketplace; "Create"/stack-based AI assembly, 2023; later AI search/"Skills"); LANDR (AI mastering since 2014; AI distribution/plugins).
- **Links:** https://splice.com ; https://www.landr.com
- **What it is:** Not generative music models per se: Splice uses retrieval/ML to assemble compatible sample stacks (key/tempo matched) and later added AI-assisted search and sample generation partnerships; LANDR is best known for automated mastering. Both are *tool-level* AI inside producer workflows rather than text-to-song.
- **Evidence:** None.
- **Why it matters for the studio:** Examples of AI as *assistant inside the DAW* (matching, mastering) rather than composer replacement—closer in spirit to the studio's "enabler" framing.
- **Tags:** [product] [DAW-plugin]
- **Verification:** unverified (recall; not fetched)
- **BibKey:** splice2025landr

## C. Meta AudioCraft family — controllable extensions (2024–2025)

### MAGNeT — Masked Audio Generation using a Single Non-Autoregressive Transformer
- **Who/where/when:** Alon Ziv, Itai Gat, Gael Le Lan, et al. (Tal Remez, Felix Kreuk, Alexandre Défossez, Jade Copet, Gabriel Synnaeve, Yossi Adi); Meta FAIR; ICLR 2024.
- **Links:** https://arxiv.org/abs/2401.04577 ; code/weights in AudioCraft
- **What it is:** Non-autoregressive masked generative modelling over EnCodec token streams with span masking, iterative decoding, and rescoring by an external model; hybrid AR-then-NAR variant. ~7× faster than MusicGen at comparable quality. Text only; weights CC-BY-NC.
- **Evidence:** Human + objective evaluation vs MusicGen/AudioGen; latency/throughput trade-offs analysed.
- **Why it matters for the studio:** Masked/iterative decoding is inherently editable (re-mask a region and re-decode)—a natural fit for local re-compilation.
- **Tags:** [audio-generation] [infilling] [text-conditioning]
- **Verification:** verified
- **BibKey:** ziv2024magnet

### MusicGenStyle — Audio Conditioning for Music Generation via Discrete Bottleneck Features (MusicGen-Style)
- **Who/where/when:** Simon Rouard, Yossi Adi, Jade Copet, Axel Roebel, Alexandre Défossez; Meta / IRCAM; ISMIR 2024.
- **Links:** https://arxiv.org/abs/2407.12563 ; code/weights in AudioCraft (musicgen-style)
- **What it is:** Conditions MusicGen on an **audio excerpt's style** via a discrete bottleneck (RVQ + heavy dropout) so the model copies *style* not *content*; also compares to textual inversion; **double classifier-free guidance** balances text vs audio conditioning at inference. Weights CC-BY-NC.
- **Evidence:** Automatic + human studies on style adherence vs text adherence.
- **Why it matters for the studio:** "Insert example audio" as an annotation channel—the composer drops in a reference track and the renderer adopts its style while keeping the composer's material.
- **Tags:** [audio-generation] [style-transfer] [multimodal-input] [controllability]
- **Verification:** verified (abstract; authors partial)
- **BibKey:** rouard2024musicgenstyle

### JASCO — Joint Audio and Symbolic Conditioning for Temporally Controlled Text-to-Music Generation
- **Who/where/when:** Or Tal, Alon Ziv, Itai Gat, Felix Kreuk, Yossi Adi; Hebrew University / Meta FAIR; ISMIR 2024 (arXiv Jun 2024).
- **Links:** https://arxiv.org/abs/2406.10970 ; project https://pages.cs.huji.ac.il/adiyoss-lab/JASCO ; code/weights in AudioCraft
- **What it is:** Flow-matching text-to-music model that accepts **symbolic local controls—chord progressions (time-aligned), melody (salience matrix)—and audio controls—separated drum track, full-mix embedding**, via information-bottleneck layers and temporal blurring. Generates ~10-s 32 kHz clips. Open code (MIT) and weights (CC-BY-NC 4.0).
- **Evidence:** Objective metrics + human study: comparable quality to baselines with "significantly better and more versatile controls" (chord/melody adherence).
- **Why it matters for the studio:** The clearest open example of **lead-sheet-style conditioning (chords + melody) of an audio model**—the basic "compile a lead sheet to audio" primitive. Clip length and NC license are limits.
- **Tags:** [audio-generation] [controllability] [symbolic-generation] [accompaniment] [text-conditioning]
- **Verification:** verified
- **BibKey:** tal2024jasco

### MelodyFlow — High Fidelity Text-Guided Music Editing via Single-Stage Flow Matching
- **Who/where/when:** Gael Le Lan, Bowen Shi, Zhaoheng Ni, et al. (12 authors incl. Wei-Ning Hsu, Vikas Chandra); Meta; arXiv Jul 2024 (rev. Oct 2024).
- **Links:** https://arxiv.org/abs/2407.03648 ; demo https://melodyflow.github.io ; weights (facebook/melodyflow) in AudioCraft
- **What it is:** Diffusion-transformer trained with flow matching on stereo variable-length audio; adapts **ReNoise latent inversion** to flow matching with regularisation for **zero-shot text-guided editing** of an existing clip (change genre/instrumentation while preserving melody/structure). Fast (few steps). Weights CC-BY-NC.
- **Evidence:** Outperformed ReNoise and DDIM inversion baselines on editing consistency/quality.
- **Why it matters for the studio:** Inversion-based editing keeps the composer's *content* fixed while changing rendering—analogous to re-orchestrating a passage.
- **Tags:** [audio-generation] [editing] [style-transfer]
- **Verification:** verified
- **BibKey:** lelan2024melodyflow

### MusicGenStem — MusicGen-Stem: Multi-stem Music Generation and Edition through Autoregressive Modeling
- **Who/where/when:** Simon Rouard, Robin San Roman, Yossi Adi, Axel Roebel; IRCAM / Meta; ICASSP 2025.
- **Links:** https://arxiv.org/abs/2501.01757 ; demo https://simonrouard.github.io/musicgenstem/ ; weights promised (AudioCraft)
- **What it is:** Trains **one EnCodec-style codec per stem (bass, drums, other)** and a MusicGen-style LM over the parallel token streams, so it can generate full mixes *or* **edit/regenerate one stem given the others** ("bass on top of existing drums"), enabling iterative, mixed-initiative composition. Text conditioning; ~30 s.
- **Evidence:** Objective metrics + subjective tests on stem-conditional generation quality and coherence.
- **Why it matters for the studio:** Directly implements "compile one part while others are fixed"—a stem-wise loop; also shows per-stem codecs as a representation choice.
- **Tags:** [audio-generation] [accompaniment] [editing] [mixed-initiative] [representation]
- **Verification:** verified
- **BibKey:** rouard2025musicgenstem

## D. Open-weights song generation and live models (2025–2026)

### ACEStep1 — ACE-Step: A Step Towards Music Generation Foundation Model (v1.0)
- **Who/where/when:** Junmin Gong, Sean Zhao (Wenxiao Zhao), Sen Wang, Shengyuan Xu, Jing Guo; **ACE Studio + StepFun**; arXiv May/Jun 2025; released May 2025.
- **Links:** https://arxiv.org/abs/2506.00045 ; code https://github.com/ace-step/ACE-Step ; https://ace-step.github.io
- **What it is:** Diffusion (flow) model over Sana's Deep Compression AutoEncoder (DCAE) latents with a lightweight *linear* transformer; semantic alignment via REPA to MERT and m-hubert. Generates up to 4 min of music with vocals in ~20 s on an A100 (≈15× faster than LM-based systems). Supports **variations, repainting (local re-generation of a time range), lyric editing (change words while keeping melody/accompaniment), lyric2vocal, singing2accompaniment, voice cloning, remixing** via LoRA controllers. Inputs: tags/caption + structured lyrics; audio reference; no MIDI. Apache-2.0.
- **Evidence:** Claims better structural coherence than diffusion-only baselines; internal comparisons only.
- **Why it matters for the studio:** First fully open model with a *menu of editing operations* (repaint / lyric-edit / variation) rather than one-shot generation—effectively an open Suno with edit primitives; Apache-2.0.
- **Tags:** [audio-generation] [editing] [infilling] [text-conditioning] [toolkit]
- **Verification:** verified
- **BibKey:** gong2025acestep

### ACEStep15 — ACE-Step 1.5: Pushing the Boundaries of Open-Source Music Generation
- **Who/where/when:** Junmin Gong, Yulin Song, Wenxiao Zhao, Sen Wang, Shengyuan Xu, et al.; **co-led by ACE Studio and StepFun**; arXiv Jan 31 / Feb 6 2026; XL (4B) release Apr 2 2026; repo v0.1.8 May 18 2026.
- **Links:** https://arxiv.org/abs/2602.00744 ; code https://github.com/ace-step/ACE-Step-1.5 ; https://ace-step.github.io
- **What it is:** **Hybrid LM-planner + Diffusion Transformer**: a language model (0.6B/1.7B/4B) converts a user query into a "song blueprint" (metadata, lyrics, captions via chain-of-thought), which conditions a DiT decoder over DCAE latents. New in 1.5 vs 1.0: LM planner; **intrinsic RL alignment** (no external reward model); **XL 4B DiT** series (base/sft/turbo); 8-step turbo; **cover generation, repainting (selective local editing), vocal-to-accompaniment, track separation, multi-track layering, lyric-structure control, BPM/key/time-signature metadata control, audio understanding (BPM/key extraction)**, 50+ languages, **LoRA from a few songs**. Speed: <2 s per full song on A100, <10 s on RTX 3090; runs from <4–6 GB VRAM (2B turbo, DiT only) to ≥24 GB (XL sft + 4B LM); CUDA/ROCm/Intel XPU/macOS MLX/CPU; Gradio UI, REST/Python API, **VST3 plugin**. **MIT license.** No MIDI/chord input; no training-data statement.
- **Evidence:** Tech report claims "quality beyond most commercial music models" (internal listening tests); no third-party benchmark.
- **Why it matters for the studio:** The strongest open candidate for the studio's *audio renderer/arranger* today: permissive license, consumer hardware, DAW plugin, and native repaint/cover/vocal→BGM primitives. Its LM-planner is essentially a "compiler front-end" from intent to blueprint—the studio can replace that planner with the composer's notation + annotations. Missing symbolic conditioning is the gap to fill (LoRA/ControlNet-style adapters on the DiT).
- **Tags:** [audio-generation] [editing] [infilling] [accompaniment] [LLM-agent] [toolkit] [DAW-plugin]
- **Verification:** verified (README + arXiv)
- **BibKey:** gong2026acestep15

### YuE — YuE: Scaling Open Foundation Models for Long-Form Music Generation
- **Who/where/when:** Ruibin Yuan, Hanfeng Lin, Shuyue Guo, Ge Zhang, Jiahao Pan, et al. (44 authors); Multimodal Art Projection (M-A-P) / HKUST / others; arXiv Mar 2025 (v2 Sep 2025); released Jan 2025.
- **Links:** https://arxiv.org/abs/2503.08638 ; code/weights https://github.com/multimodal-art-projection/YuE
- **What it is:** LLaMA-2-based two-stage LM (7B stage-1 over semantic tokens + 1B stage-2 acoustic + upsampler) for **lyrics-to-song up to 5 min** with **track-decoupled next-token prediction** (vocal and accompaniment tokens interleaved), structural progressive conditioning (segment-by-segment), and **in-context learning with a 30-s audio prompt** (single or dual-track) for style/voice transfer; bidirectional generation. Multilingual (EN/ZH/YUE/JA/KO). **Apache-2.0** code and weights, commercial use encouraged. Heavy: 24 GB VRAM minimum, ~360 s per 30 s on a 4090.
- **Evidence:** Human preference and objective metrics vs Suno/Udio-class systems (claims parity/superiority on some axes); strong MARBLE understanding transfer.
- **Why it matters for the studio:** Proof that open lyrics-to-song at commercial quality is possible; dual-track generation yields separable vocal/accompaniment stems; ICL-from-audio is a form of "insert example audio" annotation.
- **Tags:** [audio-generation] [text-conditioning] [accompaniment] [multimodal-input]
- **Verification:** verified
- **BibKey:** yuan2025yue

### DiffRhythm — DiffRhythm: Blazingly Fast and Embarrassingly Simple End-to-End Full-Length Song Generation with Latent Diffusion
- **Who/where/when:** Ziqian Ning, Huakang Chen, Yuepeng Jiang, et al. (Chunbo Hao, Guobin Ma, Shuai Wang, Jixun Yao, Lei Xie); ASLP Lab, Northwestern Polytechnical University; ACL 2025 (arXiv Mar 2025); DiffRhythm 2 arXiv 2510.22950 (Oct 2025).
- **Links:** https://arxiv.org/abs/2503.01183 ; code/weights https://github.com/ASLP-lab/DiffRhythm
- **What it is:** Non-autoregressive latent diffusion (DiT) generating **full songs up to 4 m 45 s in ~10 s** from **timestamped lyrics (.lrc) + a style prompt (text or reference audio)**; instrumental mode; v1.2 adds extension/editing; DiffRhythm+ variant. **Apache-2.0** code and weights; ≥8 GB VRAM.
- **Evidence:** Objective (FAD, intelligibility) and subjective results vs Suno/YuE-class baselines.
- **Why it matters for the studio:** Sentence-level lyric timestamps are a *structural, time-aligned* condition—closer to a score than free text; speed makes iterative re-rendering practical.
- **Tags:** [audio-generation] [text-conditioning] [structure] [editing]
- **Verification:** verified
- **BibKey:** ning2025diffrhythm

### SongGen — SongGen: A Single Stage Auto-regressive Transformer for Text-to-Song Generation
- **Who/where/when:** Zihan Liu, Shuangrui Ding, Zhixiong Zhang, et al. (Xiaoyi Dong, Pan Zhang, Yuhang Zang, Yuhang Cao, Dahua Lin, Jiaqi Wang); Shanghai AI Lab / CUHK; ICML 2025.
- **Links:** https://arxiv.org/abs/2502.13128 ; code/weights https://github.com/LiuZH-19/SongGen
- **What it is:** 1.3B single-stage AR transformer over X-Codec tokens; inputs = lyrics + descriptive text + optional 3-s voice reference; **mixed mode** (vocals+accompaniment jointly, "Mixed Pro" with auxiliary vocal target) and **dual-track mode** (separate vocal and accompaniment streams, interleaved). 30-s English songs; **Apache-2.0**; fully open data pipeline (~2k h).
- **Evidence:** Ablations of token patterns across modes; objective + MOS vs baselines.
- **Why it matters for the studio:** Small, fully open, and produces *separated* vocal/accompaniment—useful as a research baseline for stem-aware rendering.
- **Tags:** [audio-generation] [text-conditioning] [accompaniment] [toolkit]
- **Verification:** verified
- **BibKey:** liu2025songgen

### HeartMuLa — HeartMuLa family (HeartMuLa, HeartCodec, HeartTranscriptor, HeartCLAP)
- **Who/where/when:** HeartMuLa org (HKUST-affiliated team — institution partial); releases Dec 2025 – Feb 2026 (HeartMuLa-oss-3B "happy-new-year" Feb 13 2026); 7B internal.
- **Links:** https://github.com/HeartMuLa/heartlib
- **What it is:** Open-source song foundation model family: **HeartMuLa** (music LM, 3B open; 7B internal), **HeartCodec** (12.5 Hz audio codec), **HeartTranscriptor** (Whisper-based lyrics transcription), **HeartCLAP** (audio–text alignment). Inputs: lyrics + comma-separated tags (reference-audio conditioning planned); outputs full songs (default ≤240 s) at RTF≈1.0; multi-GPU or lazy-loaded single GPU. **Apache-2.0** code and weights.
- **Evidence:** Self-reported: 7B "comparable to Suno in musicality, fidelity and controllability"; no external benchmark.
- **Why it matters for the studio:** Representative of the 2026 wave of permissively licensed song models; its bundled transcription/CLAP tools are useful for annotation pipelines.
- **Tags:** [audio-generation] [text-conditioning] [toolkit] [transcription]
- **Verification:** verified (README); institution partial
- **BibKey:** heartmula2026

### MagentaRT — Magenta RealTime (v1, Jun 2025) / Magenta RealTime 2 (Jun 2026) and "Live Music Models"
- **Who/where/when:** Lyria Team, Google DeepMind (paper "Live Music Models", arXiv Aug 2025); Magenta RT v1 Jun 20 2025 (800M); **Magenta RT 2 Jun 4 2026** (230M small / 2.4B base).
- **Links:** paper https://arxiv.org/abs/2508.04651 ; code https://github.com/magenta/magenta-realtime ; https://magenta.withgoogle.com/magenta-realtime ; https://magenta.withgoogle.com/magenta-realtime-2
- **What it is:** "Live music models" produce a continuous audio stream with synchronised user control. v1: 800M encoder–decoder transformer over **SpectroStream** (48 kHz stereo codec) tokens, steered by weighted blends of text/audio prompt embeddings from **MusicCoCa**; 10-s context, 2-s chunks; ran on free Colab TPU; trained on ~190k h instrumental stock music; open weights (permissive + bespoke terms). **v2**: ~15× lower latency (40-ms frames, ~200 ms control latency), runs in real time on Apple Silicon (C++/MLX engine), causal sliding-window attention, **MIDI note control (Auto-Strum and precise-onset modes), drums on/off, multi-signal classifier-free guidance**; trained on ~71k h mostly-instrumental stock music with **MT3-inferred MIDI labels**; fine-tuning "coming soon". Open counterpart of Lyria RealTime.
- **Evidence:** Paper reports real-time factor and listening comparisons; product pages give latency figures.
- **Why it matters for the studio:** The only open, on-laptop, **MIDI-steerable real-time audio model**—the closest thing to an AI band member for a keyboardist; also the first open model whose training explicitly pairs audio with (transcribed) symbolic data. Limitation: short context (no long-form structure), instrumental only.
- **Tags:** [audio-generation] [real-time] [controllability] [symbolic-generation] [accompaniment] [toolkit]
- **Verification:** verified
- **BibKey:** lyria2025livemusic

## E. Controllable and editable audio generation (research, 2023–2026)

### MusicControlNet — Music ControlNet: Multiple Time-Varying Controls for Music Generation
- **Who/where/when:** Shih-Lun Wu, Chris Donahue, Shinji Watanabe, Nicholas J. Bryan; CMU + Adobe Research; IEEE/ACM TASLP 2024 (arXiv Nov 2023).
- **Links:** https://arxiv.org/abs/2311.07069 ; demo https://MusicControlNet.github.io/web/ — no code/weights
- **What it is:** ControlNet-style adapter on a spectrogram diffusion model giving **precise, time-varying control over melody (chroma), dynamics (loudness curve) and rhythm (beat/downbeat)**; controls can be **partially specified in time** (masking), so a composer can pin melody for bars 1–4 and leave the rest free. 35× fewer parameters and 11× less data than MusicGen.
- **Evidence:** 49% more faithful to input melodies than MusicGen (melody accuracy) with comparable quality; ablations on control combinations.
- **Why it matters for the studio:** Time-aligned, *partially specified* musical controls are exactly how annotations behave (a scribble over some bars); the model formalises "constrain here, improvise there".
- **Tags:** [audio-generation] [controllability] [annotation] [expression-performance]
- **Verification:** verified
- **BibKey:** wu2024musiccontrolnet

### CocoMulla — Content-based Controls for Music Large Language Modeling (Coco-Mulla)
- **Who/where/when:** Liwei Lin, Gus Xia, Junyan Jiang, Yixiao Zhang; NYU Shanghai / MBZUAI / QMUL; arXiv Oct 2023 (rev. 2024); ISMIR 2024 version "Arrange, Inpaint, and Refine".
- **Links:** https://arxiv.org/abs/2310.17162 ; code https://github.com/Kikyo-16/coco-mulla-repo
- **What it is:** Parameter-efficient (<4% params) fine-tuning of MusicGen to accept **chord progressions and drum tracks (MIDI/symbolic) plus pitch/melody content controls** alongside text, trained on <300 songs; supports arrangement and variation from symbolic input.
- **Evidence:** Chord/rhythm adherence and quality vs MusicGen baselines; low-resource training.
- **Why it matters for the studio:** Cheap recipe for teaching an existing audio LM to read *the composer's chords and drum MIDI*—the bridge from lead sheet to audio with tiny data.
- **Tags:** [audio-generation] [controllability] [symbolic-generation] [accompaniment]
- **Verification:** verified
- **BibKey:** lin2023cocomulla

### DITTO — DITTO: Diffusion Inference-Time T-Optimization for Music Generation / DITTO-2
- **Who/where/when:** Zachary Novack, Julian McAuley, Taylor Berg-Kirkpatrick, Nicholas J. Bryan; UC San Diego + Adobe Research; DITTO: ICML 2024 (oral); DITTO-2: ISMIR 2024.
- **Links:** https://arxiv.org/abs/2401.12179 ; https://arxiv.org/abs/2405.20289 ; demos https://DITTO-Music.github.io/web/ , https://ditto-music.github.io/ditto2/
- **What it is:** **Training-free control**: optimise the initial noise latents of a frozen text-to-music diffusion model through any differentiable feature-matching loss—yielding **inpainting, outpainting, looping, intensity (loudness curve), melody, and musical-structure (self-similarity) control** from one model. DITTO-2 distils the model (consistency-trajectory distillation) and optimises through a one-step surrogate, giving 10–20× speed-up (faster than real time) and new targets such as maximising CLAP text adherence.
- **Evidence:** SOTA on nearly all control tasks vs training-based baselines (Music ControlNet) and guidance methods; user-study/objective metrics; DITTO-2 improves both control and quality while much faster.
- **Why it matters for the studio:** General mechanism to turn *any* composer annotation with a computable target (a hummed contour, a dynamics sketch, a form diagram) into a constraint on a frozen renderer—no retraining per annotation type.
- **Tags:** [audio-generation] [controllability] [editing] [infilling] [structure] [annotation]
- **Verification:** verified
- **BibKey:** novack2024ditto

### MusicMagus — MusicMagus: Zero-Shot Text-to-Music Editing via Diffusion Models
- **Who/where/when:** Yixiao Zhang, Yukara Ikemiya, Gus Xia, et al. (Naoki Murata, Marco Martínez-Ramírez, Wei-Hsiang Liao, Yuki Mitsufuji, Simon Dixon); QMUL + Sony AI + MBZUAI; IJCAI 2024.
- **Links:** https://arxiv.org/abs/2402.06178 ; code https://github.com/ldzhangyx/MusicMagus
- **What it is:** Zero-shot editing of *generated* music by manipulating the text-embedding difference in latent space (word swap, e.g., "piano"→"guitar") with cross-attention constraints to keep unedited attributes; works with pretrained text-to-music diffusion (AudioLDM2). Edits genre, mood, instrument; limited on real (non-generated) audio.
- **Evidence:** Outperformed zero-shot and some supervised baselines on style/timbre transfer (CLAP, structure preservation, human ratings).
- **Why it matters for the studio:** Cheap "re-orchestrate this passage" via text edits; limitation on real audio motivates inversion methods (ZETA, MelodyFlow).
- **Tags:** [audio-generation] [editing] [style-transfer]
- **Verification:** verified
- **BibKey:** zhang2024musicmagus

### ZETA-ZEUS — Zero-Shot Unsupervised and Text-Based Audio Editing Using DDPM Inversion
- **Who/where/when:** Hila Manor, Tomer Michaeli; Technion; ICML 2024.
- **Links:** https://arxiv.org/abs/2402.10009 ; code https://github.com/HilaManor/AudioEditingCode ; https://hilamanor.github.io/AudioEditing/
- **What it is:** Applies **edit-friendly DDPM inversion** to AudioLDM2: **ZETA** = text-based editing of *real* recordings (change instrument/genre while preserving structure); **ZEUS** = unsupervised discovery of semantic edit directions (PCA of posterior-mean directions), enabling edits like "add/remove an instrument's participation" or **melodic improvisations** without any text.
- **Evidence:** Outperformed SDEdit/DDIM baselines on CLAP/LPAPS/FAD trade-offs; qualitative musical edits.
- **Why it matters for the studio:** Editing *the composer's own recordings* (not just model outputs) and discovering musically meaningful edit axes without labels—useful for exploration on a hummed take or a stem.
- **Tags:** [audio-generation] [editing] [style-transfer]
- **Verification:** verified
- **BibKey:** manor2024zeta

### AUDIT — AUDIT: Audio Editing by Following Instructions with Latent Diffusion Models
- **Who/where/when:** Yuancheng Wang, Zeqian Ju, Xu Tan, et al. (Lei He, Zhizheng Wu, Jiang Bian, Sheng Zhao); CUHK-Shenzhen + Microsoft Research Asia; NeurIPS 2023 (arXiv Apr 2023).
- **Links:** https://arxiv.org/abs/2304.00830 ; demo https://audit-demo.github.io/
- **What it is:** First **instruction-following audio editor**: trained on (instruction, input audio, output audio) triplets so users say "add a dog barking" / "replace the piano with guitar"; tasks: add, drop, replace, **inpainting**, super-resolution. Latent diffusion; general audio rather than music-specific.
- **Evidence:** SOTA objective and subjective results on constructed editing benchmarks.
- **Why it matters for the studio:** Establishes the "natural-language edit instruction over an existing clip" pattern later specialised to music (InstructME, Instruct-MusicGen).
- **Tags:** [audio-generation] [editing] [infilling] [text-conditioning]
- **Verification:** verified
- **BibKey:** wang2023audit

### InstructME — InstructME: An Instruction Guided Music Edit Framework with Latent Diffusion Models
- **Who/where/when:** Bing Han, Junyu Dai, Weituo Hao, et al. (Xinyan He, Dong Guo, Jitong Chen, Yuxuan Wang, Yanmin Qian); SJTU + ByteDance; IJCAI 2024 (arXiv Aug 2023). (Author list partial.)
- **Links:** https://arxiv.org/abs/2308.14360 ; demo https://musicedit.github.io/ — no code
- **What it is:** Music-specific instruction editor: **add / remove / extract / replace instruments and remix**, multi-round editing; a **chord-progression matrix** is injected as a condition to preserve harmony across edits; chunk transformer for long-range consistency.
- **Evidence:** Objective + subjective comparisons vs AUDIT-style baselines.
- **Why it matters for the studio:** Explicit harmonic conditioning inside an editor—edits stay true to the composer's chords.
- **Tags:** [audio-generation] [editing] [controllability] [symbolic-generation]
- **Verification:** verified (abstract + demo page); authors partial
- **BibKey:** han2023instructme

### InstructMusicGen — Instruct-MusicGen: Unlocking Text-to-Music Editing for Music Language Models via Instruction Tuning
- **Who/where/when:** Yixiao Zhang, Yukara Ikemiya, Woosung Choi, et al. (Naoki Murata, Marco A. Martínez-Ramírez, Liwei Lin, Gus Xia, Wei-Hsiang Liao, Yuki Mitsufuji, Simon Dixon); QMUL + Sony AI; ISMIR 2025 (arXiv May 2024).
- **Links:** https://arxiv.org/abs/2405.18386 ; code https://github.com/ldzhangyx/instruct-MusicGen
- **What it is:** Adds an audio-fusion and a text-fusion module to frozen MusicGen (+8% params, 5k steps) so it follows **"add / remove / separate a stem"** instructions over an input clip; open code and weights (inherits NC license).
- **Evidence:** Matches task-specific models on Slakh/MoisesDB-based editing metrics with tiny training cost.
- **Why it matters for the studio:** Cheap way to make an open audio LM stem-editable via language—useful for "add strings under the chorus" style annotations.
- **Tags:** [audio-generation] [editing] [accompaniment] [text-conditioning]
- **Verification:** verified
- **BibKey:** zhang2025instructmusicgen

### MuseControlLite — MuseControlLite: Multifunctional Music Generation with Lightweight Conditioners
- **Who/where/when:** Fang-Duo Tsai, Shih-Lun Wu, Weijaw Lee, et al. (Sheng-Ping Yang, Bo-Rui Chen, Hao-Chung Cheng, Yi-Hsuan Yang); National Taiwan University; ICML 2025.
- **Links:** https://arxiv.org/abs/2506.18729 ; code/weights https://github.com/fundwotsai2001/MuseControlLite
- **What it is:** 85M-parameter decoupled cross-attention adapters on **Stable Audio Open** with **rotary positional embeddings** for time-varying conditions—**melody, rhythm, dynamics—plus audio inpainting and outpainting**; 6.75× fewer trainable params than Stable Audio Open ControlNet.
- **Evidence:** Melody control accuracy 56.6%→61.1% with RoPE; beats MusicGen-Large and SAO-ControlNet on control metrics at lower cost.
- **Why it matters for the studio:** Practical, open, cheap recipe for a controllable *and* region-editable renderer on a CC-trained base—arguably the best starting point for a studio prototype's audio stage.
- **Tags:** [audio-generation] [controllability] [infilling] [editing] [toolkit]
- **Verification:** verified
- **BibKey:** tsai2025musecontrollite

### MelodyTextControlNetDiT — Editing Music with Melody and Text: Using ControlNet for Diffusion Transformer
- **Who/where/when:** Siyuan Hou, Shansong Liu, Ruibin Yuan, et al. (Wei Xue, Ying Shan, Mangsuo Zhao, Chao Zhang); Tsinghua + Tencent ARC + HKUST; ICASSP 2025 (arXiv Oct 2024). (Authors partial.)
- **Links:** https://arxiv.org/abs/2410.05151
- **What it is:** ControlNet branch on Stable Audio's DiT for **melody-conditioned editing**, using a **top-k constant-Q transform** melody representation to reduce ambiguity, with curriculum learning to balance text vs melody; variable-length generation/editing.
- **Evidence:** Better melody-controlled editing than MusicGen while retaining text-to-music quality (open instrumental data).
- **Why it matters for the studio:** Another route to "keep my melody, re-render everything else"—with a representation (CQT peaks) close to a transcribable pitch line.
- **Tags:** [audio-generation] [controllability] [editing] [style-transfer]
- **Verification:** partial (abstract fetched; authors from recall)
- **BibKey:** hou2024melodycontrolnet

### SongEditor — SongEditor: Adapting Zero-Shot Song Generation Language Model as a Multi-Task Editor
- **Who/where/when:** Chenyu Yang, Shuai Wang, Hangting Chen, et al. (Jianwei Yu, Wei Tan, Rongzhi Gu, Yaoxun Xu, Yizhi Zhou, Haina Zhu, Haizhou Li); CUHK-Shenzhen + Tencent AI Lab; AAAI 2025 (arXiv Dec 2024).
- **Links:** https://arxiv.org/abs/2412.13786 ; demo https://cypress-yang.github.io/SongEditor_demo/
- **What it is:** First **song-editing paradigm for LM-based song generation**: music tokenizer + AR LM + diffusion decoder; supports **segment-wise editing (regenerate a section with modified lyrics)** and **track-wise editing (vocals vs accompaniment)**, as well as full generation. Closed weights.
- **Evidence:** Objective + subjective metrics on editing coherence and lyric accuracy.
- **Why it matters for the studio:** Lyric-level, section-level editing of songs with vocals—the vocal counterpart of "edit the notation and recompile".
- **Tags:** [audio-generation] [editing] [infilling] [accompaniment]
- **Verification:** verified
- **BibKey:** yang2025songeditor

### SingSong — SingSong: Generating Musical Accompaniments from Singing
- **Who/where/when:** Chris Donahue, Antoine Caillon, Adam Roberts, et al. (Ethan Manilow, Philippe Esling, Andrea Agostinelli, Mauro Verzetti, Ian Simon, Olivier Pietquin, Neil Zeghidour, Jesse Engel); Google (Magenta/DeepMind); arXiv Jan 2023.
- **Links:** https://arxiv.org/abs/2301.12662 ; examples https://g.co/magenta/singsong — no code
- **What it is:** **Vocal → instrumental accompaniment**: source-separate a large corpus into (vocals, instrumental) pairs, then train AudioLM-style conditional generation (semantic + acoustic tokens) to produce accompaniment for a new a-cappella input; noise added to separated vocals to reduce bleed.
- **Evidence:** Listeners preferred SingSong accompaniments to retrieval baselines (~66% preference); ablations on separation artefacts.
- **Why it matters for the studio:** The canonical "sing → the AI arranges around you" system; directly instantiates the *hum/sing annotation → accompaniment* step.
- **Tags:** [audio-generation] [accompaniment] [humming] [multimodal-input]
- **Verification:** verified (abstract); authors partial
- **BibKey:** donahue2023singsong

### StemGen — StemGen: A Music Generation Model That Listens
- **Who/where/when:** Julian D. Parker, Janne Spijkervet, Katerina Kosta, et al. (Furkan Yesiler, Boris Kuznetsov, Ju-Chiang Wang, Matt Avent, Jitong Chen, Duc Le); ByteDance SAMI; ICASSP 2024.
- **Links:** https://arxiv.org/abs/2312.08723 ; examples https://julian-parker.github.io/stemgen/ — no weights
- **What it is:** Non-autoregressive masked transformer (MAGNeT/SoundStorm-style) that takes an **existing multi-stem musical context** and generates a **new stem** (e.g., bass given drums+keys) with a category token; improvements: causal bias sampling, classifier-free guidance over context.
- **Evidence:** FAD and MIR-descriptor alignment (key/tempo/chroma coherence with context) comparable to text-conditioned models; trained on open + proprietary data.
- **Why it matters for the studio:** Frames generation as *response to what's already there*—the essence of a co-arranger adding parts under a composer's material.
- **Tags:** [audio-generation] [accompaniment] [mixed-initiative]
- **Verification:** verified (arXiv + ICASSP listing)
- **BibKey:** parker2024stemgen

### MSDM — Multi-Source Diffusion Models for Simultaneous Music Generation and Separation
- **Who/where/when:** Giorgio Mariani, Irene Tallini, Emilian Postolache, et al. (Michele Mancusi, Luca Cosmo, Emanuele Rodolà); Sapienza University of Rome (GLADIA); ICLR 2024 (oral).
- **Links:** https://arxiv.org/abs/2302.02257 ; code https://github.com/gladia-research-group/multi-source-diffusion-models
- **What it is:** Learns the *joint* score of stems (Slakh2100: bass, drums, guitar, piano) so one diffusion model does **total generation, source separation (Dirac-likelihood inference), and source imputation—generate missing stems given the others** (e.g., piano to fit given drums). Open code/weights (research).
- **Evidence:** First single model for both generation and separation; competitive separation SI-SDR on Slakh; qualitative imputation.
- **Why it matters for the studio:** "Partial-score → complete arrangement" as *conditional sampling in a joint stem model*; also gives separation for free (annotating existing recordings).
- **Tags:** [audio-generation] [accompaniment] [infilling] [transcription]
- **Verification:** verified
- **BibKey:** mariani2024msdm

### DiffARiff — Diff-A-Riff: Musical Accompaniment Co-creation via Latent Diffusion Models
- **Who/where/when:** Javier Nistal, Marco Pasini, Cyran Aouameur, Maarten Grachten, Stefan Lattner; Sony CSL Paris; ISMIR 2024. (Follow-ups: Diff-A-Riff v2 / "Diff-MST" lineage at Sony CSL, 2025.)
- **Links:** https://arxiv.org/abs/2406.08384 ; https://sonycslparis.github.io/diffariff-companion/ — no weights
- **What it is:** Latent diffusion (consistency autoencoder, 48 kHz pseudo-stereo) that generates a **single instrumental accompaniment track fitting a given music context (mix)**, steerable by **audio reference (CLAP) and/or text**; low compute; designed for DAW workflows rather than whole-song generation.
- **Evidence:** Objective metrics + listening tests vs baselines; ablations of conditioning.
- **Why it matters for the studio:** Explicitly *co-creation*-oriented: one part at a time, matched to context, with example-audio steering—matches the "insert example audio" and "compile one part" primitives.
- **Tags:** [audio-generation] [accompaniment] [co-creation-framework] [multimodal-input]
- **Verification:** verified
- **BibKey:** nistal2024diffariff

### Text2FX — Text2FX: Harnessing CLAP Embeddings for Text-Guided Audio Effects
- **Who/where/when:** Annie Chu, Patrick O'Reilly, Julia Barnett, Bryan Pardo; Northwestern University; ICASSP 2025.
- **Links:** https://arxiv.org/abs/2409.18847 ; code https://github.com/anniejchu/text2fx
- **What it is:** Training-free: optimise **differentiable audio-effect parameters (EQ, reverb)** so the processed audio's CLAP embedding matches a text prompt ("warmer", "in-your-face"); parameters stay interpretable/editable; generalises to any differentiable effect and any shared text–audio space.
- **Evidence:** Listener study comparing algorithmic results with human perception of the prompts.
- **Why it matters for the studio:** Text annotations that adjust *interpretable production parameters* rather than regenerate audio—an "annotate → tweak the mix" path that keeps human control.
- **Tags:** [editing] [text-conditioning] [controllability] [expression-performance]
- **Verification:** verified
- **BibKey:** chu2025text2fx

### Sketch2Sound — Sketch2Sound: Controllable Audio Generation via Time-Varying Signals and Sonic Imitations
- **Who/where/when:** Hugo Flores García, Oriol Nieto, Justin Salamon, Bryan Pardo, Prem Seetharaman; Northwestern + Adobe Research; ICASSP 2025 (arXiv Dec 2024).
- **Links:** https://arxiv.org/abs/2412.08550 ; demo https://hugofloresgarcia.art/sketch2sound/
- **What it is:** Adds three **interpretable time-varying controls—loudness, spectral centroid (brightness), pitch**—to a text-to-audio DiT via one linear layer per control (40k fine-tune steps); controls are extracted from a **vocal imitation** or any "sonic sketch", with random median filtering at train time so users can choose how tightly to follow the gesture.
- **Evidence:** Retains text adherence and fidelity while following vocal-imitation control curves.
- **Why it matters for the studio:** "Hum/sing/vocalise a gesture" → time-aligned control of generation, with a tunable looseness knob—very close to the multimodal *sketch* annotation idea.
- **Tags:** [audio-generation] [humming] [sketch] [controllability] [multimodal-input]
- **Verification:** verified (abstract); authors partial
- **BibKey:** floresgarcia2025sketch2sound

### MIDIDDSP — MIDI-DDSP: Detailed Control of Musical Performance via Hierarchical Modeling
- **Who/where/when:** Yusong Wu, Ethan Manilow, Yi Deng, et al. (Rigel Swavely, Kyle Kastner, Tim Cooijmans, Aaron Courville, Cheng-Zhi Anna Huang, Jesse Engel); Mila / Google Magenta; ICLR 2022. Builds on **DDSP** (Engel, Hantrakul, Gu, Roberts; ICLR 2020).
- **Links:** https://arxiv.org/abs/2112.09312 ; code https://github.com/magenta/midi-ddsp ; DDSP https://arxiv.org/abs/2001.04643
- **What it is:** **Three-level hierarchy: notes (MIDI) → performance parameters (vibrato, attack, brightness, dynamics per note) → DDSP synthesis parameters (f0, harmonics, noise)**. Users can intervene at any level or let learned priors fill in ("expressive performance from score"). Monophonic orchestral instruments (URMP); open code/weights (Apache-2.0).
- **Evidence:** High-fidelity reconstruction, plausible performance prediction from notes, independent manipulation of expressive attributes; listening tests.
- **Why it matters for the studio:** The most direct realisation of "compile notation to audio while exposing every expressive knob"—a model of *interpretable* rendering the studio should generalise to polyphonic/ensemble writing.
- **Tags:** [expression-performance] [symbolic-generation] [controllability] [audio-generation] [notation]
- **Verification:** verified
- **BibKey:** wu2022mididdsp

### MusicHiFi — MusicHiFi: Fast High-Fidelity Stereo Vocoding
- **Who/where/when:** Ge Zhu, Juan-Pablo Caceres, Zhiyao Duan, Nicholas J. Bryan; University of Rochester + Adobe Research; IEEE Signal Processing Letters 2024 (arXiv Mar 2024). (Authors partial.)
- **Links:** https://arxiv.org/abs/2403.10493 ; demo https://MusicHiFi.github.io/web/
- **What it is:** Cascade of three GANs—mel → audio vocoder, **bandwidth extension** (downsampling-compatible), **mono → stereo upmix** (downmix-compatible)—to turn low-res mono model outputs into 44.1 kHz stereo quickly.
- **Evidence:** Comparable or better quality and spatialisation vs baselines with faster inference.
- **Why it matters for the studio:** A rendering back-end concern: many controllable models output 16–32 kHz mono; this shows the finishing stage can be modular and fast.
- **Tags:** [audio-generation] [toolkit]
- **Verification:** partial
- **BibKey:** zhu2024musichifi

### TTMUserStudy — AI-Assisted Music Production: A User Study on Text-to-Music Models
- **Who/where/when:** Francesca Ronchini, Luca Comanducci, Simone Marcucci, Fabio Antonacci; Politecnico di Milano; CMMR 2025 (arXiv Sep 2025).
- **Links:** https://arxiv.org/abs/2509.23364
- **What it is:** Qualitative study: **N = 17 music producers (7 countries)** used a custom tool combining **MusicGen** with **HT-Demucs 6-stem separation**; semi-structured interviews + thematic analysis.
- **Evidence:** Themes: "creative misalignment" between intent and output; integration pain around **tempo, key and beat alignment**; strong demand for **more control and editability**; 94% would use it for ideation, few for production; ethical concerns (copyright, compensation, homogenisation).
- **Why it matters for the studio:** Rare empirical evidence from working producers that text prompting alone fails at the *structural alignment* level (tempo/key/beat)—precisely what symbolic-first conditioning solves. Cross-cluster with HCI/co-creation studies.
- **Tags:** [HCI-study] [audio-generation] [evaluation] [creativity-support]
- **Verification:** verified (HTML full text)
- **BibKey:** ronchini2025ttmuserstudy

## F. Music understanding models, encoders and benchmarks (for annotation/critique)

### MERT — MERT: Acoustic Music Understanding Model with Large-Scale Self-supervised Training
- **Who/where/when:** Yizhi Li, Ruibin Yuan, Ge Zhang, et al. (20 authors incl. Yinghao Ma, Emmanouil Benetos, Jie Fu); M-A-P / Sheffield / QMUL / others; ICLR 2024.
- **Links:** https://arxiv.org/abs/2306.00107 ; weights https://huggingface.co/m-a-p/MERT-v1-330M ; code https://github.com/yizhilll/MERT
- **What it is:** HuBERT-style masked prediction with two teachers—an RVQ-VAE (EnCodec) acoustic teacher and a **CQT musical (pitch/harmony) teacher**; 95M and 330M; general-purpose music representation. **CC-BY-SA 4.0** (v1) weights. Used as encoder in MU-LLaMA, MusiLingo, ACE-Step (REPA), YuE evaluation.
- **Evidence:** SOTA/competitive across 14 MIR tasks (tagging, key, genre, emotion, beat, pitch, singer id…).
- **Why it matters for the studio:** The default open backbone for any audio-side annotation (key/chord/beat/emotion probes) and for embedding-based critique.
- **Tags:** [representation] [theory-analysis] [transcription] [toolkit]
- **Verification:** verified
- **BibKey:** li2024mert

### MuQ — MuQ: Self-Supervised Music Representation Learning with Mel Residual Vector Quantization
- **Who/where/when:** Haina Zhu, Yizhi Zhou, Hangting Chen, et al. (Jianwei Yu, Ziyang Ma, Rongzhi Gu, Yi Luo, Wei Tan, Xie Chen); Tencent AI Lab + SJTU; arXiv Jan 2025.
- **Links:** https://arxiv.org/abs/2501.01108 ; code/weights https://github.com/tencent-ailab/MuQ
- **What it is:** SSL music encoder using a light **Mel-RVQ** tokenizer as target (more stable/efficient than random projection or MERT's teachers) and **MuQ-MuLan**, a contrastive music–text model (open MuLan analogue). Open weights.
- **Evidence:** Beats MERT and MusicFM on downstream tasks with only 0.9k h pretraining; SOTA zero-shot tagging on MagnaTagATune.
- **Why it matters for the studio:** An open MuLan-style text–music embedding is needed for retrieval, text-adherence scoring, and DITTO/Text2FX-style optimisation targets.
- **Tags:** [representation] [text-conditioning] [evaluation] [toolkit]
- **Verification:** verified (abstract); authors partial
- **BibKey:** zhu2025muq

### LAION-CLAP — Large-scale Contrastive Language-Audio Pretraining with Feature Fusion and Keyword-to-Caption Augmentation
- **Who/where/when:** Yusong Wu, Ke Chen, Tianyu Zhang, et al. (Yuchen Hui, Marianna Nezhurina, Taylor Berg-Kirkpatrick, Shlomo Dubnov); LAION / UCSD / Mila; ICASSP 2023.
- **Links:** https://arxiv.org/abs/2211.06687 ; code/weights https://github.com/LAION-AI/CLAP ; dataset LAION-Audio-630K
- **What it is:** Contrastive text–audio encoders (HTSAT + RoBERTa) with feature fusion for variable-length audio; music-specific checkpoints exist. The de-facto text conditioner (AudioLDM, Stable Audio Open, Diff-A-Riff) and evaluation metric ("CLAP score").
- **Evidence:** SOTA text-to-audio retrieval and zero-shot classification at release.
- **Why it matters for the studio:** Shared text–audio space enables text annotations to act as loss functions (Text2FX, DITTO-2) and as retrieval of example audio.
- **Tags:** [representation] [text-conditioning] [evaluation] [dataset]
- **Verification:** verified
- **BibKey:** wu2023clap

### MULLaMA — Music Understanding LLaMA: Advancing Text-to-Music Generation with Question Answering and Captioning
- **Who/where/when:** Shansong Liu, Atin Sakkeer Hussain, Chenshuo Sun, Ying Shan; Tencent ARC / NUS; ICASSP 2024 (arXiv Aug 2023).
- **Links:** https://arxiv.org/abs/2308.11276 ; code https://github.com/shansongliu/MU-LLaMA
- **What it is:** MERT encoder + adapter + LLaMA for **music question answering and captioning**; introduces MusicQA (QA pairs generated from captioning datasets with MPT-7B). Open code/weights (research).
- **Evidence:** SOTA on MusicQA and captioning (BLEU/METEOR/ROUGE/BERTScore) vs LTU/LLaMA-Adapter at the time.
- **Why it matters for the studio:** Baseline architecture for an "annotator that answers questions about a clip"; also its dataset recipe.
- **Tags:** [LLM-agent] [annotation] [evaluation] [dataset]
- **Verification:** verified
- **BibKey:** liu2023mullama

### LLark — LLark: A Multimodal Instruction-Following Language Model for Music
- **Who/where/when:** Josh Gardner, Simon Durand, Daniel Stoller, Rachel M. Bittner; Spotify Research; ICML 2024.
- **Links:** https://arxiv.org/abs/2310.07160 ; code https://github.com/spotify-research/llark (training code; no weights)
- **What it is:** Jukebox-5B encoder + Llama-2 trained on instruction data auto-generated from open datasets' annotations (MusicCaps, YouTube8M-MusicTextClips, MusicNet, FMA, MTG-Jamendo, MagnaTagATune) for **music understanding (key, tempo, instruments), captioning and reasoning**.
- **Evidence:** Matches/outperforms baselines on understanding; high human agreement on captioning/reasoning; trained entirely on open data/models.
- **Why it matters for the studio:** Demonstrates that theory-level facts (key, tempo) can be produced conversationally from audio—an ingredient for automatic annotation of recordings.
- **Tags:** [LLM-agent] [annotation] [theory-analysis]
- **Verification:** verified
- **BibKey:** gardner2024llark

### MusiLingo — MusiLingo: Bridging Music and Text with Pre-trained Language Models for Music Captioning and Query Response
- **Who/where/when:** Zihao Deng, Yinghao Ma, Yudong Liu, et al. (Rongchen Guo, Ge Zhang, Wenhu Chen, Wenhao Huang, Emmanouil Benetos); QMUL / M-A-P; NAACL 2024 Findings (arXiv Sep 2023).
- **Links:** https://arxiv.org/abs/2309.08730 ; code https://github.com/zihaod/MusiLingo
- **What it is:** MERT + single projection layer + Vicuna, instruction-tuned on MusicCaps-derived captions and MusicInstruct QA; open weights.
- **Evidence:** Competitive captioning and QA vs MU-LLaMA / LTU.
- **Why it matters for the studio:** Lightweight open alternative for clip-level annotation.
- **Tags:** [LLM-agent] [annotation]
- **Verification:** partial
- **BibKey:** deng2024musilingo

### SALMONN — SALMONN: Towards Generic Hearing Abilities for Large Language Models
- **Who/where/when:** Changli Tang, Wenyi Yu, Guangzhi Sun, et al. (Xianzhao Chen, Tian Tan, Wei Li, Lu Lu, Zejun Ma, Chao Zhang); Tsinghua + ByteDance; ICLR 2024.
- **Links:** https://arxiv.org/abs/2310.13289 ; code https://github.com/bytedance/SALMONN
- **What it is:** Whisper (speech) + BEATs (audio) encoders → Q-Former → Vicuna; handles speech, audio events **and music** (captioning, QA); "activation tuning" unlocks emergent tasks (audio storytelling). Open weights.
- **Evidence:** Competitive on ASR/AST/emotion/music captioning; emergent zero-shot abilities.
- **Why it matters for the studio:** General "hearing" LLM able to describe hummed input, speech instructions and music in one model—relevant to a multimodal annotation front-end.
- **Tags:** [LLM-agent] [multimodal-input] [annotation]
- **Verification:** verified
- **BibKey:** tang2024salmonn

### AudioLLMs — Qwen2-Audio (2024) / Qwen2.5-Omni (2025) / Gemini 2.5 audio (2025)
- **Who/where/when:** Qwen2-Audio: Yunfei Chu, Jin Xu, Qian Yang, et al.; Alibaba Qwen; arXiv Jul 2024; 7B, Apache-2.0 weights. Qwen2.5-Omni: Qwen team; arXiv Mar 2025 (Thinker–Talker, 7B/3B, Apache-2.0). Gemini 2.5 Pro/Flash: Google DeepMind, 2025; native audio input (hours-long), closed API.
- **Links:** https://arxiv.org/abs/2407.10759 ; https://arxiv.org/abs/2503.20215 ; https://deepmind.google/models/gemini/
- **What it is:** General audio-language models with two modes (voice chat, audio analysis); trained on speech, sounds and music; can describe music (genre, instruments, mood), roughly estimate tempo and answer music questions, but are not music-specialised. Gemini 2.5 is the strongest closed generalist for long-audio understanding and is what the Music AI Sandbox / Flow Music pair with Lyria.
- **Evidence:** Qwen2-Audio beat Gemini-1.5-pro on AIR-Bench audio instruction tasks; on MuChoMusic-style music tests, open audio LLMs still show text over-reliance (see MuChoMusic).
- **Why it matters for the studio:** Off-the-shelf multimodal front-ends for parsing spoken/hummed/verbal annotations and producing first-draft critiques; not yet trustworthy for fine music-theory judgments.
- **Tags:** [LLM-agent] [multimodal-input] [annotation]
- **Verification:** partial (Qwen2-Audio abstract verified; others recall)
- **BibKey:** chu2024qwen2audio

### OpenMU — OpenMU: Your Swiss Army Knife for Music Understanding
- **Who/where/when:** Mengjie Zhao, Zhi Zhong, Zhuoyuan Mao, et al. (Shiqi Yang, Wei-Hsiang Liao, Shusuke Takahashi, Hiromi Wakaki, Yuki Mitsufuji); Sony; arXiv Oct 2024.
- **Links:** https://arxiv.org/abs/2410.15573 ; code/data https://github.com/mzhaojp22/openmu
- **What it is:** **OpenMU-Bench** (≈1M examples) covering music captioning, QA/reasoning, **lyrics understanding, ABC-notation understanding and tool use**; **OpenMU** model (LLaVA-style two-stage training) trained on it. Open.
- **Evidence:** Outperforms MU-LLaMA on the bench; ablations across task types.
- **Why it matters for the studio:** The only understanding benchmark that mixes *audio* with *symbolic notation (ABC)* and tool use—closest to what a studio critic/annotator must do.
- **Tags:** [LLM-agent] [evaluation] [dataset] [notation] [music-as-code]
- **Verification:** verified (GitHub README)
- **BibKey:** zhao2024openmu

### MuChoMusic — MuChoMusic: Evaluating Music Understanding in Multimodal Audio-Language Models
- **Who/where/when:** Benno Weck, Ilaria Manco, Emmanouil Benetos, Elio Quinton, George Fazekas, Dmitry Bogdanov; UPF Barcelona + QMUL + UMG; ISMIR 2024.
- **Links:** https://arxiv.org/abs/2408.01337 ; https://github.com/mulab-mir/muchomusic
- **What it is:** **1,187 human-validated multiple-choice questions on 644 tracks** (MusicCaps + Song Describer) spanning music knowledge (theory, instruments, structure) and reasoning (culture, function).
- **Evidence:** Five open audio LLMs (e.g., MU-LLaMA, MusiLingo, SALMONN, Qwen-Audio, M2UGen) evaluated; finding: **over-reliance on the language modality**—models often answer without using the audio.
- **Why it matters for the studio:** Cautionary evidence: current audio LLMs cannot yet be trusted as automatic critics; a symbolic-first studio can instead ground critique in notation/MIR features.
- **Tags:** [evaluation] [dataset] [LLM-agent]
- **Verification:** verified
- **BibKey:** weck2024muchomusic

### SongDescriber — The Song Describer Dataset: A Corpus of Audio Captions for Music-and-Language Evaluation
- **Who/where/when:** Ilaria Manco, Benno Weck, SeungHeon Doh, et al. (Minz Won, Yixiao Zhang, Dmitry Bogdanov, Yusong Wu, Ke Chen, Philip Tovstogan, Emmanouil Benetos, Elio Quinton, György Fazekas, Juhan Nam); QMUL / UPF / KAIST / others; NeurIPS 2023 ML4Audio workshop.
- **Links:** https://arxiv.org/abs/2311.10057 ; data https://zenodo.org/records/10072001
- **What it is:** **1.1k crowd-sourced captions for 706 CC-licensed tracks (MTG-Jamendo)**; used to evaluate captioning, text-to-music generation and retrieval (e.g., Stable Audio Open reports on it).
- **Evidence:** Shows cross-dataset performance variation vs MusicCaps.
- **Why it matters for the studio:** A clean-license evaluation set for any text-conditioned rendering the studio ships.
- **Tags:** [dataset] [evaluation]
- **Verification:** verified (abstract); authors partial
- **BibKey:** manco2023songdescriber

---

## Capability matrix (quick reference)

| System | Open weights / license | Symbolic conditioning (chords/melody/MIDI) | Region edit (inpaint/repaint) | Stems / accompaniment | Real-time |
|---|---|---|---|---|---|
| Jukebox | yes (MIT) | no (lyrics/artist only) | continuation only | no | no |
| MusicLM | no | hummed melody (audio) | no | no | no |
| MusicGen | code MIT / weights CC-BY-NC | melody chroma (audio) | no (via Instruct-MusicGen: stem add/remove) | MusicGen-Stem variant | no |
| AudioLDM/2 | yes | no | zero-shot inpaint | no | no |
| Stable Audio Open | Stability Community Lic. (CC data) | no (adapters: MuseControlLite melody/rhythm/dyn.) | via MuseControlLite | no | Open Small ≈75 ms/12 s |
| Stable Audio 2.5 | no | no | inpainting, audio-to-audio | no | <2 s / 3 min |
| JEN-1 / MusicFlow | no | no | native inpaint + continuation | no | no |
| Mustango | yes | chords/beats/key/tempo (text) | no | no | no |
| JASCO | CC-BY-NC | **chords + melody salience + drums** | no | drum-conditioned | no |
| Coco-Mulla | yes (research) | **chords + drum MIDI + pitch** | no | arrangement | no |
| Music ControlNet | no | melody/dynamics/rhythm curves, partial in time | partial | no | no |
| DITTO / DITTO-2 | method (code) | any differentiable feature (melody, structure, intensity) | inpaint/outpaint/loop | no | DITTO-2 faster than RT |
| ACE-Step 1.0 / 1.5 | **MIT** | no (BPM/key/time-sig metadata, lyrics structure) | **repaint, lyric edit, cover, variations** | **vocal→BGM, separation, multi-track** | <2 s/song on A100 |
| YuE | Apache-2.0 | no (lyrics + structure tags) | segment-wise continuation | dual-track vocal/acc. | no (slow) |
| DiffRhythm | Apache-2.0 | timestamped lyrics | v1.2 extend/edit | instrumental mode | 10 s / 4m45s |
| SongGen | Apache-2.0 | no | no | dual-track | no |
| HeartMuLa | Apache-2.0 | no | no | no | RTF≈1 |
| Suno v5.5 + Studio | no | MIDI import/edit in Studio (Aug 2026); generator prompt/audio-driven | Replace Section, Covers, Remaster, Extend | stems (12), Add Vocals/Instrumental | no |
| Udio | no | no | inpainting, remix, extend | stems | no |
| Lyria 2 / Music AI Sandbox | no | key/tempo, lyrics on timeline | Edit region, Extend, fill gaps | multitrack view | MusicFX DJ / Lyria RT ≤2 s |
| Magenta RT 2 | open weights | **live MIDI notes** + text/audio | n/a (streaming) | drums toggle | **~200 ms, on laptop** |
| MIDI-DDSP | Apache-2.0 | **full MIDI → expressive audio** (monophonic) | per-note parameters | single instrument | near-RT |
| ElevenLabs Music | no | no | section regen, inpainting (API) | 2–6 stems | no |
