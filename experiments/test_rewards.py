import sys; sys.path.insert(0,'/home/claude/experiments')
from rewards import Annotation, evaluate, build_log, parse_chord

print("parse_chord('Fmaj7') ->", sorted(parse_chord('Fmaj7')))
print("parse_chord('Bbmin9') ->", sorted(parse_chord('Bbmin9')))

pinned = [(0.0, 1.0, 63, 90), (1.0, 1.0, 65, 90)]          # composer's own motif
ann = Annotation(chords={0: "Ebmaj7", 1: "Bbdom7"}, key="Eb",
                 pitch_range=(55, 84), notes_per_bar=4.0, max_leap=12, frozen=pinned)

good = pinned + [(2.0,1.0,67,80),(3.0,1.0,70,80),
                 (4.0,1.0,70,80),(5.0,1.0,69,80),(6.0,1.0,65,80),(7.0,1.0,62,80)]
bad  = [(0.0,1.0,61,90),(1.0,2.0,73,80),(3.0,0.25,44,80),(3.25,0.25,96,80)]

for label, notes in [("HONOURS the annotations", good), ("IGNORES them", bad)]:
    print(f"\n--- {label}")
    print(build_log(notes, ann, region_beats=8.0))
r_good,_ = evaluate(good, ann, 8.0); r_bad,_ = evaluate(bad, ann, 8.0)
print(f"\nreward separation: good={r_good:.3f}  bad={r_bad:.3f}  (gap {r_good-r_bad:.3f})")
assert r_good > 0.85 and r_bad == 0.0, "reward must separate these two cases"
print("PASS")
