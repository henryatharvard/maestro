# Cluster 07 — Infrastructure, Datasets, Computational Music Theory, Education & Games

## Overview
This cluster surveys the *substrate* an open-source, symbolic-first AI music studio would stand on: (A) notation engines, symbolic toolkits, browser audio/MIDI, synthesis and DAW-integration protocols, plus the arranger-keyboard / Band-in-a-Box lineage that is the historical ancestor of "type chords → get an arrangement"; (B) the symbolic and stem/caption datasets that actually exist in 2026, with sizes and licenses (the licensing picture is far messier than most generation papers admit); (C) computational music-theory models — Roman-numeral / functional-harmony labelers, structure segmentation, Schenkerian and schema work, and the new music-theory benchmarks for LLMs — which are the natural engines behind an "annotate" step; and (D) education and games — MIT 21M.385, Harmonix-derived research on game interfaces, music-as-code platforms (TunePad, EarSketch, Sonic Pi), and the first empirical papers on generative AI in composition teaching. Everything below was checked against primary sources in September 2026 unless marked otherwise; the web-search budget ran out midway, so several well-known older items are marked `partial` (recalled facts, not re-fetched).

## Key takeaways for the studio
- **Notation rendering is a solved-enough problem in the browser, but you must pick a lingua franca.** Verovio (C++→WASM, MEI-native, LGPL/GPL, v6.2 May 2026) gives engraving-quality SVG + MIDI + timemaps and reads MusicXML/Humdrum/ABC; OSMD (BSD-3, v2.0 June 2026) is MusicXML-native on top of VexFlow (MIT). MEI is richer for *annotations* (editorial layers, analytical markup) — a real asset for an annotate-heavy workflow; MusicXML is the interchange standard every DAW/notation app exports. MNX is still a W3C Community Group draft (partial).
- **The Python symbolic stack has consolidated**: symusic (C++/nanobind, 100×+ faster than pretty_midi) → MidiTok (10 tokenizations + BPE/Unigram, HF-integrated) → partitura (score/performance alignment, MEI/Kern/MusicXML) → music21 (v10.x, BSD-3, Python 3.12+, the analysis Swiss-army knife but slow on large corpora; MusicXML round-trip is good but lossy for layout). MusPy (last release 2022) is a useful dataset-loader design reference but is aging.
- **Web MIDI is still Chromium-only in practice** (Chrome 43+, Edge 79+, Firefox 108+ with a site-permission add-on; Safari desktop and iOS: no support, no roadmap as of 2026). A web studio needs a desktop shell (Tauri/Electron) or fallback for Apple users playing a Nord Stage in.
- **Browser synthesis is ready**: spessasynth (pure TS SF2/SF3/DLS, AudioWorklet, Apache-2.0), alphaTab's alphaSynth, FluidSynth via Emscripten, WebAudioFont. Tone.js (MIT) remains the de-facto scheduling/transport layer.
- **Notation-software market shifted in 2024**: Finale discontinued 26 Aug 2024 (MakeMusic sent users to Dorico at $149 crossgrade); MuseScore Studio 4.x is GPL-3, Qt 6.9, full SMuFL, and 4.7 (2026) added an online MP3→MSCZ converter (their first shipping "AI" feature); a new extensions framework to replace the QML plugin API was promised but deferred. MuseScore Studio 5 (started Dec 2025) targets automation, piano-roll, audio staves — i.e. converging on DAW features. This is the open-source editor to integrate with, not compete against.
- **Datasets: licenses decide what a research-grade studio can ship.** Truly permissive symbolic sets: Lakh MIDI (CC-BY 4.0, ~176k files), PDMX (CC-BY 4.0, >250k public-domain MusicXML), OpenScore Lieder (CC0, 1,200+ songs), GiantMIDI-Piano (CC-BY 4.0), ATEPP (CC-BY 4.0), Bach Doodle (CC-BY 4.0), Los Angeles MIDI (Apache-2.0 repo; provenance murky). Non-commercial: MAESTRO, Aria-MIDI (1.19M files, 100k h, CC-BY-NC-SA), Hooktheory/TheoryTab (CC-BY-NC-SA 3.0, "special permission" for notation uploads), DCML corpora (CC-BY-NC-SA), MetaMIDI (registration, no redistribution). Scraped MuseScore.com dumps (Xmader 2021) are legally toxic; PDMX shows the clean alternative.
- **Roman-numeral analysis is at ~45–50% full-label accuracy, ~80%+ on key** (AugmentedNet 2021 → ChordGNN 2023 → RNBert 2024). Good enough to *propose* annotations for a human to correct — exactly the mixed-initiative "annotate" step — not good enough to trust silently. When-in-Rome (2,000 analyses, RomanText) + DCML corpora are the training data; RomanText/.rntxt is a ready-made textual annotation format the studio could adopt.
- **Structure analysis for audio is mature (All-In-One 2023 does beats/downbeats/sections jointly); for symbolic pop it is Dai & Dannenberg's hierarchical repetition analysis.** Both are needed for the "compile" step to know verse/chorus boundaries.
- **LLMs do not yet know music theory reliably**: ChatMusician's MusicTheoryBench and MuChoMusic (ISMIR 2024) both show weak reasoning; use LLMs as glue/agents around symbolic analysers, not as the analyser.
- **The arranger-keyboard "style" paradigm (Korg i3 1993 → Yamaha Genos / Korg Pa) and Band-in-a-Box (chords + style → full arrangement, 4,400 h of RealTracks in 2026) are the direct ancestors of "compile."** Their strength is deterministic, editable, style-parameterized accompaniment; their weakness is genericness. The studio's "compile" can be framed as a learned, annotation-steerable descendant of the style engine.
- **Music-as-code pedagogy (TunePad, EarSketch, Sonic Pi) and Egozy's 21M.385** show composers *can* be taught to think of music as programs — evidence for the founder's compile metaphor and a source of interface ideas (live coding, cells, playbooks).

---

## A. Toolkits & engines

### music21 — music21: A Toolkit for Computer-Aided Musical Analysis and Computational Musicology
- **Who/where/when:** Michael Scott Cuthbert, Christopher Ariza et al.; MIT (cuthbertLab); ISMIR 2010 (toolkit paper); v10.x 2025–2026
- **Links:** https://github.com/cuthbertLab/music21 ; https://music21.org/music21docs/ ; ISMIR 2010 paper "music21: A Toolkit for Computer-Aided Musicology and Symbolic Music Data"
- **What it is:** Python library for parsing (MusicXML, MIDI, Humdrum/Kern, ABC, MEI import, Noteworthy, capella…), representing and analysing scores as a Stream hierarchy; includes Roman-numeral/key/chord analysis, voice-leading (`voiceLeading`), feature extraction (jSymbolic-style), a bundled corpus (Bach chorales, Beethoven quartets, Mozart, Palestrina, Essen folk, etc.), LilyPond/MuseScore rendering, and music21j (JS port). Current line v10 (v10.1 May 2025 → v10.5.0 June 2026): Python 3.12+ (drops 3.10), `uv` packaging, MIDI playback in Jupyter with soundfonts, ChordSymbol placement round-tripping in MusicXML, Dorico recognised as a MusicXML source (v9.9). License BSD-3-Clause.
- **Evidence:** Widely used in computational musicology; known limitations: pure-Python speed (parsing thousands of scores is slow — symusic benchmarks report 100×+ speedups on MIDI), MusicXML round-trip preserves pitch/rhythm/spanners well but not full layout; MEI export absent.
- **Why it matters for the studio:** The reference implementation for symbolic analysis and a source of analysis vocabulary (RomanNumeral, ChordSymbol, Key, voiceLeading) for an annotation layer; use it as an analysis backend, not as a real-time engine.
- **Tags:** [toolkit] [theory-analysis] [notation] [representation] [corpus]
- **Verification:** verified (GitHub README + releases fetched)
- **BibKey:** cuthbert2010music21

### Verovio — Verovio: A library for engraving MEI music notation into SVG
- **Who/where/when:** Laurent Pugin, Rodolfo Zitellini, Perry Roland et al.; RISM Digital (Bern); ISMIR 2014 paper; v6.2.0 May 2026
- **Links:** https://github.com/rism-digital/verovio ; https://www.verovio.org ; ISMIR 2014 paper "Verovio: A library for Engraving MEI Music Notation into SVG"
- **What it is:** C++20 engraving library (LGPL-3.0/GPL-3.0 dual) compiled to JS/WASM via Emscripten, with Python/Swift/Go/Java bindings. Input: MEI (native), MusicXML, Humdrum, ABC, Plaine & Easie, MuseData, EsAC. Output: SVG (with element IDs mapping back to MEI), MIDI, and a *timemap* for audio/score synchronisation. Also includes the Verovio Humdrum Viewer and online editor.
- **Evidence:** Engraving quality is close to commercial apps; used by RISM, Digital Mozart Edition, Beethovens Werkstatt, mei-friend editor.
- **Why it matters for the studio:** The best open-source route to an in-browser, engraving-quality, *annotatable* score: MEI supports editorial/analytical layers and every rendered glyph carries an ID, enabling scribble/sketch overlays and click-to-annotate tied to symbolic elements.
- **Tags:** [notation] [toolkit] [representation] [annotation]
- **Verification:** verified
- **BibKey:** pugin2014verovio

### OSMD — OpenSheetMusicDisplay
- **Who/where/when:** Andrea Zanchi (PhonicScore, Vienna) and contributors; 2016–; v2.0.0 June 2026
- **Links:** https://github.com/opensheetmusicdisplay/opensheetmusicdisplay ; https://opensheetmusicdisplay.org
- **What it is:** TypeScript MusicXML renderer for browser/Node built on VexFlow; BSD-3-Clause. Parses MusicXML into an internal graphical model and lays out systems automatically; a renderer, not an editor. Sponsor-only extras (OSMD Audio Player, React Native/iOS/Android examples). Documented gaps: some pedal marks, tremolo between notes, cross-staff slurs.
- **Evidence:** De-facto choice for MusicXML display in web music-ed apps; version 2.0 (2026) is the first major since 1.x.
- **Why it matters for the studio:** Fast path to displaying MusicXML from any notation app; pair with cursor/playback for score-following. For annotation depth, Verovio/MEI is stronger.
- **Tags:** [notation] [toolkit]
- **Verification:** verified
- **BibKey:** osmd2026

