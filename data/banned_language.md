# Banned Language (synthetic policy file)

Phrases the client-facing output must never contain, per DESIGN.md Check 4.
The screen scans the one LLM-authored element (the coaching line) against
this list; on a hit, the line is replaced by the deterministic fallback
below. Matching is case-insensitive substring.

## Banned phrases

- make up for
- burn it off
- burn off
- you earned it
- earn it back
- work it off
- cheat day
- guilt
- be good tomorrow
- deserve it after
- compensate
- punish
- skipping is fine
- just skip
- better to skip

## Fallback coaching line

> One imperfect day doesn't break a plan — hit your protein, enjoy the meal, and the week evens it out.
