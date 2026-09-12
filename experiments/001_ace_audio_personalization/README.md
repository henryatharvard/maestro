# 001 — ACE audio personalization

Question: Does adapting ACE-Step 1.5 to Henry's original piano, violin, and duet
performances improve useful musical output over the unmodified model? Does offline
human or AI preference training add value beyond SFT?

This experiment follows AI Kitchen's scoped configs, separate checkpoints, held-out
evaluation, and matched conditions. It uses ACE's audio/flow model, so the text-model
`SFTTrainer` and `GRPOTrainer` from Gandalf are **not** reused. The feedback stage is
an **experimental offline flow-DPO surrogate**, not PPO, GRPO, or a proven ACE recipe.
Human ranking is the primary feedback signal; CLAP ranking only tests prompt/audio
match and is a weak RLAIF baseline. Do not infer “musical quality” from its score.

## Open the work

- **Run the experiment:** [CLI and training guide](https://github.com/henryatharvard/maestro/tree/main/experiments/001_ace_audio_personalization), [training loop](https://github.com/henryatharvard/maestro/blob/main/experiments/001_ace_audio_personalization/src/maestro_ace/train.py), [frozen config](https://github.com/henryatharvard/maestro/blob/main/experiments/001_ace_audio_personalization/configs/piano_violin.toml).
- **Inspect the evidence:** [public results index](https://github.com/henryatharvard/maestro/blob/main/experiments/001_ace_audio_personalization/results/README.md), [September 12 synthetic smoke record](https://github.com/henryatharvard/maestro/blob/main/experiments/001_ace_audio_personalization/results/smoke-2026-09-12.md), and [two informal ACE Music Playground baselines](https://github.com/henryatharvard/maestro/blob/main/experiments/001_ace_audio_personalization/results/ace-music-playground-2026-09-12.md).
- **Prepare recordings:** [manifest example](https://github.com/henryatharvard/maestro/blob/main/experiments/001_ace_audio_personalization/examples/recordings.jsonl) and the [recording intake guide](#recording-intake). No real piano audio is public yet.
- **Understand ACE:** [ACE-Step 1.5 paper](https://arxiv.org/abs/2602.00744), [official interactive demo](https://huggingface.co/spaces/ACE-Step/Ace-Step-v1.5), and [upstream source](https://github.com/ace-step/ACE-Step-1.5).

## Layout

```text
configs/piano_violin.toml       frozen experiment settings
data/audio/                     your original WAV/FLAC recordings (ignored)
data/recordings.jsonl           your annotated recording manifest (ignored)
prompts/feedback.jsonl          prompts used to make preference candidates
prompts/eval.jsonl              frozen, separate evaluation prompts
artifacts/prepared/             validated split, staged audio, hashes (ignored)
artifacts/tensors/              ACE preprocessed tensors (ignored)
artifacts/checkpoints/          SFT, human, AI adapter branches (ignored)
artifacts/generations/          seeded feedback and evaluation audio (ignored)
artifacts/preferences/          ballots, pairs, AI scores (ignored)
artifacts/reports/              matched-seed listening index (ignored)
```

## Recording intake

Record original music as lossless WAV or FLAC, ideally 48 kHz stereo for piano
and duet, mono or stereo for violin. Keep aligned piano, violin, and duet exports
under one `composition_id`; they must all be in the same train/validation split.
Start with distinct 60–120 second pieces. The code accepts 10–180 seconds as
configured, rejects near-silent or clipped files, hashes exact audio bytes, and
does not quantize or normalize your recordings. Keep MIDI separately if captured;
ACE LoRA consumes audio, not MIDI. Example rows are in
`examples/recordings.jsonl`. Captions describe what is audible, not an artist name.
Set `provenance` to document authorship and the right to train on each take.

Copy the example rows into `data/recordings.jsonl`, update paths/captions, and
put the matching files under `data/audio/`. The example is a schema, not a real
dataset. At least two distinct compositions are required for a held-out split;
20–30 is a sensible pilot before claiming any style improvement. Once prepared,
the inputs and split are frozen under this experiment ID; changes require a new ID.

## Environment and checkpoints

Run from this directory. `uv` manages the experiment's own Python 3.12 environment.
The light environment supports intake without ACE or a GPU:

```bash
uv sync
uv run maestro-ace doctor
uv run maestro-ace prepare
```

To check that the entire pipeline is wired up before recordings or checkpoints
exist, run the synthetic CPU smoke test:

```bash
uv sync --extra smoke
uv run --extra smoke maestro-ace smoke
```

It creates a unique ignored `artifacts/smoke/run-*/` directory with synthetic
48 kHz audio, fake preprocessed tensors, a tiny trainable stand-in decoder,
one SFT step, human and AI preference branches, candidate files, and a
four-variant listening report. The AI smoke scorer uses audio energy, **not
CLAP**. The command prints the artifact path and fails on a broken stage.
This tests orchestration and real PyTorch loss/backprop/optimizer paths; it
does **not** load ACE weights, run ACE's preprocessor or generator, validate
adapter compatibility, or measure music quality.

On the Linux CUDA machine, install a **separate ACE checkout at the revision in
`configs/piano_violin.toml`**, and install it into this experiment environment:

```bash
git clone https://github.com/ace-step/ACE-Step-1.5.git /path/to/ACE-Step-1.5
git -C /path/to/ACE-Step-1.5 checkout ca1e85fe9430179831e6bc6be790c332190a3866
uv pip install -e /path/to/ACE-Step-1.5
ACE_ROOT=/path/to/ACE-Step-1.5
ACE_CKPT=/path/to/ACE-Step-1.5/checkpoints
```

ACE's package includes CUDA-specific PyTorch and model dependencies. Use ACE's
documented downloader to populate a checkpoint directory containing `vae/`,
`Qwen3-Embedding-0.6B/`, and the selected `acestep-v15-base/` DiT checkpoint.
After installation, download only the main bundle and base DiT:

```bash
.venv/bin/acestep-download --model main --dir "$ACE_CKPT"
.venv/bin/acestep-download --model acestep-v15-base --dir "$ACE_CKPT"
```

The pinned **base** model supports subsequent layer/extract/complete tasks for
Maestro Studio. To switch variants, edit the config and fetch the corresponding
checkpoint. The adapter belongs to the exact base variant and revision.

After `uv pip install -e`, call `.venv/bin/maestro-ace` directly so a fresh
`uv sync` does not remove the editable ACE install. Keep the path variables in
your shell for the commands below.

## Run the stages

```bash
.venv/bin/maestro-ace --ace-root "$ACE_ROOT" --checkpoints "$ACE_CKPT" preprocess
.venv/bin/maestro-ace --ace-root "$ACE_ROOT" --checkpoints "$ACE_CKPT" sft
.venv/bin/maestro-ace --ace-root "$ACE_ROOT" --checkpoints "$ACE_CKPT" generate --split feedback --model sft
```

SFT uses ACE's preprocessed tensors, DiT LoRA injection, continuous ACE timestep
sampling, flow-matching velocity loss and CFG dropout. It trains **exactly**
`sft.steps` optimizer steps, records metrics, saves interval/final adapters, and
compares seeded held-out flow loss before and after. Training never touches the
held-out composition's tensors.

For human feedback, listen to each two-seed pair in
`artifacts/generations/feedback/sft/`. Record a chosen and rejected ID, reviewer
and concrete reason in a private JSONL file like `examples/human_ballots.jsonl`.
The example ballot is illustrative; listen before using a real ballot.

```bash
.venv/bin/maestro-ace rank --source human --ballots /path/to/my-ballots.jsonl
.venv/bin/maestro-ace --ace-root "$ACE_ROOT" --checkpoints "$ACE_CKPT" preprocess-pairs --source human
.venv/bin/maestro-ace --ace-root "$ACE_ROOT" --checkpoints "$ACE_CKPT" preference --source human
```

For the separate AI-feedback branch, install the ML environment first and run
`.venv/bin/maestro-ace rank --source ai`. It uses a frozen CLAP model to compare candidates under the
same prompt; score margins below `judge.min_margin` are rejected. Then run
`preprocess-pairs --source ai` and `preference --source ai`. Both branches reload
the same SFT adapter and use a frozen copy of that adapter as reference.
No cross-branch continuation occurs.

For evaluation, generate the **same prompts and seeds** for the base model,
SFT adapter, and available feedback adapters, then build the listening index:

```bash
.venv/bin/maestro-ace --ace-root "$ACE_ROOT" --checkpoints "$ACE_CKPT" generate --split eval --model base
.venv/bin/maestro-ace --ace-root "$ACE_ROOT" --checkpoints "$ACE_CKPT" generate --split eval --model sft
.venv/bin/maestro-ace --ace-root "$ACE_ROOT" --checkpoints "$ACE_CKPT" generate --split eval --model human
.venv/bin/maestro-ace report
```

The report copies generated audio to anonymous take names and writes a separate
`artifacts/reports/answer_key.json`; keep the key closed until ratings are done.
Rate which take you would keep, phrasing, instrumentation, and artifacts.
A lower flow loss or higher CLAP score alone is not evidence of
better composition. Track copy/memorization concerns by comparing outputs with
the training recordings before sharing a model.

## Current verification boundary

The synthetic CPU smoke has run through every pipeline stage, including one
PyTorch optimizer step for SFT and for each preference branch. It passed in
September 2026. **No ACE weights, GPU training, CLAP inference, or listening
study has been run for this experiment yet.** Real model integration still
requires the pinned upstream checkout and checkpoint bundle on your RTX PRO
5000/C3 environment. The smoke command does not call a cloud API or upload
recordings.