### VexFlow — VexFlow music notation rendering library
- **Who/where/when:** Mohit Muthanna Cheppudira (2010–) and contributors; v4.2.6 Aug 2024 stable; VexFlow 5 in development at github.com/vexflow/vexflow
- **Links:** https://github.com/0xfe/vexflow ; https://vexflow.com
- **What it is:** MIT-licensed TypeScript library rendering notation and tablature to SVG/Canvas; low-level (you place staves/voices) with EasyScore text API (`score.notes('C#5/q, B4')`). Used by OSMD, Flat (historically), many ed-tech apps.
- **Evidence:** 4.3k stars; long-lived; no automatic system/page layout — that is what OSMD adds.
- **Why it matters for the studio:** The building block for custom, non-standard views (e.g., sketch overlays, partial fragments, lead-sheet chord grids) where a full-score engraver is overkill.
- **Tags:** [notation] [toolkit]
- **Verification:** verified
- **BibKey:** vexflow2024

### alphaTab — cross-platform notation/tablature rendering with built-in synth
- **Who/where/when:** Daniel Kuschny (CoderLine); v1.8.3 May 2026
- **Links:** https://github.com/CoderLine/alphaTab ; https://alphatab.net
- **What it is:** MPL-2.0 TypeScript library (also .NET and Kotlin/Android builds) that renders Guitar Pro 3–7, alphaTex, and MusicXML to SVG/raster and plays them back via its own MIDI + SoundFont2 synthesizer (alphaSynth) through Web Audio, with cursor/score sync and tempo control.
- **Evidence:** 1.7k stars; one of the few OSS engines shipping notation + synchronised synth playback in one package.
- **Why it matters for the studio:** Reference architecture for "score + playback + cursor" in the browser; guitar/tab focus is complementary to piano-centric tools.
- **Tags:** [notation] [toolkit] [real-time]
- **Verification:** verified
- **BibKey:** alphatab2026

### abcjs — ABC notation renderer and player
- **Who/where/when:** Paul Rosen; v6.6.3 Apr 2026
- **Links:** https://github.com/paulrosen/abcjs ; https://abcjs.net
- **What it is:** JavaScript library rendering ABC text to SVG, with editor live-rendering, transposition, tablature, chord grids, and Web Audio playback via soundfonts. MIT license (partial: fetched page did not confirm license text).
- **Evidence:** 2.3k stars; the standard for ABC-on-the-web; ABC is also the notation LLMs (ChatMusician, MuPT) generate most fluently.
- **Why it matters for the studio:** Cheapest text↔notation round trip — an LLM can emit ABC and the user sees/edits notation instantly; ideal for lead-sheet-level "compile" drafts.
- **Tags:** [notation] [toolkit] [music-as-code]
- **Verification:** verified (license partial)
- **BibKey:** abcjs2026

### LilyPond — LilyPond music engraving program
- **Who/where/when:** Han-Wen Nienhuys, Jan Nieuwenhuizen (1996–) and community; v2.26.0 stable 21 Apr 2026; 2.27.x dev
- **Links:** https://lilypond.org ; https://gitlab.com/lilypond/lilypond
- **What it is:** GPL text-based engraver (`.ly` language, Scheme-extensible) producing PDF/SVG/MIDI; batch, not interactive. 2.26 consolidates changes since Oct 2022 branch (Guile 3, Cairo backend work). Used as the render backend by music21, Frescobaldi, Denemo.
- **Evidence:** Long regarded as the engraving-quality benchmark for OSS.
- **Why it matters for the studio:** A "music as code" ancestor: score-as-program compiled to notation — literally the founder's compile metaphor. Slow (seconds per page) so suited to final export, not live editing.
- **Tags:** [notation] [music-as-code] [toolkit] [history]
- **Verification:** verified
- **BibKey:** lilypond2026

### MuseScore Studio 4.x — open-source notation editor (Muse Group)
- **Who/where/when:** Muse Group (Martin Keary, Tantacrul; Peter Jonas et al.); 4.5 Feb 2025, 4.6 30 Sep 2025, 4.7.x 2026; MuseScore Studio 5 development started Dec 2025
- **Links:** https://musescore.org/en/4.6 ; https://musescore.org/en/4.7.4 ; https://musescore.org/en/4.5-and-beyond ; https://github.com/musescore/MuseScore
- **What it is:** GPL-3 notation editor (C++/Qt 6.9) with MuseSounds sample libraries (free, distributed via the proprietary Muse Hub app), VST3 hosting, MusicXML/MIDI import-export, and a QML plugin API (updated in 4.6 to expose all elements/properties added since 4.0; a replacement "extensions framework" was announced then deferred). 4.6: any SMuFL font, realtime MIDI note preview with duration/velocity, guitar techniques, TablEdit import. 4.7 (2026): engraving tools, audio-engine upgrades, and a File-menu shortcut to an online **MP3→MSCZ converter (beta)** — Muse Group's first shipped audio-to-score AI feature. Roadmap for 5.0: DAW-like automation, piano-roll, audio staves with time-stretch, MIDI mapping.
- **Evidence:** Most-used free notation software; musescore.com hosts millions of user scores (see PDMX / scraping entries).
- **Why it matters for the studio:** The obvious open editor to interoperate with (MSCZ/MusicXML), and its 5.0 direction (notation+DAW hybrid) overlaps the studio's; the limited, read-mostly plugin API is a known pain point.
- **Tags:** [notation] [product] [toolkit] [DAW-plugin]
- **Verification:** verified
- **BibKey:** musescore2026studio

### Finale sunset → Dorico / Sibelius — commercial notation landscape 2024–2026
- **Who/where/when:** MakeMusic (Finale) 26 Aug 2024; Steinberg Dorico 6 (2025), 6.2 10 Mar 2026; Avid Sibelius (subscription, ongoing)
- **Links:** https://www.makemusic.com/press-room/press-releases-2024/makemusic-sunsets-finale/ ; https://blog.dorico.com/2026/03/dorico-6-2-update-released/
- **What it is:** MakeMusic ended Finale development and sales (no further updates to Finale, PrintMusic, Songwriter, Notepad), citing "millions of lines of code" and OS churn; support through 26 Aug 2025; partnered with Steinberg to offer Dorico Pro at $149 (list $579). Dorico 6.x continues rapid iteration (6.2: repeat-barline cautionaries, European tab styles, harmonics popover, >70 fixes; Pro/Elements/SE/iPad). Sibelius remains (Ultimate/Artist/First, cloud sharing) — not re-verified here.
- **Evidence:** Verified by MakeMusic press release; Scoring Notes coverage.
- **Why it matters for the studio:** Shows the fragility of closed monoliths and the market gap (Finale users displaced); MusicXML export from Dorico/Sibelius is the interchange path; the studio should target MusicXML (and MEI) import robustly.
- **Tags:** [product] [notation] [history]
- **Verification:** verified
- **BibKey:** makemusic2024finale

### Soundslice — web notation + audio/video sync platform and API
- **Who/where/when:** Adrian Holovaty (Chicago), 2012–
- **Links:** https://www.soundslice.com ; https://www.soundslice.com/help/data-api/
- **What it is:** Browser player/editor where notation (MusicXML, Guitar Pro, PowerTab, TuxGuitar upload; PDF/image scanning via web UI) is synchronised to recordings (YouTube/Vimeo/MP3/video) through *syncpoints*; loop/slow-down/transpose for practice. Data API (Teacher/Licensing plans only; HTTP Basic auth) covers slices, notation upload/download & MusicXML export, recordings, syncpoints, lists; embed API for players. In 2025 Holovaty added ASCII-tab import after ChatGPT repeatedly hallucinated that Soundslice supported it (widely reported).
- **Evidence:** Commercial, closed; strong UX benchmark for notation↔audio alignment.
- **Why it matters for the studio:** The best worked example of aligning symbolic notation to reference audio — directly relevant to "insert example audio" annotations and rendering feedback loops.
- **Tags:** [product] [notation] [education] [multimodal-input]
- **Verification:** verified (API docs fetched)
- **BibKey:** soundslice2026

