# Maestro

**An open research program on human-centered AI for music composition.**

> The composer stays at the centre. The machine compiles.

Most music AI takes a sentence and returns a finished master. That is the wrong shape for
someone who actually writes music: a prompt is a narrow channel for musical intent, and the
output arrives as an opaque mixdown with nothing to grab hold of.

Maestro studies the opposite arrangement. The composer authors and marks up the material, and
the model **compiles** a fuller realization under those marks — then the composer edits,
re-annotates, and recompiles, at the granularity of a bar or a part:

```
compose → annotate → compile → edit → annotate → compile → …
```

*Compile* is meant literally: a source the human owns, intermediate representations that can be
inspected, a repeatable build, and a build log that says what the machine did with each
instruction.

**→ [maestro site](https://henryatharvard.github.io/maestro/)**

---

## What's here

This repository begins with a survey of where the field actually stands, because the argument
above is only worth making if it survives contact with the literature.

| | |
|---|---|
| **[Literature review](https://henryatharvard.github.io/maestro/survey/literature-review.html)** | 43,900 words · 398 works cited · thirteen sections following the loop |
| **[Taxonomy](https://henryatharvard.github.io/maestro/survey/taxonomy.html)** | 49 nodes, 10 coding dimensions — the frame the review follows |
| **[Annotated bibliography](https://henryatharvard.github.io/maestro/survey/annotated-bibliography.html)** | 394 records with evidence and verification level |
| **[references.bib](research/references.bib)** | 398 BibTeX entries; every key resolves through pandoc citeproc |

Corpus: **463 annotated entries, 1957–2026**, assembled across eight research clusters in
September 2026.

### Working material

- `research/notes/01–08*.md` — the eight raw research clusters. **This is the ground truth.**
  Every claim in the review traces to an entry here, and each entry carries a verification
  level: *verified* (a primary source was fetched), *partial* (secondary sources only), or
  *unverified* (recall, not re-confirmed). 373 verified, 85 partial, 5 unverified.
- `research/taxonomy-map.{md,csv}` — every entry assigned to a primary node (462 hand-coded).
- `research/VERIFICATION.md` — an independent pass re-checking 34 high-stakes claim clusters
  against primary sources. 16 corrections, all applied.
- `research/AUDIT.md` — internal-consistency audit: claim traceability, hedging discipline,
  contradictions, redundancy, citation hygiene. 70 findings.
- `research/CHANGELOG.md` — exactly which of the 56 fixes were applied, and which were left.
- `research/bib/` — per-cluster BibTeX before merging.

## Five findings the survey establishes

1. **Infilling under hard constraints — not generation from scratch — is the primitive that
   implements the loop.** Mature since Coconet (2017), which framed it as modelling how
   composers "write music in a nonlinear fashion, scribbling motifs here and there, often
   revisiting choices previously made." The best deployment evidence is Hookpad Aria's: ~23%
   of 318,000 span-level suggestions accepted by ~3,000 users inside a notation editor.
2. **Interface steerability moves control and ownership at least as much as model capability
   does.** The two controlled studies that varied both found the gains complementary, not
   substitutable.
3. **Every input modality that works routes through an editable symbolic representation.**
   Straight-to-audio is impressive and uncorrectable.
4. **The annotation layer is the field's genuine white space.** The pieces exist — MEI and
   Dezrann anchoring, analysis models that propose labels, a converged control vocabulary,
   ExpressEdit's reference grammar — and have never been assembled for music.
5. **Symbolic-first, human-authored work sits on materially better legal ground** than
   prompt-to-audio, and licence-clean symbolic training data genuinely exists.

## Open directions

Twelve gaps, each naming the nearest prior art so none starts from nothing —
**[full list on the site](https://henryatharvard.github.io/maestro/#directions)**. The ones
most worth someone's time:

- **G1** Annotations as a compilable instruction set on notation *(S2.4 — 4 entries in the
  corpus, none of them music)*
- **G2** A lossless bridge between an LLM-friendly text IR and engraving-grade notation
  *(no verified system generates MusicXML or MEI natively)*
- **G5** A return channel: the compiler's build log *(S4.4 — 2 entries)*
- **G7** Composer-controllable audio rendering *(no commercial system takes MIDI or chords as
  a generation condition)*

Take them. They are worth more to the field than to any one person.

## Link previews

`index.html` and the three survey pages carry a full Open Graph + Twitter card set, so links
unfurl properly in iMessage, WhatsApp, Signal, Slack, Discord, LinkedIn and X.

- **Card image:** `assets/og-cover.png` — 1200×630, 62 KB (comfortably under WhatsApp's limit).
- **Source:** `assets/og-image.html`. Icons come from `assets/icon.html`.
- **Regenerate:** `./build-og.sh` (needs `npm i playwright` and ImageMagick).

Two things to know. `og:image` **must be an absolute URL** — scrapers do not resolve relative
paths — so it is hard-coded to `https://henryatharvard.github.io/maestro/`; change it in
`index.html` and `assets/doc.template.html` if the site ever moves. And the shipped PNG was
rendered without network access, so it uses Charter rather than Newsreader; re-running
`./build-og.sh` on a machine that can reach Google Fonts produces the card in the real faces.

**Previews are cached hard.** After the first share, iMessage and WhatsApp will keep serving the
old card. To force a refresh: share `...maestro/?v=2`, or clear the cache — Facebook's
[sharing debugger](https://developers.facebook.com/tools/debug/) re-scrapes for most platforms,
and [opengraph.xyz](https://www.opengraph.xyz/) is a quick way to see what a scraper sees.

## Building the site

The site is plain HTML with no build step for the landing page. The document pages are rendered
from the markdown in `research/` with pandoc:

```bash
./build.sh          # research/*.md → survey/*.html   (requires pandoc ≥ 3)
```

`assets/site.css` carries the shared identity; `assets/doc.template.html` is the pandoc
template. GitHub Pages serves from the repository root (`.nojekyll` is present so nothing is
filtered).

To regenerate the research artefacts themselves from the source notes:

```bash
cd research
python3 merge_bib.py       # bib/*.bib     → references.bib + bib_aliases.json
python3 build_map.py       # notes/*.md    → taxonomy-map.{md,csv}
python3 build_annobib.py   # notes/*.md    → annotated-bibliography.md
```

## Contributing

**Corrections are the most valuable contribution.** Every claim is traceable to a source note,
so a correction can be checked rather than argued. Open an issue with the section, the claim as
written, and the primary source that contradicts it.

Also welcome: works the survey missed (say which taxonomy node they belong to), disagreement
with the gap analysis, and replication of anything in §10.

## Citing

See [`CITATION.cff`](CITATION.cff).

```bibtex
@misc{tan2026maestro,
  author = {Tan, Henry},
  title  = {Maestro: Human-Centered {AI} for Composition --- A Literature Review and Taxonomy},
  year   = {2026},
  url    = {https://henryatharvard.github.io/maestro/},
  note   = {Survey of 463 works, 1957--2026}
}
```

## Licence

Prose, survey and research notes: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
Code, scripts and templates: Apache 2.0 (see [`LICENSE`](LICENSE)). Full detail: [`LICENSE-TEXT.md`](LICENSE-TEXT.md).

---

Henry Tan · Harvard University · survey compiled September 2026
