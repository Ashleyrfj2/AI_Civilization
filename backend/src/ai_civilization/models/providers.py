"""AI provider adapter interfaces. External providers disabled by default.

Local-first: an Ollama-ready interface is included, but Phase 0 performs no
network calls and requires no API keys for tests or simulation startup.
"""

from __future__ import annotations

from typing import Protocol


class ModelProvider(Protocol):
    """Provider contract. Implementations must not mutate world state."""

    name: str

    def complete(self, prompt: str) -> str:
        """Return a model completion for the prompt."""
        ...


class NullProvider:
    """Safe default: deterministic echo, no network, no keys."""

    name = "none"

    def complete(self, prompt: str) -> str:
        """Echo a truncated prompt deterministically."""
        return f"[null-provider echo] {prompt[:120]}"


class OllamaProvider:
    """Ollama-ready stub. Phase 0 does not call the network."""

    name = "ollama"

    def __init__(self, host: str = "http://localhost:11434", model: str = "") -> None:
        self.host = host
        self.model = model

    def complete(self, prompt: str) -> str:
        """Not wired in Phase 0."""
        raise NotImplementedError("Ollama provider not wired in Phase 0.")
