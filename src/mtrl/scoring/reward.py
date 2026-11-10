"""Reward: gate x (1 - MetricX-QE / 25). MetricX range is 0 (best) .. 25 (worst)."""


def reward(gate_ok: bool, metricx_qe: float) -> float:
    return float(gate_ok) * (1.0 - min(max(metricx_qe, 0.0), 25.0) / 25.0)
