const fs = require("fs");
const {
  AlignmentType,
  BorderStyle,
  Document,
  Footer,
  HeadingLevel,
  LevelFormat,
  PageBreak,
  PageNumber,
  Packer,
  Paragraph,
  ShadingType,
  Table,
  TableCell,
  TableLayoutType,
  TableRow,
  TextRun,
  VerticalAlign,
  WidthType,
} = require("/private/tmp/maestro-docx-deps/node_modules/docx");

const OUTPUT = "research/AI-MUSIC-POSITIONING.docx";
const navy = "18324A";
const blue = "2E5D78";
const paleBlue = "EAF1F5";
const paleGold = "F5F0E4";
const gray = "5D6770";
const lightGray = "E1E5E8";
const white = "FFFFFF";

const noBorders = {
  top: { style: BorderStyle.NONE, size: 0, color: white },
  bottom: { style: BorderStyle.NONE, size: 0, color: white },
  left: { style: BorderStyle.NONE, size: 0, color: white },
  right: { style: BorderStyle.NONE, size: 0, color: white },
  insideHorizontal: { style: BorderStyle.NONE, size: 0, color: white },
  insideVertical: { style: BorderStyle.NONE, size: 0, color: white },
};

const thinBorders = {
  top: { style: BorderStyle.SINGLE, size: 4, color: lightGray },
  bottom: { style: BorderStyle.SINGLE, size: 4, color: lightGray },
  left: { style: BorderStyle.SINGLE, size: 4, color: lightGray },
  right: { style: BorderStyle.SINGLE, size: 4, color: lightGray },
  insideHorizontal: { style: BorderStyle.SINGLE, size: 4, color: lightGray },
  insideVertical: { style: BorderStyle.SINGLE, size: 4, color: lightGray },
};

function run(text, options = {}) {
  return new TextRun({ text, font: "Aptos", size: 18, color: "20272D", ...options });
}

function body(text, options = {}) {
  return new Paragraph({
    children: [run(text)],
    spacing: { after: 70, line: 210 },
    keepLines: true,
    ...options,
  });
}

function richBody(parts, options = {}) {
  return new Paragraph({
    children: parts.map((part) => typeof part === "string" ? run(part) : run(part.text, part)),
    spacing: { after: 70, line: 210 },
    keepLines: true,
    ...options,
  });
}

function heading(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_1,
    children: [run(text, { bold: true, size: 22, color: navy })],
    spacing: { before: 90, after: 45, line: 230 },
    keepNext: true,
    border: { bottom: { style: BorderStyle.SINGLE, size: 8, color: blue, space: 2 } },
  });
}

function small(text, options = {}) {
  return new Paragraph({
    children: [run(text, { size: 15, color: gray })],
    spacing: { after: 35, line: 180 },
    ...options,
  });
}

function cell(text, width, options = {}) {
  const {
    bold = false,
    color = "20272D",
    fill,
    align = AlignmentType.LEFT,
    size = 15,
  } = options;
  return new TableCell({
    width: { size: width, type: WidthType.DXA },
    verticalAlign: VerticalAlign.CENTER,
    margins: { top: 55, bottom: 55, left: 70, right: 70 },
    shading: fill ? { fill, type: ShadingType.CLEAR, color: "auto" } : undefined,
    children: [new Paragraph({
      alignment: align,
      children: [run(text, { bold, color, size })],
      spacing: { after: 0, line: 175 },
      keepLines: true,
    })],
  });
}

function table(headers, rows, widths, options = {}) {
  const header = new TableRow({
    tableHeader: true,
    children: headers.map((h, i) => cell(h, widths[i], { bold: true, color: white, fill: navy, size: 15 })),
  });
  const bodyRows = rows.map((row, rowIndex) => new TableRow({
    children: row.map((value, i) => cell(value, widths[i], {
      fill: rowIndex % 2 === 0 ? "F8FAFB" : white,
      bold: options.boldFirst && i === 0,
      align: options.centerColumns && options.centerColumns.includes(i) ? AlignmentType.CENTER : AlignmentType.LEFT,
      size: options.size || 15,
    })),
  }));
  return new Table({
    width: { size: widths.reduce((a, b) => a + b, 0), type: WidthType.DXA },
    columnWidths: widths,
    layout: TableLayoutType.FIXED,
    borders: thinBorders,
    rows: [header, ...bodyRows],
  });
}

function callout(text) {
  return new Table({
    width: { size: 11160, type: WidthType.DXA },
    columnWidths: [11160],
    layout: TableLayoutType.FIXED,
    borders: noBorders,
    rows: [new TableRow({ children: [new TableCell({
      width: { size: 11160, type: WidthType.DXA },
      margins: { top: 85, bottom: 85, left: 120, right: 120 },
      shading: { fill: paleGold, type: ShadingType.CLEAR, color: "auto" },
      children: [new Paragraph({
        children: [run(text, { bold: true, size: 19, color: navy })],
        spacing: { after: 0, line: 220 },
      })],
    })] })],
  });
}

