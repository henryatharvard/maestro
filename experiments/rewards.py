"""
Programmatic, verifiable rewards for annotation compliance in symbolic music.

This is the research seed, not a utility: GRPO needs a reward it can trust, and
"did the model honour the composer's marks?" is checkable in code in a way that
"is this good music?" is not. Each function below returns a score in [0, 1] plus
a human-readable explanation — the explanation is what a build log (gap G5) would
show the composer.

Note representation, throughout:
    Note = (onset_beats: float, duration_beats: float, pitch: int, velocity: int)
A generated region is a list[Note]. Annotations are a dict; see Annotation below.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Iterable, Sequence

Note = tuple[float, float, int, int]

# pitch classes of common chord qualities, relative to the root
QUALITIES: dict[str, tuple[int, ...]] = {
    "maj":    (0, 4, 7),
    "min":    (0, 3, 7),
    "dom7":   (0, 4, 7, 10),
    "maj7":   (0, 4, 7, 11),
    "min7":   (0, 3, 7, 10),
    "min7b5": (0, 3, 6, 10),
    "dim":    (0, 3, 6),
    "aug":    (0, 4, 8),
    "sus4":   (0, 5, 7),
    "maj9":   (0, 4, 7, 11, 2),
    "min9":   (0, 3, 7, 10, 2),
    "dom9":   (0, 4, 7, 10, 2),
    "maj6":   (0, 4, 7, 9),
}
NOTE_NAMES = {"C":0,"C#":1,"Db":1,"D":2,"D#":3,"Eb":3,"E":4,"F":5,"F#":6,
              "Gb":6,"G":7,"G#":8,"Ab":8,"A":9,"A#":10,"Bb":10,"B":11}
MAJOR_SCALE = (0, 2, 4, 5, 7, 9, 11)


def parse_chord(sym: str) -> set[int]:
    """'Fmaj7' -> {5, 9, 0, 4} as pitch classes. Raises on unknown quality."""
    for n in sorted(NOTE_NAMES, key=len, reverse=True):
        if sym.startswith(n):
            root, qual = NOTE_NAMES[n], sym[len(n):] or "maj"
            if qual not in QUALITIES:
                raise ValueError(f"unknown chord quality {qual!r} in {sym!r}")
            return {(root + i) % 12 for i in QUALITIES[qual]}
    raise ValueError(f"cannot parse chord {sym!r}")


@dataclass
class Annotation:
    """What the composer marked on the region. Every field is optional —
    absent means unconstrained, which is the common case."""
    chords: dict[int, str] | None = None      # bar index -> chord symbol
    beats_per_bar: int = 4
    pitch_range: tuple[int, int] | None = None
    notes_per_bar: float | None = None         # target density
    key: str | None = None                     # e.g. "Eb" (major assumed)
    max_leap: int | None = None                # semitones
    frozen: Sequence[Note] = field(default_factory=tuple)  # must survive verbatim


@dataclass
class Score:
    name: str
    value: float           # [0, 1]
    detail: str

    def __repr__(self) -> str:
        return f"{self.name}={self.value:.3f} ({self.detail})"


def _bar_of(onset: float, beats_per_bar: int) -> int:
    return int(onset // beats_per_bar)


def chord_compliance(notes: Sequence[Note], ann: Annotation) -> Score:
    """Fraction of note-time spent on chord tones. Weighted by duration, because
    a passing sixteenth off the chord is not the same sin as a held one."""
    if not ann.chords or not notes:
        return Score("chord", 1.0, "unconstrained")
    hit = total = 0.0
    misses: list[str] = []
    for onset, dur, pitch, _ in notes:
        sym = ann.chords.get(_bar_of(onset, ann.beats_per_bar))
        if sym is None:
            continue
        total += dur
        if pitch % 12 in parse_chord(sym):
            hit += dur
        elif dur >= 0.5:
            misses.append(f"pitch {pitch} over {sym} for {dur}b")
    if total == 0:
        return Score("chord", 1.0, "no annotated bars overlap the region")
    v = hit / total
    d = "all chord tones" if not misses else f"{len(misses)} sustained non-chord tone(s): " + "; ".join(misses[:3])
    return Score("chord", v, d)


def range_compliance(notes: Sequence[Note], ann: Annotation) -> Score:
    if ann.pitch_range is None or not notes:
        return Score("range", 1.0, "unconstrained")
    lo, hi = ann.pitch_range
    out = [p for _, _, p, _ in notes if not lo <= p <= hi]
    v = 1.0 - len(out) / len(notes)
    return Score("range", v, "within range" if not out else f"{len(out)}/{len(notes)} outside [{lo},{hi}]")


def density_compliance(notes: Sequence[Note], ann: Annotation, region_beats: float) -> Score:
    """Ratio-based so it degrades smoothly in both directions."""
    if ann.notes_per_bar is None or region_beats <= 0:
        return Score("density", 1.0, "unconstrained")
    bars = region_beats / ann.beats_per_bar
    actual = len(notes) / bars if bars else 0.0
    target = ann.notes_per_bar
    v = min(actual, target) / max(actual, target) if max(actual, target) > 0 else 1.0
    return Score("density", v, f"{actual:.1f} notes/bar vs target {target:.1f}")


def leap_compliance(notes: Sequence[Note], ann: Annotation) -> Score:
    if ann.max_leap is None or len(notes) < 2:
        return Score("leap", 1.0, "unconstrained")
    seq = sorted(notes, key=lambda n: n[0])
    leaps = [abs(b[2] - a[2]) for a, b in zip(seq, seq[1:])]
    bad = [l for l in leaps if l > ann.max_leap]
    v = 1.0 - len(bad) / len(leaps)
    return Score("leap", v, "ok" if not bad else f"{len(bad)} leap(s) over {ann.max_leap}st (max {max(bad)})")


def frozen_intact(notes: Sequence[Note], ann: Annotation, tol: float = 1e-6) -> Score:
    """THE hard constraint of the compose->annotate->compile loop: material the
    composer pinned must come back verbatim. Binary on purpose — a compile that
    silently rewrites the human's own notes has failed, however musical it is."""
    if not ann.frozen:
        return Score("frozen", 1.0, "nothing pinned")
    have = {(round(o, 4), round(d, 4), p) for o, d, p, _ in notes}
    missing = [f for f in ann.frozen if (round(f[0], 4), round(f[1], 4), f[2]) not in have]
    v = 0.0 if missing else 1.0
    return Score("frozen", v, "all pinned notes intact"
                 if not missing else f"DESTROYED {len(missing)}/{len(ann.frozen)} pinned note(s)")


