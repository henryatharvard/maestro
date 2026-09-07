# 05 — HCI / Creativity-Support / Mixed-Initiative Literature on Human–AI Music Co-Creation

**Overview.** This cluster covers (a) the theoretical frameworks HCI and computational-creativity researchers use to describe human–AI co-creation (creativity support tools, mixed-initiative creative interfaces, COFI, alternating vs. task-divided co-creativity, Lubart's four roles, evaluation frameworks); (b) music co-creation *systems that were actually put in front of musicians* with a study (ChordRipple, FlowComposer, Cococo, Music-Creation-by-Example, Expressive Communication, Calliope/MMM-C, Amuse, ReaLJam, Loop Copilot, RefinPaint, Rhapsody Refiner, Composer's Assistant 2, Notochord, Magenta Studio, Music AI Sandbox); (c) empirical studies of what musicians, composers and producers want and fear (AI Song Contest 2020/2023/2024 and the HAISP dataset, Sony CSL's 18-month practitioner study, Newman/Morris/Lee ISMIR 2023, Fu et al. DIS 2025, Ronchini et al. 2025, Sturm/Ben-Tal folk-rnn work); and (d) evaluation and interaction-paradigm papers (CSI, Karimi et al., Yang & Lerch, XAI-for-the-arts, interactive ML, alternatives/version-control anchors). The consistent finding across 2016–2026 is that musicians accept AI most readily as a *steerable, decomposable, interruptible partner* that operates on material they authored, inside the tools they already use, and that leaves them with a sense of ownership; "generate a whole song from a prompt" interfaces rate lowest on control, ownership and comprehension, and are used mainly for ideation.

## Key takeaways for the studio

1. **Steering beats generating.** In the two controlled studies that varied *both* model and interface (Louie et al. 2020, 2022), a better steering interface produced larger gains in control, ownership and self-efficacy than a better model did; both improved listener-rated quality. Design the loop (annotate → compile → edit) first; the model is the second lever.
2. **Decompose, don't blob.** AI Song Contest teams (Huang et al. 2020; Micchi et al. 2021; HAISP 2024/2025) split songwriting into structure / harmony / melody / lyrics / arrangement, ran separate models, then recombined and curated by hand. The founder's "compile from parts + annotations" maps directly onto what practitioners already do by hand.
3. **Ownership tracks effort and authored input.** Cococo, Amuse and Rhapsody Refiner (Krol et al. 2025, 4-week ecological study) all show that systems that *require* strong human input and let users fix "moments, not whole ideas" preserve ownership; automatic completion is rejected by practising musicians.
4. **Interruptible, bar-level, in-place editing is the accepted primitive.** FlowComposer (2016), Calliope/MMM (2022), RefinPaint (2024) and Composer's Assistant 2 (2024) all converge on "select bars/tracks → regenerate with constraints → keep the rest." Users rarely generate > 8 bars at a time (FlowComposer usage data).
5. **Stay inside the DAW / notation surface.** Sony CSL (Deruty et al. 2022), MMM-C, Magenta Studio, Composer's Assistant 2 and Loop Copilot's participants all say tool-switching kills adoption; interoperability via MIDI/MusicXML/WAV is a top design implication in Newman et al. 2023.
6. **A single parameter is not control.** MMM-C's one-slider (temperature) design scored acceptable usability but "desire for more control" averaged 9.54/10; ReaLJam users disagreed on almost every setting — expose fine-grained, per-user-tunable controls (density, polyphony, rhythm, pitch range, example similarity).
7. **Communication from AI to human is the under-designed half.** COFI's analysis of 92 systems found almost no AI→human communication; Cococo's "explain/debug" strategies and RefinPaint's critic ("where to modify") are early examples of AI *annotating back* — a natural complement to human annotations in the studio loop.
8. **Example-based and multimodal steering work.** Cococo's example-similarity slider, MidiMe's personal-style latent, Music-Creation-by-Example (104 video creators), Amuse (images/text/audio → chords, CHI 2025) and Sketch2Sound (vocal imitation → sound) validate "steer with an example / a hum / an image" rather than only with text.
9. **Measure with CSI + ownership + control + comprehension, plus listener tests.** The field's de-facto instrument set: Creativity Support Index (Cherry & Latulipe), SUS/TAM, Likert items on control/ownership/self-efficacy, think-aloud, and paired listener comparisons (Louie 2022, Amuse). Karimi et al. 2018 warns that co-creative systems over-evaluate UX and under-evaluate the *creativity of the collaboration*.
10. **Ethics and provenance are design requirements, not afterthoughts.** Professional creators (Newman 2023; Sturm 2019; Deruty 2022) prefer open, explainable, locally-run models trained on consented data; Micchi et al. argue that documented human selection/modification constitutes ownership — log the annotation/compile history as provenance.

---

## A. Frameworks and theory

### CST2007 — Creativity Support Tools: Accelerating Discovery and Innovation
- **Who/where/when:** Ben Shneiderman, University of Maryland; Communications of the ACM 50(12):20–32, 2007
- **Links:** https://doi.org/10.1145/1323688.1323689
- **What it is:** Agenda-setting essay defining creativity support tools (CSTs) and principles for designing them: support exploratory search, enable collaboration, provide rich history-keeping (undo, versioning, replay), design with low thresholds/high ceilings/wide walls, and support many paths and many styles. Argues CST research needs new evaluation methods (long-term case studies rather than short lab tasks).
- **Evidence:** Position/essay; synthesises the 2005 NSF workshop on CSTs.
- **Why it matters for the studio:** "Rich history-keeping" and "many paths/styles" are exactly the version-tree / annotation-history features a compile-loop needs; also legitimises longitudinal case-study evaluation of a composer's tool.
- **Tags:** [creativity-support] [co-creation-framework] [evaluation]
- **Verification:** verified (Crossref metadata)
- **BibKey:** shneiderman2007cst

### HCAI — Human-Centered Artificial Intelligence: Reliable, Safe & Trustworthy (and the 2022 book)
- **Who/where/when:** Ben Shneiderman, University of Maryland; International Journal of Human–Computer Interaction 36(6):495–504, 2020; book *Human-Centered AI*, Oxford University Press, 2022
- **Links:** https://doi.org/10.1080/10447318.2020.1741118
- **What it is:** Proposes a two-dimensional framework (human control × computer automation) replacing the one-dimensional "more automation = less control" view; argues for designs with *high* human control *and* high automation, with "supertools" and "active appliances" rather than autonomous agents; emphasises reliable, safe, trustworthy systems via audit trails, explainability and human oversight.
- **Evidence:** Conceptual framework; the book expands it with design patterns and governance structures.
- **Why it matters for the studio:** Gives the founder's "human is the center; AI is the compiler" thesis a citable HCI grounding: high automation (compile arrangements) and high human control (notation editing, annotations) are not a trade-off.
- **Tags:** [co-creation-framework] [creativity-support]
- **Verification:** verified (Crossref metadata)
- **BibKey:** shneiderman2020hcai

### CSI — Quantifying the Creativity Support of Digital Tools through the Creativity Support Index
- **Who/where/when:** Erin Cherry, Celine Latulipe; UNC Charlotte; ACM Transactions on Computer-Human Interaction 21(4), Article 21, 2014
- **Links:** https://doi.org/10.1145/2617588
- **What it is:** A validated psychometric survey instrument (the CSI) that scores a tool on six factors — Collaboration, Enjoyment, Exploration, Expressiveness, Immersion, Results Worth Effort — using paired-factor comparisons to weight the factors per task; yields a 0–100 score.
- **Evidence:** Developed and validated over several iterations with hundreds of participants; now the standard instrument in music co-creation studies (used by Amuse 2025, MMM-C 2023 and many others).
- **Why it matters for the studio:** The instrument the studio should adopt for comparing interaction designs (e.g., with/without annotations, with/without version tree).
- **Tags:** [evaluation] [creativity-support]
- **Verification:** partial (title/venue/DOI confirmed via search results; full text not fetched)
- **BibKey:** cherry2014csi

### Lubart2005 — How can computers be partners in the creative process: Classification and commentary on the Special Issue
- **Who/where/when:** Todd Lubart; Université Paris Descartes; International Journal of Human-Computer Studies 63(4–5):365–369, 2005
- **Links:** https://doi.org/10.1016/j.ijhcs.2005.04.002 ; PDF: http://www.cs.tufts.edu/~jacob/250aui/creativity-hci.pdf
- **What it is:** Classifies computers' roles in creative work as *nanny* (manages the process, time, breaks), *pen-pal* (mediates human collaboration), *coach* (teaches creativity techniques), and *colleague* (generates alternatives that the human evaluates and refines).
- **Evidence:** Commentary on a special issue; no study.
- **Why it matters for the studio:** Still the most-cited vocabulary for "what role does the AI play"; the studio's compiler is a colleague for arrangement but could be a coach (theory hints) and nanny (session/version management) too.
- **Tags:** [co-creation-framework] [creativity-support]
- **Verification:** verified (fetched PDF)
- **BibKey:** lubart2005partners

### MICI — Mixed-Initiative Creative Interfaces
- **Who/where/when:** Sebastian Deterding, Jonathan Hook, Rebecca Fiebrink, Marco Gillies, Jeremy Gow, Memo Akten, Gillian Smith, Antonios Liapis, Kate Compton; York, Goldsmiths, WPI, Malta, UCSC; CHI 2017 Extended Abstracts (workshop)
- **Links:** https://doi.org/10.1145/3027063.3027072 ; workshop proceedings https://ceur-ws.org/Vol-1907/
- **What it is:** Defines mixed-initiative creative interfaces as systems where human and computer take turns constraining, suggesting and evaluating in a tight loop, sitting between human-driven creativity tools and autonomous computational creativity. Names open challenges: letting non-programmers express formal constraints, legibility of AI decisions, fatigue, evaluation of co-creativity, up-skilling vs de-skilling.
- **Evidence:** Workshop proposal; the CEUR proceedings collect ~20 position papers.
- **Why it matters for the studio:** Annotations are precisely a way for non-programmers to "express constraints"; the paper's questions (legibility, fatigue, evaluation) are the studio's research questions.
- **Tags:** [mixed-initiative] [co-creation-framework] [creativity-support]
- **Verification:** verified (fetched White Rose eprint PDF)
- **BibKey:** deterding2017mici

### Kantosalo2016 — Modes for Creative Human-Computer Collaboration: Alternating and Task-Divided Co-Creativity
- **Who/where/when:** Anna Kantosalo, Hannu Toivonen; University of Helsinki; ICCC 2016, Paris
- **Links:** https://researchportal.helsinki.fi/en/publications/modes-for-creative-human-computer-collaboration-alternating-and-t/ ; PDF via computationalcreativity.net/iccc2016
- **What it is:** Using Wiggins' creativity-as-search formalism, distinguishes *alternating co-creativity* (turn-taking on the same artefact) from *task-divided co-creativity* (human and computer own different sub-tasks, working in parallel), and analyses what the computational agent must be able to do in each.
- **Evidence:** Theoretical; grounded in the authors' Poetry Machine work with children.
- **Why it matters for the studio:** The compile loop is *both*: alternating at the notation level (compose → compile → edit) and task-divided at the arrangement level (human writes lead sheet, AI voices/orchestrates). Naming the mode per feature clarifies the interaction design.
- **Tags:** [co-creation-framework] [mixed-initiative]
- **Verification:** verified (fetched Helsinki research-portal record)
- **BibKey:** kantosalo2016modes

### Karimi2018 — Evaluating Creativity in Computational Co-Creative Systems
- **Who/where/when:** Pegah Karimi, Kazjon Grace, Mary Lou Maher, Nicholas Davis; UNC Charlotte, University of Sydney; ICCC 2018
- **Links:** https://arxiv.org/abs/1807.09886 ; https://computationalcreativity.net/iccc2018/sites/default/files/papers/ICCC_2018_paper_26.pdf
- **What it is:** A framework of four questions for evaluating co-creative systems — *who* evaluates (user, system, third party), *what* is evaluated (product, process, interaction, user experience), *when*, and *how* — applied to co-creative systems in art, humour, games and robotics.
- **Evidence:** Survey/analysis; finds existing systems overwhelmingly evaluate user experience rather than the creativity of the collaboration or the artefact.
- **Why it matters for the studio:** A checklist for designing studies that evaluate the *compiled music* and the *process* (e.g., how annotations change outputs), not only satisfaction.
- **Tags:** [evaluation] [co-creation-framework]
- **Verification:** verified (fetched arXiv abstract)
- **BibKey:** karimi2018evaluating

### DrawingApprentice — Empirically Studying Participatory Sense-Making in Abstract Drawing with a Co-Creative Cognitive Agent
- **Who/where/when:** Nicholas Davis, Chih-Pin Hsiao, Kunwar Yashraj Singh, Lisa Li, Brian Magerko; Georgia Tech; IUI 2016 (plus "Quantifying Collaboration with a Co-Creative Drawing Agent," ACM TiiS 2017)
- **Links:** https://doi.org/10.1145/2856767.2856795 ; https://doi.org/10.1145/3009981 ; http://mici.codingconduct.cc/drawing-apprentice/
- **What it is:** Drawing Apprentice is a real-time co-creative drawing partner that responds to the user's strokes with its own, alternating on a shared canvas; the papers introduce *participatory sense-making* and the "creative sense-making" framework for analysing turn-by-turn co-creation, later formalised as Observable Creative Sense-Making (C&C 2023).
- **Evidence:** IUI 2016 study compared the agent to a Wizard-of-Oz human; users often could not distinguish them, and enjoyment/collaboration ratings were comparable; TiiS 2017 quantifies collaboration behaviours.
- **Why it matters for the studio:** The canonical non-music example of *simultaneous* (rather than turn-taking) co-creation; its sense-making coding scheme is reusable for analysing composer–AI sessions.
- **Tags:** [co-creation-framework] [HCI-study] [real-time] [evaluation]
- **Verification:** partial (venue/DOI from search results and ACM listing; PDF not fetched)
- **BibKey:** davis2016drawingapprentice

### MoraiMaker — Friend, Collaborator, Student, Manager: How Design of an AI-Driven Game Level Editor Affects Creators
- **Who/where/when:** Matthew Guzdial, Nicholas Liao, Jonathan Chen, Shao-Yu Chen, Shukan Shah, Vishwa Shah, Joshua Reno, Gillian Smith, Mark O. Riedl; Georgia Tech, WPI; CHI 2019
- **Links:** https://arxiv.org/abs/1901.06417 ; https://doi.org/10.1145/3290605.3300854 ; companion framework paper https://arxiv.org/abs/1903.09709
- **What it is:** Morai Maker is a *turn-based* co-creative level editor for Super Mario-style games: the human edits, then the AI takes a turn adding content, and so on. Compares three AI agents (Markov chain, Bayes net, LSTM) and how designers frame the AI's role.
- **Evidence:** Two mixed-methods studies, >100 participants total (91 in the controlled study). Designers split by preferred AI role — friend, collaborator, student or manager — and the AI changed how they designed; the same agent was rated helpful or annoying depending on the role a designer wanted.
- **Why it matters for the studio:** Strong evidence that role preference is *individual* and that turn-taking must be interruptible; the studio should let the composer set how much initiative the compiler takes.
- **Tags:** [mixed-initiative] [game] [HCI-study] [co-creation-framework]
- **Verification:** verified (fetched arXiv abstract page)
- **BibKey:** guzdial2019friend

### COFI — Designing Creative AI Partners with COFI: A Framework for Modeling Interaction in Human-AI Co-Creative Systems
- **Who/where/when:** Jeba Rezwana, Mary Lou Maher; UNC Charlotte; ACM Transactions on Computer-Human Interaction 30(5), 2023 (arXiv 2022)
- **Links:** https://doi.org/10.1145/3519026 ; https://arxiv.org/abs/2204.07666
- **What it is:** The Co-Creative Framework for Interaction design (COFI) decomposes co-creative interaction into *collaboration* dimensions (participation style: alternating/parallel; timing: spontaneous/planned; task distribution; contribution type; creative process) and *communication* dimensions (human→AI: direct manipulation, embodied, intentional; AI→human: task-related and non-task-related communication).
- **Evidence:** Coded 92 existing co-creative systems; found the field concentrates on AI generative ability and almost entirely lacks AI→human communication (explanations, intentions, confidence), which the authors argue is what makes AI a *partner* rather than a tool.
- **Why it matters for the studio:** The best available vocabulary for specifying the studio's interaction design; suggests the compiler should *talk back* (annotate what it changed and why) — the mirror image of the composer's annotations.
- **Tags:** [co-creation-framework] [mixed-initiative] [evaluation]
- **Verification:** verified (fetched arXiv abstract)
- **BibKey:** rezwana2023cofi

### CreativePenpal — Understanding User Perceptions, Collaborative Experience and User Engagement in Different Human-AI Interaction Designs for Co-Creative Systems
- **Who/where/when:** Jeba Rezwana, Mary Lou Maher; UNC Charlotte; ACM Creativity & Cognition 2022, pp. 38–48
- **Links:** https://doi.org/10.1145/3527927.3532789
- **What it is:** Compares two versions of a co-creative sketching system ("Creative Penpal"): one where the AI only contributes sketches, and one where it also *communicates* (speech/text about its intentions and reactions).
- **Evidence:** Between-subjects user study; the communicating version was perceived as more collaborative, engaging and partner-like, with higher perceived reliability, though some users found it intrusive.
- **Why it matters for the studio:** Direct evidence for adding AI→human commentary to the compile step (e.g., "I re-voiced the piano because your annotation asked for a Foster-style ballad").
- **Tags:** [HCI-study] [co-creation-framework] [mixed-initiative]
- **Verification:** partial (Crossref metadata fetched; findings from recall)
- **BibKey:** rezwana2022perceptions

### CCEval — Computational-creativity evaluation anchors (Boden; Colton & Wiggins; Jordanous)
- **Who/where/when:** Margaret Boden, *The Creative Mind: Myths and Mechanisms*, 2nd ed., Routledge 2004; Simon Colton & Geraint Wiggins, "Computational Creativity: The Final Frontier?", ECAI 2012; Anna Jordanous, "A Standardised Procedure for Evaluating Creative Systems (SPECS)", Cognitive Computation 4(3):246–279, 2012
- **Links:** https://doi.org/10.1007/s12559-012-9156-1 (Jordanous)
- **What it is:** Boden's P-/H-creativity and combinational/exploratory/transformational creativity; Colton & Wiggins' definition of computational creativity and the "creative tripod" (skill, appreciation, imagination); Jordanous' SPECS — 14 components of creativity and a three-step procedure (define creativity for the domain, choose standards, test).
- **Evidence:** Theoretical; SPECS was validated on musical-improvisation systems.
- **Why it matters for the studio:** Provides the definitions a literature review needs before discussing "co-creativity"; SPECS is a candidate for evaluating the compiler's contributions as *creative* rather than merely useful.
- **Tags:** [co-creation-framework] [evaluation] [theory-analysis]
- **Verification:** partial (Jordanous verified via Crossref; Boden/Colton–Wiggins from recall)
- **BibKey:** jordanous2012standardised

### SecondMind — "It Felt Like Having a Second Mind": Investigating Human-AI Co-creativity in Prewriting with Large Language Models
- **Who/where/when:** Qian Wan, Siying Hu, Yu Zhang, Piaohong Wang, Bo Wen, Zhicong Lu; City University of Hong Kong; PACM HCI 8 (CSCW1), 2024 (arXiv 2023)
- **Links:** https://arxiv.org/abs/2307.10811 ; https://doi.org/10.1145/3637361
- **What it is:** Qualitative study of how people co-create with GPT-3 during prewriting (story and slogan tasks); proposes a three-stage iterative co-creativity model — Ideation (LLM-led), Illumination (human-led, LLM organises), Implementation (human-led, LLM enriches details) — with humans holding initiative except when blocked.
- **Evidence:** N=15 creativity-major students, three sessions each (scenario ideation, think-aloud, interviews), constructivist grounded theory.
- **Why it matters for the studio:** A general-purpose model of *who leads when* in LLM co-creation that transfers to compose/annotate/compile; supports designing the compiler to take initiative mainly at ideation/blockage points.
- **Tags:** [HCI-study] [co-creation-framework] [LLM-agent]
- **Verification:** verified (fetched arXiv abstract page)
- **BibKey:** wan2024secondmind

### MLasTool — The Machine Learning Algorithm as Creative Musical Tool (and Wekinator)
- **Who/where/when:** Rebecca Fiebrink, Baptiste Caramiaux; Goldsmiths / IRCAM; chapter in *The Oxford Handbook of Algorithmic Music*, 2018 (arXiv 2016); Wekinator: Fiebrink, Trueman, Cook, "A Meta-Instrument for Interactive, On-the-Fly Machine Learning," NIME 2009
- **Links:** https://arxiv.org/abs/1611.00379 ; http://www.wekinator.org
- **What it is:** Argues that ML algorithms should be understood as *interfaces* whose affordances intersect with musicians' goals — supervised learning by demonstration lets a musician teach an idiosyncratic mapping in minutes and then "break the rules." Wekinator operationalises this: record a few gesture→sound examples, train, play, correct, retrain (interactive machine learning).
- **Evidence:** Years of workshops and studies with composers/performers (Fiebrink's PhD, 2011) showing fast iteration and example-based specification outperform parameter tweaking for non-programmers.
- **Why it matters for the studio:** The founding case for *example-based* steering ("here is a hummed phrase / an audio clip; make it like this") and for tight train–test–correct loops — the interactive-ML lineage the compile loop belongs to.
- **Tags:** [co-creation-framework] [expression-performance] [real-time] [HCI-study]
- **Verification:** verified (fetched arXiv abstract)
- **BibKey:** fiebrink2018mlcreativetool

---

## B. Music co-creation systems with user studies

### ChordRipple — Recommending Chords to Help Novice Composers Go Beyond the Ordinary
- **Who/where/when:** Cheng-Zhi Anna Huang, David Duvenaud, Krzysztof Z. Gajos; Harvard; IUI 2016
- **Links:** https://doi.org/10.1145/2856767.2856792 ; PDF https://www.eecs.harvard.edu/~kgajos/papers/2016/huang16chordripple.pdf
- **What it is:** A chord-progression editor with a Chord2Vec (skip-gram) embedding trained on 200 rock songs; recommends *adventurous* single-chord substitutions and "ripples" that re-write neighbouring chords to smooth a substitution. User types/edits chords; the tool proposes; the user accepts or ignores.
- **Evidence:** Study 1: 15 participants with composition experience, think-aloud + interviews. Study 2: 9 music students, three conditions (typical, adventurous, ripple); adventurous recommendations significantly increased chord novelty (p=0.0039); ripples did not increase adoption; users split between wanting familiar vs "breaking-out" suggestions.
- **Why it matters for the studio:** Early template for *local* suggestions inside a symbolic editor with context repair — the chord-level analogue of "edit one thing, let the compiler reconcile the neighbours."
- **Tags:** [symbolic-generation] [editing] [HCI-study] [creativity-support] [notation]
- **Verification:** verified (fetched PDF)
- **BibKey:** huang2016chordripple

### FlowComposer — Assisted Lead Sheet Composition using FlowComposer (Flow Machines / "Daddy's Car")
- **Who/where/when:** Alexandre Papadopoulos, Pierre Roy, François Pachet; Sony CSL Paris; CP 2016 (22nd Int. Conf. on Principles and Practice of Constraint Programming), Toulouse
- **Links:** https://www.francoispachet.fr/wp-content/uploads/2021/01/roy-16b.pdf ; "Daddy's Car" (Carré, Pachet, Ghedini 2016) https://www.youtube.com/watch?v=LSHZ_b05W7o
- **What it is:** Web lead-sheet editor: the user picks a style corpus (from >12,000 lead sheets), enters partial melody and/or chords, and the system fills in the rest using Markov chains with regular (metrical) constraints; the user can select any region and regenerate only that fragment, with sliders for harmonic conformance, "inspiration" from the current piece vs corpus, note duration and chord-change rate.
- **Evidence:** Deployed in professional projects (Benoît Carré's album incl. "Daddy's Car"; three songs for the musical *Beyond the Fence*, London 2016). Observed usage: composers rarely generate more than 8 bars at a time; they use it for fragments inside longer human compositions.
- **Why it matters for the studio:** The closest 2016 precedent for the founder's loop — symbolic lead sheet, partial human input, constrained regeneration of selected regions, style-by-corpus. Its usage data (short fragments, lock-and-regenerate) are design priors.
- **Tags:** [symbolic-generation] [infilling] [editing] [controllability] [notation] [style-transfer] [history]
- **Verification:** verified (fetched CP 2016 PDF)
- **BibKey:** papadopoulos2016flowcomposer

### MagentaStudio — Magenta Studio: Augmenting Creativity with Deep Learning in Ableton Live
- **Who/where/when:** Adam Roberts, Jesse Engel, Yotam Mann, Jon Gillick, Claire Kayacik, Signe Nørly, Monica Dinculescu, Carey Radebaugh, Curtis Hawthorne, Douglas Eck; Google Brain (Magenta); MUME 2019 workshop
- **Links:** https://magenta.tensorflow.org/studio ; https://research.google/pubs/magenta-studio-augmenting-creativity-with-deep-learning-in-ableton-live/ ; https://github.com/magenta
- **What it is:** Five Max-for-Live devices — Continue (RNN melody/drum continuation up to 32 bars), Generate (MusicVAE 4-bar phrases), Interpolate (up to 16 clips morphing between two clips), Groove and Drumify (GrooVAE humanisation / rhythm→drums). Built with Electron + TensorFlow.js; open source (Apache-2.0).
- **Evidence:** No formal user study in the paper; adoption/feedback informal. Demonstrated that in-DAW clip-level AI tools are feasible for mainstream producers.
- **Why it matters for the studio:** The reference architecture for "AI operates on the clip you selected, inside your DAW"; Interpolate is an early example of *alternatives as a navigable space*.
- **Tags:** [DAW-plugin] [symbolic-generation] [toolkit] [product]
- **Verification:** verified (fetched Magenta page and Google Research record)
- **BibKey:** roberts2019magentastudio

### BachDoodle — The Bach Doodle: Approachable Music Composition with Machine Learning at Scale
- **Who/where/when:** Cheng-Zhi Anna Huang, Curtis Hawthorne, Adam Roberts, Monica Dinculescu, James Wexler, Leon Hong, Jacob Howcroft; Google; ISMIR 2019
- **Links:** https://arxiv.org/abs/1907.06637
- **What it is:** Users enter a two-bar melody on a staff; Coconet (Gibbs-sampling convolutional infilling model) harmonises it in Bach's style in ~2 s in the browser (TF.js, 400 KB quantised model); users could rate and donate compositions.
- **Evidence:** >55 million harmonisation queries in three days; "350 years" of cumulative interaction; produced a public dataset of user melodies + harmonisations + ratings.
- **Why it matters for the studio:** Largest-scale evidence that *notation-first, human-melody-in, AI-harmony-out* is approachable to non-experts; Coconet's infilling is the same primitive as "annotate a voice, compile the others."
- **Tags:** [symbolic-generation] [infilling] [notation] [HCI-study] [dataset] [education]
- **Verification:** verified (fetched arXiv abstract)
- **BibKey:** huang2019bachdoodle

### MidiMe — Personalizing a MusicVAE model with user data
- **Who/where/when:** Monica Dinculescu, Jesse Engel, Adam Roberts; Google Brain (Magenta); NeurIPS 2019 Workshop on Machine Learning for Creativity and Design
- **Links:** https://magenta.tensorflow.org/midi-me
- **What it is:** Trains a tiny VAE (4-D latent) on top of MusicVAE's 256-D latent space using one user MIDI file, in-browser in seconds; the user then explores a personal 4-knob space that generates variations "in the style of" their input without memorising it.
- **Evidence:** Demo/technique paper; no controlled study.
- **Why it matters for the studio:** A lightweight mechanism for *example-based personalisation* — the composer's own sketches define the space the compiler samples from.
- **Tags:** [symbolic-generation] [controllability] [style-transfer] [toolkit]
- **Verification:** verified (fetched Magenta blog)
- **BibKey:** dinculescu2019midime

### PianoGenie — Piano Genie
- **Who/where/when:** Chris Donahue, Ian Simon, Sander Dieleman; UC San Diego, Google Brain, DeepMind; IUI 2019
- **Links:** https://arxiv.org/abs/1810.05246 ; https://doi.org/10.1145/3301275.3302288
- **What it is:** An 8-button controller decoded in real time into 88-key piano performances via an RNN autoencoder with a discrete bottleneck and musically motivated constraints; the user controls contour/rhythm, the model chooses pitches.
- **Evidence:** Informal user evaluation; widely deployed as a web demo.
- **Why it matters for the studio:** Archetype of *AI as instrument* (the human performs intent at low dimensionality; the model realises it) — a paradigm the studio can use for humming/tapping input.
- **Tags:** [real-time] [expression-performance] [controllability] [humming]
- **Verification:** verified (fetched arXiv abstract)
- **BibKey:** donahue2019pianogenie

### Cococo — Novice-AI Music Co-Creation via AI-Steering Tools for Deep Generative Models
- **Who/where/when:** Ryan Louie, Andy Coenen, Cheng-Zhi Anna Huang, Michael Terry, Carrie J. Cai; Northwestern University, Google Research; CHI 2020
- **Links:** https://doi.org/10.1145/3313831.3376739 ; PDF https://youralien.github.io/files/cococo_chi2020_copy.pdf
- **What it is:** A four-voice piano-roll editor over Coconet with four *AI-steering tools*: voice lanes (restrict which voices/time-steps are generated), semantic sliders (happy–sad, conventional–surprising), an example-based similarity slider, and multiple alternatives for audition. The human composes bit-by-bit and asks the model to fill constrained regions.
- **Evidence:** Formative study N=11; summative within-subjects study N=21 novice composers (two pieces, one per interface, think-aloud + interviews). Versus a plain generate-and-accept baseline, Cococo significantly improved creative expression (5.5 vs 3.8), self-efficacy (5.9 vs 3.7), engagement (6.0 vs 4.4), controllability (5.9 vs 3.5), comprehensibility (5.3 vs 3.2) and ownership (5.2 vs 3.8). Users developed "debugging" strategies to understand model behaviour.
- **Why it matters for the studio:** The most direct evidence that region-restricted infilling + semantic/example sliders + alternatives raise ownership and control; its "debug the AI" behaviour motivates AI-side explanations.
- **Tags:** [HCI-study] [infilling] [controllability] [symbolic-generation] [creativity-support] [mixed-initiative]
- **Verification:** verified (fetched author PDF)
- **BibKey:** louie2020cococo

### MusicByExample — Music Creation by Example
- **Who/where/when:** Emma Frid, Celso Gomes, Zeyu Jin; KTH, Adobe Research; CHI 2020
- **Links:** https://doi.org/10.1145/3313831.3376514
- **What it is:** UI paradigm for video creators who need soundtrack music: the user supplies an *example song*; an AI engine generates similar music which the user can interactively regenerate and mix (stem-level control), rather than describing music in words.
- **Evidence:** Multi-phase studies with 104 video creators in total; example-based input was found more natural than tag/text search and revealed design insights on human–AI collaboration (control, trust in regeneration).
- **Why it matters for the studio:** Validates "insert example audio as an annotation" as a primary steering modality for people who think in references rather than theory terms.
- **Tags:** [HCI-study] [multimodal-input] [audio-generation] [controllability]
- **Verification:** verified (Semantic Scholar abstract + Crossref metadata; full text not fetched)
- **BibKey:** frid2020example

### AISongContest2020 — AI Song Contest: Human-AI Co-Creation in Songwriting
- **Who/where/when:** Cheng-Zhi Anna Huang, Hendrik Vincent Koops, Ed Newton-Rex, Monica Dinculescu, Carrie J. Cai; Google, RTL/Utrecht, Jukedeck; ISMIR 2020
- **Links:** https://arxiv.org/abs/2010.05388 ; https://doi.org/10.5281/zenodo.4245530
- **What it is:** Qualitative study of the 13 teams (61 people; musicians + ML developers) who entered the first AI Song Contest, examining how they built songs with ML models.
- **Evidence:** Teams decomposed songwriting into building blocks (melody, harmony, lyrics, drums, structure), ran separate models and recombined; because models were not steerable they generated huge numbers of samples and curated post hoc or ranked algorithmically; authors call for interfaces that are *decomposable, steerable, interpretable and adaptive*.
- **Why it matters for the studio:** The empirical origin of "decomposable + steerable" as design requirements — practically a spec for the compile loop.
- **Tags:** [HCI-study] [co-creation-framework] [controllability] [structure]
- **Verification:** verified (fetched arXiv abstract)
- **BibKey:** huang2020aisongcontest

### IKeepCounting — I Keep Counting: An Experiment in Human/AI Co-creative Songwriting
- **Who/where/when:** Gianluca Micchi, Louis Bigo, Mathieu Giraud, Richard Groult, Florence Levé; Algomus (Univ. Lille / CRIStAL, Univ. Picardie); TISMIR 4(1), 2021
- **Links:** https://doi.org/10.5334/tismir.93
- **What it is:** First-person account of an AI Song Contest 2020 entry: structure from a Markov model (SALAMI), chords from an LSTM (Eurovision MIDI), lyrics from GPT-2 seeded with Eurovision bigrams, hook from a classical-theme database; humans filtered candidates (sometimes by dice roll), composed verse melodies, arranged and produced. Contrasts "AI as automation" with "AI as suggestion."
- **Evidence:** >25 documented human interventions; surprising AI chords (F#maj7, Bbm) acted as productive constraints; the team argues deliberate selection/modification of AI material constitutes authorship and released the song CC-BY-SA.
- **Why it matters for the studio:** A concrete, honest log of a *compile-from-parts* workflow and of how constraints from AI suggestions can enhance creativity; supports logging interventions as provenance.
- **Tags:** [HCI-study] [co-creation-framework] [symbolic-generation] [structure] [ethics-legal]
- **Verification:** verified (fetched TISMIR article page)
- **BibKey:** micchi2021ikeepcounting

### SocialGlue — AI as Social Glue: Uncovering the Roles of Deep Generative AI during Social Music Composition
- **Who/where/when:** Minhyang (Mia) Suh, Emily Youngblom, Michael Terry, Carrie J. Cai; Google Research / University of Washington; CHI 2021
- **Links:** https://doi.org/10.1145/3411764.3445219
- **What it is:** Lab study of *pairs* of strangers co-composing with and without Cococo's generative model, to see how AI reshapes human–human creative collaboration.
- **Evidence:** N=30 (15 pairs stratified: 5 novice, 5 hobbyist, 5 serious composer pairs), two 20-minute co-composition tasks, think-aloud + interviews. AI acted as common-ground seeder, psychological safety net, progress catalyst, friction mitigator and *role transformer* — pairs shifted from co-composing to co-*producing* (evaluating AI output), easing collaboration but reducing its depth.
- **Why it matters for the studio:** Warns that a generous compiler can turn composers into curators; the studio should keep authoring primitives (notation editing, sketching) primary and generation secondary.
- **Tags:** [HCI-study] [co-creation-framework] [creativity-support]
- **Verification:** partial (ACM page blocked; N/method from a secondary summary and OUCI index)
- **BibKey:** suh2021socialglue

### COSMIC — A Conversational Interface for Human-AI Music Co-Creation
- **Who/where/when:** Yixiao Zhang, Gus Xia, Mark Levy, Simon Dixon; QMUL C4DM, NYU Shanghai, Apple; NIME 2021
- **Links:** https://doi.org/10.21428/92fbeb44.110a7a32
- **What it is:** An early chatbot-style music co-creation system: natural-language requests are parsed into intents and routed to generation modules (melody, lyrics), and the user iterates by conversation.
- **Evidence:** System paper with preliminary demonstration; no large study.
- **Why it matters for the studio:** Precursor of LLM-orchestrated conversational music tools (Loop Copilot, MusicAgent); useful as the origin point of the "conversational vs direct-manipulation" comparison.
- **Tags:** [LLM-agent] [symbolic-generation] [co-creation-framework]
- **Verification:** partial (Crossref metadata verified; content from recall)
- **BibKey:** zhang2021cosmic

### ExpressiveComm — Expressive Communication: Evaluating Developments in Generative Models and Steering Interfaces for Music Creation
- **Who/where/when:** Ryan Louie, Jesse Engel, Cheng-Zhi Anna Huang; Northwestern University, Google Research; ACM IUI 2022 (arXiv 2021)
- **Links:** https://doi.org/10.1145/3490099.3511159 ; https://arxiv.org/abs/2111.14951
- **What it is:** A 2×2 evaluation framework crossing *model* (PerformanceRNN vs Music Transformer) with *interface* (radio-button curation of 10 whole phrases vs chunk-by-chunk steering with semantic filters); composers must communicate the feeling of a Dixit card through generated music.
- **Evidence:** 26 composers (ages 24–60) created 100+ pieces; 20 listeners made 1,020+ pairwise comparisons. Steering interface: better evocation (p<0.0001), musicality (p<0.001), and composer control/ownership/efficacy (all p<0.001). Better model: better evocation and musicality (p<0.001), coherence (p<0.003). Interface effects on composer empowerment were larger; steering compensated for model bias.
- **Why it matters for the studio:** The key citation for "interface and model are complementary, and steering matters more for agency"; also a reusable evaluation protocol (communicative goal + listener judgments).
- **Tags:** [HCI-study] [evaluation] [controllability] [symbolic-generation]
- **Verification:** verified (fetched arXiv PDF)
- **BibKey:** louie2022expressive

### Calliope — Calliope: A Co-creative Interface for Multi-Track Music Generation (and Apollo)
- **Who/where/when:** Renaud Bougueng Tchemeube, Jeff Ens, Philippe Pasquier; Metacreation Lab, Simon Fraser University; ACM Creativity & Cognition 2022 and ICCC 2022 (Apollo: ICCC 2019)
- **Links:** https://doi.org/10.1145/3527927.3535200 ; https://arxiv.org/abs/2504.14058 ; https://metacreation.net/calliope ; Apollo https://arxiv.org/abs/2504.14055
- **What it is:** Web app over the Multi-Track Music Machine (MMM, Transformer trained on ~500k MIDI files): upload MIDI, view piano roll, select bars/tracks for *infilling* or generate full multi-track material, batch-generate up to 1,000 candidates and rank them; global controls (temperature, polyphony limit, % preservation, tracks/bars per step) and per-track controls (128 GM instruments, note density 0–10, polyphony range, duration range). Apollo (2019) is the earlier corpus-based style-imitation environment.
- **Evidence:** System paper; the human-factors evaluation appeared as MMM-C (below).
- **Why it matters for the studio:** Demonstrates the *attribute-controlled bar/track infilling + batch alternatives + ranking* workflow on symbolic multi-track material — the natural implementation of "compile the parts I annotated."
- **Tags:** [symbolic-generation] [infilling] [controllability] [DAW-plugin] [toolkit]
- **Verification:** verified (fetched ICCC 2022 PDF)
- **BibKey:** tchemeube2022calliope

### MMM-C — Evaluating Human-AI Interaction via Usability, User Experience and Acceptance Measures for MMM-C: A Creative AI System for Music Composition
- **Who/where/when:** Renaud Bougueng Tchemeube, Jeff Ens, Cale Plut, Philippe Pasquier, Maryam Safi, Yvan Grabit, Jean-Baptiste Rolland; Simon Fraser University, Steinberg; IJCAI 2023 (AI, the Arts and Creativity track)
- **Links:** https://doi.org/10.24963/ijcai.2023/640 ; https://arxiv.org/abs/2504.14071
- **What it is:** MMM integrated into Cubase as a one-parameter plugin: select bars on tracks → set temperature → Generate (model conditions on vertical and horizontal context and instrument).
- **Evidence:** 3-part mixed-methods study, 18 expert composers (8 hobbyist, 10 professional). SUS 73.8–75.7; TAM ease 3.1–3.3/5, usefulness 3.4–3.7/5; CSI enjoyment highest (3.85/5); ease of control 5.2/10 but *desire for more control 9.5/10*. Users engaged in repeated generation and heavy curation; retained authorship; no hobbyist/professional differences.
- **Why it matters for the studio:** Quantifies the cost of under-parameterised control and shows in-DAW integration is necessary but insufficient — the annotation layer is the missing control channel.
- **Tags:** [HCI-study] [DAW-plugin] [controllability] [evaluation] [symbolic-generation]
- **Verification:** verified (fetched arXiv HTML)
- **BibKey:** tchemeube2023mmmc

### MMM4Live — MMM4Live: Multi-Track Music Machine for Ableton Live
- **Who/where/when:** Metacreation Lab (Philippe Pasquier, Jeff Ens, Renaud Bougueng Tchemeube et al.), Simon Fraser University; Max-for-Live device, beta 2023–2024
- **Links:** https://www.metacreation.net/projects/mmm4live ; https://cycling74.com/projects/mmm4live
- **What it is:** Ableton Live device that generates or continues multi-track MIDI clips (4- or 16-bar templates) with the MMM Transformer, conditioning new tracks on existing ones, with "fine control of iterative resampling"; runs locally on macOS.
- **Evidence:** Closed beta; documentation v0.1b2; no published study yet.
- **Why it matters for the studio:** Shows the Metacreation lineage moving from web to in-DAW; useful comparator for a symbolic compiler plugin.
- **Tags:** [DAW-plugin] [symbolic-generation] [product]
- **Verification:** verified (fetched project page)
- **BibKey:** metacreation2023mmm4live

### Notochord — Notochord: A Flexible Probabilistic Model for Real-Time MIDI Performance
- **Who/where/when:** Victor Shepardson, Thor Magnusson (Intelligent Instruments Lab, Iceland University of the Arts); AIMC 2022 (arXiv 2024)
- **Links:** https://arxiv.org/abs/2403.12000 ; https://github.com/Intelligent-Instruments-Lab/notochord (MIT)
- **What it is:** Autoregressive model over MIDI *sub-events* (instrument, pitch, time, velocity) trained on Lakh MIDI with <10 ms latency; because each sub-event is sampled separately, a performer can fix or constrain any of them, enabling harmonisers, improvisers, steerable generation and likelihood-based interfaces (apps: Homunculus, Harmonizer, Improviser).
- **Evidence:** Open-source system paper with live performances; no controlled user study.
- **Why it matters for the studio:** The clearest example of *sub-event-level* human intervention in a generative model — the real-time analogue of editing a note in the score and letting the model re-condition.
- **Tags:** [real-time] [symbolic-generation] [controllability] [accompaniment] [toolkit]
- **Verification:** verified (fetched arXiv abstract + GitHub README)
- **BibKey:** shepardson2022notochord

### LoopCopilot — Loop Copilot: Conducting AI Ensembles for Music Generation and Iterative Editing
- **Who/where/when:** Yixiao Zhang, Akira Maezawa, Gus Xia, Kazuhiko Yamamoto, Simon Dixon; QMUL, Yamaha, NYU Shanghai; arXiv 2023
- **Links:** https://arxiv.org/abs/2310.12404
- **What it is:** Conversational system where an LLM "conductor" interprets requests, selects and chains backend audio models (MusicGen, AudioLDM, Demucs, etc.) for generation (text-to-music, drums, impression-to-music) and *editing* (add/remove track, regenerate, effects, pitch/speed), with a Global Attribute Table (tempo, key, genre, mood, instruments, audio files) as shared blackboard for continuity across turns.
- **Evidence:** N=8 music/audio-technology users; SUS 75.3±15.3, TAM 4.09±1.09; valued for inspiration; complaints: limited musical-attribute control, prompt responsiveness, desire for DAW integration.
- **Why it matters for the studio:** Its Global Attribute Table is an early "compilation state" object; its failure modes (coarse control, no DAW) argue for symbolic, editable intermediate representations.
- **Tags:** [LLM-agent] [audio-generation] [editing] [HCI-study]
- **Verification:** verified (fetched arXiv abstract)
- **BibKey:** zhang2023loopcopilot

### MusicAgent — MusicAgent: An AI Agent for Music Understanding and Generation with Large Language Models
- **Who/where/when:** Dingyao Yu, Kaitao Song, Peiling Lu, Tianyu He, Xu Tan, Wei Ye, Shikun Zhang, Jiang Bian; Microsoft Research Asia, Peking University; EMNLP 2023 (system demonstrations)
- **Links:** https://arxiv.org/abs/2310.11954 ; https://github.com/microsoft/muzic
- **What it is:** LLM (ChatGPT) decomposes a user request into sub-tasks and invokes music tools aggregated from Hugging Face, GitHub and web APIs (generation such as timbre synthesis and analysis such as classification), handling format conversions between tools.
- **Evidence:** Demonstration; no user study.
- **Why it matters for the studio:** Shows the tool-orchestration pattern the "compiler" could use internally (route sub-tasks to specialised models) — but without a human-editable intermediate.
- **Tags:** [LLM-agent] [toolkit]
- **Verification:** partial (arXiv abstract fetched; author list from recall)
- **BibKey:** yu2023musicagent

### ComposerX — ComposerX: Multi-Agent Symbolic Music Composition with LLMs
- **Who/where/when:** Qixin Deng, Qikai Yang, Ruibin Yuan, Yipeng Huang, Yi Wang, Xubo Liu, et al. (19 authors incl. Gus Xia, Emmanouil Benetos, Wenwu Wang, Wei Xue, Yike Guo); Rochester, CMU, HKUST, QMUL, Surrey; ISMIR 2024 (arXiv 2024)
- **Links:** https://arxiv.org/abs/2404.18081 ; https://github.com/lllindsey0615/ComposerX
- **What it is:** Six GPT-4 agents — Group Leader, Melody, Harmony, Instrument, Reviewer, Arrangement — collaborate to write polyphonic pieces in ABC notation from a text brief, with a review/revision loop.
- **Evidence:** 98.2% generation success; multi-agent preferred over single-agent (0.77 preference); 32.2% of outputs judged human-composed vs 55.4% for real human pieces; ~$0.80 per piece. Rater counts not reported.
- **Why it matters for the studio:** A pure-LLM, notation-native "compiler" with explicit role decomposition and a critic; a baseline the studio could extend with human annotations entering at any agent.
- **Tags:** [LLM-agent] [symbolic-generation] [notation] [music-as-code] [evaluation]
- **Verification:** verified (fetched arXiv HTML)
- **BibKey:** deng2024composerx

### RefinPaint — Music Proofreading with RefinPaint: Where and How to Modify Compositions Given Context
- **Who/where/when:** Pedro Ramoneda, Martín Rocamora, Taketo Akama; Universitat Pompeu Fabra, Sony CSL Tokyo; ISMIR 2024
- **Links:** https://arxiv.org/abs/2407.09099 ; https://github.com/ta603/RefinPaint ; https://refinpaint.github.io/
- **What it is:** Two-model loop for symbolic music: a *feedback/critic* model identifies which notes are weakest given context ("where to modify"), and an inpainting model resamples them ("how"); iterated as "proofreading" for both machine- and human-composed drafts. Users pick bars and how much content to keep.
- **Evidence:** Listening study with 15 annotators across 50/30/10% fragment sizes — RefinPaint preferred over baseline at all sizes; 4 amateur composers all reported improved drafts and time saved.
- **Why it matters for the studio:** Literally an AI *annotator*: it marks the score where it thinks changes are needed — the machine half of the annotate→edit loop and a model for AI→human communication on notation.
- **Tags:** [infilling] [editing] [annotation] [notation] [symbolic-generation] [evaluation]
- **Verification:** verified (fetched arXiv HTML)
- **BibKey:** ramoneda2024refinpaint

### ComposersAssistant2 — Composer's Assistant 2: Interactive Multi-Track MIDI Infilling with Fine-Grained User Control
- **Who/where/when:** Martin E. Malandro; Sam Houston State University; ISMIR 2024
- **Links:** https://arxiv.org/abs/2407.14700 ; https://github.com/m-malandro/composers-assistant-REAPER (CC BY 4.0)
- **What it is:** A REAPER plugin: select empty/partial regions in a multi-track MIDI project and a T5-like transformer infills them; controls include two rhythmic-conditioning modes, horizontal and vertical note-onset density, several pitch controls and "rhythmic interest."
- **Evidence:** Listening study found no significant quality difference between real music and pieces co-composed with the tool; objective metrics improved substantially over v1.
- **Why it matters for the studio:** A working, open, in-DAW example of fine-grained *constraint annotations* driving infilling — very close to the studio's intended primitive.
- **Tags:** [infilling] [DAW-plugin] [controllability] [symbolic-generation] [toolkit]
- **Verification:** verified (fetched arXiv abstract)
- **BibKey:** malandro2024composersassistant2

### Amuse — Amuse: Human-AI Collaborative Songwriting with Multimodal Inspirations
- **Who/where/when:** Yewon Kim, Sung-Ju Lee, Chris Donahue; KAIST, Carnegie Mellon; CHI 2025 (covered briefly here; another agent covers it in depth)
- **Links:** https://arxiv.org/abs/2412.18940 ; https://yewon-kim.com/amuse
- **What it is:** Chrome extension for Hookpad: images, text or audio "inspirations" → GPT-4o extracts keywords → chord progressions, filtered by rejection sampling against an LSTM harmonic prior trained on HookTheory; also a chord transcriber for audio.
- **Evidence:** Formative N=8 Hookpad/Aria users; within-subjects study N=10 songwriters (8 hobbyist, 2 professional) writing 8-bar choruses, Amuse+Aria vs Aria-only: significant gains in inspiration support (6.2 vs 4.6), controllability (5.8 vs 4.4), collaborative feel (5.8 vs 3.9), expressiveness, exploration (all p<0.05); no time difference. Listening study N=45: coherence on par with the prior, keyword relevance 58% preferred.
- **Why it matters for the studio:** Direct evidence that *multimodal annotations* (image/text/audio) can steer symbolic harmony while keeping the songwriter in control.
- **Tags:** [multimodal-input] [image] [HCI-study] [symbolic-generation] [creativity-support] [product]
- **Verification:** verified (fetched arXiv HTML)
- **BibKey:** kim2025amuse

### ReaLJam — ReaLJam: Real-Time Human-AI Music Jamming with Reinforcement Learning-Tuned Transformers
- **Who/where/when:** Alexander Scarlatos, Yusong Wu, Ian Simon, Adam Roberts, Tim Cooijmans, Natasha Jaques, Cassie Tarakajian, Cheng-Zhi Anna Huang; UMass Amherst, Mila, Google DeepMind; CHI EA 2025
- **Links:** https://arxiv.org/abs/2502.21267 ; demo https://storage.googleapis.com/genjam/index.html
- **What it is:** Live jamming interface over ReaLchords (RL-fine-tuned Transformer accompanist): the agent *anticipates* and displays upcoming chords in a waterfall view, with a commit window (fixed) and adaptive window (may change) — a protocol for balancing anticipatability and responsiveness.
- **Evidence:** N=6 experienced pianists/improvisers, ~1 h each, baseline + 8 conditions (chord display, metronome, model variant, temperature, commit time, silence). RL agents clearly outperformed pre-trained baselines; 5/6 wanted visible chord previews; preferences on other settings varied widely; agents ignored 4-bar phrase structure.
- **Why it matters for the studio:** A model of *AI intention display* (showing its plan before acting) and of per-user tunable protocol parameters; relevant if the studio adds live "play along with the arrangement" modes.
- **Tags:** [real-time] [accompaniment] [HCI-study] [mixed-initiative]
- **Verification:** verified (fetched arXiv HTML)
- **BibKey:** scarlatos2025realjam

### MusicAISandbox — Music AI Sandbox (Google DeepMind × YouTube Music AI Incubator)
- **Who/where/when:** Google DeepMind and YouTube; announced Nov 2023, expanded 24 Apr 2025 (Lyria 2 / Lyria RealTime)
- **Links:** https://deepmind.google/discover/blog/music-ai-sandbox-now-with-new-features-and-broader-access/
- **What it is:** Experimental toolkit with *Create* (describe sound/genre/mood, place lyrics on a timeline with tempo and key), *Extend* (continue uploaded or generated audio), and *Edit* (transform mood/genre/style by prompt or presets, fill gaps, create transitions); Lyria RealTime enables moment-to-moment interactive control. Co-designed with musicians in the YouTube Music AI Incubator (e.g., The Range, Isabella Kensington, Adrie, Sidecar Tommy).
- **Evidence:** Blog/industry; no peer-reviewed user study published as of this writing.
- **Why it matters for the studio:** The most prominent industry attempt at *musician-co-designed* generative tooling whose verbs (create/extend/edit on a timeline) mirror the studio's loop, but audio-first and closed.
- **Tags:** [product] [audio-generation] [editing] [real-time] [co-creation-framework]
- **Verification:** verified (fetched DeepMind blog)
- **BibKey:** googledeepmind2025sandbox

### JamBot — The Jam_bot, a Real-Time System for Collaborative Free Improvisation with Music Language Models
- **Who/where/when:** Lancelot Blanchard, Perry Naseck, Stephen Brade, Kimaya Lecamwasam, Jordan Rudess, Cheng-Zhi Anna Huang, Joseph Paradiso; MIT Media Lab (with Dream Theater keyboardist Jordan Rudess); ISMIR 2025
- **Links:** https://doi.org/10.5281/zenodo.17706584
- **What it is:** Real-time system that listens to a human improviser and responds with a music language model, developed with and performed by a virtuoso keyboardist (Rudess), exploring free improvisation rather than chord-following accompaniment.
- **Evidence:** Performance-based evaluation and practitioner reflection (details not fetched).
- **Why it matters for the studio:** A 2025 data point on *AI as improvising colleague* built with an expert performer — relevant to the founder's Nord Stage practice and to "jam with the arrangement" features.
- **Tags:** [real-time] [accompaniment] [expression-performance] [HCI-study]
- **Verification:** partial (title/authors from ISMIR 2025 proceedings list; abstract not fetched)
- **BibKey:** blanchard2025jambot

### RhapsodyRefiner — Supporting Creative Ownership through Deep Learning-Based Music Variation
- **Who/where/when:** Stephen James Krol, Maria Teresa Llano, Jon McCormack; Monash University, University of Sussex; arXiv 2025 (2509.25834)
- **Links:** https://arxiv.org/abs/2509.25834
- **What it is:** "Rhapsody Refiner": a standalone tool that takes the musician's own MIDI and produces *variations* by selectively masking notes and re-predicting them with MusicBERT under user-set parameters; deliberately depends on strong human input and does not compose from scratch.
- **Evidence:** Four-week ecological study with 8 practising musicians (songwriters, producers, educators, instrumentalists): tutorial, independent use, journals, logs, semi-structured interviews, thematic analysis. Findings: valued for "moments, not whole ideas"; dependence on the musician's input promoted ownership of process and artefact; participants rejected automatic completion; imperfection/randomness prompted creative problem-solving.
- **Why it matters for the studio:** Strongest recent evidence for the founder's stance — AI that transforms *authored* material preserves ownership; also a rare longitudinal (in-the-wild) study design to emulate.
- **Tags:** [HCI-study] [editing] [symbolic-generation] [creativity-support] [evaluation]
- **Verification:** verified (fetched arXiv HTML)
- **BibKey:** krol2025ownership

---

## C. Empirical studies of musicians' perceptions and needs

### MachineFolk — Machine learning research that matters for music creation: A case study (folk-rnn)
- **Who/where/when:** Bob L. Sturm, Oded Ben-Tal, Úna Monaghan, Nick Collins, Dorien Herremans, Elaine Chew, Gaëtan Hadjeres, Emmanuel Deruty, François Pachet; KTH, Kingston, Cambridge, Durham, SUTD, QMUL, Sony CSL; Journal of New Music Research 48(1):36–55, 2019
- **Links:** https://doi.org/10.1080/09298215.2018.1515233 ; https://folkrnn.org ; album *Let's Have Another Gan Ainm* (2018)
- **What it is:** Case study of folk-rnn (LSTM over ABC-notation Irish/Scottish tunes) used by traditional and contemporary musicians and composers over several years — concerts, an album, a musical — to ask what ML research "matters" for music creation.
- **Evidence:** Practitioner accounts: generated tunes are *raw material* requiring editing, arrangement and performance; musicians valued the tool as a source of unexpected ideas but cared about the tradition's social meaning; the paper argues for evaluating ML by its usefulness to practice rather than by likelihood.
- **Why it matters for the studio:** Notation-native (ABC) generation actually used by working musicians; validates "AI output is material to edit," and the community-attitude concerns the studio must respect.
- **Tags:** [HCI-study] [symbolic-generation] [notation] [ethics-legal] [evaluation]
- **Verification:** verified (Crossref metadata; content from companion Arts paper)
- **BibKey:** sturm2019machinefolk

### AIMusicOpenQuestions — Artificial Intelligence and Music: Open Questions of Copyright Law and Engineering Praxis
- **Who/where/when:** Bob L. T. Sturm, Maria Iglesias, Oded Ben-Tal, Marius Miron, Emilia Gómez; KTH, EC Joint Research Centre, Kingston, UPF; *Arts* 8(3):115, 2019
- **Links:** https://doi.org/10.3390/arts8030115
- **What it is:** Uses folk-rnn to examine (1) EU copyright questions (authorship of AI output, training on protected works, accidental reproduction) and (2) engineers' responsibilities (document limitations; evaluate for fairness/accountability/transparency, not just accuracy).
- **Evidence:** Legal analysis plus practitioner testimony: musicians treated output as raw material; concerns centred on disrupting traditions rather than job loss; some gained regular performance work from AI-assisted repertoire.
- **Why it matters for the studio:** Frames provenance logging and consented training data as engineering duties; supports human-authored-input designs as the clearest path to copyrightable output.
- **Tags:** [ethics-legal] [HCI-study] [symbolic-generation]
- **Verification:** verified (fetched MDPI page)
- **BibKey:** sturm2019openquestions

### SonyCSLPractice — On the Development and Practice of AI Technology for Contemporary Popular Music Production
- **Who/where/when:** Emmanuel Deruty, Maarten Grachten, Stefan Lattner, Javier Nistal, Cyran Aouameur; Sony CSL Paris; TISMIR 5(1), 2022
- **Links:** https://doi.org/10.5334/tismir.100
- **What it is:** Reflection on 6–18-month collaborations with six professional acts (Niro, Twenty9, Hyper Music, Uèle Lamore, Whim Therapy, Donn Healy) using Sony CSL prototypes (DrumNet, BassNet, LeadNet, DrumGAN, Notono, Planet Drums, ResonanceEQ, ProfileEQ); argues in-studio popular-music practice is audio-first and that audio tools fit it better than MIDI tools.
- **Evidence:** Qualitative thematic analysis of interviews and workflow documentation. Patterns: "pull" (explicit queries) over "push" (unsolicited suggestions); *priming* on the artist's own audio; generate-and-curate; latent-space navigation; exploiting artefacts ("AI, the new analog?"); repurposing tools. Friction: leaving the DAW, lack of recognisable control, need for visualisation. Proposes validation by workflow integration, task simplification, stimulation, identifiable contribution and commercial viability.
- **Why it matters for the studio:** The most in-depth professional-producer study; its "pull, prime on my material, keep me in the DAW" findings are design constraints — and its audio-first claim is the counterpoint the symbolic-first studio must answer (e.g., by rendering stems).
- **Tags:** [HCI-study] [audio-generation] [DAW-plugin] [controllability] [evaluation]
- **Verification:** verified (fetched TISMIR page)
- **BibKey:** deruty2022sonycsl

### Newman2023 — Human-AI Music Creation: Understanding the Perceptions and Experiences of Music Creators for Ethical and Productive Collaboration
- **Who/where/when:** Michele Newman, Lidia J. Morris, Jin Ha Lee; University of Washington iSchool; ISMIR 2023
- **Links:** https://doi.org/10.5281/zenodo.10265227 ; https://archives.ismir.net/ismir2023/paper/000008.pdf
- **What it is:** Case studies of how professional creators perceive and use AI for melody, harmony, lyrics and mixing.
- **Evidence:** N=6 professionals (classical/jazz composer, film/game composer, interactive-media composer, electroacoustic composer, sound artist, DJ; 5+ years experience; 5 active AI users, 1 sceptic), 60–90 min semi-structured interviews, two-coder inductive–deductive coding (ATLAS.ti). Twelve categories in two themes (AI as collaborator; democratisation). Design implications: preserve creative control (AI for ideation/exploration, not intentional decisions); interoperability (MIDI/WAV/MusicXML export or in-software integration); separate "influences" (ideas) from "mechanisms" (housekeeping); prefer open-source, explainable models over black boxes; role of AI shifts with context.
- **Why it matters for the studio:** Explicitly asks for MusicXML/MIDI interoperability, open models and control preservation — a near-verbatim endorsement of the studio's symbolic-first, open-source stance.
- **Tags:** [HCI-study] [ethics-legal] [co-creation-framework] [notation]
- **Verification:** verified (fetched ISMIR PDF)
- **BibKey:** newman2023perceptions

### HAISP — HAISP: A Dataset of Human-AI Songwriting Processes from the AI Song Contest (and its 2025 expansion)
- **Who/where/when:** Lidia J. Morris, Rebecca Leger, Michele Newman, John Ashley Burgoyne, Ryan Groves, Natasha Mangal, Jin Ha Lee; University of Washington, Fraunhofer IIS, University of Amsterdam, AI Song Contest; ISMIR 2024; expansion: Morris, Newman, Tang, Singh, Vélez Vásquez, Leger, Lee, ISMIR 2025
- **Links:** https://doi.org/10.5281/zenodo.14877357 ; https://doi.org/10.5281/zenodo.17706323
- **What it is:** Coded dataset of the *process* descriptions submitted by AI Song Contest teams (34 submissions from 2023; extended with 2024 entries) — which tools were used for which task, how decisions were made, what control creators retained — rather than the songs.
- **Evidence:** 2025 paper compares 2023 vs 2024 cohorts: shifts in collaboration patterns, differences in creative agency between general-purpose systems (e.g., Suno/ChatGPT-style) and fine-tuned/custom tools, and design recommendations for songwriting platforms.
- **Why it matters for the studio:** The only longitudinal, coded corpus of real human–AI songwriting workflows; a source for a taxonomy of tasks and control points the compile loop should cover.
- **Tags:** [dataset] [HCI-study] [co-creation-framework] [structure]
- **Verification:** verified (fetched Zenodo records)
- **BibKey:** morris2024haisp

### ReflectionAIMusic — Reflection Across AI-based Music Composition
- **Who/where/when:** Corey Ford, Ashley Noel-Hirst, Sara Cardinale, Jackson Loth, Pedro Sarmento, Elizabeth Wilson, Lewis Wolstanholme, Kyle Worrall, Nick Bryan-Kinns; QMUL, York, UAL Creative Computing Institute; ACM Creativity & Cognition 2024
- **Links:** https://doi.org/10.1145/3635636.3656185
- **What it is:** Eight composer-researchers each composed with a different AI tool (Markov chains to VAEs), pausing hourly to reflect on screenshots of their work; first-person accounts, interviews and questionnaires analysed for patterns of *reflection*.
- **Evidence:** Composers reflected mostly on future directions while *curating* AI-generated content; curation is where creative decisions concentrate; supports designing for reflection (history, comparison) rather than only generation.
- **Why it matters for the studio:** Suggests the compile loop should surface *history and alternatives* to support reflection, and that annotation moments are reflective moments worth capturing.
- **Tags:** [HCI-study] [creativity-support] [evaluation]
- **Verification:** verified (Semantic Scholar abstract)
- **BibKey:** ford2024reflection

### NoviceProduction — Exploring the Collaborative Co-Creation Process with AI: A Case Study in Novice Music Production
- **Who/where/when:** Yue Fu, Michele Newman, Lewis Going, Qiuzi Feng, Jin Ha Lee; University of Washington iSchool; ACM DIS 2025
- **Links:** https://arxiv.org/abs/2501.15276
- **What it is:** 10-week capstone course in which three teams of undergraduates with little production experience each produced three tracks using AI tools; artefact review plus interviews.
- **Evidence:** N=9 interviewed (of 20), 55–70 min each, reflexive thematic analysis. AI accelerated ideation but compressed preparation; a new "collaging and refinement" stage emerged to integrate heterogeneous AI outputs; AI mediated group dynamics (blunter critique of AI output); participants prized human emotional expression and consciously retained control.
- **Why it matters for the studio:** "Collaging and refinement" is precisely the assembly step the founder calls *compile*; the study shows novices need tooling for it.
- **Tags:** [HCI-study] [education] [co-creation-framework]
- **Verification:** verified (fetched arXiv HTML)
- **BibKey:** fu2025novice

### TTMProducers — AI-Assisted Music Production: A User Study on Text-to-Music Models
- **Who/where/when:** Francesca Ronchini, Luca Comanducci, Simone Marcucci, Fabio Antonacci; Politecnico di Milano; CMMR 2025 (17th Int. Symposium on Computer Music Multidisciplinary Research), London (arXiv 2509.23364)
- **Links:** https://arxiv.org/abs/2509.23364
- **What it is:** Custom web interface pairing MusicGen (text-to-music) with HT-Demucs (stem separation); producers make music with it for an hour.
- **Evidence:** N=17 producers from 7 countries (mixed experience); pre-survey, recorded session, Likert questionnaire, interviews, thematic analysis. TTM seen as *inspiration*, not production-ready: 94% would use it in ideation; barriers were intent–output misalignment, tempo/key/beat alignment, limited editability; ethical worries about copyright, compensation and homogenisation from Western-centric data.
- **Why it matters for the studio:** Quantifies why prompt-to-audio fails as a composition paradigm (alignment, editability) — the founder's critique of text-to-song, with data.
- **Tags:** [HCI-study] [text-conditioning] [audio-generation] [ethics-legal]
- **Verification:** verified (fetched arXiv PDF)
- **BibKey:** ronchini2025ttm

### ArtistPositions — Artist-led positions: Holly Herndon's Holly+ and Spawning; Dadabots
- **Who/where/when:** Holly Herndon & Mat Dryhurst (Holly+, 2021; Spawning / "Have I Been Trained?", 2022–); CJ Carr & Zack Zukowski (Dadabots; "Generating Albums with SampleRNN to Imitate Metal, Rock, and Punk Bands," MUME 2018, arXiv 1811.06633)
- **Links:** https://holly.plus ; https://spawning.ai ; https://dadabots.com ; https://arxiv.org/abs/1811.06633
- **What it is:** Practising artists' models of consent and co-creation: Holly+ offers a voice model of Herndon under a DAO-governed licence so others can *co-create with her identity*; Spawning builds consent/opt-out infrastructure for training data; Dadabots run raw-audio models as a "band," publishing 24/7 generated streams and arguing for AI as a new genre/instrument rather than a replacement.
- **Evidence:** Artist practice and public writing; no formal studies.
- **Why it matters for the studio:** Articulates what leading artists want from AI — consent, identity control, and AI as instrument — useful positioning for an open, composer-centred studio.
- **Tags:** [ethics-legal] [product] [audio-generation] [history]
- **Verification:** partial (well-known projects; pages not fetched in this session)
- **BibKey:** herndon2021hollyplus

---

## D. Evaluation, explainability, and interaction-paradigm anchors

### YangLerch — On the evaluation of generative models in music
- **Who/where/when:** Li-Chia Yang, Alexander Lerch; Georgia Tech Center for Music Technology; Neural Computing and Applications 32:4773–4784, 2020 (online 2018)
- **Links:** https://doi.org/10.1007/s00521-018-3849-7 ; https://github.com/RichardYang40148/mgeval
- **What it is:** Proposes musically informed objective metrics (pitch/rhythm feature distributions; absolute measures and relative measures via KL divergence and overlap area against a reference set) so that generative-model papers can report reproducible, comparable results when full listening studies are infeasible.
- **Evidence:** Demonstrated on symbolic generation systems; the mgeval toolkit is widely used.
- **Why it matters for the studio:** Complements HCI measures with artefact-level metrics for regression-testing the compiler (e.g., does an annotation move feature distributions as intended?).
- **Tags:** [evaluation] [symbolic-generation] [toolkit]
- **Verification:** verified (fetched Springer page)
- **BibKey:** yang2020evaluation

### XAIArts — Exploring XAI for the Arts: Explaining Latent Space in Generative Music
- **Who/where/when:** Nick Bryan-Kinns, Berker Banar, Corey Ford, Courtney N. Reed, Yixiao Zhang, Simon Colton, Jack Armitage; QMUL; XAI4Debugging workshop @ NeurIPS 2021 (arXiv 2023); follow-ups: Bryan-Kinns et al., "Exploring Variational Auto-Encoder Architectures, Configurations, and Datasets for Generative Music Explainable AI," Machine Intelligence Research 2024; Bryan-Kinns, "Reflections on Explainable AI for the Arts (XAIxArts)," Interactions 2024
- **Links:** https://arxiv.org/abs/2308.05496
- **What it is:** Regularises the first four latent dimensions of MeasureVAE to correspond to rhythmic complexity, note range, note density and average interval jump, and builds a real-time interface + visualisations so users can see and manipulate what each dimension does.
- **Evidence:** Technical demonstration; later user studies in the XAIxArts line (2023–2024 workshops at C&C) evaluate explanations with musicians.
- **Why it matters for the studio:** Shows how to make generative controls *legible* — semantic knobs plus visual explanations — a requirement for annotations to have predictable effects.
- **Tags:** [controllability] [evaluation] [symbolic-generation] [co-creation-framework]
- **Verification:** verified (fetched arXiv PDF)
- **BibKey:** bryankinns2021xai

### CoExplorer — Designing Deep Reinforcement Learning for Human Parameter Exploration
- **Who/where/when:** Hugo Scurto, Bavo Van Kerrebroeck, Baptiste Caramiaux, Frédéric Bevilacqua; IRCAM/STMS, Sorbonne Université; ACM Transactions on Computer-Human Interaction 28(1), 2021 (arXiv 2019)
- **Links:** https://arxiv.org/abs/1907.00824 ; https://doi.org/10.1145/3414472
- **What it is:** Co-Explorer: a deep-RL agent explores a synthesiser's high-dimensional parameter space and adapts to the sound designer's *like/dislike feedback*, alternating between autonomous exploration and user-directed moves — a critique/feedback-loop paradigm rather than direct manipulation.
- **Evidence:** User-centred design with observational studies, agent-behaviour tests and a workshop evaluation with professional sound designers; positive reception; diverse exploration behaviours; design guidelines for "co-exploration."
- **Why it matters for the studio:** A concrete design for *feedback-as-steering* (thumbs up/down on compiled results shaping the next compile) with musicians in the loop.
- **Tags:** [HCI-study] [controllability] [mixed-initiative] [real-time]
- **Verification:** partial (arXiv abstract fetched; N and TOCHI DOI from recall)
- **BibKey:** scurto2021coexplorer

### Alternatives — Alternatives, history and branching in creative tools (Side Views; Juxtapose; Subjunctive Interfaces)
- **Who/where/when:** Michael Terry & Elizabeth Mynatt, "Side Views: Persistent, On-Demand Previews for Open-Ended Tasks," UIST 2002; Björn Hartmann, Loren Yu, Abel Allison, Yeonsoo Yang, Scott Klemmer, "Design as Exploration: Creating Interface Alternatives through Parallel Authoring and Runtime Tuning" (Juxtapose), UIST 2008; Aran Lunzer & Kasper Hornbæk, "Subjunctive Interfaces: Extending Applications to Support Parallel Setup, Viewing and Control of Alternative Scenarios," ACM TOCHI 14(4), 2008
- **Links:** https://doi.org/10.1145/571985.571996 ; https://doi.org/10.1145/1449715.1449724 ; https://doi.org/10.1145/1314683.1314685
- **What it is:** The HCI lineage for working with *multiple alternatives in parallel*: previews of possible outcomes before committing (Side Views), parallel code/design variants with linked editing and runtime tuning (Juxtapose), and side-by-side alternative scenarios (Subjunctive Interfaces). Terry & Mynatt's "Recognizing Creative Needs in User Interface Design" (C&C 2002) frames near-term experimentation, variation and evaluation as core creative needs.
- **Evidence:** Lab studies in each paper showing users explore more alternatives and compare more readily; conceptual foundation for later "version tree" tools in creative software.
- **Why it matters for the studio:** Anchors the version-tree / branching requirement of the compile loop (each annotate→compile produces alternatives that must be compared, kept, or merged) in established HCI results; complements Cococo's "multiple alternatives" and Calliope's batch+rank.
- **Tags:** [creativity-support] [history] [co-creation-framework]
- **Verification:** partial (canonical works; DOIs from recall, not fetched this session)
- **BibKey:** terry2002sideviews

### HookpadAria — Hookpad Aria (Hooktheory)
- **Who/where/when:** Hooktheory (Chris Anderson, Dave Carlton, Ryan Miyakawa); commercial feature in Hookpad, 2023–
- **Links:** https://www.hooktheory.com/hookpad/aria
- **What it is:** In-editor AI assistant in the Hookpad chord/melody sketching tool that proposes chords and melodies conditioned on the current sketch, trained on the HookTheory (TheoryTab) corpus of user-annotated pop songs; used as the baseline condition in Amuse (CHI 2025).
- **Evidence:** No published study by Hooktheory; Amuse's formative interviews (N=8 Aria users) report it is valued for contextual suggestions but lacks multimodal inspiration input.
- **Why it matters for the studio:** A shipping example of symbolic, lead-sheet-level co-creation used by songwriters — and the closest commercial analogue to the founder's chord/lead-sheet workflow.
- **Tags:** [product] [symbolic-generation] [notation] [accompaniment]
- **Verification:** partial (existence and role confirmed via Amuse paper; product page not fetched)
- **BibKey:** hooktheory2023aria

---

## Interaction-paradigm summary (for the taxonomy)

| Paradigm | Exemplars in this cluster | Evidence notes |
|---|---|---|
| Turn-taking / alternating | Morai Maker (games), FlowComposer, Cococo, Calliope, RefinPaint | Interruptible turns and region-scoped regeneration preserve ownership; role preference is individual (Guzdial 2019). |
| Simultaneous / real-time | Drawing Apprentice, Notochord, ReaLJam, Jam_bot, Piano Genie | Needs intention display (ReaLJam commit/adaptive windows) and sub-event control (Notochord). |
| Task-divided | AI Song Contest teams, ComposerX agents, Micchi et al. | Humans keep structure/arrangement/verse; AI proposes parts; assembly ("collaging", Fu 2025) is the bottleneck. |
| Direct manipulation / semantic knobs | Cococo sliders, XAI MeasureVAE, MidiMe, Composer's Assistant 2 controls | Legible, few, musically named dimensions outperform temperature-only (MMM-C). |
| Conversational / LLM-orchestrated | COSMIC, Loop Copilot, MusicAgent, ComposerX | Good for ideation and orchestration; weak on fine musical control; users ask for DAW integration and editable intermediates. |
| Example-based steering | Cococo similarity slider, Music-Creation-by-Example, MidiMe, Amuse (audio/image), Sketch2Sound (vocal imitation) | Natural for reference-thinking musicians; works for harmony, style, timbre. |
| Critique / feedback loops | Co-Explorer, RefinPaint critic, Reviewer agent in ComposerX | Feedback-as-steering and AI-side critique are the least explored (COFI gap) and most promising for AI→human annotation. |
| AI as instrument vs collaborator | Piano Genie, Wekinator (instrument); Cococo, Calliope, Rhapsody Refiner (collaborator) | Ownership stays highest when the human authors the material the AI transforms (Krol 2025; Louie 2020). |
| Alternatives / history / branching | Side Views, Juxtapose, Subjunctive Interfaces; Cococo alternatives; Calliope batch+rank; Ford 2024 reflection | Under-implemented in music AI; a clear differentiator for a compile-loop studio. |

## Cross-cluster pointers
- Infilling/editing models (Coconet, MMM, Composer's Assistant 2, RefinPaint, Instruct-MusicGen ISMIR 2025, VampNet) → infilling/editing cluster.
- LLM agents (MusicAgent, ComposerX, Loop Copilot; also ByteComposer, ChatMusician) → LLM-agent cluster.
- Multimodal steering (Amuse; Sketch2Sound — García, Seetharaman, Kumar, Pardo, ICASSP 2025, arXiv 2412.08550; Expotion ISMIR 2025) → multimodal-input cluster.
- Real-time accompaniment (ReaLchords/ReaLJam, Notochord, Jam_bot, SongDriver) → real-time/accompaniment cluster.
- Ethics/copyright (Sturm 2019; Newman 2023; HAISP; MusGO ISMIR 2025 openness framework) → ethics-legal cluster.
- Products (Magenta Studio, MMM4Live, Music AI Sandbox, Hookpad Aria, Suno/Udio) → product cluster.
