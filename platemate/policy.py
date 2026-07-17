"""Read the pre-authored wording blocks and policy data files.

Every client-facing sentence on a safety path is authored in
data/safety_policy.md and read verbatim — the model never writes stop or
nudge wording (DESIGN.md: templated language on every path where a bad
sentence could do damage).
"""

from __future__ import annotations

import json
import re
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

_BLOCK_RE = re.compile(
    r"<!--\s*block:(?P<name>[a-z_]+)\s*-->\s*\n(?P<body>.*?)\n<!--\s*end\s*-->",
    re.S,
)


def _load_blocks(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    return {m.group("name"): m.group("body").strip() for m in _BLOCK_RE.finditer(text)}


_blocks_cache: dict[str, str] | None = None


def block(name: str, **fmt) -> str:
    """Return a pre-authored wording block, optionally formatted."""
    global _blocks_cache
    if _blocks_cache is None:
        _blocks_cache = _load_blocks(DATA_DIR / "safety_policy.md")
    text = _blocks_cache[name]
    return text.format(**fmt) if fmt else text


def tolerance() -> dict:
    """The compliance band as data (data/tolerance.json)."""
    return json.loads((DATA_DIR / "tolerance.json").read_text(encoding="utf-8"))


def banned_language() -> tuple[list[str], str]:
    """(banned phrases, deterministic fallback coaching line) from
    data/banned_language.md."""
    text = (DATA_DIR / "banned_language.md").read_text(encoding="utf-8")
    phrases: list[str] = []
    in_list = False
    fallback = ""
    for line in text.splitlines():
        if line.startswith("## Banned phrases"):
            in_list = True
            continue
        if line.startswith("## Fallback"):
            in_list = False
            continue
        if in_list and line.strip().startswith("- "):
            phrases.append(line.strip()[2:].strip().lower())
        if line.strip().startswith("> ") and not fallback:
            fallback = line.strip()[2:].strip()
    return phrases, fallback
