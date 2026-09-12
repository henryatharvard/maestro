"""ACE-compatible flow-matching loss and an experimental offline preference objective."""

from __future__ import annotations

import torch
import torch.nn.functional as F


def sample_timesteps(batch_size: int, device, dtype, mu: float, sigma: float) -> torch.Tensor:
    """ACE v1.5 non-meanflow logit-normal t; in that mode r equals t."""
    first = torch.sigmoid(torch.randn(batch_size, device=device, dtype=dtype) * sigma + mu)
    second = torch.sigmoid(torch.randn(batch_size, device=device, dtype=dtype) * sigma + mu)
    return torch.maximum(first, second)


def flow_mse(model, batch: dict, *, t: torch.Tensor | None = None,
             noise: torch.Tensor | None = None, cfg_dropout: float = 0.0) -> torch.Tensor:
    """Per-example masked MSE for ACE's velocity target; same t/noise can be reused."""
    device = next(model.decoder.parameters()).device
    dtype = next(model.decoder.parameters()).dtype
    x0 = batch["target_latents"].to(device=device, dtype=dtype)
    mask = batch["attention_mask"].to(device=device, dtype=dtype)
    hidden = batch["encoder_hidden_states"].to(device=device, dtype=dtype)
    hidden_mask = batch["encoder_attention_mask"].to(device=device, dtype=dtype)
    context = batch["context_latents"].to(device=device, dtype=dtype)
    if t is None:
        t = sample_timesteps(x0.shape[0], device, dtype,
                             getattr(model.config, "timestep_mu", -0.4),
                             getattr(model.config, "timestep_sigma", 1.0))
    if noise is None:
        noise = torch.randn_like(x0)
    if cfg_dropout and hasattr(model, "null_condition_emb"):
        keep = (torch.rand(x0.shape[0], device=device) >= cfg_dropout)[:, None, None]
        hidden = torch.where(keep, hidden, model.null_condition_emb.expand_as(hidden))
    xt = t[:, None, None] * noise + (1 - t[:, None, None]) * x0
    prediction = model.decoder(
        hidden_states=xt, timestep=t, timestep_r=t, attention_mask=mask,
        encoder_hidden_states=hidden, encoder_attention_mask=hidden_mask,
        context_latents=context,
    )[0]
    squared = (prediction.float() - (noise - x0).float()).square()
    return (squared * mask.float()[:, :, None]).sum(dim=(1, 2)) / (
        mask.float().sum(dim=1).clamp_min(1) * squared.shape[-1])


def preference_objective(model, chosen: dict, rejected: dict, beta: float,
                         anchor: float) -> tuple[torch.Tensor, dict]:
    """Flow-DPO surrogate: reference-relative chosen/rejected velocity MSE gap.

    This is offline direct preference optimization, not an on-policy RL algorithm.
    Paired examples share timestep and per-position noise. The SFT adapter is the
    frozen reference via PEFT's disable_adapter(), so no second model is loaded.
    """
    device = next(model.decoder.parameters()).device
    dtype = next(model.decoder.parameters()).dtype
    t = sample_timesteps(1, device, dtype,
                         getattr(model.config, "timestep_mu", -0.4),
                         getattr(model.config, "timestep_sigma", 1.0))
    length = max(chosen["target_latents"].shape[1], rejected["target_latents"].shape[1])
    common_noise = torch.randn(1, length, chosen["target_latents"].shape[-1],
                               device=device, dtype=dtype)

    def loss_for(batch):
        n = batch["target_latents"].shape[1]
        return flow_mse(model, batch, t=t, noise=common_noise[:, :n])

    decoder = model.decoder
    decoder.set_adapter("reference")
    with torch.no_grad():
        ref_c = loss_for(chosen)
        ref_r = loss_for(rejected)
    decoder.set_adapter("default")
    for name, parameter in decoder.named_parameters():
        if "lora_" in name:
            parameter.requires_grad_(".default." in name)
    policy_c = loss_for(chosen)
    policy_r = loss_for(rejected)
    logit = beta * ((ref_c - policy_c) - (ref_r - policy_r))
    loss = -F.logsigmoid(logit).mean() + anchor * policy_c.mean()
    return loss, {"dpo": float((-F.logsigmoid(logit)).mean().detach()),
                  "chosen_mse": float(policy_c.mean().detach()),
                  "rejected_mse": float(policy_r.mean().detach())}
