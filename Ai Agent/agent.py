# agent.py
# Core AI agent — three-stage reasoning pipeline using Groq API

import os
from groq import Groq
from memory import AgentMemory
from prompts import DECOMPOSE_SYSTEM_PROMPT, CRITIQUE_SYSTEM_PROMPT, IMPROVE_SYSTEM_PROMPT


class ProblemDecomposerAgent:
    """
    A self-improving AI agent that:
      1. Decomposes a problem into steps      (Planning)
      2. Critiques its own steps              (Reflection)
      3. Produces an improved plan            (Goal-based improvement)

    This demonstrates: reasoning, memory, reflection, and goal-based action.
    """

    MODEL = "llama-3.3-70b-versatile"   # Fast, capable Groq model

    def __init__(self):
        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key:
            raise EnvironmentError(
                "GROQ_API_KEY not found. "
                "Add it to your .env file or export it in your shell."
            )
        self.client = Groq(api_key=api_key)
        self.memory = AgentMemory()

    # ── Private helpers ────────────────────────────────────────────────────

    def _call_llm(self, system_prompt: str, user_message: str) -> str:
        """Send a request to the Groq API and return the response text."""
        response = self.client.chat.completions.create(
            model=self.MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user",   "content": user_message},
            ],
            temperature=0.7,
            max_tokens=1024,
        )
        return response.choices[0].message.content.strip()

    def _parse_numbered_list(self, text: str) -> list[str]:
        """Extract items from a numbered list response."""
        items = []
        for line in text.splitlines():
            line = line.strip()
            if not line:
                continue
            # Match "1. item", "1) item", or "- item"
            for prefix in ["1234567890"]:
                if line[0].isdigit():
                    dot = line.find(".")
                    paren = line.find(")")
                    cut = min(
                        dot if dot > 0 else 9999,
                        paren if paren > 0 else 9999,
                    )
                    if cut < 5:
                        items.append(line[cut + 1:].strip())
                        break
                elif line.startswith("- ") or line.startswith("• "):
                    items.append(line[2:].strip())
                    break
            else:
                if len(line) > 10:
                    items.append(line)
        return items if items else [text.strip()]

    def _parse_bullet_list(self, text: str) -> list[str]:
        """Extract items from a bullet list response."""
        items = []
        for line in text.splitlines():
            line = line.strip()
            if not line:
                continue
            clean = line.lstrip("-•*123456789. ").strip()
            if len(clean) > 8:
                items.append(clean)
        return items if items else [text.strip()]

    # ── The three agent stages ─────────────────────────────────────────────

    def decompose(self, problem: str) -> list[str]:
        """Stage 1 — Plan: Break the problem into actionable steps."""
        print("\n🧩 [Stage 1] Decomposing problem into steps...")

        self.memory.clear()
        self.memory.set_problem(problem)
        self.memory.set_phase("decomposing")

        user_msg = f'Problem: "{problem}"\n\nDecompose this into steps:'
        raw = self._call_llm(DECOMPOSE_SYSTEM_PROMPT, user_msg)
        steps = self._parse_numbered_list(raw)

        self.memory.set_steps(steps)
        self.memory.set_phase("decomposed")
        return steps

    def critique(self) -> list[str]:
        """Stage 2 — Reflect: Critique the steps generated in Stage 1."""
        print("\n🔍 [Stage 2] Self-critiquing the plan...")

        problem = self.memory.get_problem()
        steps = self.memory.get_steps()

        if not steps:
            raise RuntimeError("No steps in memory. Run decompose() first.")

        self.memory.set_phase("critiquing")

        numbered = "\n".join(f"{i+1}. {s}" for i, s in enumerate(steps))
        user_msg = (
            f'Problem: "{problem}"\n\n'
            f"Plan:\n{numbered}\n\n"
            f"Critique this plan:"
        )
        raw = self._call_llm(CRITIQUE_SYSTEM_PROMPT, user_msg)
        critiques = self._parse_bullet_list(raw)

        self.memory.set_critiques(critiques)
        self.memory.set_phase("critiqued")
        return critiques

    def improve(self) -> list[str]:
        """Stage 3 — Improve: Generate a better plan addressing all critiques."""
        print("\n✨ [Stage 3] Generating improved plan...")

        problem   = self.memory.get_problem()
        steps     = self.memory.get_steps()
        critiques = self.memory.get_critiques()

        if not critiques:
            raise RuntimeError("No critiques in memory. Run critique() first.")

        self.memory.set_phase("improving")

        numbered  = "\n".join(f"{i+1}. {s}" for i, s in enumerate(steps))
        bulletted = "\n".join(f"- {c}" for c in critiques)
        user_msg  = (
            f'Problem: "{problem}"\n\n'
            f"Original Plan:\n{numbered}\n\n"
            f"Critiques:\n{bulletted}\n\n"
            f"Provide the improved plan:"
        )
        raw     = self._call_llm(IMPROVE_SYSTEM_PROMPT, user_msg)
        improved = self._parse_numbered_list(raw)

        self.memory.set_improved(improved)
        self.memory.set_phase("complete")
        return improved

    # ── Full pipeline ──────────────────────────────────────────────────────

    def run(self, problem: str) -> dict:
        """
        Execute all three stages sequentially and return the full result.

        Returns:
            {
                "problem":   str,
                "steps":     list[str],
                "critiques": list[str],
                "improved":  list[str],
            }
        """
        steps     = self.decompose(problem)
        critiques = self.critique()
        improved  = self.improve()

        return {
            "problem":   problem,
            "steps":     steps,
            "critiques": critiques,
            "improved":  improved,
        }
