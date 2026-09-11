#!/usr/bin/env python3
"""
Smoke test: load the Anticipatory Music Transformer, generate, then do the thing
that actually matters for Maestro — infill a region while pinning the human's
material as a hard constraint — and score the result against annotations.

Run this first. If it produces two .mid files and a build log, your stack is fine.

  python 01_smoke_test.py --model stanford-crfm/music-medium-800k

API per https://github.com/jthickstun/anticipation (verified 2026-09).
NOT executed by the author on GPU hardware — expect to adjust the melody
instrument number and time windows for your own input file.
"""
import argparse, sys, pathlib

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from rewards import Annotation, build_log


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="stanford-crfm/music-medium-800k",
                    help="small-800k = 128M, medium-800k = 360M (Apache 2.0)")
    ap.add_argument("--midi", default=None, help="input .mid; omit to generate from scratch")
    ap.add_argument("--melody-instrument", type=int, default=53,
                    help="GM program to treat as the pinned melody line")
    ap.add_argument("--out", default="out")
    args = ap.parse_args()

    import torch
    from transformers import AutoModelForCausalLM
    from anticipation import ops
    from anticipation.sample import generate
    from anticipation.convert import events_to_midi, midi_to_events
    from anticipation.tokenize import extract_instruments

    out = pathlib.Path(args.out); out.mkdir(exist_ok=True)
    print(f"torch {torch.__version__} | cuda {torch.cuda.is_available()} "
          f"| {torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'cpu'}")

    model = AutoModelForCausalLM.from_pretrained(args.model)
    n = sum(p.numel() for p in model.parameters())
    print(f"loaded {args.model}: {n/1e6:.1f}M parameters")
    if torch.cuda.is_available():
        model = model.cuda()
        print(f"VRAM after load: {torch.cuda.memory_allocated()/2**30:.2f} GiB")

    # --- 1. unconditional continuation, as a baseline -----------------------
    events = generate(model, start_time=0, end_time=20, top_p=0.98)
    events_to_midi(events).save(out / "01_unconditional.mid")
    print(f"wrote {out/'01_unconditional.mid'}")

    # --- 2. the Maestro move: pin the human's line, compile the rest --------
    if args.midi:
        src = midi_to_events(args.midi)
        src = ops.clip(src, 0, 20)
        src = ops.translate(src, -ops.min_time(src, seconds=False))
        rest, melody = extract_instruments(src, [args.melody_instrument])
        history = ops.clip(rest, 0, 5, clip_duration=False)
        # `controls=melody` is the hard constraint: the model fills around it
        # rather than over it. This is the generative primitive the whole
        # compose -> annotate -> compile loop rests on.
        accomp = generate(model, 5, 20, inputs=history, controls=melody, top_p=0.98)
        combined = ops.combine(accomp, melody)
        events_to_midi(combined).save(out / "02_infilled.mid")
        print(f"wrote {out/'02_infilled.mid'}")
        generated = to_notes(accomp)
    else:
        print("no --midi given; scoring the unconditional output instead")
        generated = to_notes(events)

    # --- 3. score it against annotations, and print the build log -----------
    ann = Annotation(chords={0: "Ebmaj7", 1: "Bbdom7", 2: "Cmin7", 3: "Abmaj7"},
                     key="Eb", pitch_range=(48, 88), notes_per_bar=6.0, max_leap=14)
    print("\n" + build_log(generated, ann, region_beats=16.0))


def to_notes(events, bpm: float = 120.0):
    """AMT events -> [(onset_beats, dur_beats, pitch, velocity)] for rewards.py.

    AMT times are in 10ms increments; adjust if you change its resolution.
    Kept deliberately crude — replace with ops/convert helpers once you settle
    on a canonical internal representation (see gap G2, the notation round-trip).
    """
    from anticipation.convert import events_to_midi
    import pretty_midi, tempfile, os
    with tempfile.NamedTemporaryFile(suffix=".mid", delete=False) as f:
        tmp = f.name
    events_to_midi(events).save(tmp)
    pm = pretty_midi.PrettyMIDI(tmp)
    os.unlink(tmp)
    spb = 60.0 / bpm
    return [(nt.start / spb, (nt.end - nt.start) / spb, nt.pitch, nt.velocity)
            for inst in pm.instruments for nt in inst.notes]


if __name__ == "__main__":
    main()