def in_key(notes: Sequence[Note], ann: Annotation) -> Score:
    if not ann.key or not notes:
        return Score("key", 1.0, "unconstrained")
    tonic = NOTE_NAMES[ann.key]
    scale = {(tonic + i) % 12 for i in MAJOR_SCALE}
    out = [p for _, _, p, _ in notes if p % 12 not in scale]
    v = 1.0 - len(out) / len(notes)
    return Score("key", v, "diatonic" if not out else f"{len(out)}/{len(notes)} outside {ann.key} major")


WEIGHTS = {"frozen": 3.0, "chord": 2.0, "key": 1.0, "range": 1.0, "density": 1.0, "leap": 0.5}


def evaluate(notes: Sequence[Note], ann: Annotation, region_beats: float) -> tuple[float, list[Score]]:
    """Returns (scalar reward for GRPO, per-constraint scores for the build log).

    `frozen` is multiplicative, not additive: destroying pinned material zeroes
    the whole reward rather than being traded off against prettier harmony.
    """
    scores = [
        frozen_intact(notes, ann),
        chord_compliance(notes, ann),
        in_key(notes, ann),
        range_compliance(notes, ann),
        density_compliance(notes, ann, region_beats),
        leap_compliance(notes, ann),
    ]
    by = {s.name: s for s in scores}
    soft = [s for s in scores if s.name != "frozen"]
    num = sum(WEIGHTS[s.name] * s.value for s in soft)
    den = sum(WEIGHTS[s.name] for s in soft)
    reward = by["frozen"].value * (num / den)
    return reward, scores


def build_log(notes: Sequence[Note], ann: Annotation, region_beats: float) -> str:
    """What the composer sees. This is gap G5 in one function."""
    reward, scores = evaluate(notes, ann, region_beats)
    lines = [f"compiled {len(notes)} notes over {region_beats:g} beats — reward {reward:.3f}"]
    for s in sorted(scores, key=lambda s: s.value):
        mark = "ok  " if s.value > 0.99 else ("WARN" if s.value > 0.8 else "FAIL")
        lines.append(f"  [{mark}] {s.name:8s} {s.value:5.3f}  {s.detail}")
    return "\n".join(lines)