### Hookpad + Aria — Hooktheory's chord/melody sketchpad with theory hints and an AI co-writer
- **Who/where/when:** Hooktheory (Dave Carlton, Chris Anderson, Ryan Miyakawa); Aria launched Dec 2024, built on the Anticipatory Music Transformer (Chris Donahue's group, CMU/Stanford) fine-tuned on TheoryTab
- **Links:** https://www.hooktheory.com/hookpad ; https://www.hooktheory.com/hookpad/aria ; https://www.hooktheory.com/blog/generative-ai-songwriting/
- **What it is:** Browser songwriting tool where users enter chords (Roman-numeral/functional colour coding) and melody on a scale-degree grid, with theory "hints" (common next chords, borrowed chords), band-style playback, MIDI/MusicXML export. Aria: select a region → generate chord+melody continuation, chords under a melody, or melody over chords; context-aware; 10 free infills/day. Trained on >50,000 community TheoryTab analyses; training-data consent not discussed.
- **Evidence:** Commercial; no published user study. Anticipatory Music Transformer = Thickstun, Hall, Donahue, Liang 2023 (cross-cluster).
- **Why it matters for the studio:** The closest existing product to the founder's loop — symbolic, human-authored material + region-scoped AI infill + theory annotations shown inline. Its limits (lead-sheet granularity, no arrangement, no multimodal annotation) mark the studio's opportunity.
- **Tags:** [product] [symbolic-generation] [infilling] [theory-analysis] [education] [controllability]
- **Verification:** verified
- **BibKey:** hooktheory2024aria

### Flat.io / Noteflight — cloud notation editors with APIs
- **Who/where/when:** Flat (Tutteo, Paris, 2015–); Noteflight (Hal Leonard, 2008–)
- **Links:** https://flat.io/developers
- **What it is:** Flat: collaborative browser notation editor with REST API, Embed JS API (render/play/edit scores in your page), and "Edit on Flat" import API; MusicXML/MIDI import-export; Flat for Education. Noteflight: browser editor with Noteflight Learn (education), audio-recording assessment; API less open (partial).
- **Evidence:** Commercial; widely adopted in schools.
- **Why it matters for the studio:** Demonstrates embeddable editable notation as a service; the studio could either embed or, more consistently with its open ethos, build on Verovio/OSMD.
- **Tags:** [product] [notation] [education]
- **Verification:** partial (Flat page fetched; Noteflight recalled)
- **BibKey:** flat2026

### Web MIDI + Web Audio + Tone.js — browser audio/MIDI substrate (status 2026)
- **Who/where/when:** W3C Web MIDI API (Working Draft; Chris Wilson et al.); Web Audio API (W3C Recommendation 2021); Tone.js by Yotam Mann (2014–), MIT
- **Links:** https://caniuse.com/midi ; https://developer.mozilla.org/en-US/docs/Web/API/Web_MIDI_API ; https://github.com/Tonejs/Tone.js
- **What it is:** Web MIDI support: Chrome 43+, Edge 79+, Opera 30+, Samsung Internet, Firefox 108+ (via site-permission add-on); **Safari desktop and iOS: unsupported, no roadmap** (Apple cites fingerprinting). Web Audio API is universal; AudioWorklet enables sample-accurate DSP/WASM synths. Tone.js provides DAW-like Transport, scheduling, synths, effects, Sampler (npm v15.x 2024; GitHub release tags lag).
- **Evidence:** caniuse global support ~81%; the Safari gap is the single biggest platform risk for a web-first studio taking live keyboard input.
- **Why it matters for the studio:** Determines architecture: web UI for notation/annotation, but MIDI-controller input (Nord Stage) needs Chromium or a desktop wrapper; Tone.js is the natural playback/transport layer.
- **Tags:** [toolkit] [real-time]
- **Verification:** verified (caniuse, Tone.js repo); Tone.js version partial
- **BibKey:** w3c2026webmidi

### Browser synthesis: spessasynth, FluidSynth-WASM, alphaSynth, SoundFont/SFZ
- **Who/where/when:** spessasus (spessasynth_lib v4.3, Apache-2.0); FluidSynth (LGPL-2.1, 2002–; Emscripten ports e.g. js-synthesizer); SFZ format (rgc:audio 2002, open spec; sfizz LGPL/BSD player)
- **Links:** https://github.com/spessasus/spessasynth_lib ; https://github.com/spessasus/spessasynth_core ; https://www.fluidsynth.org ; https://sfzformat.com
- **What it is:** spessasynth: pure TypeScript SF2/SF3/DLS/SFOGG synthesizer running in an AudioWorklet or Worker, MIDI file read/write/playback, offline render to WAV, soundbank editing — no WASM needed. FluidSynth: the reference SoundFont synth (C), used server-side and via WASM in browsers. SFZ: text-based sample-instrument format widely used for free orchestral libraries.
- **Evidence:** spessasynth is actively maintained (2025–26); FluidSynth remains the standard for offline MIDI→audio rendering in research pipelines (used by symusic via prestosynth, MusPy).
- **Why it matters for the studio:** Enables immediate audition of symbolic output in-browser and headless rendering for evaluation; SF2/SFZ give a free, redistributable sound palette (GM soundfonts, Salamander piano, VSCO).
- **Tags:** [toolkit] [real-time] [audio-generation]
- **Verification:** verified (spessasynth); FluidSynth/SFZ partial
- **BibKey:** spessasynth2026

### symusic — a swift and unified toolkit for symbolic music processing
- **Who/where/when:** Yikai Liao, Zhongqi Luo et al.; ISMIR 2024 Late-Breaking Demo; v0.5–0.6 2025–26
- **Links:** https://github.com/Yikai-Liao/symusic ; https://symusic.readthedocs.io
- **What it is:** C++20 core with nanobind Python bindings; loads/saves MIDI and ABC; tick/quarter/second time units; vectorised transforms (shift pitch/time/velocity, filter), piano-roll extraction, NumPy/pickle serialisation, SoundFont synthesis via prestosynth. MIT.
- **Evidence:** Benchmarks show parsing "hundreds of times faster" than mido/pretty_midi/miditoolkit; adopted as MidiTok's I/O backend.
- **Why it matters for the studio:** The performance backbone for corpus-scale preprocessing and low-latency in-app MIDI manipulation.
- **Tags:** [toolkit] [representation]
- **Verification:** verified
- **BibKey:** liao2024symusic

### MidiTok — MIDI tokenization for deep learning
- **Who/where/when:** Nathan Fradet, Jean-Pierre Briot, Fabien Chhel, Amal El Fallah Seghrouchni, Nicolas Gutowski; Sorbonne/LIP6; ISMIR 2021 LBD; v3.0.x 2025
- **Links:** https://github.com/Natooz/MidiTok ; https://miditok.readthedocs.io
- **What it is:** Python package (MIT) implementing REMI, REMI+, MIDI-Like, TSD, Structured, CPWord, Octuple, MuMIDI, MMM, PerTok tokenizers with BPE/Unigram/WordPiece vocabulary training (HF tokenizers backend), data augmentation, PyTorch datasets, HF Hub push/pull; symusic I/O.
- **Evidence:** Standard tokeniser in symbolic-generation papers 2022–2026; companion paper "Byte Pair Encoding for Symbolic Music" (Fradet et al., EMNLP 2023).
- **Why it matters for the studio:** Any in-house symbolic model (infill, continuation, arrangement) will need a tokeniser; MidiTok is the interoperable default and its MMM/bar-infilling tokenisations map directly onto region-scoped editing.
- **Tags:** [toolkit] [representation] [symbolic-generation]
- **Verification:** verified
- **BibKey:** fradet2021miditok

### MusPy — a toolkit for symbolic music generation
- **Who/where/when:** Hao-Wen Dong, Ke Chen, Julian McAuley, Taylor Berg-Kirkpatrick; UC San Diego; ISMIR 2020; v0.5.0 Apr 2022
- **Links:** https://github.com/salu133445/muspy ; https://arxiv.org/abs/2008.01951
- **What it is:** MIT Python library unifying dataset download/management (Lakh, MAESTRO, NES-MDB, JSB, Nottingham, Essen, Wikifonia…), I/O (MIDI, MusicXML, ABC, note-seq, pretty_midi, music21), representations (pitch, event, piano-roll, note) and objective metrics (pitch-class entropy, scale consistency, groove consistency) plus rendering via FluidSynth.
- **Evidence:** ISMIR 2020 paper includes a cross-dataset generalisation study; maintenance slowed after 2022.
- **Why it matters for the studio:** Blueprint for a dataset/representation abstraction layer and for objective metrics in an evaluation harness.
- **Tags:** [toolkit] [dataset] [evaluation] [representation]
- **Verification:** verified
- **BibKey:** dong2020muspy

### partitura — Python package for symbolic music processing (score–performance)
- **Who/where/when:** Carlos Cancino-Chacón, Silvan Peter, Emmanouil Karystinaios, Francesco Foscarin, Maarten Grachten, Gerhard Widmer; JKU Linz; ISMIR 2019 LBD, MEC 2022; v1.9.0 May 2026
- **Links:** https://github.com/CPJKU/partitura ; https://partitura.readthedocs.io
- **What it is:** Apache-2.0 library parsing MusicXML, MEI, Humdrum **kern, MIDI into a `Score` with structured note arrays; performance MIDI handling; score–performance alignment (Match files); performance-feature extraction; export to MIDI/MusicXML/WAV. Basis of JKU's expressive-performance (Basis Mixer), score-following (ACCompanion) and GNN analysis (ChordGNN, cadence detection) work.
- **Evidence:** ERC "Whither Music?" funded; actively released through 2026.
- **Why it matters for the studio:** The toolkit for linking notation to human performances (e.g., the founder playing a passage on the Nord as an annotation of how a phrase should feel).
- **Tags:** [toolkit] [representation] [expression-performance] [notation]
- **Verification:** verified
- **BibKey:** cancinochacon2022partitura

### mido / pretty_midi / miditoolkit / note-seq — legacy Python MIDI stack
- **Who/where/when:** mido (Ole Martin Bjørndalen, 2013–, MIT); pretty_midi (Colin Raffel & Daniel Ellis, ISMIR 2014 LBD, MIT); miditoolkit (Yu-Siang Huang, 2020, MIT; tick-based, used by REMI/Compound Word); note-seq (Google Magenta, Apache-2.0) with the `NoteSequence` protobuf (music.proto) used across Magenta models
- **Links:** https://github.com/mido/mido ; https://github.com/craffel/pretty-midi ; https://github.com/YatingMusic/miditoolkit ; https://github.com/magenta/note-seq/blob/main/note_seq/protobuf/music.proto
- **What it is:** mido = message-level MIDI I/O and real-time ports (rtmidi); pretty_midi = note-level, seconds-based API with tempo-map handling and FluidSynth rendering; miditoolkit = tick-preserving alternative; NoteSequence = language-neutral protobuf schema (notes, tempos, time signatures, pitch bends, control changes) with quantisation utilities.
- **Evidence:** Still the most common dependencies in MIR code; symusic now outperforms them but exposes compatible concepts.
- **Why it matters for the studio:** Interop requirement — most public checkpoints and datasets are read with these; NoteSequence is a proven serialisation design for an internal symbolic IR.
- **Tags:** [toolkit] [representation]
- **Verification:** partial (recalled; note-seq proto URL confirmed by search snippet)
- **BibKey:** raffel2014prettymidi

### Magenta.js / MIDI-DDSP — browser inference for Magenta models
- **Who/where/when:** Google Magenta (Adam Roberts, Curtis Hawthorne, Monica Dinculescu et al.); @magenta/music 1.x (2018–2021), Apache-2.0; MIDI-DDSP (Yusong Wu et al., ICLR 2022)
- **Links:** https://github.com/magenta/magenta-js ; https://github.com/magenta/midi-ddsp ; https://magenta.github.io/magenta-js/music/demos/
- **What it is:** TypeScript/TensorFlow.js packages running MusicVAE, MelodyRNN, DrumsRNN, PerformanceRNN, ImprovRNN (plus Onsets&Frames, Piano Genie, GANSynth, DDSP in later releases) in the browser; MIDI-DDSP renders MIDI to expressive monophonic instrument audio with note-level expression controls (Colab demo; no maintained browser build). Magenta.js has no recent releases — effectively frozen; Magenta's active work moved to Magenta RealTime (2025, audio).
- **Evidence:** Demos powered many 2018–2021 co-creation prototypes (e.g., Bach Doodle used Coconet in TF.js).
- **Why it matters for the studio:** Proof that small symbolic models run client-side; but the stack is stale — plan on ONNX Runtime Web / WebGPU or server inference instead.
- **Tags:** [toolkit] [symbolic-generation] [expression-performance] [history]
- **Verification:** verified (magenta-js README); MIDI-DDSP partial
- **BibKey:** roberts2018magentajs

### DAW integration protocols — VST3, CLAP, AU, ReaScript, Ableton Link, Max for Live
- **Who/where/when:** VST3 (Steinberg, SDK dual GPLv3/proprietary); CLAP (u-he + Bitwig, announced June 2022, MIT, C ABI); Audio Units (Apple); ReaScript (Cockos REAPER: Lua/EEL2/Python scripting of the DAW); Ableton Link (Ableton, 2016, GPLv2+ with commercial option; tempo/beat/phase sync over LAN); Max for Live (Cycling '74/Ableton)
- **Links:** https://github.com/free-audio/clap ; https://github.com/Ableton/link ; https://www.reaper.fm/sdk/reascript/reascript.php ; https://steinbergmedia.github.io/vst3_dev_portal/
- **What it is:** Plugin ABIs let a studio "compiler" appear inside a DAW as an instrument/MIDI-effect; CLAP is the permissively-licensed, extension-based alternative to VST3 with per-note modulation and thread-pool hosting, supported by Bitwig, REAPER, FL Studio, MultitrackStudio and via NIH-plug/iPlug2/JUCE 8. ReaScript enables scripted manipulation of REAPER projects (used by many MIR/AI bridges). Link syncs tempo across apps — an easy way to keep a browser studio in time with Ableton Live.
- **Evidence:** CLAP README (fetched) confirms stable 1.x ABI and MIT; adoption details recalled.
- **Why it matters for the studio:** Composers live in DAWs; a CLAP/VST3 bridge plus Link keeps the studio a co-creator inside existing workflows rather than another island.
- **Tags:** [DAW-plugin] [toolkit] [real-time]
- **Verification:** partial (CLAP verified; others recalled)
- **BibKey:** clap2022

### Arranger keyboards — Korg i3 (1993) and the "style" paradigm (Yamaha Genos, Korg Pa)
- **Who/where/when:** Korg i3 "Interactive Music Workstation", 1993 (Japan); lineage i2/i4S/i5S → i30/iS series (1998) → Pa-series (2001–, Pa5X 2022); Yamaha PSR → Tyros → Genos (2017) / Genos2 (2023); Roland G-800/E-series; Korg reused the "i3" name in 2020
- **Links:** https://en.wikipedia.org/wiki/Korg_i3 ; https://www.korg.com/us/products/synthesizers/i3/ ; https://www.muzines.co.uk/articles/korg-i3/7651
- **What it is:** The i3 established the "pro arranger" category: 48 styles × (4 variations, 2 fills, 2 intros/endings), chord recognition from the left hand driving multi-part accompaniment (drums, bass, 3–4 accompaniment parts), AI² synthesis (32 voices, 340 programs), 16-track GM sequencer plus a "Backing Sequencer" that records the style performance into an editable song. Modern arrangers (Genos2, Pa5X) add hundreds of styles, style-creator editors, chord-sequencer, audio styles, and MIDI implementations exposing style parts on fixed channels.
- **Evidence:** Wikipedia/Music Technology Nov 1993 review; $2,500 launch price; "inspired Roland G-800 and Yamaha PSR variants."
- **Why it matters for the studio:** The founder's formative instrument is literally a rule-based "compile" engine: human chords + a parameterised style → arrangement, then editable in a sequencer. The studio can be framed as the learned, annotation-steered successor, keeping the arranger's virtues (instant, deterministic, editable) and fixing its genericness.
- **Tags:** [history] [accompaniment] [product] [real-time]
- **Verification:** verified (Wikipedia); Genos/Pa details partial
- **BibKey:** korg1993i3

### Band-in-a-Box — chords + style → full arrangement (PG Music, 1990–2026)
- **Who/where/when:** PG Music (Peter Gannon, Victoria BC); first Atari/PC release 1990; RealTracks (recorded musicians, 2007–); Band-in-a-Box 2026 (Windows/Mac)
- **Links:** https://www.pgmusic.com ; https://www.pgmusic.com/manuals/bbw2026full/chapter7.htm
- **What it is:** Type chord symbols (C, Fm7, C13b9) into a bar grid, choose a style → complete arrangement (piano, bass, drums, guitar, strings/horns) rendered either as MIDI styles or as time-stretched, pitch-shifted **RealTracks** audio (>4,400 hours of studio recordings in 2026; 202 new sets this year). 2026 adds a redesigned GUI, Multi-View, and "AI-Notes" polyphonic audio→MIDI transcription. Also melodist/soloist generators, notation view, export to DAW (RealBand, DAW plugin).
- **Evidence:** Continuous commercial development for 36 years; closed source.
- **Why it matters for the studio:** The longest-lived "compile" product: symbolic, human-authored input (chords) → arrangement; its style library/RealTracks show the value of curated, licensed performance data over generic synthesis — and its dated UX shows the room for an annotation-driven, notation-first alternative.
- **Tags:** [accompaniment] [product] [history] [symbolic-generation]
- **Verification:** verified (2026 product page); history partial
- **BibKey:** pgmusic2026biab

### Nord Stage (MIDI implementation basics)
- **Who/where/when:** Clavia (Stockholm); Nord Stage 4 (2023) is current — a "Nord Stage 6" does not exist as of Sept 2026 (not verified; the founder's instrument is likely a Stage 3 or 4)
- **Links:** https://www.nordkeyboards.com/products/nord-stage-4 (manual PDF lists MIDI implementation)
- **What it is:** Stage 3/4 transmit on a global MIDI channel with per-section (Organ/Piano/Synth) channels optionally, Program Change/Bank Select for program selection, CC for panel controls, and USB-MIDI class-compliant output — i.e., trivially usable as a Web MIDI input device in Chromium.
- **Evidence:** Not re-fetched.
- **Why it matters for the studio:** Confirms the "hum/play it in" annotation path is a plain MIDI input problem; program-change mapping can select studio sounds from the keyboard.
- **Tags:** [product] [real-time]
- **Verification:** unverified (recall)
- **BibKey:** clavia2023nordstage4

---

## B. Datasets & corpora

### Lakh MIDI Dataset (LMD) — 176,581 unique MIDI files
- **Who/where/when:** Colin Raffel; Columbia University; PhD thesis "Learning-Based Methods for Comparing Sequences…" 2016
- **Links:** https://colinraffel.com/projects/lmd/
- **What it is:** 176,581 deduplicated MIDI files scraped from the web; LMD-matched (45,129 files aligned to Million Song Dataset entries) and LMD-aligned subsets. License CC-BY 4.0 for the collection; the MIDI files are user transcriptions of copyrighted songs (legal grey zone for downstream commercial use).
- **Evidence:** The most-used multitrack symbolic training set 2016–2024 (MuseGAN, MMM, MidiCaps, etc.); quality is very uneven (many files are GM karaoke-style).
- **Why it matters for the studio:** Primary source of multi-instrument arrangements for training/eval "compile" models; quality filtering essential.
- **Tags:** [dataset] [corpus] [ethics-legal]
- **Verification:** partial (recalled; widely documented)
- **BibKey:** raffel2016lakh

### MAESTRO — MIDI and Audio Edited for Synchronous TRacks and Organization
- **Who/where/when:** Curtis Hawthorne, Andriy Stasyuk, Adam Roberts et al.; Google Magenta; ICLR 2019 ("Enabling Factorized Piano Music Modeling and Generation with the MAESTRO Dataset"); v3.0.0 2021
- **Links:** https://magenta.tensorflow.org/datasets/maestro ; https://arxiv.org/abs/1810.12247
- **What it is:** ~200 hours, 1,276 performances from the International Piano-e-Competition (Yamaha Disklavier), audio + fine-aligned MIDI (~3 ms), composer/title metadata, train/val/test splits. License CC-BY-NC-SA 4.0.
- **Evidence:** Standard benchmark for piano transcription (Onsets & Frames) and expressive piano generation (Music Transformer, Perceiver-AR).
- **Why it matters for the studio:** Gold standard for expressive performance MIDI; the NC license blocks use in a commercial product but not in a research-grade open studio.
- **Tags:** [dataset] [expression-performance] [transcription]
- **Verification:** partial (recalled)
- **BibKey:** hawthorne2019maestro

### GiantMIDI-Piano — 10,855 transcribed classical piano pieces
- **Who/where/when:** Qiuqiang Kong, Bochen Li, Jitong Chen, Yuxuan Wang; ByteDance; arXiv 2020, TISMIR 2022
- **Links:** https://github.com/bytedance/GiantMIDI-Piano ; https://arxiv.org/abs/2010.07061
- **What it is:** 10,855 MIDI files / ~1,237 hours from 2,786 composers, transcribed from YouTube solo-piano audio with Kong's high-resolution transcription model; curated subset 7,236 files (1,787 composers). CC-BY 4.0. Repo archived (read-only) April 2025.
- **Evidence:** Transcription quality evaluated against MAESTRO; widely used as a large classical-piano pretraining corpus.
- **Why it matters for the studio:** Permissive-licence expressive piano data (the founder's instrument family) for pretraining.
- **Tags:** [dataset] [transcription] [expression-performance]
- **Verification:** verified
- **BibKey:** kong2020giantmidi

### ATEPP — Automatically Transcribed Expressive Piano Performance
- **Who/where/when:** Huan Zhang, Jingjing Tang, Syed Rifat Mahmud Rafee, Simon Dixon, George Fazekas; QMUL; ISMIR 2022; v1.2
- **Links:** https://github.com/tangjjbetsy/ATEPP
- **What it is:** 11,674 performances (~1,000 h) by 49 virtuoso pianists covering 1,595 movements by 25 composers, transcribed from commercial recordings; ~43% have aligned MusicXML scores; Composition Entity Linker for metadata. CC-BY 4.0.
- **Evidence:** Designed for performer-identification and expressive-rendering studies (multiple performances per piece).
- **Why it matters for the studio:** Multiple interpretations of the same score = training signal for "render this passage *like this*" expression controls.
- **Tags:** [dataset] [expression-performance] [transcription]
- **Verification:** verified
- **BibKey:** zhang2022atepp

### Aria-MIDI — 1.19M transcribed solo-piano MIDI files (100k hours)
- **Who/where/when:** Louis Bradshaw, Simon Colton; Queen Mary University of London / EleutherAI; ICLR 2025
- **Links:** https://arxiv.org/abs/2504.15071 ; https://github.com/loubbrad/aria-midi ; HF `loubb/aria-midi`
- **What it is:** 1,186,253 MIDI files (~100,629 h) transcribed from YouTube solo-piano recordings with Aria-AMT (seq2seq transcription) after filtering with Aria-CL (solo-piano classifier); metadata: composer/genre/performer identifiers, audio-quality scores; variants full/pruned/deduped/unique (32,522–1.19M files). License CC-BY-NC-SA 4.0 with click-through disclaimer. Companion model: Aria (EleutherAI, ISMIR 2025, "Scaling Self-Supervised Representation Learning for Symbolic Piano Performance").
- **Evidence:** ~500× MAESTRO's hours; largest expressive symbolic corpus to date.
- **Why it matters for the studio:** The scale needed for foundation-model-style symbolic pretraining; NC license and YouTube provenance are the trade-offs.
- **Tags:** [dataset] [transcription] [expression-performance] [ethics-legal]
- **Verification:** verified
- **BibKey:** bradshaw2025ariamidi

### PDMX — Public Domain MusicXML dataset (>250k scores)
- **Who/where/when:** Phillip Long, Zachary Novack, Taylor Berg-Kirkpatrick, Julian McAuley; UC San Diego; ICASSP 2025 (arXiv Sept 2024)
- **Links:** https://arxiv.org/abs/2409.10831 ; https://github.com/pnlong/PDMX ; Zenodo 13763756
- **What it is:** >250,000 MusicXML scores collected from MuseScore.com restricted to works marked public domain, with user ratings, genre tags, and annotations enabling quality filtering; CC-BY 4.0; released with MusicRender (a MusPy extension handling MusicXML expressive markings). Experiments show rating-based subsets improve multitrack generation.
- **Evidence:** Authors call it "the largest available copyright-free symbolic music dataset."
- **Why it matters for the studio:** The cleanest large notation-level (not MIDI-level) corpus — includes dynamics, articulations, lyrics — i.e., exactly the representation a notation-first studio manipulates.
- **Tags:** [dataset] [notation] [ethics-legal]
- **Verification:** verified
- **BibKey:** long2024pdmx

### Hooktheory / TheoryTab dataset (via Sheet Sage) — aligned melody + harmony annotations
- **Who/where/when:** Chris Donahue, John Thickstun, Percy Liang; Stanford; ISMIR 2022 ("Melody transcription via generative pre-training")
- **Links:** https://github.com/chrisdonahue/sheetsage ; https://arxiv.org/abs/2212.01884
- **What it is:** ~50 hours of crowd-sourced TheoryTab segments (melody as scale degrees + Roman-numeral/functional harmony, key, meter) aligned to YouTube audio, JSON (20 MB) with 80/10/10 splits; test set as MIDI. License CC-BY-NC-SA 3.0. Sheet Sage itself transcribes pop audio to lead sheets (PDF/MIDI) using Jukebox features.
- **Evidence:** Jukebox features improved melody-transcription F1 substantially over spectrogram baselines (paper). TheoryTab overall >50k analyses powers Hookpad Aria (see above).
- **Why it matters for the studio:** The only sizeable *functional-harmony-annotated pop* corpus with audio alignment; NC-licensed.
- **Tags:** [dataset] [theory-analysis] [transcription] [ethics-legal]
- **Verification:** verified
- **BibKey:** donahue2022sheetsage

### Chordonomicon — 666,000 songs' chord progressions
- **Who/where/when:** Spyridon Kantarelis, Konstantinos Thomas, Vassilis Lyberatos, Edmund Dervakos, Giorgos Stamou; NTUA Athens; arXiv Oct 2024 (v3 Dec 2024)
- **Links:** https://arxiv.org/abs/2410.22046 ; HF `ailsntua/Chordonomicon`
- **What it is:** >666k user-generated chord sequences scraped from guitar-tab sites, with section labels (verse/chorus…), genre, release year, Spotify IDs, and harmonic-function tags; provided as text and graph representations. Paper CC-BY 4.0; dataset license per repo (partial).
- **Evidence:** Demonstrated genre classification and progression generation baselines.
- **Why it matters for the studio:** Chord-level structural priors for pop songwriting (David Foster-style harmonic vocabulary) at a scale no MIDI corpus offers.
- **Tags:** [dataset] [theory-analysis] [structure]
- **Verification:** verified
- **BibKey:** kantarelis2024chordonomicon

### MetaMIDI Dataset (MMD) — 436,631 MIDI files with audio/metadata matches
- **Who/where/when:** Jeff Ens, Philippe Pasquier; Simon Fraser University; ISMIR 2021
- **Links:** https://github.com/jeffreyjohnens/MetaMIDIDataset ; Zenodo (registration)
- **What it is:** 436,631 MIDIs; scraped artist/title for 221,504; 10.7M audio–MIDI matches linking 237,236 MIDIs to Spotify tracks (829,728 high-reliability); 168,032 with MusicBrainz IDs; genre for 143,868. Access requires registration, affiliation, and a no-redistribution agreement.
- **Evidence:** Underlies MMM (Multi-Track Music Machine) training.
- **Why it matters for the studio:** Larger and better-labelled than Lakh, but its terms preclude bundling; useful for research-only pretraining.
- **Tags:** [dataset] [ethics-legal]
- **Verification:** verified
- **BibKey:** ens2021metamidi

### Los Angeles MIDI Dataset — ~405k deduplicated MIDIs
- **Who/where/when:** Aleksandr Lev (asigalov61, "Project Los Angeles"); v4.0 2024
- **Links:** https://github.com/asigalov61/Los-Angeles-MIDI-Dataset ; HF `projectlosangeles/Los-Angeles-MIDI-Dataset`
- **What it is:** ~405,000 "read-checked, 100% de-duped" MIDI files aggregated from public sources, with metadata and per-file chord data plus search utilities; repo Apache-2.0 (underlying files' provenance unstated).
- **Evidence:** Community dataset behind the author's many "Tegridy" MIDI models; no peer-reviewed paper.
- **Why it matters for the studio:** Quick, large, permissively-labelled multitrack data — but provenance is weaker than PDMX/Lakh; treat as research-only.
- **Tags:** [dataset] [ethics-legal]
- **Verification:** verified (repo)
- **BibKey:** lev2024lamidi

### JSB Chorales, Nottingham, POP909, Wikifonia — classic small symbolic sets
- **Who/where/when:** JSB Chorales: 382 four-part Bach chorales (Boulanger-Lewandowski, Bengio, Vincent ICML 2012 splits; music21 corpus has 371+); Nottingham: ~1,200 British/American folk tunes with chords in ABC (Eric Foxley; Boulanger-Lewandowski 2012 MIDI version); POP909: 909 Chinese pop songs, piano arrangements (melody/bridge/piano tracks) + chord/beat/key annotations, ~60 h (Ziyu Wang, Ke Chen, Junyan Jiang et al., NYU Shanghai, ISMIR 2020); Wikifonia: ~6,000 lead sheets in MusicXML (site closed 2013 after publisher pressure; still circulates in research, not legally redistributable)
- **Links:** https://github.com/music-x-lab/POP909-Dataset ; https://abc.sourceforge.net/NMD/ ; music21 corpus
- **What it is:** The standard "toy-to-medium" corpora for harmonisation (JSB), melody+chord modelling (Nottingham, Wikifonia), and pop arrangement/accompaniment (POP909). POP909 license: research/non-commercial (partial).
- **Evidence:** JSB remains the canonical benchmark for voice-leading/harmonisation models (DeepBach, Coconet).
- **Why it matters for the studio:** Fast evaluation beds for harmonisation and lead-sheet→arrangement tasks; POP909's melody/accompaniment split is a direct analogue of "compile a piano part from a lead sheet."
- **Tags:** [dataset] [corpus] [accompaniment]
- **Verification:** partial (recalled)
- **BibKey:** wang2020pop909

### OpenScore Lieder & OpenScore String Quartets — CC0 critical-quality encodings
- **Who/where/when:** Mark Gotham, Peter Jonas (OpenScore / MuseScore); MEC 2021 (proc. 2022) "The OpenScore Lieder Corpus"; String Quartets corpus (Gotham et al., 2023)
- **Links:** https://github.com/OpenScore/Lieder ; https://github.com/OpenScore/StringQuartets ; https://musescore.com/openscore-lieder-corpus
- **What it is:** Lieder: 1,200+ 19th-century songs by 100+ composers, crowd-transcribed and professionally proofread, in MuseScore .mscx (batch-convertible to MusicXML/MIDI/PDF/MP3) with composers/scores/sets TSV metadata; CC0. String Quartets: ~100 movements from the classical/romantic repertoire (partial), same pipeline.
- **Evidence:** Best Poster, MEC 2021; used by When-in-Rome analyses and DCML.
- **Why it matters for the studio:** Public-domain, notation-level, *proofread* scores — ideal both for training and as the demo repertoire for annotation tools.
- **Tags:** [corpus] [dataset] [notation]
- **Verification:** verified (Lieder); Quartets partial
- **BibKey:** gotham2022openscore

### When in Rome — meta-corpus of Roman numeral analyses (RomanText)
- **Who/where/when:** Mark Gotham, Dmitri Tymoczko, Michael Scott Cuthbert et al.; TU Dortmund / Princeton / MIT; ISMIR 2019 (RomanText), ongoing
- **Links:** https://github.com/MarkGotham/When-in-Rome
- **What it is:** ~2,000 analyses of ~1,500 works encoded in RomanText (.rntxt; parsed by music21), aligned to scores (mxl or remote links): Bach chorales (371) & preludes, Beethoven quartets (16) & sonata first movements (32) & variations, Mozart sonatas (18) & variations, Chopin mazurkas (56), Haydn Op. 20, Schubert cycles, Monteverdi madrigals (48), textbook modulation examples. New content CC-BY-SA 4.0; converted analyses keep source licences.
- **Evidence:** The largest open training/eval set for symbolic Roman-numeral analysis (used by AugmentedNet, RNBert).
- **Why it matters for the studio:** RomanText is a compact *textual annotation format* for harmony that humans write and machines parse — a candidate for the studio's harmony-annotation layer.
- **Tags:** [corpus] [theory-analysis] [annotation] [representation]
- **Verification:** verified
- **BibKey:** gotham2019wheninrome

### DCML corpora — Distant Listening Corpus and the DCML harmony standard
- **Who/where/when:** Johannes Hentschel, Markus Neuwirth, Martin Rohrmeier et al.; EPFL Digital and Cognitive Musicology Lab; ABC (Annotated Beethoven Corpus) 2018 (Frontiers), Annotated Mozart Sonatas 2021 (TISMIR), Distant Listening Corpus 2025
- **Links:** https://github.com/DCMLab/dcml_corpora ; https://github.com/DCMLab/ABC ; https://github.com/DCMLab/mozart_piano_sonatas
- **What it is:** Expert Roman-numeral annotations (DCML standard: chord, inversion, applied chords, phrase and cadence labels) entered directly in MuseScore .mscx files and extracted to TSV (notes, measures, harmonies) with the `ms3` parser; 12 public sub-corpora (Beethoven quartets and sonatas, Mozart sonatas, Chopin mazurkas, Corelli, Debussy, Dvořák, Grieg, Liszt, Medtner, Schumann, Tchaikovsky). Licence CC-BY-NC-SA 4.0 (partial).
- **Evidence:** Multi-annotator review workflow; the basis of numerous corpus-study papers.
- **Why it matters for the studio:** Exemplar of annotations *living inside the score file* (harmony labels as staff text) — the same pattern the studio needs for human+AI annotations.
- **Tags:** [corpus] [theory-analysis] [annotation]
- **Verification:** verified (repo); licence/paper partial
- **BibKey:** hentschel2021mozart

### Bach Doodle Dataset — 21.6M user melodies + Coconet harmonisations
- **Who/where/when:** Cheng-Zhi Anna Huang, Curtis Hawthorne, Adam Roberts et al.; Google Magenta; ISMIR 2019 ("The Bach Doodle: Approachable music composition with machine learning at scale")
- **Links:** https://magenta.tensorflow.org/datasets/bach-doodle
- **What it is:** 21.6 million two-bar user melodies with Coconet four-voice harmonisations, plus country, rating (poor/neutral/good), composition time, key, playbacks, backend (TPU vs TF.js). CC-BY 4.0.
- **Evidence:** ~8.5M sessions, >50M harmonisation requests — the largest HCI log of a co-creative music tool.
- **Why it matters for the studio:** Both a dataset of amateur melodic input and evidence about mass-scale mixed-initiative harmonisation UX.
- **Tags:** [dataset] [co-creation-framework] [education] [HCI-study]
- **Verification:** verified
- **BibKey:** huang2019bachdoodle

### MidiCaps — 168k MIDI files with text captions
- **Who/where/when:** Jan Melechovsky, Abhinaba Roy, Dorien Herremans; SUTD Singapore; ISMIR 2024
- **Links:** https://arxiv.org/abs/2406.02255 ; HF `amaai-lab/MidiCaps`
- **What it is:** >168,000 Lakh-derived MIDI files each with an LLM-generated caption built from extracted features (tempo, chords, time signature, instruments, genre, mood); listening study validated caption quality. Licence CC-BY-SA 4.0 (partial). Follow-ups: Text2midi (2024), symbolic captioning work 2025.
- **Evidence:** "First openly available large-scale MIDI dataset with text captions."
- **Why it matters for the studio:** Enables text annotations ↔ symbolic mapping (e.g., "make the bridge darker") for training or retrieval.
- **Tags:** [dataset] [text-conditioning] [annotation]
- **Verification:** verified (abstract); licence partial
- **BibKey:** melechovsky2024midicaps

### Audio stems & captions — MusicNet, Slakh2100, MedleyDB, MUSDB18, MusicCaps, Song Describer
- **Who/where/when:** MusicNet (John Thickstun, Zaid Harchaoui, Sham Kakade; ICLR 2017; 330 classical recordings, 34 h, >1M note labels; CC-BY 4.0); Slakh2100 (Ethan Manilow, Gordon Wichern, Prem Seetharaman, Jonathan Le Roux; MERL; WASPAA 2019; 2,100 Lakh MIDIs rendered with pro sample libraries, 145 h of stems; CC-BY 4.0); MedleyDB 1.0/2.0 (Rachel Bittner et al., NYU; ISMIR 2014; 122+74 multitracks; CC-BY-NC-SA); MUSDB18 / MUSDB18-HQ (Zafar Rafii et al., 2017; 150 songs ~10 h, 4 stems; mixed licences, some tracks restricted); MusicCaps (Andrea Agostinelli et al., Google, 2023; 5,521 ten-second AudioSet clips with expert captions; CC-BY-SA 4.0); Song Describer (Ilaria Manco, Benno Weck et al.; NeurIPS 2023 ML4Audio; ~1.1k captions for 706 CC-licensed tracks; CC-BY)
- **Links:** https://zenodo.org/record/5120004 (MusicNet) ; http://www.slakh.com ; https://medleydb.weebly.com ; https://sigsep.github.io/datasets/musdb.html ; https://www.kaggle.com/datasets/googleai/musiccaps ; https://github.com/mulab-mir/song-describer-dataset
- **What it is:** The audio-side complements: MusicNet and Slakh give note-aligned audio (Slakh synthetic but multitrack with MIDI ground truth — the ideal "render a compile" testbed); MedleyDB/MUSDB18 are separation benchmarks; MusicCaps/Song Describer are the text-audio evaluation sets used by every text-to-music model.
- **Evidence:** All are standard benchmarks in their tasks.
- **Why it matters for the studio:** Slakh2100 is uniquely useful: symbolic multitrack ↔ stems pairs for training arrangement-rendering and for evaluating symbolic "compiles" by audio similarity.
- **Tags:** [dataset] [transcription] [audio-generation] [evaluation]
- **Verification:** partial (recalled)
- **BibKey:** manilow2019slakh

### MuseScore.com scraping — the "musescore-dataset" and its ethics
- **Who/where/when:** Xmader (GitHub), 2020–Sept 2021 (unmaintained); contrasted with PDMX (2024)
- **Links:** https://github.com/Xmader/musescore-dataset
- **What it is:** Unofficial dump of MuseScore.com score metadata, user data and MSCZ files via the site's public API, distributed over IPFS explicitly so that "no one can take it down"; no licence, "at your own risk" warnings. Most scores on musescore.com are user arrangements of copyrighted works; Muse Group's ToS forbids bulk download. Several 2022–2024 symbolic-model papers trained on such dumps without disclosure of terms.
- **Evidence:** Repo status confirmed; PDMX authors explicitly cite copyright concerns as motivation and filter to public-domain scores.
- **Why it matters for the studio:** A research-grade open studio should adopt PDMX-style provenance discipline (public domain / CC-only, per-file licence metadata) — both ethically and to keep the door open to commercial adoption.
- **Tags:** [ethics-legal] [dataset]
- **Verification:** verified
- **BibKey:** xmader2021musescore

---

## C. Computational music theory & analysis

### AugmentedNet — Roman numeral analysis network with synthetic training examples
- **Who/where/when:** Néstor Nápoles López, Mark Gotham, Ichiro Fujinaga; McGill / Cornell; ISMIR 2021; v1.9.1 (2022 dissertation)
- **Links:** https://github.com/napulen/AugmentedNet ; ISMIR 2021 paper
- **What it is:** CRNN reading MusicXML (pitch-spelling-aware encoding) and predicting 11 tonal tasks jointly (key, degree, quality, inversion, root, harmonic rhythm, pitch-class sets…) then assembling Roman numerals; trained on aggregated corpora (BPS, When-in-Rome, Haydn Sun quartets, ABC, TAVERN, WTC) plus synthetic texturisation. Outputs annotated MusicXML + CSV; MIT.
- **Evidence:** Best config: 82.9% key, 67.0% scale degree, 46.4% full Roman numeral on the held-out test sets. Adopted in Sibelius (harmonic analysis), Vimu.app, MusicLang.
- **Why it matters for the studio:** A deployable "auto-annotate harmony" backend whose confidence is low enough that the human-in-the-loop correction step is essential — perfectly matching the annotate→edit loop.
- **Tags:** [theory-analysis] [annotation] [toolkit]
- **Verification:** verified
- **BibKey:** napoleslopez2021augmentednet

### ChordGNN — Roman Numeral Analysis with Graph Neural Networks (onset-wise from note-wise)
- **Who/where/when:** Emmanouil Karystinaios, Gerhard Widmer; JKU Linz; ISMIR 2023
- **Links:** https://arxiv.org/abs/2307.03544 ; https://github.com/manoskary/chordgnn
- **What it is:** Represents the score as a note graph (partitura), runs a GNN over notes, then a learned edge-contraction pools note-wise features to onset-wise predictions of Roman numeral components; variants with NADE and post-processing.
- **Evidence:** Reported higher accuracy than AugmentedNet on the same reference datasets (exact deltas not re-fetched). Related JKU work: cadence detection with GNNs (ISMIR 2022), voice separation (2023).
- **Why it matters for the studio:** Shows note-level graph representations (not piano-roll) as the right substrate for analysis — the same structure a notation editor already holds.
- **Tags:** [theory-analysis] [representation]
- **Verification:** verified
- **BibKey:** karystinaios2023chordgnn

### RNBert — Fine-tuning a masked language model for Roman numeral analysis
- **Who/where/when:** Malcolm Sailor; Yale; ISMIR 2024 (Zenodo DOI 10.5281/zenodo.14877455)
- **Links:** https://github.com/malcolmsailor/rnbert
- **What it is:** Takes MusicBERT (Zeng et al. 2021, OctupleMIDI) pretrained on large unlabeled symbolic data and fine-tunes it (with layer freezing) for key prediction and key-conditioned Roman-numeral prediction on When-in-Rome-style data; compares against AugmentedNet/ChordGNN.
- **Evidence:** Reports state-of-the-art on the Roman numeral task via transfer from unlabeled pretraining (numbers not re-fetched).
- **Why it matters for the studio:** Demonstrates the pretrain-then-analyse recipe: one symbolic foundation model can serve both generation and annotation heads.
- **Tags:** [theory-analysis] [representation]
- **Verification:** verified (repo)
- **BibKey:** sailor2024rnbert

### Chen & Su — Functional harmony recognition and "Attend to Chords" (Harmony Transformer)
- **Who/where/when:** Tsung-Ping Chen, Li Su; Academia Sinica, Taipei; ISMIR 2018 ("Functional harmony recognition of symbolic music data with multi-task recurrent neural networks"), ISMIR 2019 (Harmony Transformer), TISMIR 2021 ("Attend to Chords…", DOI 10.5334/tismir.65)
- **Links:** https://doi.org/10.5334/tismir.65
- **What it is:** Multi-task RNN then Transformer encoder-decoder that jointly segments chord regions and labels key/Roman numerals from symbolic (BPS-FH) or audio input; introduced the Beethoven Piano Sonata Functional Harmony (BPS-FH) dataset.
- **Evidence:** TISMIR paper shows Transformer-based models outperform RNN baselines on chord symbol and Roman-numeral recognition on BPS-FH.
- **Why it matters for the studio:** Established the segmentation+labelling framing of functional harmony analysis that later models adopt.
- **Tags:** [theory-analysis]
- **Verification:** verified (Crossref record)
- **BibKey:** chen2021attend

### Computational Schenkerian analysis — new dataset, notation software, graph representation
- **Who/where/when:** Stephen Ni-Hahn, Weihan Xu, Jerry Yin, Rico Zhu, Simon Mak, Yue Jiang, Cynthia Rudin; Duke University; ISMIR 2024 (arXiv 2408.07184). Anchored by Phillip Kirlin & David Jensen (ISMIR 2011 / JNMR 2015 probabilistic MOP models, 41 analyses)
- **Links:** https://arxiv.org/abs/2408.07184
- **What it is:** Largest machine-readable Schenkerian analysis dataset (>140 excerpts vs 41 previously), custom notation software for entering/visualising reductions, and a heterogeneous-graph representation framing analysis as hierarchical graph clustering (allowing multiple voices and complex harmonic relations, beyond Kirlin's maximal outerplanar graphs).
- **Evidence:** Dataset and software released; baseline models reported.
- **Why it matters for the studio:** Hierarchical reduction is the theory-side counterpart of the founder's "compile" (surface ← deep structure); this is the only open dataset/tooling for it.
- **Tags:** [theory-analysis] [dataset] [structure] [notation]
- **Verification:** verified
- **BibKey:** nihahn2024schenker

### Galant schema detection — computational Gjerdingen schemata
- **Who/where/when:** Christoph Finkensiep, Markus Neuwirth, Martin Rohrmeier (EPFL; ISMIR 2018 "Generalized Skipgrams for Pattern Discovery in Polyphonic Streams"); Andreas Katsiavalos, Tom Collins, Bret Battey (ISMIR 2019, "An initial computational model for musical schemata theory"); James Symons (Music Theory Spectrum 2017, "Temporal regularity as a key to uncovering statistically significant schemas in an eighteenth-century corpus")
- **Links:** (ISMIR archive PDFs; not re-fetched)
- **What it is:** Pattern-discovery and matching approaches to identify Gjerdingen's voice-leading schemata (Prinner, Romanesca, Fonte, Monte…) in encoded scores; Finkensiep et al. use skipgrams over polyphonic note streams with a hand-annotated schema dataset; Katsiavalos et al. build a prototype-matching model.
- **Evidence:** Small annotated sets; precision/recall modest — schema detection remains open.
- **Why it matters for the studio:** Schemata are the "idioms/design patterns" of a style — a natural annotation vocabulary for style-aware compile hints (cf. arranger styles).
- **Tags:** [theory-analysis] [style-transfer]
- **Verification:** unverified (recall; could not fetch ISMIR archive)
- **BibKey:** finkensiep2018skipgrams

### MSAF — Music Structure Analysis Framework
- **Who/where/when:** Oriol Nieto, Juan Pablo Bello; NYU; ISMIR 2016 ("Systematic exploration of computational music structure research"); v0.1.80 June 2023
- **Links:** https://github.com/urinieto/msaf
- **What it is:** MIT Python framework bundling boundary algorithms (Foote, Structural Features, C-NMF, OLDA, Spectral Clustering, VMO) and labelling algorithms with mir_eval evaluation on SALAMI/Beatles/Isophonics, from audio features.
- **Evidence:** The reference comparison harness for classical structure methods.
- **Why it matters for the studio:** Baseline section segmentation for reference audio the composer drops in as an annotation.
- **Tags:** [structure] [toolkit] [evaluation]
- **Verification:** verified
- **BibKey:** nieto2016msaf

### All-In-One — metrical and functional structure analysis on demixed audio
- **Who/where/when:** Taejun Kim, Juhan Nam; KAIST; WASPAA 2023 (arXiv 2307.16425); pip `allin1`
- **Links:** https://arxiv.org/abs/2307.16425 ; https://github.com/mir-aidj/all-in-one
- **What it is:** Single model on source-separated spectrograms jointly predicting beats, downbeats, section boundaries and functional labels (intro/verse/chorus/bridge/outro) using dilated neighbourhood attention; ablations show tasks mutually improve.
- **Evidence:** State of the art on Harmonix Set across all four tasks with fewer parameters than prior models.
- **Why it matters for the studio:** One call gives the structural skeleton of a reference track — the scaffold onto which a "compile" can map sections.
- **Tags:** [structure] [transcription]
- **Verification:** verified
- **BibKey:** kim2023allinone

### Dai & Dannenberg — hierarchical structure, repetition and personalised pop generation
- **Who/where/when:** Shuqi Dai, Huiran Yu / Huan Zhang, Roger B. Dannenberg; Carnegie Mellon University; ISMIR 2022 ("What is missing in deep music generation? A study of repetition and structure in popular music"), JNMR 2023 ("Personalised popular music generation using imitation and structure"), plus earlier "Automatic analysis and influence of hierarchical structure on melody, rhythm and harmony in popular music" (CSMC+MuMe 2020)
- **Links:** https://www.cs.cmu.edu/~rbd/papers/ (PDFs repetition-ismir2022, pop-imitation-arxiv-jnmr-2023)
- **What it is:** Symbolic analysis of pop songs (POP909) at multiple levels — repetition patterns, phrase structure, melody/rhythm/harmony hierarchy — showing deep generators lack long-range repetition; a structure-first generation pipeline that imitates a seed song's structure with controllable melody/harmony/rhythm.
- **Evidence:** Quantitative repetition statistics on POP909 vs. generated music; listening tests for the imitation system (details not re-fetched).
- **Why it matters for the studio:** Argues for explicit structural annotation (sections, repetition relations) as a first-class input to generation — exactly what the annotate step should capture. (Cross-ref: Dannenberg belongs to accompaniment/HCI clusters too.)
- **Tags:** [structure] [theory-analysis] [symbolic-generation] [controllability]
- **Verification:** partial (PDF listing fetched; contents recalled)
- **BibKey:** dai2022repetition

### Key/chord estimation and phrase segmentation — the standard baselines
- **Who/where/when:** Chord/key from audio: madmom (Böck et al., 2016), Korzeniowski & Widmer (ISMIR 2016/2018 CNN chord & key), Essentia/Chordino (Mauch & Dixon 2010); symbolic key: Krumhansl–Schmuckler / Temperley (music21 `analyze('key')`); melodic phrase segmentation: Cambouropoulos LBDM (2001), Pearce et al. IDyOM (2010), Guan et al. "Melodic phrase segmentation by deep neural networks" (2018); lead-sheet harmonic function labelling: Chen & Su, Hooktheory data, and "functional" chord labels in Chordonomicon
- **Links:** https://github.com/CPJKU/madmom ; https://github.com/mtg/essentia
- **What it is:** Mature, mostly pre-transformer components that still power practical systems (Chordify, Moises chord detection). Symbolic phrase segmentation lacks a large shared benchmark (Essen folk phrase marks are the usual one).
- **Evidence:** MIREX chord estimation plateaued ~80–85% MajMin accuracy by 2019.
- **Why it matters for the studio:** Off-the-shelf pieces for turning hummed/recorded input into chords and phrases before symbolic editing.
- **Tags:** [theory-analysis] [transcription] [toolkit]
- **Verification:** partial (recalled)
- **BibKey:** bock2016madmom

### Counterpoint / voice-leading rule checkers
- **Who/where/when:** music21 `voiceLeading` module (VoiceLeadingQuartet: parallel fifths/octaves, hidden intervals, voice crossing — Cuthbert lab); Palestrina Pal (Jonathan Huang & Elaine Chew, 2005); species-counterpoint solvers/checkers in Strasheela (Anders & Miranda), and LLM-era checkers used as reward functions (e.g., rule-based critics in 2024–25 RL fine-tuning of Bach-style generators)
- **Links:** https://music21.org/music21docs/moduleReference/moduleVoiceLeading.html
- **What it is:** Deterministic rule engines that flag voice-leading errors in SATB/species exercises; used pedagogically and as constraints/rewards for generation.
- **Evidence:** No large comparative benchmark; rule sets vary by textbook.
- **Why it matters for the studio:** Cheap, explainable "linters" for the compile output — the software-engineering analogy the founder will appreciate (compiler warnings for parallel fifths).
- **Tags:** [theory-analysis] [education] [toolkit]
- **Verification:** partial (music21 module recalled; others unverified)
- **BibKey:** huang2005palestrinapal

### ChatMusician & MusicTheoryBench — LLMs with ABC notation, and how little theory they know
- **Who/where/when:** Ruibin Yuan, Hanfeng Lin, Yi Wang et al. (Multimodal Art Projection / HKUST / Skywork); ACL 2024 Findings (arXiv 2402.16153)
- **Links:** https://arxiv.org/abs/2402.16153 ; https://github.com/hf-lin/ChatMusician
- **What it is:** LLaMA-2-7B continually pretrained/fine-tuned on MusicPile (4B tokens of ABC notation + music text) to compose and analyse in ABC as "a second language"; releases MusicTheoryBench (college-level theory knowledge and reasoning MCQs). Weights, data, and code open.
- **Evidence:** ChatMusician beats LLaMA-2 and GPT-3.5 zero-shot on MusicTheoryBench; GPT-4 reasoning accuracy reported near random on the reasoning split (recalled; not re-fetched).
- **Why it matters for the studio:** ABC-native LLMs are the practical bridge between text annotations and symbolic edits; the benchmark warns that LLM "theory" must be checked by symbolic analysers.
- **Tags:** [LLM-agent] [symbolic-generation] [theory-analysis] [evaluation]
- **Verification:** verified (abstract); scores partial
- **BibKey:** yuan2024chatmusician

### MuChoMusic — evaluating music understanding in audio-language models
- **Who/where/when:** Benno Weck, Ilaria Manco, Emmanouil Benetos, Elio Quinton, George Fazekas, Dmitry Bogdanov; UPF / QMUL / UMG; ISMIR 2024 (arXiv 2408.01337)
- **Links:** https://arxiv.org/abs/2408.01337 ; https://github.com/mulab-mir/muchomusic
- **What it is:** 1,187 human-validated multiple-choice questions on 644 tracks (from MusicCaps and Song Describer) covering knowledge (theory, instrumentation) and reasoning (cultural/functional context); evaluates five open audio-language models.
- **Evidence:** Models over-rely on the language modality; audio grounding weak. Related: ZIQI-Eval (ACL 2024 Findings) for text-only music knowledge.
- **Why it matters for the studio:** Sets expectations for multimodal LLM "listeners" that would interpret audio annotations — they currently hear less than they claim.
- **Tags:** [evaluation] [LLM-agent] [multimodal-input]
- **Verification:** verified
- **BibKey:** weck2024muchomusic

---

## D. Education & games

### MIT 21M.385 / 6.809 Interactive Music Systems (Egozy) — and 21M.383 (cross-ref)
- **Who/where/when:** Eran Egozy (Harmonix co-founder; MIT Music & Theater Arts / EECS); offered since ~2014; OCW Fall 2016. 21M.383 Computational Music Theory & Analysis (Cuthbert) is covered by another agent.
- **Links:** https://ocw.mit.edu/courses/21m-385-interactive-music-systems-fall-2016/ ; https://musictech.mit.edu/ims
- **What it is:** Studio course where students build interactive music systems in **Python with Kivy** (Egozy's `imslib`/common library: real-time audio synthesis and looping via FluidSynth, MIDI sequencing, generative composition, motion/gesture sensors, music-game design, GUI/visualisation); weekly programming assignments and a team final project; Guitar Hero is used as a case study of interactive systems' cultural reach.
- **Evidence:** Course site archives dozens of student games/instruments per year.
- **Why it matters for the studio:** A proven curriculum for teaching composers to build musical software — and a pipeline of collaborators; its architecture (Python + real-time audio + notation-free interaction) contrasts with the studio's notation-first stance.
- **Tags:** [education] [game] [real-time] [music-as-code]
- **Verification:** verified
- **BibKey:** egozy2016ims

### Egozy — Approaches to Musical Expression in Harmonix Video Games; live score following; AI-augmented instruments
- **Who/where/when:** Eran Egozy; IMS NUS Lecture Notes 2016 (DOI 10.1142/9789813140103_0002); Matthew Caren & Eran Egozy, JAES 2025 ("Real-Time In-Browser Time Warping for Live Score Following"); Lancelot Blanchard, Perry Naseck, Egozy, Joseph Paradiso, 2024 ("Developing Symbiotic Virtuosity: AI-Augmented Musical Instruments…")
- **Links:** https://doi.org/10.1142/9789813140103_0002 ; https://doi.org/10.17743/jaes.2022.0244
- **What it is:** Egozy's account of how Guitar Hero/Rock Band/Dance Central/Fuser designed for *musical expression* within game constraints (scoring, freestyle sections, note-highway abstraction); recent MIT work on browser-based real-time score following (online time warping) and on AI-augmented instruments in live performance (with the Media Lab).
- **Evidence:** Descriptive/design papers; the JAES paper reports latency/accuracy of in-browser alignment (numbers not fetched).
- **Why it matters for the studio:** Direct lineage from game interfaces to expressive control; in-browser score following is a component for aligning the composer's live playing/singing to notation as an annotation.
- **Tags:** [game] [HCI-study] [real-time] [education]
- **Verification:** verified (Crossref records)
- **BibKey:** egozy2016harmonix

### Kiri Miller — Guitar Hero/Rock Band as musical performance and learning
- **Who/where/when:** Kiri Miller; Brown University; JSAM 2009 ("Schizophonic Performance: Guitar Hero, Rock Band, and Virtual Virtuosity"); book *Playing Along: Digital Games, YouTube, and Virtual Performance* (Oxford 2012, ch. "How Musical Is Guitar Hero?")
- **Links:** https://doi.org/10.1017/s1752196309990666 ; https://doi.org/10.1093/acprof:oso/9780199753451.003.0003
- **What it is:** Ethnographic study (interviews, surveys of players) arguing these games are a form of musical performance and informal music learning (rhythm, structure, listening), while analysing their limits; later pedagogical literature (e.g., "Musical Representation in Guitar Hero and Rock Band," 2010) and Harmonix's *Rock Band* in-classroom pilots build on this.
- **Evidence:** Qualitative; the canonical reference for game-based music learning.
- **Why it matters for the studio:** Grounds the claim that game-like interfaces can carry genuine musical agency — relevant if the studio uses playful, game-derived interaction for annotation (e.g., tapping rhythms, "note highway" input).
- **Tags:** [game] [education] [HCI-study]
- **Verification:** verified (Crossref)
- **BibKey:** miller2009schizophonic

### Harmonix Fuser / DropMix — mashup games as arrangement interfaces
- **Who/where/when:** Harmonix (Boston; acquired by Epic Games 2021); DropMix (with Hasbro, 2017: physical NFC cards + app mixing stems in-key/in-tempo); Fuser (2020: real-time 4-slot stem mashups, key/tempo matching, live-DJ campaign; servers shut down Dec 2022)
- **Links:** https://en.wikipedia.org/wiki/Fuser_(video_game) ; https://en.wikipedia.org/wiki/DropMix
- **What it is:** Consumer products that made *arrangement by stem selection* a game mechanic: pick vocals/bass/drums/lead from different licensed songs, engine time-stretches/pitch-shifts to a common key and tempo, with scoring for musical timing (drops on downbeats).
- **Evidence:** Commercial; critically praised for accessibility of musical mixing.
- **Why it matters for the studio:** Demonstrates casual users can make coherent arrangements from constrained stems when the system handles key/tempo — a UX lesson for the "compile" step.
- **Tags:** [game] [product] [accompaniment]
- **Verification:** partial (recalled)
- **BibKey:** harmonix2020fuser

### TunePad — Python + music for CS learning (Northwestern TIDAL Lab)
- **Who/where/when:** Michael Horn, Nichole Pinkard, Amartya Banerjee, Matthew Brucker, Jamie Gorson et al.; Northwestern University with Georgia Tech (EarSketch team); IDC 2017 demo; CHI 2022 ("TunePad Playbooks", DOI 10.1145/3491102.3502021); NSF DRL-1612619/1451762/1837661
- **Links:** https://tunepad.com ; https://doi.org/10.1145/3491102.3502021
- **What it is:** Free browser platform where learners write Python (`playNote`, `rest`, loops, functions) in notebook-like cells to produce beats, basslines, chords and melodies with real-time playback; Playbooks are tutorial+code documents; classroom research with teens in Chicago.
- **Evidence:** CHI 2022 reports design and deployment findings; multiple studies of engagement/computational-thinking gains (details not fetched).
- **Why it matters for the studio:** The clearest existing realisation of "music as code that compiles to sound," including cell/notebook UI ideas for a composition-as-program editor.
- **Tags:** [education] [music-as-code] [HCI-study]
- **Verification:** verified (Crossref + site)
- **BibKey:** horn2022tunepad

### EarSketch — coding + music remixing for broadening participation (Georgia Tech)
- **Who/where/when:** Jason Freeman, Brian Magerko, Doug Edwards, Roxanne Moore et al.; Georgia Tech; Organised Sound 2013; SIGCSE 2014–2017; CACM 2019 ("EarSketch: engaging broad populations in computing through music", DOI 10.1145/3333613)
- **Links:** https://earsketch.gatech.edu ; https://doi.org/10.1145/3333613
- **What it is:** Browser DAW-like environment where students write Python or JavaScript to place licensed loop samples on tracks, apply effects and algorithmic structure (`fitMedia`, `makeBeat`), with curriculum aligned to AP CS Principles; used by >1M learners (claim, partial).
- **Evidence:** Studies report increased intent to persist in computing, especially among under-represented students (CACM 2019 summarises).
- **Why it matters for the studio:** Evidence that code-as-composition scales to novices and that a sample/loop palette plus algorithmic structure is an approachable "compile" model.
- **Tags:** [education] [music-as-code] [HCI-study]
- **Verification:** verified (Crossref)
- **BibKey:** freeman2019earsketch

### Sonic Pi — live coding for schools
- **Who/where/when:** Sam Aaron (with Alan Blackwell, Pamela Burnard); University of Cambridge / Raspberry Pi Foundation; JMTE 2016 ("The development of Sonic Pi and its use in educational partnerships", DOI 10.1386/jmte.9.1.75_1); IJPADM 2016; MIT-licensed software
- **Links:** https://sonic-pi.net ; https://doi.org/10.1386/jmte.9.1.75_1
- **What it is:** Ruby-based live-coding environment (SuperCollider backend) with `live_loop`, samples, synths and effects, designed for the UK computing curriculum and for performance ("Sonic Pi: Live & Coding" project with schools).
- **Evidence:** Classroom studies with teachers/students in Cambridge; later Korean and UK Code Club studies.
- **Why it matters for the studio:** Live loops embody an *iterative edit-while-playing* loop — an interaction model worth borrowing for annotate→compile cycles.
- **Tags:** [education] [music-as-code] [real-time]
- **Verification:** verified (Crossref)
- **BibKey:** aaron2016sonicpi

### Practice/learning apps — Yousician, Simply Piano, Flowkey, Melodics, Piano Marvel, SmartMusic, Chordify, Moises
- **Who/where/when:** Yousician (Helsinki, 2010–; pitch-detection feedback for guitar/piano/bass/ukulele/voice); Simply Piano (JoyTunes/Simply, Tel Aviv); Flowkey (Berlin; Yamaha-partnered); Melodics (Auckland; pad/keys/drums timing training); Piano Marvel (US; MIDI-based assessment + SASR sight-reading test); SmartMusic (MakeMusic; assessment of scanned band/orchestra parts — sunset alongside Finale, status partial); Chordify (Utrecht, 2013–; automatic chord extraction from any audio/YouTube, from de Haas/Koops/Wiering's research); Moises (Moises Systems, 2019–; stem separation, chord and key detection, tempo control for practice)
- **Links:** https://yousician.com ; https://www.simplypiano.com ; https://www.flowkey.com ; https://melodics.com ; https://pianomarvel.com ; https://chordify.net ; https://moises.ai
- **What it is:** Commercial "AI tutor" ecosystem based on real-time pitch/onset detection (mic) or MIDI, gamified progress, and, increasingly, source separation and chord recognition to turn any recording into practice material.
- **Evidence:** Few peer-reviewed efficacy studies; industry-scale user bases.
- **Why it matters for the studio:** They define user expectations for real-time feedback on playing/singing — reusable for the "hum or play it in" annotation path — and show stem separation (Moises) as a practical way to ingest example audio.
- **Tags:** [education] [product] [transcription] [real-time]
- **Verification:** partial (recalled)
- **BibKey:** yousician2026

### Generative AI in composition teaching — early empirical papers (2024–2026)
- **Who/where/when:** Jose Eduardo Oros, Richard Randall, Rahul Telang (CMU), "Help That Hurts: The Creativity Cost of Generative AI Ideation in Music Composition" (SSRN 2026, DOI 10.2139/ssrn.6481538); Bin Liu & Yuanyuan Liao, "Integrating IBM Watson BEAT generative AI software into flute music learning" (Education and Information Technologies 2025, DOI 10.1007/s10639-025-13394-y); SunYoung Park & YoungSun Choo, "Exploring Interactions with AI-Based Music Composition Tools Across Different Levels of Musical Expertise" (Korean Music Education Society 2026); Prapussornchaikul & Gonsalves, WAIE 2024
- **Links:** https://doi.org/10.2139/ssrn.6481538 ; https://doi.org/10.1007/s10639-025-13394-y
- **What it is:** First wave of studies on generative AI in music learning: an experiment suggesting AI ideation can *reduce* creative output quality/originality in composition tasks ("help that hurts"); classroom integrations of generative tools; expertise-dependent interaction patterns with AI composition tools.
- **Evidence:** Study designs and N not fetched (Crossref metadata only); venue quality mixed — treat as indicative, not conclusive. No dedicated ISMIR/NIME "LLM feedback on student compositions" paper could be verified in this pass.
- **Why it matters for the studio:** Early evidence that *how* AI assistance is inserted matters for creative outcomes — supporting the founder's "human-centred, AI as compiler not ideator" stance; also a gap the studio could study (feedback on compositions rather than generation).
- **Tags:** [education] [HCI-study] [creativity-support] [evaluation]
- **Verification:** partial (Crossref records only)
- **BibKey:** oros2026helpthathurts