const pageOne = [
  new Paragraph({
    children: [run("AI MUSIC GENERATION IN 2026", { bold: true, size: 32, color: navy })],
    spacing: { after: 15, line: 320 },
  }),
  new Paragraph({
    children: [run("Where value is moving in research, products, and startups", { size: 20, color: blue })],
    spacing: { after: 25, line: 230 },
  }),
  new Paragraph({
    children: [run("September 10, 2026  |  Henry Tan  |  Maestro", { size: 15, color: gray })],
    spacing: { after: 70, line: 180 },
    border: { bottom: { style: BorderStyle.SINGLE, size: 12, color: navy, space: 5 } },
  }),
  small("Scope assumption: 6–12 month thesis, limited model-training compute, and an eventual product for serious score-based composers, arrangers, educators, or production teams."),
  heading("Executive position"),
  body("The inherited analysis is directionally right about research and too broad about the market. Raw generation is now mature for ideation: leading systems create full songs, vocals, stems, MIDI, and real-time audio. Professional creation is not solved, because a pleasing output is different from a controllable, repeatable, rights-clear workflow."),
  body("The market has also moved beyond prompt-to-song. Suno v6 performs local language-directed edits while preserving surrounding material; Suno Studio 2.0 includes MIDI and generative chat; Udio Sessions supports timeline edits and saved takes; Moises generates context-aware stems in a collaborative studio [E1–E4]. The claim that editing was left untouched is no longer defensible at the audio and DAW layer."),
  callout("Build the control plane, not another generator: score-based instructions, executable checks, semantic diffs, reversible edits, and provenance."),
  heading("The state of the field"),
  table(
    ["Layer", "2026 state", "Solved enough", "Open problem"],
    [
      ["Full-song audio", "Mature for ideation", "Songs, vocals, local edits, multimodal prompts, real-time steering [E1, E5]", "Repeatability, multilevel structure, fine symbolic control, production consistency"],
      ["Symbolic generation", "Mature in scope", "Continuation, accompaniment, infilling with fixed notes [E6, E7]", "General instruction following across notation, form, instrumentation, and idiom"],
      ["Decompose and render", "Infrastructure", "Stems, bounded audio-to-MIDI, MIDI-driven voices and instruments [E3, E8]", "Polyphonic understanding, expressive intent, semantic interchange"],
      ["Editing and workflow", "Productizing fast", "Region edits, takes, MIDI clips, stems, DAW integration [E1–E4, E9]", "Constraint checking, semantic diffs, cross-tool provenance, score-native workflows"],
      ["Evaluation and governance", "Immature", "Better perceptual metrics and early AI-credit standards [E10, E11]", "Workflow benchmarks, calibrated reliance, attribution, edit lineage"],
    ],
    [1600, 1500, 3820, 4240],
    { boldFirst: true, size: 14 }
  ),
  small("Judgment: generation is becoming an embedded capability. The durable problem is governing how it participates in creative work.", { spacing: { before: 35, after: 30, line: 180 } }),
  heading("Five corrections to the inherited position"),
  table(
    ["Claim", "Critical revision"],
    [
      ["Generation is no longer the bottleneck", "True for ideation, false for professional delivery. Revision, consistency, control, and rights still bind."],
      ["Notation editors ship zero AI", "False as written. Sibelius has AI chord suggestions [E12]. Broad region generation with inspectable constraints remains open."],
      ["No commercial MIDI conditioning", "Too broad. AIVA accepts MIDI influence; Moises and Suno use MIDI in generative workflows [E2, E3, E13]. Enforceable score conditioning is the real gap."],
      ["A build log creates trust", "Potentially dangerous. Prose explanations can increase trust without correctness [E14]. Separate verified facts, estimates, and provenance."],
      ["Thin literature means startup opportunity", "It means novelty. A company also needs recurring pain, budget, distribution, and a compounding asset."],
    ],
    [3180, 7980],
    { boldFirst: true, size: 14 }
  ),
  heading("Opportunity map"),
  table(
    ["Opportunity", "Thesis fit", "Startup", "Judgment"],
    [
      ["Full-song foundation model", "Low", "Low", "Capital-, data-, licensing-, and distribution-intensive"],
      ["Generic AI DAW or stem copilot", "Medium", "Medium", "Real demand, but Suno, Udio, Moises, ACE Studio, and DAW integrations make it crowded"],
      ["Score-native auditable editing", "High", "Medium", "Strong research gap and feasible prototype; narrow market must be validated"],
      ["Evaluation and compliance", "High", "Medium-high B2B", "Potential value to vendors, labels, publishers, and schools; integration and sales are hard"],
      ["Music version control alone", "Medium", "Low", "Useful embedded capability, weak standalone product before workflow adoption"],
    ],
    [3050, 1350, 1820, 4940],
    { boldFirst: true, centerColumns: [1, 2], size: 14 }
  ),
  new Paragraph({ children: [new PageBreak()] }),
];

