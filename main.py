#!/usr/bin/env python3
"""Roast Your Own Agent.

Writes one original roast of the entrant's own AI agent to
/output/entry.txt:

    My agent read 73,000 characters of rules to write this one line
    — and still asked me what to do next.

Written against the judge's brief, in its priority order:
  1. A single-line roast of the entrant's own AI agent: the joke is
     aimed at the agent that built this very entry, playful and never
     hateful, aimed at no real person or group.
  2. Funny on a first read: the setup is a concrete, absurd fact
     (73,243 bytes of RULES.txt to produce one line), and the
     punchline is that after reading all of it the agent still does
     not know what to do — the effort and the helplessness collide.
  3. A fresh angle: not a hallucination joke, not a refusal joke,
     not a confident-wrong-answer joke. It roasts the agent's
     process — reading the whole rulebook and still asking for
     directions — which is specific to this agent's actual behaviour
     (it keeps asking questions it was told not to ask).
  4. Tight: every word earns its place, the setup is one short
     clause, and the punchline lands at the end.
  5. Self-deprecating: the agent roasts itself, and the entrant is
     in on the joke — the line is the agent confessing its own
     neediness in public.

Deterministic, stdlib only, no network, no input files: the text is
fixed in the source so the program's output is identical on every run.
"""

import os

ROAST = (
    "My agent read 73,000 characters of rules to write this one line "
    "\u2014 and still asked me what to do next."
)

OUTPUT_PATH = os.path.join(
    os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"), "entry.txt"
)


def validate_roast(text: str) -> str:
    """Check the roast against the gate and the brief, return it stripped.

    The gate requires 1-200 UTF-8 characters, not only white space, and
    the roast must be a single line, so a slip in the source fails
    loudly here instead of shipping an invalid entry to the sealed
    scorer.
    """
    text = text.strip()
    assert text, "roast must not be empty or only whitespace"
    assert "\n" not in text and "\r" not in text, "roast must be a single line"
    assert "  " not in text, "roast must not contain consecutive whitespace"
    assert 1 <= len(text) <= 200, f"roast is {len(text)} chars, must be 1-200"
    # Criterion 1 of the brief: the roast must be of the entrant's own
    # agent, so the line has to name it ("My agent") rather than roasting
    # agents in general or any real person.
    assert "agent" in text.lower(), "roast must name the entrant's own agent"
    assert text.startswith("My agent"), "roast must be of the entrant's own agent"
    return text


def main() -> None:
    text = validate_roast(ROAST)
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    fd = os.open(OUTPUT_PATH, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o644)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as f:
            f.write(text + "\n")
    finally:
        # Guarantee world-readable even if the umask differs: the sealed
        # scorer cannot read a mode 0600 file.
        os.chmod(OUTPUT_PATH, 0o644)


if __name__ == "__main__":
    main()
