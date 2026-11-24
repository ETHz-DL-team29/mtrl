"""Pure budgeting, batching and selection helpers for the new R0."""
import math
import random


def next_group(examples, cursor, remaining, effective_batch, seed):
    """Deterministic example stream; whole targets only, never exceed budget."""
    if not examples or remaining < 1:
        return [], cursor
    selected = []
    epoch_cache = {}
    while len(selected) < effective_batch:
        epoch, offset = divmod(cursor, len(examples))
        if epoch not in epoch_cache:
            order = list(range(len(examples)))
            random.Random(seed + epoch).shuffle(order)
            epoch_cache[epoch] = order
        example = examples[epoch_cache[epoch][offset]]
        size = len(example['target'])
        if size > remaining:
            break
        selected.append(example)
        remaining -= size
        cursor += 1
    return selected, cursor


def lr_multiplier(tokens, schedule_budget):
    warmup = max(1, int(schedule_budget * .03))
    if tokens < warmup:
        return max(1, tokens) / warmup
    progress = min(1, (tokens - warmup) / max(1, schedule_budget - warmup))
    return .1 + .9 * .5 * (1 + math.cos(math.pi * progress))


def collate(examples, pad_id, device='cpu'):
    """Left padding puts every target end at the same position for tail logits."""
    import torch
    width = max(len(x['prompt']) + len(x['target']) for x in examples)
    target_width = max(len(x['target']) for x in examples)
    inputs, masks, labels = [], [], []
    for x in examples:
        full = x['prompt'] + x['target']
        pad = width - len(full)
        inputs.append([pad_id] * pad + full)
        masks.append([0] * pad + [1] * len(full))
        labels.append([-100] * (target_width - len(x['target'])) + x['target'])
    return {k: torch.tensor(v, dtype=torch.long, device=device) for k, v in
            [('input_ids', inputs), ('attention_mask', masks), ('labels', labels)]}


def selection_key(metrics):
    # Structural eligibility is necessary; semantics still require inspection.
    eligible = metrics['failure_rate'] <= .10 and metrics['wrong_language_rate'] <= .10
    return (int(eligible), metrics['chrfpp'], -metrics['nll'])
