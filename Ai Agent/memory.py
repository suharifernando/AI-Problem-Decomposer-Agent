# memory.py
# Agent memory system — stores state across all stages of the pipeline

class AgentMemory:
    """
    Stores the agent's working memory across all three reasoning stages.
    Provides a simple key-value store with typed helper methods.
    """

    def __init__(self):
        self._store = {}

    # ── Core store operations ──────────────────────────────────────────────

    def save(self, key: str, value):
        """Store any value under a key."""
        self._store[key] = value

    def get(self, key: str, default=None):
        """Retrieve a value by key, with optional default."""
        return self._store.get(key, default)

    def clear(self):
        """Reset memory for a fresh run."""
        self._store = {}

    # ── Typed helpers ──────────────────────────────────────────────────────

    def set_problem(self, problem: str):
        self.save("problem", problem)

    def get_problem(self) -> str:
        return self.get("problem", "")

    def set_steps(self, steps: list[str]):
        self.save("steps", steps)
        self.save("steps_count", len(steps))

    def get_steps(self) -> list[str]:
        return self.get("steps", [])

    def set_critiques(self, critiques: list[str]):
        self.save("critiques", critiques)
        self.save("critiques_count", len(critiques))

    def get_critiques(self) -> list[str]:
        return self.get("critiques", [])

    def set_improved(self, improved: list[str]):
        self.save("improved", improved)
        self.save("improved_count", len(improved))

    def get_improved(self) -> list[str]:
        return self.get("improved", [])

    def set_phase(self, phase: str):
        self.save("phase", phase)

    def get_phase(self) -> str:
        return self.get("phase", "idle")

    # ── Display ────────────────────────────────────────────────────────────

    def summary(self) -> str:
        lines = ["🧠 Agent Memory State:"]
        for key, value in self._store.items():
            if isinstance(value, list):
                lines.append(f"  {key}: [{len(value)} items]")
            elif isinstance(value, str) and len(value) > 60:
                lines.append(f"  {key}: \"{value[:60]}...\"")
            else:
                lines.append(f"  {key}: {repr(value)}")
        return "\n".join(lines)