const pageTwo = [
  heading("Recommended thesis: auditable score editing"),
  richBody([
    { text: "Research question. ", bold: true, color: navy },
    "Does verifiable and contestable feedback improve musical task success, correction time, and calibrated reliance compared with a black-box infiller or a prose explanation?",
  ]),
  richBody([
    { text: "Artifact. ", bold: true, color: navy },
    "Use a frozen symbolic infiller. A musician selects a MusicXML or MEI region and chooses three or four bounded operations: reharmonize under a fixed melody, simplify rhythm, change density, or preserve a motif while replacing accompaniment. Return alternatives with hard-constraint test results, descriptive measurements, explicitly labeled uncertainty estimates, a semantic diff, and reversible provenance.",
  ]),
  richBody([
    { text: "Study. ", bold: true, color: navy },
    "Preregister a within-subject comparison of bare generation, generation plus prose rationale, and generation plus an evidence-backed inspector. Primary measures: violations, time to acceptable result, manual edit distance, undo or rejection, and whether reliance tracks correctness. Ownership, Creativity Support Index, and trust are secondary. Use a power analysis to set N.",
  ]),
  richBody([
    { text: "Novelty. ", bold: true, color: navy },
    "The contribution is the coupling of composer instructions, executable tests, contestability, and measured reliance. Transparency alone is no longer safe novelty: an unreviewed preprint already compares hidden, visible, and editable reasoning surfaces with musicians [E15].",
  ]),
  table(
    ["Timing", "Deliverable"],
    [
      ["Months 1–2", "Co-design bounded tasks; define benchmark; preregister study"],
      ["Months 3–5", "Build the smallest end-to-end system and deterministic constraint suite"],
      ["Months 6–8", "Pilot, remove unreliable claims, stabilize instrumentation"],
      ["Months 9–10", "Run the study and analyze behavioral plus subjective measures"],
      ["Months 11–12", "Release benchmark and code; write the paper"],
    ],
    [2050, 9110],
    { boldFirst: true, size: 14 }
  ),
  small("Six-month scope: omit generalized natural language and provenance export. Keep deterministic verification and the user study.", { spacing: { before: 35, after: 30, line: 180 } }),
  heading("Startup position"),
  callout("The audit and control layer for AI-assisted composition: every change is constrained, inspectable, reversible, and exportable."),
  body("Do not begin as another notation editor. Enter through MuseScore, MusicXML, or a DAW bridge. Start where revisions cost money: arranging and publishing teams, media-composition teams, or advanced music programs. The composer is the user; a team or institution is the more plausible buyer."),
  body("The moat is not model weights. It is the corpus of instructions, constraint failures, accepted corrections, and semantic diffs, plus integrations and trusted provenance. More real edits improve checks and ranking, reducing correction cost. Provenance also aligns with the Copyright Office's distinction between assistive human modification and prompt-only generation, and with emerging granular AI credits [E11, E16]. A log preserves process evidence; it does not guarantee copyright."),
  richBody([
    { text: "Kill tests. ", bold: true, color: navy },
    "Before calling this a company, confirm that target users perform the chosen revision tasks weekly, demonstrate at least 25 percent lower correction time without more violations, and find a buyer willing to pay for workflow or compliance rather than novelty. Failure still leaves a strong HCI or ISMIR thesis, but not a startup.",
  ]),
  small("Evidence IDs E1–E18, source links, grades, and caveats are in AI-MUSIC-POSITIONING-EVIDENCE.md.", {
    spacing: { before: 65, after: 0, line: 175 },
    border: { top: { style: BorderStyle.SINGLE, size: 6, color: lightGray, space: 4 } },
  }),
];

const doc = new Document({
  creator: "Henry Tan",
  title: "AI Music Generation in 2026: Where Value Is Moving",
  subject: "Research, product, and startup positioning",
  description: "A critical two-page positioning memo on AI music generation as of September 10, 2026.",
  styles: {
    default: {
      document: { run: { font: "Aptos", size: 18, color: "20272D" }, paragraph: { spacing: { after: 70, line: 210 } } },
    },
    paragraphStyles: [
      {
        id: "Heading1",
        name: "Heading 1",
        basedOn: "Normal",
        next: "Normal",
        quickFormat: true,
        run: { font: "Aptos Display", size: 22, bold: true, color: navy },
        paragraph: { spacing: { before: 90, after: 45 }, outlineLevel: 0 },
      },
    ],
  },
  numbering: {
    config: [{
      reference: "memo-bullets",
      levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 300, hanging: 150 } } } }],
    }],
  },
  sections: [{
    properties: {
      page: {
        size: { width: 12240, height: 15840 },
        margin: { top: 520, right: 540, bottom: 520, left: 540, header: 220, footer: 220 },
      },
    },
    footers: {
      default: new Footer({ children: [new Paragraph({
        alignment: AlignmentType.CENTER,
        children: [run("PAGE ", { size: 13, color: gray }), new TextRun({ children: [PageNumber.CURRENT], font: "Aptos", size: 13, color: gray })],
        spacing: { before: 0, after: 0 },
      })] }),
    },
    children: [...pageOne, ...pageTwo],
  }],
});

Packer.toBuffer(doc).then((buffer) => {
  fs.writeFileSync(OUTPUT, buffer);
  process.stdout.write(`${OUTPUT}\n`);
});
