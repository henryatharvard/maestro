# Changelog — fixes applied after the QA passes

Two independent passes ran against the assembled review: `VERIFICATION.md` (external, primary-source
re-checking of high-stakes claims) and `AUDIT.md` (internal consistency against `notes/`).
**56 fixes were applied.** Below is what changed and what was deliberately left.

## Substantive corrections (from VERIFICATION.md)

| # | Fix |
|---|---|
| C1 | Dynamic HumTrans next-best baseline corrected 0.564 → **0.604** (MIR-ST500); "a large gain" softened to "real but modest" (~11% relative). |
| C2 | The "single-digit vs 0.67" humming comparison **removed** — the single-digit F1s were scored against HumTrans's *defective* onset labels. Now: off-the-shelf 0.43–0.60 vs purpose-built 0.67 on relabelled data. Fixed in §4.6 and §13.1 G8. The argument (interactive correction is mandatory) survives. |
| C3 | Roman-numeral accuracy corrected from "45–50% full labels" to **51% (AugmentedNet) / 62% (RNBert), key 82–83%** — the review had tracked only the weakest number. §1.4 and §4.6. |
| C4 | **Thesis-bearing.** Expressive Communication does *not* rank interface above model; its finding is symmetric. §3.2 and §13.3 rewritten to "each independently improved … complementary rather than substitutes." |
| C5 | GEMA v. Suno: the January 2026 hearing was **postponed** over a recusal motion and heard 9 March 2026. Judgment date (31 July 2026) confirmed correct. |
| C6 | Finale quotation was not verbatim — replaced with the actual press-release wording; crossgrade specified as Dorico **Pro** (list $579). |
| C7 | music21 requires Python **3.11**, not 3.12. |
| C8 | "Human-AI Resonance group" / "HAI-Res lab" **has no primary MIT source** — replaced with Huang's attested title and appointment. Two places. |
| C9 | MIT MTC: the ten-student figure is the **2026–27 intake**; founding cohort was five. Showcase dated 13 May 2026. |
| C10 | Magenta RealTime 2 Max/PD/SuperCollider bindings **unverified** — clause removed. |
| C11 | MMM-C SUS range corrected 73.8–75.7 → **71.4–75.7**. Two places. |
| C12 | Google/Producer.ai: acquisition (24 Feb 2026) and Flow Music rebrand (April 2026, trade press) separated. |
| C13 | Deezer fraud figure: "**up to** 85%… identified in **2025** and demonetised", not "approximately 85% are". |
| C14 | Verovio current release 6.2.0 → **6.2.1**. |
| C16 | Suno download caps re-marked as **reported** (no primary source; release notes are silent). |

C15 was a false alarm in the verification brief itself (Cococo's author list was already correct).

## Claim-drift and unsupported-primacy fixes (from AUDIT.md)

- **Four primacy claims no source makes** scoped to the corpus or cut: Music Transformer as "first neural lead-sheet→piano" (§6.5), Udio as "first mainstream audio inpainting" (§7.1), Magenta RealTime 2 as "first open audio model pairing audio with transcribed symbolic data" (§7.2), FMD as "first standard symbolic distributional metric" (§10.4).
- **§2.3 contradicted §6.2/§13.1** on the earliest notation-surface generative feature — Hookpad Aria now scoped to the first *commercial* one, with DeepBach's 2017 MuseScore plugin credited.
- **"The largest gap" was awarded three times to three referents.** Now reserved for S2.4 (the annotation layer); §8.2 is "the largest gap on the *editing* side" and §10.1 "the largest measured control deficit."
- RefinPaint re-attributed as a **UPF–Sony CSL Tokyo** collaboration (two of three authors are UPF).
- The Harmonix mission quote re-attributed to **Machover**, not Egozy.
- Dai & Dannenberg's structure corpus specified as **Chinese pop** (load-bearing for a claim about "human pop").
- Composer's Assistant licence result softened from "proves" to "shows."

## Hedging discipline (11 breaches closed)

Added "reportedly"/"per the project page"-style hedges, or removed invented precision, for: Lakh MIDI's file count and licence, MAESTRO's performance count, the EU AI Act dates, the **ELVIS Act effective date** (absent from the notes — removed), Goldmedia's **fabricated day precision** ("30 January" → "January"), CISAC's 24% ("a modelled 24 per cent"), Harmonix unit sales, Vercoe's Synthetic Performer, Eck & Schmidhuber, and the RNN-RBM benchmark-provenance claim.

## Double-counting risk (founder's own seed — flagged, not buried)

`oros2026helpthathurts` (SSRN, unresolvable DOI) shares authors, finding and period with the CMU
poster study `oros2026cmu`. The review no longer presents them as mutually corroborating: §10.6 now
says it is "plausibly the same experiment written up," and §11.5 no longer frames it as a
*classroom* study (nothing in the notes supports student participants).

## Contradictions between sections (9 resolved)

MusicTheoryBench's GPT-4 figure now hedged consistently in §6.6 and §10.6 · ACE-Step latency split
by version in Table 7.1 (1.5 turbo <2 s; 1.0 ~20 s) · Hookpad Aria's derived "nine months" replaced
with the actual reporting period · Amuse's keyword-relevance win restored to §10.1 so its null
conclusion is not overstated · SingSong's ~66% margin stated once and marked reported · §9.5's
participant tally no longer counts ReaLchords' listening panel as interactive participants.

## Redundancy (~430 words recovered)

Cut to cross-references: §4.4's text-to-symbolic paragraph (duplicated §6.3) · §3.2's Design Space
passage (duplicated §9.4) · Hookpad Aria's telemetry, stated in full four times, now full only in
§10.3 (E3) · §8.2's RefinPaint/Composer's Assistant/FlowComposer repeats, which had *announced*
their own cross-reference and then repeated anyway · §8.1's ExpressEdit study figures (kept in §5.4).

## Companion-file fixes

- `references.bib`: dropped the duplicate VexFlow record (`cheppudira2010vexflow`); 399 → **398 records, all now cited**.
- `taxonomy-map.csv`: Composer's Assistant v1 recoded F4 → **S3.2**; the "ProductTable" summary row dropped (464 → **463** entries); four junk values in the `verification` column repaired. All fixed in `build_map.py`, so the map regenerates correctly.
- `taxonomy.md`: thinnest-node list completed (S1.5 and S5.2 were omitted); entry count corrected to 463.

## Deliberately left

- **§7's subsection order** (S3.9 → S3.8 → S3.10) is out of taxonomy order on purpose: the paradigm being inverted is introduced before the rendering path that answers it.
- **Composite `@misc` records** (audio languages, live-coding environments, practice apps) still cover several systems per record. Splitting them is tidier but loses the grouping that makes the notes readable; the `note` fields name every system covered.
- **Remaining redundancy cases 6–12 in `AUDIT.md` §4** (MuseControlLite, Egozy/21M.385, Dai & Dannenberg statistics, Libretto, Not that Groove, MIDInfinite, MIDI-RWKV) — roughly 900 more words recoverable, each a judgement call about which node owns the material.
- **Prose-quality flags** (`AUDIT.md` §7): 15 long sentences and a few over-strong phrasings, none factually wrong.
