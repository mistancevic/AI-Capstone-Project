"""Registered-but-stubbed domain agents (future work, per the PRD demo).

They appear in the agent registry so the demo can show the intended
architecture, but any attempt to route to them raises NotImplementedError —
requests in their domains escalate to the coach instead.
"""

from __future__ import annotations


class StubAgent:
    def __init__(self, name: str, domain: str):
        self.name = name
        self.domain = domain
        self.stub = True

    def handle(self, *_args, **_kwargs):
        raise NotImplementedError(
            f"{self.name} is registered but not implemented yet — "
            f"{self.domain} requests escalate to the coach."
        )


FITNESS = StubAgent("fitness", "training programming")
MOVEMENT = StubAgent("movement", "daily movement / NEAT")
RECOVERY = StubAgent("recovery", "recovery modalities")

STUB_AGENTS = [FITNESS, MOVEMENT, RECOVERY]
