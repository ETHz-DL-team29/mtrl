"""Loss masks for selective token updates (later stage; not implemented).

Three planned schemes, all over the Rollout's reasoning / translation split:
  1. translation-only: gradient on translation tokens only;
  2. translation + a random subset of reasoning tokens;
  3. translation + a scored subset of reasoning tokens.
Purpose: reduce B_back while keeping the GRPO signal.
"""
