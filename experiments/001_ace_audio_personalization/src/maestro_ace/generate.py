"""Matched-seed ACE audio generation for feedback and frozen evaluation."""

from __future__ import annotations

import os
import shutil
from pathlib import Path

from .config import Config
from .data import load_prompts
from .io import file_hash, write_jsonl


def generate(root: Path, ace_root: Path, checkpoint_dir: Path, cfg: Config,
             stage: str, adapter: Path | None, split: str, output: Path,
             *, renderer=None) -> list[dict]:

    prompts = load_prompts(root, cfg)[split]
    if renderer is None:
        from .ace import check_ace_checkout, check_checkpoint_dir

        check_ace_checkout(ace_root, cfg)
        check_checkpoint_dir(checkpoint_dir, cfg)
        from acestep.handler import AceStepHandler
        from acestep.inference import GenerationConfig, GenerationParams, generate_music

        os.environ["ACESTEP_CHECKPOINTS_DIR"] = str(checkpoint_dir.resolve())
        dit = AceStepHandler()
        status, success = dit.initialize_service(
            project_root=str(ace_root),
            config_path="acestep-v15-" + cfg.runtime.variant.replace("_", "-"),
            device=cfg.runtime.device)
        if not success:
            raise RuntimeError(f"ACE initialization failed: {status}")
        if adapter:
            message = dit.load_lora(str(adapter))
            if not message.startswith("✅"):
                raise RuntimeError(f"ACE adapter load failed: {message}")

        def renderer(prompt, seed, target):
            params = GenerationParams(task_type="text2music", caption=prompt["caption"],
                                      lyrics="[Instrumental]", instrumental=True,
                                      duration=prompt["duration"], bpm=prompt["bpm"],
                                      keyscale=prompt["keyscale"],
                                      timesignature=prompt["timesignature"],
                                      inference_steps=cfg.generation.inference_steps,
                                      guidance_scale=cfg.generation.guidance_scale,
                                      thinking=False, use_cot_metas=False, use_cot_caption=False,
                                      seed=seed)
            result = generate_music(dit, None, params,
                                    GenerationConfig(batch_size=1, use_random_seed=False,
                                                     seeds=[seed], audio_format="flac"),
                                    save_dir=str(output / "ace_raw"))
            if not result.success or len(result.audios) != 1:
                raise RuntimeError(f"ACE generation failed for {prompt['id']}-{seed}: {result.error}")
            src = Path(result.audios[0]["path"])
            if not src.is_file():
                raise FileNotFoundError(f"ACE reported missing output: {src}")
            shutil.copyfile(src, target)
    output.mkdir(parents=True, exist_ok=True)
    rows = []
    for prompt in prompts:
        for seed in cfg.generation.seeds:
            ident = f"{prompt['id']}-{seed}"
            target = output / f"{ident}.flac"
            if target.exists():
                raise FileExistsError(f"Refusing to overwrite generated audio: {target}")
            renderer(prompt, seed, target)
            if not target.is_file():
                raise FileNotFoundError(f"Renderer did not create audio: {target}")
            rows.append({"id": ident, "prompt_id": prompt["id"], "stage": stage,
                         "seed": seed, "audio_path": str(target.resolve()),
                         "sha256": file_hash(target), **{k: prompt[k] for k in
                           ("caption", "duration", "bpm", "keyscale", "timesignature")}})
            write_jsonl(output / "candidates.jsonl", rows)
    return rows
